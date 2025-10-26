"""
AUREX.AI - Cache Manager Tests.
"""

import pytest

from packages.db_core.cache import CacheManager


@pytest.mark.asyncio
class TestCacheManager:
    """Test Redis cache manager."""

    @pytest.mark.skip(reason="Requires Redis connection")
    async def test_cache_set_get(self):
        """Test setting and getting cache values."""
        cache = CacheManager()

        # Set value
        await cache.set("test_key", {"value": 123})

        # Get value
        value = await cache.get("test_key")
        assert value == {"value": 123}

    @pytest.mark.skip(reason="Requires Redis connection")
    async def test_cache_delete(self):
        """Test deleting cache values."""
        cache = CacheManager()

        # Set and delete
        await cache.set("test_key", "test_value")
        await cache.delete("test_key")

        # Should return None
        value = await cache.get("test_key")
        assert value is None

    @pytest.mark.skip(reason="Requires Redis connection")
    async def test_cache_ttl(self):
        """Test cache TTL."""
        cache = CacheManager()

        # Set with 1 second TTL
        await cache.set("test_key", "test_value", ttl=1)

        # Should exist immediately
        value = await cache.get("test_key")
        assert value == "test_value"

        # Wait and check if expired
        import asyncio

        await asyncio.sleep(2)
        value = await cache.get("test_key")
        assert value is None

    @pytest.mark.skip(reason="Requires Redis connection")
    async def test_cache_health_check(self):
        """Test cache health check."""
        cache = CacheManager()
        is_healthy = await cache.health_check()
        assert isinstance(is_healthy, bool)

