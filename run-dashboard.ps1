# AUREX.AI - Dashboard Startup Script
Write-Host "Starting AUREX.AI Dashboard..." -ForegroundColor Green

# Navigate to dashboard
Set-Location apps/dashboard

# Check if node_modules exists
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    npm install
}

# Create .env.local if it doesn't exist
if (-not (Test-Path ".env.local")) {
    Write-Host "Creating .env.local..." -ForegroundColor Yellow
    "NEXT_PUBLIC_API_URL=http://localhost:8000" | Out-File -FilePath ".env.local" -Encoding UTF8
}

# Run dev server
npm run dev

