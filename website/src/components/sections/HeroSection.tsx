import { CTA, HERO } from "@/content/copy";
import { BriefingButton } from "../BriefingModal";
import HeroDemoVideo from "../visuals/HeroDemoVideo";
import WatchButton from "./WatchButton";

export default function HeroSection() {
  return (
    <section id="top" className="border-b border-slate-200 bg-gradient-to-b from-canvas to-white">
      <div className="mx-auto max-w-[1200px] px-5 pb-16 pt-14 sm:px-8 sm:pb-20 sm:pt-20">
        <div className="mx-auto max-w-[860px] text-center">
          <h1 className="font-serif text-[2.6rem] leading-[1.05] tracking-tight text-ink sm:text-6xl lg:text-[4.4rem]">{HERO.h1}</h1>
          <p className="mx-auto mt-5 max-w-[640px] text-xl text-ink-2 sm:text-2xl">{HERO.sub}</p>
          <p className="mx-auto mt-6 max-w-[680px] text-[17px] leading-relaxed text-ink">{HERO.resolution.join(" ")}</p>
          <div className="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row">
            <BriefingButton from="hero" className="h-12 w-full px-6 sm:w-auto">{CTA.primary}</BriefingButton>
            <WatchButton>{CTA.watch}</WatchButton>
          </div>
        </div>
        <div className="mx-auto mt-12 max-w-[1080px] sm:mt-14">
          <HeroDemoVideo />
        </div>
      </div>
    </section>
  );
}
