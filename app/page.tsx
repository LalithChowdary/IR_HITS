'use client';

import { useState, useEffect } from 'react';
import { Network, Sparkles, TrendingUp, Search, BarChart3, Loader2 } from 'lucide-react';
import { api } from './lib/api';
import { ComparisonResult, VisualizationData, NetworkInfo } from './lib/types';
import RankingChart from './components/RankingChart';
import StatCard from './components/StatCard';
import InsightsPanel from './components/InsightsPanel';
import NetworkGraph from './components/NetworkGraph';

export default function Home() {
  const [networkType, setNetworkType] = useState<'citation' | 'social'>('citation');
  const [loading, setLoading] = useState(false);
  const [comparisonData, setComparisonData] = useState<ComparisonResult | null>(null);
  const [visualizationData, setVisualizationData] = useState<VisualizationData | null>(null);
  const [networkInfo, setNetworkInfo] = useState<NetworkInfo | null>(null);
  const [dampingFactor, setDampingFactor] = useState(0.85);

  useEffect(() => {
    loadData();
  }, [networkType]);

  const loadData = async () => {
    setLoading(true);
    try {
      const [comparison, visualization, info] = await Promise.all([
        api.compareAlgorithms(networkType, dampingFactor),
        api.getVisualization(networkType, true),
        api.getNetworkInfo(networkType),
      ]);
      setComparisonData(comparison);
      setVisualizationData(visualization);
      setNetworkInfo(info);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-zinc-50 via-blue-50 to-purple-50 dark:from-zinc-950 dark:via-zinc-900 dark:to-zinc-950">
      {/* Header */}
      <header className="bg-white/80 dark:bg-zinc-900/80 backdrop-blur-md border-b border-zinc-200 dark:border-zinc-800 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg">
                <Network className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  PageRank & HITS Analysis
                </h1>
                <p className="text-sm text-zinc-600 dark:text-zinc-400">
                  Network Ranking & Authority Detection
                </p>
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <div className="flex gap-2 bg-zinc-100 dark:bg-zinc-800 p-1 rounded-lg">
                <button
                  onClick={() => setNetworkType('citation')}
                  className={`px-4 py-2 rounded-md text-sm font-medium transition-all ${
                    networkType === 'citation'
                      ? 'bg-white dark:bg-zinc-700 text-blue-600 dark:text-blue-400 shadow-sm'
                      : 'text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200'
                  }`}
                >
                  📚 Citation Network
                </button>
                <button
                  onClick={() => setNetworkType('social')}
                  className={`px-4 py-2 rounded-md text-sm font-medium transition-all ${
                    networkType === 'social'
                      ? 'bg-white dark:bg-zinc-700 text-purple-600 dark:text-purple-400 shadow-sm'
                      : 'text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200'
                  }`}
                >
                  👥 Social Network
                </button>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {loading ? (
          <div className="flex items-center justify-center h-96">
            <div className="text-center">
              <Loader2 className="w-12 h-12 text-blue-600 animate-spin mx-auto mb-4" />
              <p className="text-zinc-600 dark:text-zinc-400">Analyzing network...</p>
            </div>
          </div>
        ) : (
          <>
            {/* Network Info */}
            {networkInfo && (
              <div className="mb-8">
                <div className="bg-white dark:bg-zinc-900 rounded-xl p-6 shadow-lg border border-zinc-200 dark:border-zinc-800">
                  <h2 className="text-xl font-bold text-zinc-900 dark:text-zinc-100 mb-4">
                    {networkInfo.name}
                  </h2>
                  <p className="text-zinc-600 dark:text-zinc-400 mb-4">{networkInfo.description}</p>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div>
                      <p className="text-sm text-zinc-500 dark:text-zinc-500">Nodes</p>
                      <p className="text-2xl font-bold text-blue-600">{networkInfo.num_nodes}</p>
                    </div>
                    <div>
                      <p className="text-sm text-zinc-500 dark:text-zinc-500">Edges</p>
                      <p className="text-2xl font-bold text-purple-600">{networkInfo.num_edges}</p>
                    </div>
                    <div>
                      <p className="text-sm text-zinc-500 dark:text-zinc-500">Density</p>
                      <p className="text-2xl font-bold text-green-600">
                        {(networkInfo.density * 100).toFixed(1)}%
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-zinc-500 dark:text-zinc-500">Avg Degree</p>
                      <p className="text-2xl font-bold text-amber-600">
                        {networkInfo.avg_degree.toFixed(1)}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Stats Cards */}
            {comparisonData && (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <StatCard
                  title="PageRank Iterations"
                  value={comparisonData.pagerank.iterations}
                  subtitle={`Damping factor: ${(comparisonData.pagerank.damping_factor * 100).toFixed(0)}%`}
                  icon="trending"
                  color="text-blue-600"
                />
                <StatCard
                  title="HITS Iterations"
                  value={comparisonData.hits.iterations}
                  subtitle="Authority & Hub scores computed"
                  icon="award"
                  color="text-green-600"
                />
                <StatCard
                  title="Overlap Nodes"
                  value={comparisonData.overlap_authorities.length}
                  subtitle="In both PageRank & Authority"
                  icon="network"
                  color="text-purple-600"
                />
              </div>
            )}

            {/* Graph Visualization */}
            {visualizationData && (
              <div className="mb-8">
                <NetworkGraph data={visualizationData} />
              </div>
            )}

            {/* Rankings */}
            {comparisonData && (
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
                <RankingChart
                  data={comparisonData.pagerank.top_nodes}
                  title="🏆 Top 5 PageRank"
                  color="#3b82f6"
                />
                <RankingChart
                  data={comparisonData.hits.top_authorities}
                  title="⭐ Top 5 Authorities"
                  color="#10b981"
                />
                <RankingChart
                  data={comparisonData.hits.top_hubs}
                  title="🔗 Top 5 Hubs"
                  color="#f59e0b"
                />
              </div>
            )}

            {/* Insights */}
            {comparisonData && (
              <InsightsPanel
                insights={comparisonData.insights}
                overlaps={{
                  authorities: comparisonData.overlap_authorities,
                  hubs: comparisonData.overlap_hubs,
                }}
              />
            )}

            {/* Controls */}
            <div className="mt-8 bg-white dark:bg-zinc-900 rounded-xl p-6 shadow-lg border border-zinc-200 dark:border-zinc-800">
              <h3 className="text-lg font-semibold mb-4 text-zinc-900 dark:text-zinc-100">
                Algorithm Parameters
              </h3>
              <div className="flex items-center gap-4">
                <label className="flex items-center gap-2 text-sm text-zinc-600 dark:text-zinc-400">
                  Damping Factor (ε = {(1 - dampingFactor).toFixed(2)}):
                  <input
                    type="range"
                    min="0.7"
                    max="0.95"
                    step="0.05"
                    value={dampingFactor}
                    onChange={(e) => setDampingFactor(parseFloat(e.target.value))}
                    className="w-48"
                  />
                  <span className="font-mono text-blue-600">{dampingFactor.toFixed(2)}</span>
                </label>
                <button
                  onClick={loadData}
                  className="px-6 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-medium hover:from-blue-700 hover:to-purple-700 transition-all shadow-lg hover:shadow-xl flex items-center gap-2"
                >
                  <Sparkles className="w-4 h-4" />
                  Recalculate
                </button>
              </div>
            </div>
          </>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white/80 dark:bg-zinc-900/80 backdrop-blur-md border-t border-zinc-200 dark:border-zinc-800 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-sm text-zinc-600 dark:text-zinc-400">
            <p>Built with Next.js, FastAPI, and cutting-edge graph algorithms</p>
            <p className="mt-1">PageRank & HITS Analysis Tool © 2025</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
