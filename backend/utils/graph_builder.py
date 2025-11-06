"""
Graph utility functions
"""
import networkx as nx
from typing import List, Tuple, Dict


def build_graph(nodes: List[str], edges: List[Tuple[str, str]]) -> nx.DiGraph:
    """
    Build a NetworkX directed graph from nodes and edges
    
    Args:
        nodes: List of node names
        edges: List of directed edges (source, target)
        
    Returns:
        NetworkX DiGraph object
    """
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    return G


def get_network_statistics(nodes: List[str], edges: List[Tuple[str, str]]) -> Dict:
    """
    Calculate network statistics
    
    Args:
        nodes: List of node names
        edges: List of directed edges (source, target)
        
    Returns:
        Dictionary containing network statistics
    """
    G = build_graph(nodes, edges)
    
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    
    # Calculate density
    if num_nodes > 1:
        density = num_edges / (num_nodes * (num_nodes - 1))
    else:
        density = 0.0
    
    # Calculate average degree
    if num_nodes > 0:
        total_degree = sum(dict(G.degree()).values())
        avg_degree = total_degree / num_nodes
    else:
        avg_degree = 0.0
    
    return {
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "density": density,
        "avg_degree": avg_degree
    }


def get_node_degrees(nodes: List[str], edges: List[Tuple[str, str]]) -> Dict[str, Dict[str, int]]:
    """
    Get in-degree and out-degree for each node
    
    Args:
        nodes: List of node names
        edges: List of directed edges (source, target)
        
    Returns:
        Dictionary mapping node names to their in/out degrees
    """
    G = build_graph(nodes, edges)
    
    node_degrees = {}
    for node in nodes:
        node_degrees[node] = {
            "in_degree": G.in_degree(node),
            "out_degree": G.out_degree(node),
            "total_degree": G.degree(node)
        }
    
    return node_degrees


def prepare_visualization_data(
    nodes: List[str], 
    edges: List[Tuple[str, str]], 
    pagerank_scores: Dict[str, float] = None,
    authority_scores: Dict[str, float] = None,
    hub_scores: Dict[str, float] = None,
    top_pagerank: List[str] = None,
    top_authorities: List[str] = None,
    top_hubs: List[str] = None
) -> Dict:
    """
    Prepare data for graph visualization
    
    Args:
        nodes: List of node names
        edges: List of directed edges
        pagerank_scores: PageRank scores for nodes
        authority_scores: Authority scores for nodes
        hub_scores: Hub scores for nodes
        top_pagerank: List of top PageRank nodes
        top_authorities: List of top authority nodes
        top_hubs: List of top hub nodes
        
    Returns:
        Dictionary containing visualization data
    """
    G = build_graph(nodes, edges)
    
    # Get positions using spring layout
    pos = nx.spring_layout(G, k=2, iterations=50)
    
    # Prepare node data
    node_data = []
    for node in nodes:
        node_info = {
            "id": node,
            "label": node,
            "x": float(pos[node][0]),
            "y": float(pos[node][1]),
        }
        
        # Add scores if available
        if pagerank_scores:
            node_info["pagerank"] = pagerank_scores.get(node, 0)
            # Size proportional to PageRank
            node_info["size"] = 10 + (pagerank_scores.get(node, 0) * 100)
        
        if authority_scores:
            node_info["authority"] = authority_scores.get(node, 0)
        
        if hub_scores:
            node_info["hub"] = hub_scores.get(node, 0)
        
        # Determine node category for coloring
        category = "regular"
        if top_pagerank and node in top_pagerank:
            if top_authorities and node in top_authorities:
                category = "both_pagerank_authority"
            elif top_hubs and node in top_hubs:
                category = "both_pagerank_hub"
            else:
                category = "top_pagerank"
        elif top_authorities and node in top_authorities:
            if top_hubs and node in top_hubs:
                category = "both_authority_hub"
            else:
                category = "top_authority"
        elif top_hubs and node in top_hubs:
            category = "top_hub"
        
        node_info["category"] = category
        
        node_data.append(node_info)
    
    # Prepare edge data
    edge_data = []
    for source, target in edges:
        edge_data.append({
            "source": source,
            "target": target
        })
    
    return {
        "nodes": node_data,
        "edges": edge_data
    }
