/**
 * AUREX.AI - Real-Time React Hooks
 * 
 * New hooks using WebSocket for real-time updates.
 * Replaces old polling-based hooks.
 */

import { useEffect, useState, useCallback } from 'react';
import { getWebSocketClient } from './websocket';
import { api, News, Alert } from './api';

export interface Price {
  symbol: string;
  close: number;
  open: number;
  high: number;
  low: number;
  change: number;
  change_pct: number;
  timestamp: string;
  volume?: number;
}

/**
 * Real-time price updates via WebSocket
 * NO MORE POLLING! Updates pushed from server in real-time.
 */
export function useRealtimePrice() {
  const [price, setPrice] = useState<Price | null>(null);
  const [connectionState, setConnectionState] = useState<string>('disconnected');
  const [updateCount, setUpdateCount] = useState(0);

  useEffect(() => {
    const client = getWebSocketClient();
    
    // Connect if not already connected
    if (client.getState() === 'disconnected') {
      client.connect();
    }

    // Subscribe to price updates
    const unsubscribe = client.onPriceUpdate((data) => {
      setPrice(data);
      setUpdateCount(prev => prev + 1);
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

  return { 
    price, 
    connectionState, 
    updateCount,
    isConnected: connectionState === 'connected'
  };
}

/**
 * Real-time alerts via WebSocket
 */
export function useRealtimeAlerts() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [newAlertCount, setNewAlertCount] = useState(0);

  useEffect(() => {
    const client = getWebSocketClient();
    
    if (client.getState() === 'disconnected') {
      client.connect();
    }

    // Subscribe to alert updates
    const unsubscribe = client.onAlert((alert) => {
      setAlerts(prev => [alert, ...prev]);
      setNewAlertCount(prev => prev + 1);
    });

    return () => unsubscribe();
  }, []);

  const clearNewAlerts = useCallback(() => {
    setNewAlertCount(0);
  }, []);

  return { alerts, newAlertCount, clearNewAlerts };
}

/**
 * Real-time news updates via WebSocket
 */
export function useRealtimeNews() {
  const [news, setNews] = useState<News[]>([]);
  const [newNewsCount, setNewNewsCount] = useState(0);

  useEffect(() => {
    const client = getWebSocketClient();
    
    if (client.getState() === 'disconnected') {
      client.connect();
    }

    // Subscribe to news updates
    const unsubscribe = client.onNews((newsItem) => {
      setNews(prev => [newsItem, ...prev].slice(0, 50)); // Keep last 50
      setNewNewsCount(prev => prev + 1);
    });

    return () => unsubscribe();
  }, []);

  const clearNewNews = useCallback(() => {
    setNewNewsCount(0);
  }, []);

  return { news, newNewsCount, clearNewNews };
}

/**
 * Hybrid approach: Use real-time WebSocket with HTTP fallback
 * For historical data that doesn't change
 */
export function usePriceHistory(hours: number = 24) {
  const [data, setData] = useState<any[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await api.price.history({ hours, page_size: 500 });
        if (response.data) {
          setData(response.data);
        }
        setError(null);
      } catch (err) {
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [hours]);

  return { data, loading, error };
}

/**
 * Connection status hook
 */
export function useWebSocketConnection() {
  const [state, setState] = useState<string>('disconnected');
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    const client = getWebSocketClient();
    
    const interval = setInterval(() => {
      setState(client.getState());
    }, 1000);

    // Request stats periodically
    const statsInterval = setInterval(() => {
      if (client.getState() === 'connected') {
        client.requestStats();
      }
    }, 10000);

    return () => {
      clearInterval(interval);
      clearInterval(statsInterval);
    };
  }, []);

  return { 
    state, 
    isConnected: state === 'connected',
    stats
  };
}

