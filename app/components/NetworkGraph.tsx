'use client';

import React, { useEffect, useRef, useState } from 'react';
import dynamic from 'next/dynamic';
import { VisualizationData } from '../lib/types';

// Dynamically import ForceGraph2D with SSR disabled
const ForceGraph2D = dynamic(() => import('react-force-graph-2d'), {
  ssr: false,
  loading: () => <div className="flex items-center justify-center h-96 text-zinc-400">Loading graph...</div>
});

interface NetworkGraphProps {
  data: VisualizationData;
}

export default function NetworkGraph({ data }: NetworkGraphProps) {
  const fgRef = useRef<any>(null);
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  useEffect(() => {
    if (fgRef.current) {
      // Much stronger repulsive force to separate nodes
      fgRef.current.d3Force('charge').strength(-1500);
      
      // Much longer link distance for better spacing
      fgRef.current.d3Force('link').distance(200).strength(0.5);
      
      // Weaker center force to allow more spreading
      fgRef.current.d3Force('center', fgRef.current.d3.forceCenter().strength(0.05));
      
      // Strong collision detection with larger radius
      fgRef.current.d3Force('collide', fgRef.current.d3.forceCollide().radius((node: any) => node.val + 20));
      
      // Add radial force to spread nodes in a circle
      fgRef.current.d3Force('radial', fgRef.current.d3.forceRadial(200, 0, 0).strength(0.1));
      
      // Warm restart to apply new forces
      fgRef.current.d3ReheatSimulation();
      
      // Auto-fit zoom after simulation settles
      setTimeout(() => {
        if (fgRef.current) {
          fgRef.current.zoomToFit(400, 50); // 400ms duration, 50px padding
        }
      }, 3000);
    }
  }, [data]);

  const getCategoryColor = (category?: string) => {
    switch (category) {
      case 'top_pagerank':
        return '#3b82f6'; // blue
      case 'top_authority':
        return '#10b981'; // green
      case 'top_hub':
        return '#f59e0b'; // amber
      case 'both_pagerank_authority':
        return '#8b5cf6'; // purple
      case 'both_pagerank_hub':
        return '#ec4899'; // pink
      case 'both_authority_hub':
        return '#14b8a6'; // teal
      default:
        return '#6b7280'; // gray
    }
  };

  const graphData = {
    nodes: data.nodes.map((node, index) => ({
      id: node.id,
      name: node.label,
      val: Math.max(15, (node.size || 15) * 2), // Larger minimum size and more scaling
      color: getCategoryColor(node.category),
      pagerank: node.pagerank,
      authority: node.authority,
      hub: node.hub,
      // Pre-position nodes in a rough circle to avoid initial clustering
      x: Math.cos((index / data.nodes.length) * 2 * Math.PI) * 250,
      y: Math.sin((index / data.nodes.length) * 2 * Math.PI) * 250,
      fx: undefined, // Allow movement
      fy: undefined, // Allow movement
    })),
    links: data.edges.map((edge) => ({
      source: edge.source,
      target: edge.target,
    })),
  };

  return (
    <div className="bg-zinc-900 rounded-xl shadow-lg border border-zinc-800 overflow-hidden">
      <div className="p-4 bg-zinc-800 border-b border-zinc-700">
        <h3 className="text-lg font-semibold text-white">Network Visualization</h3>
        <p className="text-sm text-zinc-400 mt-1">
          {data.network_info?.name || 'Interactive Graph'} - Node size by PageRank
        </p>
      </div>
      
      <div className="relative">
        {isClient && (
          <ForceGraph2D
          ref={fgRef}
          graphData={graphData}
          nodeLabel={(node: any) => `
            <div style="background: #1f2937; padding: 8px; border-radius: 6px; border: 1px solid #374151;">
              <div style="color: #fff; font-weight: bold; margin-bottom: 4px;">${node.name}</div>
              ${node.pagerank ? `<div style="color: #3b82f6; font-size: 12px;">PageRank: ${(node.pagerank * 100).toFixed(2)}%</div>` : ''}
              ${node.authority ? `<div style="color: #10b981; font-size: 12px;">Authority: ${node.authority.toFixed(4)}</div>` : ''}
              ${node.hub ? `<div style="color: #f59e0b; font-size: 12px;">Hub: ${node.hub.toFixed(4)}</div>` : ''}
            </div>
          `}
          nodeCanvasObject={(node: any, ctx, globalScale) => {
            const label = node.name;
            const fontSize = Math.max(12, 16 / globalScale);
            ctx.font = `bold ${fontSize}px Sans-Serif`;
            
            // Draw outer glow/shadow
            ctx.beginPath();
            ctx.arc(node.x, node.y, node.val + 3, 0, 2 * Math.PI, false);
            ctx.fillStyle = 'rgba(0, 0, 0, 0.3)';
            ctx.fill();
            
            // Draw thick black border
            ctx.beginPath();
            ctx.arc(node.x, node.y, node.val + 2, 0, 2 * Math.PI, false);
            ctx.fillStyle = '#000000';
            ctx.fill();
            
            // Draw main node
            ctx.beginPath();
            ctx.arc(node.x, node.y, node.val, 0, 2 * Math.PI, false);
            ctx.fillStyle = node.color;
            ctx.fill();
            
            // Draw inner highlight
            ctx.beginPath();
            ctx.arc(node.x - node.val * 0.3, node.y - node.val * 0.3, node.val * 0.3, 0, 2 * Math.PI, false);
            ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
            ctx.fill();
            
            // Draw label with better contrast
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            
            // Black outline for text
            ctx.strokeStyle = '#000000';
            ctx.lineWidth = 3;
            ctx.strokeText(label, node.x, node.y + node.val + 20);
            
            // White text
            ctx.fillStyle = '#ffffff';
            ctx.fillText(label, node.x, node.y + node.val + 20);
          }}
          linkDirectionalArrowLength={10}
          linkDirectionalArrowRelPos={0.9}
          linkColor={() => '#9ca3af'}
          linkWidth={3}
          linkDirectionalParticles={2}
          linkDirectionalParticleSpeed={0.006}
          linkDirectionalParticleWidth={2}
          backgroundColor="#09090b"
          width={1000}
          height={800}
          cooldownTicks={200}
          d3AlphaDecay={0.005}
          d3VelocityDecay={0.2}
          enableNodeDrag={true}
          enableZoomInteraction={true}
          enablePanInteraction={true}
        />
        )}
        
        {/* Controls */}
        <div className="absolute top-4 right-4 bg-zinc-800/90 backdrop-blur-sm rounded-lg p-3 border border-zinc-700">
          <div className="flex gap-2 mb-3">
            <button
              onClick={() => fgRef.current?.zoomToFit?.(400, 50)}
              className="px-2 py-1 bg-blue-600 hover:bg-blue-700 rounded text-xs text-white"
            >
              Fit View
            </button>
            <button
              onClick={() => fgRef.current?.d3ReheatSimulation?.()}
              className="px-2 py-1 bg-green-600 hover:bg-green-700 rounded text-xs text-white"
            >
              Restart
            </button>
          </div>
        </div>
        
        {/* Legend */}
        <div className="absolute bottom-4 right-4 bg-zinc-800/90 backdrop-blur-sm rounded-lg p-3 border border-zinc-700">
          <p className="text-xs font-semibold text-zinc-300 mb-2">Legend</p>
          <div className="space-y-1 text-xs">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-blue-500"></div>
              <span className="text-zinc-400">Top PageRank</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-green-500"></div>
              <span className="text-zinc-400">Top Authority</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-amber-500"></div>
              <span className="text-zinc-400">Top Hub</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-purple-500"></div>
              <span className="text-zinc-400">PR + Authority</span>
            </div>
          </div>
          <div className="mt-2 pt-2 border-t border-zinc-600 text-xs text-zinc-500">
            Drag nodes • Zoom • Pan
          </div>
        </div>
      </div>
    </div>
  );
}
