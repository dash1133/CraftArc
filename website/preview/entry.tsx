// The preview build: the same page components, copy and styles as the live site, rendered in the browser
// into one self-contained HTML file for a claude.ai Artifact (scripts/build_preview.mjs). Mirrors src/app/page.tsx.
import { createRoot } from "react-dom/client";
import { BriefingProvider } from "@/components/BriefingModal";
import Navbar from "@/components/Navbar";
import HeroSection from "@/components/sections/HeroSection";
import UrgencyStrip from "@/components/sections/UrgencyStrip";
import ThreePromisesSection from "@/components/sections/ThreePromisesSection";
import FourPartCycleSection from "@/components/sections/FourPartCycleSection";
import FormsVsConversationSection from "@/components/sections/FormsVsConversationSection";
import BoardDashboardSection from "@/components/sections/BoardDashboardSection";
import TrustGuardrailsSection from "@/components/sections/TrustGuardrailsSection";
import ProofAndSetupSection from "@/components/sections/ProofAndSetupSection";
import FinalCtaSection from "@/components/sections/FinalCtaSection";
import { FOOTER_HTML } from "@/content/footer";

// The footer is the live footer. Only its links to other pages are pointed at the matching part of
// this single page, because the preview has no other pages.
const PREVIEW_FOOTER = FOOTER_HTML
  .replace(/href="index\.html#/g, 'href="#')
  .replace(/href="about\.html"/g, 'href="#setup"')
  .replace(/href="book-a-demo\.html"/g, 'href="#final"')
  .replace(/href="private-equity\.html#video"/g, 'href="#video"');

function Preview() {
  return (
    <BriefingProvider>
      <a className="skip" href="#main">Skip to content</a>
      <Navbar />
      <main id="main">
        <HeroSection />
        <UrgencyStrip />
        <ThreePromisesSection />
        <FourPartCycleSection />
        <FormsVsConversationSection />
        <BoardDashboardSection />
        <TrustGuardrailsSection />
        <ProofAndSetupSection />
        <FinalCtaSection />
      </main>
      <div className="contents" dangerouslySetInnerHTML={{ __html: PREVIEW_FOOTER }} />
    </BriefingProvider>
  );
}

createRoot(document.getElementById("craftarc-root")!).render(<Preview />);
