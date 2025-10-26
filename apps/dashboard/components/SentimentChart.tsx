/**
 * AUREX.AI - Sentiment Chart Component
 */

'use client';

import { useState } from 'react';
import { useSentimentHistory } from '@/lib/hooks';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  ReferenceLine,
} from 'recharts';

type TimeRange = '24h' | '7d' | '30d';

const TIME_RANGES: { label: string; value: TimeRange; hours: number }[] = [
  { label: '24 Hours', value: '24h', hours: 24 },
  { label: '7 Days', value: '7d', hours: 168 },
  { label: '30 Days', value: '30d', hours: 720 },
];

export default function SentimentChart() {
  const [timeRange, setTimeRange] = useState<TimeRange>('7d');
  const hours = TIME_RANGES.find((r) => r.value === timeRange)?.hours || 168;
  
  const { data: sentimentHistory, loading, error } = useSentimentHistory(hours, 1);

  // Prepare chart data
  const chartData = sentimentHistory
    ?.map((summary) => ({
      timestamp: new Date(summary.timestamp).getTime(),
      date: new Date(summary.timestamp).toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
      }),
      sentiment: summary.aggregate_score,
      positive: summary.percentages.positive,
      neutral: summary.percentages.neutral,
      negative: summary.percentages.negative,
      articles: summary.total_articles,
    }))
    .reverse(); // Reverse to show oldest first

  // Calculate stats
  const currentSentiment = chartData?.[chartData.length - 1]?.sentiment || 0;
  const avgSentiment = chartData?.length
    ? chartData.reduce((sum, d) => sum + d.sentiment, 0) / chartData.length
    : 0;
  
  // Determine sentiment status
  const getSentimentLabel = (score: number) => {
    if (score > 0.3) return { label: 'Bullish', color: 'text-green-600' };
    if (score < -0.3) return { label: 'Bearish', color: 'text-red-600' };
    return { label: 'Neutral', color: 'text-gray-600' };
  };

  const currentStatus = getSentimentLabel(currentSentiment);

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
          Sentiment Trend
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
            Sentiment Trend
          </h2>
          <div className="flex items-center gap-3 mt-1">
            <span className="text-2xl font-bold text-gray-900 dark:text-white tabular-nums">
              {currentSentiment.toFixed(2)}
            </span>
            <span className={`text-sm font-semibold px-2.5 py-1 rounded ${currentStatus.color === 'text-green-600' ? 'bg-green-100 dark:bg-green-900/30' : currentStatus.color === 'text-red-600' ? 'bg-red-100 dark:bg-red-900/30' : 'bg-gray-100 dark:bg-gray-700'} ${currentStatus.color} dark:${currentStatus.color.replace('text-', 'text-').replace('-600', '-400')}`}>
              {currentStatus.label}
            </span>
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
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id="sentimentGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#10b981" stopOpacity={0.8} />
                <stop offset="50%" stopColor="#6b7280" stopOpacity={0.4} />
                <stop offset="100%" stopColor="#ef4444" stopOpacity={0.8} />
              </linearGradient>
            </defs>
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
              domain={[-1, 1]}
              ticks={[-1, -0.5, 0, 0.5, 1]}
              tickFormatter={(value) => value.toFixed(1)}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1f2937',
                border: 'none',
                borderRadius: '8px',
                color: '#fff',
              }}
              formatter={(value: number, name: string) => {
                if (name === 'sentiment') return [value.toFixed(2), 'Sentiment Score'];
                if (name === 'articles') return [value, 'Articles'];
                return [value, name];
              }}
              labelFormatter={(label) => `Time: ${label}`}
            />
            <Legend />
            <ReferenceLine y={0} stroke="#6b7280" strokeDasharray="3 3" />
            <ReferenceLine y={0.3} stroke="#10b981" strokeDasharray="3 3" label="Bullish" />
            <ReferenceLine y={-0.3} stroke="#ef4444" strokeDasharray="3 3" label="Bearish" />
            <Area
              type="monotone"
              dataKey="sentiment"
              stroke="#3b82f6"
              strokeWidth={3}
              fill="url(#sentimentGradient)"
              name="Sentiment Score"
              animationDuration={1000}
            />
          </AreaChart>
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
                d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
              />
            </svg>
            <p className="text-lg">No sentiment data available</p>
            <p className="text-sm text-gray-400 mt-2">
              Run the pipeline to analyze news sentiment
            </p>
          </div>
        </div>
      )}

      {/* Stats Footer */}
      {chartData && chartData.length > 1 && (
        <div className="grid grid-cols-4 gap-4 mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
          <div>
            <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Average</div>
            <div className="text-lg font-bold text-gray-900 dark:text-white">
              {avgSentiment.toFixed(2)}
            </div>
          </div>
          <div>
            <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Most Bullish</div>
            <div className="text-lg font-bold text-green-600">
              {Math.max(...chartData.map((d) => d.sentiment)).toFixed(2)}
            </div>
          </div>
          <div>
            <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Most Bearish</div>
            <div className="text-lg font-bold text-red-600">
              {Math.min(...chartData.map((d) => d.sentiment)).toFixed(2)}
            </div>
          </div>
          <div>
            <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Total Articles</div>
            <div className="text-lg font-bold text-gray-900 dark:text-white">
              {chartData.reduce((sum, d) => sum + d.articles, 0)}
            </div>
          </div>
        </div>
      )}

      {/* Sentiment Distribution */}
      {chartData && chartData.length > 0 && (
        <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Recent Distribution
          </h3>
          <div className="grid grid-cols-3 gap-4">
            <div className="bg-green-50 dark:bg-green-900/20 rounded-lg p-4">
              <div className="text-sm text-green-600 dark:text-green-400 mb-1">Positive</div>
              <div className="text-2xl font-bold text-green-700 dark:text-green-300">
                {chartData[chartData.length - 1]?.positive.toFixed(1)}%
              </div>
            </div>
            <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
              <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Neutral</div>
              <div className="text-2xl font-bold text-gray-700 dark:text-gray-300">
                {chartData[chartData.length - 1]?.neutral.toFixed(1)}%
              </div>
            </div>
            <div className="bg-red-50 dark:bg-red-900/20 rounded-lg p-4">
              <div className="text-sm text-red-600 dark:text-red-400 mb-1">Negative</div>
              <div className="text-2xl font-bold text-red-700 dark:text-red-300">
                {chartData[chartData.length - 1]?.negative.toFixed(1)}%
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

