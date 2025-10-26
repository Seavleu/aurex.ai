/**
 * AUREX.AI - Alert Management Panel
 */

'use client';

import { useState } from 'react';
import { useAlerts } from '@/lib/hooks';
import { api } from '@/lib/api';

type SeverityFilter = 'all' | 'critical' | 'high' | 'medium' | 'low';

export default function AlertPanel() {
  const [severityFilter, setSeverityFilter] = useState<SeverityFilter>('all');
  const [showCreateModal, setShowCreateModal] = useState(false);
  
  const severity = severityFilter === 'all' ? undefined : severityFilter;
  const { data: alerts, loading, error, refetch } = useAlerts(72, severity, true, 30000);

  const handleAcknowledge = async (id: number) => {
    try {
      await api.alerts.acknowledge(id);
      refetch();
    } catch (err) {
      console.error('Failed to acknowledge alert:', err);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this alert?')) return;
    try {
      await api.alerts.delete(id);
      refetch();
    } catch (err) {
      console.error('Failed to delete alert:', err);
    }
  };

  // Get severity color
  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'critical':
        return 'bg-red-100 text-red-800 border-red-300 dark:bg-red-900/30 dark:text-red-400';
      case 'high':
        return 'bg-orange-100 text-orange-800 border-orange-300 dark:bg-orange-900/30 dark:text-orange-400';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-300 dark:bg-yellow-900/30 dark:text-yellow-400';
      case 'low':
        return 'bg-blue-100 text-blue-800 border-blue-300 dark:bg-blue-900/30 dark:text-blue-400';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300 dark:bg-gray-700 dark:text-gray-300';
    }
  };

  // Get alert icon
  const getAlertIcon = (type: string) => {
    if (type.includes('price')) {
      return (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      );
    }
    if (type.includes('sentiment')) {
      return (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
        </svg>
      );
    }
    return (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
    );
  };

  if (loading && !alerts) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-xl">
        <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-48 mb-6 animate-pulse"></div>
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-20 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-xl">
        <h2 className="text-2xl font-bold mb-4 text-gray-900 dark:text-white">Alerts</h2>
        <p className="text-red-500">{error.message}</p>
      </div>
    );
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <h2 className="text-lg font-bold text-gray-900 dark:text-white">Alerts</h2>
          <span className="text-xs bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 px-2 py-1 rounded-full">
            {alerts?.length || 0}
          </span>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="px-3 py-1.5 bg-amber-500 hover:bg-amber-600 text-white rounded-lg font-medium transition text-sm flex items-center gap-2"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          Create
        </button>
      </div>

      {/* Filters */}
      <div className="flex gap-2 mb-4 overflow-x-auto pb-2">
        {(['all', 'critical', 'high', 'medium', 'low'] as SeverityFilter[]).map((sev) => (
          <button
            key={sev}
            onClick={() => setSeverityFilter(sev)}
            className={`px-3 py-1.5 rounded-lg font-medium transition-all whitespace-nowrap text-xs ${
              severityFilter === sev
                ? 'bg-amber-500 text-white'
                : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
            }`}
          >
            {sev.charAt(0).toUpperCase() + sev.slice(1)}
          </button>
        ))}
      </div>

      {/* Alerts List */}
      {alerts && alerts.length > 0 ? (
        <div className="space-y-4">
          {alerts.map((alert) => (
            <div
              key={alert.id}
              className={`p-4 rounded-lg border-2 transition-all hover:shadow-md ${getSeverityColor(alert.severity)}`}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-3 flex-1">
                  <div className="mt-0.5">{getAlertIcon(alert.type)}</div>
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="font-bold text-sm uppercase">
                        {alert.severity}
                      </span>
                      <span className="text-xs opacity-75">•</span>
                      <span className="text-xs opacity-75">{alert.type}</span>
                    </div>
                    <p className="text-sm font-medium mb-2">{alert.message}</p>
                    <p className="text-xs opacity-75">
                      {new Date(alert.timestamp).toLocaleString()}
                    </p>
                  </div>
                </div>
                <div className="flex gap-2 ml-4">
                  <button
                    onClick={() => handleAcknowledge(alert.id)}
                    className="p-2 hover:bg-white/50 dark:hover:bg-black/20 rounded transition"
                    title="Acknowledge"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  </button>
                  <button
                    onClick={() => handleDelete(alert.id)}
                    className="p-2 hover:bg-white/50 dark:hover:bg-black/20 rounded transition"
                    title="Delete"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
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
              d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
            />
          </svg>
          <p className="text-lg text-gray-600 dark:text-gray-400">No active alerts</p>
          <p className="text-sm text-gray-500 dark:text-gray-500 mt-2">
            Create an alert to get notified about price or sentiment changes
          </p>
        </div>
      )}

      {/* Create Alert Modal */}
      {showCreateModal && (
        <CreateAlertModal
          onClose={() => setShowCreateModal(false)}
          onSuccess={() => {
            setShowCreateModal(false);
            refetch();
          }}
        />
      )}
    </div>
  );
}

// Create Alert Modal Component
function CreateAlertModal({
  onClose,
  onSuccess,
}: {
  onClose: () => void;
  onSuccess: () => void;
}) {
  const [formData, setFormData] = useState({
    type: 'price_threshold',
    severity: 'medium',
    message: '',
    threshold: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await api.alerts.create({
        type: formData.type,
        severity: formData.severity,
        message: formData.message || `Alert: ${formData.type}`,
        metadata: { threshold: parseFloat(formData.threshold) },
      });
      onSuccess();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white dark:bg-gray-800 rounded-2xl p-8 max-w-md w-full mx-4 shadow-2xl">
        <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Create Alert</h3>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Alert Type
            </label>
            <select
              value={formData.type}
              onChange={(e) => setFormData({ ...formData, type: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            >
              <option value="price_threshold">Price Threshold</option>
              <option value="price_change">Price Change %</option>
              <option value="sentiment_shift">Sentiment Shift</option>
              <option value="sentiment_extreme">Extreme Sentiment</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Severity
            </label>
            <select
              value={formData.severity}
              onChange={(e) => setFormData({ ...formData, severity: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="critical">Critical</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Threshold Value
            </label>
            <input
              type="number"
              step="0.01"
              value={formData.threshold}
              onChange={(e) => setFormData({ ...formData, threshold: e.target.value })}
              placeholder="e.g., 2800 for price, 0.5 for sentiment"
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Custom Message (optional)
            </label>
            <textarea
              value={formData.message}
              onChange={(e) => setFormData({ ...formData, message: e.target.value })}
              placeholder="Custom alert message..."
              rows={3}
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            />
          </div>

          {error && (
            <div className="p-3 bg-red-100 dark:bg-red-900/30 border border-red-300 dark:border-red-700 rounded-lg">
              <p className="text-sm text-red-800 dark:text-red-400">{error}</p>
            </div>
          )}

          <div className="flex gap-3 mt-6">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-300 rounded-lg font-semibold hover:bg-gray-300 dark:hover:bg-gray-600 transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="flex-1 px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg font-semibold transition disabled:opacity-50"
            >
              {loading ? 'Creating...' : 'Create Alert'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

