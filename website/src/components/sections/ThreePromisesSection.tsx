import { PROMISES } from "@/content/copy";
import EvidenceCardVisual from "../visuals/EvidenceCardVisual";
import DevelopmentArcVisual from "../visuals/DevelopmentArcVisual";
import TimeComparisonVisual from "../visuals/TimeComparisonVisual";

const VISUALS = { know: EvidenceCardVisual, grow: DevelopmentArcVisual, time: TimeComparisonVisual } as const;

export default function ThreePromisesSection() {
  return (
    <section id="promises" className="bg-white">
      <div className="mx-auto max-w-[1200px] px-5 py-20 sm:px-8 sm:py-24">
        <p className="text-xs font-semibold uppercase tracking-[0.14em] text-ink-2">{PROMISES.eyebrow}</p>
        <h2 className="mt-3 max-w-[720px] text-3xl font-semibold tracking-tight sm:text-4xl">{PROMISES.h2}</h2>
        <div className="mt-10 grid grid-cols-1 gap-6 lg:grid-cols-3">
          {PROMISES.cards.map((c) => {
            const V = VISUALS[c.id];
            return (
              <article key={c.id} id={`promise-${c.id}`} className="flex flex-col rounded-2xl border border-slate-200 bg-canvas p-5 sm:p-6">
                <V />
                <h3 className="mt-6 text-xl font-semibold tracking-tight">{c.title}</h3>
                <p className="mt-2 text-[15px] leading-relaxed text-ink">{c.summary}</p>
                <ul className="mt-4 space-y-2.5 border-t border-slate-200 pt-4">
                  {c.outcomes.map((o) => (
                    <li key={o} className="flex gap-2.5 text-[14.5px] leading-snug text-ink-2">
                      <svg className="mt-1 h-3.5 w-3.5 flex-none text-ink" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5" /></svg>
                      <span>{o}</span>
                    </li>
                  ))}
                </ul>
              </article>
            );
          })}
        </div>
      </div>
    </section>
  );
}
