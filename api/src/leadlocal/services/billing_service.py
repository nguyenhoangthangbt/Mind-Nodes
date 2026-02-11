"""Stripe billing service — checkout, portal, webhook handling."""

import stripe
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from leadlocal.core.config import settings
from leadlocal.core.exceptions import AppException
from leadlocal.models.subscription import Subscription
from leadlocal.models.user import User

stripe.api_key = settings.stripe_secret_key

PRICE_TO_TIER = {
    settings.stripe_starter_monthly_price_id: "starter",
    settings.stripe_starter_annual_price_id: "starter",
    settings.stripe_pro_monthly_price_id: "pro",
    settings.stripe_pro_annual_price_id: "pro",
    settings.stripe_agency_monthly_price_id: "agency",
    settings.stripe_agency_annual_price_id: "agency",
}


async def create_checkout_session(user: User, price_id: str) -> str:
    if not settings.stripe_secret_key:
        raise AppException("Stripe is not configured", 500)

    customer_id = user.stripe_customer_id
    if not customer_id:
        customer = stripe.Customer.create(email=user.email, name=user.full_name)
        customer_id = customer.id

    session = stripe.checkout.Session.create(
        customer=customer_id,
        mode="subscription",
        line_items=[{"price": price_id, "quantity": 1}],
        success_url=f"{settings.app_url}/dashboard?checkout=success",
        cancel_url=f"{settings.app_url}/pricing?checkout=canceled",
        metadata={"user_id": str(user.id)},
    )
    return session.url


async def create_portal_session(user: User) -> str:
    if not user.stripe_customer_id:
        raise AppException("No billing account found")

    session = stripe.billing_portal.Session.create(
        customer=user.stripe_customer_id,
        return_url=f"{settings.app_url}/dashboard/settings",
    )
    return session.url


async def handle_checkout_completed(db: AsyncSession, event_data: dict) -> None:
    session = event_data["object"]
    user_id = session["metadata"]["user_id"]
    sub_id = session["subscription"]

    stripe_sub = stripe.Subscription.retrieve(sub_id)
    price_id = stripe_sub["items"]["data"][0]["price"]["id"]
    tier = PRICE_TO_TIER.get(price_id, "starter")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return

    user.stripe_customer_id = session["customer"]
    user.tier = tier

    sub = Subscription(
        user_id=user.id,
        stripe_subscription_id=sub_id,
        stripe_price_id=price_id,
        status=stripe_sub["status"],
        tier=tier,
        current_period_start=stripe_sub["current_period_start"],
        current_period_end=stripe_sub["current_period_end"],
    )
    db.add(sub)


async def handle_invoice_paid(db: AsyncSession, event_data: dict) -> None:
    invoice = event_data["object"]
    sub_id = invoice.get("subscription")
    if not sub_id:
        return

    result = await db.execute(
        select(Subscription).where(Subscription.stripe_subscription_id == sub_id)
    )
    sub = result.scalar_one_or_none()
    if sub:
        sub.status = "active"


async def handle_invoice_failed(db: AsyncSession, event_data: dict) -> None:
    invoice = event_data["object"]
    sub_id = invoice.get("subscription")
    if not sub_id:
        return

    result = await db.execute(
        select(Subscription).where(Subscription.stripe_subscription_id == sub_id)
    )
    sub = result.scalar_one_or_none()
    if sub:
        sub.status = "past_due"


async def handle_subscription_updated(db: AsyncSession, event_data: dict) -> None:
    stripe_sub = event_data["object"]
    sub_id = stripe_sub["id"]

    result = await db.execute(
        select(Subscription).where(Subscription.stripe_subscription_id == sub_id)
    )
    sub = result.scalar_one_or_none()
    if not sub:
        return

    price_id = stripe_sub["items"]["data"][0]["price"]["id"]
    sub.stripe_price_id = price_id
    sub.tier = PRICE_TO_TIER.get(price_id, sub.tier)
    sub.status = stripe_sub["status"]
    sub.cancel_at_period_end = stripe_sub.get("cancel_at_period_end", False)
    sub.current_period_end = stripe_sub["current_period_end"]

    # Sync tier to user
    user_result = await db.execute(select(User).where(User.id == sub.user_id))
    user = user_result.scalar_one_or_none()
    if user:
        user.tier = sub.tier


async def handle_subscription_deleted(db: AsyncSession, event_data: dict) -> None:
    stripe_sub = event_data["object"]
    sub_id = stripe_sub["id"]

    result = await db.execute(
        select(Subscription).where(Subscription.stripe_subscription_id == sub_id)
    )
    sub = result.scalar_one_or_none()
    if not sub:
        return

    sub.status = "canceled"

    user_result = await db.execute(select(User).where(User.id == sub.user_id))
    user = user_result.scalar_one_or_none()
    if user:
        user.tier = "free"
