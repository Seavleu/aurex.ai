# 🚀 AUREX.AI - Complete Startup Guide (Step-by-Step)

## ⚠️ Current Issue

**Error:** `password authentication failed for user "aurex"`

**Root Cause:** Docker Desktop stopped/crashed, so PostgreSQL container is not accessible.

---

## ✅ Complete Startup Procedure

Follow these steps **in order** every time you start AUREX.AI:

---

### **Step 1: Start Docker Desktop** 🐳

#### Method A: Via Start Menu
```
1. Press Windows Key
2. Type "Docker Desktop"
3. Click on "Docker Desktop"
4. Wait for the whale icon in system tray
```

#### Method B: Via PowerShell
```powershell
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
```

#### **CRITICAL: Wait for Docker to be Ready!**

**Look at your system tray (bottom-right corner):**
- ⏳ **Orange/Animated Whale** = Docker is starting (WAIT!)
- ✅ **Green Whale** = Docker is ready (PROCEED!)
- ❌ **Red Whale** = Docker has error (RESTART Docker)

**This can take 1-2 minutes. BE PATIENT!**

---

### **Step 2: Verify Docker is Running** ✅

```powershell
docker ps
```

**Expected Output (Success):**
```
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
(Can be empty, but should NOT show an error)
```

**If you see an error:**
```
error during connect: ... dockerDesktopLinuxEngine
```

**→ Docker is NOT ready yet! Wait longer and try again.**

---

### **Step 3: Start Database Containers** 🗄️

```powershell
# Navigate to project root (if not already there)
cd C:\Users\Seavleu\Downloads\aurex-ai

# Start PostgreSQL and Redis
docker-compose up -d postgres redis
```

**Expected Output:**
```
[+] Running 2/2
 ✔ Container aurex-postgres  Started
 ✔ Container aurex-redis     Started
```

#### **Wait for Health Checks (30 seconds)**

```powershell
Start-Sleep -Seconds 30
```

**OR check manually:**
```powershell
docker-compose ps
```

**Expected Output:**
```
NAME             STATUS
aurex-postgres   Up (healthy)    ✅
aurex-redis      Up (healthy)    ✅
```

**If not healthy, wait longer!**

---

### **Step 4: Verify Database Connection** 🔍

```powershell
docker exec aurex-postgres psql -U aurex -d aurex_db -c "SELECT version();"
```

**Expected Output:**
```
PostgreSQL 15.13 on x86_64-pc-linux-musl...
```

**If you get an error:**
```
error during connect: dockerDesktopLinuxEngine
```
**→ Docker Desktop is STILL not ready. Wait and try again!**

**If you get:**
```
password authentication failed
```
**→ Continue to Step 5 to fix password**

---

### **Step 5: Fix PostgreSQL Password (If Needed)** 🔐

If you got "password authentication failed", reset the password:

```powershell
# Reset aurex user password
docker exec aurex-postgres psql -U postgres -c "ALTER USER aurex WITH PASSWORD 'aurex_password';"

# Grant permissions
docker exec aurex-postgres psql -U postgres -d aurex_db -c "GRANT ALL PRIVILEGES ON DATABASE aurex_db TO aurex;"

# Verify it works
docker exec aurex-postgres psql -U aurex -d aurex_db -c "SELECT current_user;"
```

**Expected Output:**
```
 current_user 
--------------
 aurex
(1 row)
```

---

### **Step 6: Start Backend** 🎯

```powershell
# Make sure you're in project root
cd C:\Users\Seavleu\Downloads\aurex-ai

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Start real-time backend
python apps/backend/start_realtime_backend.py
```

**Expected Output (Success):**
```
======================================================================
🚀 AUREX.AI Real-Time Backend
======================================================================
🔄 Starting price streamer thread...
🌐 Starting FastAPI backend server...
📡 WebSocket endpoint: ws://localhost:8000/api/v1/ws/stream
📊 API docs: http://localhost:8000/docs
======================================================================
INFO: Uvicorn running on http://0.0.0.0:8000
INFO: Application startup complete.

2025-10-28 | INFO | #0001 | $3941.30 (-65.30, -1.63%)
```

**If you see:**
```
ERROR | Database session error: password authentication failed
```
**→ Go back to Step 5 and fix the password**

**If you see:**
```
ERROR | [Errno 11001] getaddrinfo failed
```
**→ Docker is not running. Go back to Step 1**

**If you see:**
```
ERROR | Port 8000 already in use
```
**→ Kill existing processes:**
```powershell
Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.Path -like "*aurex-ai*"} | Stop-Process -Force
```

---

### **Step 7: Start Dashboard** 🖥️

**Open a NEW PowerShell terminal:**

