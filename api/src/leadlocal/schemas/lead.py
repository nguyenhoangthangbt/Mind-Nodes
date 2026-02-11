"""Lead request/response schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel


class LeadCreate(BaseModel):
    business_name: str
    google_place_id: str | None = None
    address: str | None = None
    phone: str | None = None
    email: str | None = None
    website: str | None = None
    category: str | None = None
    rating: float | None = None
    review_count: int | None = None
    latitude: float | None = None
    longitude: float | None = None
    source: str = "manual"
    contact_name: str | None = None
    contact_email: str | None = None
    pipeline_stage: str = "new"
    tag_ids: list[uuid.UUID] = []


class LeadUpdate(BaseModel):
    business_name: str | None = None
    phone: str | None = None
    email: str | None = None
    website: str | None = None
    pipeline_stage: str | None = None
    contact_name: str | None = None
    contact_email: str | None = None


class LeadResponse(BaseModel):
    id: uuid.UUID
    business_name: str
    google_place_id: str | None
    address: str | None
    phone: str | None
    email: str | None
    website: str | None
    category: str | None
    rating: float | None
    review_count: int | None
    latitude: float | None
    longitude: float | None
    pipeline_stage: str
    source: str
    contact_name: str | None
    contact_email: str | None
    created_at: datetime
    updated_at: datetime
    tags: list["TagResponse"] = []
    notes_count: int = 0

    model_config = {"from_attributes": True}


class LeadListResponse(BaseModel):
    items: list[LeadResponse]
    total: int
    page: int
    per_page: int


class TagCreate(BaseModel):
    name: str
    color: str = "#6366f1"


class TagResponse(BaseModel):
    id: uuid.UUID
    name: str
    color: str

    model_config = {"from_attributes": True}


class PipelineStats(BaseModel):
    new: int = 0
    contacted: int = 0
    responded: int = 0
    meeting: int = 0
    proposal: int = 0
    won: int = 0
    lost: int = 0


# --- Analytics schemas ---


class LeadsBySource(BaseModel):
    source: str
    count: int


class LeadsByCategory(BaseModel):
    category: str
    count: int


class LeadsByMonth(BaseModel):
    month: str  # "2025-01"
    count: int


class RatingDistribution(BaseModel):
    bucket: str  # "1-2", "2-3", "3-4", "4-5"
    count: int


class LeadAnalytics(BaseModel):
    total_leads: int
    pipeline: PipelineStats
    by_source: list[LeadsBySource]
    by_category: list[LeadsByCategory]
    by_month: list[LeadsByMonth]
    rating_distribution: list[RatingDistribution]
    avg_rating: float | None
    with_email_count: int
    with_phone_count: int
    with_website_count: int
    conversion_rate: float  # won / (won + lost) if any closed, else 0


class LeadExportRow(BaseModel):
    business_name: str
    address: str | None
    phone: str | None
    email: str | None
    website: str | None
    category: str | None
    rating: float | None
    review_count: int | None
    pipeline_stage: str
    source: str
    contact_name: str | None
    contact_email: str | None
    tags: str  # comma-separated
    created_at: datetime
