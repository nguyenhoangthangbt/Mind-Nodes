"""Unit tests for application configuration."""

from leadlocal.core.config import Settings, settings


class TestConfig:
    def test_default_settings_exist(self):
        assert settings.app_name == "LeadLocal"
        assert settings.environment == "development"

    def test_tier_limits_free(self):
        limits = settings.get_tier_limits("free")
        assert limits["max_leads"] == 50
        assert limits["max_searches"] == 10

    def test_tier_limits_starter(self):
        limits = settings.get_tier_limits("starter")
        assert limits["max_leads"] == 500
        assert limits["max_searches"] == 75

    def test_tier_limits_pro(self):
        limits = settings.get_tier_limits("pro")
        assert limits["max_leads"] == 2500
        assert limits["max_searches"] == 300

    def test_tier_limits_agency(self):
        limits = settings.get_tier_limits("agency")
        assert limits["max_leads"] == 15000
        assert limits["max_searches"] == 999999

    def test_unknown_tier_defaults_to_free(self):
        limits = settings.get_tier_limits("unknown-tier")
        assert limits == settings.get_tier_limits("free")
