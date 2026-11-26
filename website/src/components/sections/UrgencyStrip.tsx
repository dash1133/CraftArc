import { URGENCY } from "@/content/copy";

function Meter({ m }: { m: (typeof URGENCY.stats)[number]["meter"] }) {
  const color = m.tone === "risk" ? "bg-risk" : "bg-below";
  if (m.kind === "segments") {
    return (
      <div className="flex gap-1.5" aria-hidden="true">
        {Array.from({ length: m.total }).map((_, i) => (
          <span key={i} className={`h-1.5 flex-1 rounded-full ${i < m.filled ? color : "bg-slate-700"}`} />
        ))}
      </div>
    );
  }
  return (
    <div className="relative h-1.5 rounded-full bg-slate-700" aria-hidden="true">
      <span className={`absolute inset-y-0 left-0 rounded-full ${color}`} style={{ width: `${m.fill}%` }} />
      <span className="absolute -top-1.5 h-4.5 w-0.5 bg-slate-300" style={{ left: `${m.target}%` }} />
    </div>
  );
}

export default function UrgencyStrip() {
  return (
    <section id="why-now" aria-label={URGENCY.label} className="bg-ink text-white">
      <div className="mx-auto max-w-[1200px] px-5 py-12 sm:px-8 sm:py-14">
        <h2 className="sr-only">{URGENCY.label}</h2>
        <div className="grid divide-y divide-slate-800 md:grid-cols-3 md:divide-x md:divide-y-0">
          {URGENCY.stats.map((s) => (
            <div key={s.value} className="py-6 first:pt-0 last:pb-0 md:px-8 md:py-0 md:first:pl-0 md:last:pr-0">
              <p className="tabular font-serif text-5xl leading-none">{s.value}</p>
              <p className="mt-3 text-[15px] leading-snug text-slate-300">{s.text}</p>
              <div className="mt-4"><Meter m={s.meter} /></div>
              <a href={s.href} target="_blank" rel="noopener" className="mt-3 inline-block text-xs text-slate-400 underline decoration-slate-600 underline-offset-2 hover:text-white">{s.source}</a>
            </div>
          ))}
        </div>
        <p className="mt-6" data-placeholder><span className="ph-badge">{URGENCY.verifyNote}</span></p>
      </div>
    </section>
  );
}
