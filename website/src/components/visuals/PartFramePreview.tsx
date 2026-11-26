import { CYCLE, STANDARD_WORD } from "@/content/copy";
import { benchDepth, frameworkTargets, LEVELS, leverProgress, targetScale } from "@/content/sampleDashboard";
import { Frame, Pill, SampleBadge, StackBar, Legend, StatusTag } from "./ui";

/** The product frame beside the cycle. It shows the part that is selected. */
export default function PartFramePreview({ part }: { part: number }) {
  const p = CYCLE.parts[part - 1];
  const titles = ["Leadership framework", "Evaluator brief", "Coach check-in", "Board pack summary"];
  return (
    <Frame title={`Part ${p.n}: ${titles[part - 1]}`} right={<SampleBadge />} className="min-h-[360px]">
      <div data-sample className="p-5 sm:p-6">
        {part === 1 && <Framework />}
        {part === 2 && <Assess />}
        {part === 3 && <Coach />}
        {part === 4 && <Depth />}
      </div>
    </Frame>
  );
}

function Framework() {
  return (
    <div className="overflow-x-auto">
      <p className="mb-3 text-sm text-ink-2">What {STANDARD_WORD.toLowerCase()} looks like: the target for each competency at each level</p>
      <table className="w-full min-w-[300px] text-xs sm:text-sm">
        <thead>
          <tr className="border-b border-slate-200 text-left text-xs text-ink-2">
            <th className="py-2 font-medium">Competency</th>
            {LEVELS.map((l) => <th key={l} className="py-2 text-center font-medium">{l}</th>)}
          </tr>
        </thead>
        <tbody>
          {frameworkTargets.map((c) => (
            <tr key={c.name} className={`border-b border-slate-100 ${c.emerging ? "bg-blue-50/60" : ""}`}>
              <td className="py-2 pr-2">
                {c.name}
                {c.emerging && <span className="ml-2 rounded bg-blue-100 px-1.5 py-0.5 text-[10px] font-semibold uppercase tracking-wide text-blue-700">Emerging</span>}
              </td>
              {c.targets.map((t, i) => (
                <td key={i} className="py-2 text-center">
                  <span className="inline-flex items-center gap-1 text-xs text-ink-2" title={targetScale[t]}>
                    {[1, 2, 3, 4].map((d) => <span key={d} className={`h-1.5 w-1.5 rounded-full ${d <= t ? "bg-ink" : "bg-slate-200"}`} />)}
                  </span>
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      <p className="mt-3 text-xs text-ink-2">3 levels, 7 competencies: 5 traditional and 2 emerging.</p>
    </div>
  );
}

function Assess() {
  const bars = [6, 14, 9, 18, 11, 22, 8, 16, 12, 20, 7, 15, 10, 19, 13, 9, 17, 6, 12, 15];
  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
      <div className="rounded-lg border border-slate-200 p-4">
        <p className="text-xs font-medium text-ink-2">360-degree dialogue, voice</p>
        <div className="mt-3 flex h-12 items-center gap-[3px]" aria-hidden="true">
          {bars.map((h, i) => <span key={i} className="w-1.5 rounded-full bg-slate-400" style={{ height: `${h * 2}px` }} />)}
        </div>
        <p className="tabular mt-3 text-xs text-ink-2">25 min, 3 colleagues</p>
      </div>
      <div className="rounded-lg border border-slate-200 p-4">
        <p className="text-xs font-medium text-ink-2">Evaluator brief, draft</p>
        <ul className="mt-2 space-y-2 text-[13px] leading-snug">
          <li><span className="mr-1 rounded bg-emerald-50 px-1.5 py-0.5 text-[10px] font-semibold text-emerald-700">Seen first-hand</span>Rebuilt the downside case before the vote.</li>
          <li><span className="mr-1 rounded bg-blue-50 px-1.5 py-0.5 text-[10px] font-semibold text-blue-700">Heard</span>Clients ask for her by name.</li>
        </ul>
        <p className="mt-3 text-xs font-medium text-ink">The evaluator decides.</p>
      </div>
    </div>
  );
}

function Coach() {
  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
      <div className="rounded-lg border border-slate-200 p-4">
        <p className="text-xs font-medium text-ink-2">Check-in, before Thursday</p>
        <p className="mt-2 text-sm leading-snug">Your investor meeting is on Thursday. The next role needs you to lead it. Want two minutes to plan your part?</p>
        <div className="mt-3 flex gap-2 text-xs"><span className="rounded-md bg-ink px-2.5 py-1 text-white">Plan it now</span><span className="rounded-md border border-slate-200 px-2.5 py-1">Later</span></div>
      </div>
      <div className="rounded-lg border border-slate-200 p-4">
        <p className="text-xs font-medium text-ink-2">Development plan, four levers</p>
        <div className="mt-3 space-y-2.5">
          {leverProgress.map((l) => (
            <div key={l.lever} className="text-xs">
              <div className="mb-1 flex justify-between"><span>{l.lever}</span><span className="tabular text-ink-2">{l.pct}%</span></div>
              <div className="h-1.5 rounded-full bg-slate-100"><div className="h-1.5 rounded-full bg-on" style={{ width: `${l.pct}%` }} /></div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function Depth() {
  return (
    <div>
      <div className="mb-3 flex items-center justify-between gap-3">
        <p className="text-sm text-ink-2">Bench depth by level</p>
        <StatusTag>In development</StatusTag>
      </div>
      <div className="space-y-3">
        {benchDepth.map((r) => (
          <div key={r.level}>
            <div className="mb-1 flex justify-between text-sm"><span className="font-medium">{r.level}</span><span className="tabular text-ink-2">{r.above + r.at + r.below} leaders</span></div>
            <StackBar below={r.below} at={r.at} above={r.above} />
          </div>
        ))}
      </div>
      <div className="mt-3"><Legend /></div>
      <div className="mt-4 flex flex-wrap items-center gap-2 text-sm">
        <Pill tone="above">Move up: 7</Pill>
        <Pill tone="risk">Move out: 2</Pill>
        <span className="ml-auto inline-flex items-center gap-1.5 rounded-md border border-dashed border-slate-300 px-2.5 py-1 text-xs text-ink-2">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" aria-hidden="true"><path d="M3 12a9 9 0 0 1 15-6.7L21 8M21 3v5h-5" /></svg>
          Update Part 1 targets
        </span>
      </div>
    </div>
  );
}
