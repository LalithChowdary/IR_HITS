'use client';

import React from 'react';
import { CheckCircle2, AlertCircle } from 'lucide-react';

interface InsightsPanelProps {
  insights: string[];
  overlaps: {
    authorities: string[];
    hubs: string[];
  };
}

export default function InsightsPanel({ insights, overlaps }: InsightsPanelProps) {
  return (
    <div className="bg-gradient-to-br from-purple-50 to-blue-50 dark:from-zinc-900 dark:to-zinc-800 rounded-xl p-6 shadow-lg border border-purple-200 dark:border-zinc-700">
      <h3 className="text-xl font-bold mb-4 text-purple-900 dark:text-purple-300 flex items-center gap-2">
        <AlertCircle className="w-5 h-5" />
        Key Insights
      </h3>
      
      <div className="space-y-4">
        {/* Overlaps */}
        <div className="bg-white dark:bg-zinc-800 rounded-lg p-4">
          <h4 className="font-semibold text-sm text-zinc-700 dark:text-zinc-300 mb-2">Overlap Analysis</h4>
          <div className="space-y-2">
            <div className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
              <p className="text-sm text-zinc-600 dark:text-zinc-400">
                <span className="font-semibold text-green-600 dark:text-green-400">{overlaps.authorities.length}</span> nodes in both PageRank & Authorities
                {overlaps.authorities.length > 0 && (
                  <span className="text-xs block mt-1 text-zinc-500">
                    {overlaps.authorities.slice(0, 3).join(', ')}
                    {overlaps.authorities.length > 3 && '...'}
                  </span>
                )}
              </p>
            </div>
            <div className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-blue-500 mt-0.5 flex-shrink-0" />
              <p className="text-sm text-zinc-600 dark:text-zinc-400">
                <span className="font-semibold text-blue-600 dark:text-blue-400">{overlaps.hubs.length}</span> nodes in both PageRank & Hubs
                {overlaps.hubs.length > 0 && (
                  <span className="text-xs block mt-1 text-zinc-500">
                    {overlaps.hubs.slice(0, 3).join(', ')}
                    {overlaps.hubs.length > 3 && '...'}
                  </span>
                )}
              </p>
            </div>
          </div>
        </div>

        {/* Insights */}
        <div className="space-y-2">
          {insights.map((insight, idx) => (
            <div
              key={idx}
              className="bg-white dark:bg-zinc-800 rounded-lg p-3 text-sm text-zinc-700 dark:text-zinc-300 flex items-start gap-2"
            >
              <span className="text-purple-500 font-bold flex-shrink-0">•</span>
              <span>{insight}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
