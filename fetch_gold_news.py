"""
AUREX.AI - Fetch Gold News and Analyze Sentiment

This script:
1. Fetches gold-related news from NewsAPI
2. Stores articles in the database
3. Runs sentiment analysis on each article
"""

import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from loguru import logger
from sqlalchemy import select
from apps.pipeline.tasks.fetch_news import NewsFetcher
from packages.ai_core.sentiment import SentimentAnalyzer
from packages.db_core.connection import db_manager
from packages.db_core.models import News
from packages.shared.logging_config import setup_logging


async def main():
    """Fetch gold news, store in DB, and analyze sentiment."""
    setup_logging("gold-news-fetcher", log_level="INFO")
    
    logger.info("="*70)
    logger.info("🚀 AUREX.AI - Gold News Fetcher & Sentiment Analyzer")
    logger.info("="*70)
    
    # Set NewsAPI key
    os.environ["NEWSAPI_KEY"] = "7fb09c63f7d64edfa67acaf40e497218"
    
    try:
        # Step 1: Fetch news
        logger.info("\n📰 Step 1: Fetching gold-related news from NewsAPI...")
        fetcher = NewsFetcher()
        articles = await fetcher.fetch_news()
        
        if not articles:
            logger.warning("⚠️  No articles fetched. Exiting.")
            return
        
        logger.info(f"✅ Fetched {len(articles)} articles")
        
        # Step 2: Store articles in database
        logger.info("\n💾 Step 2: Storing articles in database...")
        stored_count = await fetcher.store_news(articles)
        logger.info(f"✅ Stored {stored_count} articles")
        
        # Step 3: Run sentiment analysis
        logger.info("\n🧠 Step 3: Running sentiment analysis...")
        analyzer = SentimentAnalyzer()
        
        # Get articles without sentiment
        async with db_manager.get_session() as session:
            result = await session.execute(
                select(News)
                .where(News.sentiment_label == None)
                .order_by(News.timestamp.desc())
                .limit(50)
            )
            news_items = result.scalars().all()
            
            if not news_items:
                logger.info("ℹ️  All articles already have sentiment scores")
            else:
                logger.info(f"📊 Analyzing {len(news_items)} articles...")
                
                analyzed_count = 0
                for news in news_items:
                    try:
                        # Analyze sentiment
                        text = f"{news.title}. {news.content or ''}"
                        sentiment = analyzer.analyze_text(text)
                        
                        # Update news record
                        news.sentiment_label = sentiment["label"]
                        news.sentiment_score = sentiment["score"]
                        
                        analyzed_count += 1
                        
                        # Log every 10 articles
                        if analyzed_count % 10 == 0:
                            logger.info(f"  ✓ Analyzed {analyzed_count}/{len(news_items)} articles...")
                    
                    except Exception as e:
                        logger.warning(f"Error analyzing article {news.id}: {e}")
                        continue
                
                await session.commit()
                logger.info(f"✅ Analyzed {analyzed_count} articles")
        
        # Step 4: Display statistics
        logger.info("\n📊 Step 4: News Statistics")
        logger.info("-" * 70)
        
        async with db_manager.get_session() as session:
            # Count by sentiment
            result = await session.execute(
                select(News.sentiment_label, News.sentiment_score)
                .where(News.sentiment_label != None)
                .order_by(News.timestamp.desc())
                .limit(100)
            )
            sentiments = result.all()
            
            if sentiments:
                positive = sum(1 for s in sentiments if s[0] == 'positive')
                negative = sum(1 for s in sentiments if s[0] == 'negative')
                neutral = sum(1 for s in sentiments if s[0] == 'neutral')
                total = len(sentiments)
                
                logger.info(f"📈 Positive: {positive} ({positive/total*100:.1f}%)")
                logger.info(f"📉 Negative: {negative} ({negative/total*100:.1f}%)")
                logger.info(f"⚖️  Neutral:  {neutral} ({neutral/total*100:.1f}%)")
                logger.info(f"📊 Total analyzed: {total}")
                
                # Average sentiment score
                avg_score = sum(s[1] for s in sentiments) / len(sentiments)
                logger.info(f"💯 Average sentiment score: {avg_score:.3f}")
        
        logger.info("\n" + "="*70)
        logger.info("✅ Gold news fetching and sentiment analysis completed!")
        logger.info("🌐 View dashboard at: http://localhost:3000")
        logger.info("="*70)
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await db_manager.close()


if __name__ == "__main__":
    asyncio.run(main())

