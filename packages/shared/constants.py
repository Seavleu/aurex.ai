"""
AUREX.AI - Shared Constants.

Global constants used across the application.
"""

# Application
APP_NAME = "AUREX.AI"
APP_VERSION = "1.0.0"

# Sentiment Labels
SENTIMENT_POSITIVE = "positive"
SENTIMENT_NEGATIVE = "negative"
SENTIMENT_NEUTRAL = "neutral"

# Symbols
SYMBOL_XAUUSD = "XAUUSD"
SYMBOL_GC_F = "GC=F"  # yfinance symbol for Gold futures

# Cache Keys
CACHE_KEY_PRICE_LATEST = "price:xauusd:latest"
CACHE_KEY_SENTIMENT_LATEST = "sentiment:xauusd:latest"
CACHE_KEY_NEWS_PREFIX = "news:forexfactory:"

# Cache TTL (seconds)
CACHE_TTL_PRICE = 10
CACHE_TTL_SENTIMENT = 30
CACHE_TTL_NEWS = 300

# API Endpoints
ENDPOINT_SENTIMENT_LATEST = "/sentiment/latest"
ENDPOINT_PRICE_CURRENT = "/price/current"
ENDPOINT_NEWS_RECENT = "/news/recent"
ENDPOINT_CORRELATION = "/correlation"

# News Sources
NEWS_SOURCE_FOREXFACTORY = "ForexFactory"
NEWS_SOURCE_INVESTING = "Investing.com"

# Model Configuration
FINBERT_MODEL_NAME = "ProsusAI/finbert"
INFERENCE_BATCH_SIZE = 32

# Time Windows
TIME_WINDOW_1H = "1h"
TIME_WINDOW_4H = "4h"
TIME_WINDOW_1D = "1d"
TIME_WINDOW_1W = "1w"

