# 🔌 Port 8000 Already in Use - Quick Fix Guide

## ❌ Error

```
ERROR: [Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000): 
[winerror 10048] only one usage of each socket address (protocol/network address/port) 
is normally permitted
```

---

## 🎯 What This Means

**Port 8000 is already in use!**

This happens when:
1. Backend is already running from a previous session
2. Another application is using port 8000
3. A crashed process didn't release the port

---

## ✅ Quick Fix

### **Option 1: Kill Processes Using Port 8000 (Recommended)**

```powershell
# Find what's using port 8000
netstat -ano | Select-String ":8000"

# You'll see something like:
# TCP  0.0.0.0:8000  LISTENING  12345
#                                 ^^^^^ This is the Process ID (PID)

# Kill the process (replace 12345 with actual PID)
Stop-Process -Id 12345 -Force

# If multiple PIDs, kill all at once:
Stop-Process -Id 12345,67890 -Force
```

### **Option 2: Kill All Python Processes**

```powershell
# Stop all Python processes in this project
Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.Path -like "*aurex-ai*"} | Stop-Process -Force
```

### **Option 3: Use a Different Port**

Edit `.env` file:
```bash
# Change this:
API_PORT=8000

# To this:
API_PORT=8001
```

Then update dashboard to connect to new port in `apps/dashboard/.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8001
```

---

## 🔍 How to Check if Port is Free

```powershell
netstat -ano | Select-String ":8000"
```

**Expected Output (Port Free):**
```
(No output) ✅
```

**Output (Port in Use):**
```
TCP  0.0.0.0:8000  LISTENING  12345 ❌
```

---

## 🚀 Proper Startup Sequence

To avoid this issue:

### **1. Stop Any Running Instances**
```powershell
# Kill any existing backend processes
Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.Path -like "*aurex-ai*"} | Stop-Process -Force
```

### **2. Verify Port is Free**
```powershell
netstat -ano | Select-String ":8000"
# Should return nothing
```

### **3. Start Backend**
```powershell
.\run-backend.ps1
```

---

## 🛠️ Advanced Troubleshooting

### **Find What Application is Using Port 8000**

```powershell
# Get the PID
$pid = (netstat -ano | Select-String ":8000" | Select-Object -First 1) -replace '.*\s(\d+)$','$1'

# Get the process details
Get-Process -Id $pid | Select-Object Id, ProcessName, Path
```

### **Check if Docker Backend is Running**

```powershell
docker ps --filter "name=aurex-backend"
```

If the backend is running in Docker, you have two options:

**Option A: Use Docker Backend**
```powershell
# Stop local backend
Get-Process python | Stop-Process -Force

# Let Docker backend handle it
docker-compose up -d backend
```

**Option B: Use Local Backend**
```powershell
# Stop Docker backend
docker-compose stop backend

# Start local backend
.\run-backend.ps1
```

---

## ⚠️ Common Scenarios

### **Scenario 1: Backend Running in Background**

**Symptom:** You closed the terminal but backend is still running

**Fix:**
```powershell
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
```

### **Scenario 2: Multiple Terminal Windows**

**Symptom:** You opened multiple terminals and ran backend in each

**Fix:**
```powershell
# Close all terminals
# Kill all Python processes
Get-Process python | Where-Object {$_.Path -like "*aurex-ai*"} | Stop-Process -Force
```

### **Scenario 3: Docker and Local Backend Both Running**

**Symptom:** Both Docker container and local Python trying to use port 8000

**Fix:**
```powershell
# Stop Docker backend
docker-compose stop backend

# Or stop local backend
Get-Process python | Stop-Process -Force
```

---

## 📝 Prevention Tips

### **1. Always Check Before Starting**
```powershell
# Check if anything is running on 8000
netstat -ano | Select-String ":8000"

# If nothing shows up, you're good to start!
```

### **2. Use ONE Method**

Choose either:
- **Local Python** → Use `.\run-backend.ps1`
- **Docker** → Use `docker-compose up -d`

**Don't mix both!**

### **3. Clean Shutdown**

Always stop properly:
```powershell
# For local backend: Press Ctrl+C in terminal

# For Docker backend:
docker-compose down
```

### **4. Create a Restart Script**

Create `restart-backend.ps1`:
```powershell
# Stop any existing
Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.Path -like "*aurex-ai*"} | Stop-Process -Force

# Wait
Start-Sleep -Seconds 2

# Start fresh
.\run-backend.ps1
```

---

## 🔄 Complete Reset

If nothing works, do a complete reset:

```powershell
# 1. Stop all Python processes
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

# 2. Stop Docker containers
docker-compose down

# 3. Wait
Start-Sleep -Seconds 5

# 4. Start Docker infrastructure only
docker-compose up -d postgres redis

# 5. Wait for health checks
Start-Sleep -Seconds 30

# 6. Start backend
.\run-backend.ps1
```

---

## ✅ Success Indicators

When backend starts successfully, you should see:

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
```

**No errors about port binding!** ✅

---

## 🆘 Still Having Issues?

### **Last Resort: Change the Port**

1. Edit `.env`:
```bash
API_PORT=8001
```

2. Edit `apps/dashboard/.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8001
```

3. Restart both backend and dashboard

---

## 📊 Quick Command Reference

| Task | Command |
|------|---------|
| Check port usage | `netstat -ano \| Select-String ":8000"` |
| Kill process by PID | `Stop-Process -Id <PID> -Force` |
| Kill all Python | `Get-Process python \| Stop-Process -Force` |
| Stop Docker backend | `docker-compose stop backend` |
| Verify backend running | `curl http://localhost:8000/` |

---

## 💡 Pro Tips

1. **Use one terminal** for backend - easier to track
2. **Check port before starting** - save time
3. **Use Ctrl+C to stop** - clean shutdown
4. **Don't run in background** - harder to manage
5. **Keep terminal open** - see logs in real-time

---

**Last Updated:** October 28, 2025  
**Common Issue:** Port conflicts  
**Fix Time:** < 1 minute  
**Prevention:** Check port before starting

