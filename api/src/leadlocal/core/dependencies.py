"""FastAPI dependency injection helpers."""

from typing import Annotated

import jwt
from fastapi import Depends, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from leadlocal.core.config import settings
from leadlocal.core.database import get_db
from leadlocal.core.exceptions import AuthenticationError, ForbiddenError, TierLimitError
from leadlocal.models.user import User

DBSession = Annotated[AsyncSession, Depends(get_db)]


async def get_current_user(
    db: DBSession,
    authorization: str = Header(...),
) -> User:
    if not authorization.startswith("Bearer "):
        raise AuthenticationError("Missing Bearer token")
    token = authorization.removeprefix("Bearer ")
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        if payload.get("type") != "access":
            raise AuthenticationError("Invalid token type")
        user_id = payload["sub"]
    except jwt.ExpiredSignatureError:
        raise AuthenticationError("Token expired")
    except jwt.InvalidTokenError:
        raise AuthenticationError("Invalid token")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise AuthenticationError("User not found")
    if not user.is_active:
        raise ForbiddenError("Account is deactivated")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def require_tier(min_tier: str):
    tier_order = {"free": 0, "starter": 1, "pro": 2, "agency": 3}

    async def _check(user: CurrentUser) -> User:
        user_level = tier_order.get(user.tier, 0)
        required_level = tier_order.get(min_tier, 0)
        if user_level < required_level:
            raise TierLimitError("features")
        return user

    return _check


async def check_lead_limit(user: CurrentUser, db: DBSession) -> User:
    from leadlocal.models.lead import Lead

    limits = settings.get_tier_limits(user.tier)
    result = await db.execute(
        select(Lead).where(Lead.user_id == user.id).limit(limits["max_leads"] + 1)
    )
    count = len(result.scalars().all())
    if count >= limits["max_leads"]:
        raise TierLimitError("leads")
    return user
