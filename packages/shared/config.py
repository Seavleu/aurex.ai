"""
AUREX.AI - Configuration Management.

Centralized configuration from environment variables.
"""

import os
from typing import Any

from loguru import logger
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Config:
    """Application configuration."""

    # Application
    APP_NAME: str = "AUREX.AI"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # API
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    CORS_ORIGINS: list[str] = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000,https://aurex-ai.vercel.app",
    ).split(",")

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://aurex:aurex_password@postgres:5432/aurex_db",
    )
    DATABASE_POOL_SIZE: int = int(os.getenv("DATABASE_POOL_SIZE", "20"))
    DATABASE_MAX_OVERFLOW: int = int(os.getenv("DATABASE_MAX_OVERFLOW", "0"))

    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CACHE_TTL_PRICE: int = int(os.getenv("CACHE_TTL_PRICE", "10"))
    CACHE_TTL_SENTIMENT: int = int(os.getenv("CACHE_TTL_SENTIMENT", "30"))
    CACHE_TTL_NEWS: int = int(os.getenv("CACHE_TTL_NEWS", "300"))

    # FinBERT Model
    FINBERT_MODEL_NAME: str = os.getenv("FINBERT_MODEL_NAME", "ProsusAI/finbert")
    MODEL_CACHE_DIR: str = os.getenv("MODEL_CACHE_DIR", "./models")
    DEVICE: str = os.getenv("DEVICE", "cpu")  # cpu or cuda
    INFERENCE_BATCH_SIZE: int = int(os.getenv("INFERENCE_BATCH_SIZE", "32"))

    # Data Sources
    YFINANCE_SYMBOL: str = os.getenv("YFINANCE_SYMBOL", "GC=F")  # XAUUSD
    PRICE_FETCH_INTERVAL: int = int(os.getenv("PRICE_FETCH_INTERVAL", "10"))  # seconds

    FOREXFACTORY_RSS_URL: str = os.getenv(
        "FOREXFACTORY_RSS_URL",
        "https://www.forexfactory.com/rss",
    )
    INVESTING_RSS_URL: str = os.getenv(
        "INVESTING_RSS_URL",
        "https://www.investing.com/rss/news.rss",
    )
    NEWS_FETCH_INTERVAL: int = int(os.getenv("NEWS_FETCH_INTERVAL", "300"))  # seconds

    # Sentiment Analysis
    SENTIMENT_POSITIVE_THRESHOLD: float = float(
        os.getenv("SENTIMENT_POSITIVE_THRESHOLD", "0.7"),
    )
    SENTIMENT_NEGATIVE_THRESHOLD: float = float(
        os.getenv("SENTIMENT_NEGATIVE_THRESHOLD", "0.7"),
    )

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-this")
    API_KEY: str = os.getenv("API_KEY", "your-api-key-here")

    # Feature Flags
    ENABLE_ALERTS: bool = os.getenv("ENABLE_ALERTS", "False").lower() == "true"
    ENABLE_CORRELATION_ANALYSIS: bool = (
        os.getenv("ENABLE_CORRELATION_ANALYSIS", "False").lower() == "true"
    )
    ENABLE_API_RATE_LIMITING: bool = (
        os.getenv("ENABLE_API_RATE_LIMITING", "True").lower() == "true"
    )

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """
        Get configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value
        """
        return getattr(cls, key, default)

    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production."""
        return cls.ENVIRONMENT.lower() == "production"

    @classmethod
    def is_development(cls) -> bool:
        """Check if running in development."""
        return cls.ENVIRONMENT.lower() == "development"

    @classmethod
    def log_config(cls) -> None:
        """Log current configuration (excluding secrets)."""
        logger.info("=" * 50)
        logger.info("AUREX.AI Configuration")
        logger.info("=" * 50)
        logger.info(f"Environment: {cls.ENVIRONMENT}")
        logger.info(f"Debug: {cls.DEBUG}")
        logger.info(f"Log Level: {cls.LOG_LEVEL}")
        logger.info(f"API Host: {cls.API_HOST}:{cls.API_PORT}")
        logger.info(f"Database: {cls.DATABASE_URL.split('@')[-1]}")  # Hide credentials
        logger.info(f"Redis: {cls.REDIS_URL.split('@')[-1]}")
        logger.info(f"FinBERT Model: {cls.FINBERT_MODEL_NAME}")
        logger.info(f"Device: {cls.DEVICE}")
        logger.info(f"Price Symbol: {cls.YFINANCE_SYMBOL}")
        logger.info("=" * 50)


# Global config instance
config = Config()

