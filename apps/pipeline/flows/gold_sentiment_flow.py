"""
AUREX.AI - Gold Sentiment Analysis Flow.

This flow orchestrates the end-to-end pipeline for gold price and sentiment analysis.
"""

import asyncio
from datetime import timedelta

from loguru import logger
from prefect import flow, task
from prefect.tasks import task_input_hash

from apps.pipeline.tasks.fetch_news import NewsScraper
from apps.pipeline.tasks.fetch_price import PriceFetcher
from apps.pipeline.tasks.sentiment_aggregator import SentimentAggregator
from packages.shared.config import config
from packages.shared.logging_config import setup_logging


@task(
    name="fetch-gold-price",
    description="Fetch current gold price from yfinance",
    retries=3,
    retry_delay_seconds=60,
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(minutes=5),
)
async def fetch_gold_price_task() -> dict:
    """
    Fetch gold price task.

    Returns:
        dict: Price data
    """
    logger.info("🔍 Fetching gold price...")
    fetcher = PriceFetcher(symbol=config.GOLD_SYMBOL)
    result = await fetcher.run()
    return result


@task(
    name="fetch-financial-news",
    description="Scrape financial news from multiple sources",
    retries=3,
    retry_delay_seconds=120,
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(minutes=15),
)
async def fetch_news_task() -> dict:
    """
    Fetch financial news task.

    Returns:
        dict: News data
    """
    logger.info("📰 Fetching financial news...")
    scraper = NewsScraper()
    result = await scraper.run()
    return result


@task(
    name="analyze-sentiment",
    description="Analyze sentiment from news articles",
    retries=2,
    retry_delay_seconds=60,
)
async def analyze_sentiment_task(hours_back: int = 24) -> dict:
    """
    Analyze sentiment task.

    Args:
        hours_back: How many hours back to analyze

    Returns:
        dict: Sentiment analysis results
    """
    logger.info("🤖 Analyzing sentiment...")
    aggregator = SentimentAggregator()
    result = await aggregator.run(hours_back=hours_back)
    return result


@flow(
    name="gold-sentiment-pipeline",
    description="End-to-end pipeline for gold price and sentiment analysis",
    log_prints=True,
)
async def gold_sentiment_pipeline(hours_back: int = 24) -> dict:
    """
    Main pipeline flow.

    This flow orchestrates:
    1. Fetching gold price
    2. Scraping financial news
    3. Analyzing sentiment
    4. Aggregating results

    Args:
        hours_back: How many hours back to analyze sentiment

    Returns:
        dict: Pipeline results
    """
    setup_logging("gold-sentiment-flow", log_level=config.LOG_LEVEL)

    logger.info("=" * 80)
    logger.info("🚀 AUREX.AI Gold Sentiment Pipeline")
    logger.info("=" * 80)
    logger.info(f"Environment: {config.ENVIRONMENT}")
    logger.info(f"Analyzing last {hours_back} hours")
    logger.info("=" * 80)

    results = {}

    # Task 1: Fetch gold price (parallel with news)
    price_future = fetch_gold_price_task()
    news_future = fetch_news_task()

    # Wait for both to complete
    price_result = await price_future
    news_result = await news_future

    results["price"] = price_result
    results["news"] = news_result

    logger.info("✅ Data collection complete")

    # Task 2: Analyze sentiment (depends on news)
    if news_result.get("status") == "success":
        sentiment_result = await analyze_sentiment_task(hours_back=hours_back)
        results["sentiment"] = sentiment_result
    else:
        logger.warning("⚠️  Skipping sentiment analysis (no news available)")
        results["sentiment"] = {"status": "skipped", "reason": "no_news"}

    # Final summary
    logger.info("=" * 80)
    logger.info("📊 Pipeline Summary")
    logger.info("=" * 80)

    if results["price"].get("status") == "success":
        price_data = results["price"].get("price", {})
        logger.info(
            f"💰 Gold Price: ${price_data.get('close', 0):.2f} "
            f"({price_data.get('change_pct', 0):+.2f}%)"
        )
    else:
        logger.warning("⚠️  Price fetch failed")

    if results["news"].get("status") == "success":
        logger.info(f"📰 News Articles: {results['news'].get('articles_saved', 0)} saved")
    else:
        logger.warning("⚠️  News fetch failed")

    if results["sentiment"].get("status") == "success":
        sentiment = results["sentiment"]
        logger.info(
            f"🤖 Sentiment: {sentiment.get('aggregate_score', 0):.2f} "
            f"(confidence: {sentiment.get('confidence', 0):.2%})"
        )
        dist = sentiment.get("distribution", {})
        logger.info(
            f"   Distribution: {dist.get('positive', 0)}+ / "
            f"{dist.get('neutral', 0)}= / {dist.get('negative', 0)}-"
        )
    else:
        logger.warning("⚠️  Sentiment analysis unavailable")

    logger.info("=" * 80)
    logger.info("✅ Pipeline complete!")
    logger.info("=" * 80)

    return results


@flow(
    name="continuous-monitoring",
    description="Continuous monitoring flow (runs every 5 minutes)",
    log_prints=True,
)
async def continuous_monitoring() -> None:
    """
    Continuous monitoring flow.

    This flow runs the pipeline continuously with a 5-minute interval.
    """
    setup_logging("continuous-monitoring", log_level=config.LOG_LEVEL)

    logger.info("🔄 Starting continuous monitoring...")

    while True:
        try:
            await gold_sentiment_pipeline(hours_back=24)
            logger.info("⏳ Waiting 5 minutes until next run...")
            await asyncio.sleep(300)  # 5 minutes

        except Exception as e:
            logger.error(f"❌ Pipeline error: {e}")
            logger.info("⏳ Waiting 1 minute before retry...")
            await asyncio.sleep(60)  # 1 minute on error


async def main() -> None:
    """Main entry point for testing."""
    # Run pipeline once
    await gold_sentiment_pipeline(hours_back=24)


if __name__ == "__main__":
    asyncio.run(main())

