"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { ChevronLeft, ChevronRight, Pause, Play, RotateCcw, X } from "lucide-react";
import { HERO, STORY_BEATS } from "@/content/copy";
import { benchDepth, frameworkTargets, LEVELS, leverProgress, successorSlate } from "@/content/sampleDashboard";
import { Frame, Pill, SampleBadge, StackBar, Legend, TONE } from "./ui";

type Props = { src?: string; poster?: string; captionsSrc?: string };

/** Hero visual. Idle: a coded preview of the Leadership Depth & Risk View with a play pill.
 *  Active: a lightbox with the 60s film when `src` is set, or a 5-beat storyboard player until then. */
export default function HeroDemoVideo({ src, poster, captionsSrc }: Props) {
  const dlg = useRef<HTMLDialogElement>(null);
  const trigger = useRef<HTMLButtonElement>(null);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const d = dlg.current;
    if (!d) return;
    if (open && !d.open) d.showModal();
    if (!open && d.open) d.close();
  }, [open]);

  const close = useCallback(() => { setOpen(false); trigger.current?.focus(); }, []);

  useEffect(() => {
    const onWatch = () => setOpen(true);
    window.addEventListener("craftarc:watch", onWatch);
    return () => window.removeEventListener("craftarc:watch", onWatch);
  }, []);

  return (
    <div id="video" data-anchor className="relative">
      <Frame title={HERO.previewTitle} right={<SampleBadge />} className="shadow-xl">
        <div data-sample className="relative">
          <DepthPreview />
          <div className="absolute inset-0 flex items-center justify-center bg-[radial-gradient(ellipse_at_center,rgba(255,255,255,0.92)_0%,rgba(255,255,255,0.55)_28%,rgba(255,255,255,0)_60%)]">
            <button
              ref={trigger}
              type="button"
              data-cta="watch-pill"
              onClick={() => setOpen(true)}
              className="group inline-flex items-center gap-3 rounded-full bg-ink py-3 pl-3 pr-5 text-[15px] font-semibold text-white shadow-2xl ring-1 ring-white/20 transition hover:bg-slate-800"
            >
              <span className="grid h-9 w-9 place-items-center rounded-full bg-white text-ink"><Play size={16} strokeWidth={1.5} fill="currentColor" /></span>
              {HERO.playPill} <span className="tabular font-normal text-slate-300">{HERO.playLength}</span>
            </button>
          </div>
        </div>
      </Frame>
      <p className="mt-2 text-center" data-placeholder={src ? undefined : ""}>
        <span className="ph-badge">{HERO.placeholderNote}</span>
      </p>

      {/* Text alternative for the story, for screen readers and the copy checks. */}
      <ol className="sr-only">
        {STORY_BEATS.map((b) => <li key={b.title}>{b.title}. {b.line}</li>)}
      </ol>

      <dialog
        ref={dlg}
        id="story"
        aria-modal="true"
        aria-label="CraftArc in 60 seconds"
        onCancel={(e) => { e.preventDefault(); close(); }}
        onClick={(e) => { if (e.target === dlg.current) close(); }}
        className="w-[min(1080px,calc(100vw-24px))] overflow-hidden rounded-2xl bg-ink p-0 text-white shadow-2xl"
      >
        <button type="button" onClick={close} aria-label="Close" className="absolute right-3 top-3 z-10 rounded-full bg-white/10 p-2 text-white hover:bg-white/20">
          <X size={18} strokeWidth={1.5} />
        </button>
        {open && (src
          ? (
            <video controls autoPlay playsInline poster={poster} className="aspect-video w-full bg-black">
              <source src={src} type="video/mp4" />
              {captionsSrc && <track kind="captions" src={captionsSrc} srcLang="en" label="English" default />}
            </video>
          )
          : <Storyboard />)}
      </dialog>
    </div>
  );
}

