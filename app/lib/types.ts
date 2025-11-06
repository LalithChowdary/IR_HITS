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
