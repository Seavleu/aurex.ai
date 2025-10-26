/**
 * AUREX.AI - Price Card Component
 */

'use client';

import { useLatestPrice } from '@/lib/hooks';

export default function PriceCard() {
  const { data: price, loading, error } = useLatestPrice(true, 30000);

  if (loading && !price) {
    return (
      <div className="bg-gradient-to-br from-amber-500 to-yellow-600 rounded-2xl p-8 shadow-2xl animate-pulse">
        <div className="h-8 bg-white/20 rounded w-32 mb-4"></div>
        <div className="h-16 bg-white/20 rounded w-48"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-gradient-to-br from-red-500 to-red-600 rounded-2xl p-8 shadow-2xl">
        <h2 className="text-white text-xl font-bold mb-2">Error</h2>
        <p className="text-white/80">{error.message}</p>
      </div>
    );
  }

  if (!price) {
    return (
      <div className="bg-gradient-to-br from-gray-500 to-gray-600 rounded-2xl p-8 shadow-2xl">
        <h2 className="text-white text-xl font-bold mb-2">No Data</h2>
        <p className="text-white/80">Price data unavailable</p>
      </div>
    );
  }

  const isPositive = (price.change_pct || 0) >= 0;
  const changeColor = isPositive ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400';

  return (
    <div className="bg-gradient-to-br from-amber-500 to-amber-600 rounded-lg p-6 shadow-sm border border-amber-600 h-full">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-white text-xl font-bold">XAU/USD</h2>
          <p className="text-white/80 text-xs mt-0.5">Gold Spot Price</p>
        </div>
        <span className="text-white/70 text-xs tabular-nums">
          {new Date(price.timestamp).toLocaleTimeString()}
        </span>
      </div>

      <div className="mb-6">
        <div className="text-white text-5xl font-bold mb-2 tabular-nums">
          ${price.close.toFixed(2)}
        </div>
        <div className={`${changeColor} text-xl font-semibold inline-flex items-center gap-2 bg-white/20 dark:bg-black/20 px-3 py-1.5 rounded-lg`}>
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            {isPositive ? (
              <path fillRule="evenodd" d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z" clipRule="evenodd" />
            ) : (
              <path fillRule="evenodd" d="M14.707 10.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 12.586V5a1 1 0 012 0v7.586l2.293-2.293a1 1 0 011.414 0z" clipRule="evenodd" />
            )}
          </svg>
          <span>${Math.abs(price.change || 0).toFixed(2)}</span>
          <span>({(price.change_pct || 0).toFixed(2)}%)</span>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-4 pt-4 border-t border-white/30">
        <div>
          <div className="text-white/70 text-xs mb-1">Open</div>
          <div className="text-white text-lg font-semibold tabular-nums">${price.open.toFixed(2)}</div>
        </div>
        <div>
          <div className="text-white/70 text-xs mb-1">High</div>
          <div className="text-white text-lg font-semibold tabular-nums">${price.high.toFixed(2)}</div>
        </div>
        <div>
          <div className="text-white/70 text-xs mb-1">Low</div>
          <div className="text-white text-lg font-semibold tabular-nums">${price.low.toFixed(2)}</div>
        </div>
      </div>
    </div>
  );
}

