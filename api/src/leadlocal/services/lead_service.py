"""Lead CRUD service with advanced filtering, sorting, and analytics."""

import uuid
from datetime import datetime

from sqlalchemy import case, extract, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from leadlocal.core.config import settings
from leadlocal.core.exceptions import NotFoundError, TierLimitError
from leadlocal.models.lead import Lead, LeadTag, Tag
from leadlocal.models.user import User
from leadlocal.schemas.lead import (
    LeadAnalytics,
    LeadCreate,
    LeadExportRow,
    LeadListResponse,
    LeadResponse,
    LeadsByCategory,
    LeadsByMonth,
    LeadsBySource,
    LeadUpdate,
    PipelineStats,
    RatingDistribution,
)

# Valid sort columns and directions
SORT_COLUMNS = {
    "business_name": Lead.business_name,
    "category": Lead.category,
    "rating": Lead.rating,
    "review_count": Lead.review_count,
    "pipeline_stage": Lead.pipeline_stage,
    "source": Lead.source,
    "created_at": Lead.created_at,
    "updated_at": Lead.updated_at,
}


async def create_lead(db: AsyncSession, user: User, data: LeadCreate) -> Lead:
    limits = settings.get_tier_limits(user.tier)
    count_result = await db.execute(
        select(func.count(Lead.id)).where(Lead.user_id == user.id)
    )
    current_count = count_result.scalar() or 0
    if current_count >= limits["max_leads"]:
        raise TierLimitError("leads")

    lead = Lead(
        user_id=user.id,
        business_name=data.business_name,
        google_place_id=data.google_place_id,
        address=data.address,
        phone=data.phone,
        email=data.email,
        website=data.website,
        category=data.category,
        rating=data.rating,
        review_count=data.review_count,
        latitude=data.latitude,
        longitude=data.longitude,
        source=data.source,
        contact_name=data.contact_name,
        contact_email=data.contact_email,
        pipeline_stage=data.pipeline_stage,
    )
    db.add(lead)
    await db.flush()

    if data.tag_ids:
        for tag_id in data.tag_ids:
            db.add(LeadTag(lead_id=lead.id, tag_id=tag_id))
        await db.flush()

    return lead


async def list_leads(
    db: AsyncSession,
    user: User,
    page: int = 1,
    per_page: int = 25,
    pipeline_stage: str | None = None,
    search: str | None = None,
    tag_id: uuid.UUID | None = None,
    category: str | None = None,
    source: str | None = None,
    has_email: bool | None = None,
    has_phone: bool | None = None,
    has_website: bool | None = None,
    min_rating: float | None = None,
    max_rating: float | None = None,
    created_after: datetime | None = None,
    created_before: datetime | None = None,
    sort_by: str = "created_at",
    sort_dir: str = "desc",
) -> LeadListResponse:
    query = select(Lead).where(Lead.user_id == user.id)

    # --- Filters ---
    if pipeline_stage:
        # Support comma-separated multi-stage filter: "new,contacted"
        stages = [s.strip() for s in pipeline_stage.split(",")]
        if len(stages) == 1:
            query = query.where(Lead.pipeline_stage == stages[0])
        else:
            query = query.where(Lead.pipeline_stage.in_(stages))
    if search:
        pattern = f"%{search}%"
        query = query.where(
            Lead.business_name.ilike(pattern)
            | Lead.address.ilike(pattern)
            | Lead.category.ilike(pattern)
            | Lead.contact_name.ilike(pattern)
        )
    if tag_id:
        query = query.join(LeadTag).where(LeadTag.tag_id == tag_id)
    if category:
        query = query.where(Lead.category.ilike(f"%{category}%"))
    if source:
        query = query.where(Lead.source == source)
    if has_email is True:
        query = query.where(Lead.email.isnot(None), Lead.email != "")
    elif has_email is False:
        query = query.where((Lead.email.is_(None)) | (Lead.email == ""))
    if has_phone is True:
        query = query.where(Lead.phone.isnot(None), Lead.phone != "")
    elif has_phone is False:
        query = query.where((Lead.phone.is_(None)) | (Lead.phone == ""))
    if has_website is True:
        query = query.where(Lead.website.isnot(None), Lead.website != "")
    elif has_website is False:
        query = query.where((Lead.website.is_(None)) | (Lead.website == ""))
    if min_rating is not None:
        query = query.where(Lead.rating >= min_rating)
    if max_rating is not None:
        query = query.where(Lead.rating <= max_rating)
    if created_after:
        query = query.where(Lead.created_at >= created_after)
    if created_before:
        query = query.where(Lead.created_at <= created_before)

    # --- Count ---
    count_q = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_q)).scalar() or 0

    # --- Sorting ---
    col = SORT_COLUMNS.get(sort_by, Lead.created_at)
    if sort_dir == "asc":
        query = query.order_by(col.asc().nullslast())
    else:
        query = query.order_by(col.desc().nullslast())

    # --- Pagination ---
    query = query.offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)
    leads = result.scalars().all()

    items = [LeadResponse.model_validate(l) for l in leads]
    return LeadListResponse(items=items, total=total, page=page, per_page=per_page)


