# 🚀 START HERE - AUREX.AI Setup

## ⚡ Quick Start (Follow These Steps)

### Step 1: Start Backend (Terminal 1)

Open a **NEW PowerShell terminal** and run:

```powershell
cd C:\Users\Seavleu\Downloads\aurex-ai
.\run-backend.ps1
```

**Keep this terminal running!** You should see:
```
✅ AUREX.AI Backend Starting...
✅ INFO: Uvicorn running on http://0.0.0.0:8000
```

---

### Step 2: Start Dashboard (Terminal 2 - Current One)

In your **CURRENT terminal** where the dashboard is running, do:

```powershell
# Press CTRL+C to stop the dashboard first
# Then restart it:

cd apps/dashboard
npm run dev
```

---

## 🎯 Expected Result

After both are running:

1. **Backend:** http://localhost:8000 ✅
2. **Dashboard:** http://localhost:3000 ✅
3. **No more "Failed to fetch" errors!** 🎉

---

## 📊 What You'll See

The dashboard will show:
- 💰 Real-time Gold Price
- 🤖 Sentiment Analysis Gauge
- 📰 Latest News Feed
- ✨ Auto-refreshing data every 30-60s

---

## ⚠️ Current Issue

Your dashboard is running, but the **backend is NOT running yet**.

That's why you're seeing:
```
❌ Failed to fetch
```

The dashboard is trying to connect to `http://localhost:8000` but nothing is there!

---

## 🔧 Solution

**Run the backend script now in a NEW terminal!**

```powershell
.\run-backend.ps1
```

Leave it running, then your dashboard will work! 🚀

