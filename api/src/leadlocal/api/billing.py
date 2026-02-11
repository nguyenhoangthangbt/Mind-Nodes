"""Billing API routes — Stripe checkout, portal, webhooks."""

import stripe
from fastapi import APIRouter, Header, Request

from leadlocal.core.config import settings
from leadlocal.core.dependencies import CurrentUser, DBSession
from leadlocal.core.exceptions import AppException
from leadlocal.schemas.billing import (
    CheckoutResponse,
    CreateCheckoutRequest,
    PortalResponse,
    SubscriptionResponse,
    UsageResponse,
)
from leadlocal.services import billing_service

router = APIRouter(prefix="/billing", tags=["billing"])


@router.post("/checkout", response_model=CheckoutResponse)
async def create_checkout(data: CreateCheckoutRequest, user: CurrentUser):
    url = await billing_service.create_checkout_session(user, data.price_id)
    return CheckoutResponse(checkout_url=url)


@router.post("/portal", response_model=PortalResponse)
async def create_portal(user: CurrentUser):
    url = await billing_service.create_portal_session(user)
    return PortalResponse(portal_url=url)


@router.get("/subscription", response_model=SubscriptionResponse)
async def get_subscription(user: CurrentUser):
    return SubscriptionResponse(
        tier=user.tier,
        status=user.subscription.status if user.subscription else "none",
        current_period_end=(
            user.subscription.current_period_end if user.subscription else None
        ),
        cancel_at_period_end=(
            user.subscription.cancel_at_period_end if user.subscription else False
        ),
    )


@router.get("/usage", response_model=UsageResponse)
async def get_usage(user: CurrentUser, db: DBSession):
    from datetime import UTC, datetime

    from sqlalchemy import func, select

    from leadlocal.models.lead import Lead
    from leadlocal.models.search_log import SearchLog

    limits = settings.get_tier_limits(user.tier)

    leads_count = (
        await db.execute(select(func.count(Lead.id)).where(Lead.user_id == user.id))
    ).scalar() or 0

    month_start = datetime.now(UTC).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    searches_count = (
        await db.execute(
            select(func.count(SearchLog.id)).where(
                SearchLog.user_id == user.id, SearchLog.created_at >= month_start
            )
        )
    ).scalar() or 0

    return UsageResponse(
        tier=user.tier,
        leads_used=leads_count,
        leads_limit=limits["max_leads"],
        searches_used=searches_count,
        searches_limit=limits["max_searches"],
    )


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    db: DBSession,
    stripe_signature: str = Header(alias="stripe-signature"),
):
    if not settings.stripe_webhook_secret:
        raise AppException("Webhook secret not configured", 500)

    payload = await request.body()
    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, settings.stripe_webhook_secret
        )
    except stripe.SignatureVerificationError:
        raise AppException("Invalid webhook signature", 400)

    handlers = {
        "checkout.session.completed": billing_service.handle_checkout_completed,
        "invoice.payment_succeeded": billing_service.handle_invoice_paid,
        "invoice.payment_failed": billing_service.handle_invoice_failed,
        "customer.subscription.updated": billing_service.handle_subscription_updated,
        "customer.subscription.deleted": billing_service.handle_subscription_deleted,
    }

    handler = handlers.get(event["type"])
    if handler:
        await handler(db, event["data"])

    return {"status": "ok"}
