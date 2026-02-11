"""Unit tests for JWT token handling and password hashing."""

import pytest

from leadlocal.core.security import (
    create_access_token,
    create_magic_link_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)


class TestPasswordHashing:
    def test_hash_and_verify(self):
        plain = "mysecretpassword"
        hashed = hash_password(plain)
        assert hashed != plain
        assert verify_password(plain, hashed) is True

    def test_wrong_password(self):
        hashed = hash_password("correct")
        assert verify_password("wrong", hashed) is False

    def test_hash_is_unique(self):
        h1 = hash_password("same")
        h2 = hash_password("same")
        assert h1 != h2  # bcrypt uses random salt


class TestAccessToken:
    def test_create_and_decode(self):
        token = create_access_token("user-123")
        payload = decode_token(token)
        assert payload["sub"] == "user-123"
        assert payload["type"] == "access"

    def test_extra_claims(self):
        token = create_access_token("user-123", extra={"tier": "pro"})
        payload = decode_token(token)
        assert payload["tier"] == "pro"


class TestRefreshToken:
    def test_create_and_decode(self):
        token = create_refresh_token("user-456")
        payload = decode_token(token)
        assert payload["sub"] == "user-456"
        assert payload["type"] == "refresh"


class TestMagicLinkToken:
    def test_create_and_decode(self):
        token = create_magic_link_token("user@example.com")
        payload = decode_token(token)
        assert payload["sub"] == "user@example.com"
        assert payload["type"] == "magic"


class TestDecodeInvalidToken:
    def test_garbage_token(self):
        import jwt

        with pytest.raises(jwt.InvalidTokenError):
            decode_token("not-a-valid-token")
