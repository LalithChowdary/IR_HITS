"""
PageRank Algorithm Implementation using Matrix Multiplication
"""
import numpy as np
from typing import Dict, List, Tuple


class PageRank:
    """
    PageRank algorithm using explicit matrix multiplication
    
    The PageRank formula with teleportation:
    R_{k+1} = (1 - ε) * M' * R_k + (ε / N) * U
    
    Where:
    - R_k is the PageRank vector at iteration k
    - M' is the column-normalized adjacency matrix (transition matrix)
    - ε (epsilon) is the teleportation probability (reset probability)
    - N is the number of nodes
    - U is a vector of ones (uniform teleportation)
    """
    
    def __init__(self, damping_factor: float = 0.85, max_iterations: int = 100, 
                 convergence_threshold: float = 0.0001):
        """
        Initialize PageRank algorithm
        
        Args:
            damping_factor: Probability of following links (typically 0.85)
            max_iterations: Maximum number of iterations
            convergence_threshold: Convergence threshold for stopping
        """
        self.damping_factor = damping_factor
        self.epsilon = 1 - damping_factor  # Teleportation probability
        self.max_iterations = max_iterations
        self.convergence_threshold = convergence_threshold
        
    def build_transition_matrix(self, n: int, edges: List[Tuple[int, int]]) -> np.ndarray:
        """
        Build column-normalized transition matrix M'
        
        Args:
            n: Number of nodes
            edges: List of directed edges as (source_idx, target_idx)
            
        Returns:
            Column-normalized adjacency matrix M'
        """
        # Initialize adjacency matrix
        M = np.zeros((n, n))
        
        # Build adjacency matrix
        # M[i, j] = 1 if there's an edge from j to i (column j points to row i)
        for source_idx, target_idx in edges:
            M[target_idx, source_idx] = 1
        
        # Column-normalize: divide each column by its sum
        # This makes each column a probability distribution
        col_sums = M.sum(axis=0)
        
        # Handle dangling nodes (nodes with no outlinks)
        for j in range(n):
            if col_sums[j] == 0:
                # Distribute probability uniformly to all nodes
                M[:, j] = 1.0 / n
            else:
                M[:, j] = M[:, j] / col_sums[j]
        
        return M
        
    def calculate(self, nodes: List[str], edges: List[Tuple[str, str]]) -> Dict:
        """
        Calculate PageRank using matrix multiplication
        
        Args:
            nodes: List of node names
            edges: List of directed edges (source, target)
            
        Returns:
            Dictionary containing PageRank scores, top nodes, and iteration count
        """
        n = len(nodes)
        
        # Create node to index mapping
        node_to_idx = {node: idx for idx, node in enumerate(nodes)}
        
        # Convert edges to indices
        edge_indices = []
        for source, target in edges:
            if source in node_to_idx and target in node_to_idx:
                source_idx = node_to_idx[source]
                target_idx = node_to_idx[target]
                edge_indices.append((source_idx, target_idx))
        
        # Build transition matrix M'
        M_prime = self.build_transition_matrix(n, edge_indices)
        
        # Initialize PageRank vector (uniform distribution)
        R = np.ones(n) / n
        
        # Uniform teleportation vector
        U = np.ones(n)
        
        # Store history of scores
        history = []
        
        # Iterative computation using matrix multiplication
        iterations = 0
        for iteration in range(self.max_iterations):
            # R_{k+1} = (1 - ε) * M' * R_k + (ε / N) * U
            R_new = self.damping_factor * (M_prime @ R) + (self.epsilon / n) * U
            
            # Store current iteration scores
            history.append({
                "iteration": iteration + 1,
                "scores": {nodes[i]: float(R_new[i]) for i in range(n)}
            })
            
            # Check for convergence
            diff = np.sum(np.abs(R_new - R))
            R = R_new
            iterations = iteration + 1
            
            if diff < self.convergence_threshold:
                break
        
        # Normalize to sum to 1 (should already be close)
        R = R / np.sum(R)
        
        # Create result dictionary
        node_scores = {nodes[i]: float(R[i]) for i in range(n)}
        
        # Get top 5 nodes
        sorted_nodes = sorted(node_scores.items(), key=lambda x: x[1], reverse=True)
        top_nodes = [{node: score} for node, score in sorted_nodes[:5]]
        
        return {
            "node_scores": node_scores,
            "top_nodes": top_nodes,
            "iterations": iterations,
            "convergence_threshold": self.convergence_threshold,
            "damping_factor": self.damping_factor,
            "history": history
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