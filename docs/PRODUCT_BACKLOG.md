# AUREX.AI - Product Backlog
**Version:** 1.0  
**Last Updated:** 2025-10-26  
**Maintained By:** CTO / Scrum Master

---

## 🎯 Product Vision
Build an AI intelligence system that analyzes global financial news sentiment to predict XAUUSD price movements in real-time.

---

## 📈 Sprint Overview

| Sprint | Duration | Goal | Status |
|--------|----------|------|--------|
| Sprint 0 | Week 0 | Project setup & infrastructure | 🔄 Planned |
| Sprint 1 | Weeks 1-2 | Data ingestion MVP | 📋 Ready |
| Sprint 2 | Weeks 3-4 | Backend foundation | 📋 Ready |
| Sprint 3 | Weeks 5-6 | Frontend & Dashboard | 📋 Ready |
| Sprint 4 | Weeks 7-8 | Correlation & Alerts | 📋 Ready |
| Sprint 5 | Weeks 9-10 | Optimization & Deployment | 📋 Ready |

---

## 🏗️ SPRINT 0: Project Setup & Infrastructure (Week 0)

### Epic: Development Environment Setup
**Story Points:** 8

#### User Stories:

**US-001: As a developer, I want a standardized project structure so that the codebase is maintainable**
- **Tasks:**
  - [ ] Create monorepo folder structure (apps/, packages/, infra/)
  - [ ] Set up Python virtual environment and package management
  - [ ] Create requirements.txt with all dependencies
  - [ ] Set up .env.example for environment variables
  - [ ] Create .gitignore for Python, Node.js, and IDE files
- **Acceptance Criteria:**
  - All folders follow architecture spec
  - Dependencies are versioned and documented
- **Story Points:** 3

**US-002: As a developer, I want Docker Compose configuration so that I can run services locally**
- **Tasks:**
  - [ ] Create docker-compose.yml with all services
  - [ ] Configure PostgreSQL service with init scripts
  - [ ] Configure Redis service with proper volumes
  - [ ] Set up FastAPI service container
  - [ ] Set up network and volume configurations
- **Acceptance Criteria:**
  - `docker-compose up` starts all services
  - Services can communicate with each other
- **Story Points:** 3

**US-003: As a developer, I want code quality tools configured so that code remains consistent**
- **Tasks:**
  - [ ] Set up Black formatter configuration
  - [ ] Set up Ruff linter configuration
  - [ ] Create pre-commit hooks configuration
  - [ ] Set up pytest configuration
  - [ ] Create GitHub Actions workflow templates
- **Acceptance Criteria:**
  - Black and Ruff run without errors
  - Pre-commit hooks enforce standards
- **Story Points:** 2

---

## 📊 SPRINT 1: Data Ingestion MVP (Weeks 1-2)

### Epic: Data Collection Pipeline
**Story Points:** 21

#### User Stories:

**US-101: As a system, I want to fetch XAUUSD price data so that I can track real-time market movements**
- **Tasks:**
  - [ ] Create price fetcher using yfinance
  - [ ] Implement async price polling function
  - [ ] Add error handling and retry logic
  - [ ] Write unit tests for price fetcher
  - [ ] Add logging for price updates
- **Acceptance Criteria:**
  - Fetches XAUUSD price every 10 seconds
  - Handles API failures gracefully
  - Logs all fetch attempts
- **Story Points:** 5
- **Priority:** P0

**US-102: As a system, I want to scrape ForexFactory news so that I can analyze financial sentiment**
- **Tasks:**
  - [ ] Create ForexFactory RSS parser
  - [ ] Implement news headline extraction
  - [ ] Add deduplication logic
  - [ ] Handle parsing errors
  - [ ] Write unit tests for scraper
- **Acceptance Criteria:**
  - Fetches news headlines every 5 minutes
  - Filters duplicate articles
  - Extracts title, timestamp, source
- **Story Points:** 5
- **Priority:** P0

**US-103: As a system, I want to analyze sentiment using FinBERT so that I can classify news polarity**
- **Tasks:**
  - [ ] Set up FinBERT model loading
  - [ ] Create sentiment inference function
  - [ ] Implement batch processing for efficiency
  - [ ] Add model caching
  - [ ] Write integration tests
