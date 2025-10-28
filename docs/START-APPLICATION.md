# 🚀 AUREX.AI - Application Startup Guide

Complete guide to start the AUREX.AI real-time gold sentiment analysis platform.

---

## 📋 Prerequisites

### Required:
- **Docker Desktop** (for database & Redis)
- **Python 3.11+** with virtual environment
- **Node.js 18+** and npm 9+
- **PowerShell** (Windows) or Bash (Linux/Mac)

### Check Installation:
```bash
docker --version        # Should be 20.10+
python --version        # Should be 3.11+
node --version          # Should be v18+
npm --version           # Should be 9+
```

---

## 🎯 Quick Start (Recommended)

### **Option A: Using Helper Scripts** ⚡ (Fastest)

#### 1. Start Infrastructure & Backend
```powershell
# In PowerShell terminal
.\run-backend.ps1
```

This will:
- ✅ Start Docker containers (PostgreSQL, Redis)
- ✅ Activate Python virtual environment
- ✅ Start real-time backend server
- ✅ Initialize WebSocket streaming

#### 2. Start Dashboard (New Terminal)
```powershell
# In a new PowerShell terminal
.\run-dashboard.ps1
```

This will:
- ✅ Navigate to dashboard folder
- ✅ Install dependencies (if needed)
- ✅ Start Next.js development server

#### 3. Access Application
```
🌐 Dashboard:  http://localhost:3000
📊 API:        http://localhost:8000
📚 API Docs:   http://localhost:8000/docs
📡 WebSocket:  ws://localhost:8000/api/v1/ws/stream
```

---

## 📝 Manual Step-by-Step

### **Step 1: Start Docker Infrastructure**

```bash
# Start PostgreSQL and Redis
docker-compose up -d postgres redis

# Wait for health checks (30 seconds)
Start-Sleep -Seconds 30

# Verify containers are running
docker-compose ps
```

**Expected Output:**
```
NAME              STATUS         PORTS
aurex-postgres    Up (healthy)   0.0.0.0:5432->5432/tcp
aurex-redis       Up (healthy)   0.0.0.0:6379->6379/tcp
```

---

### **Step 2: Start Backend Server**

#### Activate Virtual Environment:
```powershell
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

#### Start Real-Time Backend:
```bash
python apps/backend/start_realtime_backend.py
```

**Expected Output:**
```
======================================================================
🚀 AUREX.AI Real-Time Backend
======================================================================
🔄 Starting price streamer thread...
🌐 Starting FastAPI backend server...
📡 WebSocket endpoint: ws://localhost:8000/api/v1/ws/stream
📊 API docs: http://localhost:8000/docs
======================================================================
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

---

### **Step 3: Start Dashboard (New Terminal)**

```bash
# Navigate to dashboard
cd apps/dashboard

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

**Expected Output:**
```
> @aurex/dashboard@1.0.0 dev
> next dev

  ▲ Next.js 15.5.6
  - Local:        http://localhost:3000
  - Network:      http://192.168.1.x:3000

 ✓ Starting...
 ✓ Ready in 2.3s
```

---

### **Step 4: Verify Everything Works**

#### Check Backend Health:
```powershell
curl http://localhost:8000/
```

**Should return:**
```json
{
  "name": "AUREX.AI API",
  "version": "1.0.0",
  "status": "operational",
  "docs": "/docs",
  "health": "/api/v1/health"
}
```

#### Check API Health:
```powershell
curl http://localhost:8000/api/v1/health
```

**Should return:**
```json
{
  "status": "healthy",
  "database": "connected",
  "cache": "connected",
  "timestamp": "2025-10-28T..."
}
```

#### Check Dashboard:
```
Open: http://localhost:3000
Look for: "AUREX.AI" header
Check: Price updates every 5 seconds
```

---

## 🔄 Optional: Fetch Initial Data

### Fetch News Articles (NewsAPI):
```bash
# In backend container
python scripts/docker_cli.py fetch-news

