# 🐳 Docker MCP Quick Reference

## Usage

### Check Status
```bash
python scripts/docker_cli.py status
```

### Fetch News
```bash
python scripts/docker_cli.py fetch-news
```

### Fetch Prices
```bash
python scripts/docker_cli.py fetch-prices
```

### View Logs
```bash
python scripts/docker_cli.py logs backend --tail 100
python scripts/docker_cli.py logs pipeline
```

### Restart Service
```bash
python scripts/docker_cli.py restart backend
```

### Execute Command
```bash
python scripts/docker_cli.py exec backend python --version
python scripts/docker_cli.py exec postgres psql -U aurex -d aurex_db -c "SELECT COUNT(*) FROM news;"
```

### Run Pipeline
```bash
# Run once
python scripts/docker_cli.py pipeline

# Run continuously
python scripts/docker_cli.py pipeline --continuous
```

## Services
- `postgres` - PostgreSQL database
- `redis` - Redis cache
- `backend` - FastAPI backend
- `pipeline` - Data pipeline
- `prefect` - Prefect server

## For More Details
See: `docs/MCP_DOCKER_GUIDE.md`

