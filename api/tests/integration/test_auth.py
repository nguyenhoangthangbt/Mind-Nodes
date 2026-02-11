"""Integration tests for auth API endpoints."""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from leadlocal.models.user import User


@pytest.mark.asyncio
async def test_signup_success(client: AsyncClient):
    resp = await client.post(
        "/api/v1/auth/signup",
        json={
            "email": "newuser@test.com",
            "password": "strongpassword123",
            "full_name": "New User",
            "company": "StartupCo",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_signup_duplicate_email(client: AsyncClient, test_user: User):
    resp = await client.post(
        "/api/v1/auth/signup",
        json={
            "email": test_user.email,
            "password": "anotherpassword",
            "full_name": "Duplicate",
        },
    )
    assert resp.status_code == 409


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, test_user: User):
    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "testpassword123"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, test_user: User):
    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "wrongpassword"},
    )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient):
    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "nobody@test.com", "password": "whatever"},
    )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_get_me(client: AsyncClient, test_user: User, auth_headers: dict):
    resp = await client.get("/api/v1/auth/me", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert data["tier"] == "free"


@pytest.mark.asyncio
async def test_get_me_no_token(client: AsyncClient):
    resp = await client.get("/api/v1/auth/me")
    assert resp.status_code == 422  # Missing required header


@pytest.mark.asyncio
async def test_refresh_token(client: AsyncClient, test_user: User):
    # First login to get tokens
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "testpassword123"},
    )
    refresh_token = login_resp.json()["refresh_token"]

    # Refresh
    resp = await client.post(
        "/api/v1/auth/refresh", json={"refresh_token": refresh_token}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data


@pytest.mark.asyncio
async def test_refresh_invalid_token(client: AsyncClient):
    resp = await client.post(
        "/api/v1/auth/refresh", json={"refresh_token": "invalid-token"}
    )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_magic_link_request(client: AsyncClient, test_user: User):
    resp = await client.post(
        "/api/v1/auth/magic-link", json={"email": "test@example.com"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "token" in data


@pytest.mark.asyncio
async def test_magic_link_verify(client: AsyncClient, test_user: User):
    # Request magic link
    ml_resp = await client.post(
        "/api/v1/auth/magic-link", json={"email": "test@example.com"}
    )
    token = ml_resp.json()["token"]

    # Verify
    resp = await client.post(
        "/api/v1/auth/magic-link/verify", json={"token": token}
    )
    assert resp.status_code == 200
    assert "access_token" in resp.json()
