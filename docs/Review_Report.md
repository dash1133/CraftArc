# CraftArc VSL and website: review report

Three independent reviewers, each a fresh agent with no sight of the writer's reasoning, scored both pieces, and each fix went back to the same reviewer to confirm. Scores are out of 10.

**Bottom line.** Both pieces rose from 5 to 7 to about 7 to 7.5 in two rounds, and every fix the reviewers said could be made now has been applied. Each reviewer said the copy alone tops out at about 8. The rest needs facts and approvals only Dash can give (see Needs Dash). Nothing in either piece states a [Claim], [To build] or [Internal] item as fact.

- **Hormozi lens (simulated).** Alex Hormozi's published frameworks: the value equation, the Grand Slam Offer, hooks, FAQ, proof, guarantees and his VSL order. This is not Alex Hormozi and does not speak for him.
- **Buyer.** A PE COO at a firm of about $3B, using the persona in `docs/CraftArc_Buyer_Persona.md`.
- **Dash tester.** The claims gate against the CraftArc VSL Fact Set, plus Dash's writing rules (`dash-writing`).

## Scores

| Reviewer | VSL round 1 | Website round 1 | VSL round 2 | Website round 2 |
|---|---|---|---|---|
| Hormozi lens (simulated) | 5 | 6 | 7 | 7 |
| Buyer (PE COO) | 6 | 7 | 7 | 7.5 |
| Dash tester (claims and voice) | 6 | 5 | 7 | 6, and 7.5 with the two blockers fixed |

## Round 1: what the reviewers found, and what changed

**Hormozi lens.** The VSL had no FAQ, a dead zone from 0:49 to 1:02, a hook that reached the viewer only at 10.8 s, a pain question nothing answered, and proof that undersold the best fact. On the website the proof was described rather than shown, the video was buried on mobile, a price comparison had no price, and the form was too long.
- Fixed: the call-out now opens the video. The navigation screens are cut. There is an FAQ scene. The second pain question is now the partner-readiness evidence question. The proof leads with "the firm that gave up ... then signed a 24-month licence". The proof section shows the writeup crop. On mobile the video sits under the headline. The anchor line is gone. The form shows five fields and the button reads "Request my demo".
- Not taken: the flat fee, no build-out fee, implementation consultant "in three to four meetings" and "small number of firms". The claims gate rules these unapproved public terms, so they are kept out of the public copy, with ready wording in the ledger for when Dash approves them. The spoken AI disclosure also stays, because it is Dash's rule.

**Buyer.** The VSL made a top-down reader wait for the answer. The screens contradicted the voiceover: "anonymous" over a named roster, a voice line over the coordinator's chat, and grading with nothing graded on screen. It also left open who sets the ratings. The website screens were too small to read, "It does not decide alone" dodged the judgement question, and "performance management", "groom", the scarcity line and the anchor read as vendor talk.
- Fixed: "CraftArc runs your review cycle on your own competency framework" arrives by about 0:45. The visual mismatches are corrected, and the grades are now a designed card, not fake UI. The FAQ says the evaluation coordinator decides. The screens are readable crops you can enlarge, each with an honest caption. The flagged phrases are removed.

**Dash tester.** Eleven claims-gate failures, including offer terms, a promised sandbox demo, [Claim] lines stated as fact, "before the interviews close", "says so at the top", and saying the AI "could not hold the framework". It also flagged screens that showed the real first name "Parth" in a critical sample writeup, test names, invented chip names missing from the edit log, and text from a client framework.
- Fixed: all eleven, with the wording in `docs/Claims_Ledger.md`. Parth, Nishritha and Karan became Arjun, Anushka and Varun (with Kabir as the coordinator on screen 03) on every screen, with an OCR check that none remain. The chips are listed in `EDITS.md`. The client-framework text is blurred. The writing-rule items B1, B3, B6, B11 and B12 are fixed.

## Round 2

Round 2 found nine "do it now" fixes. All nine are applied, and both blockers are cleared. These fixes came after the round-2 scores, and no third round was run, so the scores above do not yet reflect them.

- **Blocker 1, stale video.** The site played the round-1 cut, which included withdrawn claims. Fixed: the final 2:52 render, the 720p cut, the captions and the poster now ship together. A new test checks that the length stated on the page matches the real file.
- **Blocker 2, unapproved terms in the source.** Hiding them with CSS still published them. Fixed: they are removed from the HTML. Approved lines can be added later through `extraOfferItems` in `config.js`, as escaped plain text. A test checks the source for the old wording.
- **Claims and wording.**
  - "The evaluation coordinator runs each review" replaces "senior colleague", which screen 03 contradicted.
  - The VSL's FAQ beats are statements, not questions answered on the spot (A5).
  - "Voice or text" drops the unsourced "every".
  - "Begin with the principals, MDs and partners only" drops the [To build] "then expand".
  - "Participants and evaluators are unlimited" fixes C9.
  - "running on your framework" replaces "set up", since set-up is billed hourly.
  - "One firm" fixes B11, and "the team still had no process" removes the misread "it".
  - "anonymous to the person reviewed" is flagged for Dash.
