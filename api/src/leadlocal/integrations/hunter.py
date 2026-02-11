"""Hunter.io API client for email enrichment (optional)."""

import httpx

from leadlocal.core.config import settings
from leadlocal.core.redis import PLACE_DETAIL_TTL, cache_get, cache_set


async def find_email(domain: str) -> dict | None:
    if not settings.hunter_api_key or not domain:
        return None

    key = f"hunter:{domain}"
    cached = await cache_get(key)
    if cached:
        return cached

    params = {"domain": domain, "api_key": settings.hunter_api_key}
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get("https://api.hunter.io/v2/domain-search", params=params)

    if resp.status_code != 200:
        return None

    data = resp.json().get("data", {})
    result = {
        "domain": data.get("domain"),
        "organization": data.get("organization"),
        "emails": [
            {"email": e["value"], "type": e.get("type"), "confidence": e.get("confidence")}
            for e in data.get("emails", [])[:5]
        ],
    }

    await cache_set(key, result, PLACE_DETAIL_TTL)
    return result
