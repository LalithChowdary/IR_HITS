// API client for backend communication
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

export interface NetworkInfo {
  name: string;
  description: string;
  type: string;
  num_nodes: number;
  num_edges: number;
  density: number;
  avg_degree: number;
}

export interface PageRankResult {
  node_scores: Record<string, number>;
  top_nodes: Array<Record<string, number>>;
  iterations: number;
  convergence_threshold: number;
  damping_factor: number;
}

export interface HITSResult {
  authority_scores: Record<string, number>;
  hub_scores: Record<string, number>;
  top_authorities: Array<Record<string, number>>;
  top_hubs: Array<Record<string, number>>;
  iterations: number;
}

export interface ComparisonResult {
  pagerank: PageRankResult;
  hits: HITSResult;
  overlap_authorities: string[];
  overlap_hubs: string[];
  insights: string[];
}

export interface VisualizationNode {
  id: string;
  label: string;
  x: number;
  y: number;
  pagerank?: number;
  authority?: number;
  hub?: number;
  size?: number;
  category?: string;
}

export interface VisualizationEdge {
  source: string;
  target: string;
}

export interface VisualizationData {
  nodes: VisualizationNode[];
  edges: VisualizationEdge[];
  network_info?: {
    name: string;
    type: string;
  };
}

export const api = {
  async getNetworks() {
    const response = await fetch(`${API_BASE_URL}/api/networks`);
    if (!response.ok) throw new Error('Failed to fetch networks');
    return response.json();
  },

  async getNetworkInfo(networkType: string): Promise<NetworkInfo> {
    const response = await fetch(`${API_BASE_URL}/api/network/${networkType}`);
    if (!response.ok) throw new Error('Failed to fetch network info');
    return response.json();
  },

  async runPageRank(networkType: string, dampingFactor: number = 0.85): Promise<PageRankResult> {
    const response = await fetch(`${API_BASE_URL}/api/algorithms/pagerank`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        network_type: networkType,
        damping_factor: dampingFactor,
        max_iterations: 100,
        convergence_threshold: 0.0001,
      }),
    });
    if (!response.ok) throw new Error('Failed to run PageRank');
    return response.json();
  },

  async runHITS(networkType: string): Promise<HITSResult> {
    const response = await fetch(`${API_BASE_URL}/api/algorithms/hits`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        network_type: networkType,
        max_iterations: 100,
        convergence_threshold: 0.0001,
      }),
    });
    if (!response.ok) throw new Error('Failed to run HITS');
    return response.json();
  },

  async compareAlgorithms(networkType: string, dampingFactor: number = 0.85): Promise<ComparisonResult> {
    const response = await fetch(`${API_BASE_URL}/api/algorithms/compare`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        network_type: networkType,
        damping_factor: dampingFactor,
        max_iterations: 100,
        convergence_threshold: 0.0001,
      }),
    });
    if (!response.ok) throw new Error('Failed to compare algorithms');
    return response.json();
  },

  async getVisualization(networkType: string, includeScores: boolean = true): Promise<VisualizationData> {
    const response = await fetch(
      `${API_BASE_URL}/api/visualization/${networkType}?include_scores=${includeScores}`
    );
    if (!response.ok) throw new Error('Failed to fetch visualization data');
    return response.json();
  },
};
