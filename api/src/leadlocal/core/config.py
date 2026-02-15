"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # App
    app_name: str = "LeadLocal"
    app_url: str = "http://localhost:3000"
    api_url: str = "http://localhost:8000"
    environment: str = "development"  # development, staging, production
    debug: bool = False

    # Database
    database_url: str = "postgresql+asyncpg://leadlocal:localdev@localhost:5432/leadlocal"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Auth
    jwt_secret_key: str = "change-me-to-random-64-char-string"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 15
    jwt_refresh_token_expire_days: int = 7
    magic_link_expire_minutes: int = 15

    # Google Places API
    google_places_api_key: str = ""

    # Yelp (optional)
    yelp_api_key: str = ""

    # Foursquare (optional)
    foursquare_api_key: str = ""

    # Hunter.io (optional)
    hunter_api_key: str = ""

    # Stripe
    stripe_secret_key: str = ""
    stripe_publishable_key: str = ""
    stripe_webhook_secret: str = ""
    stripe_starter_monthly_price_id: str = ""
    stripe_starter_annual_price_id: str = ""
    stripe_pro_monthly_price_id: str = ""
    stripe_pro_annual_price_id: str = ""
    stripe_agency_monthly_price_id: str = ""
    stripe_agency_annual_price_id: str = ""

    # Email (Resend)
    resend_api_key: str = ""
    from_email: str = "hello@leadlocal.io"

    # Sentry (optional)
    sentry_dsn: str = ""

    # Tier limits (revised per market research — docs/market-research.md §6.4)
    free_max_leads: int = 50
    free_max_searches: int = 10
    starter_max_leads: int = 500
    starter_max_searches: int = 75
    pro_max_leads: int = 2500
    pro_max_searches: int = 300
    agency_max_leads: int = 15000
    agency_max_searches: int = 999999  # effectively unlimited

    def get_tier_limits(self, tier: str) -> dict[str, int]:
        limits = {
            "free": {"max_leads": self.free_max_leads, "max_searches": self.free_max_searches},
            "starter": {
                "max_leads": self.starter_max_leads,
                "max_searches": self.starter_max_searches,
            },
            "pro": {"max_leads": self.pro_max_leads, "max_searches": self.pro_max_searches},
            "agency": {
                "max_leads": self.agency_max_leads,
                "max_searches": self.agency_max_searches,
            },
        }
        return limits.get(tier, limits["free"])


settings = Settings()
