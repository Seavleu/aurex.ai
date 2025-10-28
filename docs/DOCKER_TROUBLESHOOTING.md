# 🐳 Docker Troubleshooting Guide

## Issue: Docker Desktop Not Running

### Error Message
```
error during connect: Get "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/v1.51/...": 
open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified.
```

### Root Cause
**Docker Desktop is not running on your system.**

---

## ✅ Solution: Start Docker Desktop

### **Step 1: Launch Docker Desktop**

#### Method A: Start Menu
```
1. Press Windows key
2. Type "Docker Desktop"
3. Click on "Docker Desktop"
4. Wait for Docker icon in system tray to appear
```

#### Method B: PowerShell
```powershell
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
```

### **Step 2: Wait for Docker to Be Ready**

**Look for the Docker icon in your system tray (bottom-right):**
- ⏳ **Orange/Animated** = Docker is starting up (wait)
- ✅ **Green** = Docker is ready
- ❌ **Red** = Docker has an error

**This usually takes 30-60 seconds.**

### **Step 3: Verify Docker is Running**

```powershell
docker ps
```

**Expected Output:**
```
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

If you see this (even with no containers), Docker is ready!

---

## 🚀 Starting AUREX.AI After Docker is Ready

Once Docker Desktop is running:

```powershell
# Method 1: Use helper script (recommended)
.\run-backend.ps1

# Method 2: Manual start
docker-compose up -d postgres redis
Start-Sleep -Seconds 30
.\venv\Scripts\Activate.ps1
python apps/backend/start_realtime_backend.py
```

---

## 🔧 Common Docker Desktop Issues

### **Issue 1: Docker Desktop Won't Start**

**Symptoms:**
- Docker icon never turns green
- Docker Desktop crashes on startup

**Solutions:**

#### A. Restart Docker Desktop
```powershell
# Close Docker Desktop
Stop-Process -Name "Docker Desktop" -Force

# Wait 5 seconds
Start-Sleep -Seconds 5

# Start Docker Desktop again
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
```

#### B. Restart WSL (Windows Subsystem for Linux)
```powershell
# As Administrator
wsl --shutdown
Start-Sleep -Seconds 5
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
```

#### C. Restart Your Computer
Sometimes Windows needs a fresh start!

---

### **Issue 2: "Docker Desktop requires a newer WSL kernel"**

**Solution:**
```powershell
# As Administrator
wsl --update
wsl --set-default-version 2
```

Then restart Docker Desktop.

---

### **Issue 3: "Hypervisor Not Enabled"**

**Solution:**
1. Restart computer
2. Enter BIOS/UEFI (usually F2, F10, or Del during boot)
3. Find "Virtualization Technology" or "Intel VT-x" or "AMD-V"
4. Enable it
5. Save and exit
6. Start Windows
7. Start Docker Desktop

---

### **Issue 4: Docker Containers Won't Start**

**Error:**
```
Error response from daemon: Conflict. The container name "/aurex-postgres" is already in use
```

**Solution:**
```powershell
# Stop all containers
docker-compose down

# Remove all containers
docker-compose down -v

# Start fresh
docker-compose up -d
```

---

### **Issue 5: Port Already in Use**

**Error:**
```
Bind for 0.0.0.0:5432 failed: port is already allocated
```

**Solution:**

#### Option A: Find and Kill Process
```powershell
# Find what's using port 5432
netstat -ano | findstr :5432

# Kill the process (replace PID with the number from above)
Stop-Process -Id <PID> -Force
```

#### Option B: Use Different Port
Edit `docker-compose.yml`:
```yaml
postgres:
  ports:
    - "5433:5432"  # Changed from 5432:5432
```

Then update `.env` file:
```
DATABASE_URL=postgresql://aurex:aurex_password@localhost:5433/aurex_db
```

---

## 📊 Docker Health Check

Use this to verify everything is working:

```powershell
# Check Docker is running
docker info

# Check containers
docker-compose ps

