"use client";

import { useRef, useState } from "react";
import { CYCLE } from "@/content/copy";
import CycleDiagramSvg from "../visuals/CycleDiagramSvg";
import PartFramePreview from "../visuals/PartFramePreview";
import { StatusTag } from "../visuals/ui";

export default function FourPartCycleSection() {
  const [active, setActive] = useState(1);
  const tabs = useRef<(HTMLButtonElement | null)[]>([]);

  const onKey = (e: React.KeyboardEvent, i: number) => {
    const n = CYCLE.parts.length;
    let next = -1;
    if (e.key === "ArrowDown" || e.key === "ArrowRight") next = (i + 1) % n;
    if (e.key === "ArrowUp" || e.key === "ArrowLeft") next = (i - 1 + n) % n;
    if (e.key === "Home") next = 0;
    if (e.key === "End") next = n - 1;
    if (next >= 0) { e.preventDefault(); setActive(next + 1); tabs.current[next]?.focus(); }
  };

  return (
    <section id="how" className="border-y border-slate-200 bg-canvas">
      <div className="mx-auto max-w-[1200px] px-5 py-20 sm:px-8 sm:py-24">
        <p className="text-xs font-semibold uppercase tracking-[0.14em] text-ink-2">{CYCLE.eyebrow}</p>
        <h2 className="mt-3 max-w-[720px] text-3xl font-semibold tracking-tight sm:text-4xl">{CYCLE.h2}</h2>
        <p className="mt-3 max-w-[640px] text-ink-2">{CYCLE.lede}</p>
        <div className="mt-10 grid grid-cols-1 gap-10 lg:grid-cols-12">
          <div className="min-w-0 lg:col-span-5">
            <CycleDiagramSvg active={active} onSelect={setActive} />
            <div role="tablist" aria-label="The four parts" aria-orientation="vertical" className="mt-6 space-y-2">
              {CYCLE.parts.map((p, i) => {
                const on = active === p.n;
                return (
                  <button
                    key={p.n}
                    id={p.anchor}
                    data-anchor
                    ref={(el) => { tabs.current[i] = el; }}
                    type="button"
                    role="tab"
                    aria-selected={on}
                    aria-controls="part-panel"
                    tabIndex={on ? 0 : -1}
                    onClick={() => setActive(p.n)}
                    onKeyDown={(e) => onKey(e, i)}
                    className={`block w-full rounded-xl border p-4 text-left transition ${on ? "border-ink bg-white shadow-sm" : "border-transparent hover:border-slate-200 hover:bg-white"}`}
                  >
                    <span className="flex items-center gap-2">
                      <span className="tabular text-xs font-semibold text-ink-2">Part {p.n}</span>
                      {"status" in p && <StatusTag>{p.status}</StatusTag>}
                    </span>
                    <span className="mt-1 block font-semibold">{p.title}</span>
                    <span className={`mt-1 block text-[14.5px] leading-snug text-ink-2 ${on ? "" : "hidden lg:block lg:line-clamp-1"}`}>{p.body}</span>
                  </button>
                );
              })}
            </div>
          </div>
          <div id="part-panel" role="tabpanel" aria-label={CYCLE.parts[active - 1].title} className="min-w-0 lg:col-span-7 lg:sticky lg:top-24 lg:self-start">
            <PartFramePreview part={active} />
          </div>
        </div>
      </div>
    </section>
  );
}
