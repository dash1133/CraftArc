# CraftArc website and VSL: build plan and checks

Inputs: the **CraftArc VSL Fact Set** (13 Nov 2026) and **Craft ARC Spotlight FY26 screenshots** (six app frames from `arc-dev`). Output: a 2:35 VSL and a one-page website with a tested lead form. Every step below has a check, and the check's result is recorded in `docs/Review_Report.md`.

| # | Step | What was built | How it was checked |
|---|---|---|---|
| 1 | Claims ledger | `docs/Claims_Ledger.md`: every claim mapped to its fact-set tag. Only `[Live]` and `[CT]` are stated as fact. | Claims tester (fresh eyes) re-checked every line against the PDF. `website/tests/copy_lint.py` blocks forbidden claims and any number not in the ledger. |
| 2 | Buyer persona | `docs/CraftArc_Buyer_Persona.md`: PE COO or managing partner, with a meta question and a Leader test. | Used by the persona tester. |
| 3 | Clean screens | `vsl/src/clean_screens.py` relabels test data ("ARC H1 2026 - TESTING", "Parth 1") and replaces a real staff name in the header. Log in `vsl/assets/screens/clean/EDITS.md`. | Every edit inspected at 2x zoom. No feature, layout or number changed. |
| 4 | VSL script | `vsl/src/script.py` is the one source for the voiceover, captions, visuals and claim IDs. `vsl/VSL_Script.md` is generated from it. | Copy lint (dashes, semicolons, banned words, US spellings, sentence length, numbers). Hormozi-lens, buyer and claims reviews. |
| 5 | Voiceover | Offline Kokoro voice (`af_heart`). The script never leaves the machine. | Words-per-minute per sentence, phonemes checked for COO, McKinsey, Siemens, CraftArc and write-up. |
| 6 | Render | `vsl/src/render_vsl.py` draws every frame (Pillow) and encodes with ffmpeg. Captions are burned in and also exported as VTT and SRT. | Stills per sentence and a contact sheet, reviewed. ffprobe (1920x1080, 30 fps, AAC 48 kHz), EBU R128 loudness (target -16 LUFS), blackdetect (no black frames). |
| 7 | Website | `website/`: static HTML, CSS and JS, no build step. VSL, five steps with real screens, proof, offer, FAQ, lead form. | `website/tests/e2e.mjs` (23 Playwright tests, desktop, tablet and mobile) and the copy lint. |
| 8 | Leads | Validation, honeypot, double-submit guard, UTM and LinkedIn click-ID capture, lead fit score (hot, warm, nurture), JSON POST to any webhook, email fallback. | 15 of the 23 tests are on the lead form, against a local mock endpoint that records every payload. |
| 9 | Reviews | Three fresh-eyes reviewers: a simulated Hormozi lens, the buyer persona, and the Dash writing and claims tester. | Scores and fixes logged in `docs/Review_Report.md`. Fixes applied, then re-scored. |
| 10 | Ship | Commit to the working branch and push. | Tests re-run on the final files. |

## Decisions made without Dash (change any of them)

- **Name:** CraftArc in prose, CRAFT ARC wordmark, as in the app. Not ARC360.
- **Steps:** five, as the live product shows, not the nine-stage contract plan.
- **Price:** not shown. The flat-fee structure is shown, and the number is quoted after a call.
- **Anchor client:** described, never named.
- **Narrator:** a calm AI voice in the "we" voice of the company, with an AI disclosure at the end, following Dash's rule.
- **Length:** 2:35 against a 2-minute target. Nothing that carries a claim's frame was cut to hit the target.
