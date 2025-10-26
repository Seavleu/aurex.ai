"""
AUREX.AI - Database Models.

SQLAlchemy ORM models for all database tables.
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    UUID,
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB

from .connection import Base


class News(Base):
    """News articles with sentiment analysis."""

    __tablename__ = "news"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(Text, nullable=False)
    source = Column(String(100), nullable=False)
    url = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    sentiment_label = Column(String(20), nullable=True)  # positive, negative, neutral
    sentiment_score = Column(Float, nullable=True)  # 0-1 confidence
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        """String representation."""
        return f"<News(id={self.id}, title='{self.title[:50]}...', sentiment={self.sentiment_label})>"


class Price(Base):
    """Price data for financial instruments."""

    __tablename__ = "price"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    symbol = Column(String(20), nullable=False, index=True)  # e.g., XAUUSD
    timestamp = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, index=True)
    price = Column(Float, nullable=False)
    open = Column(Float, nullable=True)
    high = Column(Float, nullable=True)
    low = Column(Float, nullable=True)
    close = Column(Float, nullable=True)
    volume = Column(BigInteger, nullable=True)
    change_pct = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    def __repr__(self) -> str:
        """String representation."""
        return f"<Price(symbol={self.symbol}, price={self.price}, timestamp={self.timestamp})>"


class SentimentSummary(Base):
    """Aggregated sentiment data."""

    __tablename__ = "sentiment_summary"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    timestamp = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, index=True)
    avg_sentiment = Column(Float, nullable=False)  # Average sentiment score
    positive_count = Column(Integer, default=0)
    negative_count = Column(Integer, default=0)
    neutral_count = Column(Integer, default=0)
    sample_size = Column(Integer, nullable=False)
    symbol = Column(String(20), default="XAUUSD", index=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"<SentimentSummary(symbol={self.symbol}, avg={self.avg_sentiment:.2f}, "
            f"samples={self.sample_size})>"
        )


class Alert(Base):
    """System alerts and notifications."""

    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    alert_type = Column(String(50), nullable=False)  # divergence, threshold_breach, etc.
    severity = Column(String(20), default="info")  # info, warning, critical
    message = Column(Text, nullable=False)
    alert_metadata = Column(JSONB, nullable=True)  # Additional context (renamed from metadata)
    timestamp = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, index=True)
    acknowledged = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    def __repr__(self) -> str:
        """String representation."""
        return f"<Alert(type={self.alert_type}, severity={self.severity}, ack={self.acknowledged})>"

