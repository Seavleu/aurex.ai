"""
AUREX.AI - Health Check Endpoints.
"""

from datetime import datetime

from fastapi import APIRouter, HTTPException
from loguru import logger

from packages.db_core.cache import get_cache
from packages.db_core.connection import db_manager
from packages.shared.config import config

router = APIRouter()


@router.get("/health")
async def health_check() -> dict:
    """
    Health check endpoint.

    Returns:
        dict: Health status of the application
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": config.APP_VERSION,
        "environment": config.ENVIRONMENT,
    }


@router.get("/health/detailed")
async def detailed_health_check() -> dict:
    """
    Detailed health check with service status.

    Returns:
        dict: Detailed health status including DB and cache
    """
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": config.APP_VERSION,
        "environment": config.ENVIRONMENT,
        "services": {},
    }

    # Check database
    try:
        db_healthy = await db_manager.health_check()
        health_status["services"]["database"] = {
            "status": "healthy" if db_healthy else "unhealthy",
            "type": "PostgreSQL",
        }
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        health_status["services"]["database"] = {
            "status": "unhealthy",
            "error": str(e),
        }
        health_status["status"] = "degraded"

    # Check cache
    try:
        cache_manager = await get_cache()
        cache_healthy = await cache_manager.health_check()
        health_status["services"]["cache"] = {
            "status": "healthy" if cache_healthy else "unhealthy",
            "type": "Redis",
        }
    except Exception as e:
        logger.error(f"Cache health check failed: {e}")
        health_status["services"]["cache"] = {
            "status": "unhealthy",
            "error": str(e),
        }
        health_status["status"] = "degraded"

    return health_status

