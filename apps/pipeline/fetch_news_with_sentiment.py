"""
AUREX.AI - Docker News Fetcher with Sentiment Analysis

This script runs inside the Docker pipeline container to:
1. Fetch gold-related news from NewsAPI
2. Store articles in the database
3. Run sentiment analysis
"""

import asyncio
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from loguru import logger
from sqlalchemy import select, func
from tasks.fetch_news import NewsFetcher
from packages.ai_core.sentiment import SentimentAnalyzer
from packages.db_core.connection import db_manager
from packages.db_core.models import News
from packages.shared.logging_config import setup_logging


async def fetch_and_analyze_news():
    """Fetch news and analyze sentiment - single iteration."""
    try:
        # Fetch news
        logger.info("📰 Fetching gold-related news from NewsAPI...")
        fetcher = NewsFetcher()
        articles = await fetcher.fetch_news()
        
        if not articles:
            logger.warning("⚠️  No new articles fetched")
            return False
        
        logger.info(f"✅ Fetched {len(articles)} articles")
        
        # Store articles
        logger.info("💾 Storing articles in database...")
        stored_count = await fetcher.store_news(articles)
        logger.info(f"✅ Stored {stored_count} articles")
        
        # Analyze sentiment
        logger.info("🧠 Running sentiment analysis...")
        analyzer = SentimentAnalyzer()
        
        async with db_manager.get_session() as session:
            # Get articles without sentiment (limit to recent 50)
            result = await session.execute(
                select(News)
                .where(News.sentiment_label == None)
                .order_by(News.timestamp.desc())
                .limit(50)
            )
            news_items = result.scalars().all()
            
            if news_items:
                analyzed_count = 0
                for news in news_items:
                    try:
                        text = f"{news.title}. {news.content or ''}"
                        sentiment = analyzer.analyze_text(text)
                        
                        news.sentiment_label = sentiment["label"]
                        news.sentiment_score = sentiment["score"]
                        analyzed_count += 1
                        
                        if analyzed_count % 10 == 0:
                            logger.info(f"  ✓ Analyzed {analyzed_count}/{len(news_items)}...")
                    
                    except Exception as e:
                        logger.warning(f"Error analyzing article {news.id}: {e}")
                        continue
                
                await session.commit()
                logger.info(f"✅ Analyzed {analyzed_count} articles")
            
            # Display statistics
            result = await session.execute(
                select(
                    News.sentiment_label,
                    func.count(News.id).label('count'),
                    func.avg(News.sentiment_score).label('avg_score')
                )
                .where(News.sentiment_label != None)
                .group_by(News.sentiment_label)
            )
            stats = result.all()
            
            if stats:
                logger.info("📊 Sentiment Statistics:")
                total = sum(s.count for s in stats)
                for stat in stats:
                    pct = (stat.count / total * 100) if total > 0 else 0
                    logger.info(f"  {stat.sentiment_label.upper()}: {stat.count} ({pct:.1f}%) | Avg score: {stat.avg_score:.3f}")
        
        return True
    
    except Exception as e:
        logger.error(f"❌ Error in fetch_and_analyze_news: {e}")
        import traceback
        traceback.print_exc()
        return False


async def run_continuous(interval_minutes: int = 60):
    """Run news fetching continuously."""
    logger.info("="*70)
    logger.info("🚀 AUREX.AI - Continuous News Fetcher & Sentiment Analyzer")
    logger.info("="*70)
    logger.info(f"⏱️  Fetch interval: {interval_minutes} minutes")
    logger.info(f"💾 Database: {os.getenv('DATABASE_URL', 'N/A')}")
    logger.info(f"🔑 NewsAPI: {'Configured' if os.getenv('NEWSAPI_KEY') else 'Not configured'}")
    logger.info("="*70)
    
    iteration = 0
    
    try:
        while True:
            iteration += 1
            logger.info(f"\n{'='*70}")
            logger.info(f"🔄 Iteration #{iteration} - {asyncio.get_event_loop().time():.0f}s")
            logger.info(f"{'='*70}")
            
            success = await fetch_and_analyze_news()
            
            if success:
                logger.info(f"✅ Iteration #{iteration} completed successfully")
            else:
                logger.warning(f"⚠️  Iteration #{iteration} completed with warnings")
            
            # Wait before next iteration
            logger.info(f"⏳ Waiting {interval_minutes} minutes until next fetch...")
            await asyncio.sleep(interval_minutes * 60)
    
    except KeyboardInterrupt:
        logger.info("\n👋 Shutting down gracefully...")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await db_manager.close()


async def run_once():
    """Run news fetching once and exit."""
    logger.info("="*70)
    logger.info("🚀 AUREX.AI - News Fetcher & Sentiment Analyzer (One-time)")
    logger.info("="*70)
    
    try:
        success = await fetch_and_analyze_news()
        
        if success:
            logger.info("\n" + "="*70)
            logger.info("✅ News fetching completed!")
            logger.info("🌐 View dashboard at: http://localhost:3000")
            logger.info("="*70)
        else:
            logger.error("❌ News fetching failed")
    
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await db_manager.close()


if __name__ == "__main__":
    setup_logging("news-fetcher", log_level="INFO")
    
    # Check if we should run continuously or once
    mode = os.getenv("NEWS_FETCH_MODE", "once")  # "once" or "continuous"
    
    if mode == "continuous":
        interval = int(os.getenv("NEWS_FETCH_INTERVAL", "60"))  # minutes
        asyncio.run(run_continuous(interval))
    else:
        asyncio.run(run_once())

