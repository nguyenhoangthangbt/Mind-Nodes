"""Google Places API (New) integration client."""

import hashlib
import json

import httpx

from leadlocal.core.config import settings
from leadlocal.core.exceptions import ExternalAPIError
from leadlocal.core.redis import PLACE_DETAIL_TTL, SEARCH_CACHE_TTL, cache_get, cache_set
from leadlocal.schemas.search import SearchResult

BASE_URL = "https://places.googleapis.com/v1/places"


def _cache_key(query: str, lat: float | None, lng: float | None, radius: int) -> str:
    raw = f"gp:{query}:{lat}:{lng}:{radius}"
    return f"search:{hashlib.md5(raw.encode()).hexdigest()}"


async def search_nearby(
    query: str,
    latitude: float,
    longitude: float,
    radius_meters: int = 5000,
) -> list[SearchResult]:
    key = _cache_key(query, latitude, longitude, radius_meters)
    cached = await cache_get(key)
    if cached:
        return [SearchResult(**r) for r in cached]

    if not settings.google_places_api_key:
        raise ExternalAPIError("Google Places", "API key not configured")

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": settings.google_places_api_key,
        "X-Goog-FieldMask": (
            "places.id,places.displayName,places.formattedAddress,"
            "places.internationalPhoneNumber,places.websiteUri,"
            "places.primaryTypeDisplayName,places.rating,"
            "places.userRatingCount,places.location"
        ),
    }
    body = {
        "textQuery": query,
        "locationBias": {
            "circle": {
                "center": {"latitude": latitude, "longitude": longitude},
                "radius": float(radius_meters),
            }
        },
        "maxResultCount": 20,
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.post(f"{BASE_URL}:searchText", headers=headers, json=body)

    if resp.status_code != 200:
        raise ExternalAPIError("Google Places", f"HTTP {resp.status_code}")

    data = resp.json()
    results = []
    for place in data.get("places", []):
        loc = place.get("location", {})
        results.append(
            SearchResult(
                google_place_id=place.get("id"),
                business_name=place.get("displayName", {}).get("text", "Unknown"),
                address=place.get("formattedAddress"),
                phone=place.get("internationalPhoneNumber"),
                website=place.get("websiteUri"),
                category=place.get("primaryTypeDisplayName", {}).get("text"),
                rating=place.get("rating"),
                review_count=place.get("userRatingCount"),
                latitude=loc.get("latitude"),
                longitude=loc.get("longitude"),
                source="google_places",
            )
        )

    await cache_set(key, [r.model_dump() for r in results], SEARCH_CACHE_TTL)
    return results


async def get_place_details(place_id: str) -> dict:
    key = f"place:{place_id}"
    cached = await cache_get(key)
    if cached:
        return cached

    if not settings.google_places_api_key:
        raise ExternalAPIError("Google Places", "API key not configured")

    headers = {
        "X-Goog-Api-Key": settings.google_places_api_key,
        "X-Goog-FieldMask": (
            "id,displayName,formattedAddress,internationalPhoneNumber,"
            "websiteUri,primaryTypeDisplayName,rating,userRatingCount,"
            "location,regularOpeningHours,businessStatus"
        ),
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(f"{BASE_URL}/{place_id}", headers=headers)

    if resp.status_code != 200:
        raise ExternalAPIError("Google Places", f"HTTP {resp.status_code}")

    data = resp.json()
    await cache_set(key, data, PLACE_DETAIL_TTL)
    return data
