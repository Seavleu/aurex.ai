"""
AUREX.AI - Shared Schemas.

Pydantic models for data validation and serialization.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class NewsArticle(BaseModel):
    """News article schema."""

    id: Optional[UUID] = None
    title: str = Field(..., min_length=1, max_length=500)
    source: str = Field(..., min_length=1, max_length=100)
    url: Optional[str] = None
    content: Optional[str] = None
    timestamp: datetime
    sentiment_label: Optional[str] = None
    sentiment_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    created_at: Optional[datetime] = None


class PriceData(BaseModel):
    """Price data schema."""

    id: Optional[UUID] = None
    symbol: str = Field(..., min_length=1, max_length=20)
    timestamp: datetime
    price: float = Field(..., gt=0)
    open: Optional[float] = Field(None, gt=0)
    high: Optional[float] = Field(None, gt=0)
    low: Optional[float] = Field(None, gt=0)
    close: Optional[float] = Field(None, gt=0)
    volume: Optional[int] = Field(None, ge=0)
    change_pct: Optional[float] = None


class SentimentSummary(BaseModel):
    """Sentiment summary schema."""

    id: Optional[UUID] = None
    timestamp: datetime
    avg_sentiment: float = Field(..., ge=-1.0, le=1.0)
    positive_count: int = Field(0, ge=0)
    negative_count: int = Field(0, ge=0)
    neutral_count: int = Field(0, ge=0)
    sample_size: int = Field(..., gt=0)
    symbol: str = Field("XAUUSD", min_length=1, max_length=20)


class SentimentResult(BaseModel):
    """Individual sentiment analysis result."""

    label: str = Field(..., pattern="^(positive|negative|neutral)$")
    score: float = Field(..., ge=0.0, le=1.0)


class CorrelationData(BaseModel):
    """Correlation analysis result."""

    correlation: float = Field(..., ge=-1.0, le=1.0)
    p_value: float = Field(..., ge=0.0, le=1.0)
    sample_size: int = Field(..., gt=0)
    time_window: str
    timestamp: datetime


class HealthCheck(BaseModel):
    """Health check response."""

    status: str = Field(..., pattern="^(healthy|unhealthy|degraded)$")
    service: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.now)


class APIResponse(BaseModel):
    """Generic API response wrapper."""

    success: bool
    message: str
    data: Optional[dict] = None
    timestamp: datetime = Field(default_factory=datetime.now)