function DepthPreview() {
  return (
    <div className="grid grid-cols-1 gap-4 p-4 sm:grid-cols-5 sm:gap-6 sm:p-6">
      <div className="sm:col-span-3">
        <p className="text-xs font-medium uppercase tracking-wide text-ink-2">Bench depth by level</p>
        <div className="mt-3 space-y-3">
          {benchDepth.map((r) => {
            const total = r.above + r.at + r.below;
            return (
              <div key={r.level}>
                <div className="mb-1 flex justify-between text-sm">
                  <span className="font-medium">{r.level}</span>
                  <span className="tabular text-ink-2">{Math.round((r.below / total) * 100)}% below</span>
                </div>
                <StackBar below={r.below} at={r.at} above={r.above} />
              </div>
            );
          })}
        </div>
        <div className="mt-3 hidden sm:block"><Legend /></div>
      </div>
      <div className="hidden space-y-3 sm:col-span-2 sm:block">
        <p className="text-xs font-medium uppercase tracking-wide text-ink-2">Risk callouts</p>
        {HERO.previewCallouts.map((c) => (
          <div key={c.label} className="rounded-lg border border-slate-200 p-3">
            <p className="text-xs text-ink-2">{c.label}</p>
            <p className={`tabular mt-0.5 text-lg font-semibold ${TONE[c.tone as "risk" | "below"].text}`}>{c.value}</p>
          </div>
        ))}
      </div>
      <div className="hidden sm:col-span-5 sm:block">
        <p className="text-xs font-medium uppercase tracking-wide text-ink-2">Slate of successors, key roles</p>
        <table className="tabular mt-2 w-full text-sm">
          <thead>
            <tr className="border-b border-slate-200 text-left text-xs text-ink-2">
              <th className="py-1.5 font-medium">Role</th>
              <th className="py-1.5 text-center font-medium">Ready now</th>
              <th className="py-1.5 text-center font-medium">Ready in 3 years</th>
              <th className="py-1.5 text-center font-medium">Ready in 5 to 7 years</th>
            </tr>
          </thead>
          <tbody>
            {successorSlate.map((r) => (
              <tr key={r.role} className="border-b border-slate-100">
                <td className="py-1.5">{r.role}</td>
                <td className={`py-1.5 text-center font-semibold ${r.now === 0 ? "text-red-700" : "text-emerald-700"}`}>{r.now}</td>
                <td className="py-1.5 text-center">{r.three}</td>
                <td className="py-1.5 text-center">{r.fiveToSeven}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const BEAT_MS = 12000; // 5 beats x 12 s = 60 s

function Storyboard() {
  const ms = (typeof window !== "undefined" && (window as unknown as { __craftarcBeatMs?: number }).__craftarcBeatMs) || BEAT_MS;
  const total = ms * STORY_BEATS.length;
  const [t, setT] = useState(0); // time into the story, in ms
  const [playing, setPlaying] = useState(true);
  const ended = t >= total;
  const beat = Math.min(STORY_BEATS.length - 1, Math.floor(t / ms));
  const elapsed = ended ? ms : t - beat * ms;

  useEffect(() => {
    if (!playing || ended) return;
    const id = setInterval(() => setT((x) => Math.min(total, x + 100)), 100);
    return () => clearInterval(id);
  }, [playing, ended, total]);

  const go = (n: number) => setT(Math.max(0, Math.min(STORY_BEATS.length - 1, n)) * ms);
  const b = STORY_BEATS[beat];

  return (
    <div data-sample className="flex flex-col" data-beat={beat}>
      <div className="grid aspect-video grid-cols-1 items-center gap-6 bg-gradient-to-br from-slate-900 to-slate-800 p-6 sm:grid-cols-2 sm:p-10">
        <div>
          <p className="tabular text-xs font-medium uppercase tracking-[0.18em] text-slate-400">Beat {beat + 1} of {STORY_BEATS.length}</p>
          <h3 className="mt-3 font-serif text-3xl leading-tight sm:text-5xl" id="story-title">{b.title}</h3>
          <p className="mt-4 max-w-md text-base text-slate-300 sm:text-lg">{b.line}</p>
        </div>
        <div className="hidden sm:block"><Scene beat={beat} /></div>
      </div>
      <div className="flex items-center gap-3 border-t border-white/10 px-4 py-3">
        <button type="button" onClick={() => go(beat - 1)} aria-label="Previous beat" className="rounded p-1.5 hover:bg-white/10"><ChevronLeft size={18} strokeWidth={1.5} /></button>
        {ended ? (
          <button type="button" onClick={() => { go(0); setPlaying(true); }} aria-label="Replay" className="rounded p-1.5 hover:bg-white/10"><RotateCcw size={18} strokeWidth={1.5} /></button>
        ) : (
          <button type="button" onClick={() => setPlaying((p) => !p)} aria-label={playing ? "Pause" : "Play"} className="rounded p-1.5 hover:bg-white/10">
            {playing ? <Pause size={18} strokeWidth={1.5} /> : <Play size={18} strokeWidth={1.5} />}
          </button>
        )}
        <button type="button" onClick={() => go(beat + 1)} aria-label="Next beat" className="rounded p-1.5 hover:bg-white/10"><ChevronRight size={18} strokeWidth={1.5} /></button>
        <div className="flex flex-1 gap-1.5" role="tablist" aria-label="Story beats">
          {STORY_BEATS.map((s, i) => (
            <button key={s.title} type="button" role="tab" aria-selected={i === beat} aria-label={s.title} onClick={() => go(i)} className="h-1.5 flex-1 overflow-hidden rounded-full bg-white/15">
              <span className="block h-full bg-white" style={{ width: i < beat ? "100%" : i === beat ? `${Math.min(100, (elapsed / ms) * 100)}%` : "0%" }} />
            </button>
          ))}
        </div>
        <span className="tabular w-12 text-right text-xs text-slate-400">{formatTime(beat * ms + elapsed, ms)}</span>
      </div>
    </div>
  );
}

function formatTime(t: number, ms: number) {
  const s = Math.min(60, Math.round((t / (ms * STORY_BEATS.length)) * 60));
  return `0:${String(s).padStart(2, "0")}`;
}

function Scene({ beat }: { beat: number }) {
  const card = "rounded-xl bg-white p-5 text-ink shadow-2xl";
  if (beat === 0) {
    return (
      <div className={card}>
        <p className="text-xs font-medium uppercase tracking-wide text-ink-2">Below target, by level</p>
        <div className="mt-3 space-y-3">
          {[["Principals", 18], ["MDs", 0], ["Partners", 56]].map(([l, v]) => (
            <div key={l as string}>
              <div className="mb-1 flex justify-between text-sm"><span>{l}</span><span className="tabular font-semibold">{v}%</span></div>
              <div className="h-2 rounded-full bg-slate-100"><div className={`h-2 rounded-full ${Number(v) > 40 ? "bg-risk" : "bg-below"}`} style={{ width: `${v}%` }} /></div>
            </div>
          ))}
        </div>
      </div>
    );
  }
  if (beat === 1) {
    return (
      <div className={card}>
        <p className="text-xs font-medium uppercase tracking-wide text-ink-2">Target by level</p>
        <table className="mt-3 w-full text-sm">
          <thead><tr className="text-left text-xs text-ink-2"><th className="pb-1 font-medium">Competency</th>{LEVELS.map((l) => <th key={l} className="pb-1 text-center font-medium">{l}</th>)}</tr></thead>
          <tbody>
            {frameworkTargets.slice(0, 4).concat(frameworkTargets.slice(5, 6)).map((c) => (
              <tr key={c.name} className="border-t border-slate-100"><td className="py-1.5">{c.name}</td>{c.targets.map((t, i) => <td key={i} className="tabular text-center">{t}</td>)}</tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }
  if (beat === 2) {
    return (
      <div className={`${card} space-y-3 text-sm`}>
        <p className="rounded-lg bg-canvas p-3">What did you see first-hand when the plan was challenged?</p>
        <p className="ml-8 rounded-lg bg-slate-900 p-3 text-white">She rebuilt the downside case overnight and brought it back.</p>
        <div className="flex gap-2"><Pill tone="above">Seen first-hand</Pill><Pill tone="at">Heard</Pill></div>
      </div>
    );
  }
  if (beat === 3) {
    return (
      <div className={card}>
        <p className="text-sm">Ahead of Thursday&apos;s investor meeting: want two minutes to plan your part?</p>
        <div className="mt-4 space-y-2">
          {leverProgress.map((l) => (
            <div key={l.lever} className="text-xs">
              <div className="mb-1 flex justify-between"><span>{l.lever}</span><span className="tabular">{l.pct}%</span></div>
              <div className="h-1.5 rounded-full bg-slate-100"><div className="h-1.5 rounded-full bg-on" style={{ width: `${l.pct}%` }} /></div>
            </div>
          ))}
        </div>
      </div>
    );
  }
  return (
    <div className={card}>
      <p className="text-xs font-medium uppercase tracking-wide text-ink-2">Bench depth</p>
      <div className="mt-3 space-y-3">
        {benchDepth.map((r) => (
          <div key={r.level}><p className="mb-1 text-sm">{r.level}</p><StackBar below={r.below} at={r.at} above={r.above} /></div>
        ))}
      </div>
      <div className="mt-4 flex gap-2"><Pill tone="above">Move up</Pill><Pill tone="risk">Move out</Pill></div>
    </div>
  );
}
