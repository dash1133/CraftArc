# CLAUDE.md — CraftArc Marketing Website Build Instructions

> Saved verbatim from Dash's message of 26 Nov 2026, with this note added. Dash's overrides on the same day:
> "remove all visuals" (no photos, screenshots or video on the site; every visual is drawn in code) and
> "Don't change the footer no matter what the instruction says" (the site keeps its existing AgenticPM-style
> footer, not the minimal footer described in Section 9). How the build follows and departs from this
> document is recorded in `website/CHANGELOG.md` (issue 013) and `docs/Claims_Ledger.md`.

## 1. Project Overview
Build the marketing website for **CraftArc**, an AI-powered leadership assessment, continuous coaching, and succession-readiness platform built for **CEOs, executive committees, and boards** (not HR).

### Core Design Mandate: "Let the Picture Tell the Story"
- **Zero stock photography.** Do not use generic office photos, smiling headshots, or AI sparkle illustrations.
- **Visual-first architecture.** Every section must pair concise executive copy (1–2 sentences max per block) with a live, code-rendered visual (interactive UI mockups, data charts, or clean inline SVGs) that demonstrates the product directly.
- **Executive aesthetic.** Style like a modern executive briefing tool (Stripe, Linear, McKinsey Digital)—high contrast, disciplined whitespace, crisp 1px borders, tabular numerals (`tabular-nums`), and zero visual clutter.

---

## 2. Tech Stack & Conventions
- **Framework:** Next.js 15+ (App Router) with TypeScript (`strict: true`)
- **Styling:** Tailwind CSS v4 (or v3 with `tailwind.config.ts`)
- **Charts:** `recharts` for Section 6 interactive dashboard visualizations
- **Icons:** `lucide-react` (thin stroke `1.5`, restrained usage)
- **Fonts:** `Inter` (UI/body) + `Newsreader` or `Instrument Serif` (optional editorial accent for H1/pull-quotes) via `next/font/google`
- **No external image dependencies.** All diagrams, UI previews, and charts must be self-contained React/SVG/Recharts components so the app renders completely on day one.

### Design Tokens
- **Canvas Light:** `#F8FAFC` / `#FFFFFF`
- **Dark Band / Primary Ink:** `#0F172A`
- **Secondary Ink:** `#475569`
- **Borders:** `#E2E8F0`
- **Semantic Status Colors (strictly reserved for leadership data):**
  - Above Target / Ready Now: `#10B981` (Emerald)
  - At Target / On Track: `#3B82F6` (Slate Blue)
  - Below Target / Risk / Action Needed: `#F59E0B` (Amber) and `#EF4444` (Coral/Red)

---

## 3. Compliance & Copy Guardrails (STRICT)
1. **Centralized Copy Config:** Put all marketing copy, headlines, and sample dashboard numbers in `src/content/copy.ts` and `src/content/sampleDashboard.ts`.
2. **Configurable Wording Constant:** Define `export const STANDARD_WORD = "Great";` (toggleable to `"Good"`) in `src/content/copy.ts` and interpolate it everywhere "What Great/Good Looks Like" appears.
3. **Never name the first client:** Refer only to "live in production at a private equity firm." Do not include any firm name or mention any client DIY/ChatGPT attempt.
4. **Never imply AI makes employment decisions:** Frame the AI agent strictly as holding conversations, gathering/tagging evidence, drafting assessments, and coaching. Always reinforce that **human evaluators and boards make every promotion, succession, and exit call**.
5. **Label sample data explicitly:** All charts and insights in Section 6 must display a clear `Illustrative Sample Data` badge.
6. **Do not organize by industry:** The site speaks to CEOs and business leaders across all industries.

---

