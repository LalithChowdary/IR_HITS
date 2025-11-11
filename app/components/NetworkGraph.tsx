'use client';

import React, { useEffect, useRef } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import { VisualizationData } from '../lib/types';

interface NetworkGraphProps {
  data: VisualizationData;
}

export default function NetworkGraph({ data }: NetworkGraphProps) {
  const fgRef = useRef<any>(null);

  useEffect(() => {
    if (fgRef.current) {
      fgRef.current.d3Force('charge').strength(-600);
      fgRef.current.d3Force('link').distance(150);
    }
  }, []);

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
    nodes: data.nodes.map((node) => ({
      id: node.id,
      name: node.label,
      val: node.size || 10,
      color: getCategoryColor(node.category),
      pagerank: node.pagerank,
      authority: node.authority,
      hub: node.hub,
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
            const fontSize = 12 / globalScale;
            ctx.font = `${fontSize}px Sans-Serif`;
            
            // Draw node
            ctx.beginPath();
            ctx.arc(node.x, node.y, node.val, 0, 2 * Math.PI, false);
            ctx.fillStyle = node.color;
            ctx.fill();
            
            // Draw label
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillStyle = '#fff';
            ctx.fillText(label, node.x, node.y + node.val + 8);
          }}
          linkDirectionalArrowLength={10}
          linkDirectionalArrowRelPos={1}
          linkColor={() => '#9ca3af'}
          linkWidth={2}
          backgroundColor="#09090b"
          width={800}
          height={600}
        />
        
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
        </div>
      </div>
    </div>
  );
}
