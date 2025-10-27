"""
AUREX.AI - Fetch Gold News (Backend Container Version)

Simple news fetcher that runs in the backend container.
Fetches news from NewsAPI and stores in database (without sentiment for now).
"""

import asyncio
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from loguru import logger
from newsapi import NewsApiClient
from hashlib import md5

from packages.db_core.connection import db_manager
from packages.db_core.models import News


async def fetch_and_store_news():
    """Fetch news from NewsAPI and store in database."""
    logger.info("="*70)
    logger.info("📰 AUREX.AI - Gold News Fetcher")
    logger.info("="*70)
    
    # Initialize NewsAPI
    api_key = os.getenv("NEWSAPI_KEY", "7fb09c63f7d64edfa67acaf40e497218")
    newsapi = NewsApiClient(api_key=api_key)
    
    logger.info(f"🔑 NewsAPI Key: {api_key[:20]}...")
    
    try:
        # Fetch articles
        logger.info("📡 Fetching gold-related news from NewsAPI...")
        from_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        response = newsapi.get_everything(
            q='gold OR XAUUSD OR "gold spot" OR "gold prices"',
            language='en',
            from_param=from_date,
            sort_by='publishedAt',
            page_size=50
        )
        
        if response.get('status') != 'ok':
            logger.error(f"❌ NewsAPI error: {response}")
            return
        
        articles_data = response.get('articles', [])
        logger.info(f"✅ Fetched {len(articles_data)} articles")
        
        # Store in database
        logger.info("💾 Storing articles in database...")
        
        async with db_manager.get_session() as session:
            stored_count = 0
            seen = set()
            
            for article in articles_data:
                try:
                    url = article.get('url', '')
                    article_id = md5(url.encode()).hexdigest()
                    
                    if article_id in seen:
                        continue
                    seen.add(article_id)
                    
                    # Parse timestamp
                    published_at = article.get('publishedAt', '')
                    try:
                        timestamp = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                    except:
                        timestamp = datetime.utcnow()
                    
                    # Create news record
                    news = News(
                        title=article.get('title', 'Untitled'),
                        url=url,
                        source=article.get('source', {}).get('name', 'NewsAPI'),
                        timestamp=timestamp,
                        content=(article.get('description') or article.get('content') or '')[:500]
                    )
                    
                    session.add(news)
                    stored_count += 1
                
                except Exception as e:
                    logger.warning(f"Error processing article: {e}")
                    continue
            
            await session.commit()
            logger.info(f"✅ Stored {stored_count} articles")
        
        # Show sample articles
        logger.info("\n📄 Sample articles:")
        for i, article in enumerate(articles_data[:5], 1):
            logger.info(f"{i}. {article.get('title', 'N/A')}")
            logger.info(f"   Source: {article.get('source', {}).get('name', 'N/A')}")
        
        logger.info("\n" + "="*70)
        logger.info("✅ News fetching completed!")
        logger.info("🌐 View at: http://localhost:3000")
        logger.info("="*70)
    
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await db_manager.close()


if __name__ == "__main__":
    asyncio.run(fetch_and_store_news())

