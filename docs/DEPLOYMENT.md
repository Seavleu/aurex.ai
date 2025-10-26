# 🚀 AUREX.AI - Deployment Guide

This guide covers deploying AUREX.AI to production environments.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Prefect Deployment](#prefect-deployment)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

- Docker & Docker Compose
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Node.js 18+ (for dashboard)

---

## Environment Setup

### 1. Configure Environment Variables

```bash
cp env.example .env
```

Edit `.env` and set your values:

```bash
# Database
DATABASE_URL=postgresql+asyncpg://aurex:your_password@localhost:5432/aurex_db

# Redis
REDIS_URL=redis://localhost:6379/0

# API
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# AI/ML
FINBERT_MODEL_NAME=ProsusAI/finbert
DEVICE=gpu  # or cpu
INFERENCE_BATCH_SIZE=16

# Application
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=INFO
```

---

## Docker Deployment

### 1. Build and Start Services

```bash
docker-compose up -d
```

### 2. Check Service Health

```bash
docker-compose ps
```

All services should show "healthy" or "running".

### 3. Initialize Database

The database is automatically initialized via `infra/init_db.sql` on first startup.

To manually initialize:

```bash
docker-compose exec postgres psql -U aurex -d aurex_db -f /docker-entrypoint-initdb.d/init_db.sql
```

### 4. View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f pipeline
docker-compose logs -f prefect
```

---

## Cloud Deployment

### Railway.app (Backend & Database)

1. **Create Railway Project**
   ```bash
   railway login
   railway init
   ```

2. **Add PostgreSQL Plugin**
   - Go to Railway dashboard
   - Add PostgreSQL plugin
   - Note the `DATABASE_URL`

3. **Add Redis Plugin**
   - Add Redis plugin
   - Note the `REDIS_URL`

4. **Deploy Backend**
   ```bash
   railway up
   ```

5. **Set Environment Variables**
   - Go to project settings
   - Add all variables from `.env`

### Vercel (Dashboard)

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Deploy Dashboard**
   ```bash
   cd apps/dashboard
   vercel
   ```

3. **Set Environment Variables**
   - Go to Vercel dashboard
   - Add:
     ```
     NEXT_PUBLIC_API_URL=https://your-railway-api.railway.app
     ```

---

## Prefect Deployment

### 1. Start Prefect Server

Already running in Docker:

```bash
docker-compose up -d prefect
```

Access UI at: http://localhost:4200

### 2. Deploy Flows

From inside the pipeline container:

```bash
docker-compose exec pipeline bash

# Register deployments
prefect deployment apply apps/pipeline/prefect.yaml
```

### 3. Start Worker

```bash
# Inside container
python apps/pipeline/main.py --continuous
```

Or use the Docker service (already configured):

```bash
docker-compose up -d pipeline
```

### 4. Trigger Flow Manually

```bash
prefect deployment run gold-sentiment-pipeline/gold-sentiment-pipeline
```

---

## Monitoring

### Prefect UI

- **URL:** http://localhost:4200
- **Features:**
  - Flow runs history
  - Task execution details
  - Logs and errors
  - Scheduled runs

### Application Logs

```bash
# View logs
docker-compose logs -f pipeline

# Search logs
docker-compose logs pipeline | grep ERROR
```

### Database Monitoring

```bash
# Connect to database
docker-compose exec postgres psql -U aurex -d aurex_db

# Check table sizes
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

# Check recent data
SELECT COUNT(*), MAX(timestamp) FROM price;
SELECT COUNT(*), MAX(published) FROM news;
SELECT COUNT(*), MAX(timestamp) FROM sentiment_summary;
```

### Redis Monitoring

```bash
# Connect to Redis
docker-compose exec redis redis-cli

# Check keys
KEYS *

# Check memory usage
INFO memory
```

---

## Troubleshooting

### Service Won't Start

```bash
# Check logs
docker-compose logs service_name

# Restart service
docker-compose restart service_name

# Rebuild and restart
docker-compose up -d --build service_name
```

### Database Connection Issues

```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Check connection from container
docker-compose exec backend python -c "from packages.db_core.connection import get_db_manager; import asyncio; asyncio.run(get_db_manager().health_check())"
```

### FinBERT Model Loading Issues

```bash
# Check GPU availability
docker-compose exec pipeline python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"

# Download model manually
docker-compose exec pipeline python -c "from transformers import AutoModel; AutoModel.from_pretrained('ProsusAI/finbert')"
```

### Prefect Flow Failures

1. Check Prefect UI: http://localhost:4200
2. View flow run logs
3. Check task retry settings
4. Verify environment variables

### Out of Memory

```bash
# Check memory usage
docker stats

# Increase Docker memory limit
# Docker Desktop -> Settings -> Resources -> Memory
```

---

## Production Checklist

- [ ] Set `ENVIRONMENT=production` in `.env`
- [ ] Set `DEBUG=False`
- [ ] Use strong database password
- [ ] Enable HTTPS/TLS for API
- [ ] Set up database backups
- [ ] Configure log aggregation (e.g., ELK, Datadog)
- [ ] Set up monitoring alerts
- [ ] Enable rate limiting on API
- [ ] Use secrets manager for credentials
- [ ] Configure CORS properly
- [ ] Set up CI/CD pipeline
- [ ] Enable automatic restarts (Docker restart policy)
- [ ] Document runbook for incidents
- [ ] Test disaster recovery procedures

---

## Backup & Recovery

### Database Backup

```bash
# Backup
docker-compose exec postgres pg_dump -U aurex aurex_db > backup_$(date +%Y%m%d).sql

# Restore
docker-compose exec -T postgres psql -U aurex aurex_db < backup_20250127.sql
```

### Full System Backup

```bash
# Export Docker volumes
docker run --rm -v aurex-ai_postgres_data:/data -v $(pwd):/backup ubuntu tar czf /backup/postgres_backup.tar.gz /data
```

---

## Scaling

### Horizontal Scaling

1. **Add more pipeline workers:**
   ```bash
   docker-compose up -d --scale pipeline=3
   ```

2. **Add more API workers:**
   Edit `docker-compose.yml`:
   ```yaml
   command: uvicorn main:app --host 0.0.0.0 --port 8000 --workers 8
   ```

### Vertical Scaling

Increase resource limits in `docker-compose.yml`:

```yaml
services:
  pipeline:
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
```

---

## Support

- **Documentation:** `/docs`
- **Issues:** GitHub Issues
- **Contact:** dev@aurex.ai

---

**Last Updated:** Sprint 1
**Version:** 1.0.0

