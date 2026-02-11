"""FastAPI application factory."""

import logging

import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from leadlocal.api import auth, billing, leads, notes, reminders, search
from leadlocal.core.config import settings
from leadlocal.core.middleware import register_middleware

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
)


def create_app() -> FastAPI:
    # Sentry error tracking (optional — only active if DSN configured)
    if settings.sentry_dsn:
        sentry_sdk.init(
            dsn=settings.sentry_dsn,
            traces_sample_rate=0.1,
            environment=settings.environment,
        )

    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="Local business lead discovery + mini CRM",
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.app_url],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Custom middleware (rate limiting, security headers, logging)
    register_middleware(app)

    # Routes
    app.include_router(auth.router, prefix="/api/v1")
    app.include_router(search.router, prefix="/api/v1")
    app.include_router(leads.router, prefix="/api/v1")
    app.include_router(notes.router, prefix="/api/v1")
    app.include_router(reminders.router, prefix="/api/v1")
    app.include_router(billing.router, prefix="/api/v1")

    @app.get("/health")
    async def health():
        return {"status": "ok", "version": "0.1.0", "env": settings.environment}

    return app


app = create_app()
