"""Redis client for caching search results."""

import json
from typing import Any

import redis.asyncio as redis

from leadlocal.core.config import settings

pool = redis.ConnectionPool.from_url(settings.redis_url, decode_responses=True)


def get_redis() -> redis.Redis:
    return redis.Redis(connection_pool=pool)


SEARCH_CACHE_TTL = 86400  # 24 hours
PLACE_DETAIL_TTL = 604800  # 7 days


async def cache_get(key: str) -> Any | None:
    r = get_redis()
    data = await r.get(key)
    if data:
        return json.loads(data)
    return None


async def cache_set(key: str, value: Any, ttl: int = SEARCH_CACHE_TTL) -> None:
    r = get_redis()
    await r.set(key, json.dumps(value, default=str), ex=ttl)


async def cache_delete(key: str) -> None:
    r = get_redis()
    await r.delete(key)
