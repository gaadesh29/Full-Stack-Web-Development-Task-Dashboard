import React from 'react';
import { Info } from 'lucide-react';
import dynamic from "next/dynamic";
import { useEffect, useRef } from "react";
import * as d3 from "d3";
import { sankey, sankeyLinkHorizontal } from "d3-sankey";

export default function SankeyChart() {
  const ref = useRef(null);

  useEffect(() => {
    const data = {
      nodes: [
        { name: "Nippon Large Cap Fund - Direct Plan", color: "#E6C76A" },
        { name: "Motilal Large Cap Fund - Direct Plan", color: "#2B6CB0" },
        { name: "HDFC Large Cap Fund", color: "#F2994A" },
        { name: "ICICI Prudential Midcap Fund", color: "#B7C94B" },
        { name: "HDFC LTD.", color: "#FFC300" },
        { name: "RIL", color: "#00B894" },
        { name: "INFY", color: "#6C47FF" },
        { name: "TCS", color: "#00BFFF" },
        { name: "HDFCBANK", color: "#FF5733" },
        { name: "BHARTIARTL", color: "#FF5733" }
      ],
      links: [
        { source: 0, target: 4, value: 5 },
        { source: 0, target: 5, value: 3 },
        { source: 1, target: 4, value: 2 },
        { source: 1, target: 6, value: 6 },
        { source: 2, target: 5, value: 4 },
        { source: 2, target: 7, value: 2 },
        { source: 3, target: 8, value: 3 },
        { source: 3, target: 9, value: 2 }
      ]
    };

    const svg = d3.select(ref.current);
    svg.selectAll("*").remove();

    const { width, height } = ref.current.getBoundingClientRect();
    svg.attr("width", width).attr("height", height);

    const sankeyGen = sankey()
      .nodeWidth(16)
      .nodePadding(24)
      .extent([[1, 1], [width - 1, height - 1]]);

    const sankeyData = sankeyGen({
      nodes: data.nodes.map(d => ({ ...d })),
      links: data.links.map(d => ({ ...d }))
    });

    // Draw links
    svg.append("g")
      .selectAll("path")
      .data(sankeyData.links)
      .join("path")
      .attr("d", sankeyLinkHorizontal())
      .attr("fill", "none")
      .attr("stroke", "#444")
      .attr("opacity", 0.5)
      .attr("stroke-width", d => Math.max(1, d.width));

    // Draw nodes (vertical bars)
    svg.append("g")
      .selectAll("rect")
      .data(sankeyData.nodes)
      .join("rect")
      .attr("x", d => d.x0)
      .attr("y", d => d.y0)
      .attr("height", d => d.y1 - d.y0)
      .attr("width", d => d.x1 - d.x0)
      .attr("fill", d => d.color || "#e0f2fe")
      .attr("rx", 4)
      .attr("ry", 4);

    // Add labels
    svg.append("g")
      .selectAll("text")
      .data(sankeyData.nodes)
      .join("text")
      .attr("x", d => d.x0 < width / 2 ? d.x1 + 10 : d.x0 - 10)
      .attr("y", d => (d.y1 + d.y0) / 2)
      .attr("dy", "0.35em")
      .attr("text-anchor", d => d.x0 < width / 2 ? "start" : "end")
      .attr("fill", "#fff")
      .style("font-family", "Inter, sans-serif")
      .style("font-size", "15px")
      .style("font-weight", 500)
      .text(d => d.name);

  }, []);

  return (
    <div className="bg-[#181C23] p-8 rounded-2xl shadow-lg">
      <div className="flex items-center mb-2">
        <span className="text-white text-lg font-bold mr-2">Overlap Analysis</span>
        <Info className="w-4 h-4 text-gray-400" />
      </div>
      <div className="text-gray-300 text-sm mb-2">Comparing : <span className="text-white font-medium">Motilal Large Cap Fund and Nippon Large Cap Fund</span></div>
      <div className="text-gray-400 text-xs mb-4">
        <span className="text-white font-bold">• X Stocks Overlap</span> across these funds.<br />
        <span className="text-white font-bold">• Y% Average Overlap</span> in holdings.
      </div>
      <svg ref={ref} style={{ width: "100%", height: "340px" }} />
    </div>
  );
}