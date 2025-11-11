"""
FastAPI Backend for PageRank and HITS Analysis
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Tuple
import csv
import os

from algorithms.pagerank import PageRank
from algorithms.hits import HITS
from models.graph_models import (
    AlgorithmRequest, 
    PageRankResult, 
    HITSResult, 
    ComparisonResult,
    NetworkInfo,
    VisualizationData
)
from utils.graph_builder import (
    get_network_statistics,
    prepare_visualization_data,
    get_node_degrees
)

# Load citation network from CSV
def load_citation_network() -> Tuple[List[str], List[Tuple[str, str]]]:
    """Load citation network from CSV file"""
    edges = []
    nodes_set = set()
    
    csv_path = os.path.join(os.path.dirname(__file__), 'data', 'citation_network.csv')
    
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

# Load the network at startup
_nodes, _edges = load_citation_network()

def get_network():
    """Get the citation network data"""
    return {
        "name": "Academic Citation Network",
        "description": f"Research papers citing each other ({len(_nodes)} nodes, {len(_edges)} edges)",
        "type": "citation",
        "nodes": _nodes,
        "edges": _edges,
        "csv_file": "citation_network.csv"
    }

app = FastAPI(
    title="PageRank & HITS Analysis API",
    description="API for analyzing networks using PageRank and HITS algorithms",
    version="1.0.0"
)

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "PageRank & HITS Analysis API",
        "version": "1.0.0",
        "endpoints": {
            "network_info": "/api/network",
            "pagerank": "/api/algorithms/pagerank",
            "hits": "/api/algorithms/hits",
            "compare": "/api/algorithms/compare",
            "visualization": "/api/visualization"
        }
    }


@app.get("/api/network-info")
def get_network_summary():
    """Get network summary information"""
    network = get_network()
    
    return {
        "name": network["name"],
        "description": network["description"],
        "num_nodes": len(network["nodes"]),
        "num_edges": len(network["edges"])
    }


@app.get("/api/network", response_model=NetworkInfo)
def get_network_info():
    """Get detailed information about the citation network"""
    try:
        network = get_network()
        stats = get_network_statistics(network["nodes"], network["edges"])
        
        return NetworkInfo(
            name=network["name"],
            description=network["description"],
            type=network["type"],
            num_nodes=stats["num_nodes"],
            num_edges=stats["num_edges"],
            density=stats["density"],
            avg_degree=stats["avg_degree"]
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Network not found: {str(e)}")


@app.post("/api/algorithms/pagerank", response_model=PageRankResult)
def run_pagerank(request: AlgorithmRequest):
    """Run PageRank algorithm on citation network"""
    try:
        # Get network data
        network = get_network()
        
        # Initialize and run PageRank
        pr = PageRank(
            damping_factor=request.damping_factor,
            max_iterations=request.max_iterations,
            convergence_threshold=request.convergence_threshold
        )
        
        result = pr.calculate(network["nodes"], network["edges"])
        
        # Exclude history for this endpoint
        result.pop("history", None)
        
        return PageRankResult(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PageRank calculation failed: {str(e)}")


@app.post("/api/algorithms/pagerank/iterations", response_model=PageRankResult)
def run_pagerank_with_iterations(request: AlgorithmRequest):
    """Run PageRank and return results with iteration history"""
    try:
        network = get_network()
        pr = PageRank(
            damping_factor=request.damping_factor,
            max_iterations=request.max_iterations,
            convergence_threshold=request.convergence_threshold
        )
        result = pr.calculate(network["nodes"], network["edges"])
        return PageRankResult(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PageRank calculation failed: {str(e)}")


@app.post("/api/algorithms/hits", response_model=HITSResult)
def run_hits(request: AlgorithmRequest):
    """Run HITS algorithm on citation network"""
    try:
        # Get network data
        network = get_network()
        
        # Initialize and run HITS
        hits = HITS(
            max_iterations=request.max_iterations,
            convergence_threshold=request.convergence_threshold
        )
        
        result = hits.calculate(network["nodes"], network["edges"])
        
        # Exclude history for this endpoint
        result.pop("history", None)
        
        return HITSResult(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"HITS calculation failed: {str(e)}")


@app.post("/api/algorithms/hits/iterations", response_model=HITSResult)
def run_hits_with_iterations(request: AlgorithmRequest):
    """Run HITS and return results with iteration history"""
    try:
        network = get_network()
        hits = HITS(
            max_iterations=request.max_iterations,
            convergence_threshold=request.convergence_threshold
        )
        result = hits.calculate(network["nodes"], network["edges"])
        return HITSResult(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"HITS calculation failed: {str(e)}")


@app.post("/api/algorithms/compare", response_model=ComparisonResult)
def compare_algorithms(request: AlgorithmRequest):
    """Run both PageRank and HITS, then compare results"""
    try:
        # Get network data
        network = get_network()
        
        # Run PageRank
        pr = PageRank(
            damping_factor=request.damping_factor,
            max_iterations=request.max_iterations,
            convergence_threshold=request.convergence_threshold
        )
        pagerank_result = pr.calculate(network["nodes"], network["edges"])
        
        # Exclude history for comparison
        pagerank_result_for_comparison = pagerank_result.copy()
        pagerank_result_for_comparison.pop("history", None)
        
        # Run HITS
        hits = HITS(
            max_iterations=request.max_iterations,
            convergence_threshold=request.convergence_threshold
        )
        hits_result = hits.calculate(network["nodes"], network["edges"])
        
        # Exclude history for comparison
        hits_result_for_comparison = hits_result.copy()
        hits_result_for_comparison.pop("history", None)
        
        # Extract top node names
        top_pagerank_nodes = [list(item.keys())[0] for item in pagerank_result_for_comparison["top_nodes"]]
        top_authority_nodes = [list(item.keys())[0] for item in hits_result_for_comparison["top_authorities"]]
        top_hub_nodes = [list(item.keys())[0] for item in hits_result_for_comparison["top_hubs"]]
        
        # Find overlaps
        overlap_authorities = list(set(top_pagerank_nodes) & set(top_authority_nodes))
        overlap_hubs = list(set(top_pagerank_nodes) & set(top_hub_nodes))
        
        # Get top scoring nodes for detailed analysis
        top_pr_node = list(pagerank_result_for_comparison["top_nodes"][0].keys())[0]
        top_pr_score = list(pagerank_result_for_comparison["top_nodes"][0].values())[0]
        top_auth_node = list(hits_result_for_comparison["top_authorities"][0].keys())[0]
        top_auth_score = list(hits_result_for_comparison["top_authorities"][0].values())[0]
        top_hub_node = list(hits_result_for_comparison["top_hubs"][0].keys())[0]
        top_hub_score = list(hits_result_for_comparison["top_hubs"][0].values())[0]
        
        # Get node degrees for context
        node_degrees = get_node_degrees(network["nodes"], network["edges"])
        
        # Generate enhanced insights
        insights = []
        
        # Overlap insights with percentages
        overlap_auth_pct = (len(overlap_authorities) / len(top_pagerank_nodes)) * 100 if top_pagerank_nodes else 0
        overlap_hub_pct = (len(overlap_hubs) / len(top_pagerank_nodes)) * 100 if top_pagerank_nodes else 0
        
        if overlap_authorities:
            insights.append(
                f"📊 {len(overlap_authorities)} node(s) appear in both top PageRank and top Authorities ({overlap_auth_pct:.0f}% overlap): {', '.join(overlap_authorities)}"
            )
        else:
            insights.append("📊 No overlap between top PageRank nodes and top Authorities - different ranking criteria")
        
        if overlap_hubs:
            insights.append(
                f"📊 {len(overlap_hubs)} node(s) appear in both top PageRank and top Hubs ({overlap_hub_pct:.0f}% overlap): {', '.join(overlap_hubs)}"
            )
        else:
            insights.append("📊 No overlap between top PageRank nodes and top Hubs - different ranking criteria")
        
        # Top node analysis with degree information
        top_pr_in = node_degrees.get(top_pr_node, {}).get("in_degree", 0)
        top_pr_out = node_degrees.get(top_pr_node, {}).get("out_degree", 0)
        insights.append(
            f"🏆 Node {top_pr_node} has highest PageRank ({top_pr_score:.4f}) with {top_pr_in} incoming and {top_pr_out} outgoing citations"
        )
        
        top_auth_in = node_degrees.get(top_auth_node, {}).get("in_degree", 0)
        insights.append(
            f"⭐ Node {top_auth_node} is the top Authority ({top_auth_score:.4f}) with {top_auth_in} papers citing it"
        )
        
        top_hub_out = node_degrees.get(top_hub_node, {}).get("out_degree", 0)
        insights.append(
            f"🔗 Node {top_hub_node} is the top Hub ({top_hub_score:.4f}) citing {top_hub_out} other papers"
        )
        
        # Convergence insights
        pr_iters = pagerank_result_for_comparison.get("iterations", 0)
        hits_iters = hits_result_for_comparison.get("iterations", 0)
        if pr_iters and hits_iters:
            insights.append(
                f"⚡ Algorithms converged: PageRank in {pr_iters} iterations, HITS in {hits_iters} iterations"
            )
        
        # Domain-specific insights
        insights.append("💡 In citation networks, high PageRank indicates papers that are both cited and cite other influential papers")
        insights.append("💡 High Authority scores identify foundational/seminal papers that are frequently referenced")
        insights.append("💡 High Hub scores identify survey/review papers that cite many important works")
        
        # Network structure insight
        avg_in_degree = sum(d.get("in_degree", 0) for d in node_degrees.values()) / len(node_degrees) if node_degrees else 0
        avg_out_degree = sum(d.get("out_degree", 0) for d in node_degrees.values()) / len(node_degrees) if node_degrees else 0
        insights.append(
            f"📈 Network structure: Average {avg_in_degree:.1f} citations received, {avg_out_degree:.1f} citations made per paper"
        )
        
        # Correlation insight
        if len(overlap_authorities) > len(overlap_hubs):
            insights.append("🔍 PageRank correlates more strongly with Authority scores - citation quality matters more than quantity")
        elif len(overlap_hubs) > len(overlap_authorities):
            insights.append("🔍 PageRank correlates more strongly with Hub scores - citing behavior influences overall importance")
        else:
            insights.append("🔍 PageRank shows balanced correlation with both Authority and Hub scores")
        
        return ComparisonResult(
            pagerank=PageRankResult(**pagerank_result_for_comparison),
            hits=HITSResult(**hits_result_for_comparison),
            overlap_authorities=overlap_authorities,
            overlap_hubs=overlap_hubs,
            insights=insights
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")


@app.get("/api/visualization")
def get_visualization(include_scores: bool = False):
    """Get graph visualization data"""
    try:
        # Get network data
        network = get_network()
        
        viz_data = {
            "nodes": [],
            "edges": [],
            "network_info": {
                "name": network["name"],
                "type": network["type"]
            }
        }
        
        if include_scores:
            # Run algorithms to get scores
            pr = PageRank()
            pr_result = pr.calculate(network["nodes"], network["edges"])
            
            hits = HITS()
            hits_result = hits.calculate(network["nodes"], network["edges"])
            
            # Get top nodes
            top_pr = [list(item.keys())[0] for item in pr_result["top_nodes"]]
            top_auth = [list(item.keys())[0] for item in hits_result["top_authorities"]]
            top_hub = [list(item.keys())[0] for item in hits_result["top_hubs"]]
            
            # Prepare visualization with scores
            viz_data = prepare_visualization_data(
                network["nodes"],
                network["edges"],
                pagerank_scores=pr_result["node_scores"],
                authority_scores=hits_result["authority_scores"],
                hub_scores=hits_result["hub_scores"],
                top_pagerank=top_pr,
                top_authorities=top_auth,
                top_hubs=top_hub
            )
            viz_data["network_info"] = {
                "name": network["name"],
                "type": network["type"]
            }
        else:
            # Simple visualization without scores
            viz_data = prepare_visualization_data(
                network["nodes"],
                network["edges"]
            )
            viz_data["network_info"] = {
                "name": network["name"],
                "type": network["type"]
            }
        
        return viz_data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Visualization generation failed: {str(e)}")


@app.get("/api/node-degrees")
def get_degrees():
    """Get in-degree and out-degree for all nodes"""
    try:
        network = get_network()
        degrees = get_node_degrees(network["nodes"], network["edges"])
        return {"node_degrees": degrees}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Degree calculation failed: {str(e)}")


@app.get("/api/dataset")
def get_dataset_info():
    """Get dataset information including CSV file location"""
    try:
        network = get_network()
        return {
            "name": network["name"],
            "description": network["description"],
            "type": network["type"],
            "csv_file": network.get("csv_file", "N/A"),
            "num_nodes": len(network["nodes"]),
            "num_edges": len(network["edges"]),
            "sample_edges": network["edges"][:10]  # First 10 edges as sample
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Dataset not found: {str(e)}")