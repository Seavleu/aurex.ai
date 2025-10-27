"""
AUREX.AI - Real-Time Gold Price Fetcher (Docker Version)
Runs inside Docker backend container with database access.
"""

import asyncio
import sys
from datetime import datetime
sys.path.insert(0, '/app')

import yfinance as yf
from loguru import logger
from sqlalchemy import text

from packages.db_core.connection import db_manager

# Configuration
FETCH_INTERVAL = 30  # seconds
SYMBOL_YF = "GC=F"  # Gold Futures
SYMBOL_DB = "XAUUSD"

logger.info(f"🚀 Real-Time Gold Fetcher starting...")


async def fetch_and_store_price():
    """Fetch current gold price and store in database."""
    try:
        # Fetch from Yahoo Finance
        ticker = yf.Ticker(SYMBOL_YF)
        hist = ticker.history(period="1d", interval="1m")
        
        if hist.empty:
            logger.warning("No data from Yahoo Finance")
            return False
        
        latest = hist.iloc[-1]
        previous = hist.iloc[-2] if len(hist) > 1 else latest
        
        change_pct = ((latest['Close'] - previous['Close']) / previous['Close']) * 100 if previous['Close'] > 0 else 0.0
        
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
        
        # Store in database
        async with db_manager.get_session() as session:
            insert_sql = text("""
                INSERT INTO price (symbol, timestamp, price, open, high, low, close, volume, change_pct)
                VALUES (:symbol, :timestamp, :price, :open, :high, :low, :close, :volume, :change_pct)
            """)
            await session.execute(insert_sql, price_data)
            await session.commit()
        
        logger.info(f"✅ ${price_data['price']:.2f} ({change_pct:+.2f}%) stored")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return False


async def run_forever():
    """Run fetcher continuously."""
    logger.info("=" * 60)
    logger.info(f"📊 Symbol: {SYMBOL_DB} ({SYMBOL_YF})")
    logger.info(f"⏱️  Interval: {FETCH_INTERVAL} seconds")
    logger.info("💡 Press Ctrl+C to stop")
    logger.info("=" * 60)
    
    fetch_count = 0
    success_count = 0
    
    while True:
        try:
            fetch_count += 1
            logger.info(f"📊 Fetch #{fetch_count}")
            
            if await fetch_and_store_price():
                success_count += 1
            
            logger.info(f"📈 Success: {success_count}/{fetch_count}")
            
        except KeyboardInterrupt:
            logger.info("⏹️  Stopped by user")
            break
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
        
        await asyncio.sleep(FETCH_INTERVAL)
    
    logger.info(f"Final: {success_count}/{fetch_count} successful")


if __name__ == "__main__":
    try:
        asyncio.run(run_forever())
    except KeyboardInterrupt:
        logger.info("Goodbye!")

