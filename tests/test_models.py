"""
AUREX.AI - Database Models Tests.
"""

from datetime import datetime

import pytest
from sqlalchemy import select

from packages.db_core.models import Alert, News, Price, SentimentSummary


@pytest.mark.asyncio
class TestDatabaseModels:
    """Test database models."""

    async def test_news_model(self, db_session, sample_news_data):
        """Test News model."""
        news = News(
            url=sample_news_data["url"],
            title=sample_news_data["title"],
            content=sample_news_data["content"],
            published=datetime.fromisoformat(sample_news_data["published"].replace("Z", "+00:00")),
            source=sample_news_data["source"],
        )

        db_session.add(news)
        await db_session.commit()
        await db_session.refresh(news)

        assert news.id is not None
        assert news.title == sample_news_data["title"]
        assert news.source == sample_news_data["source"]

    async def test_price_model(self, db_session, sample_price_data):
        """Test Price model."""
        price = Price(
            timestamp=datetime.utcnow(),
            symbol=sample_price_data["symbol"],
            open=sample_price_data["open"],
            high=sample_price_data["high"],
            low=sample_price_data["low"],
            close=sample_price_data["close"],
            volume=sample_price_data["volume"],
            change=sample_price_data["change"],
            change_pct=sample_price_data["change_pct"],
        )

        db_session.add(price)
        await db_session.commit()
        await db_session.refresh(price)

        assert price.id is not None
        assert price.symbol == sample_price_data["symbol"]
        assert price.close == sample_price_data["close"]

    async def test_sentiment_summary_model(self, db_session):
        """Test SentimentSummary model."""
        summary = SentimentSummary(
            timestamp=datetime.utcnow(),
            period_hours=24,
            positive_count=10,
            neutral_count=5,
            negative_count=3,
            total_articles=18,
            aggregate_score=0.45,
            confidence=0.87,
            source="test",
        )

        db_session.add(summary)
        await db_session.commit()
        await db_session.refresh(summary)

        assert summary.id is not None
        assert summary.total_articles == 18
        assert summary.aggregate_score == 0.45

    async def test_alert_model(self, db_session):
        """Test Alert model."""
        alert = Alert(
            timestamp=datetime.utcnow(),
            type="price_spike",
            severity="high",
            message="Gold price increased by 5%",
            alert_metadata={"change_pct": 5.0, "price": 2900.0},
        )

        db_session.add(alert)
        await db_session.commit()
        await db_session.refresh(alert)

        assert alert.id is not None
        assert alert.type == "price_spike"
        assert alert.alert_metadata["change_pct"] == 5.0

    async def test_news_query(self, db_session, sample_news_data):
        """Test querying news."""
        # Add multiple news items
        for i in range(3):
            news = News(
                url=f"https://example.com/article{i}",
                title=f"Article {i}",
                content=f"Content {i}",
                published=datetime.utcnow(),
                source="test",
            )
            db_session.add(news)

        await db_session.commit()

        # Query all news
        result = await db_session.execute(select(News))
        news_items = result.scalars().all()

        assert len(news_items) == 3
        assert all(n.source == "test" for n in news_items)

    async def test_price_query(self, db_session, sample_price_data):
        """Test querying prices."""
        # Add multiple price points
        for i in range(5):
            price = Price(
                timestamp=datetime.utcnow(),
                symbol="XAUUSD",
                open=2750.0 + i,
                high=2800.0 + i,
                low=2740.0 + i,
                close=2780.0 + i,
                volume=100000,
                change=30.0,
                change_pct=1.1,
            )
            db_session.add(price)

        await db_session.commit()

        # Query all prices
        result = await db_session.execute(select(Price))
        prices = result.scalars().all()

        assert len(prices) == 5
        assert all(p.symbol == "XAUUSD" for p in prices)

