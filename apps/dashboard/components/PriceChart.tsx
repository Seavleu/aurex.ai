/**
 * AUREX.AI - Price Chart Component
 */

'use client';

import { useState } from 'react';
import { usePriceHistory } from '@/lib/hooks';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';

type TimeRange = '24h' | '7d' | '30d';

const TIME_RANGES: { label: string; value: TimeRange; hours: number }[] = [
  { label: '24 Hours', value: '24h', hours: 24 },
  { label: '7 Days', value: '7d', hours: 168 },
  { label: '30 Days', value: '30d', hours: 720 },
];

export default function PriceChart() {
  const [timeRange, setTimeRange] = useState<TimeRange>('24h');
  const hours = TIME_RANGES.find((r) => r.value === timeRange)?.hours || 24;
  
  const { data: priceHistory, loading, error } = usePriceHistory(hours);

  // Prepare chart data
  const chartData = priceHistory
    ?.map((price) => ({
      timestamp: new Date(price.timestamp).getTime(),
      date: new Date(price.timestamp).toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      }),
      price: price.close,
      high: price.high,
      low: price.low,
    }))
    .reverse(); // Reverse to show oldest first

  // Calculate stats
  const currentPrice = chartData?.[chartData.length - 1]?.price || 0;
  const firstPrice = chartData?.[0]?.price || 0;
  const priceChange = currentPrice - firstPrice;
  const priceChangePct = firstPrice ? (priceChange / firstPrice) * 100 : 0;
  const isPositive = priceChangePct >= 0;

  if (loading && !chartData) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700 h-full">
        <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-32 mb-4 animate-pulse"></div>
        <div className="h-96 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700 h-full">
        <h2 className="text-lg font-bold mb-4 text-gray-900 dark:text-white">
          Price History
        </h2>
        <p className="text-red-500 text-sm">{error.message}</p>
      </div>
    );
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700 h-full">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-lg font-bold text-gray-900 dark:text-white">
            Price History
          </h2>
          <div className="flex items-center gap-3 mt-1">
            <span className="text-2xl font-bold text-gray-900 dark:text-white tabular-nums">
              ${currentPrice.toFixed(2)}
            </span>
            {chartData && chartData.length > 1 && (
              <span
                className={`text-sm font-semibold ${
                  isPositive ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'
                }`}
              >
                {priceChangePct > 0 ? '+' : ''}
                {priceChangePct.toFixed(2)}%
              </span>
            )}
          </div>
        </div>

        {/* Time Range Selector */}
        <div className="flex gap-2">
          {TIME_RANGES.map((range) => (
            <button
              key={range.value}
              onClick={() => setTimeRange(range.value)}
              className={`px-3 py-1.5 rounded-lg font-medium transition-all text-xs ${
                timeRange === range.value
                  ? 'bg-amber-500 text-white'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
              }`}
            >
              {range.label}
            </button>
          ))}
        </div>
      </div>

      {/* Chart */}
      {chartData && chartData.length > 0 ? (
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis
              dataKey="date"
              stroke="#6b7280"
              style={{ fontSize: '12px' }}
              angle={-45}
              textAnchor="end"
              height={80}
            />
            <YAxis
              stroke="#6b7280"
              style={{ fontSize: '12px' }}
              domain={['auto', 'auto']}
              tickFormatter={(value) => `$${value.toFixed(0)}`}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1f2937',
                border: 'none',
                borderRadius: '8px',
                color: '#fff',
              }}
              formatter={(value: number) => [`$${value.toFixed(2)}`, 'Price']}
              labelFormatter={(label) => `Time: ${label}`}
            />
            <Legend />
            <Line
              type="monotone"
              dataKey="price"
              stroke="#f59e0b"
              strokeWidth={3}
              dot={false}
              name="Gold Price (USD)"
              animationDuration={1000}
            />
          </LineChart>
        </ResponsiveContainer>
      ) : (
        <div className="h-96 flex items-center justify-center text-gray-500">
          <div className="text-center">
            <svg
              className="w-16 h-16 mx-auto mb-4 text-gray-300"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"
              />
            </svg>
            <p className="text-lg">No price data available</p>
            <p className="text-sm text-gray-400 mt-2">
              Run the pipeline to fetch historical prices
            </p>
          </div>
        </div>
      )}

      {/* Stats Footer */}
      {chartData && chartData.length > 1 && (
        <div className="grid grid-cols-4 gap-3 mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
          <div>
            <div className="text-xs text-gray-600 dark:text-gray-400 mb-0.5">High</div>
            <div className="text-base font-semibold text-gray-900 dark:text-white tabular-nums">
              ${Math.max(...chartData.map((d) => d.high)).toFixed(2)}
            </div>
          </div>
          <div>
            <div className="text-xs text-gray-600 dark:text-gray-400 mb-0.5">Low</div>
            <div className="text-base font-semibold text-gray-900 dark:text-white tabular-nums">
              ${Math.min(...chartData.map((d) => d.low)).toFixed(2)}
            </div>
          </div>
          <div>
            <div className="text-xs text-gray-600 dark:text-gray-400 mb-0.5">Average</div>
            <div className="text-base font-semibold text-gray-900 dark:text-white tabular-nums">
              ${(chartData.reduce((sum, d) => sum + d.price, 0) / chartData.length).toFixed(2)}
            </div>
          </div>
          <div>
            <div className="text-xs text-gray-600 dark:text-gray-400 mb-0.5">Points</div>
            <div className="text-base font-semibold text-gray-900 dark:text-white tabular-nums">
              {chartData.length}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