- **Acceptance Criteria:**
  - Classifies sentiment as positive/negative/neutral
  - Returns confidence scores
  - Processes batches of 32 headlines
- **Story Points:** 8
- **Priority:** P0

**US-104: As a system, I want Prefect workflows orchestrating data collection so that pipelines run reliably**
- **Tasks:**
  - [ ] Create Prefect flow for news collection
  - [ ] Create Prefect flow for price collection
  - [ ] Create Prefect flow for sentiment analysis
  - [ ] Set up flow scheduling
  - [ ] Add flow monitoring and alerts
- **Acceptance Criteria:**
  - Flows run on schedule without intervention
  - Failures are logged and retried
- **Story Points:** 5
- **Priority:** P1

---

## 🗄️ SPRINT 2: Backend Foundation (Weeks 3-4)

### Epic: API & Data Storage
**Story Points:** 21

#### User Stories:

**US-201: As a system, I want a PostgreSQL database schema so that I can store historical data**
- **Tasks:**
  - [ ] Create news table schema
  - [ ] Create price table schema
  - [ ] Create sentiment_summary table schema
  - [ ] Write migration scripts
  - [ ] Add indexes for performance
  - [ ] Create SQLAlchemy ORM models
- **Acceptance Criteria:**
  - Tables created with proper constraints
  - Indexes on timestamp columns
  - ORM models match schema
- **Story Points:** 5
- **Priority:** P0

**US-202: As a system, I want Redis caching layer so that API responses are fast**
- **Tasks:**
  - [ ] Create Redis connection manager
  - [ ] Implement cache set/get utilities
  - [ ] Add TTL configuration for each data type
  - [ ] Create cache invalidation logic
  - [ ] Write integration tests
- **Acceptance Criteria:**
  - Price cached for 10s
  - Sentiment cached for 30s
  - News cached for 5m
- **Story Points:** 3
- **Priority:** P1

**US-203: As a trader, I want REST API endpoints so that I can access sentiment and price data**
- **Tasks:**
  - [ ] Create FastAPI application structure
  - [ ] Implement GET /sentiment/latest endpoint
  - [ ] Implement GET /price/current endpoint
  - [ ] Implement GET /news/recent endpoint
  - [ ] Implement GET /correlation endpoint
  - [ ] Add request validation with Pydantic
  - [ ] Add error handling middleware
  - [ ] Write API integration tests
- **Acceptance Criteria:**
  - All endpoints return valid JSON
  - Response time < 150ms (cached)
  - Proper error codes (404, 500, etc.)
- **Story Points:** 8
- **Priority:** P1

**US-204: As a developer, I want database seed data so that I can test the system**
- **Tasks:**
  - [ ] Create sample news data
  - [ ] Create sample price data
  - [ ] Create sample sentiment data
  - [ ] Write seed script
  - [ ] Add seed command to docker-compose
- **Acceptance Criteria:**
  - Seed script populates all tables
  - Data is realistic and diverse
- **Story Points:** 2
- **Priority:** P2

**US-205: As a system admin, I want API logging and monitoring so that I can debug issues**
- **Tasks:**
  - [ ] Set up structured logging
  - [ ] Log all API requests
  - [ ] Log database operations
  - [ ] Add health check endpoint
  - [ ] Create logging utilities in shared package
- **Acceptance Criteria:**
  - All requests logged with timestamps
  - Errors include stack traces
- **Story Points:** 3
- **Priority:** P1

---

## 🎨 SPRINT 3: Frontend & Dashboard (Weeks 5-6)

### Epic: Visualization & User Interface
**Story Points:** 21

#### User Stories:

**US-301: As a trader, I want a dashboard UI so that I can visualize sentiment trends**
- **Tasks:**
  - [ ] Create Next.js app with App Router
  - [ ] Set up TailwindCSS configuration
  - [ ] Create layout component
  - [ ] Create navigation component
  - [ ] Add responsive design
- **Acceptance Criteria:**
  - Dashboard loads in < 2.5s
  - Mobile-responsive layout
- **Story Points:** 5
- **Priority:** P1

