import { SETUP } from "@/content/copy";

export default function ProofAndSetupSection() {
  return (
    <section id="setup" className="bg-white">
      <div className="mx-auto max-w-[1200px] px-5 py-20 sm:px-8 sm:py-24">
        <p className="text-xs font-semibold uppercase tracking-[0.14em] text-ink-2">{SETUP.eyebrow}</p>
        <h2 className="mt-3 text-3xl font-semibold tracking-tight sm:text-4xl">{SETUP.h2}</h2>
        <div className="mt-10 grid grid-cols-1 gap-6 md:grid-cols-2">
          {[SETUP.proof, SETUP.setup].map((c) => (
            <article key={c.title} className="rounded-2xl border border-slate-200 p-6 sm:p-8">
              <h3 className="text-xl font-semibold tracking-tight">{c.title}</h3>
              <p className="mt-3 leading-relaxed text-ink-2">{c.body}</p>
            </article>
          ))}
        </div>
        <ol className="mt-10 grid grid-cols-1 gap-4 md:grid-cols-3" aria-label="How setup works">
          {SETUP.steps.map((s, i) => (
            <li key={s} className="relative flex items-center gap-4 rounded-xl border border-slate-200 bg-canvas p-5">
              <span className="tabular font-serif text-3xl text-ink-2">{`0${i + 1}`}</span>
              <span className="font-semibold">{s}</span>
              {i < SETUP.steps.length - 1 && (
                <svg className="absolute -right-4 top-1/2 z-10 hidden h-4 w-4 -translate-y-1/2 text-slate-400 md:block" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" /></svg>
              )}
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}
