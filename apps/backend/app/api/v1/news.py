"""
AUREX.AI - News API Endpoints.
"""

from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Query
from loguru import logger
from sqlalchemy import desc, select

from packages.db_core.cache import get_cache
from packages.db_core.connection import db_manager
from packages.db_core.models import News

router = APIRouter()


@router.get("/recent")
async def get_recent_news(
    hours: int = Query(24, ge=1, le=168, description="Hours of news to fetch"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    source: str = Query(None, description="Filter by source"),
):
    """
    Get recent news articles.

    Args:
        hours: Number of hours of news (1-168)
        page: Page number
        page_size: Number of items per page
        source: Filter by news source

    Returns:
        dict: Recent news articles with pagination
    """
    cache_manager = await get_cache()

    # Try cache first
    cache_key = f"news:recent:{hours}:page{page}:size{page_size}:source{source}"
    cached_data = await cache_manager.get(cache_key)

    if cached_data:
        logger.info(f"Returning cached recent news (hours={hours}, page={page})")
        return cached_data

    try:
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)

        async with db_manager.get_session() as session:
            # Build query  
            query = select(News).where(News.timestamp >= cutoff_time)

            if source:
                query = query.where(News.source == source)

            # Count total
            count_result = await session.execute(query)
            total_count = len(count_result.scalars().all())

            # Fetch page
            query = (
                query.order_by(desc(News.timestamp))
                .offset((page - 1) * page_size)
                .limit(page_size)
            )

            result = await session.execute(query)
            news_items = result.scalars().all()

            news_data = [
                {
                    "id": str(n.id),  # Convert UUID to string
                    "url": n.url,
                    "title": n.title,
                    "content": n.content[:200] + "..." if n.content and len(n.content) > 200 else n.content,
                    "published": n.timestamp.isoformat(),
                    "source": n.source,
                    "sentiment_label": n.sentiment_label,
                    "sentiment_score": float(n.sentiment_score) if n.sentiment_score else None,
                    "created_at": n.created_at.isoformat(),
                }
                for n in news_items
            ]

            response = {
                "status": "success",
                "data": news_data,
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total_items": total_count,
                    "total_pages": (total_count + page_size - 1) // page_size,
                },
                "params": {
                    "hours": hours,
                    "source": source,
                },
            }

            # Cache for 2 minutes
            await cache_manager.set(cache_key, response, ttl=120)

            return response

    except Exception as e:
        logger.error(f"Error fetching recent news: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{news_id}")
async def get_news_by_id(news_id: int):
    """
    Get a single news article by ID.

    Args:
        news_id: News article ID

    Returns:
        dict: News article details
    """
    cache_manager = await get_cache()

    # Try cache first
    cache_key = f"news:id:{news_id}"
    cached_news = await cache_manager.get(cache_key)

    if cached_news:
        logger.info(f"Returning cached news (id={news_id})")
        return cached_news

    try:
        async with db_manager.get_session() as session:
            query = select(News).where(News.id == news_id)
            result = await session.execute(query)
            news = result.scalar_one_or_none()

            if not news:
                raise HTTPException(status_code=404, detail="News article not found")

            news_data = {
                "status": "success",
                "data": {
                    "id": news.id,
                    "url": news.url,
                    "title": news.title,
                    "content": news.content,
                    "published": news.timestamp.isoformat(),
                    "source": news.source,
                    "sentiment_label": news.sentiment_label,
                    "sentiment_score": float(news.sentiment_score) if news.sentiment_score else None,
                    "created_at": news.created_at.isoformat(),
                },
            }

            # Cache for 10 minutes
            await cache_manager.set(cache_key, news_data, ttl=600)

            return news_data

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching news by ID: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/sentiment/distribution")
async def get_sentiment_distribution(
    hours: int = Query(24, ge=1, le=168, description="Hours to analyze"),
):
    """
    Get sentiment distribution of news articles.

    Args:
        hours: Number of hours to analyze

    Returns:
        dict: Sentiment distribution counts
    """
    cache_manager = await get_cache()

    # Try cache first
    cache_key = f"news:sentiment:distribution:{hours}"
    cached_data = await cache_manager.get(cache_key)

    if cached_data:
        logger.info(f"Returning cached sentiment distribution (hours={hours})")
        return cached_data

    try:
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)

        async with db_manager.get_session() as session:
            query = select(News).where(
                News.timestamp >= cutoff_time,
                News.sentiment_label.isnot(None),
            )

            result = await session.execute(query)
            news_items = result.scalars().all()

            # Calculate distribution
            distribution = {"positive": 0, "neutral": 0, "negative": 0}

            for news in news_items:
                if news.sentiment_label in distribution:
                    distribution[news.sentiment_label] += 1

            total = sum(distribution.values())

            response = {
                "status": "success",
                "data": {
                    "distribution": distribution,
                    "percentages": {
                        label: (count / total * 100) if total > 0 else 0
                        for label, count in distribution.items()
                    },
                    "total_articles": total,
                    "period_hours": hours,
                },
            }

            # Cache for 5 minutes
            await cache_manager.set(cache_key, response, ttl=300)

            return response

    except Exception as e:
        logger.error(f"Error calculating sentiment distribution: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

