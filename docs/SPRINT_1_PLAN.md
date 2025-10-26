# Sprint 1: Data Ingestion MVP - Development Plan

**Sprint Duration:** Weeks 1-2  
**Status:** 🚀 In Progress  
**Goal:** Build data ingestion pipeline with AI sentiment analysis

---

## ✅ Prerequisites Complete

| Component | Status | Details |
|-----------|--------|---------|
| Docker Services | ✅ Running | All 5 containers healthy |
| Backend API | ✅ Running | http://localhost:8000 |
| PostgreSQL | ✅ Running | TimescaleDB ready |
| Redis | ✅ Running | Cache ready |
| Prefect | ✅ Running | UI at http://localhost:4200 |
| API Docs | ✅ Accessible | http://localhost:8000/docs |

---

## 🎯 Sprint 1 Goals (21 Story Points)

### US-101: XAUUSD Price Fetcher (5 pts) 🔄
**Priority:** P0  
**Status:** Ready to start

**Tasks:**
1. Create `packages/shared/config.py` - Configuration management
2. Create `apps/pipeline/tasks/fetch_price.py` - Price fetching logic
3. Implement yfinance integration for XAUUSD (GC=F)
4. Add error handling and retry logic
5. Store price data in PostgreSQL
6. Cache latest price in Redis
7. Write unit tests

**Acceptance Criteria:**
- ✅ Fetches XAUUSD price every 10 seconds
- ✅ Handles API failures gracefully
- ✅ Logs all fetch attempts
- ✅ Data stored in PostgreSQL `price` table
- ✅ Latest price cached in Redis

---

### US-102: ForexFactory News Scraper (5 pts)
**Priority:** P0  
**Status:** Pending

**Tasks:**
1. Create `apps/pipeline/tasks/fetch_news.py`
2. Implement RSS feed parser for ForexFactory
3. Extract headline, timestamp, source
4. Add deduplication logic
5. Store in PostgreSQL `news` table
6. Handle parsing errors
7. Write unit tests

**Acceptance Criteria:**
- ✅ Fetches news headlines every 5 minutes
- ✅ Filters duplicate articles
- ✅ Extracts title, timestamp, source

---

### US-103: FinBERT Sentiment Analysis (8 pts)
**Priority:** P0  
**Status:** Pending

**Tasks:**
1. Create `packages/ai_core/sentiment.py`
2. Load FinBERT model (ProsusAI/finbert)
3. Implement sentiment inference function
4. Add batch processing (32 headlines at a time)
5. Cache model in memory
6. Store results in PostgreSQL
7. Write integration tests

**Acceptance Criteria:**
- ✅ Classifies sentiment as positive/negative/neutral
- ✅ Returns confidence scores (0-1)
- ✅ Processes batches of 32 headlines
- ✅ 85%+ accuracy on test data

---

### US-104: Prefect Workflow Orchestration (5 pts)
**Priority:** P1  
**Status:** Pending

**Tasks:**
1. Create `apps/pipeline/flows/price_flow.py`
2. Create `apps/pipeline/flows/news_flow.py`
3. Create `apps/pipeline/flows/sentiment_flow.py`
4. Set up flow scheduling
5. Add monitoring and alerts
6. Configure Prefect deployment

**Acceptance Criteria:**
- ✅ Flows run on schedule without intervention
- ✅ Failures are logged and retried
- ✅ Visible in Prefect UI

---

## 📁 Files to Create (Sprint 1)

### Configuration
```
packages/shared/
├── config.py          # Configuration management
└── utils.py           # Shared utilities
```

### Database Layer
```
packages/db_core/
├── connection.py      # Database connection pool
├── models.py          # SQLAlchemy ORM models
├── repositories/
│   ├── price_repo.py
│   ├── news_repo.py
│   └── sentiment_repo.py
└── cache.py           # Redis cache utilities
```

### AI/ML Layer
```
packages/ai_core/
├── sentiment.py       # FinBERT sentiment analyzer
├── model_loader.py    # Model management
└── preprocessing.py   # Text preprocessing
```

### Pipeline Tasks
```
apps/pipeline/
├── tasks/
│   ├── fetch_price.py    # US-101
│   ├── fetch_news.py     # US-102
│   └── analyze_sentiment.py  # US-103
├── flows/
│   ├── price_flow.py     # US-104
│   ├── news_flow.py      # US-104
│   └── sentiment_flow.py # US-104
└── main.py               # Updated entry point
```

