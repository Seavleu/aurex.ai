"""
AUREX.AI - Start Backend with Real-Time Price Streaming

Starts the FastAPI backend and real-time price streamer as background tasks.
"""

import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from loguru import logger
import uvicorn

from apps.backend.realtime_price_streamer import RealtimePriceStreamer
from apps.backend.websocket_manager import ws_manager


async def start_price_streaming():
    """Start the real-time price streaming service."""
    logger.info("Starting real-time price streaming service...")
    
    # Create streamer with 5-second updates (more real-time)
    streamer = RealtimePriceStreamer(update_interval=5.0)
    
    # Start streaming with WebSocket broadcast
    await streamer.stream_prices(broadcast_callback=ws_manager.broadcast_price)


def run_backend():
    """Run the FastAPI backend server."""
    logger.info("Starting FastAPI backend server...")
    
    # Start price streaming in background
    asyncio.create_task(start_price_streaming())
    
    # Run Uvicorn server
    uvicorn.run(
        "apps.backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    try:
        run_backend()
    except KeyboardInterrupt:
        logger.info("\n👋 Shutting down gracefully...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

