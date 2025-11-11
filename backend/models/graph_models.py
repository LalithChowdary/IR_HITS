"""
Pydantic models for API requests and responses
"""
from typing import List, Dict, Tuple, Optional
from pydantic import BaseModel, Field


class GraphData(BaseModel):
    """Graph structure with nodes and edges"""
    nodes: List[str]
    edges: List[Tuple[str, str]]
    name: str = "Custom Network"
    description: str = ""
    type: str = "custom"


class PageRankIterationHistory(BaseModel):
    """PageRank scores at a single iteration"""
    iteration: int
    scores: Dict[str, float]


class PageRankResult(BaseModel):
    """PageRank algorithm results"""
    node_scores: Dict[str, float] = Field(..., description="PageRank score for each node")
    top_nodes: List[Dict[str, float]] = Field(..., description="Top 5 ranked nodes")
    iterations: int = Field(..., description="Number of iterations to convergence")
    convergence_threshold: float = Field(default=0.0001)
    damping_factor: float = Field(default=0.85)
    history: Optional[List[PageRankIterationHistory]] = Field(None, description="History of scores at each iteration")


class IterationHistory(BaseModel):
    """HITS scores at a single iteration"""
    iteration: int
    authority_scores: Dict[str, float]
    hub_scores: Dict[str, float]


class HITSResult(BaseModel):
    """HITS algorithm results"""
    authority_scores: Dict[str, float] = Field(..., description="Authority score for each node")
    hub_scores: Dict[str, float] = Field(..., description="Hub score for each node")
    top_authorities: List[Dict[str, float]] = Field(..., description="Top 5 authority nodes")
    top_hubs: List[Dict[str, float]] = Field(..., description="Top 5 hub nodes")
    iterations: int = Field(..., description="Number of iterations to convergence")
    history: Optional[List[IterationHistory]] = Field(None, description="History of scores at each iteration")


class ComparisonResult(BaseModel):
    """Combined results from both algorithms"""
    pagerank: PageRankResult
    hits: HITSResult
    overlap_authorities: List[str] = Field(..., description="Nodes in both top PageRank and top authorities")
    overlap_hubs: List[str] = Field(..., description="Nodes in both top PageRank and top hubs")
    insights: List[str] = Field(..., description="Key insights from comparison")


class NetworkInfo(BaseModel):
    """Network metadata and statistics"""
    name: str
    description: str
    type: str
    num_nodes: int
    num_edges: int
    density: float
    avg_degree: float


class AlgorithmRequest(BaseModel):
    """Request to run an algorithm"""
    damping_factor: float = Field(default=0.85, description="Damping factor for PageRank (1 - ε)")
    max_iterations: int = Field(default=100, description="Maximum iterations")
    convergence_threshold: float = Field(default=0.0001, description="Convergence threshold")


class VisualizationData(BaseModel):
    """Data for graph visualization"""
    nodes: List[Dict]
    edges: List[Dict]
    layout: str = "force"
    
    class Config:
        arbitrary_types_allowed = True
