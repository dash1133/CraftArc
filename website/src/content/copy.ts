// All marketing copy for the CraftArc website, in one place.
// Sources: docs/Website_Build_Instructions.md (Dash, 26 Nov 2026) and the CraftArc Concept Memo,
// Draft v1 (Dash, 25 Nov 2026). Lines are used as written, except where Dash's writing rules
// (CLAUDE.md, items 1 and 2) required a change: em dashes became commas, colons or full stops,
// one 26-word sentence was split, and "senior time" became "leadership time" (one term per concept).
// Every fact traces to docs/Claims_Ledger.md (section "Next.js rebuild").

/** The wording for the standard. The memo leaves "good" or "great" open; flip it here. */
export const STANDARD_WORD: "Great" | "Good" = "Great";
const w = STANDARD_WORD;
const wl = STANDARD_WORD.toLowerCase();

export const CTA = {
  primary: "Book a Briefing",
  final: "Schedule an Executive Briefing",
  watch: "Watch the 60s Story",
  submit: "Request my briefing",
};

export const NAV = [
  { href: "#how", label: "How It Works" },
  { href: "#board", label: "Board View" },
  { href: "#trust", label: "Trust" },
  { href: "#setup", label: "Setup" },
];

export const HERO = {
  h1: "Can you tell if your company has a gap in leadership depth?",
  sub: "What are the risks associated with your current leadership profile?",
  resolution: [
    "CraftArc answers both, with evidence, not opinion.",
    "Know where every leader stands and spot where your bench is thin.",
    "Keep every leader growing toward their next role, without blocking days of leadership time.",
  ],
  previewTitle: "Leadership Depth & Risk View",
  previewCallouts: [
    { tone: "risk", label: "Partner layer", value: "56% below target" },
    { tone: "below", label: "Below target for 3+ years", value: "5 leaders" },
  ],
  playPill: "Watch the 60s Story",
  playLength: "(1:00)",
  placeholderNote: "Placeholder: a 60-second storyboard plays until the film is ready.",
};

export const STORY_BEATS = [
  { title: "The gap", line: "The board asks how deep the bench is. Most companies cannot answer." },
  { title: "Define the standard", line: `CraftArc writes down what ${wl} looks like at each leadership level.` },
  { title: "AI 360-degree dialogue", line: "The agent talks with each colleague and tags every fact by its source." },
  { title: "Continuous coaching", line: "A just-in-time coach keeps each leader's plan alive all year." },
  { title: "Board depth view", line: "The board sees where the bench is deep, where it is thin, and who should move up or move out." },
];

export const URGENCY = {
  label: "Why boards are asking now",
  stats: [
    {
      value: "1 in 4",
      text: "CEO successions are unprepared.",
      source: "Korn Ferry, CEO succession study, 2026",
      href: "https://www.kornferry.com/about-us/press/new-korn-ferry-study-finds-ceo-transitions-are-outpacing-succession-readiness",
      meter: { kind: "segments", total: 4, filled: 1, tone: "risk" },
    },
    {
      value: "17%",
      text: "of organizations review succession plans every quarter, though 60% of directors and CEOs say it should be continuous.",
      source: "Korn Ferry, CEO and Board Survey, 2026",
      href: "https://www.kornferry.com/insights/featured-topics/leadership-articles/what-ceo-succession-reveals-about-board-governance",
      meter: { kind: "bar", fill: 17, target: 60, tone: "below" },
    },
    {
      value: "1/3+",
      text: "of US companies lack a CEO with the capabilities they need in the near term.",
      source: "Heidrick & Struggles, Route to the Top US 2026",
      href: "https://www.heidrick.com/en/insights/chief-executive-officer/route-to-the-top-us-2026-closing-the-ceo-capability-gap",
      meter: { kind: "segments", total: 3, filled: 1, tone: "below" },
    },
  ],
  verifyNote: "Placeholder: verify these figures against the full reports before launch.",
} as const;

export const PROMISES = {
  eyebrow: "What you get",
  h2: "Three promises to the CEO and the board.",
  cards: [
    {
      id: "know",
      title: "Know",
      summary: "See how close every leader is to each key role, based on evidence, not opinion.",
      outcomes: [
        "A slate of successors for every key role: ready now, ready in 3 years, ready in 5 to 7 years.",
        "Fair calls on who should move up or move out, based on what colleagues actually saw.",
        `One clear standard for what ${wl} looks like at each leadership level.`,
      ],
    },
    {
      id: "grow",
      title: "Grow",
      summary: "Grow a slate of successors for every key role, measured against the standard, not against each other.",
      outcomes: [
        "Your best people know exactly what to work on to reach the next role.",
        "Leaders who are off track find out early, while there is still time to change.",
        "Everyone on the slate keeps moving forward, all year.",
      ],
    },
    {
      id: "time",
      title: "Without the time",
      summary: "Run the way the best firms grow their leaders, without blocking days of leadership time.",
      outcomes: [
        "Your leaders spend their time on meaningful dialogue, not chasing feedback.",
        "Review season stops taking over your leaders' calendars.",
        "Up and running before your next review cycle.",
      ],
    },
  ],
} as const;

