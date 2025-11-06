"""
PageRank Algorithm Implementation
"""
import numpy as np
from typing import Dict, List, Tuple


class PageRank:
    """
    PageRank algorithm implementation
    
    The PageRank formula:
    PR(A) = (1-d) + d * Σ(PR(Ti)/C(Ti))
    
    Where:
    - PR(A) is the PageRank of page A
    - d is the damping factor (typically 0.85, so ε = 0.15)
    - Ti are pages that link to page A
    - C(Ti) is the number of outbound links from page Ti
    """
    
    def __init__(self, damping_factor: float = 0.85, max_iterations: int = 100, 
                 convergence_threshold: float = 0.0001):
        """
        Initialize PageRank algorithm
        
        Args:
            damping_factor: Probability of following links (1 - ε)
            max_iterations: Maximum number of iterations
            convergence_threshold: Convergence threshold for stopping
        """
        self.damping_factor = damping_factor
        self.max_iterations = max_iterations
        self.convergence_threshold = convergence_threshold
        
    def calculate(self, nodes: List[str], edges: List[Tuple[str, str]]) -> Dict:
        """
        Calculate PageRank for a graph
        
        Args:
            nodes: List of node names
            edges: List of directed edges (source, target)
            
        Returns:
            Dictionary containing PageRank scores, top nodes, and iteration count
        """
        n = len(nodes)
        
        # Create node to index mapping
        node_to_idx = {node: idx for idx, node in enumerate(nodes)}
        
        # Initialize PageRank values (equal distribution)
        pagerank = np.ones(n) / n
        
        # Build adjacency information
        # outlinks[i] = list of nodes that node i links to
        # inlinks[i] = list of nodes that link to node i
        outlinks = {i: [] for i in range(n)}
        inlinks = {i: [] for i in range(n)}
        
        for source, target in edges:
            if source in node_to_idx and target in node_to_idx:
                source_idx = node_to_idx[source]
                target_idx = node_to_idx[target]
                outlinks[source_idx].append(target_idx)
                inlinks[target_idx].append(source_idx)
        
        # Count outlinks for each node
        outlink_counts = {i: len(outlinks[i]) for i in range(n)}
        
        # Iterative computation
        iterations = 0
        for iteration in range(self.max_iterations):
            new_pagerank = np.zeros(n)
            
            for i in range(n):
                # Base rank (random jump)
                rank_sum = (1 - self.damping_factor) / n
                
                # Add rank from incoming links
                for j in inlinks[i]:
                    if outlink_counts[j] > 0:
                        rank_sum += self.damping_factor * (pagerank[j] / outlink_counts[j])
                    else:
                        # If node has no outlinks, distribute its rank equally
                        rank_sum += self.damping_factor * (pagerank[j] / n)
                
                new_pagerank[i] = rank_sum
            
            # Check for convergence
            diff = np.sum(np.abs(new_pagerank - pagerank))
            pagerank = new_pagerank
            iterations = iteration + 1
            
            if diff < self.convergence_threshold:
                break
        
        # Normalize to sum to 1
        pagerank = pagerank / np.sum(pagerank)
        
        # Create result dictionary
        node_scores = {nodes[i]: float(pagerank[i]) for i in range(n)}
        
        # Get top 5 nodes
        sorted_nodes = sorted(node_scores.items(), key=lambda x: x[1], reverse=True)
        top_nodes = [{node: score} for node, score in sorted_nodes[:5]]
        
        return {
            "node_scores": node_scores,
            "top_nodes": top_nodes,
            "iterations": iterations,
            "convergence_threshold": self.convergence_threshold,
            "damping_factor": self.damping_factor
        }
    
    def get_top_k(self, node_scores: Dict[str, float], k: int = 5) -> List[Tuple[str, float]]:
        """
        Get top k nodes by PageRank score
        
        Args:
            node_scores: Dictionary of node scores
            k: Number of top nodes to return
            
        Returns:
            List of (node, score) tuples
        """
        sorted_nodes = sorted(node_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_nodes[:k]
