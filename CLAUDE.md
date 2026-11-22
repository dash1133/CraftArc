# CraftArc repository: instructions for agents

## Website change checklist (mandatory)

Every change to the website (`website/`), however small, is complete only when you have worked through this checklist **in order**. Do not tell the user the request is done until every item passes. If an item fails, fix it and run the checklist again from item 1.

Run the automated items in one go with:

```bash
bash website/tests/check_all.sh
```

1. **No em dashes or other AI-writing fingerprints.** All copy follows Dash's writing rules (`dash-writing` skill, edit-pass checklist part A). That means: no em or en dashes, and no double hyphens as dashes. No "not X, but Y", "it's not X, it's Y" or "not just" framing used as filler. No set-up questions answered straight away ("The result?"). No colon teasers ("Here's the thing:"). No arrows in prose, no stacked hedges ("could potentially"), no stock AI words ("seamless", "unlock", "leverage", "robust" and the rest of the list in `website/tests/copy_lint.py`), no semicolons and no exclamation marks. Automated by `copy_lint.py`, whose `--self-test` proves the checks still fire. Then read every changed sentence once yourself, because the lint cannot catch everything (reflexive lists of three, telegram-style fragments, piles of abstract nouns).
2. **American spelling and the writing standards.** Website copy uses American spelling (organization, judgment, license, color, center). This overrides the British-spelling rule in the `dash-writing` skill for the website. Copy also meets three standards:
   - **ASD-STE100 (Simplified Technical English), adapted for marketing copy.** Descriptive sentences have 25 words at most, and instructions (calls to action, form help) have 20 at most. Paragraphs have 6 sentences at most. Use the active voice, simple tenses and common words with one meaning each. Use one term per concept, as listed below, never a synonym. Avoid noun clusters of more than three words.
   - **S1000D, applied to web pages.** Each section is a self-contained module with one purpose and one heading, and it makes sense on its own. Pages share one structure: the same header, Industries menu and footer, with shared parts kept in `styles.css` and `app.js` and changed in one place. Every version gets an issue entry in `website/CHANGELOG.md` (item 9).
   - **Alex Hormozi's standards (from his published books, applied by us).** The first line of every page names who it is for and the outcome they want. Every section raises the dream outcome or the perceived likelihood of getting it (proof), or cuts time delay or effort. Cut any line that does none of these. Put proof next to each claim (a sourced number, a real screen or a named fact). Give one clear call to action per section, worded the same everywhere: links say "Book a demo" and the form button says "Request my demo". Answer objections in the FAQ, and show the risk reversal wherever there is an offer. Use specific numbers and nouns, not adjectives.

   Automated by `copy_lint.py` (American spelling, sentence and paragraph limits, passive-voice warnings), plus your own read for the rest.

   **Terminology (one term per concept):** self-evaluation (not self-review), contributor interviews, evaluation coordinator (not evaluator), memo for the Executive Committee or leadership document, write-ups for the full set of drafted documents (memo, note to the person, scorecard), development dialogue (the conversation between the evaluation coordinator and the leader), Prepare the dialogue (step 4), development plan, Book a demo. Labels inside product screenshots keep the product's own wording.
3. **Every claim is sourced.** Each new fact, figure or name traces to `docs/Claims_Ledger.md`. Only items tagged [Live] or [CT] in the CraftArc VSL Fact Set are stated as fact. A number added to the copy lint's allowlist must carry its ledger ID. Never invent a result, quote, client name or price.
4. **Placeholders are visible.** Anything invented or unfinished (proof slots, the homepage video placeholder, sector pages) carries a visible "Placeholder" or "in development" badge and a `data-placeholder` attribute, so `launch_check.py` blocks it.
5. **All browser tests pass.** `node website/tests/e2e.mjs` must report 0 failures. When you add a page, add it to `PAGES` in `e2e.mjs`, to the Industries menu if it is a sector page, and make sure every menu, footer and in-page link resolves.
6. **Look at it.** Screenshot every changed page at desktop (1440 px) and phone (390 px) width with the pre-installed Playwright, and check for overlaps, clipped text, broken layout and anything covering the video controls or captions. The tests cannot see design problems.
7. **The video is untouched unless asked.** The private equity video lives on `website/private-equity.html`. Do not re-render, re-encode or move it unless the user asks. If it does change, update the stated length on the page (a test checks it). Its captions are burned in, so the caption track stays off by default. The video still uses British spelling ("judgement") in its burned-in captions, and the lint reports this as a warning until the user asks for a re-render.
8. **Deployment still works.** `vercel.json` serves `website/` as the site root with no rewrites. If you add or rename pages or change `vercel.json` or `.vercelignore`, run `npx vercel build` on a copy and confirm every page appears in `.vercel/output/static` and nothing from `docs/` or `vsl/` does.
9. **Docs match the change.** Add an issue entry to `website/CHANGELOG.md` (next issue number, date, change, reason). Update `website/README.md`, `docs/Claims_Ledger.md` and, where relevant, the launch to-do list (`docs/todo/build_todo.py`, then re-run it).
10. **Run the launch check and report it.** `python3 website/tests/launch_check.py`. NOT READY is expected while placeholders remain, so report which items are still open rather than hiding them.
11. **Commit and push.** Commit on the working branch with a clear message. Push it, and bring `main` up to the same commit when the user has asked for changes to go live. Confirm the branch and `main` point to the same commit.
12. **Report back.** Tell the user what changed, the checklist results (tests passed, lint clean, launch check status) and anything they need to decide or confirm. Flag risks, but do not bury them.

## Where things live

- `website/`: the static site (no build step). `index.html` is industry-neutral. `private-equity.html` is the Private Markets page with the video. Five sector pages are placeholders. Shared `styles.css`, `app.js` and `config.js`.
- `website/tests/`: `e2e.mjs` (browser tests), `copy_lint.py` (writing rules and claims), `launch_check.py` (go or no-go), `check_all.sh` (runs them in checklist order).
- `vsl/`: the video, its script (`vsl/src/script.py`) and the renderer.
- `tools/`: one-off build scripts (for example `build_home_v5.py`, which produced the current homepage). Edit `website/index.html` directly now; re-running a build script overwrites later edits.
- `docs/`: the claims ledger, review report, buyer persona, build plan and launch to-do list.
