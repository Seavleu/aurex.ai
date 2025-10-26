"""
AUREX.AI - Pipeline Worker Entry Point.

This is the main entry point for the Prefect pipeline worker.
"""

import asyncio
import sys

from loguru import logger

from apps.pipeline.flows.gold_sentiment_flow import (
    continuous_monitoring,
    gold_sentiment_pipeline,
)
from packages.shared.config import config
from packages.shared.logging_config import setup_logging


async def run_once() -> None:
    """Run the pipeline once."""
    logger.info("🚀 Running pipeline once...")
    await gold_sentiment_pipeline(hours_back=24)


async def run_continuous() -> None:
    """Run the pipeline continuously."""
    logger.info("🔄 Starting continuous monitoring...")
    await continuous_monitoring()


async def main() -> None:
    """Main entry point."""
    setup_logging("pipeline-worker", log_level=config.LOG_LEVEL)

    logger.info("=" * 80)
    logger.info("AUREX.AI - Pipeline Worker")
    logger.info("=" * 80)
    logger.info(f"Environment: {config.ENVIRONMENT}")
    logger.info(f"Mode: {'Continuous' if '--continuous' in sys.argv else 'Once'}")
    logger.info("=" * 80)

    if "--continuous" in sys.argv or "-c" in sys.argv:
        await run_continuous()
    else:
        await run_once()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n⏹️  Pipeline stopped by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)
