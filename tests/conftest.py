"""
AUREX.AI - Pytest Configuration and Fixtures.
"""

import asyncio
import os
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from packages.db_core.models import Base

# Set test environment
os.environ["ENVIRONMENT"] = "test"
os.environ["DEBUG"] = "True"
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def db_engine():
    """Create a test database engine."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(db_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    async_session = sessionmaker(
        db_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session


@pytest.fixture
def sample_news_data():
    """Sample news data for testing."""
    return {
        "url": "https://example.com/article1",
        "title": "Gold prices surge to record highs",
        "content": "Gold reached $2800 per ounce today amid economic uncertainty.",
        "published": "2025-01-27T12:00:00Z",
        "source": "test_source",
    }


@pytest.fixture
def sample_price_data():
    """Sample price data for testing."""
    return {
        "symbol": "XAUUSD",
        "open": 2750.0,
        "high": 2825.0,
        "low": 2745.0,
        "close": 2800.0,
        "volume": 125000,
        "change": 50.0,
        "change_pct": 1.82,
    }


@pytest.fixture
def sample_sentiment_data():
    """Sample sentiment data for testing."""
    return {
        "label": "positive",
        "score": 0.92,
        "probabilities": {"positive": 0.92, "neutral": 0.06, "negative": 0.02},
    }

