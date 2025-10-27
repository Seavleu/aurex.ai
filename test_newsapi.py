"""
Test NewsAPI integration for gold-related news.
"""

import asyncio
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from loguru import logger
from apps.pipeline.tasks.fetch_news import NewsFetcher
from packages.shared.logging_config import setup_logging

async def main():
    """Test NewsAPI fetching."""
    setup_logging("test-newsapi", log_level="INFO")
    
    logger.info("="*70)
    logger.info("🧪 Testing NewsAPI Integration for AUREX.AI")
    logger.info("="*70)
    
    # Set the NewsAPI key
    os.environ["NEWSAPI_KEY"] = "7fb09c63f7d64edfa67acaf40e497218"
    
    try:
        # Initialize news fetcher
        fetcher = NewsFetcher()
        
        # Test NewsAPI only
        logger.info("\n📰 Testing NewsAPI fetch...")
        articles = await fetcher.fetch_from_newsapi()
        
        if articles:
            logger.info(f"✅ Successfully fetched {len(articles)} articles from NewsAPI")
            logger.info("\n📄 Sample articles:")
            for i, article in enumerate(articles[:5], 1):
                logger.info(f"\n{i}. {article['title']}")
                logger.info(f"   Source: {article['source']}")
                logger.info(f"   Published: {article['timestamp']}")
                logger.info(f"   URL: {article['url'][:100]}...")
        else:
            logger.warning("⚠️  No articles fetched from NewsAPI")
        
        logger.info("\n" + "="*70)
        logger.info("✅ Test completed!")
        logger.info("="*70)
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())