# Or directly
docker-compose exec backend python fetch_gold_news.py
```

### Run Data Pipeline:
```bash
# Start the pipeline service
docker-compose up -d pipeline

# Check logs
docker-compose logs -f pipeline
```

---

## 🛑 Stopping the Application

### Stop All Services:
```bash
# Stop backend (Ctrl+C in terminal)
# Stop dashboard (Ctrl+C in terminal)

# Stop Docker containers
docker-compose down
```

### Stop but Keep Data:
```bash
# Just stop containers
docker-compose stop
```

### Complete Cleanup (Remove All Data):
```bash
# Stop and remove volumes
docker-compose down -v
```

---

## 🔧 Troubleshooting

### **Issue 1: Port Already in Use**

**Error:** `Bind for 0.0.0.0:5432 failed: port is already allocated`

**Solution:**
```bash
# Check what's using the port
netstat -ano | findstr :5432

# Kill the process or change port in docker-compose.yml
```

### **Issue 2: Database Connection Failed**

**Error:** `could not connect to server: Connection refused`

**Solution:**
```bash
# Wait for database to be ready
docker-compose logs postgres

# Restart database
docker-compose restart postgres
Start-Sleep -Seconds 10
```

### **Issue 3: Module Not Found**

**Error:** `ModuleNotFoundError: No module named 'packages'`

**Solution:**
```bash
# Activate virtual environment first
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

### **Issue 4: WebSocket Not Connecting**

**Error:** Browser console shows `WebSocket connection failed`

**Solution:**
```bash
# 1. Check backend is running
curl http://localhost:8000/

# 2. Check WebSocket endpoint
# Open: http://localhost:8000/docs
# Look for: /api/v1/ws/stream

# 3. Restart backend
# Ctrl+C, then restart
```

### **Issue 5: Dashboard Shows "Loading..."**

**Cause:** Backend not responding or CORS issue

**Solution:**
```bash
# 1. Check backend health
curl http://localhost:8000/api/v1/health

# 2. Check browser console for errors
# Open DevTools (F12) -> Console

# 3. Clear cache and reload
# Ctrl+Shift+R or Cmd+Shift+R
```

### **Issue 6: Event Loop Error**

**Error:** `RuntimeError: no running event loop`

**Solution:**
This is already fixed in the latest code. Make sure you're using:
```bash
python apps/backend/start_realtime_backend.py
```

NOT the old `main.py`.

---

## 🐳 Docker-Only Mode (Alternative)

