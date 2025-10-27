"""
AUREX.AI - News Fetcher Task.

Fetches financial news from NewsAPI and RSS feeds and stores it in the database.
"""

import asyncio
import os
from datetime import datetime, timedelta
from hashlib import md5

import feedparser
from loguru import logger
from newsapi import NewsApiClient

from packages.db_core.cache import cache_manager
from packages.db_core.connection import db_manager
from packages.db_core.models import News
from packages.shared.config import config
from packages.shared.constants import NEWS_SOURCE_FOREXFACTORY


class NewsFetcher:
    """Fetches and stores news articles from NewsAPI and RSS feeds."""

    def __init__(self, rss_url: str | None = None) -> None:
        """Initialize news fetcher."""
        # NewsAPI configuration
        self.newsapi_key = os.getenv("NEWSAPI_KEY", "7fb09c63f7d64edfa67acaf40e497218")
        self.newsapi_client = NewsApiClient(api_key=self.newsapi_key) if self.newsapi_key else None
        
        # RSS fallback sources
        self.rss_urls = [
            rss_url if rss_url else config.FOREXFACTORY_RSS_URL,
            config.INVESTING_RSS_URL,
            "https://feeds.finance.yahoo.com/rss/2.0/headline?s=GC=F&region=US&lang=en-US",
        ]
        self.cache_ttl = config.CACHE_TTL_NEWS
        self.seen_articles = set()  # For deduplication
        
        if self.newsapi_client:
            logger.info("NewsFetcher initialized with NewsAPI + RSS fallback sources")
        else:
            logger.info(f"NewsFetcher initialized with {len(self.rss_urls)} RSS sources only")

    async def fetch_from_newsapi(self) -> list[dict]:
        """
        Fetch gold-related news from NewsAPI.

        Returns:
            list[dict]: List of news articles
        """
        if not self.newsapi_client:
            logger.warning("NewsAPI client not initialized")
            return []

        try:
            logger.info("Fetching gold news from NewsAPI...")
            
            # Search for gold-related articles from the last 24 hours
            from_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            
            # Run synchronous NewsAPI call in executor
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.newsapi_client.get_everything(
                    q='gold OR XAUUSD OR "gold spot" OR "gold prices"',
                    language='en',
                    from_param=from_date,
                    sort_by='publishedAt',
                    page_size=50
                )
            )
            
            articles = []
            if response.get('status') == 'ok':
                for article_data in response.get('articles', []):
                    try:
                        # Create unique ID for deduplication
                        url = article_data.get('url', '')
                        article_id = md5(url.encode()).hexdigest()

                        if article_id in self.seen_articles:
                            continue  # Skip duplicates

                        # Parse timestamp
                        published_at = article_data.get('publishedAt', '')
                        try:
                            timestamp = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                        except:
                            timestamp = datetime.utcnow()

                        # Extract article data
                        article = {
                            "title": article_data.get('title', 'Untitled'),
                            "url": url,
                            "source": article_data.get('source', {}).get('name', 'NewsAPI'),
                            "timestamp": timestamp,
                            "content": (article_data.get('description') or article_data.get('content') or '')[:500],
                        }

                        articles.append(article)
                        self.seen_articles.add(article_id)

                    except Exception as e:
                        logger.warning(f"Error parsing NewsAPI article: {e}")
                        continue

                logger.info(f"✅ Fetched {len(articles)} articles from NewsAPI")
            else:
                logger.warning(f"NewsAPI returned status: {response.get('status')}")
            
            return articles

        except Exception as e:
            logger.error(f"NewsAPI error: {e}")
            return []

    async def fetch_from_rss(self) -> list[dict]:
        """
        Fetch news from RSS feeds (fallback method).

        Returns:
            list[dict]: List of news articles
        """
        all_articles = []

        for rss_url in self.rss_urls:
            try:
                logger.info(f"Trying RSS feed: {rss_url}")

                # feedparser is synchronous, run in executor
                loop = asyncio.get_event_loop()
                feed = await loop.run_in_executor(None, feedparser.parse, rss_url)

                if feed.bozo:  # Feed parsing error
                    logger.warning(f"RSS feed error: {feed.bozo_exception}")
                    continue  # Try next source

                articles_from_feed = []
                for entry in feed.entries:
                    try:
                        # Create unique ID for deduplication
                        article_id = md5(entry.link.encode()).hexdigest()

                        if article_id in self.seen_articles:
                            continue  # Skip duplicates

                        # Extract article data
                        published = entry.get("published_parsed") or entry.get("updated_parsed")
                        timestamp = (
                            datetime(*published[:6])
                            if published
                            else datetime.utcnow()
                        )

                        article = {
                            "title": entry.title,
                            "url": entry.link,
                            "source": feed.feed.get("title", "Financial News"),
                            "timestamp": timestamp,
                            "content": entry.get("summary", "")[:500],  # Limit content
                        }

                        articles_from_feed.append(article)
                        self.seen_articles.add(article_id)

                    except Exception as e:
                        logger.warning(f"Error parsing article: {e}")
                        continue

                logger.info(f"Fetched {len(articles_from_feed)} articles from {rss_url}")
                all_articles.extend(articles_from_feed)

                # If we got articles, we can stop trying other sources
                if len(all_articles) >= 10:
                    break

            except Exception as e:
                logger.warning(f"Error with {rss_url}: {e}")
                continue

        return all_articles

    async def fetch_news(self) -> list[dict]:
        """
        Fetch news from all sources (NewsAPI first, then RSS fallback).

        Returns:
            list[dict]: List of news articles
        """
        all_articles = []

        # Try NewsAPI first (more reliable and structured)
        if self.newsapi_client:
            newsapi_articles = await self.fetch_from_newsapi()
            all_articles.extend(newsapi_articles)

        # If NewsAPI didn't get enough articles, use RSS feeds
        if len(all_articles) < 10:
            logger.info("Fetching additional articles from RSS feeds...")
            rss_articles = await self.fetch_from_rss()
            all_articles.extend(rss_articles)

        logger.info(f"Total fetched: {len(all_articles)} new articles")
        return all_articles

    async def store_news(self, articles: list[dict]) -> int:
        """
        Store news articles in database.

        Args:
            articles: List of article dictionaries

        Returns:
            int: Number of articles stored
        """
        if not articles:
            return 0

        try:
            async with db_manager.get_session() as session:
                stored_count = 0
                for article_data in articles:
                    # Check if article already exists
                    # (In production, would use a unique constraint)
                    news_record = News(**article_data)
                    session.add(news_record)
                    stored_count += 1

                await session.commit()

            logger.info(f"Stored {stored_count} articles in database")
            return stored_count

        except Exception as e:
            logger.error(f"Error storing news: {e}")
            return 0

    async def cache_news(self, articles: list[dict]) -> bool:
        """
        Cache recent news in Redis.

        Args:
            articles: List of article dictionaries

        Returns:
            bool: True if successful
        """
        if not articles:
            return False

        try:
            # Cache only headlines for quick access
            headlines = [
                {
                    "title": article["title"],
                    "url": article["url"],
                    "timestamp": article["timestamp"].isoformat(),
                }
                for article in articles[:20]  # Top 20 recent
            ]

            await cache_manager.set(
                "news:recent:headlines",
                headlines,
                ttl=self.cache_ttl,
            )

            logger.info(f"Cached {len(headlines)} headlines")
            return True

        except Exception as e:
            logger.error(f"Error caching news: {e}")
            return False

    async def run(self) -> bool:
        """
        Run the news fetching task.

        Returns:
            bool: True if successful
        """
        try:
            # Fetch news
            articles = await self.fetch_news()

            if not articles:
                logger.warning("No new articles found")
                return False

            # Store in database
            stored_count = await self.store_news(articles)

            # Cache recent headlines
            cached = await self.cache_news(articles)

            success = stored_count > 0
            if success:
                logger.info(f"✅ News fetch completed: {stored_count} articles")
            else:
                logger.warning("⚠️  News fetch partially failed")

            return success

        except Exception as e:
            logger.error(f"❌ News fetch failed: {e}")
            return False


async def fetch_news_task() -> bool:
    """
    Standalone task function for Prefect.

    Returns:
        bool: True if successful
    """
    fetcher = NewsFetcher()
    return await fetcher.run()


async def main() -> None:
    """Main entry point for testing."""
    from packages.shared.logging_config import setup_logging

    setup_logging("news-fetcher", log_level="INFO")
    config.log_config()

    logger.info("Starting news fetcher...")

    # Run once
    fetcher = NewsFetcher()
    success = await fetcher.run()

    if success:
        logger.info("✅ News fetch successful!")

        # Test cache retrieval
        cached_news = await cache_manager.get("news:recent:headlines")
        if cached_news:
            logger.info(f"Cached headlines: {len(cached_news)} articles")
            for headline in cached_news[:3]:
                logger.info(f"  - {headline['title']}")
    else:
        logger.error("❌ News fetch failed!")

    # Cleanup
    await db_manager.close()
    await cache_manager.close()


if __name__ == "__main__":
    asyncio.run(main())