- **Hormozi lens.** The repeated DIY line is cut. The grade pills are opaque. A fit qualifier comes before the call to action ("It works best when leadership commits to running the cycle"). The effort answer is fuller. The step 2 crop is now readable on a phone.
- **Buyer.** The opening line now states the outcome ("here is how to review them on evidence"). The voice line matches the screen. "Why not a general AI assistant?" is answered with how the product works. The step 4 crop is readable. One new consistency issue was fixed: Varun appeared as both a coordinator and a subject, so the coordinator on screen 03 is now Kabir.
- **Video quality, found in QA, not by the reviewers.** The text cards held completely still for up to 8 seconds, which loses viewers. Every non-screen scene now has a slow push-in. On a test excerpt, ffmpeg's freezedetect then found no still stretch over 2 seconds.

**Reviewers' verdicts in their own words.**
- Buyer: "Website yes… VSL maybe." Their blockers are partner hours per cycle, seeing the coach interview a principal, and how the fee works.
- Hormozi lens: the copy-only fixes "take each piece to about 8, not 9". Reaching 9 needs the hidden offer approved, an outcome metric, a named client quote, a price or starting figure, and Dash's own voice.
- Dash tester: the voice rubric scores 26 of 40 on both pieces. "Turn" and "authentic" stay at 3 until Dash voices the founder line himself.

## Tests

**Website: 27 of 27 pass** (`node website/tests/e2e.mjs`, Chromium; run three times in a row on the final files, including while a render loaded the CPU).

| Area | Checks |
|---|---|
| Page health | No console errors. One h1. The meta description is under 160 characters. Every image has alt text, loads, and has explicit dimensions, so nothing shifts as it loads. |
| Video | The source, poster and captions load. The captions have 30 or more cues. The length stated on the page matches the real file to within 1.5 s. |
| Layout | No sideways scroll at 390, 820 and 1366 px. The header CTA lands on the form, clear of the sticky header. The screenshot viewer opens and closes with Escape. |
| Claims | Unapproved offer terms are absent from the page source. Offer lines added from config are escaped, never injected as HTML. |
| Leads (15 tests) | Required-field errors appear and focus the first bad field. Bad emails are rejected. A full submission sends the whole lead (contact details, firm profile, fit score, priority and attribution), checked field by field, and pushes a `lead_submitted` event. First-touch UTM and LinkedIn click IDs are kept across pages. A double click sends one lead. Personal email domains are tagged and score 10 lower. Optional fields can be left blank. The honeypot drops bots silently. A server error or network failure keeps the visitor's input and allows a retry. The form submits from the keyboard. The email fallback opens a filled-in email. An unconfigured form fails loudly, never silently. Labels and the live status region are wired. |

**Copy lint: 0 errors, 0 warnings** across 283 text items (`python3 website/tests/copy_lint.py`). It checks the site and every VSL caption, card and label for dashes, semicolons, banned words, US spellings, sentences over 25 words, forbidden claims (client name, prices, roadmap features), and any number that is not in the claims ledger. That last check caught a stale video length twice.

**Screens.** Tesseract OCR finds no Parth, Nishritha, Karan, "TESTING", "nine-step" or "pulse" in the cleaned or website images.

**VSL.** 2:52 at 1920x1080 and 30 fps, plus a 1280x720 web cut, with AAC at 48 kHz.

- Loudness is -16.2 LUFS integrated, the web standard, and the true peak is -1.4 dBFS.
- blackdetect finds no black frames, freezedetect finds no still stretch over 3 seconds, and silencedetect finds no gap over 2 seconds.
- A full decode reports no errors.
- The caption files (VTT, SRT) are generated from the same timeline as the voice, so they cannot drift.
- Frames at every scene transition and at 11 points through the final file were checked by eye.

## Needs Dash

These are the items that move the scores to 9 or more. Each one is a fact or a decision, not copy.

1. **Connect the lead form.** Set `leadEndpoint` (or at least `leadEmail`) in `website/config.js`. Until then the form tells visitors it is not connected.
2. **Approve, or drop, the offer terms** (ledger flag 4): the flat annual fee fixed for four years, no build-out fee, the implementation consultant in three to four meetings, and limited onboarding. Also confirm that the exit right and "unlimited participants and evaluators" are standard terms.
3. **One outcome metric from the live firm**, such as the participation rate or senior hours per cycle. Also permission to name the firm, and a quote or short video from its COO.
4. **Partner time per conversation.** The buyer needs this number to sell the product internally.
5. **A self-review screenshot** showing the coach interviewing a principal. Today no screen shows the coach itself.
6. **Anonymity in small teams.** Who exactly is it anonymous to, and how does it hold when a writeup cites "a Principal who ran the operations workstream"?
7. **Data handling**: where the data is hosted, whether it trains models, and who can see the transcripts.
8. **Demo readiness.** If the sample-firm demo is ready, the call to action can promise "we will show you" rather than "talk through".
9. **Dash's own voice.** Record the voiceover, or at least the founder line in the first person, and appear on camera. That lifts "authentic" and lets the spoken AI disclosure go.
10. **The domain and a calendar link**, for the end card and for the "Request my demo" follow-up.
11. **Confirm the demo framework is not a client's.** The competency names are still readable on the screens.
12. **Use of "a general AI assistant".** It stands in for Claude, the AI assistant named in the source story. Treat it as a risk line wherever it appears.
