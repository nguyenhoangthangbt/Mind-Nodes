"""Search service — orchestrates lead discovery across providers."""

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from leadlocal.core.config import settings
from leadlocal.core.exceptions import TierLimitError
from leadlocal.integrations import google_places, yelp
from leadlocal.models.lead import Lead
from leadlocal.models.search_log import SearchLog
from leadlocal.models.user import User
from leadlocal.schemas.search import SearchRequest, SearchResponse, SearchResult


async def search_leads(
    db: AsyncSession,
    user: User,
    req: SearchRequest,
) -> SearchResponse:
    # Check search limit
    limits = settings.get_tier_limits(user.tier)
    month_start = datetime.now(UTC).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    result = await db.execute(
        select(SearchLog)
        .where(SearchLog.user_id == user.id, SearchLog.created_at >= month_start)
    )
    searches_this_month = len(result.scalars().all())
    if searches_this_month >= limits["max_searches"]:
        raise TierLimitError("searches")

    lat = req.latitude
    lng = req.longitude

    # If no coords but location string given, we rely on Google's text search
    # which handles location strings natively
    if lat is None or lng is None:
        lat = lat or 0.0
        lng = lng or 0.0

    results: list[SearchResult] = []

    if req.source in ("google_places", "all"):
        gp_results = await google_places.search_nearby(
            query=req.query,
            latitude=lat,
            longitude=lng,
            radius_meters=req.radius_meters,
        )
        results.extend(gp_results)

    if req.source in ("yelp", "all") and settings.yelp_api_key:
        yelp_results = await yelp.search_businesses(
            term=req.query,
            latitude=lat,
            longitude=lng,
            radius_meters=req.radius_meters,
        )
        results.extend(yelp_results)

    # Mark already-saved leads
    if results:
        place_ids = [r.google_place_id for r in results if r.google_place_id]
        if place_ids:
            existing = await db.execute(
                select(Lead.google_place_id)
                .where(Lead.user_id == user.id, Lead.google_place_id.in_(place_ids))
            )
            saved_ids = set(existing.scalars().all())
            for r in results:
                if r.google_place_id and r.google_place_id in saved_ids:
                    r.already_saved = True

    # Log the search
    log = SearchLog(
        user_id=user.id,
        query=req.query,
        location=req.location,
        latitude=lat,
        longitude=lng,
        radius_meters=req.radius_meters,
        result_count=len(results),
        source=req.source,
    )
    db.add(log)

    return SearchResponse(results=results, total=len(results), query=req.query)
