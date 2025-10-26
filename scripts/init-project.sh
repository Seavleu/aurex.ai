#!/bin/bash
# AUREX.AI - Project Initialization Script

echo "🚀 Initializing AUREX.AI Project..."
echo "===================================="

# Step 1: Create .env file
echo "📝 Step 1: Creating .env file..."
if [ ! -f .env ]; then
    cp env.example .env
    echo "✅ .env file created"
else
    echo "⚠️  .env file already exists, skipping..."
fi

# Step 2: Python environment
echo ""
echo "🐍 Step 2: Setting up Python environment..."
if [ ! -d "venv" ]; then
    python -m venv venv
    echo "✅ Virtual environment created"
else
    echo "⚠️  Virtual environment already exists"
fi

echo "📦 Installing Python dependencies..."
source venv/bin/activate || . venv/Scripts/activate
pip install -r requirements.txt
echo "✅ Python dependencies installed"

# Step 3: Pre-commit hooks
echo ""
echo "🎣 Step 3: Installing pre-commit hooks..."
pre-commit install
echo "✅ Pre-commit hooks installed"

# Step 4: Next.js setup
echo ""
echo "⚛️  Step 4: Setting up Next.js dashboard..."
cd apps/dashboard
if [ ! -d "node_modules" ]; then
    npm install
    echo "✅ Next.js dependencies installed"
else
    echo "⚠️  node_modules already exists"
fi
cd ../..

# Step 5: Docker setup
echo ""
echo "🐳 Step 5: Starting Docker services..."
docker-compose up -d
echo "✅ Docker services started"

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check services
echo ""
echo "🔍 Checking service health..."
curl -s http://localhost:8000/health | jq || echo "⚠️  Backend not ready yet"

echo ""
echo "======================================"
echo "✅ Project initialization complete!"
echo ""
echo "📊 Access Points:"
echo "  - Backend API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - Dashboard: http://localhost:3000 (run 'cd apps/dashboard && npm run dev')"
echo "  - Prefect UI: http://localhost:4200"
echo ""
echo "🚀 Next steps:"
echo "  1. Test backend: curl http://localhost:8000/health"
echo "  2. Start dashboard: cd apps/dashboard && npm run dev"
echo "  3. Check Sprint 1 backlog: cat docs/SPRINT_PLANNING.md"
echo ""
echo "Happy coding! 🎉"

