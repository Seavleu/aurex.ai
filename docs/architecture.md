# AUREX.AI - System Architecture Specification
**Version:** 1.0  
**Date:** 2025-10-26  
**Owner:** Jenny (AI Engineer / CTO)  
**Architecture Type:** Modular AI-Centric Microservice  
**Methodology:** Agile (Scrum + Iterative Delivery)

---

## 1. Overview
AUREX.AI is a modular AI-driven analytics system that collects global financial news, analyzes sentiment, and correlates it with XAUUSD price movements in real time. The system emphasizes scalability, modularity, and low-latency delivery.

---

## 2. Architectural Goals
1. **Scalable** – support additional symbols or data sources.  
2. **Reliable** – ensure continuous data flow even if one service fails.  
3. **Performant** – sub-200ms API response with caching.  
4. **Maintainable** – modular microservices separated by responsibility.  
5. **Free-tier compatible** – optimized for Railway, Vercel, and free cloud tools.

---

## 3. High-Level Architecture

                ┌───────────────────────┐
                │     Data Sources      │
                │ ForexFactory, NewsAPI │
                │     yfinance (XAUUSD) │
                └──────────┬────────────┘
                           │
                    [Prefect Pipeline]
                           │
           ┌───────────────┴────────────────┐
           │         ML Inference           │
           │     (FinBERT Sentiment)        │
           └───────────────┬────────────────┘
                           │
               ┌───────────┴───────────┐
               │                       │
      [Redis Cache]            [PostgreSQL DB]
    (Recent data)             (Historical data)
               │                       │
               └───────────┬───────────┘
                           │
                     [FastAPI Backend]
                           │
               ┌───────────┴───────────┐
               │     REST Endpoints    │
               │  /sentiment /price    │
               └───────────┬───────────┘
                           │
                      [Next.js UI]
               (Dashboard Visualization)

---

## 4. Component Summary

| Component | Language | Function | Deployment |
|------------|-----------|-----------|-------------|
| **Pipeline Worker** | Python | Scrape, clean, and analyze news & prices via Prefect | Railway / Cron |
| **FinBERT Model Service** | Python | Transformer-based sentiment inference | Same container |
| **FastAPI Backend** | Python | REST API for sentiment, price, and correlation data | Railway |
| **Redis Cache** | Redis | Short-term data store for high-speed queries | Railway |
| **PostgreSQL Database** | SQL | Long-term storage for historical sentiment & prices | Railway |
| **Next.js Frontend** | TypeScript | Visualization dashboard | Vercel |

---

## 5. Data Flow

| Step | Source | Process | Destination |
|------|---------|----------|--------------|
| 1 | ForexFactory RSS | Prefect fetch & clean | Redis + Postgres |
| 2 | yfinance (XAUUSD) | Price tracking | Redis + Postgres |
| 3 | FinBERT model | Sentiment inference | Postgres |
| 4 | FastAPI | Expose `/sentiment`, `/price`, `/correlation` | Next.js |
| 5 | Next.js | Visualize charts and correlations | User |

---

## 6. Database Schema (Simplified)

**news**  
- id (UUID)  
- title (TEXT)  
- source (TEXT)  
- timestamp (TIMESTAMP)  
- sentiment_label (VARCHAR)  
- sentiment_score (FLOAT)

**price**  
- id (UUID)  
- symbol (VARCHAR)  
- timestamp (TIMESTAMP)  
- price (FLOAT)  
- change_pct (FLOAT)

**sentiment_summary**  
- id (UUID)  
- avg_sentiment (FLOAT)  
- timestamp (TIMESTAMP)  
- sample_size (INT)

---

## 7. Caching Strategy
| Data Type | Cache TTL | Source |
|------------|------------|--------|
| Price Data | 10s | yfinance |
| News Headlines | 5m | ForexFactory |
| Sentiment Results | 30s | FinBERT |

Redis keys follow namespace convention:
price:xauusd:latest
news:forexfactory:{id}
sentiment:xauusd:summary

---

## 8. API Endpoints
| Method | Route | Description |
|--------|--------|-------------|
| GET | /sentiment/latest | Latest sentiment summary |
| GET | /price/current | Current XAUUSD price |
| GET | /correlation | Correlation between sentiment & price |
| GET | /news/recent | Recent analyzed headlines |

---

## 9. Deployment Strategy
- **Backend:** Dockerized FastAPI + Redis + PostgreSQL on Railway  
- **Frontend:** Next.js deployed via Vercel  
- **CI/CD:** GitHub → Cursor automation → Railway/Vercel deploy on merge  
- **Secrets:** Managed via Railway environment variables  
- **Monitoring:** Prefect cloud dashboard + Railway metrics  

---

## 10. Scalability Plan
1. Convert Prefect pipeline into distributed workers.  
2. Add message queue (RabbitMQ or Kafka) for scaling.  
3. Introduce vector DB (Qdrant) for semantic clustering.  
4. Add model fine-tuning for domain-specific sentiment.  
5. Expand to other pairs (e.g., EURUSD, BTCUSD).

---

## 11. Security Considerations
- All API keys stored in Railway secrets.  
- CORS restricted to Vercel domain.  
- Rate limiting on public endpoints.  
- Redis & Postgres behind private network.

---

## 12. Agile Implementation
- **Sprint 1:** Data ingestion + FinBERT inference  
- **Sprint 2:** FastAPI core + Redis integration  
- **Sprint 3:** Dashboard and visualization  
- **Sprint 4:** Correlation and alerts  
- **Sprint 5:** Deployment and CI/CD optimization  

---

## 13. Summary
| Category | Choice |
|-----------|---------|
| **Architecture** | AI-centric modular microservices |
| **Core Stack** | FastAPI + Prefect + FinBERT + Redis + PostgreSQL + Next.js |
| **Hosting** | Railway (backend) + Vercel (frontend) |
| **Pipeline** | Prefect with scheduled cron jobs |
| **Methodology** | Agile / Scrum |
| **Target Delivery** | MVP in 6 weeks |

---
