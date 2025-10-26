# 🚀 AUREX.AI - Quick Start Guide

## Start the Application (2 Terminals Required)

### Terminal 1: Backend API

```powershell
# Set PYTHONPATH and run backend
$env:PYTHONPATH = "$pwd"
python apps/backend/main.py
```

**Backend will run on:** http://localhost:8000  
**API Docs:** http://localhost:8000/docs

---

### Terminal 2: Dashboard

```powershell
# Navigate to dashboard
cd apps/dashboard

# Create .env.local (first time only)
"NEXT_PUBLIC_API_URL=http://localhost:8000" | Out-File -FilePath ".env.local" -Encoding UTF8

# Install dependencies (first time only)
npm install

# Run dev server
npm run dev
```

**Dashboard will run on:** http://localhost:3000

---

## Alternative: Use PowerShell Scripts

### Terminal 1:
```powershell
.\run-backend.ps1
```

### Terminal 2:
```powershell
.\run-dashboard.ps1
```

---

## Verify Everything Works

1. ✅ Backend: http://localhost:8000
2. ✅ API Docs: http://localhost:8000/docs
3. ✅ Dashboard: http://localhost:3000

The dashboard should now fetch data from the API!

---

## Troubleshooting

### "Failed to fetch" or CORS errors
- ✅ Make sure backend is running (Terminal 1)
- ✅ Check `.env.local` in `apps/dashboard/` has: `NEXT_PUBLIC_API_URL=http://localhost:8000`
- ✅ Restart the dashboard after creating `.env.local`

### Backend import errors
- ✅ Make sure you set: `$env:PYTHONPATH = "$pwd"`
- ✅ Run from project root, not from `apps/backend/`

### Dashboard won't start
- ✅ Run `npm install` in `apps/dashboard/`
- ✅ Make sure you have Node.js 18+ installed

---

## Docker Alternative

If you prefer Docker:

```bash
docker-compose up -d
```

This starts:
- Backend API on http://localhost:8000
- PostgreSQL on localhost:5432
- Redis on localhost:6379
- Prefect on http://localhost:4200

Then just run the dashboard separately:
```powershell
cd apps/dashboard
npm install
npm run dev
```

