"""
AUREX.AI - Price API Endpoints.
"""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from loguru import logger
from sqlalchemy import desc, select

from packages.db_core.cache import get_cache
from packages.db_core.connection import db_manager
from packages.db_core.models import Price
from packages.shared.config import config

router = APIRouter()


@router.get("/latest")
async def get_latest_price():
    """
    Get the latest gold price.

    Returns:
        dict: Latest price data
    """
    cache_manager = await get_cache()

    # Try cache first
    cache_key = "price:latest"
    cached_price = await cache_manager.get(cache_key)

    if cached_price:
        logger.info("Returning cached latest price")
        return {
            "status": "success",
            "data": cached_price,
            "source": "cache",
        }

    # Fetch from database
    try:
        async with db_manager.get_session() as session:
            query = select(Price).order_by(desc(Price.timestamp)).limit(1)
            result = await session.execute(query)
            price = result.scalar_one_or_none()

            if not price:
                raise HTTPException(status_code=404, detail="No price data available")

            price_data = {
                "id": price.id,
                "timestamp": price.timestamp.isoformat(),
                "symbol": price.symbol,
                "open": float(price.open) if price.open is not None else 0.0,
                "high": float(price.high) if price.high is not None else 0.0,
                "low": float(price.low) if price.low is not None else 0.0,
                "close": float(price.close) if price.close is not None else 0.0,
                "volume": price.volume if price.volume is not None else 0,
                "change": None,  # Calculated field, not in DB
                "change_pct": float(price.change_pct) if price.change_pct is not None else None,
            }

            # Cache for 1 minute
            await cache_manager.set(cache_key, price_data, ttl=60)

            return {
                "status": "success",
                "data": price_data,
                "source": "database",
            }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching latest price: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/history")
async def get_price_history(
    hours: int = Query(24, ge=1, le=720, description="Hours of history to fetch"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(100, ge=1, le=1000, description="Items per page"),
):
    """
    Get historical gold prices.

    Args:
        hours: Number of hours of history (1-720)
        page: Page number
        page_size: Number of items per page

    Returns:
        dict: Historical price data with pagination
    """
    cache_manager = await get_cache()

    # Try cache first
    cache_key = f"price:history:{hours}:page{page}:size{page_size}"
    cached_data = await cache_manager.get(cache_key)

    if cached_data:
        logger.info(f"Returning cached price history (hours={hours}, page={page})")
        return cached_data

    # Fetch from database
    try:
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)

        async with db_manager.get_session() as session:
            # Count total
            count_query = select(Price).where(Price.timestamp >= cutoff_time)
            count_result = await session.execute(count_query)
            total_count = len(count_result.scalars().all())

            # Fetch page
            query = (
                select(Price)
                .where(Price.timestamp >= cutoff_time)
                .order_by(desc(Price.timestamp))
                .offset((page - 1) * page_size)
                .limit(page_size)
            )

            result = await session.execute(query)
            prices = result.scalars().all()

            price_data = [
                {
                    "id": p.id,
                    "timestamp": p.timestamp.isoformat(),
                    "symbol": p.symbol,
                    "open": float(p.open) if p.open is not None else None,
                    "high": float(p.high) if p.high is not None else None,
                    "low": float(p.low) if p.low is not None else None,
                    "close": float(p.close) if p.close is not None else None,
                    "volume": p.volume,
                    "change": None,  # Calculated field, not stored in DB
                    "change_pct": None,  # Calculated field, not stored in DB
                }
                for p in prices
            ]

            response = {
                "status": "success",
                "data": price_data,
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total_items": total_count,
                    "total_pages": (total_count + page_size - 1) // page_size,
                },
                "params": {
                    "hours": hours,
                },
            }

            # Cache for 2 minutes
            await cache_manager.set(cache_key, response, ttl=120)

            return response

    except Exception as e:
        logger.error(f"Error fetching price history: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/stats")
async def get_price_stats(
    hours: int = Query(24, ge=1, le=720, description="Hours for statistics"),
):
    """
    Get price statistics for a time period.

    Args:
        hours: Number of hours for statistics

    Returns:
        dict: Price statistics (high, low, avg, change)
    """
    cache_manager = await get_cache()

    # Try cache first
    cache_key = f"price:stats:{hours}"
    cached_stats = await cache_manager.get(cache_key)

    if cached_stats:
        logger.info(f"Returning cached price stats (hours={hours})")
        return cached_stats

    try:
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)

        async with db_manager.get_session() as session:
            query = (
                select(Price)
                .where(Price.timestamp >= cutoff_time)
                .order_by(Price.timestamp)
            )

            result = await session.execute(query)
            prices = result.scalars().all()

            if not prices:
                raise HTTPException(
                    status_code=404, detail="No price data available for this period"
                )

            # Calculate stats (filter out None values)
            closes = [float(p.close) for p in prices if p.close is not None]
            highs = [float(p.high) for p in prices if p.high is not None]
            lows = [float(p.low) for p in prices if p.low is not None]
            
            if not closes:
                raise HTTPException(
                    status_code=404, detail="No valid price data available for this period"
                )

            first_price = closes[0]
            last_price = closes[-1]
            price_change = last_price - first_price
            price_change_pct = (price_change / first_price) * 100 if first_price else 0

            stats = {
                "status": "success",
                "data": {
                    "period_hours": hours,
                    "current_price": last_price,
                    "high": max(highs),
                    "low": min(lows),
                    "average": sum(closes) / len(closes),
                    "change": price_change,
                    "change_pct": price_change_pct,
                    "data_points": len(prices),
                    "first_timestamp": prices[0].timestamp.isoformat(),
                    "last_timestamp": prices[-1].timestamp.isoformat(),
                },
            }

            # Cache for 5 minutes
            await cache_manager.set(cache_key, stats, ttl=300)

            return stats

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error calculating price stats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

