# CraftArc Claims Ledger

Every claim in the VSL (`vsl/src/script.py`) and the website (`website/index.html`) traces to a line here, and every line traces to the **CraftArc VSL Fact Set** (13 Nov 2026), a cleaned product screen, or the agreed scope in `docs/ARC_Roadmap_Scope.md`.

**Rule applied.** Only `[Live]` and `[CT]` items are stated as fact. `[Claim]` items appear only as a question to the viewer or as Dash's stated view ("We believe", "I modelled"). `[To build]` and `[Internal]` items do not appear in public copy. Offer terms that only Dash can approve are written, but hidden (website `data-pending`, switched on in `config.js`) and left out of the video. `website/tests/copy_lint.py` enforces the forbidden list and the number allowlist automatically.

Revised on 18 Nov 2026 after the claims review: offer terms withdrawn to approved items, [Claim] lines framed as Dash's view, "could not hold the framework" replaced (no claim that a named AI lacks a feature), coverage and writeup lines tied to what the screens show.

Status key: **OK** = sourced and safe to publish. **FLAG** = sourced, but Dash must confirm before launch (see the end of this file).

## Website guidance refresh (24 Nov 2026, issue 010)

Source: **CraftArc Website Guidance** (Dash, 24 Nov 2026). It sets the page order, the words and the rules, and it defers to **CraftArc Approved Copy**, a master document not yet received. Lines the guidance marks *Approved* are used word for word. Copy that must come from Approved Copy, and copy the guidance marks *Needs approval*, is on the site as a draft: each draft shows a visible badge and carries `data-placeholder`, so `launch_check.py` fails until Dash signs it off. The guidance supersedes the content v5 items below where they conflict.

| ID | Claim as used | Where | Source | Status |
|---|---|---|---|---|
| W01 | Approved lines: the hero question, answer and time line; the problem statement and "The craft stays in a few heads."; the two method lines; "Up and running before your next review cycle."; "If that commitment is not there yet, we will say so." | Homepage (and the time line on every industry page) | Guidance, sections 1, 3, 4, 9, 10, labelled Approved. `copy_lint.py` checks them word for word | OK |
| W02 | Terms used one way: Leadership Cockpit, Review Cycle, Development Arc; Know, Grow, Without the time; 360-degree dialogues; a slate of successors; move up or move out; based on evidence, not opinion; leadership time; development commitments; a private equity firm | Every page | Guidance, "Use these terms, always the same way". Enforced by `GUIDANCE_RULES` in `copy_lint.py` | OK |
| W03 | "We have just come out of stealth with our first paying client, a private equity firm." | Homepage proof, Private Equity and VC page proof, About, other industry pages | Guidance section 7, Approved. Replaces naming the client (V1 withdrawn) | OK |
| W04 | A slate of successors with horizons: ready now, ready in 3 years, ready in 5 to 7 years | Three claims (Know), Leadership Cockpit card | Guidance terms. The Leadership Cockpit is **not built**, so its card says what the agent "will" do and carries a "Not yet live" tag | **FLAG 10: tag wording** (guidance gap 1) |
| W05 | Module status: Review Cycle live with the first client, Development Arc partly live, Leadership Cockpit not built | Solution section | Guidance, "What is live today". Only the Cockpit is tagged. The Development Arc card describes development commitments and progress tracking in the present tense, which matches the Stage 1 scope (`docs/ARC_Roadmap_Scope.md`, stages 8 and 9) | **FLAG 11: confirm which parts of the Development Arc are live** |
| W06 | The eight Review Cycle steps and what the agent does in each | How it works (homepage, Private Equity and VC page) | **Draft until Approved Copy arrives.** Built from the nine Stage 1 stages in `docs/ARC_Roadmap_Scope.md`, leaving out stage 7 (the development dialogue), which has no system capability in Stage 1. "About 25 minutes" is L24 | Draft, **FLAG 12** |
| W07 | The three claims' headlines and outcomes, and the "Delivered by" mapping (Know: Leadership Cockpit, Grow: Development Arc, Without the time: Review Cycle) | Three claims, every homepage-structured page | **Draft until Approved Copy section 3 arrives.** Outcomes restate W01, W02, W04 and the product facts in this ledger | Draft |
| W08 | Solution opening paragraph, module cards ("Who uses it", "What the agent does") and the agent band | Solution section | **Draft until Approved Copy section 4 arrives.** Facts from the product screens and the Stage 1 scope | Draft, and guidance gap 7 (CEO reader test, see `docs/CEO_Reader_Test.md`) |
| W09 | Industry card copy and industry page heroes, naming each sector's next role (partner, managing director, division head, CTO, COO) | Homepage industries, five industry pages | Guidance section 8 and "Industry pages": only the roles and the proof change per industry. Claude's drafts | Draft, guidance gap 3 |
| W10 | How you start: assess, write down the standard, set CraftArc up, run your next cycle | Homepage | Dash's steer in guidance section 9 (same four steps as V3) | Draft, guidance gap 4 |
| W11 | Who it is for lead-in, the seven FAQ answers, the Book a demo copy and form | Homepage, Book a demo page | Guidance sections 10 to 12. FAQ answers reuse sourced lines: L24 (about 25 minutes), the unlimited participants and free contributors offer lines, P07 (we help write down the standard), the anonymity decision (flag 7) | Draft, guidance gap 5 |
| W12 | About page: a stand-in pitch made only of approved lines (W01) and the founder note from Dash's content v5 | About page | Guidance "About": elevator pitch from Approved Copy section 1, founder note by Dash | Placeholders, guidance gap 6 |

