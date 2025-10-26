# 📚 AUREX.AI - API Documentation

## Base URL
```
http://localhost:8000
```

## Interactive Documentation
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 🔧 Health Endpoints

### GET /api/v1/health
Basic health check.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-27T12:00:00",
  "version": "1.0.0",
  "environment": "development"
}
```

### GET /api/v1/health/detailed
Detailed service health check.

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "database": {"status": "healthy", "type": "PostgreSQL"},
    "cache": {"status": "healthy", "type": "Redis"}
  }
}
```

---

## 💰 Price Endpoints

### GET /api/v1/price/latest
Get the latest gold price.

**Response:**
```json
{
  "status": "success",
  "data": {
    "id": "uuid",
    "timestamp": "2025-01-27T12:00:00",
    "symbol": "XAUUSD",
    "open": 2750.00,
    "high": 2800.00,
    "low": 2745.00,
    "close": 2780.00,
    "volume": 125000,
    "change": null,
    "change_pct": 1.09
  },
  "source": "database"
}
```

### GET /api/v1/price/history
Get historical prices with pagination.

**Parameters:**
- `hours` (int, default: 24): Hours of history (1-720)
- `page` (int, default: 1): Page number
- `page_size` (int, default: 100): Items per page (1-1000)

**Example:**
```
GET /api/v1/price/history?hours=24&page=1&page_size=100
```

**Response:**
```json
{
  "status": "success",
  "data": [...],
  "pagination": {
    "page": 1,
    "page_size": 100,
    "total_items": 288,
    "total_pages": 3
  }
}
```

### GET /api/v1/price/stats
Get price statistics for a period.

**Parameters:**
- `hours` (int, default: 24): Hours for statistics (1-720)

**Response:**
```json
{
  "status": "success",
  "data": {
    "period_hours": 24,
    "current_price": 2780.00,
    "high": 2800.00,
    "low": 2745.00,
    "average": 2772.50,
    "change": 30.00,
    "change_pct": 1.09,
    "data_points": 288
  }
}
```

---

## 📰 News Endpoints

### GET /api/v1/news/recent
Get recent news articles with sentiment.

**Parameters:**
- `hours` (int, default: 24): Hours of news (1-168)
- `page` (int, default: 1): Page number
- `page_size` (int, default: 20): Items per page (1-100)
- `source` (string, optional): Filter by source

**Example:**
```
GET /api/v1/news/recent?hours=24&page=1&page_size=20
```

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "id": "uuid",
      "url": "https://...",
      "title": "Gold prices surge...",
      "content": "Gold reached...",
      "published": "2025-01-27T12:00:00",
      "source": "ForexFactory",
      "sentiment_label": "positive",
      "sentiment_score": 0.85,
      "created_at": "2025-01-27T12:00:00"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total_items": 50,
    "total_pages": 3
  }
}
```

### GET /api/v1/news/{news_id}
Get a single news article by ID.

**Response:**
```json
{
  "status": "success",
  "data": {
    "id": "uuid",
    "url": "https://...",
    "title": "...",
    "content": "...",
    "published": "2025-01-27T12:00:00",
    "source": "ForexFactory",
    "sentiment_label": "positive",
    "sentiment_score": 0.85
  }
}
```

### GET /api/v1/news/sentiment/distribution
Get sentiment distribution of news.

**Parameters:**
- `hours` (int, default: 24): Hours to analyze

**Response:**
```json
{
  "status": "success",
  "data": {
    "distribution": {
      "positive": 15,
      "neutral": 10,
      "negative": 5
    },
    "percentages": {
      "positive": 50.0,
      "neutral": 33.33,
      "negative": 16.67
    },
    "total_articles": 30,
    "period_hours": 24
  }
}
```

---

## 🤖 Sentiment Endpoints

### GET /api/v1/sentiment/summary
Get the latest sentiment summary.

**Parameters:**
- `period_hours` (int, default: 24): Period in hours

**Response:**
```json
{
  "status": "success",
  "data": {
    "id": "uuid",
    "timestamp": "2025-01-27T12:00:00",
    "period_hours": 24,
    "positive_count": 15,
    "neutral_count": 10,
    "negative_count": 5,
    "total_articles": 30,
    "aggregate_score": 0.72,
    "confidence": 0.85,
    "distribution": {
      "positive": 15,
      "neutral": 10,
      "negative": 5
    },
    "percentages": {
      "positive": 50.0,
      "neutral": 33.33,
      "negative": 16.67
    }
  }
}
```

### GET /api/v1/sentiment/history
Get historical sentiment summaries.

**Parameters:**
- `hours` (int, default: 168): Hours of history
- `period_hours` (int, default: 24): Period for each summary
- `page` (int, default: 1): Page number
- `page_size` (int, default: 50): Items per page (1-200)

### GET /api/v1/sentiment/trend
Get sentiment trend analysis.

**Parameters:**
- `hours` (int, default: 168): Hours to analyze (24-720)

**Response:**
```json
{
  "status": "success",
  "data": {
    "trend": "improving",
    "change": 0.15,
    "average_first_half": 0.65,
    "average_second_half": 0.80,
    "data_points": 168,
    "period_hours": 168
  }
}
```

---

## 🔔 Alert Endpoints

### GET /api/v1/alerts
List alerts with filters.

**Parameters:**
- `hours` (int, default: 24): Hours of alerts
- `severity` (string, optional): Filter by severity (low/medium/high)
- `acknowledged` (bool, optional): Filter by acknowledgment status
- `page` (int, default: 1): Page number
- `page_size` (int, default: 50): Items per page (1-200)

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "id": "uuid",
      "timestamp": "2025-01-27T12:00:00",
      "type": "price_spike",
      "severity": "high",
      "message": "Gold price increased by 5%",
      "metadata": {"change_pct": 5.0},
      "acknowledged": false,
      "acknowledged_at": null
    }
  ]
}
```