# Check logs
docker-compose logs postgres
docker-compose logs redis

# Check container health
docker inspect aurex-postgres --format='{{.State.Health.Status}}'
# Should return: healthy
```

---

## 🎯 Complete Startup Checklist

Use this checklist every time you start the application:

- [ ] **Docker Desktop is running** (green icon in tray)
- [ ] **Verify:** `docker ps` works without errors
- [ ] **Start infrastructure:** `docker-compose up -d postgres redis`
- [ ] **Wait 30 seconds** for health checks
- [ ] **Verify:** `docker-compose ps` shows "healthy"
- [ ] **Activate venv:** `.\venv\Scripts\Activate.ps1`
- [ ] **Start backend:** `python apps/backend/start_realtime_backend.py`
- [ ] **In new terminal, start dashboard:** `cd apps/dashboard && npm run dev`

---

## 🛠️ Advanced: Docker Desktop Settings

### Recommended Settings for AUREX.AI

Open Docker Desktop → Settings:

#### **Resources → Advanced**
```
CPUs: 4 (minimum 2)
Memory: 4 GB (minimum 2 GB)
Swap: 1 GB
Disk image size: 60 GB
```

#### **Docker Engine**
Should have default settings, but ensure:
```json
{
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  },
  "experimental": false
}
```

---

## 📚 Quick Reference

| Command | Purpose |
|---------|---------|
| `docker ps` | Check running containers |
| `docker-compose ps` | Check project containers |
| `docker-compose up -d` | Start all services |
| `docker-compose down` | Stop all services |
| `docker-compose logs -f <service>` | View service logs |
| `docker-compose restart <service>` | Restart a service |
| `docker system prune` | Clean up unused resources |

---

## 🆘 Still Having Issues?

### Check Docker Desktop Status Page
Open Docker Desktop → Troubleshoot → View Status

### Reset Docker Desktop to Factory Defaults
**Warning:** This will delete all containers, images, and volumes!

```
Docker Desktop → Troubleshoot → Reset to factory defaults
```

### Get Docker Info
```powershell
docker info
docker version
wsl --status  # If using WSL 2 backend
```

### Check Windows Features
```powershell
# As Administrator
Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V
Get-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform
```

Both should show: `State : Enabled`

---

## ✅ Success Verification

When everything is working correctly:

### Docker Desktop
- ✅ Green whale icon in system tray
- ✅ Docker Desktop window shows "Engine running"

### Terminal
```powershell
PS> docker ps
# Shows table (even if empty)

PS> docker-compose ps
# Shows aurex-postgres (healthy) and aurex-redis (healthy)
```

### Backend
```powershell
PS> python apps/backend/start_realtime_backend.py
# Shows:
# ======================================================================
# 🚀 AUREX.AI Real-Time Backend
# ======================================================================
```

### Browser
```
http://localhost:8000/api/v1/health
# Returns: {"status": "healthy", "database": "connected", ...}
```

---

## 💡 Pro Tips

1. **Always start Docker Desktop first** before running any docker commands
2. **Wait for the green icon** in system tray before running commands
3. **Check logs** if containers fail: `docker-compose logs <service>`
4. **Clean up regularly:** `docker system prune` to free disk space
5. **Use helper scripts:** `.\run-backend.ps1` handles Docker startup automatically

---

## 🚀 After Docker is Fixed

Once Docker Desktop is running properly:

1. **Close any error terminals**
2. **Run the helper script:**
   ```powershell
   .\run-backend.ps1
   ```
3. **In a new terminal:**
   ```powershell
   .\run-dashboard.ps1
   ```
4. **Open browser:**
   ```
   http://localhost:3000
   ```

---

**Status:** Ready to troubleshoot! 🛠️  
**Most Common Fix:** Just start Docker Desktop and wait 30 seconds  
**Support:** See Docker Desktop troubleshooting section

---

**Last Updated:** October 28, 2025  
**For:** AUREX.AI v2.0.0