**Issue 011 (24 Nov 2026).** At Dash's request the homepage hero plays the existing private equity video, badged as a placeholder until the new product video is ready, and the hero has no button in the body. No new claims.

**Withdrawn from the site with issue 010** (the guidance says never name the client, never use a result or figure from the first client, and organizes the homepage around twelve sections): V1 (Brightstar named), V2 (six to eight weeks), V4, V5, V7, L01 (60 to 100 hours, about 350 lines), P02 (24-month license), the client interview count, G1 and G2 (Gallup), and R1 and R2 on the web pages. R1 and R2 remain in the video until the revamp.

## Industry-neutral homepage (21 Nov 2026)

The homepage now speaks to every industry. The private equity story, evidence (R1, R2), product screens, proof slots and video moved to `website/private-equity.html` unchanged. On 22 Nov 2026 Dash switched the website to American spelling and set ASD-STE100, S1000D and Alex Hormozi's standards for its copy (CLAUDE.md, checklist item 2). Claim wording in this ledger keeps its original spelling. On the same day Dash renamed the first group "Private Markets", with Private Equity, Venture Capital and Investment Banks beneath it. It is listed like every other industry, with no "Live today" label. The industries menu follows Dash's launch list: Private Equity and VC Firms (live), Financial Services, Healthcare & Life Sciences, Technology, Manufacturing & Industrial and Professional Services, each with three sub-sectors. The five non-PE pages are placeholders, marked as such, until the sector template is built.

| ID | Claim as used | Where | Source | Status |
|---|---|---|---|---|
| G1 | Gallup estimates that managers account for at least 70% of the variance in employee engagement across business units. | Homepage evidence | Gallup, State of the American Manager (2015); gallup.com/workplace/236570 ("at least 70%"; some Gallup summaries say "up to 70%", so the copy quotes the report body) | OK |
| G2 | Gallup finds that companies fail to choose the candidate with the right talent for a manager role 82% of the time. | Homepage evidence | Gallup, State of the American Manager (2015); gallup.com/workplace/231593. Gallup's own analytics estimate | OK |
| N06 | Homepage thesis: what separates great organisations is how they grow their next set of leaders. | Homepage hero | Dash's thesis, generalised from N04 | OK, Dash's view |

## Homepage content v5 (22 Nov 2026, Dash's copy)

Dash supplied the homepage copy. It was converted to American spelling and the checklist terms, and three long sentences were split. Claims new to the site:

