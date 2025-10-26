"""
AUREX.AI - Redis Cache Manager.

This module provides Redis caching utilities with automatic serialization.
"""

import json
import os
from typing import Any

import redis.asyncio as aioredis
from loguru import logger
from redis.asyncio import Redis

# Redis configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


class CacheManager:
    """Manages Redis cache operations."""

    def __init__(self, redis_url: str = REDIS_URL) -> None:
        """
        Initialize cache manager.

        Args:
            redis_url: Redis connection string
        """
        self.redis_url = redis_url
        self._client: Redis | None = None
        logger.info("Cache manager initialized")

    async def get_client(self) -> Redis:
        """Get or create Redis client."""
        if self._client is None:
            self._client = await aioredis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True,
                max_connections=50,
            )
            logger.info("Redis client created")
        return self._client

    async def set(
        self,
        key: str,
        value: Any,
        ttl: int | None = None,
    ) -> bool:
        """
        Set cache value.

        Args:
            key: Cache key
            value: Value to cache (will be JSON serialized)
            ttl: Time to live in seconds (None = no expiration)

        Returns:
            bool: True if successful
        """
        try:
            client = await self.get_client()
            serialized = json.dumps(value)
            if ttl:
                await client.setex(key, ttl, serialized)
            else:
                await client.set(key, serialized)
            logger.debug(f"Cache SET: {key} (TTL: {ttl}s)")
            return True
        except Exception as e:
            logger.error(f"Cache SET error for {key}: {e}")
            return False

    async def get(self, key: str) -> Any | None:
        """
        Get cache value.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found
        """
        try:
            client = await self.get_client()
            value = await client.get(key)
            if value is None:
                logger.debug(f"Cache MISS: {key}")
                return None
            logger.debug(f"Cache HIT: {key}")
            return json.loads(value)
        except Exception as e:
            logger.error(f"Cache GET error for {key}: {e}")
            return None

    async def delete(self, key: str) -> bool:
        """
        Delete cache value.

        Args:
            key: Cache key

        Returns:
            bool: True if key was deleted
        """
        try:
            client = await self.get_client()
            result = await client.delete(key)
            logger.debug(f"Cache DELETE: {key}")
            return result > 0
        except Exception as e:
            logger.error(f"Cache DELETE error for {key}: {e}")
            return False

    async def exists(self, key: str) -> bool:
        """
        Check if key exists in cache.

        Args:
            key: Cache key

        Returns:
            bool: True if key exists
        """
        try:
            client = await self.get_client()
            result = await client.exists(key)
            return result > 0
        except Exception as e:
            logger.error(f"Cache EXISTS error for {key}: {e}")
            return False

    async def flush_all(self) -> bool:
        """
        Flush all cache entries (use with caution!).

        Returns:
            bool: True if successful
        """
        try:
            client = await self.get_client()
            await client.flushdb()
            logger.warning("Cache FLUSHED")
            return True
        except Exception as e:
            logger.error(f"Cache FLUSH error: {e}")
            return False

    async def close(self) -> None:
        """Close Redis connection."""
        if self._client is not None:
            await self._client.close()
            logger.info("Redis connection closed")

    async def health_check(self) -> bool:
        """
        Check Redis connectivity.

        Returns:
            bool: True if Redis is accessible
        """
        try:
            client = await self.get_client()
            await client.ping()
            logger.info("Cache health check: OK")
            return True
        except Exception as e:
            logger.error(f"Cache health check failed: {e}")
            return False


# Global cache manager instance
cache_manager = CacheManager()


async def get_cache() -> CacheManager:
    """
    Get cache manager instance.

    Returns:
        CacheManager: Global cache manager
    """
    return cache_manager


async def close_cache() -> None:
    """Close cache connections."""
    await cache_manager.close()

