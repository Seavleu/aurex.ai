# AUREX.AI - Product Requirement Document (PRD)
**Version:** 1.0  
**Date:** 2025-10-26  
**Owner:** Jenny (AI Engineer / CTO)  
**Methodology:** Agile (Scrum + Iterative Delivery)

## 1. Product Overview
**Goal:**  
Develop an AI intelligence system that analyzes global financial news and sentiment to predict XAUUSD (Gold/USD) price movements in real time.

**Mission:**  
Provide traders and analysts with actionable sentiment signals ahead of market reactions.

## 2. Core Objectives
1. Collect real-time macroeconomic and financial news data.  
2. Analyze sentiment using FinBERT and transformer models.  
3. Correlate sentiment with XAUUSD price movements.  
4. Visualize sentiment vs. price trends in a web dashboard.  
5. Expose public and private REST API endpoints.

## 3. Core Features
| Feature | Description | Priority |
|----------|--------------|----------|
| News Data Collector | Fetch and parse ForexFactory + Investing.com RSS feeds. | P0 |
| Sentiment Engine | FinBERT-based NLP sentiment analysis of news headlines. | P0 |
| Price Tracker | Fetch XAUUSD price data using yfinance. | P0 |
| Database Storage | Store news, sentiments, and prices in PostgreSQL. | P0 |
| Caching Layer | Redis for fast retrieval of latest data. | P1 |
| Dashboard UI | Next.js dashboard to visualize sentiment trends. | P1 |
| API Service | FastAPI endpoints for /sentiment, /price, /correlation. | P1 |
| Correlation Engine | Statistical analysis of sentiment-price relationships. | P2 |
| Alert System | Notify when sentiment diverges from market movement. | P3 |

## 4. Success Metrics (KPIs)
| Metric | Definition | Target |
|--------|-------------|---------|
| Sentiment Accuracy | Correct polarity prediction percentage | ≥ 85% |
| API Latency | Average response time (cached) | ≤ 150ms |
| Pipeline Uptime | Daily data ingestion uptime | ≥ 98% |
| Dashboard Load Time | Page render time | ≤ 2.5s |
| Sprint Velocity | Feature completion per sprint | ≥ 2 modules |

## 5. User Stories
**As a trader**, I want to see sentiment vs. price movement to predict volatility.  
**As a researcher**, I want access to aggregated sentiment data for backtesting.  
**As a system admin**, I want to monitor data freshness and API uptime.

## 6. Technical Requirements
**Backend:** Python 3.11, FastAPI, Transformers, yfinance, Prefect, SQLAlchemy, Redis-py  
**Frontend:** Next.js 15, TailwindCSS, Chart.js or Plotly  
**Database:** PostgreSQL with Timescale extension  
**Cache:** Redis (TTL: sentiment 30s, price 10s, news 5m)  
**Infra:** Docker + Railway.app + Vercel (free tier)  

## 7. System Architecture
Frontend (Next.js) → FastAPI Backend → Redis Cache + PostgreSQL  
Data Source → Prefect Pipeline → FinBERT Model → Database/Cache

## 8. Database Schema
**news**(id, title, source, timestamp, sentiment_label, sentiment_score)  
**price**(id, symbol, timestamp, price, change_pct)  
**sentiment**(id, avg_sentiment, timestamp, sample_size)

## 9. Implementation Plan (Sprints)
| Sprint | Goal | Deliverables |
|---------|------|--------------|
| Sprint 1 | Data ingestion MVP | News scraper, price fetcher, FinBERT inference |
| Sprint 2 | Backend foundation | FastAPI endpoints, Redis caching, DB schema |
| Sprint 3 | Frontend + Dashboard | Charts, API integration, sentiment-price UI |
| Sprint 4 | Correlation & Alerts | Correlation analytics, alert triggers |
| Sprint 5 | Optimization | CI/CD, logging, and deployment |

## 10. System Services
| Name | Language | Description |
|------|-----------|-------------|
| api-service | Python (FastAPI) | Exposes REST endpoints |
| pipeline-worker | Python (Prefect) | Scrapes and infers data |
| redis-service | Redis | Real-time cache |
| postgres-service | PostgreSQL | Persistent database |
| frontend-web | Next.js | Visualization dashboard |

## 11. Data Flow
RSS Feed + yfinance → Prefect Worker → FinBERT → Redis + Postgres → FastAPI → Next.js Dashboard

## 12. Agile Workflow
- Two-week sprints with defined deliverables.  
- Daily commits and iterative reviews in Cursor.  
- Branching: feature/{name}, fix/{bug}, chore/{infra}.  
- CI/CD auto-deployment to Railway + Vercel on merge to main.

## 13. Summary
| Area | Decision |
|------|-----------|
| Core Stack | FastAPI, Prefect, FinBERT, Redis, PostgreSQL, Next.js |
| Infra | Docker + Railway + Vercel |
| Architecture | Event-driven microservice |
| Methodology | Agile (Scrum-based) |
| Target | MVP in 6 weeks |

