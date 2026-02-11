"""Yelp Fusion API integration client (optional enrichment)."""

import httpx

from leadlocal.core.config import settings
from leadlocal.core.exceptions import ExternalAPIError
from leadlocal.core.redis import SEARCH_CACHE_TTL, cache_get, cache_set
from leadlocal.schemas.search import SearchResult

BASE_URL = "https://api.yelp.com/v3"


async def search_businesses(
    term: str,
    latitude: float,
    longitude: float,
    radius_meters: int = 5000,
    limit: int = 20,
) -> list[SearchResult]:
    if not settings.yelp_api_key:
        return []

    key = f"yelp:{term}:{latitude}:{longitude}:{radius_meters}"
    cached = await cache_get(key)
    if cached:
        return [SearchResult(**r) for r in cached]

    headers = {"Authorization": f"Bearer {settings.yelp_api_key}"}
    params = {
        "term": term,
        "latitude": latitude,
        "longitude": longitude,
        "radius": min(radius_meters, 40000),
        "limit": limit,
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(f"{BASE_URL}/businesses/search", headers=headers, params=params)

    if resp.status_code != 200:
        raise ExternalAPIError("Yelp", f"HTTP {resp.status_code}")

    data = resp.json()
    results = []
    for biz in data.get("businesses", []):
        coords = biz.get("coordinates", {})
        loc = biz.get("location", {})
        addr_parts = [loc.get("address1", ""), loc.get("city", ""), loc.get("state", "")]
        address = ", ".join(p for p in addr_parts if p)
        cats = biz.get("categories", [])
        category = cats[0]["title"] if cats else None

        results.append(
            SearchResult(
                business_name=biz.get("name", "Unknown"),
                address=address or None,
                phone=biz.get("phone") or None,
                website=biz.get("url"),
                category=category,
                rating=biz.get("rating"),
                review_count=biz.get("review_count"),
                latitude=coords.get("latitude"),
                longitude=coords.get("longitude"),
                source="yelp",
            )
        )

    await cache_set(key, [r.model_dump() for r in results], SEARCH_CACHE_TTL)
    return results
