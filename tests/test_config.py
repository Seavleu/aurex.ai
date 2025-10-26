"""
AUREX.AI - Configuration Tests.
"""

import pytest

from packages.shared.config import Config, config


class TestConfig:
    """Test configuration management."""

    def test_config_singleton(self):
        """Test that config is a singleton."""
        assert isinstance(config, Config)

    def test_environment_settings(self):
        """Test environment settings."""
        assert config.ENVIRONMENT in ["development", "production", "test"]
        assert isinstance(config.DEBUG, bool)
        assert config.LOG_LEVEL in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    def test_database_url(self):
        """Test database URL."""
        assert config.DATABASE_URL.startswith("postgresql+asyncpg://") or config.DATABASE_URL.startswith("sqlite")
        assert "aurex" in config.DATABASE_URL or "memory" in config.DATABASE_URL

    def test_api_settings(self):
        """Test API settings."""
        assert isinstance(config.API_HOST, str)
        assert isinstance(config.API_PORT, int)
        assert 1024 <= config.API_PORT <= 65535
        assert config.API_WORKERS >= 1

    def test_finbert_settings(self):
        """Test FinBERT settings."""
        assert config.FINBERT_MODEL_NAME == "ProsusAI/finbert"
        assert config.DEVICE in ["cpu", "gpu"]
        assert config.INFERENCE_BATCH_SIZE >= 1

    def test_gold_symbol(self):
        """Test gold symbol."""
        assert config.GOLD_SYMBOL == "GC=F"

    def test_pagination_settings(self):
        """Test pagination settings."""
        assert config.DEFAULT_PAGE_SIZE >= 1
        assert config.MAX_PAGE_SIZE >= config.DEFAULT_PAGE_SIZE

