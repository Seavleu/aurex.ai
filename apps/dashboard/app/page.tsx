'use client';

import { motion } from 'framer-motion';
import PriceCard from '@/components/PriceCard';
import SentimentGauge from '@/components/SentimentGauge';
import NewsFeed from '@/components/NewsFeed';
import PriceChart from '@/components/PriceChart';
import SentimentChart from '@/components/SentimentChart';
import AlertPanel from '@/components/AlertPanel';
import ThemeToggle from '@/components/ThemeToggle';
import MarketStatus from '@/components/MarketStatus';

// Animation variants
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.08
    }
  }
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.4 } }
};

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="sticky top-0 z-50 backdrop-blur-md bg-white/90 dark:bg-gray-800/90 border-b border-gray-200 dark:border-gray-700 shadow-sm">
        <div className="max-w-[1600px] mx-auto px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-amber-500 to-amber-600 bg-clip-text text-transparent">
                AUREX.AI
              </h1>
              <p className="text-xs text-gray-600 dark:text-gray-400 mt-0.5">
                Gold Price Analysis & Sentiment Intelligence
              </p>
            </div>
            <div className="flex gap-3 items-center">
              <ThemeToggle />
              <a
                href="http://localhost:8000/docs"
                target="_blank"
                rel="noopener noreferrer"
                className="px-4 py-2 text-sm bg-amber-500 hover:bg-amber-600 text-white rounded-lg font-medium transition"
              >
                API
              </a>
            </div>
          </div>
        </div>
      </header>

      {/* Main Dashboard - Grid Layout */}
      <main className="max-w-[1600px] mx-auto px-6 lg:px-8 py-6">
        <motion.div
          variants={container}
          initial="hidden"
          animate="show"
          className="grid grid-cols-12 gap-6"
        >
          {/* Top Row: Market Status + Price Card */}
          <motion.div variants={item} className="col-span-12 lg:col-span-4">
            <MarketStatus />
          </motion.div>
          
          <motion.div variants={item} className="col-span-12 lg:col-span-8">
            <PriceCard />
          </motion.div>

          {/* Charts Row */}
          <motion.div variants={item} className="col-span-12 lg:col-span-7">
            <PriceChart />
          </motion.div>

          <motion.div variants={item} className="col-span-12 lg:col-span-5">
            <SentimentChart />
          </motion.div>

          {/* Content Grid */}
          <motion.div variants={item} className="col-span-12 lg:col-span-4">
            <SentimentGauge />
          </motion.div>

          <motion.div variants={item} className="col-span-12 lg:col-span-8">
            <NewsFeed />
          </motion.div>

          {/* Alerts - Full Width */}
          <motion.div variants={item} className="col-span-12">
            <AlertPanel />
          </motion.div>
        </motion.div>

        {/* Info Cards */}
        <motion.div 
          variants={container}
          initial="hidden"
          animate="show"
          className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6"
        >
          <motion.div variants={item} className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
            <div className="flex items-center gap-3">
              <div className="p-2.5 bg-blue-50 dark:bg-blue-900/30 rounded-lg">
                <svg className="w-5 h-5 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <h3 className="text-xs font-medium text-gray-500 dark:text-gray-400">Update Interval</h3>
                <p className="text-lg font-semibold text-gray-900 dark:text-white">30 seconds</p>
              </div>
            </div>
          </motion.div>

          <motion.div variants={item} className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
            <div className="flex items-center gap-3">
              <div className="p-2.5 bg-green-50 dark:bg-green-900/30 rounded-lg">
                <svg className="w-5 h-5 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
                </svg>
              </div>
              <div>
                <h3 className="text-xs font-medium text-gray-500 dark:text-gray-400">AI Model</h3>
                <p className="text-lg font-semibold text-gray-900 dark:text-white">FinBERT</p>
              </div>
            </div>
          </motion.div>

          <motion.div variants={item} className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
            <div className="flex items-center gap-3">
              <div className="p-2.5 bg-purple-50 dark:bg-purple-900/30 rounded-lg">
                <svg className="w-5 h-5 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
              </div>
              <div>
                <h3 className="text-xs font-medium text-gray-500 dark:text-gray-400">Data Sources</h3>
                <p className="text-lg font-semibold text-gray-900 dark:text-white">Multi-source</p>
              </div>
            </div>
          </motion.div>
        </motion.div>
      </main>

      {/* Footer */}
      <footer className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 mt-12">
        <div className="max-w-[1600px] mx-auto px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between text-sm">
            <p className="text-gray-600 dark:text-gray-400">
              © 2025 AUREX.AI - Gold Market Intelligence Platform
            </p>
            <div className="flex gap-4">
              <a href="https://github.com" className="text-gray-600 dark:text-gray-400 hover:text-amber-500 transition">
                GitHub
              </a>
              <a href="http://localhost:8000/docs" className="text-gray-600 dark:text-gray-400 hover:text-amber-500 transition">
                Documentation
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