| ID | Claim as used | Where | Source | Status |
|---|---|---|---|---|
| V1 | Brightstar Capital Partners is named as the client, and it "runs development for its managing directors and partners on CraftArc". | Homepage hero, case study, industries, FAQ; Private Markets page proof | Dash's content v5. The Fact Set says naming the client needs its permission | **FLAG: permission.** `launch_check.py` fails until the line "PERMISSION RECORDED: Brightstar (date, who approved)" is added here |
| V2 | "Ready for your next review cycle in six to eight weeks." | Homepage hero, how organizations start | Dash's content v5. Not in the Fact Set | **FLAG: Dash's commitment.** Confirm delivery can meet it |
| V3 | Onboarding in four steps: assess, write down the craft, set up CraftArc, run the next cycle. | How organizations start | Dash's content v5, consistent with the [CT] services | OK, Dash's offer |
| V4 | "Trace each one's arc from cycle to cycle." | Homepage hero promise | Dash's content v5. Cross-cycle trends are Stage 2 (June 2027) in the agreed scope | **FLAG: Stage 2** (see flag 8) |
| V5 | "The firm started with its senior investment team and plans to extend CraftArc across the firm." | Case study | Dash's content v5. Not in the Fact Set | **FLAG: confirm with Brightstar** |
| V6 | "We will show you how it would run on CraftArc." | Book a demo | Dash's content v5 | FLAG 5: confirm the demo instance is ready |
| V7 | The headline "What separates great organizations from the rest? It is how they grow their next set of leaders." | Why it matters | Dash's content v5 and thesis N06 | OK, Dash's device. Style note: Dash's writing rule A5 discourages questions answered straight away; kept as his deliberate hook |

## Research and narrative (rewrite of 18 Nov 2026, Dash's structure)

| ID | Claim as used | Where | Source | Status |
|---|---|---|---|---|
| R1 | In a study of nearly 4,000 buyout managers at about 800 firms (1970 to 2017), the individual mattered about four times as much as the firm in explaining returns. | VSL evidence card; site evidence section | Braun, Dorau, Jenkinson and Urban, working paper, as reported by Institutional Investor ("about four times as important as the organization"). A working paper, so it is named as one on screen | OK, cite as working paper |
| R2 | When senior partners leave, raising the next fund gets harder. | VSL evidence card; site evidence section | Ivashina and Lerner, "Pay now or pay later? The economics within the private equity partnership", Journal of Financial Economics 131 (2019); NBER w22660: senior partner departures have negative effects on the ability to raise additional capital | OK |
| N04 | What separates great funds from mediocre ones is not investment judgement alone, but how they grow their next set of leaders. Leadership turns a fund into an institution. | VSL opening; site hero | Dash's thesis (brief, 18 Nov 2026), framed as the answer the evidence (R1, R2) points to | OK, Dash's view |
| N05 | Most PE firms have never written down their craft. Few help each leader trace their arc. Feedback arrives once a year, too late to use. | VSL problem; site problem | Fact Set §1 "Most firms cannot say in writing" [Live] (T2); §2 [Claim] (T1, T2); Dash's brief | OK, Dash's view |
| P07 | We bring the expertise to frame your competency model with you. | VSL why; site why | Dash's brief; Fact Set §5 (built with a sitting PE COO, calibrated in 8 to 10 interviews) [Live] | OK |
| D02 | Agent lines in the five conversations are sample dialogue, except "I'm drafting the review documents now…" and "To get started, what have you worked on over the period?", which are the product's own words on screens 06 and 07. | VSL journey; site how | Screens 06 and 07 | OK, disclosed as sample |

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
| L25 | Self-review screen: the coach's welcome message and the voice controls are the live product (Dash's screenshot, 18 Nov 2026). The four conversation turns are sample text. The coach asks whether the person wants to nominate a contributor: the person nominates ([Live]); agent-suggested contributors are Stage 2 and are not shown. | `vsl/assets/screens/clean/EDITS.md` (07); fine print says "sample data and a sample conversation" | OK, sample disclosed |
| PH1 | Proof slots on the website: "[First-cycle result from the live firm goes here]" and "[Approved client quote goes here]". | Dash, 18 Nov 2026: "make up for now". Built as visible slots, not invented figures or quotes: a made-up "21 of 22" would read as real, and an unattributed COO quote could only be the anchor client's, which Dash's rule "never invent numbers" and the claims gate both forbid. Badged, kept out of the video, page marked noindex, and `launch_check.py` fails until both are real | **PLACEHOLDER** |

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
- Proof: placeholder slots for now (PH1). Replace them with a real result and an approved quote before launch.
- A coach conversation takes about 25 minutes (L24). The self-review screen is built from Dash's template (L25).
- Contributor interviews are anonymised as the firm chooses (L10, flag 7 closed).
- The voiceover stays AI generated for now. Dash will record it later.

