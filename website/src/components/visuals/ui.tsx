// Small shared pieces for the code-rendered visuals.

export const TONE = {
  above: { dot: "bg-above", text: "text-emerald-700", soft: "bg-emerald-50 text-emerald-700 ring-emerald-200", fill: "#10B981" },
  at: { dot: "bg-on", text: "text-blue-700", soft: "bg-blue-50 text-blue-700 ring-blue-200", fill: "#3B82F6" },
  below: { dot: "bg-below", text: "text-amber-700", soft: "bg-amber-50 text-amber-800 ring-amber-200", fill: "#F59E0B" },
  risk: { dot: "bg-risk", text: "text-red-700", soft: "bg-red-50 text-red-700 ring-red-200", fill: "#EF4444" },
} as const;
export type Tone = keyof typeof TONE;

export function Pill({ tone, children }: { tone: Tone; children: React.ReactNode }) {
  return (
    <span className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-medium ring-1 ring-inset ${TONE[tone].soft}`}>
      <span className={`h-1.5 w-1.5 rounded-full ${TONE[tone].dot}`} aria-hidden="true" />
      {children}
    </span>
  );
}

export function SampleBadge({ label = "Illustrative Sample Data" }: { label?: string }) {
  return (
    <span className="sample-badge inline-flex items-center gap-1.5 rounded-full border border-dashed border-slate-300 bg-white px-2.5 py-0.5 text-[11px] font-medium uppercase tracking-wide text-ink-2">
      {label}
    </span>
  );
}

export function StatusTag({ children }: { children: React.ReactNode }) {
  return <span className="inline-flex items-center rounded-full bg-amber-50 px-2 py-0.5 text-[11px] font-semibold text-amber-800 ring-1 ring-inset ring-amber-200">{children}</span>;
}

/** A crisp app shell: a thin title bar and a white body. */
export function Frame({ title, children, className = "", right }: { title?: string; children: React.ReactNode; className?: string; right?: React.ReactNode }) {
  return (
    <div className={`overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm ${className}`}>
      <div className="flex h-9 items-center gap-2 border-b border-slate-200 bg-canvas px-3">
        <span className="flex gap-1.5" aria-hidden="true">
          <span className="h-2 w-2 rounded-full bg-slate-300" /><span className="h-2 w-2 rounded-full bg-slate-300" /><span className="h-2 w-2 rounded-full bg-slate-300" />
        </span>
        {title && <span className="ml-2 truncate text-xs font-medium text-ink-2">{title}</span>}
        {right && <span className="ml-auto">{right}</span>}
      </div>
      <div>{children}</div>
    </div>
  );
}

/** A horizontal stacked bar of below / at / above shares. */
export function StackBar({ below, at, above, height = "h-2.5" }: { below: number; at: number; above: number; height?: string }) {
  const total = below + at + above || 1;
  return (
    <div className={`flex w-full overflow-hidden rounded-full bg-slate-100 ${height}`} aria-hidden="true">
      <span style={{ width: `${(below / total) * 100}%` }} className="bg-below" />
      <span style={{ width: `${(at / total) * 100}%` }} className="bg-on" />
      <span style={{ width: `${(above / total) * 100}%` }} className="bg-above" />
    </div>
  );
}

export function Legend() {
  return (
    <div className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-ink-2">
      <span className="inline-flex items-center gap-1.5"><span className="h-2 w-2 rounded-full bg-below" />Below target</span>
      <span className="inline-flex items-center gap-1.5"><span className="h-2 w-2 rounded-full bg-on" />At target</span>
      <span className="inline-flex items-center gap-1.5"><span className="h-2 w-2 rounded-full bg-above" />Above target</span>
    </div>
  );
}
