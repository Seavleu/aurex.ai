"""
AUREX.AI - Price Fetcher Task.

Fetches XAUUSD (Gold/USD) price data using yfinance and stores it in the database.
"""

import asyncio
from datetime import datetime

import yfinance as yf
from loguru import logger

from packages.db_core.cache import cache_manager
from packages.db_core.connection import db_manager
from packages.db_core.models import Price
from packages.shared.config import config
from packages.shared.constants import CACHE_KEY_PRICE_LATEST, SYMBOL_XAUUSD


class PriceFetcher:
    """Fetches and stores price data for financial instruments."""

    def __init__(self) -> None:
        """Initialize price fetcher."""
        self.symbol = config.YFINANCE_SYMBOL  # GC=F for Gold futures
        self.cache_ttl = config.CACHE_TTL_PRICE
        logger.info(f"PriceFetcher initialized for {self.symbol}")

    async def fetch_price(self) -> dict[str, any] | None:
        """
        Fetch current price from yfinance.

        Returns:
            dict: Price data or None if failed
        """
        try:
            logger.info(f"Fetching price for {self.symbol}")

            # yfinance is synchronous, run in executor
            loop = asyncio.get_event_loop()
            ticker = await loop.run_in_executor(None, yf.Ticker, self.symbol)
            info = await loop.run_in_executor(None, lambda: ticker.info)

            # Extract price data
            current_price = info.get("regularMarketPrice") or info.get("currentPrice")
            previous_close = info.get("previousClose", 0)

            if current_price is None:
                logger.error(f"No price data available for {self.symbol}")
                return None

            # Calculate change percentage
            change_pct = (
                ((current_price - previous_close) / previous_close * 100)
                if previous_close
                else 0
            )

            price_data = {
                "symbol": SYMBOL_XAUUSD,
                "price": float(current_price),
                "open": float(info.get("open", 0) or 0),
                "high": float(info.get("dayHigh", 0) or 0),
                "low": float(info.get("dayLow", 0) or 0),
                "close": float(info.get("previousClose", 0) or 0),
                "volume": int(info.get("volume", 0) or 0),
                "change_pct": round(change_pct, 2),
                "timestamp": datetime.utcnow(),
            }

            logger.info(
                f"Price fetched: {SYMBOL_XAUUSD} = ${current_price:.2f} "
                f"({change_pct:+.2f}%)",
            )
            return price_data

        except Exception as e:
            logger.error(f"Error fetching price for {self.symbol}: {e}")
            return None

    async def store_price(self, price_data: dict[str, any]) -> bool:
        """
        Store price data in database.

        Args:
            price_data: Price data dictionary

        Returns:
            bool: True if successful
        """
        try:
            async with db_manager.get_session() as session:
                price_record = Price(**price_data)
                session.add(price_record)
                await session.commit()

            logger.info(f"Price stored in database: {price_data['symbol']}")
            return True

        except Exception as e:
            logger.error(f"Error storing price: {e}")
            return False

    async def cache_price(self, price_data: dict[str, any]) -> bool:
        """
        Cache latest price in Redis.

        Args:
            price_data: Price data dictionary

        Returns:
            bool: True if successful
        """
        try:
            cache_data = {
                "symbol": price_data["symbol"],
                "price": price_data["price"],
                "change_pct": price_data["change_pct"],
                "timestamp": price_data["timestamp"].isoformat(),
            }

            await cache_manager.set(
                CACHE_KEY_PRICE_LATEST,
                cache_data,
                ttl=self.cache_ttl,
            )

            logger.info(f"Price cached: {cache_data['symbol']}")
            return True

        except Exception as e:
            logger.error(f"Error caching price: {e}")
            return False

    async def run(self) -> bool:
        """
        Run the price fetching task.

        Returns:
            bool: True if successful
        """
        try:
            # Fetch price
            price_data = await self.fetch_price()
            if price_data is None:
                return False

            # Store in database
            stored = await self.store_price(price_data)

            # Cache latest price
            cached = await self.cache_price(price_data)

            success = stored and cached
            if success:
                logger.info(f"✅ Price fetch completed: {price_data['symbol']}")
            else:
                logger.warning("⚠️  Price fetch partially failed")

            return success

        except Exception as e:
            logger.error(f"❌ Price fetch failed: {e}")
            return False


async def fetch_price_task() -> bool:
    """
    Standalone task function for Prefect.

    Returns:
        bool: True if successful
    """
    fetcher = PriceFetcher()
    return await fetcher.run()


async def main() -> None:
    """Main entry point for testing."""
    from packages.shared.logging_config import setup_logging

    setup_logging("price-fetcher", log_level="INFO")
    config.log_config()

    logger.info("Starting price fetcher...")

    # Run once
    fetcher = PriceFetcher()
    success = await fetcher.run()

    if success:
        logger.info("✅ Price fetch successful!")

        # Test cache retrieval
        cached_price = await cache_manager.get(CACHE_KEY_PRICE_LATEST)
        if cached_price:
            logger.info(f"Cached price: {cached_price}")
    else:
        logger.error("❌ Price fetch failed!")

    # Cleanup
    await db_manager.close()
    await cache_manager.close()


if __name__ == "__main__":
    asyncio.run(main())

