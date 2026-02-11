"""Billing request/response schemas."""

from datetime import datetime

from pydantic import BaseModel


class CreateCheckoutRequest(BaseModel):
    price_id: str


class CheckoutResponse(BaseModel):
    checkout_url: str


class PortalResponse(BaseModel):
    portal_url: str


class SubscriptionResponse(BaseModel):
    tier: str
    status: str
    current_period_end: datetime | None = None
    cancel_at_period_end: bool = False

    model_config = {"from_attributes": True}


class UsageResponse(BaseModel):
    tier: str
    leads_used: int
    leads_limit: int
    searches_used: int
    searches_limit: int
