/**
 * AUREX.AI - News Feed Component
 */

'use client';

import { useState } from 'react';
import { useRecentNews } from '@/lib/hooks';
import { News } from '@/lib/api';

function NewsCard({ article }: { article: News }) {
  const getSentimentBadge = (label: string | null, score: number | null) => {
    if (!label) return null;

    const colors = {
      positive: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
      neutral: 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-400',
      negative: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400',
    };

    const color = colors[label as keyof typeof colors] || colors.neutral;

    return (
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${color}`}>
        {label} {score && `(${(score * 100).toFixed(0)}%)`}
      </span>
    );
  };

  return (
    <article className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow hover:shadow-lg transition-all duration-200 border border-gray-200 dark:border-gray-700">
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <a
            href={article.url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-lg font-semibold text-gray-900 dark:text-white hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
          >
            {article.title}
          </a>
        </div>
        {getSentimentBadge(article.sentiment_label, article.sentiment_score)}
      </div>

      {article.content && (
        <p className="text-gray-600 dark:text-gray-300 text-sm mb-3 line-clamp-2">
          {article.content}
        </p>
      )}

      <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
        <span className="font-medium">{article.source}</span>
        <time>{new Date(article.published).toLocaleString()}</time>
      </div>
    </article>
  );
}

export default function NewsFeed() {
  const { data: news, loading, error } = useRecentNews(24, true, 60000);
  const [showAll, setShowAll] = useState(false);

  const displayedNews = showAll ? news : news?.slice(0, 5);

  if (loading && !news) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700 h-full">
        <h2 className="text-lg font-bold mb-4 text-gray-900 dark:text-white">Latest News</h2>
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="animate-pulse">
              <div className="h-20 bg-gray-200 dark:bg-gray-700 rounded-lg"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700 h-full">
        <h2 className="text-lg font-bold mb-4 text-gray-900 dark:text-white">Latest News</h2>
        <p className="text-red-500 text-sm">{error.message}</p>
      </div>
    );
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700 h-full flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-bold text-gray-900 dark:text-white">
          Latest News
        </h2>
        <span className="text-xs bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 px-2 py-1 rounded-full">
          {news?.length || 0} articles
        </span>
      </div>

      <div className="space-y-3 flex-1 overflow-y-auto pr-2 custom-scrollbar">
        {displayedNews && displayedNews.length > 0 ? (
          displayedNews.map((article) => (
            <NewsCard key={article.id} article={article} />
          ))
        ) : (
          <div className="text-center text-gray-500 py-12">
            <svg className="w-12 h-12 mx-auto mb-3 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
            </svg>
            <p className="text-sm">No news available</p>
          </div>
        )}
      </div>

      {news && news.length > 5 && (
        <button
          onClick={() => setShowAll(!showAll)}
          className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700 text-sm text-amber-600 dark:text-amber-400 hover:text-amber-700 dark:hover:text-amber-300 font-medium transition flex items-center justify-center gap-2"
        >
          {showAll ? (
            <>
              Show Less
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
              </svg>
            </>
          ) : (
            <>
              Show All {news.length} Articles
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </>
          )}
        </button>
      )}
    </div>
  );
}

