/**
 * AUREX.AI - Sentiment Gauge Component
 */

'use client';

import { useSentimentSummary } from '@/lib/hooks';

export default function SentimentGauge() {
  const { data: sentiment, loading, error } = useSentimentSummary(24, true, 60000);

  if (loading && !sentiment) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700 h-full animate-pulse">
        <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-32 mb-4"></div>
        <div className="h-48 bg-gray-200 dark:bg-gray-700 rounded"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700 h-full">
        <h2 className="text-lg font-bold mb-4 text-gray-900 dark:text-white">Sentiment</h2>
        <p className="text-red-500 text-sm">{error.message}</p>
      </div>
    );
  }

  if (!sentiment) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700 h-full">
        <h2 className="text-lg font-bold mb-4 text-gray-900 dark:text-white">Sentiment</h2>
        <p className="text-gray-500 text-sm">No sentiment data available</p>
      </div>
    );
  }

  const score = sentiment.aggregate_score;
  const confidence = sentiment.confidence * 100;

  // Determine sentiment label and color
  let sentimentLabel = 'Neutral';
  let sentimentColor = 'text-gray-600';
  let bgColor = 'bg-gray-200';

  if (score > 0.2) {
    sentimentLabel = 'Positive';
    sentimentColor = 'text-green-600';
    bgColor = 'bg-green-200';
  } else if (score < -0.2) {
    sentimentLabel = 'Negative';
    sentimentColor = 'text-red-600';
    bgColor = 'bg-red-200';
  }

  // Calculate gauge rotation (-90deg to +90deg)
  const rotation = score * 90;

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700 h-full">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-bold text-gray-900 dark:text-white">
          Sentiment
        </h2>
        <span className="text-xs bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 px-2 py-1 rounded-full">24h</span>
      </div>

      {/* Sentiment Gauge */}
      <div className="relative w-full aspect-square max-w-xs mx-auto mb-6">
        <svg viewBox="0 0 200 120" className="w-full">
          {/* Background arc */}
          <path
            d="M 20 100 A 80 80 0 0 1 180 100"
            fill="none"
            className="stroke-gray-200 dark:stroke-gray-600"
            strokeWidth="20"
            strokeLinecap="round"
          />
          {/* Negative zone (red) */}
          <path
            d="M 20 100 A 80 80 0 0 1 100 20"
            fill="none"
            className="stroke-red-300 dark:stroke-red-500"
            strokeWidth="20"
            strokeLinecap="round"
          />
          {/* Positive zone (green) */}
          <path
            d="M 100 20 A 80 80 0 0 1 180 100"
            fill="none"
            className="stroke-green-300 dark:stroke-green-500"
            strokeWidth="20"
            strokeLinecap="round"
          />
          {/* Needle */}
          <line
            x1="100"
            y1="100"
            x2="100"
            y2="30"
            className="stroke-gray-800 dark:stroke-white transition-transform duration-500"
            strokeWidth="3"
            strokeLinecap="round"
            transform={`rotate(${rotation} 100 100)`}
          />
          {/* Center dot */}
          <circle cx="100" cy="100" r="8" className="fill-gray-800 dark:fill-white" />
        </svg>

        {/* Score display */}
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 translate-y-4 text-center">
          <div className={`text-4xl font-bold ${sentimentColor}`}>
            {score.toFixed(2)}
          </div>
          <div className={`text-lg font-semibold ${sentimentColor}`}>
            {sentimentLabel}
          </div>
        </div>
      </div>

      {/* Confidence */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-gray-600 dark:text-gray-400">Confidence</span>
          <span className="text-sm font-semibold text-gray-900 dark:text-white">
            {confidence.toFixed(1)}%
          </span>
        </div>
        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
          <div
            className="bg-blue-500 h-3 rounded-full transition-all duration-500"
            style={{ width: `${confidence}%` }}
          ></div>
        </div>
      </div>

      {/* Distribution */}
      <div className="grid grid-cols-3 gap-3">
        <div className="text-center p-2.5 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-100 dark:border-green-800">
          <div className="text-xl font-bold text-green-600 dark:text-green-400 tabular-nums">
            {sentiment.positive_count}
          </div>
          <div className="text-xs text-gray-600 dark:text-gray-400 mt-0.5">Positive</div>
          <div className="text-xs text-gray-500 mt-0.5 tabular-nums">
            {sentiment.percentages.positive.toFixed(0)}%
          </div>
        </div>
        <div className="text-center p-2.5 bg-gray-50 dark:bg-gray-700/30 rounded-lg border border-gray-200 dark:border-gray-600">
          <div className="text-xl font-bold text-gray-600 dark:text-gray-400 tabular-nums">
            {sentiment.neutral_count}
          </div>
          <div className="text-xs text-gray-600 dark:text-gray-400 mt-0.5">Neutral</div>
          <div className="text-xs text-gray-500 mt-0.5 tabular-nums">
            {sentiment.percentages.neutral.toFixed(0)}%
          </div>
        </div>
        <div className="text-center p-2.5 bg-red-50 dark:bg-red-900/20 rounded-lg border border-red-100 dark:border-red-800">
          <div className="text-xl font-bold text-red-600 dark:text-red-400 tabular-nums">
            {sentiment.negative_count}
          </div>
          <div className="text-xs text-gray-600 dark:text-gray-400 mt-0.5">Negative</div>
          <div className="text-xs text-gray-500 mt-0.5 tabular-nums">
            {sentiment.percentages.negative.toFixed(0)}%
          </div>
        </div>
      </div>

      {/* Total articles */}
      <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700 text-center">
        <span className="text-xs text-gray-600 dark:text-gray-400">
          Based on {sentiment.total_articles} articles
        </span>
      </div>
    </div>
  );
}

