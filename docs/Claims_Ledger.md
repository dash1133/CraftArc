# CraftArc Claims Ledger

Every claim in the VSL (`vsl/src/script.py`) and the website (`website/index.html`) traces to a line here, and every line traces to the **CraftArc VSL Fact Set** (13 Nov 2026), a cleaned product screen, or the agreed scope in `docs/ARC_Roadmap_Scope.md`.

**Rule applied.** Only `[Live]` and `[CT]` items are stated as fact. `[Claim]` items appear only as a question to the viewer, as Dash's stated view, or as an offer CraftArc commits to (flagged below). `[To build]` and `[Internal]` items do not appear as current capability. `website/tests/copy_lint.py` enforces the forbidden list and the number allowlist automatically.

Status key: **OK** = sourced and safe to publish. **FLAG** = sourced, but Dash must confirm before launch (see the end of this file).

## Story and pain

| ID | Claim as used | Where | Source and tag | Status |
|---|---|---|---|---|
| L01 | One firm spent 60 to 100 hours of senior time and wrote about 350 lines of instructions trying to make a general AI assistant run its reviews, then gave up. It could not hold the framework and could not be shared. | VSL hook, epiphany; site story, FAQ, offer anchor | Fact Set §2 and §4 [Live] (T2) | **FLAG 1** (the source names Claude) |
| L02 | The firm's COO had written down, on one page, what a great senior deal professional does. | VSL epiphany; site story | Fact Set §4 [Live] (T2) | **FLAG 2** (client story, anonymised) |
| L03 | A framework on paper cannot interview anyone, gather evidence or write a review. | VSL epiphany; site story | Fact Set §2: "A framework on paper is not a working process; it does not run, share or remember on its own" [Live] (T2) | OK |
| N01 | Audience: private equity leaders building their firm's next partners. | VSL hook; site hero | Fact Set §1 niche (buyer is a business leader who wants to build the next set of leaders) [Claim], used as a call-out, not a fact | OK |
| N02 | Pain as the viewer's own questions: where principals stand on each competency; whether feedback arrives in time for the next deal; evidence behind a partner-readiness call; gaps noticed before close. | VSL pain; site questions | Fact Set §2 "For the person reviewed" [Claim] (T1, T2), asked, never asserted | OK |
| N03 | Your framework is the asset. It needs a system that interviews, gathers evidence and drafts the write-up. | VSL insight; site story | Fact Set §4 "The insight" [Claim], Dash's thesis | OK |

## Product (all shown in the cleaned screens or tagged Live)

| ID | Claim as used | Source and tag | Status |
|---|---|---|---|
| L05 | Runs on the firm's own competency framework. Roles, competencies and steps live in plain English, so it adapts without code. | Fact Set §6 [Live] (T1); §4 second insight [Live] (T1) | OK |
| L06 | One home shows what changed since the last visit and what is waiting on each person. | Fact Set §6 [Live] (T2); screen 01 | OK |
| L07 | Five steps per person: launch, self-review, contributor interviews, evaluation coordinator feedback, development plan. | Fact Set §6 [Live] (T1); screen 02 | OK (see conflict C1) |
| L08 | An AI coach interviews each person for the self-review by voice or text, maps answers to competencies live, asks for what is missing and writes the summary. | Fact Set §6 [Live] (T1); CT "executive coach AI agent" | OK |
| L09 | Voice mode and dictation in the agent pane. | Screen 04 | OK |
| L10 | Anonymous, AI-led contributor interviews. Transcripts stored securely. | Fact Set §6 [Live] (T1); CT Stage 1 | OK |
| L11 | Every fact graded as directly observed, hearsay or third party. | Fact Set §5 [Live] (T1) | OK |
| L12 | The agent checks coverage by competency before close and flags gaps (screen: no contributor saw the banker meetings). | Fact Set §6 [Live] (T1); screen 05 | OK |
| L13 | The agent drafts the Executive Committee writeup, the note to the person and the scorecard. | Screen 06 | OK (see conflict C2) |
| L14 | When the evidence cannot answer a question, the writeup says so at the top. | Screen 06 ("This cycle closed with its central question unanswered") | OK |
| L15 | The evaluation coordinator owns the final wording. | Screens 04 and 06 ("AI-generated · you own the final wording") | OK |
| L16 | People can nominate contributors during the self-review. | Fact Set §6 [Live] (T1) | OK |
| L17 | The evaluation coordinator designs the survey with the agent: central questions, who to ask, what each person saw. | Fact Set §6 [Live] (T1) | OK |
| L18 | One chance to explain, no nagging. Asks once or twice, then lets go. | Fact Set §5 and §8 [Live] (T1) | OK |
| L19 | Only the person and their evaluation coordinator see the self-review. | Fact Set §8 [Live] (T1) | OK |
| L20 | Voice on one side, live working document on the other. | Fact Set §6 [Live] (T1) | OK |
| L21 | Goals in the development plan come from the evaluator's write-up. | `ARC_Roadmap_Scope.md` stage 8, Stage 1 scope [CT] | OK |
| L22 | Positioning: shows each leader's progress on their craft and feeds whichever review process you run. | Fact Set §8 [Claim] (T1), product positioning | OK |

## Proof and credibility

