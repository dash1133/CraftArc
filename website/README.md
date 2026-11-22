# CraftArc website

One static page: no build step, no framework. Open `index.html` through any web server.

```
website/
├── index.html          the homepage (industry-neutral, video placeholder)
├── private-equity.html the private equity page (PE story, evidence, product screens, video)
├── financial-services.html, healthcare-life-sciences.html, technology.html,
│   manufacturing-industrial.html, professional-services.html
│                       sector placeholder pages, one per industry in the menu
├── styles.css          all styling
├── app.js              lead form, attribution and lead scoring
├── config.js           where leads go (edit before launch)
├── assets/img/         cleaned product screens (webp + png), logo, favicon
├── assets/video/       the VSL (720p), captions (VTT) and poster
└── tests/              end-to-end tests and copy lint
```

## Before you go live

Run the launch check. It says READY only when everything below is done:

```bash
python3 website/tests/launch_check.py
```


1. **Connect the lead form.** In `config.js`, set `leadEndpoint` to a URL that accepts a JSON POST: a Formspree form (`https://formspree.io/f/<id>`), a Zapier or Make webhook, a HubSpot workflow webhook, or your own API. Optionally set `leadEmail` as the fallback address. With neither set, the form tells the visitor it is not connected and logs an error, so it never drops a lead silently.
2. **Clear the flags** in `docs/Claims_Ledger.md` (offer terms, anchor-client permission, anonymity, demo readiness). Approved offer lines go in `extraOfferItems` in `config.js` as plain text. Unapproved terms are deliberately absent from the page and its source.
3. **Add analytics** if you want it. The page pushes `lead_submitted` (with the lead's priority) and `cta_click` events to `window.dataLayer`, so Google Tag Manager or the LinkedIn Insight Tag can pick them up.
4. **Publish a full privacy notice** and link it from the footer. The current text is a short placeholder statement.
5. **Replace the two proof slots** in the `#proof` section (a first-cycle result and an approved client quote), then delete their `placeholder` markup.
6. **Remove the `robots noindex` meta tag** from `index.html`. It keeps the draft out of search engines until launch.

## What a lead looks like

```json
{
  "name": "Alex Morgan", "email": "alex.morgan@examplecapital.com", "firm": "Example Capital",
  "role": "coo", "aum": "2to5b", "team": "10to25", "timing": "q1_2027", "framework": "yes",
  "message": "...", "consent": true,
  "email_type": "work", "fit_score": 100, "priority": "hot",
  "source": "craftarc-website", "page": "https://.../", "submitted_at": "2026-11-18T07:00:00.000Z",
  "utm_source": "linkedin", "utm_medium": "paid", "utm_campaign": "coo-q1", "li_fat_id": "...",
  "referrer": "...", "landing_page": "/?utm_source=linkedin..."
}
```

`fit_score` (0 to 100) weighs role (COO and managing partner highest), AUM ($2B to $10B highest), the timing of the next cycle (Q1 2027 highest), whether a framework exists and team size. Personal email domains are accepted but score 10 points lower. `priority` is `hot` at 70 or more, `warm` at 45 or more, otherwise `nurture`. Route hot leads to Dash the same day.

## Tests

```bash
node website/tests/e2e.mjs
```

```bash
python3 website/tests/copy_lint.py
```

`e2e.mjs` serves the site locally with a mock lead endpoint and runs 28 checks in Chromium. They cover page health, images (alt text, explicit sizes so nothing shifts), video and captions, the stated video length against the real file, anchors, and layouts at 390, 820 and 1366 pixels. They also check the screenshot viewer, that unapproved offer terms are absent and config lines are escaped, that placeholder proof is visibly badged and kept out of search, the five-field form, and 15 lead-form scenarios (validation, a full payload, attribution, double submit, honeypot, server error and retry, network failure, keyboard use, email fallback, unconfigured form). `copy_lint.py` checks the site and the VSL against Dash's writing rules and the claims ledger. Results are written to `tests/e2e-results.json` and `tests/copy-lint-results.json`.

## Hosting

**Vercel works with no settings to change.** `vercel.json` at the repository root sets `outputDirectory` to `website`, so every page is served at its own address (for example `/private-equity.html`) with no rewrites. `.vercelignore` uploads only `website/` (not `docs/`, `vsl/`, the tests or this README). Push to `main`, and Vercel redeploys. In the Vercel project settings, leave Root Directory empty and the Output Directory override off, so `vercel.json` applies.

Any other static host works too (Netlify, Cloudflare Pages, GitHub Pages or S3): serve `website/` as the site root. Fonts load from Google Fonts, with a system-font fallback.
