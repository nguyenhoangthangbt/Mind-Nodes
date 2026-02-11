"""Auth API routes — signup, login, magic link, token refresh."""

from fastapi import APIRouter

from leadlocal.core.dependencies import CurrentUser, DBSession
from leadlocal.schemas.auth import (
    LoginRequest,
    MagicLinkRequest,
    MagicLinkVerify,
    RefreshRequest,
    SignupRequest,
    TokenResponse,
    UserResponse,
)
from leadlocal.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=TokenResponse, status_code=201)
async def signup(data: SignupRequest, db: DBSession):
    _, tokens = await auth_service.signup(db, data)
    return tokens


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: DBSession):
    _, tokens = await auth_service.login(db, data.email, data.password)
    return tokens


@router.post("/magic-link")
async def request_magic_link(data: MagicLinkRequest, db: DBSession):
    token = await auth_service.magic_link_request(db, data.email)
    # In production, send this token via email instead of returning it
    return {"message": "Magic link sent", "token": token}


@router.post("/magic-link/verify", response_model=TokenResponse)
async def verify_magic_link(data: MagicLinkVerify, db: DBSession):
    _, tokens = await auth_service.magic_link_verify(db, data.token)
    return tokens


@router.post("/refresh", response_model=TokenResponse)
async def refresh(data: RefreshRequest, db: DBSession):
    return await auth_service.refresh_tokens(db, data.refresh_token)


@router.get("/me", response_model=UserResponse)
async def get_me(user: CurrentUser):
    return user
