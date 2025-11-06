"""
Sample networks for PageRank and HITS analysis
"""
import csv
import os
from typing import List, Tuple, Dict

def load_network_from_csv(csv_file: str) -> Tuple[List[str], List[Tuple[str, str]]]:
    """
    Load network from CSV file
    
    Args:
        csv_file: Path to CSV file with 'source,target' format
        
    Returns:
        Tuple of (nodes list, edges list)
    """
    edges = []
    nodes_set = set()
    
    csv_path = os.path.join(os.path.dirname(__file__), csv_file)
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            source = row['source'].strip()
            target = row['target'].strip()
            edges.append((source, target))
            nodes_set.add(source)
            nodes_set.add(target)
    
    nodes = sorted(list(nodes_set))
    return nodes, edges

# Load networks from CSV files
_citation_nodes, _citation_edges = load_network_from_csv('citation_network.csv')
_social_nodes, _social_edges = load_network_from_csv('social_network.csv')

# Citation Network: Research papers citing each other
CITATION_NETWORK = {
    "name": "Academic Citation Network",
    "description": f"Research papers citing each other ({len(_citation_nodes)} nodes, {len(_citation_edges)} edges)",
    "type": "citation",
    "nodes": _citation_nodes,
    "edges": _citation_edges,
    "csv_file": "citation_network.csv"
}

# Social Network: Users mentioning/retweeting each other
SOCIAL_NETWORK = {
    "name": "Social Media Network",
    "description": f"Users mentioning and retweeting each other ({len(_social_nodes)} nodes, {len(_social_edges)} edges)",
    "type": "social",
    "nodes": _social_nodes,
    "edges": _social_edges,
    "csv_file": "social_network.csv"
}

def get_network(network_type: str = "citation"):
    """
    Get a sample network by type
    
    Args:
        network_type: "citation" or "social"
    
    Returns:
        Dictionary containing network data
    """
    if network_type.lower() == "citation":
        return CITATION_NETWORK
    elif network_type.lower() == "social":
        return SOCIAL_NETWORK
    else:
        return CITATION_NETWORK

def get_all_networks():
    """Get all available sample networks"""
    return {
        "citation": CITATION_NETWORK,
        "social": SOCIAL_NETWORK
    }
