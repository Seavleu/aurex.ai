# AUREX.AI - Makefile
# Development automation commands

.PHONY: help install setup test lint format clean docker-up docker-down docker-logs

# Default target
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "AUREX.AI - Development Commands"
	@echo "================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Setup & Installation
install: ## Install Python dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements.txt
	pre-commit install

setup: ## Complete project setup
	@echo "Setting up AUREX.AI..."
	python -m venv venv
	@echo "Please activate virtual environment:"
	@echo "  Windows: venv\\Scripts\\activate"
	@echo "  macOS/Linux: source venv/bin/activate"
	@echo "Then run: make install-dev"

# Code Quality
format: ## Format code with Black
	black apps/ packages/

lint: ## Lint code with Ruff
	ruff check apps/ packages/ --fix

lint-check: ## Check code without fixing
	ruff check apps/ packages/

type-check: ## Run type checking with mypy
	mypy apps/ packages/

quality: format lint type-check ## Run all code quality checks

# Testing
test: ## Run all tests
	pytest

test-unit: ## Run unit tests only
	pytest -m unit

test-integration: ## Run integration tests only
	pytest -m integration

test-coverage: ## Run tests with coverage report
	pytest --cov=apps --cov=packages --cov-report=html --cov-report=term

test-verbose: ## Run tests in verbose mode
	pytest -v

# Docker Commands
docker-build: ## Build all Docker images
	docker-compose build

docker-up: ## Start all services
	docker-compose up -d

docker-down: ## Stop all services
	docker-compose down

docker-restart: ## Restart all services
	docker-compose restart

docker-logs: ## View logs from all services
	docker-compose logs -f

docker-logs-backend: ## View backend logs
	docker-compose logs -f backend

docker-logs-pipeline: ## View pipeline logs
	docker-compose logs -f pipeline

docker-ps: ## Show running containers
	docker-compose ps

docker-clean: ## Remove all containers and volumes
	docker-compose down -v

# Database Commands
db-init: ## Initialize database
	docker-compose exec postgres psql -U aurex -d aurex_db -f /docker-entrypoint-initdb.d/init_db.sql

db-shell: ## Open PostgreSQL shell
	docker-compose exec postgres psql -U aurex -d aurex_db

db-migrate: ## Run database migrations
	docker-compose exec backend alembic upgrade head

db-reset: ## Reset database (WARNING: destroys data)
	docker-compose down -v
	docker-compose up -d postgres
	sleep 5
	make db-init

# Redis Commands
redis-cli: ## Open Redis CLI
	docker-compose exec redis redis-cli

redis-flush: ## Flush Redis cache
	docker-compose exec redis redis-cli FLUSHALL

# Development
dev-backend: ## Run backend locally
	cd apps/backend && uvicorn main:app --reload --port 8000

dev-pipeline: ## Run pipeline locally
	cd apps/pipeline && python main.py

dev-dashboard: ## Run Next.js dashboard locally
	cd apps/dashboard && npm run dev

# API Commands
api-docs: ## Open API documentation
	@echo "Opening API docs at http://localhost:8000/docs"
	@python -m webbrowser http://localhost:8000/docs

api-test: ## Test API endpoints
	curl -s http://localhost:8000/health | jq
	curl -s http://localhost:8000/sentiment/latest | jq
	curl -s http://localhost:8000/price/current | jq

# Pre-commit
pre-commit-install: ## Install pre-commit hooks
	pre-commit install

pre-commit-run: ## Run pre-commit on all files
	pre-commit run --all-files

# Cleanup
clean: ## Clean temporary files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/

clean-all: clean docker-clean ## Clean everything including Docker

# Sprint Management
sprint-status: ## Show current sprint status
	@echo "Current Sprint Status:"
	@echo "======================"
	@cat docs/SPRINT_PLANNING.md | grep -A 10 "Current Sprint"

backlog: ## Show product backlog
	@cat docs/PRODUCT_BACKLOG.md | less

# Quick Start
quickstart: docker-build docker-up ## Quick start all services
	@echo "✅ AUREX.AI is starting..."
	@echo "⏳ Waiting for services to be ready..."
	@sleep 10
	@echo "✅ Services ready!"
	@echo ""
	@echo "📊 Access points:"
	@echo "  - API: http://localhost:8000"
	@echo "  - API Docs: http://localhost:8000/docs"
	@echo "  - Prefect UI: http://localhost:4200"
	@echo "  - PostgreSQL: localhost:5432"
	@echo "  - Redis: localhost:6379"

# Production
prod-deploy: ## Deploy to production (Railway + Vercel)
	@echo "Deploying to production..."
	railway up
	cd apps/dashboard && vercel --prod

