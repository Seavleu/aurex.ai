# AUREX.AI 🚀

**AI-Driven Financial Sentiment Analysis & XAUUSD Price Prediction System**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-15-black.svg)](https://nextjs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📖 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [Roadmap](#roadmap)

---

## 🎯 Overview

AUREX.AI is an intelligent financial analysis system that:
- 📰 Collects real-time macroeconomic news from multiple sources
- 🤖 Analyzes sentiment using state-of-the-art FinBERT transformer model
- 📊 Correlates sentiment with XAUUSD (Gold/USD) price movements
- 📈 Provides actionable insights through a beautiful web dashboard
- 🚨 Alerts traders to sentiment-price divergences

**Mission:** Empower traders with AI-driven sentiment signals ahead of market reactions.

---

## ✨ Features

### Core Capabilities
- ✅ **Real-time Data Collection** - ForexFactory & Investing.com RSS feeds
- ✅ **AI Sentiment Analysis** - FinBERT-based NLP for financial text
- ✅ **Price Tracking** - XAUUSD price monitoring via yfinance
- ✅ **Correlation Engine** - Statistical analysis of sentiment-price relationships
- ✅ **Interactive Dashboard** - Real-time visualization with Next.js
- ✅ **REST API** - Public endpoints for data access
- ✅ **Caching Layer** - Redis for sub-200ms response times
- ✅ **Time-series Database** - PostgreSQL with TimescaleDB

### Coming Soon (Roadmap)
- 🔔 Alert system for divergence detection
- 📊 Advanced correlation analytics
- 🌍 Multi-asset support (EURUSD, BTCUSD)
- 🔐 API authentication & rate limiting
- 📱 Mobile app

---

## 🏗️ Architecture

```
┌─────────────────────────┐
│     Data Sources        │
│ (ForexFactory, NewsAPI) │
│    (yfinance - XAUUSD)  │
└───────────┬─────────────┘
            │
    [Prefect Pipeline]
            │
┌───────────┴────────────┐
│    ML Inference        │
│  (FinBERT Sentiment)   │
└───────────┬────────────┘
            │
    ┌───────┴───────┐
    │               │
[Redis Cache]  [PostgreSQL DB]
    │               │
    └───────┬───────┘
            │
    [FastAPI Backend]
            │
       [Next.js UI]
```

**See:** [Full Architecture Documentation](docs/architecture.md)

---

## 🛠️ Tech Stack

### Backend
- **API Framework:** FastAPI (async Python)
- **Workflow Orchestration:** Prefect 2.x
- **AI/ML:** Transformers (FinBERT), PyTorch
- **Database:** PostgreSQL + TimescaleDB
- **Cache:** Redis
- **ORM:** SQLAlchemy (async)

### Frontend
- **Framework:** Next.js 15 (App Router)
- **Styling:** TailwindCSS
- **Charts:** Chart.js / Plotly
- **Language:** TypeScript

### Infrastructure
- **Containerization:** Docker + Docker Compose
- **Backend Hosting:** Railway.app
- **Frontend Hosting:** Vercel
- **CI/CD:** GitHub Actions

---

## 🚀 Getting Started

### Prerequisites

- **Python:** 3.11 or higher
- **Node.js:** 18+ (for dashboard)
- **Docker:** 24+ with Docker Compose
- **Git:** 2.40+

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/your-org/aurex-ai.git
cd aurex-ai
```

#### 2. Set Up Environment Variables
```bash
cp env.example .env
# Edit .env with your configuration
```

#### 3. Start Services with Docker Compose
```bash
# Start all services (PostgreSQL, Redis, Backend, Pipeline)
docker-compose up -d

# View logs
docker-compose logs -f

# Check service health
docker-compose ps
```

#### 4. Set Up Python Environment (Local Development)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install
```

#### 5. Initialize Database
```bash
# Database is auto-initialized via init_db.sql
# To manually run migrations:
docker-compose exec backend alembic upgrade head
```

#### 6. Verify Installation
```bash
# Check API health
curl http://localhost:8000/health

# Check Prefect UI (optional)
open http://localhost:4200

# Check API documentation
open http://localhost:8000/docs
```

---

## 📁 Project Structure

```
aurex-ai/
├── apps/
│   ├── backend/          # FastAPI service
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core configuration
│   │   ├── models/       # Database models
│   │   ├── services/     # Business logic
│   │   └── tests/        # Backend tests
│   ├── pipeline/         # Prefect workers
│   │   ├── flows/        # Workflow definitions
│   │   ├── tasks/        # Individual tasks
│   │   └── tests/        # Pipeline tests
│   └── dashboard/        # Next.js UI
│       ├── app/          # App router pages
│       ├── components/   # React components
│       └── lib/          # Utilities
├── packages/
│   ├── ai_core/          # FinBERT & NLP utilities
│   ├── db_core/          # Database handlers
│   └── shared/           # Shared schemas & constants
├── infra/
│   ├── init_db.sql       # Database initialization
│   └── docker-compose.yml
├── docs/
│   ├── architecture.md   # Architecture specification
│   ├── prd.md            # Product requirements
│   ├── PRODUCT_BACKLOG.md # Agile backlog
│   └── SPRINT_PLANNING.md # Sprint tracking
├── requirements.txt      # Python dependencies
├── pyproject.toml        # Python project config
├── docker-compose.yml    # Service orchestration
└── README.md             # This file
```

---

## 💻 Development Workflow

### Agile Methodology

We follow **Agile Scrum** with 2-week sprints:

1. **Sprint Planning** - Define sprint goals and tasks
2. **Daily Standups** - Async via commits
3. **Sprint Review** - Demo completed features
4. **Retrospective** - Continuous improvement

**Current Sprint:** Sprint 0 - Project Setup  
**See:** [Sprint Planning](docs/SPRINT_PLANNING.md) | [Product Backlog](docs/PRODUCT_BACKLOG.md)

### Branching Strategy

```bash
# Feature branch
git checkout -b feature/sentiment-engine

# Bug fix branch
git checkout -b fix/cache-timeout

# Chore branch
git checkout -b chore/update-docs
```

### Code Quality

```bash
# Format code
black .

# Lint code
ruff check . --fix

# Run tests
pytest

# Run all checks
pre-commit run --all-files
```

### Running Services Locally

```bash
# Start only database and cache
docker-compose up postgres redis -d

# Run backend locally (with hot-reload)
cd apps/backend
uvicorn main:app --reload --port 8000

# Run pipeline worker locally
cd apps/pipeline
python -m prefect.cli agent start

# Run dashboard (in separate terminal)
cd apps/dashboard
npm install
npm run dev
```

---

## 📚 API Documentation

### Base URL
- **Local:** `http://localhost:8000`
- **Production:** `https://api.aurex.ai` (TBD)

### Endpoints

#### Get Latest Sentiment
```bash
GET /sentiment/latest
```
**Response:**
```json
{
  "avg_sentiment": 0.72,
  "positive_count": 15,
  "negative_count": 5,
  "neutral_count": 10,
  "timestamp": "2025-10-26T12:00:00Z"
}
```

#### Get Current Price
```bash
GET /price/current
```
**Response:**
```json
{
  "symbol": "XAUUSD",
  "price": 2050.50,
  "change_pct": 0.5,
  "timestamp": "2025-10-26T12:00:00Z"
}
```

#### Get Correlation
```bash
GET /correlation?window=24h
```

#### Get Recent News
```bash
GET /news/recent?limit=20
```

**Full API Docs:** `http://localhost:8000/docs` (Swagger UI)

---

## 🚢 Deployment

### Railway (Backend)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

### Vercel (Frontend)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd apps/dashboard
vercel --prod
```

### Environment Variables

Set these in Railway/Vercel dashboard:
- `DATABASE_URL`
- `REDIS_URL`
- `SECRET_KEY`
- `CORS_ORIGINS`

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Follow code quality standards** (Black, Ruff)
4. **Write tests** for new features
5. **Update documentation**
6. **Submit a Pull Request**

### Code of Conduct

- Write clean, maintainable code
- Add type hints and docstrings
- Test before committing
- Follow Agile practices

---

## 🗺️ Roadmap

### Sprint 1 (Weeks 1-2) ✅ In Progress
- [x] Data ingestion pipeline
- [x] FinBERT sentiment analysis
- [x] Price tracking
- [x] Prefect orchestration

### Sprint 2 (Weeks 3-4)
- [ ] FastAPI endpoints
- [ ] Redis caching
- [ ] Database integration
- [ ] API testing

### Sprint 3 (Weeks 5-6)
- [ ] Next.js dashboard
- [ ] Sentiment charts
- [ ] Price charts
- [ ] News feed

### Sprint 4 (Weeks 7-8)
- [ ] Correlation analytics
- [ ] Alert system
- [ ] WebSocket notifications

### Sprint 5 (Weeks 9-10)
- [ ] CI/CD pipeline
- [ ] Production deployment
- [ ] Performance optimization
- [ ] Security hardening

---

## 📊 Project Status

| Metric | Status |
|--------|--------|
| **Development Stage** | Sprint 0 - Setup |
| **Code Coverage** | TBD |
| **API Uptime** | TBD |
| **Test Pass Rate** | TBD |
| **Documentation** | 90% |

---

## 📧 Contact

**Project Lead:** Jenny (AI Engineer / CTO)  
**Repository:** [github.com/your-org/aurex-ai](https://github.com/your-org/aurex-ai)  
**Documentation:** [docs.aurex.ai](https://docs.aurex.ai)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **FinBERT** - ProsusAI for the financial sentiment model
- **FastAPI** - For the amazing async web framework
- **Prefect** - For workflow orchestration
- **TimescaleDB** - For time-series optimization
- **Community** - All contributors and supporters

---

## 🎯 Quick Links

- 📖 [Architecture Docs](docs/architecture.md)
- 📋 [Product Backlog](docs/PRODUCT_BACKLOG.md)
- 🏃 [Sprint Planning](docs/SPRINT_PLANNING.md)
- 🎨 [Cursor Rules](.cursor/rules/aurex-rules.mdc)
- 🐛 [Issue Tracker](https://github.com/your-org/aurex-ai/issues)

---

**Built with ❤️ using Cursor AI & Agile Methodology**