If you want to run everything in Docker:

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f backend
```

**Services:**
- Backend: http://localhost:8000
- Dashboard: Run separately with `npm run dev`
- Database: localhost:5432
- Redis: localhost:6379

---

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     AUREX.AI System                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Frontend (Next.js)          Backend (FastAPI)              │
│  ─────────────────────────────────────────────────          │
│  http://localhost:3000       http://localhost:8000          │
│                                                              │
│  ┌─────────────────┐         ┌─────────────────┐           │
│  │  Dashboard UI   │◄────────│  REST API       │           │
│  │                 │  HTTP   │                 │           │
│  │  - PriceCard    │         │  - /price       │           │
│  │  - NewsFeed     │         │  - /news        │           │
│  │  - Sentiment    │         │  - /sentiment   │           │
│  │  - Alerts       │         │  - /alerts      │           │
│  └────────┬────────┘         └────────┬────────┘           │
│           │                           │                     │
│           │ WebSocket (Real-Time)     │                     │
│           │ ws://localhost:8000/      │                     │
│           │    api/v1/ws/stream       │                     │
│           │                           │                     │
│  ┌────────▼────────┐         ┌───────▼────────┐            │
│  │  WebSocket      │◄────────│  WebSocket     │            │
│  │  Client         │         │  Manager       │            │
│  │                 │         │                │            │
│  │  - Auto-reconnect│        │  - Broadcasting│            │
│  │  - Message queue│         │  - Connections │            │
│  └─────────────────┘         └────────┬───────┘            │
│                                       │                     │
│                              ┌────────▼────────┐            │
│                              │  Price Streamer │            │
│                              │                 │            │
│                              │  - yfinance     │            │
│                              │  - 5s updates   │            │
│                              └────────┬────────┘            │
│                                       │                     │
│                       ┌───────────────┴───────────────┐     │
│                       │                               │     │
│              ┌────────▼────────┐         ┌───────────▼──┐  │
│              │   PostgreSQL    │         │    Redis     │  │
│              │   (TimescaleDB) │         │    Cache     │  │
│              │                 │         │              │  │
│              │  - Time-series  │         │  - Sessions  │  │
│              │  - Price data   │         │  - Fast reads│  │
│              │  - News/Alerts  │         │              │  │
│              └─────────────────┘         └──────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## ✅ Startup Checklist

Use this to verify everything is running:

- [ ] Docker Desktop is running
- [ ] Virtual environment activated
- [ ] PostgreSQL container is healthy
- [ ] Redis container is healthy
- [ ] Backend server started (port 8000)
- [ ] Dashboard server started (port 3000)
- [ ] Backend health check passes
- [ ] WebSocket connection established
- [ ] Dashboard loads without errors
- [ ] Price updates visible every 5 seconds

---

## 🎯 Quick Commands Reference

| Task | Command |
|------|---------|
| Start infrastructure | `docker-compose up -d postgres redis` |
| Start backend | `python apps/backend/start_realtime_backend.py` |
| Start dashboard | `cd apps/dashboard && npm run dev` |
| Check backend | `curl http://localhost:8000/` |
| Check health | `curl http://localhost:8000/api/v1/health` |
| View logs | `docker-compose logs -f backend` |
| Stop all | `docker-compose down` |
| Restart service | `docker-compose restart <service>` |
| Fetch news | `python scripts/docker_cli.py fetch-news` |

---

## 📚 Additional Resources

- **Architecture:** `docs/REALTIME_ARCHITECTURE.md`
- **Docker Management:** `docs/MCP_DOCKER_GUIDE.md`
- **API Integration:** `docs/API_INTEGRATION_GUIDE.md`
- **Project Overview:** `docs/PROJECT_IMPROVEMENTS_SUMMARY.md`
- **System Status:** `docs/SYSTEM_READY.md`

---

## 💡 Pro Tips

1. **Use Separate Terminals:** One for backend, one for dashboard, one for commands
2. **Check Logs First:** When things fail, check Docker logs
3. **Wait for Health Checks:** Give containers 30s to be fully ready
4. **Use Docker MCP:** `python scripts/docker_cli.py status` for quick checks
5. **Browser DevTools:** F12 to see WebSocket connections and errors

---

## 🎉 Success Indicators

When everything is working correctly, you should see:

1. **Backend Terminal:**
   ```
   ✅ Starting price streamer thread...
   ✅ Starting FastAPI backend server...
   ✅ Uvicorn running on http://0.0.0.0:8000
   ```

2. **Dashboard Terminal:**
   ```
   ✅ Next.js 15.5.6
   ✅ Local: http://localhost:3000
   ✅ Ready in 2.3s
   ```

3. **Browser Console (F12):**
   ```
   ✅ [WebSocket] Connected to AUREX.AI
   ✅ [WebSocket] Received price update: $2734.56
   ```

4. **Dashboard UI:**
   ```
   ✅ Price card showing current gold price
   ✅ Price updating every 5 seconds
   ✅ News feed showing articles
   ✅ Theme toggle working
   ✅ No error messages
   ```

---

**Status:** ✅ Ready to start!  
**Estimated startup time:** 1-2 minutes  
**Support:** See troubleshooting section above

**Happy trading! 🚀**

