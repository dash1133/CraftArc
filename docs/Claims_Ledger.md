# CraftArc Claims Ledger

Every claim in the VSL (`vsl/src/script.py`) and the website (`website/index.html`) traces to a line here, and every line traces to the **CraftArc VSL Fact Set** (13 Nov 2026), a cleaned product screen, or the agreed scope in `docs/ARC_Roadmap_Scope.md`.

**Rule applied.** Only `[Live]` and `[CT]` items are stated as fact. `[Claim]` items appear only as a question to the viewer or as Dash's stated view ("We believe", "I modelled"). `[To build]` and `[Internal]` items do not appear in public copy. Offer terms that only Dash can approve are written, but hidden (website `data-pending`, switched on in `config.js`) and left out of the video. `website/tests/copy_lint.py` enforces the forbidden list and the number allowlist automatically.

Revised on 18 Nov 2026 after the claims review: offer terms withdrawn to approved items, [Claim] lines framed as Dash's view, "could not hold the framework" replaced (no claim that a named AI lacks a feature), coverage and writeup lines tied to what the screens show.

Status key: **OK** = sourced and safe to publish. **FLAG** = sourced, but Dash must confirm before launch (see the end of this file).

## Story and pain

| ID | Claim as used | Where | Source and tag | Status |
|---|---|---|---|---|
| L01 | One firm spent 60 to 100 hours of senior time trying to make a general AI assistant run its reviews, then gave up. After about 350 lines of instructions it still had no process the whole firm could run. | VSL hook, epiphany, proof; site story, proof, FAQ | Fact Set §2 and §4 [Live] (T2). "No process the whole firm could run" restates "it could not be shared", without saying the AI lacks a feature | **FLAG 1** (the source names Claude) |
| L02 | The firm's COO had written down, on one page, what a great senior deal professional does. | VSL epiphany; site story | Fact Set §4 [Live] (T2) | **FLAG 2** (client story, anonymised) |
| L03 | A framework on paper cannot interview anyone, gather evidence or write a review. | VSL epiphany; site story | Fact Set §2: "A framework on paper is not a working process; it does not run, share or remember on its own" [Live] (T2) | OK |
| N01 | Audience: private equity leaders building their firm's next partners. | VSL hook; site hero | Fact Set §1 niche (buyer is a business leader who wants to build the next set of leaders) [Claim], used as a call-out, not a fact | OK |
| N02 | Pain as the viewer's own questions: where principals stand on each competency; whether feedback arrives in time for the next deal; evidence behind a partner-readiness call; gaps noticed before close. | VSL pain; site questions | Fact Set §2 "For the person reviewed" [Claim] (T1, T2), asked, never asserted | OK |
| N03 | "We believe" your framework is the asset. It needs a system that interviews, gathers evidence and drafts the write-up. | VSL insight; site story | Fact Set §4 "The insight" [Claim], framed as Dash's view | OK |

## Product (all shown in the cleaned screens or tagged Live)

