"""Unit tests for custom exceptions."""

from leadlocal.core.exceptions import (
    AppException,
    AuthenticationError,
    ConflictError,
    ExternalAPIError,
    ForbiddenError,
    NotFoundError,
    TierLimitError,
)


class TestExceptions:
    def test_not_found(self):
        err = NotFoundError("Lead")
        assert err.status_code == 404
        assert "Lead" in err.detail

    def test_auth_error(self):
        err = AuthenticationError()
        assert err.status_code == 401

    def test_forbidden_error(self):
        err = ForbiddenError()
        assert err.status_code == 403

    def test_tier_limit(self):
        err = TierLimitError("leads")
        assert err.status_code == 402
        assert "leads" in err.detail
        assert "upgrade" in err.detail.lower()

    def test_conflict_error(self):
        err = ConflictError("Email taken")
        assert err.status_code == 409
        assert "Email taken" in err.detail

    def test_external_api_error(self):
        err = ExternalAPIError("Google Places", "timeout")
        assert err.status_code == 502
        assert "Google Places" in err.detail
        assert "timeout" in err.detail

    def test_external_api_error_no_detail(self):
        err = ExternalAPIError("Yelp")
        assert "Yelp API error" in err.detail
