"use client";

import { Play } from "lucide-react";

/** Opens the hero story lightbox (HeroDemoVideo listens for the event). */
export default function WatchButton({ children }: { children: React.ReactNode }) {
  return (
    <button
      type="button"
      data-cta="watch"
      onClick={() => window.dispatchEvent(new Event("craftarc:watch"))}
      className="inline-flex h-12 w-full items-center justify-center gap-2 rounded-lg border border-slate-300 bg-white px-6 text-[15px] font-semibold text-ink transition hover:border-ink sm:w-auto"
    >
      <Play size={16} strokeWidth={1.5} /> {children}
    </button>
  );
}
