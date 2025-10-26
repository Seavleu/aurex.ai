"""
AUREX.AI - Pipeline Main Entry Point.

This module serves as the entry point for the Prefect pipeline worker.
It will be fully implemented in Sprint 1.
"""

import asyncio


async def main() -> None:
    """Main entry point for pipeline worker."""
    print("AUREX.AI Pipeline Worker Starting...")
    print("Pipeline implementation coming in Sprint 1")
    print("Worker ready and waiting for flows...")

    # Keep the worker alive
    while True:
        await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())

