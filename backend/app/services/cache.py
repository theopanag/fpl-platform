"""
Cache service for storing frequently accessed data.

Handles Redis operations and provides caching functionality.
"""

import json
from typing import Any

import redis.asyncio as redis
from loguru import logger

from app.core.config import settings


class CacheService:
    """Service for caching data using Redis."""

    def __init__(self):
        self.redis_client = None

    async def _get_client(self) -> redis.Redis:
        """Get or create Redis client."""
        if not self.redis_client:
            self.redis_client = redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
        return self.redis_client

    async def get(self, key: str) -> Any | None:
        """Get value from cache."""
        try:
            client = await self._get_client()
            cached_data = await client.get(key)

            if cached_data:
                return json.loads(cached_data)
            return None

        except Exception as e:
            logger.warning(f"Cache get error for key {key}: {e}")
            return None

    async def set(
        self, key: str, value: Any, expire: int | None = None
    ) -> bool:
        """Set value in cache with optional expiration."""
        try:
            client = await self._get_client()
            serialized_value = json.dumps(value, default=str)

            if expire:
                await client.setex(key, expire, serialized_value)
            else:
                await client.set(key, serialized_value)

            return True

        except Exception as e:
            logger.warning(f"Cache set error for key {key}: {e}")
            return False

    async def delete(self, key: str) -> bool:
        """Delete key from cache."""
        try:
            client = await self._get_client()
            await client.delete(key)
            return True

        except Exception as e:
            logger.warning(f"Cache delete error for key {key}: {e}")
            return False

    async def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        try:
            client = await self._get_client()
            return bool(await client.exists(key))

        except Exception as e:
            logger.warning(f"Cache exists error for key {key}: {e}")
            return False

    async def flush_all(self) -> bool:
        """Flush all cache data."""
        try:
            client = await self._get_client()
            await client.flushall()
            return True

        except Exception as e:
            logger.error(f"Cache flush error: {e}")
            return False

    async def close(self) -> None:
        """Close Redis connection."""
        if self.redis_client:
            await self.redis_client.aclose()