**US-302: As a trader, I want sentiment charts so that I can see trends over time**
- **Tasks:**
  - [ ] Install Chart.js or Plotly
  - [ ] Create sentiment time series chart component
  - [ ] Add chart filtering (1h, 4h, 1d, 1w)
  - [ ] Fetch data from API
  - [ ] Add loading states
- **Acceptance Criteria:**
  - Chart updates in real-time
  - Supports multiple time ranges
  - Shows sentiment labels
- **Story Points:** 5
- **Priority:** P1

**US-303: As a trader, I want price charts so that I can compare with sentiment**
- **Tasks:**
  - [ ] Create price time series chart component
  - [ ] Add candlestick or line chart
  - [ ] Sync time range with sentiment chart
  - [ ] Add hover tooltips
  - [ ] Fetch data from API
- **Acceptance Criteria:**
  - Price updates every 10 seconds
  - Charts are synchronized
- **Story Points:** 5
- **Priority:** P1

**US-304: As a trader, I want correlation visualization so that I can see sentiment-price relationships**
- **Tasks:**
  - [ ] Create correlation chart component
  - [ ] Add scatter plot or heatmap
  - [ ] Display correlation coefficient
  - [ ] Add statistical indicators
  - [ ] Fetch correlation data from API
- **Acceptance Criteria:**
  - Shows correlation strength visually
  - Updates when data changes
- **Story Points:** 3
- **Priority:** P2

**US-305: As a trader, I want to see recent news headlines so that I know what's driving sentiment**
- **Tasks:**
  - [ ] Create news feed component
  - [ ] Display headlines with sentiment badges
  - [ ] Add timestamp formatting
  - [ ] Add source links
  - [ ] Implement pagination or infinite scroll
- **Acceptance Criteria:**
  - Shows 20 most recent headlines
  - Color-coded by sentiment
- **Story Points:** 3
- **Priority:** P1

---

## 🔗 SPRINT 4: Correlation & Alerts (Weeks 7-8)

### Epic: Advanced Analytics
**Story Points:** 18

#### User Stories:

**US-401: As a researcher, I want statistical correlation analysis so that I can backtest strategies**
- **Tasks:**
  - [ ] Implement Pearson correlation calculation
  - [ ] Add time-lagged correlation analysis
  - [ ] Create correlation aggregation function
  - [ ] Store correlation results in database
  - [ ] Write unit tests
- **Acceptance Criteria:**
  - Calculates correlation for multiple time windows
  - Returns p-value and confidence intervals
- **Story Points:** 5
- **Priority:** P2

**US-402: As a trader, I want divergence alerts so that I'm notified when sentiment contradicts price**
- **Tasks:**
  - [ ] Define divergence detection logic
  - [ ] Implement alert trigger function
  - [ ] Create alert storage table
  - [ ] Add alert history endpoint
  - [ ] Write integration tests
- **Acceptance Criteria:**
  - Detects sentiment-price divergence
  - Stores alert with timestamp
- **Story Points:** 5
- **Priority:** P3

**US-403: As a trader, I want real-time notifications so that I don't miss important signals**
- **Tasks:**
  - [ ] Set up WebSocket connection
  - [ ] Implement server-sent events (SSE)
  - [ ] Create frontend notification component
  - [ ] Add browser notification permission
  - [ ] Test notification delivery
- **Acceptance Criteria:**
  - Notifications appear within 2 seconds
  - Works across modern browsers
- **Story Points:** 5
- **Priority:** P3

**US-404: As a system admin, I want alert configuration so that I can tune sensitivity**
- **Tasks:**
  - [ ] Create alert configuration schema
  - [ ] Add configuration API endpoint
  - [ ] Create admin configuration UI
  - [ ] Add validation logic
  - [ ] Write tests
- **Acceptance Criteria:**
  - Admins can adjust thresholds
  - Changes take effect immediately
- **Story Points:** 3
- **Priority:** P3

---

## 🚀 SPRINT 5: Optimization & Deployment (Weeks 9-10)

### Epic: Production Readiness
**Story Points:** 18

#### User Stories:

