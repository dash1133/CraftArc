import { TRUST } from "@/content/copy";
import ArchitectureFlowSvg from "../visuals/ArchitectureFlowSvg";

export default function TrustGuardrailsSection() {
  return (
    <section id="trust" className="border-y border-slate-200 bg-canvas">
      <span id="faq" data-anchor aria-hidden="true" />
      <div className="mx-auto grid max-w-[1200px] items-center gap-12 px-5 py-20 sm:px-8 sm:py-24 lg:grid-cols-2">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.14em] text-ink-2">{TRUST.eyebrow}</p>
          <h2 className="mt-3 text-3xl font-semibold tracking-tight sm:text-4xl">{TRUST.h2}</h2>
          <dl className="mt-8 divide-y divide-slate-200 border-y border-slate-200">
            {TRUST.pillars.map((p) => (
              <div key={p.title} className="py-4">
                <dt className="font-semibold">{p.title}</dt>
                <dd className="mt-1 text-[15px] leading-relaxed text-ink-2">{p.body}</dd>
              </div>
            ))}
          </dl>
        </div>
        <div className="flex justify-center"><ArchitectureFlowSvg /></div>
      </div>
    </section>
  );
}