| ID | Claim as used | Source and tag | Status |
|---|---|---|---|
| P01 | A mid-tier private equity firm runs its senior deal team (principals, MDs and partners) on CraftArc. | Fact Set §7 [CT] [Live] (T2) | **FLAG 2** |
| P02 | On a 24-month licence. | Fact Set §7 [CT] | **FLAG 2** |
| P03 | Built with that firm's COO, who designed the framework. The firm tried the DIY AI route first. | Fact Set §5, §7 [Live] (T2) | **FLAG 2** |
| P04 | Dash worked at McKinsey, Microsoft and Siemens, and founded AgenticPM, which builds AI agents for private equity deal teams. | Fact Set §5 [Live] | OK |
| P05 | Follows how the best management consulting firms groom and select leaders. | Fact Set §5 [Claim] (T2), worded as the Fact Set advises ("how the best management consulting firms do it", not "McKinsey's process") | **FLAG 3** |
| P06 | Eight to ten client interviews shaped how competencies are weighted and probed. | Fact Set §5 [Live] (T1) | OK |

## Offer, risk reversal, urgency, call to action

| ID | Claim as used | Source and tag | Status |
|---|---|---|---|
| O01 | You start with your senior deal team and expand once the language has settled. | Fact Set §10 [Live] (T2) | OK |
| O02 | An implementation consultant adapts your framework, language and process in three to four meetings. An internal champion runs it, supported by the consultant. | Fact Set §6 [Claim] (T2), an offer CraftArc commits to | **FLAG 4** |
| O03 | One flat annual fee. Unlimited participants and evaluators. Contributors never pay. No build-out fee. | Fact Set §9 [CT], the agreed BCP terms | **FLAG 4** |
| O04 | Exit right: miss a delivery stage and do not fix it, and you can leave with prepaid fees refunded pro rata. | Fact Set §10 [CT] | **FLAG 4** |
| O05 | Fee fixed for four years (website only). | Fact Set §9 and §10 [CT] | **FLAG 4** |
| O06 | Works best when leadership commits to running the cycle. If not, we will say so. | Fact Set §10 [Claim] (T2), Dash's stance | OK |
| O07 | Every launch includes a hands-on implementation consultant, so we take on a small number of firms at a time (website only). | Fact Set §11 [To build], an offer design | **FLAG 4** |
| U01 | If your next review cycle starts in the new year, plan it now. | Fact Set §11 [Claim] (T1), stated as a condition, not a fact | OK |
| C01 | Book a demo. Bring your framework, and we walk you through a full cycle on sample data. | Fact Set §12 [To build]; screens show the sample-data environment | **FLAG 5** |
| D01 | The voiceover is AI generated. Product screens show sample data. | Dash's writing rule; screen edits in `vsl/assets/screens/clean/EDITS.md` | OK |

## Deliberately left out

Candida's demo reactions (she is joining as CEO, so a quote reads as a testimonial from an insider). Brightstar's name (needs permission). Every price figure ($35K agreed, $50K list idea, $2K per head, the $163K four-year total). Stage 2 and roadmap items (email and chat evidence, trend write-ups, transcript capture, firm-wide insights, calibration across evaluators, reciprocity design, managing-out flavour, scores for individuals, expansion below principal). The 95% fit estimate. Succession-economy and $2B "sweet spot" market claims, which have no source yet. The client framework's structure and its "two central tests". Outcome metrics, which do not exist yet.

## Conflicts with the fact set, and how the copy resolves them

- **C1, five steps or nine.** The live product shows five steps, so the copy says five. The nine-stage plan in `ARC_Roadmap_Scope.md` is the contract scope, and the screens show "Standard nine-step journey" as a cycle option. If Dash wants the nine stages in market copy, `STEPS` in `script.py` and step 1 to 5 on the site change together.
- **C2, two drafts or three documents.** Commercial terms say "two drafts". The screen shows three documents (Executive Committee writeup, note to the person, scorecard). The copy follows the screen.
- **C3, product name.** The copy uses **CraftArc** (Fact Set title, "CraftArc Agent" in the product) and the **CRAFT ARC** wordmark from the app. Not ARC360, not "Agentic Executive Development".

## Flags for Dash to clear before launch

1. **"A general AI assistant".** The source story is about Claude. The VSL says "a general AI assistant", and the FAQ names ChatGPT and Claude only in the buyer's own question. Naming a vendor in your own claim is a risk to weigh every time.
2. **The anchor client.** The DIY story, the 24-month licence and "built with their COO" come from one client. They are anonymised ("a mid-tier private equity firm"), but the client could still recognise its story. Get their OK even for the anonymous version. The Fact Set notes that naming them needs permission.
3. **"How the best management consulting firms groom and select leaders"** is a design claim with no external source. It is phrased as the Fact Set advises.
4. **Offer terms.** The flat fee, unlimited users, no build-out fee, fee fixed for four years and the exit right are the agreed terms for one client. Publishing them makes them the public offer. The implementation consultant's three to four meetings and the "small number of firms at a time" line are offer designs, not yet contracted. Confirm each one, or tell me which to remove.
5. **Demo readiness.** The call to action promises a full cycle on sample data. The Fact Set says the demo instance was "planned for next week" on 11 Nov. Confirm it is ready before the site goes live.