## 4. Directory Structure
```text
src/
├── app/
│   ├── layout.tsx              # Fonts, metadata, smooth scroll
│   ├── page.tsx                # Single-page executive narrative composing all 9 sections
│   └── globals.css             # Tailwind directives + custom utility classes
├── content/
│   ├── copy.ts                 # All headlines, copy, CTAs, STANDARD_WORD config
│   └── sampleDashboard.ts      # Structured mock data for the 5-tab Board View
└── components/
    ├── Navbar.tsx              # Sticky minimal header: Logo, 4 anchor links, "Book a Briefing" CTA
    ├── BriefingModal.tsx       # Accessible modal form triggered by any primary CTA
    ├── sections/
    │   ├── HeroSection.tsx
    │   ├── UrgencyStrip.tsx
    │   ├── ThreePromisesSection.tsx
    │   ├── FourPartCycleSection.tsx
    │   ├── FormsVsConversationSection.tsx
    │   ├── BoardDashboardSection.tsx
    │   ├── TrustGuardrailsSection.tsx
    │   ├── ProofAndSetupSection.tsx
    │   └── FinalCtaSection.tsx
    └── visuals/
        ├── HeroDemoVideo.tsx           # 60s video player + interactive poster fallback + lightbox
        ├── EvidenceCardVisual.tsx      # Micro-visual for "Know"
        ├── DevelopmentArcVisual.tsx    # Micro-visual for "Grow"
        ├── TimeComparisonVisual.tsx    # Micro-visual for "Without the Time"
        ├── CycleDiagramSvg.tsx         # Interactive 4-part circular SVG orbiting "1 AI Agent"
        ├── PartFramePreview.tsx        # Dynamic UI preview switching for Parts 1–4
        ├── FormVsDialogueVisual.tsx    # Side-by-side survey vs. CraftArc dialogue UI
        └── ArchitectureFlowSvg.tsx     # Agent -> Human Decision -> HRIS diagram
```

## 5. Section-by-Section Specification

### Navigation (`Navbar.tsx`)
* Sticky translucent white bar (`backdrop-blur`, `border-b border-slate-200`).
* Left: CraftArc wordmark.
* Center: Anchor links (`How It Works`, `Board View`, `Trust`, `Setup`).
* Right: `Book a Briefing` button (dark slate `#0F172A`, white text).

### Section 1: Hero (`HeroSection.tsx` + `HeroDemoVideo.tsx`)
* Layout: Stacked centered copy block above a full-width 16:9 widescreen video container (`max-w-[1080px] mx-auto`).
* Copy:
   * H1: `Can you tell if your company has a gap in leadership depth?`
   * Sub-question (immediately beneath H1, muted slate `#475569`): `What are the risks associated with your current leadership profile?`
   * Resolution Line: `CraftArc answers both—with evidence, not opinion. Know where every leader stands, spot where your bench is thin, and keep every leader growing toward their next role without blocking days of leadership time.`
   * CTAs: Primary `Book a Briefing` (opens modal) | Secondary `▶ Watch the 60s Story` (triggers video playback).
* Visual (`HeroDemoVideo.tsx`):
   * Accepts optional props: `src?: string`, `poster?: string`, `captionsSrc?: string`.
   * Idle State: Framed 16:9 executive browser/app shell (`border border-slate-200 shadow-xl rounded-xl`) displaying a crisp coded preview of the Leadership Depth & Risk View (showing risk callouts: Partner layer 56% below target on emerging competencies; 5 leaders below target 3+ years) overlaid with a centered high-contrast play pill: `▶ Watch the 60s Story (1:00)`.
   * Active State: Clicking play opens a distraction-free lightbox modal (`Esc` to close, backdrop click to close). If `src` is provided, render `<video controls autoPlay playsInline>` with `<track kind="captions" default />`. If `src` is not yet provided, render an interactive 5-beat storyboard player (auto-advancing 60s preview of the 5 product beats: The Gap -> Define Standard -> AI 360 Dialogue -> Continuous Coaching -> Board Depth View) so the demo feels functional immediately.

### Section 2: The Urgency Strip (`UrgencyStrip.tsx`)
* Layout: Full-width dark slate band (`#0F172A`), 3 equal columns with thin vertical dividers (`border-slate-800`).
* Content & Micro-Visuals:
   1. `1 in 4` — CEO successions are unprepared (Korn Ferry) — subtle 4-segment indicator bar with 1 segment highlighted coral.
   2. `17%` — of boards review succession plans quarterly, though 60% say it should be continuous (Korn Ferry) — thin horizontal bar showing 17% fill vs. a 60% target tick mark.
   3. `1/3+` — of US companies lack a CEO with the capabilities needed in the near term (Heidrick & Struggles) — 3-segment indicator bar with 1+ highlighted amber.

