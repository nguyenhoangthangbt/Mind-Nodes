"""Integration tests for notes API endpoints."""

import pytest
from httpx import AsyncClient

from leadlocal.models.lead import Lead
from leadlocal.models.user import User


@pytest.mark.asyncio
async def test_create_note(
    client: AsyncClient, test_user: User, test_lead: Lead, auth_headers: dict
):
    resp = await client.post(
        f"/api/v1/leads/{test_lead.id}/notes",
        headers=auth_headers,
        json={"content": "Called and left a voicemail"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["content"] == "Called and left a voicemail"
    assert data["lead_id"] == str(test_lead.id)


@pytest.mark.asyncio
async def test_list_notes(
    client: AsyncClient, test_user: User, test_lead: Lead, auth_headers: dict
):
    # Create 2 notes
    await client.post(
        f"/api/v1/leads/{test_lead.id}/notes",
        headers=auth_headers,
        json={"content": "First call"},
    )
    await client.post(
        f"/api/v1/leads/{test_lead.id}/notes",
        headers=auth_headers,
        json={"content": "Second call"},
    )

    resp = await client.get(
        f"/api/v1/leads/{test_lead.id}/notes", headers=auth_headers
    )
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_update_note(
    client: AsyncClient, test_user: User, test_lead: Lead, auth_headers: dict
):
    # Create
    create_resp = await client.post(
        f"/api/v1/leads/{test_lead.id}/notes",
        headers=auth_headers,
        json={"content": "Original"},
    )
    note_id = create_resp.json()["id"]

    # Update
    resp = await client.patch(
        f"/api/v1/leads/{test_lead.id}/notes/{note_id}",
        headers=auth_headers,
        json={"content": "Updated content"},
    )
    assert resp.status_code == 200
    assert resp.json()["content"] == "Updated content"


@pytest.mark.asyncio
async def test_delete_note(
    client: AsyncClient, test_user: User, test_lead: Lead, auth_headers: dict
):
    create_resp = await client.post(
        f"/api/v1/leads/{test_lead.id}/notes",
        headers=auth_headers,
        json={"content": "To be deleted"},
    )
    note_id = create_resp.json()["id"]

    resp = await client.delete(
        f"/api/v1/leads/{test_lead.id}/notes/{note_id}", headers=auth_headers
    )
    assert resp.status_code == 204
