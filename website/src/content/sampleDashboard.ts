// Illustrative sample data for the Board View and the product previews.
// Made up, as in the CraftArc Concept Memo (Draft v1, "What the sample dashboard shows"):
// "These numbers come from made-up sample data. They show what each view reveals. They are not findings."
// The headline figures match the memo. The rest is filled in to be consistent with them.
// Every chart that shows this data carries an "Illustrative Sample Data" badge.

export type Status = "above" | "at" | "below";

export const LEVELS = ["Principal", "MD", "Partner"] as const;

/** Gap to target: share of each level below, at and above target (percent). Memo: 18%, 0%, 56% below; no Partner above. */
export const gapToTarget = [
  { level: "Principals", below: 18, at: 62, above: 20 },
  { level: "MDs", below: 0, at: 76, above: 24 },
  { level: "Partners", below: 56, at: 44, above: 0 },
];

/** Trajectory: share of the firm at or above target. Memo: 80%, up 16 points; FY24 targets were raised. */
export const trajectory = [
  { year: "FY22", pct: 70 },
  { year: "FY23", pct: 73 },
  { year: "FY24", pct: 58 },
  { year: "FY25", pct: 64 },
  { year: "FY26", pct: 80 },
];
export const trajectoryKpi = { value: "80%", label: "at or above target", delta: "+16 pts YoY" };
/** Memo: of the 16 below target in FY25, 7 moved up, 7 stayed below, 2 left. */
export const cohortFlow = { total: 16, movedUp: 7, stayedBelow: 7, left: 2 };

/** Competencies in focus: percent below target. Memo: at most 4% on traditional, 29% to 33% on emerging. */
export const competencies = [
  { name: "Strategic Judgment", kind: "Traditional", below: 4 },
  { name: "Commercial Acumen", kind: "Traditional", below: 3 },
  { name: "Leading People", kind: "Traditional", below: 2 },
  { name: "Execution", kind: "Traditional", below: 4 },
  { name: "Stakeholder Trust", kind: "Traditional", below: 1 },
  { name: "AI Fluency", kind: "Emerging", below: 33 },
  { name: "Data-Led Decisions", kind: "Emerging", below: 29 },
];
export const partnersOnEmerging = 28; // memo: only 28% of Partners at or above target on the emerging competencies

/** Managing out. Memo: 5 below target for 3+ years, 3 with no action; median 32 months; 8 non-regretted, 6 regretted over five years. */
export const managingOut = {
  longBelow: 5,
  noAction: 3,
  medianMonths: 32,
  exits: [
    { year: "FY22", nonRegretted: 1, regretted: 2 },
    { year: "FY23", nonRegretted: 1, regretted: 1 },
    { year: "FY24", nonRegretted: 2, regretted: 1 },
    { year: "FY25", nonRegretted: 2, regretted: 1 },
    { year: "FY26", nonRegretted: 2, regretted: 1 },
  ],
};

/** Development efforts. Memo: mentoring and non-traditional give the most growth yet get 29% of hours; all four levers about 6x faster. */
export const levers = [
  { lever: "Mentoring", hours: 15, growth: 9 },
  { lever: "Non-traditional", hours: 14, growth: 8 },
  { lever: "On-the-job", hours: 38, growth: 4 },
  { lever: "Formal training", hours: 33, growth: 3 },
];
export const leverCombos = [
  { levers: "0 to 1", growth: 2 },
  { levers: "2", growth: 5 },
  { levers: "3", growth: 8 },
  { levers: "4", growth: 12 },
];

/** Part 1 preview: target per competency per level (1 Developing, 2 Proficient, 3 Advanced, 4 Expert). */
export const frameworkTargets = [
  { name: "Strategic Judgment", emerging: false, targets: [2, 3, 4] },
  { name: "Commercial Acumen", emerging: false, targets: [2, 3, 4] },
  { name: "Leading People", emerging: false, targets: [2, 3, 3] },
  { name: "Execution", emerging: false, targets: [3, 3, 4] },
  { name: "Stakeholder Trust", emerging: false, targets: [2, 3, 4] },
  { name: "AI Fluency", emerging: true, targets: [2, 3, 3] },
  { name: "Data-Led Decisions", emerging: true, targets: [2, 2, 3] },
];
export const targetScale = ["", "Developing", "Proficient", "Advanced", "Expert"];

/** Part 4 preview and the hero view: bench depth by level (count of leaders by status). */
export const benchDepth = [
  { level: "Principal", above: 4, at: 14, below: 4 },
  { level: "MD", above: 3, at: 10, below: 0 },
  { level: "Partner", above: 0, at: 4, below: 5 },
];

/** Part 3 preview: progress on the four development levers for one leader (percent of plan done). */
export const leverProgress = [
  { lever: "Mentoring", pct: 70 },
  { lever: "Non-traditional", pct: 40 },
  { lever: "On-the-job", pct: 55 },
  { lever: "Formal training", pct: 80 },
];

/** Grow micro-visual: one leader moving from below to at target across the year. */
export const growTrajectory = [
  { q: "Q1", score: 1.6 },
  { q: "Q2", score: 2.1 },
  { q: "Q3", score: 2.6 },
  { q: "Q4", score: 3.1 },
];

/** The five Board View tabs: the question each answers (memo, Part 4) and what the sample data shows (memo, sample dashboard). */
export const boardTabs = [
  {
    id: "gap",
    label: "Gap to Target",
    question: "How far is each level from target?",
    headline: "The gap has moved to the top.",
    body: "56% of Partners are below target, against 18% of Principals and 0% of MDs. No Partner is ready for the next level.",
  },
  {
    id: "trajectory",
    label: "Trajectory",
    question: "Is the bench getting deeper, and what happened to last year's below-target group?",
    headline: "The bench is getting deeper.",
    body: "80% of the firm is at or above target, up 16 points in a year. Raising the targets on the emerging competencies in FY24 pushed the below-target share up for a while.",
  },
  {
    id: "competencies",
    label: "Competencies in Focus",
    question: "Where are we weakest?",
    headline: "The new muscle is the weak muscle.",
    body: "29% to 33% are below target on the emerging competencies, against at most 4% on any traditional one. Only 28% of Partners are at or above target on them.",
  },
  {
    id: "managing-out",
    label: "Managing Out",
    question: "Are we acting on people who are not making it?",
    headline: "Managing out is slow.",
    body: "5 people have been below target for 3 years or more, and 3 of them have no action recorded. The median time to a decision is 32 months.",
  },
  {
    id: "development",
    label: "Development Efforts",
    question: "Is development time going where it works?",
    headline: "Development time is in the wrong place.",
    body: "Mentoring and non-traditional development go with the most growth, yet get 29% of hours. People who used all four levers grew about six times as fast as those who used one or none.",
  },
] as const;

/** Hero preview: a slate of successors for three key roles (count of candidates per horizon). */
export const successorSlate = [
  { role: "CFO", now: 1, three: 2, fiveToSeven: 1 },
  { role: "Head of Supply Chain", now: 0, three: 1, fiveToSeven: 2 },
  { role: "Head of Manufacturing", now: 1, three: 1, fiveToSeven: 0 },
];
