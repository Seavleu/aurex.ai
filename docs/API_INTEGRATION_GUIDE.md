# 🚀 AUREX.AI - API Integration Guide

## ✅ Integrated APIs

### 1. NewsAPI - Gold News Fetching
**Status:** ✅ Fully Integrated & Working

- **API Key:** `7fb09c63f7d64edfa67acaf40e497218`
- **Purpose:** Fetch gold-related news articles for sentiment analysis
- **Library:** `newsapi-python` (already installed)

### 2. Alltick API - Real-time Price Data
**Status:** ⚠️ Requires Additional Configuration

- **API Key:** `73415b1086cbbd8ad10710e2ddb33729-c-app`
- **Purpose:** Fetch real-time XAUUSD price data
- **Note:** Experiencing authentication issues, needs debugging

---

## 📰 NewsAPI Integration

### How It Works

The news fetcher searches for gold-related articles using these keywords:
- `gold`
- `XAUUSD`
- `"gold spot"`
- `"gold prices"`

It fetches articles from the **last 24 hours** and analyzes their sentiment using FinBERT.

### Running News Fetcher

#### Option 1: Inside Docker (Recommended)

```bash
# Run news fetcher once inside the pipeline container
docker-compose exec pipeline python pipeline/fetch_news_with_sentiment.py

# Or run continuously (fetches every 60 minutes)
docker-compose exec pipeline sh -c "NEWS_FETCH_MODE=continuous python pipeline/fetch_news_with_sentiment.py"
```

#### Option 2: Via Prefect Pipeline

The news fetcher is already integrated into the Prefect pipeline. It will run automatically as part of the gold sentiment flow.

```bash
# Inside Docker
docker-compose exec pipeline python pipeline/main.py
```

### Verifying NewsAPI

Check the dashboard at `http://localhost:3000` - the News Feed section should show fresh articles.

### API Output Example

```
📰 Fetching gold-related news from NewsAPI...
✅ Fetched 45 articles from NewsAPI
💾 Storing articles in database...
✅ Stored 45 articles
🧠 Running sentiment analysis...
✅ Analyzed 45 articles

📊 Sentiment Statistics:
  POSITIVE: 18 (40.0%) | Avg score: 0.887
  NEGATIVE: 12 (26.7%) | Avg score: 0.823
  NEUTRAL: 15 (33.3%) | Avg score: 0.754
```

---

## 💰 Alltick API Integration

### Current Status

The Alltick API integration has been implemented but is experiencing authentication issues:

```
❌ API error: 401 - {"message":"Missing or wrong companyId in your request"}
```

### What's Implemented

- ✅ API client with proper authentication headers
- ✅ Real-time quote fetching
- ✅ K-line (candlestick) data fallback
- ✅ Automatic retry logic
- ✅ Database storage

### What's Needed

The API requires additional parameters that we don't currently have:
1. **companyId** - Not provided in the API key string
2. Possibly other authentication parameters

### Alternative: Yahoo Finance (Working)

For now, we're using Yahoo Finance (`yfinance`) as a reliable fallback:

```bash
# Run inside Docker
docker-compose exec backend python backend/fetch_realtime.py
```

This fetches real-time gold futures prices (GC=F) and stores them in the database.

---

## 🔧 Environment Configuration

Make sure your `.env` file includes:

```bash
# External APIs
NEWSAPI_KEY=7fb09c63f7d64edfa67acaf40e497218
ALLTICK_API_KEY=73415b1086cbbd8ad10710e2ddb33729-c-app

# Database (for Docker)
DATABASE_URL=postgresql+asyncpg://aurex:aurex_password@postgres:5432/aurex_db
REDIS_URL=redis://redis:6379/0
```

These are already configured in `docker-compose.yml`, so they work inside Docker containers.

---

## 📊 Complete Workflow

### Step 1: Start Services

```bash
docker-compose up -d
```

### Step 2: Fetch Gold News (with Sentiment)

```bash
docker-compose exec pipeline python pipeline/fetch_news_with_sentiment.py
```

**Expected Output:**
- ✅ Fetches 40-50 news articles from NewsAPI
- ✅ Stores them in the database
- ✅ Analyzes sentiment for each article
- ✅ Updates dashboard with fresh news

### Step 3: Fetch Real-time Prices

```bash
docker-compose exec backend python backend/fetch_realtime.py
```

**Expected Output:**
- ✅ Fetches real-time gold price every 30 seconds
- ✅ Stores in database
- ✅ Updates dashboard automatically

### Step 4: View Dashboard

Open `http://localhost:3000` to see:
- 📈 Latest gold prices
- 📰 Recent news with sentiment
- 📊 Sentiment trends
- 💹 Price history charts

---

## 🐛 Troubleshooting

### NewsAPI Issues

**Problem:** No articles fetched

**Solution:**
1. Check API key is valid: `echo $NEWSAPI_KEY`
2. Check internet connectivity inside Docker
3. Verify NewsAPI quota: https://newsapi.org/account

### Database Connection Issues

**Problem:** `password authentication failed`

**Solution:**
- ✅ Run scripts inside Docker (use `docker-compose exec`)
- ❌ Don't run local Python scripts (they can't authenticate)

### Dashboard Shows No Data

**Problem:** Dashboard is empty

**Solution:**
1. Check backend is running: `docker-compose ps`
2. Check backend logs: `docker-compose logs backend`
3. Verify database has data:
   ```bash
   docker-compose exec postgres psql -U aurex -d aurex_db -c "SELECT COUNT(*) FROM news;"
   ```

---

## 📈 What's Working Right Now

| Feature | Status | How to Use |
|---------|--------|------------|
| NewsAPI Integration | ✅ Working | `docker-compose exec pipeline python pipeline/fetch_news_with_sentiment.py` |
| Sentiment Analysis | ✅ Working | Automatic with news fetching |
| Yahoo Finance Prices | ✅ Working | `docker-compose exec backend python backend/fetch_realtime.py` |
| Dashboard Visualization | ✅ Working | `http://localhost:3000` |
| Alltick API | ⚠️ Needs Config | Requires additional auth parameters |

---

## 🎯 Next Steps

1. ✅ **Use NewsAPI** - Already working, fetch news anytime
2. ⚠️ **Debug Alltick API** - Need to contact Alltick support for `companyId` parameter
3. ✅ **Use Yahoo Finance** - Reliable fallback for real-time prices
4. ✅ **Automate Fetching** - Set up cron jobs or Prefect schedules

---

## 📞 API Support Contacts

### NewsAPI
- Website: https://newsapi.org
- Documentation: https://newsapi.org/docs
- Account: thelearningrate.team

### Alltick
- Website: https://alltick.co
- Documentation: https://alltick.co/docs
- Issue: Missing `companyId` parameter

---

## ✅ Summary

**What You Can Do Right Now:**

1. **Fetch real news about gold:**
   ```bash
   docker-compose exec pipeline python pipeline/fetch_news_with_sentiment.py
   ```

2. **Get sentiment analysis:**
   - Automatically included with news fetching
   - Uses FinBERT for financial sentiment

3. **View on dashboard:**
   - Go to `http://localhost:3000`
   - See live news feed with sentiment scores
   - See sentiment distribution and trends

4. **Fetch real-time prices:**
   ```bash
   docker-compose exec backend python backend/fetch_realtime.py
   ```

**Everything is ready to use! 🎉**

