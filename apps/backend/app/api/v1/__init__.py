"""AUREX.AI - API v1 Routes."""

from fastapi import APIRouter

from .alerts import router as alerts_router
from .health import router as health_router
from .news import router as news_router
from .price import router as price_router
from .sentiment import router as sentiment_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health_router, tags=["Health"])
api_router.include_router(price_router, prefix="/price", tags=["Price"])
api_router.include_router(news_router, prefix="/news", tags=["News"])
api_router.include_router(sentiment_router, prefix="/sentiment", tags=["Sentiment"])
api_router.include_router(alerts_router, prefix="/alerts", tags=["Alerts"])

__all__ = ["api_router"]

