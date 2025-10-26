"""
AUREX.AI - Sentiment API Endpoints.
"""

from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Query
from loguru import logger
from sqlalchemy import desc, select

from packages.db_core.cache import get_cache
from packages.db_core.connection import db_manager
from packages.db_core.models import SentimentSummary

router = APIRouter()


@router.get("/summary")
async def get_sentiment_summary(
    period_hours: int = Query(24, ge=1, le=168, description="Period in hours"),
):
    """
    Get the latest sentiment summary.

    Args:
        period_hours: Period in hours for the summary

    Returns:
        dict: Latest sentiment summary
    """
    cache_manager = await get_cache()

    # Try cache first
    cache_key = f"sentiment:summary:{period_hours}"
    cached_summary = await cache_manager.get(cache_key)

    if cached_summary:
        logger.info(f"Returning cached sentiment summary (period={period_hours}h)")
        return cached_summary

    try:
        async with db_manager.get_session() as session:
            query = (
                select(SentimentSummary)
                .order_by(desc(SentimentSummary.timestamp))
                .limit(1)
            )

            result = await session.execute(query)
            summary = result.scalar_one_or_none()

            if not summary:
                raise HTTPException(
                    status_code=404,
                    detail="No sentiment summary available",
                )

            total_articles = summary.sample_size or 0
            positive = summary.positive_count or 0
            neutral = summary.neutral_count or 0
            negative = summary.negative_count or 0

            summary_data = {
                "status": "success",
                "data": {
                    "id": str(summary.id),
                    "timestamp": summary.timestamp.isoformat(),
                    "period_hours": period_hours,  # From request, not DB
                    "positive_count": positive,
                    "neutral_count": neutral,
                    "negative_count": negative,
                    "total_articles": total_articles,
                    "aggregate_score": float(summary.avg_sentiment) if summary.avg_sentiment else 0.0,
                    "confidence": 0.85,  # Default confidence
                    "source": summary.symbol if hasattr(summary, 'symbol') else "news_articles",
                    "distribution": {
                        "positive": positive,
                        "neutral": neutral,
                        "negative": negative,
                    },
                    "percentages": {
                        "positive": (positive / total_articles * 100) if total_articles > 0 else 0,
                        "neutral": (neutral / total_articles * 100) if total_articles > 0 else 0,
                        "negative": (negative / total_articles * 100) if total_articles > 0 else 0,
                    },
                },
            }

            # Cache for 5 minutes
            await cache_manager.set(cache_key, summary_data, ttl=300)

            return summary_data

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching sentiment summary: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/history")
async def get_sentiment_history(
    hours: int = Query(168, ge=1, le=720, description="Hours of history to fetch"),
    period_hours: int = Query(24, ge=1, le=168, description="Period for each summary"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=200, description="Items per page"),
):
    """
    Get historical sentiment summaries.

    Args:
        hours: Number of hours of history
        period_hours: Period for each summary
        page: Page number
        page_size: Number of items per page

    Returns:
        dict: Historical sentiment data with pagination
    """
    cache_manager = await get_cache()

    # Try cache first
    cache_key = f"sentiment:history:{hours}:{period_hours}:page{page}:size{page_size}"
    cached_data = await cache_manager.get(cache_key)

    if cached_data:
        logger.info(f"Returning cached sentiment history (hours={hours}, page={page})")
        return cached_data

    try:
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)

        async with db_manager.get_session() as session:
            # Build query
            query = select(SentimentSummary).where(
                SentimentSummary.timestamp >= cutoff_time,
            )

            # Count total
            count_result = await session.execute(query)
            total_count = len(count_result.scalars().all())

            # Fetch page
            query = (
                query.order_by(desc(SentimentSummary.timestamp))
                .offset((page - 1) * page_size)
                .limit(page_size)
            )

            result = await session.execute(query)
            summaries = result.scalars().all()

            summary_data = [
                {
                    "id": str(s.id),
                    "timestamp": s.timestamp.isoformat(),
                    "period_hours": period_hours,  # Use the query parameter
                    "positive_count": s.positive_count,
                    "neutral_count": s.neutral_count,
                    "negative_count": s.negative_count,
                    "total_articles": s.sample_size,  # Use sample_size
                    "aggregate_score": float(s.avg_sentiment),  # Use avg_sentiment
                    "confidence": 0.85,  # Default confidence value
                    "distribution": {
                        "positive": s.positive_count,
                        "neutral": s.neutral_count,
                        "negative": s.negative_count,
                    },
                    "percentages": {
                        "positive": (s.positive_count / s.sample_size * 100) if s.sample_size > 0 else 0,
                        "neutral": (s.neutral_count / s.sample_size * 100) if s.sample_size > 0 else 0,
                        "negative": (s.negative_count / s.sample_size * 100) if s.sample_size > 0 else 0,
                    },
                }
                for s in summaries
            ]

            response = {
                "status": "success",
                "data": summary_data,
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total_items": total_count,
                    "total_pages": (total_count + page_size - 1) // page_size,
                },
                "params": {
                    "hours": hours,
                    "period_hours": period_hours,
                },
            }

            # Cache for 5 minutes
            await cache_manager.set(cache_key, response, ttl=300)

            return response

    except Exception as e:
        logger.error(f"Error fetching sentiment history: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/trend")
async def get_sentiment_trend(
    hours: int = Query(168, ge=24, le=720, description="Hours to analyze for trend"),
):
    """
    Get sentiment trend analysis.

    Args:
        hours: Number of hours to analyze

    Returns:
        dict: Sentiment trend (improving/declining/stable)
    """
    cache_manager = await get_cache()

    # Try cache first
    cache_key = f"sentiment:trend:{hours}"
    cached_trend = await cache_manager.get(cache_key)

    if cached_trend:
        logger.info(f"Returning cached sentiment trend (hours={hours})")
        return cached_trend

    try:
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)

        async with db_manager.get_session() as session:
            query = (
                select(SentimentSummary)
                .where(SentimentSummary.timestamp >= cutoff_time)
                .order_by(SentimentSummary.timestamp)
            )

            result = await session.execute(query)
            summaries = result.scalars().all()

            if len(summaries) < 2:
                raise HTTPException(
                    status_code=404,
                    detail="Not enough data to calculate trend",
                )

            # Calculate trend
            scores = [float(s.aggregate_score) for s in summaries]
            first_half = scores[: len(scores) // 2]
            second_half = scores[len(scores) // 2 :]

            avg_first_half = sum(first_half) / len(first_half)
            avg_second_half = sum(second_half) / len(second_half)

            change = avg_second_half - avg_first_half

            # Determine trend
            if change > 0.1:
                trend = "improving"
            elif change < -0.1:
                trend = "declining"
            else:
                trend = "stable"

            trend_data = {
                "status": "success",
                "data": {
                    "trend": trend,
                    "change": change,
                    "average_first_half": avg_first_half,
                    "average_second_half": avg_second_half,
                    "data_points": len(summaries),
                    "period_hours": hours,
                },
            }

            # Cache for 10 minutes
            await cache_manager.set(cache_key, trend_data, ttl=600)

            return trend_data

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error calculating sentiment trend: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

