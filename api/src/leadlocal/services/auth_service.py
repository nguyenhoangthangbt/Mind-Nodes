"""Authentication service — signup, login, magic link, token refresh."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from leadlocal.core.exceptions import AuthenticationError, ConflictError
from leadlocal.core.security import (
    create_access_token,
    create_magic_link_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from leadlocal.models.user import User
from leadlocal.schemas.auth import SignupRequest, TokenResponse


async def signup(db: AsyncSession, data: SignupRequest) -> tuple[User, TokenResponse]:
    existing = await db.execute(select(User).where(User.email == data.email))
    if existing.scalar_one_or_none():
        raise ConflictError("A user with this email already exists")

    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        full_name=data.full_name,
        company=data.company,
        tier="free",
        is_verified=False,
    )
    db.add(user)
    await db.flush()

    tokens = TokenResponse(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
    )
    return user, tokens


async def login(db: AsyncSession, email: str, password: str) -> tuple[User, TokenResponse]:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user or not user.password_hash or not verify_password(password, user.password_hash):
        raise AuthenticationError("Invalid email or password")

    tokens = TokenResponse(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
    )
    return user, tokens


async def magic_link_request(db: AsyncSession, email: str) -> str:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        raise AuthenticationError("No account found with this email")

    return create_magic_link_token(email)


async def magic_link_verify(db: AsyncSession, token: str) -> tuple[User, TokenResponse]:
    try:
        payload = decode_token(token)
        if payload.get("type") != "magic":
            raise AuthenticationError("Invalid magic link")
        email = payload["sub"]
    except Exception:
        raise AuthenticationError("Invalid or expired magic link")

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        raise AuthenticationError("User not found")

    if not user.is_verified:
        user.is_verified = True

    tokens = TokenResponse(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
    )
    return user, tokens


async def refresh_tokens(db: AsyncSession, refresh_token: str) -> TokenResponse:
    try:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise AuthenticationError("Invalid token type")
        user_id = payload["sub"]
    except Exception:
        raise AuthenticationError("Invalid or expired refresh token")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user or not user.is_active:
        raise AuthenticationError("User not found or deactivated")

    return TokenResponse(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
    )
