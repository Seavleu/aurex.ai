"""
AUREX.AI - WebSocket Manager for Real-Time Price Updates

Provides real-time gold price streaming to connected clients.
"""

import asyncio
import json
from datetime import datetime
from typing import Set
from fastapi import WebSocket
from loguru import logger


class ConnectionManager:
    """Manages WebSocket connections and broadcasts price updates."""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.last_price = None
        self.update_count = 0
    
    async def connect(self, websocket: WebSocket):
        """Accept a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"New WebSocket connection. Total: {len(self.active_connections)}")
        
        # Send last known price immediately
        if self.last_price:
            await self.send_personal_message(
                json.dumps({
                    "type": "price_update",
                    "data": self.last_price,
                    "timestamp": datetime.now().isoformat()
                }),
                websocket
            )
    
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        self.active_connections.discard(websocket)
        logger.info(f"WebSocket disconnected. Total: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send message to a specific client."""
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            self.disconnect(websocket)
    
    async def broadcast_price(self, price_data: dict):
        """Broadcast price update to all connected clients."""
        if not self.active_connections:
            return
        
        self.last_price = price_data
        self.update_count += 1
        
        message = json.dumps({
            "type": "price_update",
            "data": price_data,
            "timestamp": datetime.now().isoformat(),
            "update_count": self.update_count
        })
        
        # Broadcast to all connections
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected.add(connection)
        
        # Clean up disconnected clients
        for conn in disconnected:
            self.disconnect(conn)
        
        if len(self.active_connections) > 0:
            logger.debug(f"Broadcasted price update to {len(self.active_connections)} clients")
    
    async def broadcast_alert(self, alert_data: dict):
        """Broadcast alert to all connected clients."""
        message = json.dumps({
            "type": "alert",
            "data": alert_data,
            "timestamp": datetime.now().isoformat()
        })
        
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting alert: {e}")
                disconnected.add(connection)
        
        for conn in disconnected:
            self.disconnect(conn)
    
    async def broadcast_news(self, news_data: dict):
        """Broadcast new news article to all connected clients."""
        message = json.dumps({
            "type": "news",
            "data": news_data,
            "timestamp": datetime.now().isoformat()
        })
        
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting news: {e}")
                disconnected.add(connection)
        
        for conn in disconnected:
            self.disconnect(conn)
    
    def get_stats(self) -> dict:
        """Get connection statistics."""
        return {
            "active_connections": len(self.active_connections),
            "last_price": self.last_price,
            "update_count": self.update_count
        }


# Global connection manager instance
ws_manager = ConnectionManager()

