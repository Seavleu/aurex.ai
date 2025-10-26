# AUREX.AI - Sprint Planning & Tracking
**Scrum Master:** CTO / AI Developer  
**Sprint Duration:** 2 weeks  
**Last Updated:** 2025-10-26

---

## 🎯 Current Sprint: Sprint 0 - Project Setup

**Start Date:** 2025-10-26  
**End Date:** 2025-10-26 (Accelerated - Day 0)  
**Goal:** Establish development infrastructure and project foundation

### Sprint Objective
Set up the complete development environment, project structure, and tooling so that development can begin efficiently in Sprint 1.

### Sprint Backlog

| ID | Story | Story Points | Status | Assignee |
|----|-------|--------------|--------|----------|
| US-001 | Standardized project structure | 3 | 🔄 In Progress | AI Dev |
| US-002 | Docker Compose configuration | 3 | ⏳ Todo | AI Dev |
| US-003 | Code quality tools | 2 | ⏳ Todo | AI Dev |

**Total Committed:** 8 Story Points

### Daily Standup Notes

#### Day 1 - October 26, 2025
**Yesterday:** N/A (Sprint start)  
**Today:**
- Create folder structure
- Set up Python environment
- Create configuration files
- Initialize Docker setup

**Blockers:** None

---

## 📅 Sprint Calendar

### Sprint 0 (Week 0)
- **Oct 26:** Sprint Planning, Environment Setup
- **Oct 26:** Complete Sprint 0 (accelerated)

### Sprint 1 (Weeks 1-2)
- **Week 1 Day 1:** Sprint Planning
- **Week 1 Day 3:** Mid-sprint check-in
- **Week 2 Day 4:** Sprint Review
- **Week 2 Day 5:** Sprint Retrospective & Planning

### Sprint 2 (Weeks 3-4)
- TBD

---

## 🎬 Sprint Ceremonies

### 1. Sprint Planning (2 hours)
**When:** First day of sprint  
**Purpose:** Select backlog items and create sprint backlog  
**Outputs:**
- Sprint goal defined
- Stories committed
- Tasks identified
- Definition of Done agreed

### 2. Daily Standup (15 minutes)
**When:** Every day (async via commits in Cursor)  
**Format:**
- What did I complete yesterday?
- What will I work on today?
- Any blockers?

### 3. Sprint Review (1 hour)
**When:** Last day of sprint  
**Purpose:** Demo completed work  
**Attendees:** Stakeholder review (self-review in this case)  
**Outputs:**
- Working software demonstrated
- Feedback collected
- Backlog updated

### 4. Sprint Retrospective (1 hour)
**When:** After sprint review  
**Purpose:** Improve process  
**Format:**
- What went well?
- What didn't go well?
- What will we improve?

---

## 📊 Sprint Metrics

### Sprint 0 Goals
- [ ] 100% of committed stories completed
- [ ] Zero critical bugs introduced
- [ ] All tests passing
- [ ] Documentation updated

### Key Performance Indicators (KPIs)

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Story Points Completed | 8 | 0 | 🔄 |
| Code Coverage | ≥80% | N/A | ⏳ |
| Build Success Rate | 100% | N/A | ⏳ |
| Linting Errors | 0 | N/A | ⏳ |

---

## 🔄 Upcoming Sprints Preview

### Sprint 1: Data Ingestion MVP (Weeks 1-2)
**Story Points:** 21  
**Focus:**
- Price data fetching (yfinance)
- News scraping (ForexFactory)
- FinBERT sentiment analysis
- Prefect pipeline orchestration

**Key Deliverables:**
- Working price fetcher
- Working news scraper
- Sentiment inference working
- Prefect flows running on schedule

### Sprint 2: Backend Foundation (Weeks 3-4)
**Story Points:** 21  
**Focus:**
- Database schema implementation
- Redis caching layer
- FastAPI REST endpoints
- API testing

**Key Deliverables:**
- All API endpoints functional
- Sub-150ms response time (cached)
- Database fully operational

### Sprint 3: Frontend & Dashboard (Weeks 5-6)
**Story Points:** 21  
**Focus:**
- Next.js UI setup
- Chart components
- Real-time updates
- News feed

**Key Deliverables:**
- Working dashboard
- Sentiment and price charts
- < 2.5s page load time

---

## 🎯 Sprint Success Criteria

### Sprint 0 Success Criteria
- [x] Product backlog created and refined
- [ ] Project structure follows architecture specification
- [ ] Docker Compose starts all services successfully
- [ ] Code quality tools (Black, Ruff) configured
- [ ] README with setup instructions
- [ ] Environment ready for Sprint 1

---

## 🚧 Risk Register

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| FinBERT model too large for free tier | Medium | High | Use quantized model or smaller variant |
| API rate limits on data sources | Low | Medium | Implement caching and request throttling |
| PostgreSQL storage limits | Low | Medium | Implement data retention policy |
| Complex correlation logic | Medium | Low | Start simple, iterate with feedback |

---

## 📝 Sprint 0 Task Breakdown

### US-001: Standardized Project Structure (3 pts)
**Tasks:**
1. ✅ Create docs/ folder with architecture and PRD
2. ✅ Create PRODUCT_BACKLOG.md
3. ✅ Create SPRINT_PLANNING.md
4. ⏳ Create folder structure: apps/, packages/, infra/
5. ⏳ Set up Python virtual environment
6. ⏳ Create requirements.txt
7. ⏳ Create .env.example
8. ⏳ Create .gitignore
9. ⏳ Create README.md

### US-002: Docker Compose Configuration (3 pts)
**Tasks:**
1. ⏳ Create docker-compose.yml
2. ⏳ Configure PostgreSQL service
3. ⏳ Configure Redis service
4. ⏳ Configure FastAPI service
5. ⏳ Create init_db.sql
6. ⏳ Test docker-compose up

### US-003: Code Quality Tools (2 pts)
**Tasks:**
1. ⏳ Create pyproject.toml with Black config
2. ⏳ Create ruff.toml with linting rules
3. ⏳ Create .pre-commit-config.yaml
4. ⏳ Create pytest.ini
5. ⏳ Test all tools run successfully

---

## 🎉 Sprint Retrospective Template

### What Went Well ✅
- TBD at end of sprint

### What Didn't Go Well ❌
- TBD at end of sprint

### Action Items 🎯
- TBD at end of sprint

---

## 📈 Burndown Chart Data

### Sprint 0 Burndown
| Day | Remaining Story Points |
|-----|------------------------|
| Day 0 | 8 |
| Day 1 | TBD |

---

## 🏆 Definition of Ready (DoR)

For a story to enter a sprint, it must:
- [ ] Have clear acceptance criteria
- [ ] Be estimated (story points assigned)
- [ ] Have no external dependencies
- [ ] Be testable
- [ ] Be achievable within one sprint

---

## 🎖️ Definition of Done (DoD)

For a story to be considered done:
- [ ] Code complete and follows style guide
- [ ] Unit tests written (≥80% coverage)
- [ ] Integration tests pass
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] No linting errors
- [ ] Deployed to staging
- [ ] Acceptance criteria met

---

**Next Actions:**
1. ✅ Complete sprint planning documentation
2. ⏳ Begin US-001 implementation
3. ⏳ Complete Sprint 0 tasks
4. ⏳ Prepare for Sprint 1 planning