| ID | Claim as used | Source and tag | Status |
|---|---|---|---|
| L05 | Runs on the firm's own competency framework. Roles, competencies and steps live in plain English, so it adapts without code. | Fact Set §6 [Live] (T1); §4 second insight [Live] (T1) | OK |
| L06 | One home shows what changed since the last visit and what is waiting on each person. | Fact Set §6 [Live] (T2); screen 01 | OK |
| L07 | Five steps per person: launch, self-review, contributor interviews, evaluation coordinator feedback, development plan. | Fact Set §6 [Live] (T1); screen 02 | OK (see conflict C1) |
| L08 | An AI coach interviews each person for the self-review by voice or text, maps answers to competencies live, asks for what is missing and writes the summary. | Fact Set §6 [Live] (T1); CT "executive coach AI agent" | OK |
| L09 | Voice mode and dictation in the agent pane. The VSL labels it "Voice or text, in every agent conversation", because screen 04 is the coordinator's agent pane, not a self-review. | Screen 04 | OK (no self-review screen exists yet, see Needs Dash) |
| L10 | AI-led contributor interviews, anonymised as the firm chooses. Transcripts stored securely. | Fact Set §6 [Live] (T1); CT Stage 1; Dash, 18 Nov 2026: "it can be anonymized as desired" | OK |
| L11 | The agent grades every fact as directly observed, hearsay or third party. | Fact Set §5 [Live] (T1). No screen shows the grades, so the VSL shows a designed card, not product UI | OK |
| L12 | The agent checks coverage for every competency and flags the gaps before you complete the survey (screen: no contributor saw the banker meetings). | Fact Set §6 [Live] (T1, "before launch"); screens 04 and 05 show the check offered before the survey is completed | OK |
| L13 | The agent drafts the Executive Committee writeup, the note to the person and the scorecard. | Screen 06 | OK (see conflict C2) |
| L14 | "Here" / "in the sample", the writeup opens by naming the question the evidence could not answer. Worded as what the sample shows, not as a rule. | Screen 06 ("This cycle closed with its central question unanswered") | OK |
| L15 | The evaluation coordinator owns the final wording. | Screens 04 and 06 ("AI-generated · you own the final wording") | OK |
| L16 | People can nominate contributors during the self-review. | Fact Set §6 [Live] (T1) | OK |
| L17 | The evaluation coordinator designs the survey with the agent: central questions, who to ask, what each person saw. | Fact Set §6 [Live] (T1) | OK |
| L18 | One chance to explain, no nagging. Asks once or twice, then lets go. | Fact Set §5 and §8 [Live] (T1) | OK |
| L19 | Only the person and their evaluation coordinator see the self-review. | Fact Set §8 [Live] (T1) | OK |
| L20 | Voice on one side, live working document on the other. | Fact Set §6 [Live] (T1) | OK |
| L21 | Goals in the development plan come from the evaluator's write-up. | `ARC_Roadmap_Scope.md` stage 8, Stage 1 scope [CT] | OK |
| L22 | (Removed) "feeds whichever review process you run" | Fact Set §8 [Claim] | Not used |
| L23 | The evaluation coordinator runs each review and forms the view with the agent, from graded facts. | Fact Set §8 FAQ [Live] (T1) | OK |
| L24 | A conversation with the coach takes about 25 minutes, by voice or text. | Dash, 18 Nov 2026 ("25 min") | OK |
| L25 | Self-review screen: the coach's welcome message and the voice controls are the live product (Dash's screenshot, 18 Nov 2026). The four conversation turns below the welcome are sample text. | `vsl/assets/screens/clean/EDITS.md` (07) | OK, sample data disclosed |
| PH1 | Placeholder proof on the website: "21 of 22 senior professionals completed their self-review in the first cycle" and a COO quote. | Dash, 18 Nov 2026: "make up for now". Not a fact. Shown with a visible "Placeholder, replace before launch" badge, kept out of the video, and `website/tests/launch_check.py` fails while it is on the page | **PLACEHOLDER** |

## Proof and credibility

| ID | Claim as used | Source and tag | Status |
|---|---|---|---|
| P01 | A mid-tier private equity firm runs its senior deal team (principals, MDs and partners) on CraftArc. | Fact Set §7 [CT] [Live] (T2) | **FLAG 2** |
| P02 | On a 24-month licence. | Fact Set §7 [CT] | **FLAG 2** |
| P03 | Built with that firm's COO, who designed the framework. The firm tried the DIY AI route first. | Fact Set §5, §7 [Live] (T2) | **FLAG 2** |
| P04 | Dash worked at McKinsey, Microsoft and Siemens, and founded AgenticPM, which builds AI agents for private equity deal teams. | Fact Set §5 [Live] | OK |
| P05 | "I modelled CraftArc on how the best management consulting firms develop and select their leaders" (founder card, first person). | Fact Set §5 [Claim] (T2), framed as Dash's own account | **FLAG 3** |
| P06 | Eight to ten client interviews shaped how competencies are weighted and probed. | Fact Set §5 [Live] (T1) | OK |

## Offer, risk reversal, urgency, call to action

| ID | Claim as used | Source and tag | Status |
|---|---|---|---|
| O01 | You start with your senior deal team only, which keeps the disruption low. | Fact Set §10 [Live] (T2) | OK |
| O02 | An implementation consultant adapts your framework, language and process in three to four meetings. | Fact Set §6 [Claim] (T2), and it conflicts with the [CT] hourly custom services (§13) | **NOT PUBLISHED, FLAG 4** |
| O03 | Participants and evaluators are unlimited. Contributors are never charged. | Fact Set §6 core product [CT] ("Unlimited users; respondents never charged") | **FLAG 4** (it rules out the per-person pricing idea in §13) |
| O03b | One flat annual fee, fixed for four years, with no build-out fee. | Fact Set §9 [CT] for one client; as a public offer it is §11 early-partner terms [To build] | **NOT PUBLISHED, FLAG 4** |
| O04 | Exit right: if we miss a stage we agreed to deliver and do not fix it, you can leave with prepaid fees refunded pro rata. | Fact Set §10 [CT] | **FLAG 4** (a contract term; publishing it makes it the public promise) |
| O06 | It works best when leadership commits to running the cycle. If not, we will say so. | Fact Set §10 [Claim] (T2), Dash's stance | OK |
| O07 | Every launch includes a hands-on implementation consultant, so we take on a small number of firms at a time. | Fact Set §11 [To build] | **NOT PUBLISHED, FLAG 4** |
| O08 | We recommend an internal business champion who owns the cycle. | Fact Set §8 [Claim] (T2), framed as a recommendation | OK |
| U01 | If your next review cycle starts in the new year, plan it now. | Fact Set §11 [Claim] (T1), stated as a condition, not a fact | OK |
| C01 | Book a demo. Bring your framework, and we will talk through how it would run on CraftArc. | Fact Set §12; a conversation, not a promise of a sandbox run | OK (FLAG 5 if the sandbox demo is offered) |
| D01 | The voiceover is AI generated. Product screens show sample data. | Dash's writing rule; screen edits in `vsl/assets/screens/clean/EDITS.md` (names replaced, chips invented and listed, two areas blurred) | OK |

