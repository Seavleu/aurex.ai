# AUREX.AI - Project Initialization Script (PowerShell)

Write-Host "🚀 Initializing AUREX.AI Project..." -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green

# Step 1: Create .env file
Write-Host "`n📝 Step 1: Creating .env file..." -ForegroundColor Cyan
if (-Not (Test-Path .env)) {
    Copy-Item env.example .env
    Write-Host "✅ .env file created" -ForegroundColor Green
} else {
    Write-Host "⚠️  .env file already exists, skipping..." -ForegroundColor Yellow
}

# Step 2: Python environment
Write-Host "`n🐍 Step 2: Setting up Python environment..." -ForegroundColor Cyan
if (-Not (Test-Path venv)) {
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "⚠️  Virtual environment already exists" -ForegroundColor Yellow
}

Write-Host "📦 Installing Python dependencies..." -ForegroundColor Cyan
& .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Write-Host "✅ Python dependencies installed" -ForegroundColor Green

# Step 3: Pre-commit hooks
Write-Host "`n🎣 Step 3: Installing pre-commit hooks..." -ForegroundColor Cyan
pre-commit install
Write-Host "✅ Pre-commit hooks installed" -ForegroundColor Green

# Step 4: Next.js setup
Write-Host "`n⚛️  Step 4: Setting up Next.js dashboard..." -ForegroundColor Cyan
Set-Location apps\dashboard
if (-Not (Test-Path node_modules)) {
    npm install
    Write-Host "✅ Next.js dependencies installed" -ForegroundColor Green
} else {
    Write-Host "⚠️  node_modules already exists" -ForegroundColor Yellow
}
Set-Location ..\..

# Step 5: Docker setup
Write-Host "`n🐳 Step 5: Starting Docker services..." -ForegroundColor Cyan
docker-compose up -d
Write-Host "✅ Docker services started" -ForegroundColor Green

Write-Host "`n⏳ Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check services
Write-Host "`n🔍 Checking service health..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri http://localhost:8000/health -UseBasicParsing
    Write-Host "✅ Backend is healthy!" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Backend not ready yet, may need more time" -ForegroundColor Yellow
}

Write-Host "`n======================================" -ForegroundColor Green
Write-Host "✅ Project initialization complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Access Points:" -ForegroundColor Cyan
Write-Host "  - Backend API: http://localhost:8000"
Write-Host "  - API Docs: http://localhost:8000/docs"
Write-Host "  - Dashboard: http://localhost:3000 (run 'cd apps/dashboard; npm run dev')"
Write-Host "  - Prefect UI: http://localhost:4200"
Write-Host ""
Write-Host "🚀 Next steps:" -ForegroundColor Yellow
Write-Host "  1. Test backend: curl http://localhost:8000/health"
Write-Host "  2. Start dashboard: cd apps\dashboard; npm run dev"
Write-Host "  3. Check Sprint 1 backlog: cat docs\SPRINT_PLANNING.md"
Write-Host ""
Write-Host "Happy coding! 🎉" -ForegroundColor Green