export const CYCLE = {
  eyebrow: "How it works",
  h2: "Four parts, one cycle, one agent.",
  lede: `The four parts run as a cycle. The gaps found in Part 4 shape what ${wl} looks like in the next round.`,
  agent: { line1: "1 AI agent", line2: "Voice or text" },
  parts: [
    {
      n: 1,
      anchor: "part-1",
      title: `Define What ${w} Looks Like`,
      short: "Define the standard",
      body: `Write down what ${wl} looks like at each level, tied to what the business needs next.`,
    },
    {
      n: 2,
      anchor: "review-cycle",
      title: "Assess Leaders and Set Development Plans",
      short: "Assess and plan",
      body: "The agent holds 360-degree dialogues, tags every fact by source, and drafts an evidence-backed view. The evaluator decides.",
    },
    {
      n: 3,
      anchor: "development-arc",
      title: "Execute to Plan",
      short: "Execute to plan",
      body: "A just-in-time coach keeps the plan alive all year. It never nags, and it ties every check-in to the experience the next role needs.",
    },
    {
      n: 4,
      anchor: "part-4",
      title: "Assess Gaps in Leadership Depth",
      short: "Assess depth",
      body: "A live portfolio of your bench: where it is deep, where it is thin, and who should move up or move out.",
      status: "In development",
    },
  ],
} as const;

export const DIFFERENCE = {
  eyebrow: "The difference",
  h2: "Other tools collect forms. CraftArc holds the conversation.",
  sub: "Built on the impartial evaluator method of leading management consulting firms, delivered without blocking days of leadership time.",
  formLabel: "Review form",
  formComment: "Great team player, needs more strategic focus.",
  agentLabel: "CraftArc agent",
  dialogue: [
    { who: "Agent", text: "You mentioned the Q3 deal committee. What did you see her do when the numbers were challenged?" },
    { who: "Colleague", text: "She paused the vote, rebuilt the downside case overnight and brought it back the next morning." },
  ],
  tag: "Observed first-hand: Q3 Deal Committee",
  table: {
    head: ["", "Review form", "CraftArc agent"],
    rows: [
      ["How feedback is gathered", "A survey, often late and thin", "A conversation by voice or text, about 25 minutes"],
      ["What it captures", "Ratings and short comments", "Examples, each tagged as seen first-hand, heard, or opinion"],
      ["The framework", "The tool's template", "The client's own, in plain English, changed without code"],
      ["Who writes it up", "The evaluator, by hand", "The agent drafts. The evaluator decides."],
      ["How it ends", "A rating", "A conversation and a plan"],
      ["Between reviews", "Nothing", "A coach that keeps the plan alive"],
    ],
  },
} as const;

export const BOARD = {
  eyebrow: "Board view",
  h2: "A live portfolio of your leadership bench.",
  sampleBadge: "Illustrative Sample Data",
  status: "In development",
  insightLabel: "Key insights",
  insight: "The firm is building depth at Principal and MD level. The real risk is the Partner layer: behind on the new competencies, slow to be acted on, and short of the development that works best.",
  footnote: "Built on five measurement rules. Measure the size of the gap as well as the count, and count each person once. Judge exits by their quality, follow each group over time, and look at how development levers combine.",
} as const;

export const TRUST = {
  eyebrow: "Trust",
  h2: "Built for trust, not automation.",
  pillars: [
    { title: "People make every call.", body: "The agent gathers evidence and drafts. Evaluators and boards decide." },
    { title: "Every fact is traceable.", body: "Every assessment links back to its source and its evidence tag." },
    { title: "Designed for candor.", body: "Colleagues can give feedback anonymously. Leadership gets a frank version, and each leader gets a constructive one." },
    { title: "Feeds your existing HR stack.", body: "A screwdriver, not a Swiss Army knife. CraftArc feeds Workday or your HRIS rather than replacing it." },
  ],
  flow: [
    { title: "CraftArc AI agent", sub: "Voice and text dialogues, tagged evidence" },
    { title: "Human evaluator and board", sub: "Calibration and every decision" },
    { title: "Your existing HRIS", sub: "Workday or your current system" },
  ],
} as const;

export const SETUP = {
  eyebrow: "Proof and setup",
  h2: "Live in production, and set up with you.",
  proof: {
    title: "Proven in Private Equity",
    body: "Live and in production at a private equity firm. Built on the evaluation discipline of top management consulting firms, and proven with senior principals, managing directors and partners.",
  },
  setup: {
    title: "Setup Is Part of the Product",
    body: "We do not hand you an empty tool. Our team helps you write your leadership framework in plain English. We run your first cycle with you, so you are live before your next review season.",
  },
  steps: ["Define your standard", "Run your first cycle together", "Continuous coaching and board view"],
} as const;

export const FINAL = {
  h2: "Know your bench before your next review cycle.",
  sub: "See the live platform and walk through a sample board pack.",
} as const;

export const MODAL = {
  title: "Book an executive briefing",
  intro: "Tell us who you are, and we will email you to arrange a time.",
  fields: {
    name: "Full name",
    role: "Role or title",
    company: "Company",
    email: "Work email",
    message: "Anything we should know? (optional)",
  },
  privacy: "We use these details only to reply and to arrange your briefing.",
  thanksTitle: "Thank you. Your request is in.",
  thanksBody: "We will email you to arrange a time.",
} as const;

export const META = {
  title: "CraftArc | Know the depth of your leadership bench",
  description:
    "Can you tell if your company has a gap in leadership depth? CraftArc answers with evidence, not opinion, without blocking days of leadership time.",
} as const;
