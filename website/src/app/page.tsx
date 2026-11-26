import { BriefingProvider } from "@/components/BriefingModal";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import HeroSection from "@/components/sections/HeroSection";
import UrgencyStrip from "@/components/sections/UrgencyStrip";
import ThreePromisesSection from "@/components/sections/ThreePromisesSection";
import FourPartCycleSection from "@/components/sections/FourPartCycleSection";
import FormsVsConversationSection from "@/components/sections/FormsVsConversationSection";
import BoardDashboardSection from "@/components/sections/BoardDashboardSection";
import TrustGuardrailsSection from "@/components/sections/TrustGuardrailsSection";
import ProofAndSetupSection from "@/components/sections/ProofAndSetupSection";
import FinalCtaSection from "@/components/sections/FinalCtaSection";

/** The single-page executive narrative: nine sections, then the footer (unchanged). */
export default function Home() {
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
      <Footer />
    </BriefingProvider>
  );
}
