"""
AUREX.AI - Sentiment Aggregation Task.

This task aggregates sentiment from news articles and stores summaries.
"""

import asyncio
from datetime import datetime, timedelta
from typing import Any

from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from packages.ai_core.sentiment import get_sentiment_analyzer
from packages.db_core.cache import get_cache_manager
from packages.db_core.connection import get_db_manager
from packages.db_core.models import News, SentimentSummary
from packages.shared.config import config
from packages.shared.logging_config import setup_logging


class SentimentAggregator:
    """Aggregates sentiment from news articles."""

    def __init__(self) -> None:
        """Initialize the sentiment aggregator."""
        self.db_manager = get_db_manager()
        self.cache_manager = get_cache_manager()
        logger.info("SentimentAggregator initialized")

    async def fetch_unprocessed_news(
        self, session: AsyncSession, hours_back: int = 24
    ) -> list[News]:
        """
        Fetch news articles that haven't been processed for sentiment.

        Args:
            session: Database session
            hours_back: How many hours back to look

        Returns:
            list: List of unprocessed news articles
        """
        cutoff_time = datetime.utcnow() - timedelta(hours=hours_back)

        query = (
            select(News)
            .where(News.published >= cutoff_time)
            .where(News.sentiment_label.is_(None))  # Not yet processed
            .order_by(News.published.desc())
        )

        result = await session.execute(query)
        news_items = result.scalars().all()

        logger.info(f"Found {len(news_items)} unprocessed news articles")
        return list(news_items)

    async def analyze_news_batch(self, news_items: list[News]) -> None:
        """
        Analyze sentiment for a batch of news articles.

        Args:
            news_items: List of news articles to analyze
        """
        if not news_items:
            logger.info("No news items to analyze")
            return

        try:
            # Get analyzer
            analyzer = await get_sentiment_analyzer()

            # Prepare texts for analysis
            texts = [f"{item.title}. {item.content or ''}" for item in news_items]

            # Batch analyze
            logger.info(f"Analyzing sentiment for {len(texts)} news articles...")
            results = await analyzer.analyze_batch(texts)

            # Update news items with sentiment
            async with self.db_manager.get_async_session() as session:
                for news_item, result in zip(news_items, results):
                    news_item.sentiment_label = result["label"]
                    news_item.sentiment_score = result["score"]
                    session.add(news_item)

                await session.commit()

            logger.info(f"✅ Updated {len(news_items)} news articles with sentiment")

            # Cache the update
            cache_key = "news:sentiment:last_update"
            await self.cache_manager.set(
                cache_key,
                {"timestamp": datetime.utcnow().isoformat(), "count": len(news_items)},
                ttl=3600,
            )

        except Exception as e:
            logger.error(f"Error analyzing news batch: {e}")
            raise

    async def create_sentiment_summary(
        self, session: AsyncSession, hours_back: int = 24
    ) -> SentimentSummary | None:
        """
        Create an aggregated sentiment summary.

        Args:
            session: Database session
            hours_back: How many hours to aggregate

        Returns:
            SentimentSummary: The created summary
        """
        cutoff_time = datetime.utcnow() - timedelta(hours=hours_back)

        # Fetch processed news in time window
        query = (
            select(News)
            .where(News.published >= cutoff_time)
            .where(News.sentiment_label.isnot(None))
        )

        result = await session.execute(query)
        news_items = result.scalars().all()

        if not news_items:
            logger.warning("No processed news to summarize")
            return None

        # Calculate sentiment distribution
        sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}
        sentiment_scores = {"positive": [], "neutral": [], "negative": []}

        for item in news_items:
            label = item.sentiment_label
            score = item.sentiment_score

            if label in sentiment_counts:
                sentiment_counts[label] += 1
                sentiment_scores[label].append(score)

        total_articles = len(news_items)

        # Calculate weighted average sentiment
        positive_weight = sentiment_counts["positive"] / total_articles
        negative_weight = sentiment_counts["negative"] / total_articles

        # Aggregate score: positive = 1, neutral = 0, negative = -1
        aggregate_score = positive_weight - negative_weight

        # Average confidence
        all_scores = (
            sentiment_scores["positive"]
            + sentiment_scores["neutral"]
            + sentiment_scores["negative"]
        )
        avg_confidence = sum(all_scores) / len(all_scores) if all_scores else 0.0

        # Create summary
        summary = SentimentSummary(
            timestamp=datetime.utcnow(),
            period_hours=hours_back,
            positive_count=sentiment_counts["positive"],
            neutral_count=sentiment_counts["neutral"],
            negative_count=sentiment_counts["negative"],
            total_articles=total_articles,
            aggregate_score=aggregate_score,
            confidence=avg_confidence,
            source="news_articles",
        )

        session.add(summary)
        await session.commit()
        await session.refresh(summary)

        logger.info(
            f"✅ Created sentiment summary: "
            f"{sentiment_counts['positive']}+ / {sentiment_counts['neutral']}= / "
            f"{sentiment_counts['negative']}- (score: {aggregate_score:.2f})"
        )

        # Cache the summary
        cache_key = f"sentiment:summary:{hours_back}h"
        await self.cache_manager.set(
            cache_key,
            {
                "aggregate_score": aggregate_score,
                "confidence": avg_confidence,
                "positive": sentiment_counts["positive"],
                "neutral": sentiment_counts["neutral"],
                "negative": sentiment_counts["negative"],
                "total": total_articles,
                "timestamp": datetime.utcnow().isoformat(),
            },
            ttl=1800,  # 30 minutes
        )

        return summary

    async def run(self, hours_back: int = 24) -> dict[str, Any]:
        """
        Run the sentiment aggregation pipeline.

        Args:
            hours_back: How many hours back to process

        Returns:
            dict: Summary of what was processed
        """
        logger.info("=" * 60)
        logger.info("Starting Sentiment Aggregation")
        logger.info("=" * 60)

        try:
            # Step 1: Fetch unprocessed news
            async with self.db_manager.get_async_session() as session:
                unprocessed_news = await self.fetch_unprocessed_news(session, hours_back)

            # Step 2: Analyze sentiment for unprocessed news
            if unprocessed_news:
                await self.analyze_news_batch(unprocessed_news)
            else:
                logger.info("No new articles to process")

            # Step 3: Create sentiment summary
            async with self.db_manager.get_async_session() as session:
                summary = await self.create_sentiment_summary(session, hours_back)

            # Step 4: Return results
            if summary:
                result = {
                    "status": "success",
                    "articles_analyzed": len(unprocessed_news),
                    "aggregate_score": summary.aggregate_score,
                    "confidence": summary.confidence,
                    "distribution": {
                        "positive": summary.positive_count,
                        "neutral": summary.neutral_count,
                        "negative": summary.negative_count,
                    },
                }
            else:
                result = {
                    "status": "no_data",
                    "articles_analyzed": len(unprocessed_news),
                }

            logger.info("✅ Sentiment aggregation complete")
            return result

        except Exception as e:
            logger.error(f"❌ Sentiment aggregation failed: {e}")
            return {"status": "error", "message": str(e)}


async def main() -> None:
    """Main entry point for testing."""
    setup_logging("sentiment-aggregator", log_level=config.LOG_LEVEL)

    # Log configuration
    logger.info("=" * 60)
    logger.info("AUREX.AI Sentiment Aggregator")
    logger.info("=" * 60)
    logger.info(f"Environment: {config.ENVIRONMENT}")
    logger.info(f"Database: {config.DATABASE_URL.split('@')[1]}")  # Hide credentials
    logger.info(f"FinBERT Model: {config.FINBERT_MODEL_NAME}")
    logger.info("=" * 60)

    aggregator = SentimentAggregator()
    result = await aggregator.run(hours_back=24)

    logger.info("\n" + "=" * 60)
    logger.info("Results")
    logger.info("=" * 60)
    for key, value in result.items():
        logger.info(f"{key}: {value}")


if __name__ == "__main__":
    asyncio.run(main())

