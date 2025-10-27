"""
AUREX.AI - Real-Time Price Streamer

Continuously fetches gold prices and broadcasts to WebSocket clients.
Uses multiple data sources for redundancy.
"""

import asyncio
import os
import sys
from datetime import datetime
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from loguru import logger
import yfinance as yf

from packages.db_core.connection import db_manager
from packages.db_core.models import Price


class RealtimePriceStreamer:
    """Streams real-time gold prices."""
    
    def __init__(self, symbol: str = "GC=F", update_interval: float = 5.0):
        """
        Initialize the price streamer.
        
        Args:
            symbol: Gold futures symbol (GC=F for CME gold futures)
            update_interval: Seconds between price updates (lower = more real-time)
        """
        self.symbol = symbol
        self.update_interval = update_interval
        self.ticker = yf.Ticker(symbol)
        self.last_price = None
        self.last_update = None
        self.update_count = 0
        
        logger.info(f"RealtimePriceStreamer initialized for {symbol}")
        logger.info(f"Update interval: {update_interval} seconds")
    
    async def fetch_current_price(self) -> Optional[dict]:
        """Fetch current price from yfinance."""
        try:
            # Get fast info (current price)
            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(None, lambda: self.ticker.fast_info)
            
            if not info:
                return None
            
            current_price = float(info.get('lastPrice', 0))
            prev_close = float(info.get('previousClose', current_price))
            
            if current_price == 0:
                return None
            
            # Calculate change
            change = current_price - prev_close
            change_pct = (change / prev_close * 100) if prev_close > 0 else 0
            
            price_data = {
                "symbol": "XAUUSD",
                "timestamp": datetime.utcnow().isoformat(),
                "close": current_price,
                "open": prev_close,
                "high": current_price,
                "low": current_price,
                "volume": 0,
                "change": change,
                "change_pct": round(change_pct, 2),
                "source": "yfinance_realtime"
            }
            
            return price_data
        
        except Exception as e:
            logger.error(f"Error fetching price: {e}")
            return None
    
    async def store_price(self, price_data: dict) -> bool:
        """Store price in database."""
        try:
            async with db_manager.get_session() as session:
                price = Price(
                    symbol=price_data["symbol"],
                    timestamp=datetime.fromisoformat(price_data["timestamp"].replace("Z", "+00:00")),
                    open=price_data["open"],
                    high=price_data["high"],
                    low=price_data["low"],
                    close=price_data["close"],
                    volume=price_data.get("volume", 0),
                    change_pct=price_data.get("change_pct")
                )
                
                session.add(price)
                await session.commit()
            
            return True
        
        except Exception as e:
            logger.error(f"Error storing price: {e}")
            return False
    
    async def stream_prices(self, broadcast_callback=None):
        """
        Continuously stream prices.
        
        Args:
            broadcast_callback: Optional async function to broadcast prices
        """
        logger.info("=" * 70)
        logger.info("🚀 Real-Time Gold Price Streamer")
        logger.info("=" * 70)
        logger.info(f"📊 Symbol: {self.symbol} (XAUUSD)")
        logger.info(f"⏱️  Update interval: {self.update_interval} seconds")
        logger.info(f"💾 Database: Enabled")
        logger.info(f"📡 WebSocket: {'Enabled' if broadcast_callback else 'Disabled'}")
        logger.info("=" * 70)
        logger.info("⚡ Starting real-time price streaming...")
        logger.info("💡 Press Ctrl+C to stop")
        logger.info("")
        
        try:
            while True:
                # Fetch current price
                price_data = await self.fetch_current_price()
                
                if price_data:
                    self.update_count += 1
                    self.last_price = price_data["close"]
                    self.last_update = datetime.now()
                    
                    # Log update
                    change_symbol = "+" if price_data["change"] >= 0 else ""
                    logger.info(
                        f"#{self.update_count:04d} | ${price_data['close']:.2f} "
                        f"({change_symbol}{price_data['change']:.2f}, {change_symbol}{price_data['change_pct']:.2f}%)"
                    )
                    
                    # Store in database (async, don't block)
                    asyncio.create_task(self.store_price(price_data))
                    
                    # Broadcast to WebSocket clients
                    if broadcast_callback:
                        asyncio.create_task(broadcast_callback(price_data))
                
                # Wait before next update
                await asyncio.sleep(self.update_interval)
        
        except KeyboardInterrupt:
            logger.info("\n👋 Stopping price streamer...")
        except Exception as e:
            logger.error(f"Fatal error in price streamer: {e}")
            raise
        finally:
            await db_manager.close()


async def main():
    """Main entry point for standalone streaming."""
    # Update every 5 seconds for more real-time data
    streamer = RealtimePriceStreamer(update_interval=5.0)
    await streamer.stream_prices()


if __name__ == "__main__":
    asyncio.run(main())

