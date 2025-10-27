"""
AUREX.AI - WebSocket API Endpoints
"""

from datetime import datetime
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from loguru import logger

try:
    from backend.websocket_manager import ws_manager
except ModuleNotFoundError:
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    from apps.backend.websocket_manager import ws_manager

router = APIRouter()


@router.websocket("/stream")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time price updates.
    
    Client receives:
    - Immediate last known price on connection
    - Real-time price updates as they occur
    - Alerts and news updates
    
    Message format:
    {
        "type": "price_update" | "alert" | "news",
        "data": {...},
        "timestamp": "2025-10-27T12:00:00Z",
        "update_count": 123
    }
    """
    await ws_manager.connect(websocket)
    
    try:
        while True:
            # Keep connection alive and receive any client messages
            data = await websocket.receive_text()
            
            # Handle client messages (e.g., ping, subscription changes)
            if data == "ping":
                await websocket.send_text("pong")
            elif data == "stats":
                stats = ws_manager.get_stats()
                await websocket.send_json({
                    "type": "stats",
                    "data": stats,
                    "timestamp": str(datetime.now())
                })
    
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
        logger.info("WebSocket client disconnected normally")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        ws_manager.disconnect(websocket)


@router.get("/stats")
async def get_websocket_stats():
    """Get WebSocket connection statistics."""
    return {
        "status": "success",
        "data": ws_manager.get_stats()
    }

