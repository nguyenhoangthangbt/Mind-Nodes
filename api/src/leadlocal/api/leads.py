"""Leads CRUD API routes with advanced filtering, sorting, and analytics."""

import csv
import io
import uuid
from datetime import datetime

from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from leadlocal.core.dependencies import CurrentUser, DBSession
from leadlocal.schemas.lead import (
    LeadAnalytics,
    LeadCreate,
    LeadExportRow,
    LeadListResponse,
    LeadResponse,
    LeadUpdate,
    PipelineStats,
    TagCreate,
    TagResponse,
)
from leadlocal.services import lead_service

router = APIRouter(prefix="/leads", tags=["leads"])


@router.post("", response_model=LeadResponse, status_code=201)
async def create_lead(data: LeadCreate, user: CurrentUser, db: DBSession):
    lead = await lead_service.create_lead(db, user, data)
    return lead


@router.get("", response_model=LeadListResponse)
async def list_leads(
    user: CurrentUser,
    db: DBSession,
    page: int = Query(1, ge=1),
    per_page: int = Query(25, ge=1, le=100),
    # Filter params
    pipeline_stage: str | None = Query(None, description="Comma-separated stages: new,contacted,responded,meeting,proposal,won,lost"),
    search: str | None = Query(None, description="Full-text search across name, address, category, contact"),
    tag_id: uuid.UUID | None = None,
    category: str | None = Query(None, description="Filter by business category"),
    source: str | None = Query(None, description="Filter by source: google_places, yelp, foursquare, manual"),
    has_email: bool | None = Query(None, description="Filter leads with/without email"),
    has_phone: bool | None = Query(None, description="Filter leads with/without phone"),
    has_website: bool | None = Query(None, description="Filter leads with/without website"),
    min_rating: float | None = Query(None, ge=0, le=5, description="Minimum Google rating"),
    max_rating: float | None = Query(None, ge=0, le=5, description="Maximum Google rating"),
    created_after: datetime | None = Query(None, description="Filter leads created after this date"),
    created_before: datetime | None = Query(None, description="Filter leads created before this date"),
    # Sort params
    sort_by: str = Query("created_at", description="Sort column: business_name, category, rating, review_count, pipeline_stage, source, created_at, updated_at"),
    sort_dir: str = Query("desc", description="Sort direction: asc or desc"),
):
    return await lead_service.list_leads(
        db, user,
        page=page, per_page=per_page,
        pipeline_stage=pipeline_stage, search=search, tag_id=tag_id,
        category=category, source=source,
        has_email=has_email, has_phone=has_phone, has_website=has_website,
        min_rating=min_rating, max_rating=max_rating,
        created_after=created_after, created_before=created_before,
        sort_by=sort_by, sort_dir=sort_dir,
    )


@router.get("/pipeline", response_model=PipelineStats)
async def pipeline_stats(user: CurrentUser, db: DBSession):
    return await lead_service.get_pipeline_stats(db, user)


@router.get("/analytics", response_model=LeadAnalytics)
async def analytics(user: CurrentUser, db: DBSession):
    """Full analytics dashboard data: pipeline breakdown, source distribution,
    category breakdown, monthly trends, rating distribution, conversion rate."""
    return await lead_service.get_analytics(db, user)


@router.get("/export")
async def export_csv(user: CurrentUser, db: DBSession):
    """Export all leads as a CSV file for offline analysis."""
    rows = await lead_service.export_leads(db, user)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Business Name", "Address", "Phone", "Email", "Website",
        "Category", "Rating", "Reviews", "Pipeline Stage", "Source",
        "Contact Name", "Contact Email", "Tags", "Created At",
    ])
    for row in rows:
        writer.writerow([
            row.business_name, row.address, row.phone, row.email, row.website,
            row.category, row.rating, row.review_count, row.pipeline_stage,
            row.source, row.contact_name, row.contact_email, row.tags,
            row.created_at.isoformat(),
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=leads-export.csv"},
    )


@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(lead_id: uuid.UUID, user: CurrentUser, db: DBSession):
    return await lead_service.get_lead(db, user, lead_id)


@router.patch("/{lead_id}", response_model=LeadResponse)
async def update_lead(lead_id: uuid.UUID, data: LeadUpdate, user: CurrentUser, db: DBSession):
    return await lead_service.update_lead(db, user, lead_id, data)


@router.delete("/{lead_id}", status_code=204)
async def delete_lead(lead_id: uuid.UUID, user: CurrentUser, db: DBSession):
    await lead_service.delete_lead(db, user, lead_id)
