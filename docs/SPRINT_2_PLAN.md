# 🎯 Sprint 2 - Planning Document

**Sprint Duration:** 2 Weeks  
**Sprint Goal:** Build API endpoints and dashboard UI  
**Team Capacity:** 26 Story Points  
**Start Date:** January 27, 2025

---

## 📋 Sprint Objectives

1. ✅ Build RESTful API endpoints for data access
2. ✅ Create real-time dashboard with price & sentiment visualization
3. ✅ Implement alert system for price/sentiment changes
4. ✅ Add WebSocket support for real-time updates
5. ✅ Deploy to staging environment

---

## 📊 User Stories

### US-201: Backend API Endpoints
**Priority:** HIGH  
**Points:** 8  
**Status:** In Progress

**Acceptance Criteria:**
- [ ] GET `/api/v1/price/latest` - Latest gold price
- [ ] GET `/api/v1/price/history` - Historical prices with pagination
- [ ] GET `/api/v1/news/recent` - Recent news articles
- [ ] GET `/api/v1/news/:id` - Single news article
- [ ] GET `/api/v1/sentiment/summary` - Sentiment summary
- [ ] GET `/api/v1/sentiment/history` - Historical sentiment
- [ ] GET `/api/v1/alerts` - User alerts
- [ ] POST `/api/v1/alerts` - Create alert
- [ ] DELETE `/api/v1/alerts/:id` - Delete alert
- [ ] GET `/api/v1/health` - Health check
- [ ] API documentation with OpenAPI/Swagger
- [ ] CORS configuration for frontend
- [ ] Rate limiting
- [ ] Error handling middleware

**Technical Tasks:**
- [x] Setup FastAPI app structure
- [ ] Implement price endpoints
- [ ] Implement news endpoints
- [ ] Implement sentiment endpoints
- [ ] Implement alert endpoints
- [ ] Add pagination utilities
- [ ] Add API documentation
- [ ] Add error handling
- [ ] Add rate limiting
- [ ] Write API tests

---

### US-202: Dashboard UI
**Priority:** HIGH  
**Points:** 13  
**Status:** Pending

**Acceptance Criteria:**
- [ ] Real-time price chart (24h, 7d, 30d views)
- [ ] Current price display with change indicator
- [ ] News feed with sentiment badges
- [ ] Sentiment gauge/chart
- [ ] Alert configuration panel
- [ ] Responsive design (mobile, tablet, desktop)
- [ ] Dark/light theme toggle
- [ ] Loading states and error handling
- [ ] Auto-refresh every 30 seconds

**Components:**
- [ ] `PriceChart.tsx` - Interactive price chart
- [ ] `PriceCard.tsx` - Current price display
- [ ] `NewsFeed.tsx` - News article list
- [ ] `NewsCard.tsx` - Individual news item
- [ ] `SentimentGauge.tsx` - Sentiment visualization
- [ ] `SentimentHistory.tsx` - Sentiment timeline
- [ ] `AlertPanel.tsx` - Alert management
- [ ] `Layout.tsx` - App layout with navigation
- [ ] `Header.tsx` - App header
- [ ] `Footer.tsx` - App footer

**Technical Tasks:**
- [ ] Setup API client with axios/fetch
- [ ] Create TypeScript types for API responses
- [ ] Implement real-time polling
- [ ] Add Chart.js/Recharts for visualization
- [ ] Style with TailwindCSS
- [ ] Add loading skeletons
- [ ] Add error boundaries
- [ ] Write component tests

---

### US-203: Alert System
**Priority:** MEDIUM  
**Points:** 5  
**Status:** Pending

**Acceptance Criteria:**
- [ ] Price threshold alerts (above/below)
- [ ] Sentiment shift alerts (positive/negative)
- [ ] Alert notification system
- [ ] Email notifications (optional)
- [ ] Browser push notifications (optional)
- [ ] Alert history
- [ ] Snooze/dismiss alerts

**Alert Types:**
1. **Price Alerts**
   - Price above threshold
   - Price below threshold
   - Price change % (5%, 10%)

2. **Sentiment Alerts**
   - Sentiment shifts positive
   - Sentiment shifts negative
   - High confidence events

**Technical Tasks:**
- [ ] Create alert checking logic
- [ ] Implement alert triggers in pipeline
- [ ] Add notification service
- [ ] Create alert management UI
- [ ] Add alert persistence
- [ ] Write alert tests

---

## 🎯 Sprint Backlog

### Week 1: Backend API
- [x] Day 1-2: API endpoint implementation
  - [x] Price endpoints
  - [x] News endpoints
  - [ ] Sentiment endpoints
  - [ ] Alert endpoints

- [ ] Day 3-4: API testing & documentation
  - [ ] Write API tests
  - [ ] Add OpenAPI documentation
  - [ ] Test all endpoints
  - [ ] Add rate limiting

- [ ] Day 5: API deployment
  - [ ] Deploy to Railway
  - [ ] Test production endpoints
  - [ ] Monitor performance

### Week 2: Dashboard UI
- [ ] Day 1-2: Core components
  - [ ] Price chart
  - [ ] Price card
  - [ ] News feed

- [ ] Day 3-4: Advanced features
  - [ ] Sentiment visualization
  - [ ] Alert panel
  - [ ] Real-time updates

- [ ] Day 5: Polish & deploy
  - [ ] Responsive design
  - [ ] Theme toggle
  - [ ] Deploy to Vercel

---

## 📈 Success Metrics

| Metric | Target |
|--------|---------|
| API Response Time | <200ms (p95) |
| API Uptime | >99% |
| Dashboard Load Time | <2s |
| Test Coverage | >80% |
| User Satisfaction | 8/10 |

---

## 🚨 Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|---------|-------------|------------|
| API performance issues | High | Medium | Implement caching, optimize queries |
| WebSocket complexity | Medium | High | Use polling first, add WebSocket later |
| Chart.js integration | Low | Low | Use simpler library (Recharts) |
| Time constraints | Medium | Medium | Prioritize core features |

---

## 🔗 Dependencies

- ✅ Sprint 1 complete (pipeline working)
- ✅ PostgreSQL data available
- ✅ Redis caching operational
- ⏳ Railway account setup
- ⏳ Vercel account setup

---

## 📝 Definition of Done

- [ ] All acceptance criteria met
- [ ] Code reviewed and approved
- [ ] Tests written and passing (>80% coverage)
- [ ] Documentation updated
- [ ] Deployed to staging
- [ ] Demo prepared for stakeholders
- [ ] No critical bugs

---

**Scrum Master Approval:** ✅  
**Product Owner Approval:** ✅  
**Sprint Start:** January 27, 2025

