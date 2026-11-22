# CraftArc repository: instructions for agents

## Website change checklist (mandatory)

Every change to the website (`website/`), however small, is complete only when you have worked through this checklist **in order**. Do not tell the user the request is done until every item passes. If an item fails, fix it and run the checklist again from item 1.

Run the automated items in one go with:

```bash
bash website/tests/check_all.sh
```

1. **No em dashes or other AI-writing fingerprints.** All copy follows Dash's writing rules (`dash-writing` skill, edit-pass checklist part A). That means: no em or en dashes, and no double hyphens as dashes. No "not X, but Y", "it's not X, it's Y" or "not just" framing used as filler. No set-up questions answered straight away ("The result?"). No colon teasers ("Here's the thing:"). No arrows in prose, no stacked hedges ("could potentially"), no stock AI words ("seamless", "unlock", "leverage", "robust" and the rest of the list in `website/tests/copy_lint.py`), no semicolons and no exclamation marks. Automated by `copy_lint.py`, whose `--self-test` proves the checks still fire. Then read every changed sentence once yourself, because the lint cannot catch everything (reflexive lists of three, telegram-style fragments, piles of abstract nouns).
2. **Plain English and British spelling.** Complete sentences, one idea each, no sentence over 25 words, British spelling (organisation, judgement, licence). Automated by `copy_lint.py`, plus your own read.
3. **Every claim is sourced.** Each new fact, figure or name traces to `docs/Claims_Ledger.md`. Only items tagged [Live] or [CT] in the CraftArc VSL Fact Set are stated as fact. A number added to the copy lint's allowlist must carry its ledger ID. Never invent a result, quote, client name or price.
4. **Placeholders are visible.** Anything invented or unfinished (proof slots, the homepage video placeholder, sector pages) carries a visible "Placeholder" or "in development" badge and a `data-placeholder` attribute, so `launch_check.py` blocks it.
5. **All browser tests pass.** `node website/tests/e2e.mjs` must report 0 failures. When you add a page, add it to `PAGES` in `e2e.mjs`, to the Industries menu if it is a sector page, and make sure every menu, footer and in-page link resolves.
6. **Look at it.** Screenshot every changed page at desktop (1440 px) and phone (390 px) width with the pre-installed Playwright, and check for overlaps, clipped text, broken layout and anything covering the video controls or captions. The tests cannot see design problems.
7. **The video is untouched unless asked.** The private equity video lives on `website/private-equity.html`. Do not re-render, re-encode or move it unless the user asks. If it does change, update the stated length on the page (a test checks it).
8. **Deployment still works.** `vercel.json` serves `website/` as the site root with no rewrites. If you add or rename pages or change `vercel.json` or `.vercelignore`, run `npx vercel build` on a copy and confirm every page appears in `.vercel/output/static` and nothing from `docs/` or `vsl/` does.
9. **Docs match the change.** Update `website/README.md`, `docs/Claims_Ledger.md` and, where relevant, the launch to-do list (`docs/todo/build_todo.py`, then re-run it).
10. **Run the launch check and report it.** `python3 website/tests/launch_check.py`. NOT READY is expected while placeholders remain, so report which items are still open rather than hiding them.
11. **Commit and push.** Commit on the working branch with a clear message. Push it, and bring `main` up to the same commit when the user has asked for changes to go live. Confirm the branch and `main` point to the same commit.
12. **Report back.** Tell the user what changed, the checklist results (tests passed, lint clean, launch check status) and anything they need to decide or confirm. Flag risks, but do not bury them.

## Where things live

- `website/`: the static site (no build step). `index.html` is industry-neutral. `private-equity.html` is the Private Markets page with the video. Five sector pages are placeholders. Shared `styles.css`, `app.js` and `config.js`.
- `website/tests/`: `e2e.mjs` (browser tests), `copy_lint.py` (writing rules and claims), `launch_check.py` (go or no-go), `check_all.sh` (runs them in checklist order).
- `vsl/`: the video, its script (`vsl/src/script.py`) and the renderer.
- `docs/`: the claims ledger, review report, buyer persona, build plan and launch to-do list.