## Deliberately left out

Candida's demo reactions (she is joining as CEO, so a quote reads as a testimonial from an insider). Brightstar's name (needs permission). Every price figure ($35K agreed, $50K list idea, $2K per head, the $163K four-year total). Stage 2 and roadmap items (email and chat evidence, trend write-ups, transcript capture, firm-wide insights, calibration across evaluators, reciprocity design, managing-out flavour, scores for individuals, expansion below principal). The 95% fit estimate. Succession-economy and $2B "sweet spot" market claims, which have no source yet. The client framework's structure and its "two central tests" (the screens showed them, so the writeup body and the lines of inquiry are now blurred). Post-deal and pulse feedback ([Claim]). Outcome metrics, which do not exist yet.

## Conflicts with the fact set, and how the copy resolves them

- **C1, five steps or nine.** The live product shows five steps, so the copy says five. The nine-stage plan in `ARC_Roadmap_Scope.md` is the contract scope. (The raw screens named a cycle "Standard nine-step journey" while showing five steps. The cleaned screens rename it.) If Dash wants the nine stages in market copy, `STEPS` in `script.py` and step 1 to 5 on the site change together.
- **C2, two drafts or three documents.** Commercial terms say "two drafts". The screen shows three documents (Executive Committee writeup, note to the person, scorecard). The copy follows the screen.
- **C3, product name.** The copy uses **CraftArc** (Fact Set title, "CraftArc Agent" in the product) and the **CRAFT ARC** wordmark from the app. Not ARC360, not "Agentic Executive Development".

## Dash's decisions, 18 Nov 2026

- Leads go to dash@craftarc.ai (`website/config.js`, and on the video's end card).
- The withheld offer terms stay out of all public copy (flag 4 closed: not published).
- Proof: placeholder content for now (PH1). Replace it with a real result and an approved quote before launch.
- A coach conversation takes about 25 minutes (L24). The self-review screen is built from Dash's template (L25).
- Contributor interviews are anonymised as the firm chooses (L10, flag 7 closed).
- The voiceover stays AI generated for now. Dash will record it later.

## Flags for Dash to clear before launch

1. **"A general AI assistant".** The source story is about Claude. The VSL says "a general AI assistant", and the FAQ names ChatGPT and Claude only in the buyer's own question. Naming a vendor in your own claim is a risk to weigh every time.
2. **The anchor client.** The DIY story, the 24-month licence and "built with their COO" come from one client. They are anonymised ("a mid-tier private equity firm"), but the client could still recognise its story. Get their OK even for the anonymous version. The Fact Set notes that naming them needs permission.
3. **"How the best management consulting firms groom and select leaders"** is a design claim with no external source. It is phrased as the Fact Set advises.
4. **Offer terms.** Not published until you approve them, and not present in the page source. Candidate wording, ready to paste into `extraOfferItems` in `website/config.js` and `OFFER_ITEMS` in `vsl/src/script.py`:
   - "An implementation consultant who adapts your framework, language and process in three to four meetings."
   - "One flat annual fee, fixed for four years, with no build-out fee."
   - "Every launch includes a hands-on implementation consultant, so we take on a small number of firms at a time."
   The exit right and "participants and evaluators are unlimited" are live in both pieces. Confirm the exit right is a standard term, not one client's, and that unlimited users is the pricing you want (it rules out the per-person idea).
5. **Demo readiness.** The call to action now promises a conversation about the buyer's framework. If you want to promise a full cycle on a sample firm, confirm the demo instance is ready first.
6. **Sample names and framework.** The screens now use invented names (Arjun, Anushka, Varun, Kabir, Daniel Shaw). The competency names (Deal Sourcing & Origination, Investment Judgment, Portfolio Value Creation) are still readable. Confirm they are not a client's confidential framework.
7. **Anonymity.** The copy says contributor interviews are "anonymous to the person reviewed". Confirm that is how it works. Also confirm how it holds in a small team: the sample writeup cites "a Principal who ran the operations workstream", which a 22-person team could identify.
8. **"A general AI assistant".** This stands in for Claude, the AI assistant named in the source story. Treat it as a risk line wherever it appears.