### Section 3: The Three Promises (`ThreePromisesSection.tsx`)
* Layout: 3-column bento grid (`grid-cols-1 lg:grid-cols-3 gap-6`). Each card has a coded micro-visual at the top, followed by the promise title, 1-line summary, and 3 concise outcome bullets.
* Cards:
   1. Know — See how close every leader is to each key role, based on evidence, not opinion.
      * Outcomes: A slate of successors for every key role (ready now, in 3 years, in 5–7 years); fair calls on who should move up or move out based on what colleagues actually saw; one clear standard at each leadership level.
      * Visual (`EvidenceCardVisual.tsx`): UI card showing `Strategic Judgment` with emerald pill `Above Target` and 3 linked source chips: `Seen first-hand (2)`, `Heard (1)`, `Self-assessment (1)`.
   2. Grow — Grow a slate of successors measured against the standard, not against each other.
      * Outcomes: Your best people know exactly what to work on to reach the next role; off-track leaders find out early while there is time to change; everyone on the slate keeps moving forward all year.
      * Visual (`DevelopmentArcVisual.tsx`): Mini SVG trajectory sparkline moving from `Below Target` -> `At Target` across Q1–Q4 with an inline coach check-in bubble.
   3. Without the Time — Run the way the best firms grow their leaders, without blocking days of leadership time.
      * Outcomes: Leaders spend time on meaningful dialogue, not chasing feedback; review season stops taking over calendars; up and running before your next review cycle.
      * Visual (`TimeComparisonVisual.tsx`): Compact visual comparing a crowded red-blocked week ("Traditional Review Season") against a clean week with one 25-minute voice/text pill ("CraftArc Agent").

### Section 4: The Four-Part Cycle (`FourPartCycleSection.tsx`)
* Layout: Interactive 2-column split (`lg:grid-cols-12`). Left (`col-span-5`): interactive circular SVG cycle diagram (`CycleDiagramSvg.tsx`) + clickable step list. Right (`col-span-7`): dynamic product frame (`PartFramePreview.tsx`) that transitions smoothly based on the active step (default: Part 1).
* Diagram: 4 nodes arranged in a continuous loop (Part 4 arrow pointing back to Part 1) orbiting a central badge: `1 AI Agent (Voice or Text)`.
* Steps & Right-Side UI Previews:
   1. Part 1 — Define What {STANDARD_WORD} Looks Like: Write down what {STANDARD_WORD.toLowerCase()} looks like at each level, tied to what the business needs next.
      * Preview: Clean matrix of 3 Levels (Principal, MD, Partner) × 7 Competencies (5 Traditional + 2 Emerging highlighted, e.g., AI Fluency) showing target thresholds per level.
   2. Part 2 — Assess Leaders and Set Development Plans: The agent holds 360-degree dialogues, tags every fact by source, and drafts an evidence-backed view. The evaluator decides.
      * Preview: Split mini-UI showing a 25-min voice/text dialogue waveform on the left transforming into a structured Evaluator Brief on the right with `[Seen first-hand]` and `[Heard]` tags.
   3. Part 3 — Execute to Plan: A just-in-time coach that keeps the plan alive all year—never nagging, always tied to the experiences the next role needs.
      * Preview: Coach check-in card prompting a leader ahead of an investor meeting + a 4-lever development progress indicator (Mentoring, Non-traditional, On-the-job, Formal training).
   4. Part 4 — Assess Gaps in Leadership Depth: A live portfolio of your bench—where it is deep, where it is thin, and who should move up or move out.
      * Preview: Mini Board Pack summary showing bench depth by level and an arrow looping back to "Update Part 1 Targets."

### Section 5: Forms vs. Conversation (`FormsVsConversationSection.tsx`)
* Headline: `Other tools collect forms. CraftArc holds the conversation.`
* Subtext: `Built on the impartial evaluator method of leading management consulting firms—delivered without blocking days of senior time.`
* Visual (`FormVsDialogueVisual.tsx`): Side-by-side UI contrast:
   * Left (Muted/Grayed — Review Form): Cluttered 1–5 star rating form with thin generic text: "Great team player, needs more strategic focus."
   * Right (Crisp/Active — CraftArc Agent): Clean 25-minute dialogue snippet where the agent asks one sharp follow-up question, captures a specific behavioral example, and tags it `[Observed first-hand — Q3 Deal Committee]`.
* Compact Comparison Table underneath: 6 rows comparing `Review Form` vs. `CraftArc Agent` across: Feedback gathering, What it captures, The framework, Who writes it up, How it ends, Between reviews.

