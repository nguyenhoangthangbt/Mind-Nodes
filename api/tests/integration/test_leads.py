"""Integration tests for leads CRUD API endpoints."""

import pytest
from httpx import AsyncClient

from leadlocal.models.lead import Lead
from leadlocal.models.user import User


@pytest.mark.asyncio
async def test_create_lead(client: AsyncClient, test_user: User, auth_headers: dict):
    resp = await client.post(
        "/api/v1/leads",
        headers=auth_headers,
        json={
            "business_name": "Test Restaurant",
            "address": "456 Oak Ave",
            "phone": "+1-555-0200",
            "category": "Restaurant",
            "rating": 4.2,
            "pipeline_stage": "new",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["business_name"] == "Test Restaurant"
    assert data["pipeline_stage"] == "new"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_lead_minimal(client: AsyncClient, test_user: User, auth_headers: dict):
    resp = await client.post(
        "/api/v1/leads",
        headers=auth_headers,
        json={"business_name": "Minimal Lead"},
    )
    assert resp.status_code == 201
    assert resp.json()["source"] == "manual"


@pytest.mark.asyncio
async def test_list_leads_empty(client: AsyncClient, test_user: User, auth_headers: dict):
    resp = await client.get("/api/v1/leads", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["items"] == []
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_list_leads_with_data(
    client: AsyncClient, test_user: User, test_lead: Lead, auth_headers: dict
):
    resp = await client.get("/api/v1/leads", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["business_name"] == "Joe's Pizza"


@pytest.mark.asyncio
async def test_list_leads_filter_by_stage(
    client: AsyncClient, test_user: User, test_lead: Lead, auth_headers: dict
):
    resp = await client.get(
        "/api/v1/leads?pipeline_stage=new", headers=auth_headers
    )
    assert resp.status_code == 200
    assert resp.json()["total"] == 1

    resp = await client.get(
        "/api/v1/leads?pipeline_stage=won", headers=auth_headers
    )
    assert resp.json()["total"] == 0


@pytest.mark.asyncio
async def test_list_leads_search(
    client: AsyncClient, test_user: User, test_lead: Lead, auth_headers: dict
):
    resp = await client.get("/api/v1/leads?search=pizza", headers=auth_headers)
    assert resp.json()["total"] == 1

    resp = await client.get("/api/v1/leads?search=nonexistent", headers=auth_headers)
    assert resp.json()["total"] == 0


@pytest.mark.asyncio
async def test_list_leads_sort_by_rating(
    client: AsyncClient, test_user: User, auth_headers: dict
):
    # Create multiple leads with different ratings
    for name, rating in [("A", 3.0), ("B", 5.0), ("C", 1.0)]:
        await client.post(
            "/api/v1/leads",
            headers=auth_headers,
            json={"business_name": name, "rating": rating},
        )

    resp = await client.get(
        "/api/v1/leads?sort_by=rating&sort_dir=desc", headers=auth_headers
    )
    items = resp.json()["items"]
    ratings = [i["rating"] for i in items if i["rating"] is not None]
    assert ratings == sorted(ratings, reverse=True)


@pytest.mark.asyncio
async def test_list_leads_filter_has_email(
    client: AsyncClient, test_user: User, test_lead: Lead, auth_headers: dict
):
    resp = await client.get("/api/v1/leads?has_email=true", headers=auth_headers)
    assert resp.json()["total"] == 1

    resp = await client.get("/api/v1/leads?has_email=false", headers=auth_headers)
    assert resp.json()["total"] == 0


@pytest.mark.asyncio
async def test_list_leads_filter_min_rating(
    client: AsyncClient, test_user: User, test_lead: Lead, auth_headers: dict
):
    resp = await client.get("/api/v1/leads?min_rating=4.0", headers=auth_headers)
    assert resp.json()["total"] == 1

    resp = await client.get("/api/v1/leads?min_rating=5.0", headers=auth_headers)
    assert resp.json()["total"] == 0


@pytest.mark.asyncio
async def test_get_lead(
    client: AsyncClient, test_user: User, test_lead: Lead, auth_headers: dict
):
    resp = await client.get(f"/api/v1/leads/{test_lead.id}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["business_name"] == "Joe's Pizza"


@pytest.mark.asyncio
async def test_get_lead_not_found(client: AsyncClient, test_user: User, auth_headers: dict):
    import uuid

    resp = await client.get(f"/api/v1/leads/{uuid.uuid4()}", headers=auth_headers)
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_update_lead(
    client: AsyncClient, test_user: User, test_lead: Lead, auth_headers: dict
):
    resp = await client.patch(
        f"/api/v1/leads/{test_lead.id}",
        headers=auth_headers,
        json={"pipeline_stage": "contacted", "contact_name": "Joe"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["pipeline_stage"] == "contacted"
    assert data["contact_name"] == "Joe"


@pytest.mark.asyncio
async def test_delete_lead(
    client: AsyncClient, test_user: User, test_lead: Lead, auth_headers: dict
):
    resp = await client.delete(f"/api/v1/leads/{test_lead.id}", headers=auth_headers)
    assert resp.status_code == 204

    # Verify it's gone
    resp = await client.get(f"/api/v1/leads/{test_lead.id}", headers=auth_headers)
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_pipeline_stats(
    client: AsyncClient, test_user: User, test_lead: Lead, auth_headers: dict
):
    resp = await client.get("/api/v1/leads/pipeline", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["new"] == 1
    assert data["won"] == 0


@pytest.mark.asyncio
async def test_analytics(
    client: AsyncClient, test_user: User, test_lead: Lead, auth_headers: dict
):
    resp = await client.get("/api/v1/leads/analytics", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_leads"] == 1
    assert data["with_email_count"] == 1
    assert data["with_phone_count"] == 1
    assert data["conversion_rate"] == 0.0
    assert len(data["by_source"]) >= 1


@pytest.mark.asyncio
async def test_export_csv(
    client: AsyncClient, test_user: User, test_lead: Lead, auth_headers: dict
):
    resp = await client.get("/api/v1/leads/export", headers=auth_headers)
    assert resp.status_code == 200
    assert "text/csv" in resp.headers["content-type"]
    lines = resp.text.strip().split("\n")
    assert len(lines) == 2  # header + 1 lead
    assert "Joe's Pizza" in lines[1]


@pytest.mark.asyncio
async def test_leads_pagination(
    client: AsyncClient, test_user: User, auth_headers: dict
):
    # Create 5 leads
    for i in range(5):
        await client.post(
            "/api/v1/leads",
            headers=auth_headers,
            json={"business_name": f"Biz {i}"},
        )

    resp = await client.get(
        "/api/v1/leads?page=1&per_page=2", headers=auth_headers
    )
    data = resp.json()
    assert data["total"] == 5
    assert len(data["items"]) == 2
    assert data["page"] == 1
    assert data["per_page"] == 2

    # Page 3 should have 1 item
    resp = await client.get(
        "/api/v1/leads?page=3&per_page=2", headers=auth_headers
    )
    assert len(resp.json()["items"]) == 1


@pytest.mark.asyncio
async def test_unauthorized_access(client: AsyncClient):
    resp = await client.get("/api/v1/leads", headers={"Authorization": "Bearer invalid"})
    assert resp.status_code == 401
