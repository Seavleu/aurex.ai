# 🐳 AUREX.AI - Docker MCP Server Guide

## Overview

The Docker MCP (Model Context Protocol) server provides programmatic access to AUREX.AI container management, enabling automated operations and AI-assisted development workflows.

---

## 🚀 Quick Start

### Option 1: Use the CLI (Recommended)

```bash
# Make the CLI executable
chmod +x scripts/docker_cli.py

# Check container status
python scripts/docker_cli.py status

# Fetch news
python scripts/docker_cli.py fetch-news

# Fetch prices
python scripts/docker_cli.py fetch-prices

# View logs
python scripts/docker_cli.py logs backend --tail 100

# Restart a service
python scripts/docker_cli.py restart backend
```

### Option 2: Use the MCP Server

```bash
# Set environment variables
export PROJECT_ROOT=$(pwd)
export COMPOSE_FILE=$(pwd)/docker-compose.yml

# Run MCP server
python -m scripts.mcp_docker_manager
```

---

## 📋 Available Commands

### Container Management

#### 1. Status Check
```bash
python scripts/docker_cli.py status
```

**Output:**
```
🔍 AUREX.AI Container Status
======================================================================

✅ POSTGRES
   State: running
   Database: ✅

✅ REDIS
   State: running
   Cache: ✅

✅ BACKEND
   State: running
   API: ✅

✅ PIPELINE
   State: running

✅ PREFECT
   State: running
```

#### 2. View Logs
```bash
# Last 50 lines (default)
python scripts/docker_cli.py logs backend

# Last 100 lines
python scripts/docker_cli.py logs backend --tail 100

# All services
python scripts/docker_cli.py logs postgres
python scripts/docker_cli.py logs redis
python scripts/docker_cli.py logs pipeline
python scripts/docker_cli.py logs prefect
```

#### 3. Restart Services
```bash
python scripts/docker_cli.py restart backend
python scripts/docker_cli.py restart pipeline
```

#### 4. Execute Commands
```bash
# Run a command in a container
python scripts/docker_cli.py exec backend python --version
python scripts/docker_cli.py exec postgres psql -U aurex -d aurex_db -c "SELECT COUNT(*) FROM news;"
```

---

### Data Operations

#### 1. Fetch News
```bash
python scripts/docker_cli.py fetch-news
```

**What it does:**
- Connects to NewsAPI
- Fetches gold-related articles from last 24 hours
- Stores in database
- Shows summary of fetched articles

**Output:**
```
📰 Fetching gold news from NewsAPI...
✅ Fetched 45 articles
💾 Storing articles in database...
✅ Stored 45 articles
✅ News fetching completed
```

#### 2. Fetch Prices
```bash
python scripts/docker_cli.py fetch-prices
```

**What it does:**
- Fetches real-time gold prices from Yahoo Finance
- Stores in database
- Shows current price and change

#### 3. Run Pipeline
```bash
# Run once
python scripts/docker_cli.py pipeline

# Run continuously
python scripts/docker_cli.py pipeline --continuous
```

**What it does:**
- Runs the complete data pipeline
- Fetches prices, news, and analyzes sentiment
- Can run once or continuously

---

## 🔧 MCP Protocol Details

### Request Format

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "fetch_news",
  "params": {}
}
```

### Response Format

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "success": true,
    "output": "✅ Fetched 45 articles"
  }
}
```

### Available Methods

| Method | Parameters | Description |
|--------|------------|-------------|
| `list_containers` | - | List all containers |
| `container_status` | `service: str` | Get service status |
| `container_logs` | `service: str, tail: int` | Get container logs |
| `start_service` | `service: str` | Start a service |
| `stop_service` | `service: str` | Stop a service |
| `restart_service` | `service: str` | Restart a service |
| `exec_command` | `service: str, command: List[str]` | Execute command |
| `health_check` | - | Check all services health |
| `fetch_news` | - | Fetch gold news |
| `fetch_prices` | - | Fetch real-time prices |
| `run_pipeline` | `mode: str` | Run data pipeline |

---

## 🤖 AI Integration

The MCP server can be integrated with AI assistants (like Claude, ChatGPT, or Cursor) to enable:

1. **Automated Monitoring**
   - Check container health on schedule
   - Alert on failures
   - Automatic restart on crash

2. **Data Fetching**
   - Scheduled news fetching
   - Real-time price updates
   - Pipeline orchestration

3. **Debugging**
   - Automatic log analysis
   - Health diagnostics
   - Performance monitoring

### Example: Cursor Integration

Add to `.cursor/config.json`:

```json
{
  "mcp": {
    "servers": {
      "aurex-docker": {
        "command": "python",
        "args": ["-m", "scripts.mcp_docker_manager"],
        "env": {
          "PROJECT_ROOT": "${workspaceFolder}",
          "COMPOSE_FILE": "${workspaceFolder}/docker-compose.yml"
        }
      }
    }
  }
}
```

---

## 📊 Common Workflows

### Workflow 1: Daily News Update

```bash
#!/bin/bash
# daily_update.sh

# Check if containers are running
python scripts/docker_cli.py status

# Fetch fresh news
python scripts/docker_cli.py fetch-news

# Fetch latest prices
python scripts/docker_cli.py fetch-prices

# Check results in database
python scripts/docker_cli.py exec postgres psql -U aurex -d aurex_db -c "SELECT COUNT(*) FROM news WHERE timestamp > NOW() - INTERVAL '1 day';"
```

### Workflow 2: Health Monitoring

```bash
#!/bin/bash
# health_check.sh

# Get health status
python scripts/docker_cli.py status > health_status.txt

# If any service is down, restart it
if grep -q "❌" health_status.txt; then
    echo "Some services are down, restarting..."
    python scripts/docker_cli.py restart backend
    python scripts/docker_cli.py restart pipeline
fi
```

### Workflow 3: Continuous Data Collection

```bash
#!/bin/bash
# continuous_collection.sh

# Start continuous pipeline
python scripts/docker_cli.py pipeline --continuous &

# Fetch news every hour
while true; do
    python scripts/docker_cli.py fetch-news
    sleep 3600
done
```

---

## 🔐 Security Considerations

1. **Docker Socket Access**
   - The MCP server needs access to Docker socket
   - Ensure proper permissions: `chmod 666 /var/run/docker.sock` (dev only)
   - In production, use Docker socket proxy

2. **API Keys**
   - NewsAPI key is in environment variables
   - Alltick API key is in environment variables
   - Never commit API keys to git

3. **Network Security**
   - MCP server runs locally only
   - No external network access required
   - All operations within Docker network

---

## 🐛 Troubleshooting

### Issue: "Cannot connect to Docker daemon"

**Solution:**
```bash
# Check Docker is running
docker ps

# Check Docker socket permissions
ls -la /var/run/docker.sock

# Restart Docker service
sudo systemctl restart docker
```

### Issue: "Module not found"

**Solution:**
```bash
# Install requirements
pip install -r requirements.txt

# Add project to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Issue: "Service not responding"

**Solution:**
```bash
# Check logs
python scripts/docker_cli.py logs backend --tail 100

# Restart service
python scripts/docker_cli.py restart backend

# Full restart
docker-compose restart
```

---

## 📈 Performance Metrics

The MCP server tracks:
- Container uptime
- API response times
- Data fetch success rates
- Database query performance

View metrics:
```bash
python scripts/docker_cli.py exec backend curl http://localhost:8000/metrics
```

---

## 🎯 Next Steps

1. **Automate Data Collection**
   ```bash
   # Set up cron job
   crontab -e
   # Add: 0 * * * * cd /path/to/aurex-ai && python scripts/docker_cli.py fetch-news
   ```

2. **Set Up Monitoring**
   - Configure alerts for service failures
   - Set up dashboard for container metrics
   - Enable automatic restarts

3. **Integrate with CI/CD**
   - Add MCP commands to deployment pipeline
   - Automate health checks
   - Enable rolling updates

---

## 📚 Additional Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Model Context Protocol Spec](https://modelcontextprotocol.io/)
- [AUREX.AI Architecture](./architecture.md)
- [API Integration Guide](./API_INTEGRATION_GUIDE.md)

---

**Last Updated:** October 27, 2025  
**Version:** 1.0.0