**US-501: As a developer, I want CI/CD pipeline so that deployments are automated**
- **Tasks:**
  - [ ] Create GitHub Actions workflow
  - [ ] Add automated testing on PR
  - [ ] Add linting checks
  - [ ] Configure Railway deployment
  - [ ] Configure Vercel deployment
  - [ ] Add deployment notifications
- **Acceptance Criteria:**
  - Tests run on every PR
  - Auto-deploy on merge to main
- **Story Points:** 5
- **Priority:** P1

**US-502: As a system, I want optimized database queries so that API is fast**
- **Tasks:**
  - [ ] Add database indexes
  - [ ] Optimize N+1 queries
  - [ ] Add query result caching
  - [ ] Implement pagination
  - [ ] Run performance benchmarks
- **Acceptance Criteria:**
  - All queries < 100ms
  - No N+1 query patterns
- **Story Points:** 3
- **Priority:** P1

**US-503: As a system admin, I want monitoring and observability so that I can track system health**
- **Tasks:**
  - [ ] Set up Prefect Cloud dashboard
  - [ ] Add Railway metrics tracking
  - [ ] Create custom metrics endpoint
  - [ ] Set up error tracking (Sentry optional)
  - [ ] Create system health dashboard
- **Acceptance Criteria:**
  - Pipeline uptime visible
  - API latency tracked
  - Errors logged centrally
- **Story Points:** 5
- **Priority:** P1

**US-504: As a trader, I want API documentation so that I can integrate the system**
- **Tasks:**
  - [ ] Generate OpenAPI/Swagger docs
  - [ ] Add endpoint descriptions
  - [ ] Create example requests/responses
  - [ ] Add authentication guide (if applicable)
  - [ ] Publish API docs
- **Acceptance Criteria:**
  - Swagger UI accessible
  - All endpoints documented
- **Story Points:** 2
- **Priority:** P2

**US-505: As a system admin, I want security hardening so that the system is production-ready**
- **Tasks:**
  - [ ] Add rate limiting
  - [ ] Configure CORS properly
  - [ ] Add API key authentication
  - [ ] Implement input sanitization
  - [ ] Add security headers
  - [ ] Run security audit
- **Acceptance Criteria:**
  - Rate limits prevent abuse
  - CORS limited to Vercel domain
  - No SQL injection vulnerabilities
- **Story Points:** 3
- **Priority:** P1

---

## 📊 Backlog Summary

| Priority | Story Points | User Stories |
|----------|--------------|--------------|
| P0 | 23 | 5 stories |
| P1 | 56 | 13 stories |
| P2 | 13 | 4 stories |
| P3 | 13 | 3 stories |
| **Total** | **105** | **25 stories** |

---

## 🎯 Definition of Done (DoD)

For a story to be considered "Done", it must meet:
- [ ] Code written and follows Cursor rules (black + ruff)
- [ ] Unit tests written with ≥ 80% coverage
- [ ] Integration tests pass
- [ ] Code reviewed (AI-assisted + manual)
- [ ] Documentation updated
- [ ] Deployed to staging environment
- [ ] Acceptance criteria validated

---

## 📈 Velocity Tracking

| Sprint | Committed | Completed | Velocity |
|--------|-----------|-----------|----------|
| Sprint 0 | 8 | TBD | TBD |
| Sprint 1 | 21 | TBD | TBD |
| Sprint 2 | 21 | TBD | TBD |
| Sprint 3 | 21 | TBD | TBD |
| Sprint 4 | 18 | TBD | TBD |
| Sprint 5 | 18 | TBD | TBD |

---

## 🔄 Backlog Refinement

- **Schedule:** Every Friday at end of sprint
- **Participants:** CTO, Developer (You)
- **Agenda:**
  - Review completed stories
  - Refine upcoming sprint stories
  - Adjust priorities based on learnings
  - Update story points

---

## 📝 Notes

- Story points based on Fibonacci scale (1, 2, 3, 5, 8, 13)
- Velocity target: ≥ 18 points per sprint
- All stories follow INVEST principles (Independent, Negotiable, Valuable, Estimable, Small, Testable)
- Priorities may shift based on technical discoveries

---

**Next Steps:**
1. Start Sprint 0 by creating project structure
2. Set up development environment
3. Begin Sprint 1 once infrastructure is ready

