import { CTA, NAV } from "@/content/copy";
import { BriefingButton } from "./BriefingModal";

export default function Navbar() {
  return (
    <header className="sticky top-0 z-40 border-b border-slate-200 bg-white/85 backdrop-blur">
      <div className="mx-auto flex h-16 max-w-[1200px] items-center gap-6 px-5 sm:px-8">
        <a href="#top" className="flex items-center gap-3" aria-label="CraftArc home">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src="/assets/img/logo-mark.svg" alt="" width={32} height={32} />
          <span className="wordmark hidden sm:inline"><span className="w-craft">CRAFT</span> <span className="w-arc">ARC</span></span>
        </a>
        <nav aria-label="Main" className="mx-auto hidden items-center gap-8 md:flex">
          {NAV.map((n) => (
            <a key={n.href} href={n.href} className="text-[15px] font-medium text-ink-2 transition hover:text-ink">{n.label}</a>
          ))}
        </nav>
        <BriefingButton from="header" className="ml-auto md:ml-0 h-10">{CTA.primary}</BriefingButton>
      </div>
    </header>
  );
}
