"""Integration tests for reminders API endpoints."""

import pytest
from httpx import AsyncClient

from leadlocal.models.lead import Lead
from leadlocal.models.user import User


@pytest.mark.asyncio
async def test_create_reminder(
    client: AsyncClient, test_user: User, test_lead: Lead, auth_headers: dict
):
    resp = await client.post(
        f"/api/v1/leads/{test_lead.id}/reminders",
        headers=auth_headers,
        json={
            "title": "Follow up call",
            "description": "Ask about catering order",
            "due_at": "2025-04-01T10:00:00Z",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Follow up call"
    assert data["is_completed"] is False


@pytest.mark.asyncio
async def test_list_reminders_for_lead(
    client: AsyncClient, test_user: User, test_lead: Lead, auth_headers: dict
):
    await client.post(
        f"/api/v1/leads/{test_lead.id}/reminders",
        headers=auth_headers,
        json={"title": "Reminder 1", "due_at": "2025-04-01T10:00:00Z"},
    )
    await client.post(
        f"/api/v1/leads/{test_lead.id}/reminders",
        headers=auth_headers,
        json={"title": "Reminder 2", "due_at": "2025-04-02T10:00:00Z"},
    )

    resp = await client.get(
        f"/api/v1/leads/{test_lead.id}/reminders", headers=auth_headers
    )
    assert resp.status_code == 200
    assert len(resp.json()) == 2


@pytest.mark.asyncio
async def test_list_all_reminders(
    client: AsyncClient, test_user: User, test_lead: Lead, auth_headers: dict
):
    await client.post(
        f"/api/v1/leads/{test_lead.id}/reminders",
        headers=auth_headers,
        json={"title": "Global reminder", "due_at": "2025-05-01T10:00:00Z"},
    )

    resp = await client.get("/api/v1/reminders", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


@pytest.mark.asyncio
async def test_complete_reminder(
    client: AsyncClient, test_user: User, test_lead: Lead, auth_headers: dict
):
    create_resp = await client.post(
        f"/api/v1/leads/{test_lead.id}/reminders",
        headers=auth_headers,
        json={"title": "To complete", "due_at": "2025-04-01T10:00:00Z"},
    )
    reminder_id = create_resp.json()["id"]

    resp = await client.patch(
        f"/api/v1/reminders/{reminder_id}",
        headers=auth_headers,
        json={"is_completed": True},
    )
    assert resp.status_code == 200
    assert resp.json()["is_completed"] is True


@pytest.mark.asyncio
async def test_delete_reminder(
    client: AsyncClient, test_user: User, test_lead: Lead, auth_headers: dict
):
    create_resp = await client.post(
        f"/api/v1/leads/{test_lead.id}/reminders",
        headers=auth_headers,
        json={"title": "To delete", "due_at": "2025-04-01T10:00:00Z"},
    )
    reminder_id = create_resp.json()["id"]

    resp = await client.delete(
        f"/api/v1/reminders/{reminder_id}", headers=auth_headers
    )
    assert resp.status_code == 204
