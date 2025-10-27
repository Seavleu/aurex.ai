"""
AUREX.AI - Professional Real-Time Gold Price Fetcher
Fetches XAUUSD data every 30 seconds and stores in database.
Works reliably with Yahoo Finance data.
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
SYMBOL_YF = "GC=F"  # Gold Futures on Yahoo Finance
SYMBOL_DB = "XAUUSD"  # Symbol stored in database

# Configure logger
logger.add("gold_fetcher.log", rotation="1 day", retention="7 days")


class GoldPriceFetcher:
    """Fetches and stores real-time gold price data."""
    
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.ticker = yf.Ticker(SYMBOL_YF)
        self.fetch_count = 0
        self.success_count = 0
        logger.info(f"✅ Gold Price Fetcher initialized for {SYMBOL_YF}")
    
    def fetch_current_price(self):
        """Fetch current gold price from Yahoo Finance."""
        try:
            # Get latest 1-minute data
            hist = self.ticker.history(period="1d", interval="1m")
            
            if hist.empty:
                logger.warning("⚠️  No data returned from Yahoo Finance")
                return None
            
            # Get the most recent candle
            latest = hist.iloc[-1]
            previous = hist.iloc[-2] if len(hist) > 1 else latest
            
            # Calculate change percentage
            if previous['Close'] > 0:
                change_pct = ((latest['Close'] - previous['Close']) / previous['Close']) * 100
            else:
                change_pct = 0.0
            
            price_data = {
                'symbol': SYMBOL_DB,
                'timestamp': datetime.utcnow(),
                'price': float(latest['Close']),
                'open': float(latest['Open']) if latest['Open'] else float(latest['Close']),
                'high': float(latest['High']) if latest['High'] else float(latest['Close']),
                'low': float(latest['Low']) if latest['Low'] else float(latest['Close']),
                'close': float(latest['Close']),
                'volume': int(latest['Volume']) if latest['Volume'] else 0,
                'change_pct': round(change_pct, 2)
            }
            
            logger.info(f"✅ ${price_data['price']:.2f} ({change_pct:+.2f}%) | Vol: {price_data['volume']:,}")
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
            
            logger.info(f"💾 Stored to database")
            return True
            
        except Exception as e:
            logger.error(f"❌ Database error: {e}")
            return False
    
    def fetch_and_store(self):
        """Fetch and store current price."""
        price_data = self.fetch_current_price()
        if price_data:
            return self.store_price(price_data)
        return False
    
    async def run_forever(self):
        """Run the fetcher continuously."""
        print("\n" + "=" * 70)
        print("🚀 AUREX.AI - Real-Time Gold Price Fetcher")
        print("=" * 70)
        print(f"📊 Symbol: {SYMBOL_DB} ({SYMBOL_YF})")
        print(f"⏱️  Interval: {FETCH_INTERVAL} seconds")
        print(f"💾 Database: {DATABASE_URL.split('@')[1]}")
        print(f"🌐 Dashboard: http://localhost:3000")
        print("=" * 70)
        print("\n⚡ Fetching real-time gold prices...")
        print("💡 Press Ctrl+C to stop\n")
        
        while True:
            try:
                self.fetch_count += 1
                current_time = datetime.now().strftime('%H:%M:%S')
                
                print(f"\r📊 Fetch #{self.fetch_count} at {current_time}...", end="", flush=True)
                logger.info(f"📊 Fetch #{self.fetch_count} at {current_time}")
                
                if self.fetch_and_store():
                    self.success_count += 1
                    print(f" ✅")
                else:
                    print(f" ❌")
                
                success_rate = (self.success_count / self.fetch_count * 100) if self.fetch_count > 0 else 0
                print(f"📈 Success: {self.success_count}/{self.fetch_count} ({success_rate:.1f}%)\n")
                
            except KeyboardInterrupt:
                print("\n\n⏹️  Stopped by user")
                break
            except Exception as e:
                logger.error(f"❌ Unexpected error: {e}")
                print(f" ❌ Error: {e}\n")
            
            # Wait before next fetch
            await asyncio.sleep(FETCH_INTERVAL)
        
        print("\n" + "=" * 70)
        print(f"📊 Final Stats: {self.success_count}/{self.fetch_count} successful fetches")
        print("👋 Fetcher stopped")
        print("=" * 70 + "\n")
    
    def close(self):
        """Close database connection."""
        self.engine.dispose()
        logger.info("Database connection closed")


async def main():
    """Main entry point."""
    fetcher = GoldPriceFetcher()
    
    try:
        await fetcher.run_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down gracefully...")
    finally:
        fetcher.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")

