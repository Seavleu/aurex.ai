"""
AUREX.AI - Real-Time Data Fetcher using Alltick API
Fetches XAUUSD (Gold) data from Alltick professional market data API.
"""

import asyncio
import time
from datetime import datetime
import requests
from sqlalchemy import create_engine, text
from loguru import logger

# Configuration
ALLTICK_API_KEY = "73415b1086cbbd8ad10710e2ddb33729-c-app"
ALLTICK_BASE_URL = "https://quote.tradeswitcher.com"
DATABASE_URL = "postgresql://aurex:123456@localhost:5432/aurex_db"
FETCH_INTERVAL = 30  # seconds (Alltick supports real-time data)
SYMBOL = "XAUUSD"

# Configure logger
logger.add("alltick_fetcher.log", rotation="1 day", retention="7 days")


class AlltickDataFetcher:
    """Fetches and stores real-time gold price data from Alltick API."""
    
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.api_key = ALLTICK_API_KEY
        self.base_url = ALLTICK_BASE_URL
        self.headers = {
            "token": self.api_key,
            "Content-Type": "application/json"
        }
        logger.info(f"AlltickDataFetcher initialized for {SYMBOL}")
    
    def fetch_realtime_quote(self):
        """Fetch real-time quote from Alltick API."""
        try:
            # Alltick real-time quote endpoint
            url = f"{self.base_url}/api/quote/v1/realtime"
            
            # Request body with token
            payload = {
                "token": self.api_key,
                "symbol_list": [SYMBOL],
                "field_list": [
                    "latest_price",     # Current price
                    "open",             # Open price
                    "high",             # High price
                    "low",              # Low price
                    "prev_close",       # Previous close
                    "volume",           # Volume
                    "change",           # Price change
                    "change_ratio"      # Change percentage
                ]
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code != 200:
                logger.error(f"API error: {response.status_code} - {response.text}")
                return None
            
            data = response.json()
            
            # Check if data is valid
            if not data or "data" not in data:
                logger.warning("No data returned from API")
                return None
            
            quote_data = data.get("data", {})
            
            # Get XAUUSD data
            if SYMBOL not in quote_data:
                logger.warning(f"No data for {SYMBOL}")
                return None
            
            xauusd = quote_data[SYMBOL]
            
            # Extract price data
            latest_price = float(xauusd.get("latest_price", 0))
            if latest_price == 0:
                logger.warning("Invalid price data")
                return None
            
            open_price = float(xauusd.get("open", latest_price))
            high_price = float(xauusd.get("high", latest_price))
            low_price = float(xauusd.get("low", latest_price))
            prev_close = float(xauusd.get("prev_close", latest_price))
            volume = int(xauusd.get("volume", 0))
            change_ratio = float(xauusd.get("change_ratio", 0))
            
            price_data = {
                'symbol': 'XAUUSD',
                'timestamp': datetime.utcnow(),
                'price': latest_price,
                'open': open_price,
                'high': high_price,
                'low': low_price,
                'close': latest_price,  # Latest price is current close
                'volume': volume,
                'change_pct': round(change_ratio * 100, 2)  # Convert to percentage
            }
            
            logger.info(f"✅ Fetched: ${latest_price:.2f} ({change_ratio*100:+.2f}%) | Vol: {volume:,}")
            return price_data
            
        except requests.exceptions.Timeout:
            logger.error("⏱️  API request timeout")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ API request error: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Error fetching quote: {e}")
            return None
    
    def fetch_kline_data(self, period="1min", count=1):
        """Fetch K-line (candlestick) data from Alltick API."""
        try:
            url = f"{self.base_url}/api/quote/v1/kline"
            
            payload = {
                "token": self.api_key,
                "symbol_list": [SYMBOL],
                "period": period,  # 1min, 5min, 15min, 30min, 1hour, 1day, etc.
                "count": count
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code != 200:
                logger.error(f"K-line API error: {response.status_code}")
                return None
            
            data = response.json()
            
            if not data or "data" not in data:
                return None
            
            kline_data = data.get("data", {})
            
            if SYMBOL not in kline_data or not kline_data[SYMBOL]:
                return None
            
            # Get latest candle
            latest_candle = kline_data[SYMBOL][0]
            
            price_data = {
                'symbol': 'XAUUSD',
                'timestamp': datetime.fromtimestamp(latest_candle.get("timestamp", time.time())),
                'price': float(latest_candle.get("close", 0)),
                'open': float(latest_candle.get("open", 0)),
                'high': float(latest_candle.get("high", 0)),
                'low': float(latest_candle.get("low", 0)),
                'close': float(latest_candle.get("close", 0)),
                'volume': int(latest_candle.get("volume", 0)),
                'change_pct': 0.0
            }
            
            return price_data
            
        except Exception as e:
            logger.error(f"❌ Error fetching K-line: {e}")
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
            
            logger.info(f"💾 Stored: ${price_data['price']:.2f}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Database error: {e}")
            return False
    
    def fetch_and_store(self):
        """Fetch and store current price."""
        # Try real-time quote first
        price_data = self.fetch_realtime_quote()
        
        # Fallback to K-line if real-time fails
        if not price_data:
            logger.info("Trying K-line data as fallback...")
            price_data = self.fetch_kline_data()
        
        if price_data:
            return self.store_price(price_data)
        
        return False
    
    async def run_forever(self):
        """Run the fetcher continuously."""
        logger.info("=" * 70)
        logger.info("🚀 AUREX.AI - Alltick Real-Time Data Fetcher")
        logger.info("=" * 70)
        logger.info(f"📊 Symbol: {SYMBOL}")
        logger.info(f"🔑 API: Alltick Professional Market Data")
        logger.info(f"⏱️  Interval: {FETCH_INTERVAL} seconds")
        logger.info(f"💾 Database: {DATABASE_URL.split('@')[1]}")
        logger.info(f"🌐 Dashboard: http://localhost:3000")
        logger.info("=" * 70)
        logger.info("")
        logger.info("⚡ Fetching real-time XAUUSD prices from Alltick API...")
        logger.info("💡 Press Ctrl+C to stop")
        logger.info("")
        
        fetch_count = 0
        success_count = 0
        
        while True:
            try:
                fetch_count += 1
                current_time = datetime.now().strftime('%H:%M:%S')
                logger.info(f"📊 Fetch #{fetch_count} at {current_time}")
                
                if self.fetch_and_store():
                    success_count += 1
                
                success_rate = (success_count / fetch_count * 100) if fetch_count > 0 else 0
                logger.info(f"📈 Success: {success_count}/{fetch_count} ({success_rate:.1f}%)")
                logger.info("")
                
            except KeyboardInterrupt:
                logger.info("")
                logger.info("⏹️  Stopped by user")
                break
            except Exception as e:
                logger.error(f"❌ Unexpected error: {e}")
            
            # Wait before next fetch
            await asyncio.sleep(FETCH_INTERVAL)
        
        logger.info("")
        logger.info("=" * 70)
        logger.info(f"📊 Final Stats: {success_count}/{fetch_count} successful fetches")
        logger.info("👋 Fetcher stopped")
        logger.info("=" * 70)
    
    def close(self):
        """Close database connection."""
        self.engine.dispose()
        logger.info("Database connection closed")


async def main():
    """Main entry point."""
    print("\n" + "=" * 70)
    print("🚀 AUREX.AI - Alltick Real-Time Data Fetcher")
    print("=" * 70)
    print(f"📊 Symbol: {SYMBOL} (Gold Spot)")
    print(f"🔑 API Provider: Alltick Professional Market Data")
    print(f"⏱️  Fetch Interval: {FETCH_INTERVAL} seconds")
    print(f"💾 Database: {DATABASE_URL.split('@')[1]}")
    print(f"🌐 Dashboard: http://localhost:3000")
    print("=" * 70)
    print("\n⚡ Starting real-time gold price fetching...")
    print("💡 Press Ctrl+C to stop\n")
    
    fetcher = AlltickDataFetcher()
    
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