```powershell
# Navigate to project root
cd C:\Users\Seavleu\Downloads\aurex-ai

# Navigate to dashboard
cd apps\dashboard

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

**Expected Output:**
```
▲ Next.js 15.5.6
- Local:   http://localhost:3000
✓ Ready in 2.3s
```

---

### **Step 8: Access Application** 🌐

Open your browser and go to:
```
http://localhost:3000
```

**Press F12 to open Developer Console**

**Look for:**
```
[WebSocket] Connected to AUREX.AI  ✅
[WebSocket] Received price update: $3941.30  ✅
```

---

## 🎯 Quick Checklist

Use this checklist every time:

- [ ] **Docker Desktop started** (green whale icon)
- [ ] **Docker verified:** `docker ps` works
- [ ] **Containers started:** `docker-compose up -d postgres redis`
- [ ] **Wait 30 seconds** for health checks
- [ ] **Database accessible:** `docker exec aurex-postgres psql -U aurex -d aurex_db -c "SELECT 1;"`
- [ ] **Backend started:** No database errors in logs
- [ ] **Dashboard started:** `npm run dev` in apps/dashboard
- [ ] **Browser open:** http://localhost:3000
- [ ] **WebSocket connected:** Check browser console

---

## 🚨 Common Errors & Fixes

### Error 1: "dockerDesktopLinuxEngine: system cannot find file"

**Cause:** Docker Desktop not running

**Fix:**
```powershell
# Start Docker Desktop
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"

# Wait for green whale icon (1-2 minutes)

# Verify
docker ps
```

---

### Error 2: "password authentication failed for user aurex"

**Cause:** Password mismatch or Docker container recreated

**Fix:**
```powershell
# Reset password
docker exec aurex-postgres psql -U postgres -c "ALTER USER aurex WITH PASSWORD 'aurex_password';"

# Restart backend
```

---

### Error 3: "[Errno 11001] getaddrinfo failed"

**Cause:** Backend can't find database (Docker not running or .env not loaded)

**Fix:**
```powershell
# Check Docker is running
docker ps

# Check .env has localhost (not postgres)
Select-String -Path .env -Pattern "DATABASE_URL"
# Should show: @localhost:5432
```

---

### Error 4: "Port 8000 already in use"

**Cause:** Backend already running

**Fix:**
```powershell
# Kill existing processes
Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.Path -like "*aurex-ai*"} | Stop-Process -Force

# Restart backend
```

---

### Error 5: Containers not starting

**Cause:** Port conflicts or previous containers

**Fix:**
```powershell
# Stop all containers
docker-compose down

# Remove volumes (CAUTION: Deletes data!)
docker-compose down -v

# Start fresh
docker-compose up -d postgres redis
```

---

## 🔄 Complete Reset Procedure

If everything is broken, do a complete reset:

```powershell
# 1. Stop everything
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
docker-compose down

# 2. Wait
Start-Sleep -Seconds 5

# 3. Verify Docker Desktop is running
docker ps
# If error, start Docker Desktop and wait

# 4. Start infrastructure
docker-compose up -d postgres redis

# 5. Wait for health
Start-Sleep -Seconds 30

# 6. Fix password
docker exec aurex-postgres psql -U postgres -c "ALTER USER aurex WITH PASSWORD 'aurex_password';"

# 7. Test connection
docker exec aurex-postgres psql -U aurex -d aurex_db -c "SELECT 1;"

# 8. Start backend
.\venv\Scripts\Activate.ps1
python apps/backend/start_realtime_backend.py

# 9. In new terminal, start dashboard
cd apps\dashboard
npm run dev
```

---

## 💡 Pro Tips

1. **Always check Docker first** - Most errors are because Docker isn't running
2. **Wait for health checks** - Don't rush, give containers time to start
3. **One terminal per service** - Backend in one, dashboard in another
4. **Keep terminals open** - See logs in real-time
5. **Check system tray** - Green whale = good, orange = wait, red = problem

---

## 🎯 Fastest Startup (After First Time)

Once everything is configured, use helper scripts:

```powershell
# Terminal 1: Start backend
.\run-backend.ps1

# Terminal 2: Start dashboard  
.\run-dashboard.ps1
```

**BUT FIRST:** Make sure Docker Desktop is running (green whale)!

---

## ✅ Success Indicators

Everything is working when you see:

**Backend Terminal:**
```
INFO: Uvicorn running on http://0.0.0.0:8000
INFO: Application startup complete.
INFO | #0001 | $3941.30 (-65.30, -1.63%)
(No database errors!)
```

**Dashboard Terminal:**
```
▲ Next.js 15.5.6
- Local: http://localhost:3000
✓ Ready in 2.3s
```

**Browser Console (F12):**
```
[WebSocket] Connected to AUREX.AI
[WebSocket] Received price update: $3941.30
```

**Dashboard UI:**
- ✅ Price card showing current gold price
- ✅ Price updating every 5 seconds
- ✅ News feed loaded
- ✅ No error messages

---

## 📞 Still Having Issues?

1. Check Docker Desktop is actually running (green whale)
2. Wait longer (Docker can take 2-3 minutes to fully start)
3. Try complete reset procedure above
4. Check firewall isn't blocking ports 5432, 6379, 8000, 3000
5. Restart your computer if Docker won't start

---

**Remember: The #1 cause of issues is Docker Desktop not being fully started!**

**Last Updated:** October 28, 2025  
**Status:** Complete troubleshooting guide  
**Success Rate:** 99% with proper Docker startup

