#!/usr/bin/env python
"""
AUREX.AI - Docker CLI Manager

Command-line interface for managing AUREX.AI Docker containers.
Uses the MCP Docker Manager for operations.
"""

import argparse
import asyncio
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.mcp_docker_manager import MCPDockerManager


class DockerCLI:
    """CLI interface for Docker operations."""
    
    def __init__(self):
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.compose_file = os.path.join(self.project_root, "docker-compose.yml")
        self.manager = MCPDockerManager(self.project_root, self.compose_file)
    
    async def status(self, args):
        """Show status of all containers."""
        print("AUREX.AI Container Status")
        print("=" * 70)
        
        health = await self.manager.health_check()
        
        for service, status in health.items():
            state_symbol = "[+]" if status.get("running") else "[-]"
            print(f"\n{state_symbol} {service.upper()}")
            print(f"    State: {status.get('state', 'unknown')}")
            if "database_ready" in status:
                db_symbol = "[+]" if status["database_ready"] else "[-]"
                print(f"    Database: {db_symbol}")
            if "cache_ready" in status:
                cache_symbol = "[+]" if status["cache_ready"] else "[-]"
                print(f"    Cache: {cache_symbol}")
            if "api_ready" in status:
                api_symbol = "[+]" if status["api_ready"] else "[-]"
                print(f"    API: {api_symbol}")
        
        print("\n" + "=" * 70)
    
    async def logs(self, args):
        """Show logs for a service."""
        result = await self.manager.container_logs(args.service, args.tail)
        print(f"Logs for {args.service} (last {args.tail} lines)")
        print("=" * 70)
        print(result["logs"])
    
    async def restart(self, args):
        """Restart a service."""
        print(f"[*] Restarting {args.service}...")
        result = await self.manager.restart_service(args.service)
        
        if result["success"]:
            print(f"[+] {args.service} restarted successfully")
        else:
            print(f"[-] Failed to restart {args.service}")
            print(result["message"])
    
    async def exec(self, args):
        """Execute a command in a container."""
        print(f"[*] Executing in {args.service}: {' '.join(args.command)}")
        result = await self.manager.exec_command(args.service, args.command)
        
        print(result["stdout"])
        if result["stderr"]:
            print(f"Error: {result['stderr']}", file=sys.stderr)
        
        sys.exit(result["exit_code"])
    
    async def fetch_news(self, args):
        """Fetch gold news."""
        print("[*] Fetching gold news from NewsAPI...")
        result = await self.manager.fetch_news()
        
        if result["success"]:
            print("[+] News fetching completed")
            print(result["output"])
        else:
            print("[-] News fetching failed")
            print(result["error"], file=sys.stderr)
    
    async def fetch_prices(self, args):
        """Fetch real-time prices."""
        print("[*] Fetching real-time gold prices...")
        result = await self.manager.fetch_prices()
        
        if result["success"]:
            print("[+] Price fetching completed")
            print(result["output"])
        else:
            print("[-] Price fetching failed")
            print(result["error"], file=sys.stderr)
    
    async def run_pipeline(self, args):
        """Run the data pipeline."""
        mode = "continuous" if args.continuous else "once"
        print(f"[*] Running pipeline in {mode} mode...")
        
        result = await self.manager.run_pipeline(mode)
        
        if result["success"]:
            print("[+] Pipeline completed")
            print(result["output"])
        else:
            print("[-] Pipeline failed")
            print(result["error"], file=sys.stderr)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AUREX.AI Docker Management CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Status command
    subparsers.add_parser("status", help="Show container status")
    
    # Logs command
    logs_parser = subparsers.add_parser("logs", help="Show container logs")
    logs_parser.add_argument("service", help="Service name")
    logs_parser.add_argument("--tail", type=int, default=50, help="Number of lines to show")
    
    # Restart command
    restart_parser = subparsers.add_parser("restart", help="Restart a service")
    restart_parser.add_argument("service", help="Service name")
    
    # Exec command
    exec_parser = subparsers.add_parser("exec", help="Execute command in container")
    exec_parser.add_argument("service", help="Service name")
    exec_parser.add_argument("command", nargs="+", help="Command to execute")
    
    # Fetch news command
    subparsers.add_parser("fetch-news", help="Fetch gold news from NewsAPI")
    
    # Fetch prices command
    subparsers.add_parser("fetch-prices", help="Fetch real-time gold prices")
    
    # Run pipeline command
    pipeline_parser = subparsers.add_parser("pipeline", help="Run data pipeline")
    pipeline_parser.add_argument("--continuous", action="store_true", help="Run in continuous mode")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    cli = DockerCLI()
    
    # Map commands to methods
    commands = {
        "status": cli.status,
        "logs": cli.logs,
        "restart": cli.restart,
        "exec": cli.exec,
        "fetch-news": cli.fetch_news,
        "fetch-prices": cli.fetch_prices,
        "pipeline": cli.run_pipeline,
    }
    
    asyncio.run(commands[args.command](args))


if __name__ == "__main__":
    main()

