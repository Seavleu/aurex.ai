"""
AUREX.AI - MCP Docker Manager

Model Context Protocol server for managing AUREX.AI Docker containers.
Provides tools for container lifecycle management, health checks, and operations.
"""

import asyncio
import json
import os
import subprocess
import sys
from typing import Any, Dict, List, Optional

# MCP Protocol Implementation
class MCPDockerManager:
    """MCP server for Docker container management."""
    
    def __init__(self, project_root: str, compose_file: str):
        self.project_root = project_root
        self.compose_file = compose_file
        self.services = [
            "postgres",
            "redis", 
            "backend",
            "pipeline",
            "prefect"
        ]
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP requests."""
        method = request.get("method")
        params = request.get("params", {})
        
        handlers = {
            "list_containers": self.list_containers,
            "container_status": self.container_status,
            "container_logs": self.container_logs,
            "start_service": self.start_service,
            "stop_service": self.stop_service,
            "restart_service": self.restart_service,
            "exec_command": self.exec_command,
            "health_check": self.health_check,
            "fetch_news": self.fetch_news,
            "fetch_prices": self.fetch_prices,
            "run_pipeline": self.run_pipeline,
        }
        
        handler = handlers.get(method)
        if not handler:
            return {
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }
        
        try:
            result = await handler(**params)
            return {"result": result}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }
    
    async def list_containers(self) -> List[Dict[str, Any]]:
        """List all AUREX.AI containers."""
        result = subprocess.run(
            ["docker-compose", "-f", self.compose_file, "ps", "--format", "json"],
            capture_output=True,
            text=True,
            cwd=self.project_root
        )
        
        if result.returncode != 0:
            raise Exception(f"Failed to list containers: {result.stderr}")
        
        containers = []
        for line in result.stdout.strip().split('\n'):
            if line:
                try:
                    containers.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
        
        return containers
    
    async def container_status(self, service: str) -> Dict[str, Any]:
        """Get status of a specific service."""
        result = subprocess.run(
            ["docker-compose", "-f", self.compose_file, "ps", service],
            capture_output=True,
            text=True,
            cwd=self.project_root
        )
        
        return {
            "service": service,
            "running": result.returncode == 0,
            "output": result.stdout
        }
    
    async def container_logs(self, service: str, tail: int = 50) -> Dict[str, str]:
        """Get logs from a container."""
        result = subprocess.run(
            ["docker-compose", "-f", self.compose_file, "logs", "--tail", str(tail), service],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            cwd=self.project_root
        )
        
        return {
            "service": service,
            "logs": result.stdout
        }
    
    async def start_service(self, service: str) -> Dict[str, Any]:
        """Start a service."""
        result = subprocess.run(
            ["docker-compose", "-f", self.compose_file, "start", service],
            capture_output=True,
            text=True,
            cwd=self.project_root
        )
        
        return {
            "service": service,
            "success": result.returncode == 0,
            "message": result.stdout or result.stderr
        }
    
    async def stop_service(self, service: str) -> Dict[str, Any]:
        """Stop a service."""
        result = subprocess.run(
            ["docker-compose", "-f", self.compose_file, "stop", service],
            capture_output=True,
            text=True,
            cwd=self.project_root
        )
        
        return {
            "service": service,
            "success": result.returncode == 0,
            "message": result.stdout or result.stderr
        }
    
    async def restart_service(self, service: str) -> Dict[str, Any]:
        """Restart a service."""
        result = subprocess.run(
            ["docker-compose", "-f", self.compose_file, "restart", service],
            capture_output=True,
            text=True,
            cwd=self.project_root
        )
        
        return {
            "service": service,
            "success": result.returncode == 0,
            "message": result.stdout or result.stderr
        }
    
    async def exec_command(self, service: str, command: List[str]) -> Dict[str, Any]:
        """Execute a command in a container."""
        result = subprocess.run(
            ["docker-compose", "-f", self.compose_file, "exec", "-T", service] + command,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            cwd=self.project_root
        )
        
        return {
            "service": service,
            "command": " ".join(command),
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Check health of all services."""
        containers = await self.list_containers()
        
        health_status = {}
        for container in containers:
            service_name = container.get("Service", "unknown")
            state = container.get("State", "unknown")
            health = container.get("Health", "N/A")
            
            health_status[service_name] = {
                "state": state,
                "health": health,
                "running": state == "running"
            }
        
        # Check database connectivity
        db_check = await self.exec_command(
            "postgres",
            ["pg_isready", "-U", "aurex", "-d", "aurex_db"]
        )
        health_status["postgres"]["database_ready"] = db_check["exit_code"] == 0
        
        # Check Redis connectivity
        redis_check = await self.exec_command(
            "redis",
            ["redis-cli", "ping"]
        )
        health_status["redis"]["cache_ready"] = "PONG" in redis_check["stdout"]
        
        # Check backend API
        api_check = await self.exec_command(
            "backend",
            ["curl", "-f", "http://localhost:8000/health"]
        )
        health_status["backend"]["api_ready"] = api_check["exit_code"] == 0
        
        return health_status
    
    async def fetch_news(self) -> Dict[str, Any]:
        """Fetch gold news using NewsAPI."""
        result = await self.exec_command(
            "backend",
            ["python", "backend/fetch_gold_news.py"]
        )
        
        return {
            "success": result["exit_code"] == 0,
            "output": result["stdout"],
            "error": result["stderr"]
        }
    
    async def fetch_prices(self) -> Dict[str, Any]:
        """Fetch real-time gold prices."""
        result = await self.exec_command(
            "backend",
            ["python", "backend/fetch_realtime.py"]
        )
        
        return {
            "success": result["exit_code"] == 0,
            "output": result["stdout"],
            "error": result["stderr"]
        }
    
    async def run_pipeline(self, mode: str = "once") -> Dict[str, Any]:
        """Run the data pipeline."""
        cmd = ["python", "pipeline/main.py"]
        if mode == "continuous":
            cmd.append("--continuous")
        
        result = await self.exec_command("pipeline", cmd)
        
        return {
            "mode": mode,
            "success": result["exit_code"] == 0,
            "output": result["stdout"],
            "error": result["stderr"]
        }


async def main():
    """Main MCP server loop."""
    project_root = os.getenv("PROJECT_ROOT", os.getcwd())
    compose_file = os.getenv("COMPOSE_FILE", "docker-compose.yml")
    
    manager = MCPDockerManager(project_root, compose_file)
    
    print(json.dumps({
        "jsonrpc": "2.0",
        "method": "server.info",
        "params": {
            "name": "aurex-docker-manager",
            "version": "1.0.0",
            "capabilities": {
                "tools": [
                    "list_containers",
                    "container_status",
                    "container_logs",
                    "start_service",
                    "stop_service",
                    "restart_service",
                    "exec_command",
                    "health_check",
                    "fetch_news",
                    "fetch_prices",
                    "run_pipeline"
                ]
            }
        }
    }), flush=True)
    
    # Read requests from stdin
    try:
        for line in sys.stdin:
            if not line.strip():
                continue
            
            try:
                request = json.loads(line)
                response = await manager.handle_request(request)
                print(json.dumps(response), flush=True)
            except json.JSONDecodeError as e:
                error_response = {
                    "error": {
                        "code": -32700,
                        "message": f"Parse error: {str(e)}"
                    }
                }
                print(json.dumps(error_response), flush=True)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    asyncio.run(main())

