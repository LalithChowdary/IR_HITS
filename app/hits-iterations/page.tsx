'use client';

import { useState, useEffect } from 'react';
import { api, HITSResult } from '../lib/api';
import { Loader2, ArrowLeft } from 'lucide-react';
import Link from 'next/link';

export default function HITSİterationsPage() {
  const [loading, setLoading] = useState(true);
  const [hitsData, setHitsData] = useState<HITSResult | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await api.runHITSWithHistory();
        setHitsData(data);
      } catch (error) {
        console.error('Error fetching HITS history:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-zinc-50 via-blue-50 to-purple-50 dark:from-zinc-950 dark:via-zinc-900 dark:to-zinc-950">
      <header className="bg-white/80 dark:bg-zinc-900/80 backdrop-blur-md border-b border-zinc-200 dark:border-zinc-800 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Link href="/" className="p-2 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg text-white">
                <ArrowLeft className="w-6 h-6" />
              </Link>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  HITS Algorithm Iterations
                </h1>
                <p className="text-sm text-zinc-600 dark:text-zinc-400">
                  Step-by-step score convergence
                </p>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {loading ? (
          <div className="flex items-center justify-center h-96">
            <div className="text-center">
              <Loader2 className="w-12 h-12 text-blue-600 animate-spin mx-auto mb-4" />
              <p className="text-zinc-600 dark:text-zinc-400">Calculating iterations...</p>
            </div>
          </div>
        ) : hitsData && hitsData.history ? (
          <div className="space-y-8">
            {hitsData.history.map((iteration) => (
              <div key={iteration.iteration} className="bg-white dark:bg-zinc-900 rounded-xl p-6 shadow-lg border border-zinc-200 dark:border-zinc-800">
                <h2 className="text-xl font-bold text-zinc-900 dark:text-zinc-100 mb-4">
                  Iteration {iteration.iteration}
                </h2>
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-zinc-200 dark:divide-zinc-700">
                    <thead className="bg-zinc-50 dark:bg-zinc-800">
                      <tr>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-300 uppercase tracking-wider">
                          Node
                        </th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-300 uppercase tracking-wider">
                          Authority Score
                        </th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-300 uppercase tracking-wider">
                          Hub Score
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white dark:bg-zinc-900 divide-y divide-zinc-200 dark:divide-zinc-800">
                      {Object.keys(iteration.authority_scores).map((node) => (
                        <tr key={node}>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-zinc-900 dark:text-zinc-100">
                            {node}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-zinc-500 dark:text-zinc-400">
                            {iteration.authority_scores[node].toFixed(6)}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-zinc-500 dark:text-zinc-400">
                            {iteration.hub_scores[node].toFixed(6)}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center text-zinc-600 dark:text-zinc-400">
            No iteration data available.
          </div>
        )}
      </main>
    </div>
  );
}
