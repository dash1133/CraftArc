import { CTA, FINAL } from "@/content/copy";
import { BriefingButton } from "../BriefingModal";

export default function FinalCtaSection() {
  return (
    <section id="final" className="bg-ink text-white">
      <div className="mx-auto max-w-[900px] px-5 py-20 text-center sm:px-8 sm:py-24">
        <h2 className="font-serif text-4xl leading-tight sm:text-5xl">{FINAL.h2}</h2>
        <p className="mx-auto mt-4 max-w-[560px] text-lg text-slate-300">{FINAL.sub}</p>
        <BriefingButton from="final" variant="light" className="mt-8 h-12 px-6">{CTA.final}</BriefingButton>
      </div>
    </section>
  );
}
