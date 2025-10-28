# AUREX.AI - Backend Startup Script
Write-Host "Starting AUREX.AI Backend..." -ForegroundColor Green

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Set PYTHONPATH
$env:PYTHONPATH = $PWD

# Check if dependencies are installed
Write-Host "Checking dependencies..." -ForegroundColor Yellow
try {
    python -c "import loguru, fastapi, uvicorn" 2>$null
} catch {
    Write-Host "Installing backend dependencies..." -ForegroundColor Yellow
    pip install fastapi uvicorn loguru
}

# Start Docker infrastructure first
Write-Host "Starting Docker containers..." -ForegroundColor Yellow
docker-compose up -d postgres redis

Write-Host "Waiting for containers to be healthy (30 seconds)..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Run real-time backend
Write-Host "Starting real-time backend server on http://localhost:8000..." -ForegroundColor Green
Write-Host "WebSocket endpoint: ws://localhost:8000/api/v1/ws/stream" -ForegroundColor Cyan
python apps/backend/start_realtime_backend.py

