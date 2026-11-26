import { growTrajectory } from "@/content/sampleDashboard";

/** Grow: one leader moving from below target to at target across the year, with a coach check-in. */
export default function DevelopmentArcVisual() {
  const W = 260, H = 104, pad = 18;
  const x = (i: number) => pad + (i * (W - pad * 2)) / (growTrajectory.length - 1);
  const y = (v: number) => H - pad - ((v - 1) / 3) * (H - pad * 2);
  const targetY = y(3);
  const path = growTrajectory.map((p, i) => `${i ? "L" : "M"}${x(i)},${y(p.score)}`).join(" ");
  return (
    <div data-sample className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <div className="flex items-center justify-between text-[11px] font-medium text-ink-2">
        <span className="text-amber-700">Below Target</span>
        <span className="text-blue-700">At Target</span>
      </div>
      <svg viewBox={`0 0 ${W} ${H}`} className="mt-1 w-full" role="img" aria-label="Sample leader moving from below target to at target between Q1 and Q4">
        <line x1={pad} x2={W - pad} y1={targetY} y2={targetY} stroke="#3B82F6" strokeDasharray="4 4" strokeWidth="1" />
        <path d={path} fill="none" stroke="#0F172A" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />
        {growTrajectory.map((p, i) => (
          <g key={p.q}>
            <circle cx={x(i)} cy={y(p.score)} r="3.5" fill={p.score >= 3 ? "#3B82F6" : "#F59E0B"} stroke="#fff" strokeWidth="1.5" />
            <text x={x(i)} y={H - 2} textAnchor="middle" fontSize="10" fill="#475569">{p.q}</text>
          </g>
        ))}
      </svg>
      <div className="mt-1 rounded-lg bg-canvas px-3 py-2 text-[12px] leading-snug text-ink">
        <span className="font-semibold">Coach:</span> You lead the Q3 board update. Want to plan the opening together?
      </div>
    </div>
  );
}
