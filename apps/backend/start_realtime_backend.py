"""
AUREX.AI - Start Backend with Real-Time Price Streaming

Starts the FastAPI backend and real-time price streamer as background tasks.
"""

import asyncio
import os
import sys
import threading

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from loguru import logger
import uvicorn

from apps.backend.realtime_price_streamer import RealtimePriceStreamer
from apps.backend.websocket_manager import ws_manager


async def start_price_streaming():
    """Start the real-time price streaming service."""
    logger.info("🚀 Starting real-time price streaming service...")
    
    try:
        # Create streamer with 5-second updates (more real-time)
        streamer = RealtimePriceStreamer(update_interval=5.0)
        
        # Start streaming with WebSocket broadcast
        await streamer.stream_prices(broadcast_callback=ws_manager.broadcast_price)
    except Exception as e:
        logger.error(f"Price streaming error: {e}")


def run_price_streamer_thread():
    """Run price streamer in a separate thread with its own event loop."""
    logger.info("🔄 Starting price streamer thread...")
    
    # Create new event loop for this thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        # Run the price streaming coroutine
        loop.run_until_complete(start_price_streaming())
    except KeyboardInterrupt:
        logger.info("Price streamer interrupted")
    finally:
        loop.close()


def run_backend():
    """Run the FastAPI backend server with background price streaming."""
    logger.info("=" * 70)
    logger.info("🚀 AUREX.AI Real-Time Backend")
    logger.info("=" * 70)
    
    # Start price streaming in a background thread
    streamer_thread = threading.Thread(target=run_price_streamer_thread, daemon=True)
    streamer_thread.start()
    
    logger.info("🌐 Starting FastAPI backend server...")
    logger.info("📡 WebSocket endpoint: ws://localhost:8000/api/v1/ws/stream")
    logger.info("📊 API docs: http://localhost:8000/docs")
    logger.info("=" * 70)
    
    # Run Uvicorn server (blocking)
    uvicorn.run(
        "apps.backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # Disable reload to prevent thread issues
        log_level="info"
    )


if __name__ == "__main__":
    try:
        run_backend()
    except KeyboardInterrupt:
        logger.info("\n👋 Shutting down gracefully...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