async def get_lead(db: AsyncSession, user: User, lead_id: uuid.UUID) -> Lead:
    result = await db.execute(
        select(Lead).where(Lead.id == lead_id, Lead.user_id == user.id)
    )
    lead = result.scalar_one_or_none()
    if not lead:
        raise NotFoundError("Lead")
    return lead


async def update_lead(
    db: AsyncSession, user: User, lead_id: uuid.UUID, data: LeadUpdate
) -> Lead:
    lead = await get_lead(db, user, lead_id)
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(lead, field, value)
    await db.flush()
    return lead


async def delete_lead(db: AsyncSession, user: User, lead_id: uuid.UUID) -> None:
    lead = await get_lead(db, user, lead_id)
    await db.delete(lead)


async def get_pipeline_stats(db: AsyncSession, user: User) -> PipelineStats:
    stages = ["new", "contacted", "responded", "meeting", "proposal", "won", "lost"]
    stats = {}
    for stage in stages:
        result = await db.execute(
            select(func.count(Lead.id)).where(
                Lead.user_id == user.id, Lead.pipeline_stage == stage
            )
        )
        stats[stage] = result.scalar() or 0
    return PipelineStats(**stats)


async def get_analytics(db: AsyncSession, user: User) -> LeadAnalytics:
    base = Lead.user_id == user.id

    # Total count
    total = (await db.execute(select(func.count(Lead.id)).where(base))).scalar() or 0

    # Pipeline stats
    pipeline = await get_pipeline_stats(db, user)

    # By source
    source_rows = (
        await db.execute(
            select(Lead.source, func.count(Lead.id))
            .where(base)
            .group_by(Lead.source)
            .order_by(func.count(Lead.id).desc())
        )
    ).all()
    by_source = [LeadsBySource(source=s, count=c) for s, c in source_rows]

    # By category (top 15)
    cat_rows = (
        await db.execute(
            select(Lead.category, func.count(Lead.id))
            .where(base, Lead.category.isnot(None))
            .group_by(Lead.category)
            .order_by(func.count(Lead.id).desc())
            .limit(15)
        )
    ).all()
    by_category = [LeadsByCategory(category=c or "Unknown", count=n) for c, n in cat_rows]

    # By month (last 12 months)
    month_rows = (
        await db.execute(
            select(
                func.to_char(Lead.created_at, "YYYY-MM").label("month"),
                func.count(Lead.id),
            )
            .where(base)
            .group_by("month")
            .order_by("month")
            .limit(12)
        )
    ).all()
    by_month = [LeadsByMonth(month=m, count=c) for m, c in month_rows]

    # Rating distribution
    rating_buckets = []
    for low, high, label in [(1, 2, "1-2"), (2, 3, "2-3"), (3, 4, "3-4"), (4, 5, "4-5")]:
        cnt = (
            await db.execute(
                select(func.count(Lead.id)).where(
                    base, Lead.rating >= low, Lead.rating < (high + (0.01 if high == 5 else 0))
                )
            )
        ).scalar() or 0
        rating_buckets.append(RatingDistribution(bucket=label, count=cnt))

    # Average rating
    avg_rating = (
        await db.execute(select(func.avg(Lead.rating)).where(base, Lead.rating.isnot(None)))
    ).scalar()

    # Contact data availability
    with_email = (
        await db.execute(
            select(func.count(Lead.id)).where(base, Lead.email.isnot(None), Lead.email != "")
        )
    ).scalar() or 0
    with_phone = (
        await db.execute(
            select(func.count(Lead.id)).where(base, Lead.phone.isnot(None), Lead.phone != "")
        )
    ).scalar() or 0
    with_website = (
        await db.execute(
            select(func.count(Lead.id)).where(base, Lead.website.isnot(None), Lead.website != "")
        )
    ).scalar() or 0

    # Conversion rate
    won = pipeline.won
    lost = pipeline.lost
    conversion_rate = round(won / (won + lost) * 100, 1) if (won + lost) > 0 else 0.0

    return LeadAnalytics(
        total_leads=total,
        pipeline=pipeline,
        by_source=by_source,
        by_category=by_category,
        by_month=by_month,
        rating_distribution=rating_buckets,
        avg_rating=round(float(avg_rating), 2) if avg_rating else None,
        with_email_count=with_email,
        with_phone_count=with_phone,
        with_website_count=with_website,
        conversion_rate=conversion_rate,
    )


async def export_leads(db: AsyncSession, user: User) -> list[LeadExportRow]:
    result = await db.execute(
        select(Lead).where(Lead.user_id == user.id).order_by(Lead.created_at.desc())
    )
    leads = result.scalars().all()
    rows = []
    for lead in leads:
        tag_names = ", ".join(t.name for t in (lead.tags or []))
        rows.append(
            LeadExportRow(
                business_name=lead.business_name,
                address=lead.address,
                phone=lead.phone,
                email=lead.email,
                website=lead.website,
                category=lead.category,
                rating=lead.rating,
                review_count=lead.review_count,
                pipeline_stage=lead.pipeline_stage,
                source=lead.source,
                contact_name=lead.contact_name,
                contact_email=lead.contact_email,
                tags=tag_names,
                created_at=lead.created_at,
            )
        )
    return rows


async def save_search_result(db: AsyncSession, user: User, data: LeadCreate) -> Lead:
    """Save a search result as a lead (one-click save from search)."""
    return await create_lead(db, user, data)
