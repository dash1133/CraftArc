import { DIFFERENCE } from "@/content/copy";

/** A thin review form, greyed out, beside a CraftArc dialogue that captures a specific, tagged example. */
export default function FormVsDialogueVisual() {
  return (
    <div data-sample className="grid grid-cols-1 gap-4 md:grid-cols-2">
      <div className="rounded-xl border border-slate-200 bg-canvas p-5 opacity-80 grayscale" aria-label="A typical review form">
        <p className="text-xs font-medium uppercase tracking-wide text-ink-2">{DIFFERENCE.formLabel}</p>
        {["Strategic focus", "Teamwork", "Communication", "Leadership"].map((q, i) => (
          <div key={q} className="mt-3 flex items-center justify-between gap-3 text-sm text-ink-2">
            <span>{q}</span>
            <span className="flex gap-1" aria-hidden="true">
              {[1, 2, 3, 4, 5].map((s) => <span key={s} className={`h-3.5 w-3.5 rounded-sm ${s <= [3, 4, 3, 3][i] ? "bg-slate-400" : "bg-slate-200"}`} />)}
            </span>
          </div>
        ))}
        <div className="mt-4 rounded-md border border-slate-200 bg-white p-3 text-sm italic text-slate-500">&ldquo;{DIFFERENCE.formComment}&rdquo;</div>
      </div>
      <div className="rounded-xl border border-slate-300 bg-white p-5 shadow-sm">
        <p className="text-xs font-medium uppercase tracking-wide text-ink">{DIFFERENCE.agentLabel}</p>
        <div className="mt-3 space-y-3 text-sm">
          {DIFFERENCE.dialogue.map((d) => (
            <div key={d.who} className={d.who === "Agent" ? "mr-6 rounded-lg bg-canvas p-3" : "ml-6 rounded-lg bg-ink p-3 text-white"}>
              <p className={`mb-0.5 text-[11px] font-semibold ${d.who === "Agent" ? "text-ink-2" : "text-slate-300"}`}>{d.who}</p>
              {d.text}
            </div>
          ))}
        </div>
        <p className="mt-3 inline-flex rounded-md bg-emerald-50 px-2 py-1 text-xs font-semibold text-emerald-700 ring-1 ring-inset ring-emerald-200">{DIFFERENCE.tag}</p>
      </div>
    </div>
  );
}
