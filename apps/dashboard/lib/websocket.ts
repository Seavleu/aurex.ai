/**
 * AUREX.AI - WebSocket Client for Real-Time Data
 * 
 * Provides real-time price updates, alerts, and news via WebSocket connection.
 */

type MessageType = 'price_update' | 'alert' | 'news' | 'stats';

interface WebSocketMessage {
  type: MessageType;
  data: any;
  timestamp: string;
  update_count?: number;
}

type MessageHandler = (data: any) => void;

class AurexWebSocketClient {
  private ws: WebSocket | null = null;
  private reconnectInterval: number = 5000;
  private reconnectTimer: NodeJS.Timeout | null = null;
  private handlers: Map<MessageType, Set<MessageHandler>> = new Map();
  private url: string;
  private isConnecting: boolean = false;
  private shouldReconnect: boolean = true;
  private connectionAttempts: number = 0;
  private maxReconnectAttempts: number = 10;

  constructor(baseUrl: string = 'ws://localhost:8000') {
    this.url = `${baseUrl}/api/v1/ws/stream`;
    
    // Initialize handler sets
    this.handlers.set('price_update', new Set());
    this.handlers.set('alert', new Set());
    this.handlers.set('news', new Set());
    this.handlers.set('stats', new Set());
  }

  /**
   * Connect to WebSocket server
   */
  connect(): void {
    if (this.ws?.readyState === WebSocket.OPEN || this.isConnecting) {
      return;
    }

    this.isConnecting = true;
    this.connectionAttempts++;

    try {
      this.ws = new WebSocket(this.url);

      this.ws.onopen = () => {
        console.log('[WebSocket] Connected to AUREX.AI');
        this.isConnecting = false;
        this.connectionAttempts = 0;
        
        // Send ping to confirm connection
        this.send('ping');
      };

      this.ws.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data);
          this.handleMessage(message);
        } catch (error) {
          console.error('[WebSocket] Error parsing message:', error);
        }
      };

      this.ws.onerror = (error) => {
        console.error('[WebSocket] Error:', error);
        this.isConnecting = false;
      };

      this.ws.onclose = (event) => {
        console.log('[WebSocket] Disconnected:', event.code, event.reason);
        this.isConnecting = false;
        this.ws = null;

        if (this.shouldReconnect && this.connectionAttempts < this.maxReconnectAttempts) {
          console.log(`[WebSocket] Reconnecting in ${this.reconnectInterval / 1000}s... (attempt ${this.connectionAttempts})`);
          this.reconnectTimer = setTimeout(() => {
            this.connect();
          }, this.reconnectInterval);
        } else if (this.connectionAttempts >= this.maxReconnectAttempts) {
          console.error('[WebSocket] Max reconnection attempts reached');
        }
      };
    } catch (error) {
      console.error('[WebSocket] Connection error:', error);
      this.isConnecting = false;
    }
  }

  /**
   * Disconnect from WebSocket server
   */
  disconnect(): void {
    this.shouldReconnect = false;
    
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }

    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  /**
   * Send message to server
   */
  private send(message: string): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(message);
    }
  }

  /**
   * Handle incoming message
   */
  private handleMessage(message: WebSocketMessage): void {
    const handlers = this.handlers.get(message.type);
    
    if (handlers) {
      handlers.forEach(handler => {
        try {
          handler(message.data);
        } catch (error) {
          console.error(`[WebSocket] Error in ${message.type} handler:`, error);
        }
      });
    }
  }

  /**
   * Subscribe to price updates
   */
  onPriceUpdate(handler: MessageHandler): () => void {
    this.handlers.get('price_update')?.add(handler);
    return () => this.handlers.get('price_update')?.delete(handler);
  }

  /**
   * Subscribe to alerts
   */
  onAlert(handler: MessageHandler): () => void {
    this.handlers.get('alert')?.add(handler);
    return () => this.handlers.get('alert')?.delete(handler);
  }

  /**
   * Subscribe to news updates
   */
  onNews(handler: MessageHandler): () => void {
    this.handlers.get('news')?.add(handler);
    return () => this.handlers.get('news')?.delete(handler);
  }

  /**
   * Get connection state
   */
  getState(): string {
    if (!this.ws) return 'disconnected';
    
    switch (this.ws.readyState) {
      case WebSocket.CONNECTING:
        return 'connecting';
      case WebSocket.OPEN:
        return 'connected';
      case WebSocket.CLOSING:
        return 'closing';
      case WebSocket.CLOSED:
        return 'disconnected';
      default:
        return 'unknown';
    }
  }

  /**
   * Request stats
   */
  requestStats(): void {
    this.send('stats');
  }
}

// Global WebSocket client instance
let wsClient: AurexWebSocketClient | null = null;

/**
 * Get or create WebSocket client instance
 */
export function getWebSocketClient(): AurexWebSocketClient {
  if (!wsClient) {
    const baseUrl = process.env.NEXT_PUBLIC_API_URL?.replace('http', 'ws') || 'ws://localhost:8000';
    wsClient = new AurexWebSocketClient(baseUrl);
  }
  return wsClient;
}

/**
 * Custom hook for real-time price updates
 */
export function useRealtimePrice() {
  const [price, setPrice] = React.useState<any>(null);
  const [connectionState, setConnectionState] = React.useState<string>('disconnected');

  React.useEffect(() => {
    const client = getWebSocketClient();
    
    // Connect if not already connected
    if (client.getState() === 'disconnected') {
      client.connect();
    }

    // Subscribe to price updates
    const unsubscribe = client.onPriceUpdate((data) => {
      setPrice(data);
    });

    // Monitor connection state
    const stateInterval = setInterval(() => {
      setConnectionState(client.getState());
    }, 1000);

    return () => {
      unsubscribe();
      clearInterval(stateInterval);
    };
  }, []);

  return { price, connectionState };
}

// Export for use in components
export { AurexWebSocketClient };

// Import React at the top (needed for hooks)
import React from 'react';