### Tests
```
apps/pipeline/tests/
├── test_fetch_price.py
├── test_fetch_news.py
├── test_sentiment.py
└── test_flows.py

packages/ai_core/tests/
└── test_sentiment.py

packages/db_core/tests/
├── test_models.py
└── test_repositories.py
```

---

## 🚀 Development Order

### Phase 1: Foundation (Days 1-2)
1. ✅ Set up database connection utilities
2. ✅ Create ORM models
3. ✅ Create configuration management
4. ✅ Test database connectivity

### Phase 2: Price Fetcher (Days 3-4) 🔄 **START HERE**
1. Implement yfinance price fetcher
2. Create price repository
3. Test price storage
4. Add Redis caching
5. Write tests

### Phase 3: News Scraper (Days 5-6)
1. Implement ForexFactory RSS parser
2. Create news repository
3. Add deduplication
4. Write tests

### Phase 4: Sentiment Analysis (Days 7-9)
1. Load FinBERT model
2. Implement inference logic
3. Test on sample data
4. Optimize batch processing

### Phase 5: Orchestration (Days 10-12)
1. Create Prefect flows
2. Set up scheduling
3. Test end-to-end pipeline
4. Deploy to Prefect server

### Phase 6: Testing & Polish (Days 13-14)
1. Integration testing
2. Performance optimization
3. Documentation
4. Sprint review prep

---

## 🧪 Testing Strategy

### Unit Tests
- Each function tested independently
- Mock external dependencies (yfinance, RSS feeds)
- Fast execution (< 1 second each)

### Integration Tests
- Database operations
- Redis caching
- Model inference
- End-to-end flow

### Performance Tests
- Price fetch latency < 2s
- News processing < 30s for 100 articles
- Sentiment inference < 5s for 32 headlines

---

## 📊 Success Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Price Fetch Success Rate | ≥95% | Monitor logs |
| News Articles/Day | ≥100 | Count DB records |
| Sentiment Accuracy | ≥85% | Manual validation |
| Pipeline Uptime | ≥98% | Prefect dashboard |
| Test Coverage | ≥80% | pytest --cov |

---

## 🔍 Monitoring

### Logs to Track
- Price fetch attempts and failures
- News articles processed
- Sentiment inference results
- Database write operations
- Redis cache hits/misses

### Prefect Dashboard
- http://localhost:4200
- Monitor flow runs
- Track task failures
- View execution times

---

## 🐛 Known Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| yfinance API rate limits | High | Add caching, throttling |
| ForexFactory changes RSS format | Medium | Monitor and adapt parser |
| FinBERT model too large | High | Use CPU, consider quantization |
| Database connection limits | Medium | Use connection pooling |

---

## 📚 Resources

### Documentation
- yfinance: https://pypi.org/project/yfinance/
- FinBERT: https://huggingface.co/ProsusAI/finbert
- Prefect: https://docs.prefect.io/
- SQLAlchemy: https://docs.sqlalchemy.org/

### Existing Code
- Database schema: `infra/init_db.sql`
- Shared schemas: `packages/shared/schemas.py`
- Constants: `packages/shared/constants.py`

---

## 🎯 Next Immediate Actions

### RIGHT NOW - Start US-101: Price Fetcher

1. **Create database utilities:**
   ```bash
   # Create connection manager
   packages/db_core/connection.py
   packages/db_core/models.py
   ```

2. **Create price fetcher:**
   ```bash
   # Implement price fetching
   apps/pipeline/tasks/fetch_price.py
   ```

3. **Test it works:**
   ```bash
   # Run price fetcher
   python apps/pipeline/tasks/fetch_price.py
   ```

---

## 📝 Daily Standup Format

**What did I complete yesterday?**
- [List completed tasks]

**What will I work on today?**
- [List planned tasks]

**Any blockers?**
- [List any issues]

---

## 🎉 Sprint 1 Definition of Done

- [ ] All 4 user stories completed
- [ ] 21 story points delivered
- [ ] Test coverage ≥ 80%
- [ ] No critical bugs
- [ ] Code reviewed and merged
- [ ] Documentation updated
- [ ] Pipeline running autonomously
- [ ] Data flowing into database

---

**Status:** 🚀 Ready to begin US-101  
**Next File to Create:** `packages/db_core/connection.py`  
**Estimated Completion:** 2 weeks from start

Let's build! 💪

