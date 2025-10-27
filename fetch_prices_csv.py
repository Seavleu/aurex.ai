"""Fetch real gold prices and save to CSV."""
import yfinance as yf
import pandas as pd
from datetime import datetime

print("📊 Fetching real gold price data from Yahoo Finance...")

# Fetch gold futures data (GC=F)
gold = yf.Ticker("GC=F")

# Get 30 days of hourly data
hist = gold.history(period="1mo", interval="1h")

# Prepare data
prices = []
for index, row in hist.iterrows():
    close_price = float(row['Close'])
    prices.append({
        'symbol': 'XAUUSD',
        'timestamp': index.strftime('%Y-%m-%d %H:%M:%S'),
        'price': close_price,  # Same as close for current price
        'open': float(row['Open']),
        'high': float(row['High']),
        'low': float(row['Low']),
        'close': close_price,
        'volume': int(row['Volume']) if row['Volume'] else 0,
        'change_pct': 0.0
    })

df = pd.DataFrame(prices)
df.to_csv('gold_prices.csv', index=False)

print(f"Fetched {len(prices)} price records")
print(f"Saved to gold_prices.csv")

