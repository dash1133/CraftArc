# CraftArc website

A single-page executive site built with Next.js 15 (App Router, TypeScript strict), Tailwind CSS v4, recharts and lucide-react, to the specification in `docs/Website_Build_Instructions.md` (Dash, 26 Nov 2026) and the CraftArc Concept Memo (Draft v1). There are no photos, screenshots or video: every visual is drawn in code. The footer is the site's original footer and never changes (`CLAUDE.md`, item 7).

```
website/
├── src/
│   ├── app/                 layout (fonts, metadata, review mode), page (the nine sections), globals.css
│   ├── content/
│   │   ├── copy.ts          every headline, line and call to action, and STANDARD_WORD ("Great" or "Good")
│   │   ├── sampleDashboard.ts  all illustrative sample numbers
│   │   └── footer.ts        the footer markup, unchanged (do not edit)
│   ├── components/          Navbar, BriefingModal, Footer, sections/ (nine), visuals/ (eight)
│   └── lib/leads.ts         attribution, lead scoring, delivery
├── public/
│   ├── config.js            where leads go (edit before launch, no rebuild needed)
│   ├── assets/img/          logo and favicon
│   └── about.html, book-a-demo.html, private-equity.html   redirects for the footer's links
├── tests/                   browser tests, copy lint, launch check, footer snapshot
└── out/                     the static build (generated, not committed)
```

## Work on it

```bash
cd website && npm ci
```

```bash
npm run dev
```

```bash
npm run build
```

`npm run build` writes the static site to `website/out`. Add `?review` to any address to see the placeholder labels that visitors never see. Add `?briefing=open` to open the briefing form on arrival.

## Before you go live

```bash
python3 website/tests/launch_check.py
```

It says READY only when all of these are done:

1. **Connect the lead form.** In `public/config.js`, set `leadEndpoint` to a URL that accepts a JSON POST (Formspree, a Zapier or Make webhook, HubSpot, or your own API). With only `leadEmail` set, the form opens the visitor's email app. With neither, it says it is not connected and logs an error.
2. **Supply the 60-second film.** Until then a coded storyboard plays in the lightbox. Pass `src` (and `captionsSrc`) to `HeroDemoVideo` in `src/components/sections/HeroSection.tsx`, then remove its placeholder mark.
3. **Verify the three figures** in the urgency strip against the full Korn Ferry and Heidrick & Struggles reports (the memo asks for this), record it in `docs/Claims_Ledger.md`, and remove the placeholder mark in `UrgencyStrip.tsx`.
4. **Decide what to show of Part 4.** The board view is not built yet. It is tagged "In development" and uses sample data.
5. **Publish a full privacy notice**, and confirm the AgenticPM legal links in the footer cover CraftArc.
6. **Remove the noindex setting** (`robots` in `src/app/layout.tsx`).

## What a lead looks like

```json
{
  "name": "Alex Morgan", "role": "CEO", "company": "Example Industrial", "email": "alex.morgan@exampleindustrial.com",
  "message": "...", "email_type": "work", "fit_score": 90, "priority": "hot",
  "source": "craftarc-website", "page": "https://.../", "submitted_at": "2026-11-26T07:00:00.000Z",
  "utm_source": "linkedin", "utm_medium": "paid", "utm_campaign": "ceo-q1", "li_fat_id": "...",
  "referrer": "...", "landing_page": "/?utm_source=linkedin..."
}
```

`fit_score` (0 to 100) favors business leaders (CEO, founder, chair or managing partner highest, then COO, CFO, managing director or partner) over HR, as the memo says to sell to business leaders. A work email adds 30, a message of 20 characters or more adds 10, and a company name that matches the email domain adds 10. `priority` is `hot` at 70 or more, `warm` at 45 or more, otherwise `nurture`. The page pushes `cta_click` and `lead_submitted` events to `window.dataLayer` for analytics.

## Tests

Every change follows the ordered checklist in `CLAUDE.md`. Run its automated steps with:

```bash
bash website/tests/check_all.sh
```

It runs ESLint and the static build, the copy lint self-test and the copy lint, the 34 browser tests and the launch check. The browser tests serve `website/out` with a mock lead endpoint and cover: page health, no raster images or video, the nine sections in order, the navbar, the hero and its story player (open, auto-advance, step, Escape, backdrop), the urgency sources, the promises, the four-part tabs (click, arrow keys, diagram), the comparison table, the five board tabs (each draws a chart), trust and setup, the final call to action, the briefing form (accessibility, validation, full payload, honeypot, double submit, server error and retry, network failure, email fallback, unconfigured form, scoring, attribution, `?briefing=open`), the footer against its snapshot and every footer link, the redirect pages, phone and tablet widths, review mode, sample-data labels, and that the page never names the client, its figures or a price.

## Hosting

`vercel.json` at the repository root installs and builds `website/` and serves `website/out`. Push to `main` and Vercel redeploys. In the Vercel project settings, leave Root Directory empty and the build and output overrides off, so `vercel.json` applies. Any static host works: run `npm run build` and serve `website/out`.
