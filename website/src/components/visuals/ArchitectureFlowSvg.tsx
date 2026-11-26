import { TRUST } from "@/content/copy";

/** Agent to human decision to the client's HR system. People sit in the middle and make every call. */
export default function ArchitectureFlowSvg() {
  const boxes = TRUST.flow;
  return (
    <svg viewBox="0 0 360 400" className="w-full max-w-[420px]" role="img" aria-label="The CraftArc agent gathers evidence, people make every decision, and results feed the existing HR system">
      <defs>
        <marker id="flow-arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="8" markerHeight="8" orient="auto">
          <path d="M0,0 L10,5 L0,10 z" fill="#94A3B8" />
        </marker>
      </defs>
      {boxes.map((b, i) => {
        const y = 20 + i * 135;
        const human = i === 1;
        return (
          <g key={b.title}>
            <rect x="20" y={y} width="320" height="88" rx="12" fill={human ? "#0F172A" : "#fff"} stroke={human ? "#0F172A" : "#CBD5E1"} />
            <text x="180" y={y + 38} textAnchor="middle" fontSize="16" fontWeight="600" fill={human ? "#fff" : "#0F172A"}>{b.title}</text>
            <text x="180" y={y + 62} textAnchor="middle" fontSize="12.5" fill={human ? "#CBD5E1" : "#475569"}>{b.sub}</text>
            {i < boxes.length - 1 && <line x1="180" y1={y + 92} x2="180" y2={y + 128} stroke="#94A3B8" strokeWidth="1.5" markerEnd="url(#flow-arrow)" />}
          </g>
        );
      })}
    </svg>
  );
}