### Section 6: What the Board Sees (`BoardDashboardSection.tsx`)
* Header: `A live portfolio of your leadership bench.` + prominent subtle pill badge `Illustrative Sample Data`.
* Top Key Insights Banner (Plain English): "The firm is building depth at Principal and MD level. The real risk is the Partner layer: behind on the new competencies, slow to be acted on, and short of the development that works best."
* Interactive 5-Tab Dashboard (`recharts`):
   1. Gap to Target: Horizontal stacked bar chart by level (Principals: 18% below target; MDs: 0% below target; Partners: 56% below target, 0% above target / ready for next level).
   2. Trajectory: KPI callout (`80% at or above target, +16 pts YoY`) + Cohort Flow breakdown of last year's 16 below-target leaders (`7 moved up`, `7 stayed below`, `2 left`).
   3. Competencies in Focus: Grouped bar/heatmap comparing Traditional competencies (`≤4% below target`) vs. Emerging competencies (`29%–33% below target`; only `28%` of Partners at/above target).
   4. Managing Out: Clean metric cards + visual timeline showing `5 leaders below target for 3+ years (3 with no action recorded)`, `32 months` median time to decision, and exit quality (`8 non-regretted` vs. `6 regretted` over 5 years).
   5. Development Efforts: Comparison chart showing mentoring & non-traditional development drive the highest growth yet receive only `29%` of hours, and leaders using all 4 levers grow `~6x faster` than those using 1 or none.
* Footer Note: Small caption referencing the 5 measurement principles (measure gap size not just count; count each person once; judge exits by quality; track cohorts over time; evaluate combined levers).

### Section 7: Built for Trust, Not Automation (`TrustGuardrailsSection.tsx`)
* Layout: 2-column split.
* Left (4 Trust Pillars):
   1. People make every call: The agent gathers evidence and drafts; evaluators and boards decide.
   2. Every fact is traceable: Every assessment links directly back to its source and evidence tag.
   3. Designed for candor: Anonymous colleague feedback options, plus separate frank leadership and constructive leader versions.
   4. Feeds your existing HR stack: A screwdriver, not a Swiss Army knife—CraftArc feeds Workday or your HRIS rather than replacing it.
* Right (`ArchitectureFlowSvg.tsx`): Clean inline SVG architectural diagram: `CraftArc AI Agent (Voice/Text Dialogues & Tagged Evidence)` -> `Human Evaluator & Board (Calibration & Decisions)` -> `Existing HRIS (Workday, etc.)`.

### Section 8: Proof & White-Glove Setup (`ProofAndSetupSection.tsx`)
* Layout: 2-column card layout above a 3-step horizontal onboarding timeline.
* Left Card — Proven in Private Equity: Live and in production at a private equity firm. Built on the evaluation discipline of top management consulting firms, proven with senior principals, managing directors, and partners.
* Right Card — Setup Is Part of the Product: We do not hand you an empty tool. Our team helps you write your leadership framework in plain English and runs your first cycle with you so you are live before your next review season.
* Bottom Visual: Clean 3-step horizontal timeline: `01. Define Your Standard` -> `02. Run First Cycle Together` -> `03. Continuous Coaching & Board View`.

### Section 9: Final CTA & Footer (`FinalCtaSection.tsx`)
* CTA Band: Full-width dark slate (`#0F172A`), centered.
   * Headline: `Know your bench before your next review cycle.`
   * Subtext: `See the live platform and walk through a sample board pack.`
   * Button: `Schedule an Executive Briefing` (white button, dark text, opens `BriefingModal.tsx`).
* Footer: Minimal single-row footer with CraftArc wordmark, copyright, and anchor links.

### Briefing Modal (`BriefingModal.tsx`)
* Accessible dialog (`aria-modal="true"`, `Esc` to close, focus management).
* Fields: Full Name (required), Role / Title (required), Company (required), Work Email (required), Optional message.
* Client-side validation and clean confirmation state on submit (no backend required yet; structure submit handler for easy API/webhook drop-in).

## 6. Build & Verification Checklist
Execute in order:

1. Initialize Next.js (App Router, TypeScript, Tailwind CSS) and install `lucide-react` and `recharts`.
2. Create `src/content/copy.ts` and `src/content/sampleDashboard.ts` first.
3. Build all visual components in `src/components/visuals/` ensuring responsive behavior down to `375px` mobile viewports.
4. Build all 9 section components and compose them in `src/app/page.tsx`.
5. Run `npm run lint` and `npm run build` and fix any TypeScript, ESLint, or hydration errors (ensure Recharts uses `"use client"` and `ResponsiveContainer`).
6. Verify interactive states: Hero video modal open/close, 4-Part Cycle tab switching, 5-Tab Board Dashboard chart switching, and Briefing Modal validation/submission.
