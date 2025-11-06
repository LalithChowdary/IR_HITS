"""
HITS (Hyperlink-Induced Topic Search) Algorithm Implementation
"""
import numpy as np
from typing import Dict, List, Tuple


class HITS:
    """
    HITS algorithm implementation
    
    HITS computes two scores for each node:
    - Authority score: quality of content (cited by good hubs)
    - Hub score: quality of links (links to good authorities)
    
    Update rules:
    - Authority(p) = Σ Hub(q) for all q linking to p
    - Hub(p) = Σ Authority(q) for all q that p links to
    
    Scores are normalized after each iteration
    """
    
    def __init__(self, max_iterations: int = 100, convergence_threshold: float = 0.0001):
        """
        Initialize HITS algorithm
        
        Args:
            max_iterations: Maximum number of iterations
            convergence_threshold: Convergence threshold for stopping
        """
        self.max_iterations = max_iterations
        self.convergence_threshold = convergence_threshold
    
    def calculate(self, nodes: List[str], edges: List[Tuple[str, str]]) -> Dict:
        """
        Calculate HITS authority and hub scores
        
        Args:
            nodes: List of node names
            edges: List of directed edges (source, target)
            
        Returns:
            Dictionary containing authority scores, hub scores, top authorities, and top hubs
        """
        n = len(nodes)
        
        # Create node to index mapping
        node_to_idx = {node: idx for idx, node in enumerate(nodes)}
        
        # Initialize authority and hub scores to 1
        authority = np.ones(n)
        hub = np.ones(n)
        
        # Build adjacency lists
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
        
        # Iterative computation
        iterations = 0
        for iteration in range(self.max_iterations):
            new_authority = np.zeros(n)
            new_hub = np.zeros(n)
            
            # Update authority scores
            # Authority(p) = Σ Hub(q) for all q linking to p
            for i in range(n):
                for j in inlinks[i]:
                    new_authority[i] += hub[j]
            
            # Update hub scores
            # Hub(p) = Σ Authority(q) for all q that p links to
            for i in range(n):
                for j in outlinks[i]:
                    new_hub[i] += authority[j]
            
            # Normalize scores (L2 normalization)
            auth_norm = np.linalg.norm(new_authority)
            hub_norm = np.linalg.norm(new_hub)
            
            if auth_norm > 0:
                new_authority = new_authority / auth_norm
            if hub_norm > 0:
                new_hub = new_hub / hub_norm
            
            # Check for convergence
            auth_diff = np.sum(np.abs(new_authority - authority))
            hub_diff = np.sum(np.abs(new_hub - hub))
            
            authority = new_authority
            hub = new_hub
            iterations = iteration + 1
            
            if auth_diff < self.convergence_threshold and hub_diff < self.convergence_threshold:
                break
        
        # Create result dictionaries
        authority_scores = {nodes[i]: float(authority[i]) for i in range(n)}
        hub_scores = {nodes[i]: float(hub[i]) for i in range(n)}
        
        # Get top 5 authorities
        sorted_authorities = sorted(authority_scores.items(), key=lambda x: x[1], reverse=True)
        top_authorities = [{node: score} for node, score in sorted_authorities[:5]]
        
        # Get top 5 hubs
        sorted_hubs = sorted(hub_scores.items(), key=lambda x: x[1], reverse=True)
        top_hubs = [{node: score} for node, score in sorted_hubs[:5]]
        
        return {
            "authority_scores": authority_scores,
            "hub_scores": hub_scores,
            "top_authorities": top_authorities,
            "top_hubs": top_hubs,
            "iterations": iterations
        }
    
    def get_top_k_authorities(self, authority_scores: Dict[str, float], k: int = 5) -> List[Tuple[str, float]]:
        """
        Get top k nodes by authority score
        
        Args:
            authority_scores: Dictionary of authority scores
            k: Number of top nodes to return
            
        Returns:
            List of (node, score) tuples
        """
        sorted_nodes = sorted(authority_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_nodes[:k]
    
    def get_top_k_hubs(self, hub_scores: Dict[str, float], k: int = 5) -> List[Tuple[str, float]]:
        """
        Get top k nodes by hub score
        
        Args:
            hub_scores: Dictionary of hub scores
            k: Number of top nodes to return
            
        Returns:
            List of (node, score) tuples
        """
        sorted_nodes = sorted(hub_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_nodes[:k]