## Flags for Dash to clear before launch

1. **"A general AI assistant".** It stands in for Claude, the AI assistant named in the source story. No copy names a vendor or says an AI assistant lacks a feature. Treat the line as a risk wherever it appears.
2. **The anchor client.** The DIY story, the 24-month licence and "built with their COO" come from one client. They are anonymised ("a mid-tier private equity firm"), but the client could still recognise its story. Get their OK even for the anonymous version. The Fact Set notes that naming them needs permission.
3. **"How the best management consulting firms groom and select leaders"** is a design claim with no external source. It is phrased as the Fact Set advises.
4. **Offer terms.** Decided on 18 Nov: not published. They are absent from the page source. If that changes, the candidate wording is ready to add to `tools/build_site.py` (the config setting `extraOfferItems` was removed in issue 010 because the guidance has no offer section) and to `OFFER_ITEMS` in `vsl/src/script.py`:
   - "An implementation consultant who adapts your framework, language and process in three to four meetings."
   - "One flat annual fee, fixed for four years, with no build-out fee."
   - "Every launch includes a hands-on implementation consultant, so we take on a small number of firms at a time."
   The exit right and "participants and evaluators are unlimited" are live in both pieces. Confirm the exit right is a standard term, not one client's, and that unlimited users is the pricing you want (it rules out the per-person idea).
5. **Demo readiness.** The call to action now promises a conversation about the buyer's framework. If you want to promise a full cycle on a sample firm, confirm the demo instance is ready first.
6. **Sample names and framework.** The screens now use invented names (Arjun, Anushka, Varun, Kabir, Daniel Shaw). The competency names (Deal Sourcing & Origination, Investment Judgment, Portfolio Value Creation) are still readable. Confirm they are not a client's confidential framework.
7. **Anonymity.** Closed: Dash confirmed interviews are anonymised as the firm chooses (L10).
8. **"Tracks how each leader is progressing."** This is Dash's brief (18 Nov). The agreed Stage 1 scope has no view across review cycles (write-ups are "anchored to this cycle only"), so today progress is tracked within the year against the development plan. Cross-cycle trends arrive in Stage 2 (June 2027). Keep the line as Dash's commitment, or say "within the year" until Stage 2 ships.
9. **Footer links to AgenticPM pages (21 Nov 2026).** The footer mirrors agenticprivatemarkets.ai and says CraftArc is "part of the AgenticPM family". Its Terms of Service, Privacy Policy and Trust Center links, the About Us and Resources links, and the YouTube, LinkedIn and X icons all point to AgenticPM's own pages and accounts. Confirm the AgenticPM terms, privacy policy and trust centre cover CraftArc, or publish CraftArc versions and swap the links in `website/index.html`.
10. **Leadership Cockpit tag (24 Nov 2026).** The guidance says the Cockpit is not built and must carry a clear tag that it is not yet live. The site shows "Not yet live" as a placeholder. Approve the wording, or decide to leave the Cockpit off the homepage for now (guidance gap 1).
11. **Development Arc status.** The guidance calls it partly live. Confirm that development commitments and progress tracking on a phone are live, or say which part is not, so the card can be worded to match.
12. **The eight Review Cycle steps.** The guidance points to eight steps in Approved Copy. Until that document arrives, the site shows Claude's draft built from the Stage 1 scope. Replace it word for word when Approved Copy arrives.
13. **The video (24 Nov 2026).** The video on the Private Equity and VC page predates the guidance: it says "development plan", "evaluator" and "goals", and tells five conversations rather than eight steps. A visible "Video revamp in progress" note sits under it, and the lint reports the old terms as warnings. The revamp clears this.
14. **Investment Banks under Private Equity and VC.** The guidance names the group "Private Equity and VC". The menu keeps Investment Banks as a third sub-sector (Dash, 22 Nov), marked coming soon. Confirm it stays there.

