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

# Load citation network from CSV file
_citation_nodes, _citation_edges = load_network_from_csv('citation_network.csv')

# Citation Network: Research papers citing each other
CITATION_NETWORK = {
    "name": "Academic Citation Network",
    "description": f"Research papers citing each other ({len(_citation_nodes)} nodes, {len(_citation_edges)} edges)",
    "type": "citation",
    "nodes": _citation_nodes,
    "edges": _citation_edges,
    "csv_file": "citation_network.csv"
}

def get_network(network_type: str = "citation"):
    """
    Get the citation network
    
    Args:
        network_type: Only "citation" is supported
    
    Returns:
        Dictionary containing citation network data
    """
    return CITATION_NETWORK

def get_all_networks():
    """Get all available sample networks"""
    return {
        "citation": CITATION_NETWORK
    }
