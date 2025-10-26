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

# Run backend
Write-Host "Starting backend server on http://localhost:8000..." -ForegroundColor Green
python apps/backend/main.py