### POST /api/v1/alerts
Create a new alert.

**Request Body:**
```json
{
  "type": "price_spike",
  "severity": "high",
  "message": "Gold price increased by 5%",
  "metadata": {"change_pct": 5.0}
}
```

### GET /api/v1/alerts/{alert_id}
Get an alert by ID.

### PATCH /api/v1/alerts/{alert_id}/acknowledge
Acknowledge an alert.

### DELETE /api/v1/alerts/{alert_id}
Delete an alert.

---

## 🔒 Error Responses

All endpoints return errors in this format:

```json
{
  "status": "error",
  "message": "Error description",
  "path": "/api/v1/endpoint"
}
```

**Status Codes:**
- `200` - Success
- `404` - Not Found
- `500` - Internal Server Error

---

## 📊 Rate Limiting

Currently no rate limiting is applied. In production:
- 100 requests per minute per IP
- 1000 requests per hour per IP

---

## 🔄 Caching

Endpoints use Redis caching with these TTLs:
- Price latest: 60 seconds
- Price history: 120 seconds
- News: 120 seconds
- Sentiment: 300 seconds

---

## 🧪 Testing Endpoints

### Using curl:
```bash
# Get latest price
curl http://localhost:8000/api/v1/price/latest

# Get recent news
curl "http://localhost:8000/api/v1/news/recent?hours=24"

# Get sentiment summary
curl http://localhost:8000/api/v1/sentiment/summary
```

### Using PowerShell:
```powershell
# Get latest price
Invoke-RestMethod http://localhost:8000/api/v1/price/latest

# Get recent news
Invoke-RestMethod "http://localhost:8000/api/v1/news/recent?hours=24"
```

---

## 📱 CORS

CORS is enabled for:
- `http://localhost:3000`
- `https://aurex-ai.vercel.app`

To add more origins, update `CORS_ORIGINS` in `.env`.

---

## 🐛 Troubleshooting

### 500 Internal Server Error
- Check backend logs: `docker logs aurex-backend`
- Verify database is running: `docker-compose ps postgres`
- Check Redis: `docker-compose ps redis`

### 404 Not Found
- Check endpoint path is correct
- Use `/docs` to see all available endpoints

### Empty Data Responses
- Run pipeline to populate data: `docker-compose up pipeline -d`
- Check database has data: `docker-compose exec postgres psql -U aurex -d aurex_db`

---

**For interactive documentation, visit:** http://localhost:8000/docs

