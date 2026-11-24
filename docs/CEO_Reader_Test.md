# CEO reader test, first round (24 Nov 2026)

The CraftArc Website Guidance assigns two tests to Claude: the solution section (gap 7) and the industry copy (gap 3), both with CEO readers. This first round is **simulated**. An AI reviewer read the rendered copy cold, playing three CEOs, and checked it against `docs/Claims_Ledger.md`. It does not replace a test with real CEOs, which is on the launch to-do list.

## Readers and scores ("I would book a demo", out of 10)

| Reader | First screen answers the board's question? | Score |
|---|---|---|
| A. CEO of a mid-market private equity firm (about $3B AUM, 12 partners) | Partly. "Next role" is generic, and the board asks about partner succession. The industry page hero comes closer. | 6 |
| B. Managing partner of a 600-person professional services firm | Partly. The homepage does not mention choosing partners, and "senior manager" does not fit a law firm. | 5 |
| C. CEO of a 4,000-person industrial manufacturer | Partly, close to no. The board asks who steps in behind each key role, and the answer sits in the module that is not yet live. | 3 |

## What the readers could say back about the solution

- **Review Cycle:** clear to all three. The agent interviews the leader and colleagues and drafts the write-ups.
- **Development Arc:** clear. It turns the write-ups into development commitments.
- **Leadership Cockpit:** understood as "a successor slate for the board, not built yet". Two readers asked whether the thing the board wants exists today.

## Changes made after the test (drafts only)

| Line before | Line after | Why |
|---|---|---|
| "CraftArc gives the CEO one view of the leadership bench. Two modules do the work that keeps that view current. One agent runs across all three." | "The Review Cycle runs each leader's evaluation. The Development Arc keeps each leader growing through the year. The Leadership Cockpit, now in development, will give the CEO and the board one view of the bench." | The old line read as if the Cockpit works today, which the guidance forbids. |
| Agent band: "Interviews, gathers the evidence, drafts and follows up, in all three modules." | "runs the Review Cycle and the Development Arc, and will run the Leadership Cockpit. It interviews, grades the evidence by source and drafts the write-ups. The evaluation coordinator owns the final wording." | Same Cockpit problem, and readers asked who makes the call. |
| "A slate of successors for each key role: ready now, ..." | "Your leadership team's slate of successors for each key role: ready now, ..." (and the Cockpit card to match) | Readers took the horizons as CraftArc predicting readiness, which the guidance forbids. The slate is the leadership team's call. |
| "Leaders give their time to the development dialogue itself." | "Each conversation with the agent takes about 25 minutes, by voice or text." (L24) | Readers asked how much time it takes. A sourced number answers it. |
| PE hero: "each principal" | "each principal and managing director" | Reader A expected the managing directors in the partner pipeline. |
| Professional services: "each senior manager ... your next partner" | "each senior manager and senior associate ... making partner" | "Senior manager" is business staff in a law firm. |
| Manufacturing: "each plant leader ... your next COO" | "each plant manager ... your next VP of Operations" | Plant managers move to VP of Operations first, and "plant manager" is the reader's word. |
| Healthcare card: "running your next division" | "becoming your next division head" | Matched the industry page. |
| Status chip "Next" | "Coming next" | "Next" was unclear beside "Coming soon". |

## Feedback on approved lines (not changed, for Dash)

The guidance says approved lines are used word for word, so these stay as they are. The readers' reactions are recorded for Dash to weigh:

1. **Hero, "CraftArc can. Know where every leader stands."** Reader C read it as resting on the Leadership Cockpit, which is not built. The Review Cycle already shows where each leader stands through the write-ups, so the line holds, but the first screen does not say so.
2. **"We have just come out of stealth with our first paying client, a private equity firm."** Reader A said it reads like a seed-stage pitch. It is honest, and it is the only proof allowed until the client consents to a result or quote.
3. **Generic "next role".** Readers A and C wanted their own role named on the first screen. The industry pages do this, and the homepage stays industry-neutral by design.

## Suggestions not taken, and why

- **Rewrite the homepage hero** to "Can you show your board who could step into each key role, and why?" Not taken, because the hero is approved copy.
- **Replace "Client results in ... are coming soon"** on the five industry pages. Not taken, because the guidance says the other industries say they are coming soon.
- **Move Investment Banks to Financial Services.** Not taken, because Dash placed it under the first group on 22 Nov. It is raised as claims ledger flag 14.
- **Rename "evaluation coordinator" and "write-ups"** for manufacturing readers. Not taken, because both are fixed terms in CLAUDE.md. Worth testing with real CEOs.

## Open questions for the real test

- Do CEOs outside private equity understand "360-degree dialogues" without explanation?
- Does the "Not yet live" tag on the Leadership Cockpit lower trust, or raise it? Guidance gap 1 asks Dash whether to leave the Cockpit off the homepage for now.
- Do manufacturing and healthcare CEOs see this as different from the talent review in their HR system?
