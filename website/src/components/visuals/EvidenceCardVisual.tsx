import { Pill } from "./ui";

/** Know: one competency, its status, and the evidence behind it, tagged by source. */
export default function EvidenceCardVisual() {
  const chips = [
    { label: "Seen first-hand", n: 2, tone: "bg-emerald-50 text-emerald-700 ring-emerald-200" },
    { label: "Heard", n: 1, tone: "bg-blue-50 text-blue-700 ring-blue-200" },
    { label: "Self-assessment", n: 1, tone: "bg-slate-50 text-ink-2 ring-slate-200" },
  ];
  return (
    <div data-sample className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <div className="flex items-center justify-between gap-3">
        <p className="text-sm font-semibold">Strategic Judgment</p>
        <Pill tone="above">Above Target</Pill>
      </div>
      <div className="mt-3 h-1.5 rounded-full bg-slate-100" aria-hidden="true">
        <div className="relative h-1.5 w-[78%] rounded-full bg-above">
          <span className="absolute -top-1 left-[82%] h-3.5 w-0.5 bg-ink" title="Target" />
        </div>
      </div>
      <div className="mt-3 flex flex-wrap gap-1.5">
        {chips.map((c) => (
          <span key={c.label} className={`tabular inline-flex items-center rounded-md px-2 py-0.5 text-[11px] font-medium ring-1 ring-inset ${c.tone}`}>
            {c.label} ({c.n})
          </span>
        ))}
      </div>
    </div>
  );
}
