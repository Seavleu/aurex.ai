/**
 * AUREX.AI - Market Status Component
 * Shows live market sessions and high-impact gold price factors
 */

'use client';

import { useEffect, useState } from 'react';

// Collapsible Section Component
function CollapsibleSection({ 
  title, 
  children, 
  defaultOpen = false,
  count 
}: { 
  title: string; 
  children: React.ReactNode; 
  defaultOpen?: boolean;
  count?: number;
}) {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <div className="border-t border-gray-200 dark:border-gray-700 pt-4 mt-4">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between text-left group hover:opacity-70 transition"
      >
        <div className="flex items-center gap-2">
          <h3 className="text-sm font-semibold text-gray-700 dark:text-gray-300">
            {title}
          </h3>
          {count !== undefined && (
            <span className="text-xs bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 px-2 py-0.5 rounded-full">
              {count}
            </span>
          )}
        </div>
        <svg
          className={`w-5 h-5 text-gray-400 transition-transform ${isOpen ? 'rotate-180' : ''}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>
      {isOpen && <div className="mt-3">{children}</div>}
    </div>
  );
}

interface MarketSession {
  name: string;
  region: string;
  open: string;
  close: string;
  color: string;
  icon: string;
}

const SESSIONS: MarketSession[] = [
  {
    name: 'Asian Session',
    region: 'Tokyo/Hong Kong',
    open: '00:00',
    close: '09:00',
    color: 'bg-red-500',
    icon: 'ASIA',
  },
  {
    name: 'London Session',
    region: 'London',
    open: '08:00',
    close: '17:00',
    color: 'bg-blue-500',
    icon: 'EUR',
  },
  {
    name: 'New York Session',
    region: 'New York',
    open: '13:00',
    close: '22:00',
    color: 'bg-green-500',
    icon: 'US',
  },
];

const HIGH_IMPACT_FACTORS = [
  { factor: 'US Dollar Index (DXY)', importance: 'Critical', description: 'Inverse correlation - Strong USD = Lower Gold' },
  { factor: 'Real Interest Rates', importance: 'Critical', description: 'Nominal rate minus inflation - Most important metric' },
  { factor: 'Federal Reserve Policy', importance: 'Critical', description: 'Rate decisions, QE/QT, Powell speeches' },
  { factor: 'US Treasury Yields (10Y)', importance: 'Critical', description: 'Opportunity cost - Higher yields = Lower gold' },
  { factor: 'Inflation Data (CPI/PCE)', importance: 'High', description: 'Gold as inflation hedge' },
  { factor: 'China Economic Data', importance: 'High', description: 'Largest consumer - PMI, GDP, retail sales' },
  { factor: 'Central Bank Purchases', importance: 'High', description: 'Russia, China, India accumulating reserves' },
  { factor: 'Geopolitical Tensions', importance: 'Variable', description: 'War, conflict - Safe haven demand' },
  { factor: 'S&P 500 / Stock Market', importance: 'Medium', description: 'Risk-on vs risk-off sentiment' },
  { factor: 'ETF Gold Holdings (GLD)', importance: 'Medium', description: 'Investment demand indicator' },
  { factor: 'Oil Prices (WTI/Brent)', importance: 'Medium', description: 'Inflation proxy and economic indicator' },
  { factor: 'US Jobs Data (NFP)', importance: 'High', description: 'Employment = Fed policy expectations' },
  { factor: 'India Gold Demand', importance: 'Medium', description: '2nd largest consumer - Wedding season, festivals' },
  { factor: 'Bitcoin/Crypto Prices', importance: 'Medium', description: 'Alternative store of value competition' },
  { factor: 'Banking/Financial Crisis', importance: 'Variable', description: 'Flight to safety trigger' },
];

export default function MarketStatus() {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  if (!mounted) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700 animate-pulse h-full">
        <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-32 mb-4"></div>
        <div className="h-20 bg-gray-200 dark:bg-gray-700 rounded"></div>
      </div>
    );
  }

  // Check if market is open (Mon-Fri)
  const dayOfWeek = currentTime.getDay();
  const isWeekday = dayOfWeek >= 1 && dayOfWeek <= 5;
  const isMarketOpen = isWeekday;

  // Get current UTC hour
  const utcHour = currentTime.getUTCHours();

  // Determine active session
  const activeSession = SESSIONS.find((session) => {
    const [openHour] = session.open.split(':').map(Number);
    const [closeHour] = session.close.split(':').map(Number);
    return utcHour >= openHour && utcHour < closeHour;
  });

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700 h-full flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-bold text-gray-900 dark:text-white">
          Market Status
        </h2>
        <span className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold ${
          isMarketOpen 
            ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' 
            : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
        }`}>
          <span className={`w-2 h-2 rounded-full ${isMarketOpen ? 'bg-green-500' : 'bg-gray-400'}`}></span>
          {isMarketOpen ? 'Market Open' : 'Market Closed'}
        </span>
      </div>

      {/* Current Time */}
      <div className="mb-4">
        <div className="text-2xl font-bold text-gray-900 dark:text-white tabular-nums">
          {currentTime.toLocaleTimeString('en-US', { hour12: false })}
        </div>
        <div className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
          {currentTime.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
        </div>
      </div>

      {/* Active Session */}
      {activeSession && (
        <div className="mb-4 p-3 bg-gradient-to-r from-amber-50 to-transparent dark:from-amber-900/20 dark:to-transparent rounded-lg border border-amber-200 dark:border-amber-800">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-sm font-semibold text-gray-900 dark:text-white">
                {activeSession.name}
              </div>
              <div className="text-xs text-gray-600 dark:text-gray-400 mt-0.5">
                {activeSession.region} • {activeSession.open} - {activeSession.close} UTC
              </div>
            </div>
            <div className={`w-3 h-3 rounded-full ${activeSession.color}`}></div>
          </div>
        </div>
      )}

      {/* Trading Sessions - Collapsible */}
      <CollapsibleSection title="Trading Sessions" count={SESSIONS.length}>
        <div className="space-y-2">
          {SESSIONS.map((session, index) => (
            <div
              key={index}
              className={`p-3 rounded-lg border transition-all ${
                activeSession?.name === session.name
                  ? 'bg-amber-50 dark:bg-amber-900/20 border-amber-200 dark:border-amber-800'
                  : 'bg-gray-50 dark:bg-gray-700/30 border-gray-200 dark:border-gray-600'
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className={`w-2 h-2 rounded-full ${session.color}`}></div>
                  <div>
                    <div className="text-sm font-medium text-gray-900 dark:text-white">
                      {session.name}
                    </div>
                    <div className="text-xs text-gray-600 dark:text-gray-400">
                      {session.open} - {session.close} UTC
                    </div>
                  </div>
                </div>
                <div className="text-xs font-mono text-gray-500 dark:text-gray-400">
                  {session.icon}
                </div>
              </div>
            </div>
          ))}
        </div>
      </CollapsibleSection>

      {/* Gold Price Drivers - Collapsible */}
      <CollapsibleSection title="Gold Price Drivers" count={HIGH_IMPACT_FACTORS.length}>
        <div className="space-y-2 max-h-80 overflow-y-auto pr-2 custom-scrollbar">
          {HIGH_IMPACT_FACTORS.map((item, index) => (
            <div
              key={index}
              className="group p-3 bg-gray-50 dark:bg-gray-700/30 rounded-lg border border-gray-200 dark:border-gray-600 hover:border-amber-300 dark:hover:border-amber-600 transition-all cursor-help"
              title={item.description}
            >
              <div className="flex items-start justify-between gap-3">
                <div className="flex-1 min-w-0">
                  <div className="font-medium text-sm text-gray-900 dark:text-white">
                    {item.factor}
                  </div>
                  <div className="text-xs text-gray-600 dark:text-gray-400 mt-1 line-clamp-2 group-hover:line-clamp-none transition-all">
                    {item.description}
                  </div>
                </div>
                <span
                  className={`text-xs font-semibold px-2 py-1 rounded whitespace-nowrap flex-shrink-0 ${
                    item.importance === 'Critical'
                      ? 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
                      : item.importance === 'High'
                      ? 'bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-400'
                      : item.importance === 'Medium'
                      ? 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400'
                      : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400'
                  }`}
                >
                  {item.importance}
                </span>
              </div>
            </div>
          ))}
        </div>
      </CollapsibleSection>

      {/* Info */}
      <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
        <div className="text-xs text-gray-500 dark:text-gray-400 space-y-1">
          <div>Market Hours: 24/5 (Monday - Friday)</div>
          <div>Gold: XAU/USD spot price</div>
        </div>
      </div>
    </div>
  );
}
