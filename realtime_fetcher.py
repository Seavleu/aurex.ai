"""
AUREX.AI - Real-Time Data Fetcher
Continuously fetches gold price and news data every 30 seconds.
"""

import asyncio
import time
from datetime import datetime
import yfinance as yf
from sqlalchemy import create_engine, text
from loguru import logger

# Configuration
DATABASE_URL = "postgresql://aurex:123456@localhost:5432/aurex_db"
FETCH_INTERVAL = 30  # seconds
SYMBOL = "GC=F"  # Gold Futures

# Configure logger
logger.add("realtime_fetcher.log", rotation="1 day", retention="7 days")

class RealtimeDataFetcher:
    """Fetches and stores real-time gold price data."""
    
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.gold = yf.Ticker(SYMBOL)
        logger.info("RealtimeDataFetcher initialized")
    
    def fetch_current_price(self):
        """Fetch current gold price from yfinance."""
        try:
            # Get current price data
            info = self.gold.info
            current_price = info.get("regularMarketPrice") or info.get("currentPrice")
            
            if not current_price:
                logger.warning("No current price available")
                return None
            
            # Get latest price data
            hist = self.gold.history(period="1d", interval="1m")
            if hist.empty:
                logger.warning("No historical data available")
                return None
            
            latest = hist.iloc[-1]
            previous = hist.iloc[-2] if len(hist) > 1 else latest
            
            # Calculate change
            change_pct = ((latest['Close'] - previous['Close']) / previous['Close'] * 100) if previous['Close'] else 0
            
            price_data = {
                'symbol': 'XAUUSD',
                'timestamp': datetime.utcnow(),
                'price': float(latest['Close']),
                'open': float(latest['Open']) if latest['Open'] else float(latest['Close']),
                'high': float(latest['High']) if latest['High'] else float(latest['Close']),
                'low': float(latest['Low']) if latest['Low'] else float(latest['Close']),
                'close': float(latest['Close']),
                'volume': int(latest['Volume']) if latest['Volume'] else 0,
                'change_pct': round(change_pct, 2)
            }
            
            logger.info(f"✅ Fetched price: ${price_data['price']:.2f} ({price_data['change_pct']:+.2f}%)")
            return price_data
            
        except Exception as e:
            logger.error(f"❌ Error fetching price: {e}")
            return None
    
    def store_price(self, price_data):
        """Store price data in database."""
        try:
            with self.engine.connect() as conn:
                insert_sql = text("""
                    INSERT INTO price (symbol, timestamp, price, open, high, low, close, volume, change_pct)
                    VALUES (:symbol, :timestamp, :price, :open, :high, :low, :close, :volume, :change_pct)
                """)
                conn.execute(insert_sql, price_data)
                conn.commit()
            
            logger.info(f"💾 Stored price: ${price_data['price']:.2f}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error storing price: {e}")
            return False
    
    def fetch_and_store(self):
        """Fetch and store current price."""
        price_data = self.fetch_current_price()
        if price_data:
            return self.store_price(price_data)
        return False
    
    async def run_forever(self):
        """Run the fetcher continuously."""
        logger.info("🚀 Starting real-time data fetcher...")
        logger.info(f"⏱️  Fetch interval: {FETCH_INTERVAL} seconds")
        
        fetch_count = 0
        success_count = 0
        
        while True:
            try:
                fetch_count += 1
                logger.info(f"📊 Fetch #{fetch_count} at {datetime.now().strftime('%H:%M:%S')}")
                
                if self.fetch_and_store():
                    success_count += 1
                
                logger.info(f"📈 Success rate: {success_count}/{fetch_count} ({success_count/fetch_count*100:.1f}%)")
                
            except KeyboardInterrupt:
                logger.info("⏹️  Stopped by user")
                break
            except Exception as e:
                logger.error(f"❌ Unexpected error: {e}")
            
            # Wait before next fetch
            await asyncio.sleep(FETCH_INTERVAL)
    
    def close(self):
        """Close database connection."""
        self.engine.dispose()
        logger.info("Database connection closed")


async def main():
    """Main entry point."""
    print("\n" + "=" * 60)
    print("🚀 AUREX.AI - Real-Time Data Fetcher")
    print("=" * 60)
    print(f"📊 Symbol: {SYMBOL} (Gold Futures)")
    print(f"⏱️  Interval: {FETCH_INTERVAL} seconds")
    print(f"💾 Database: {DATABASE_URL.split('@')[1]}")
    print(f"🌐 Dashboard: http://localhost:3000")
    print("=" * 60)
    print("\n⚡ Fetching real-time gold prices...")
    print("💡 Press Ctrl+C to stop\n")
    
    fetcher = RealtimeDataFetcher()
    
    try:
        await fetcher.run_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down gracefully...")
    finally:
        fetcher.close()
        print("✅ Fetcher stopped.\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")


