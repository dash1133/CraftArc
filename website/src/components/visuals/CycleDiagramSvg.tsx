"use client";

import { CYCLE } from "@/content/copy";

/** Four parts on a loop around one agent. Part 4 points back to Part 1. The step list beside it is the accessible control. */
export default function CycleDiagramSvg({ active, onSelect }: { active: number; onSelect: (n: number) => void }) {
  const C = 160, R = 112;
  const pos = [
    { x: C, y: C - R }, // Part 1, top
    { x: C + R, y: C }, // Part 2, right
    { x: C, y: C + R }, // Part 3, bottom
    { x: C - R, y: C }, // Part 4, left
  ];
  // arcs between nodes, clockwise, stopping short of each node
  const arc = (from: number) => {
    const a0 = (-90 + from * 90 + 22) * (Math.PI / 180);
    const a1 = (-90 + (from + 1) * 90 - 22) * (Math.PI / 180);
    const p0 = { x: C + R * Math.cos(a0), y: C + R * Math.sin(a0) };
    const p1 = { x: C + R * Math.cos(a1), y: C + R * Math.sin(a1) };
    return `M${p0.x},${p0.y} A${R},${R} 0 0 1 ${p1.x},${p1.y}`;
  };
  return (
    <svg viewBox="0 0 320 320" className="mx-auto w-full max-w-[340px]" aria-hidden="true">
      <defs>
        <marker id="cyc-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
          <path d="M0,0 L10,5 L0,10 z" fill="#94A3B8" />
        </marker>
      </defs>
      <circle cx={C} cy={C} r={R} fill="none" stroke="#E2E8F0" strokeWidth="1" />
      {[0, 1, 2, 3].map((i) => (
        <path key={i} d={arc(i)} fill="none" stroke={i === 3 ? "#0F172A" : "#94A3B8"} strokeWidth={i === 3 ? 1.5 : 1.25} strokeDasharray={i === 3 ? "4 4" : undefined} markerEnd="url(#cyc-arrow)" />
      ))}
      <g>
        <rect x={C - 62} y={C - 28} width="124" height="56" rx="12" fill="#0F172A" />
        <text x={C} y={C - 4} textAnchor="middle" fontSize="13" fontWeight="600" fill="#fff">{CYCLE.agent.line1}</text>
        <text x={C} y={C + 14} textAnchor="middle" fontSize="11" fill="#CBD5E1">{CYCLE.agent.line2}</text>
      </g>
      {CYCLE.parts.map((p, i) => {
        const on = active === p.n;
        return (
          <g key={p.n} onClick={() => onSelect(p.n)} className="cursor-pointer">
            <circle cx={pos[i].x} cy={pos[i].y} r="24" fill={on ? "#0F172A" : "#fff"} stroke={on ? "#0F172A" : "#CBD5E1"} strokeWidth="1.25" />
            <text x={pos[i].x} y={pos[i].y + 5} textAnchor="middle" fontSize="14" fontWeight="600" fill={on ? "#fff" : "#0F172A"}>{p.n}</text>
          </g>
        );
      })}
      <text x={C - R - 4} y={C - R + 18} textAnchor="middle" fontSize="10" fill="#475569">next cycle</text>
    </svg>
  );
}
