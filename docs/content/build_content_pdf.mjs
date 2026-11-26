// Builds docs/CraftArc_Website_Content.pdf (and .html): every word on the website, section by section.
// Sources: the site's own copy and sample data (website/src/content), plus the text shown inside the product
// visuals in every state (tabs, parts, story beats, form errors), read from the built site (website/out).
// Run from the repository root, after `npm run build` in website/:  node docs/content/build_content_pdf.mjs
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { execSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const SITE = path.join(ROOT, "website");
const OUT = path.join(SITE, "out");
const req = createRequire(path.join(SITE, "package.json"));
const { build } = req("esbuild");
const { chromium } = req("playwright");

// ---------------------------------------------------------------- the site's copy and sample data
const bundled = await build({
  stdin: {
    contents: `export * from "./src/content/copy.ts"; export * as S from "./src/content/sampleDashboard.ts";`,
    resolveDir: SITE, loader: "ts",
  },
  bundle: true, write: false, format: "esm", platform: "neutral", logLevel: "error",
});
const C = await import(`data:text/javascript;base64,${Buffer.from(bundled.outputFiles[0].text).toString("base64")}`);
const S = C.S;
const commit = execSync("git rev-parse --short HEAD", { cwd: ROOT }).toString().trim();

// ---------------------------------------------------------------- text inside the visuals, in every state
const TYPES = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".svg": "image/svg+xml", ".woff2": "font/woff2" };
const server = http.createServer((q, r) => {
  const f = path.join(OUT, decodeURIComponent(new URL(q.url, "http://x").pathname === "/" ? "/index.html" : new URL(q.url, "http://x").pathname));
  if (!f.startsWith(OUT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { r.writeHead(404); return r.end(); }
  r.writeHead(200, { "Content-Type": TYPES[path.extname(f)] || "application/octet-stream" }); fs.createReadStream(f).pipe(r);
});
await new Promise((r) => server.listen(0, "127.0.0.1", r));
const BASE = `http://127.0.0.1:${server.address().port}`;
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
await page.goto(BASE + "/");
await page.waitForTimeout(600);
const lines = (t) => [...new Set(t.split("\n").map((x) => x.trim()).filter(Boolean))];
const text = async (sel) => lines(await page.locator(sel).first().innerText());

const V = {};
V.hero = await text("#video [data-sample]");
V.promises = [];
for (let i = 0; i < 3; i++) V.promises.push(lines(await page.locator("#promises article [data-sample]").nth(i).innerText()));
V.parts = [];
for (let i = 0; i < 4; i++) { await page.locator('#how [role="tab"]').nth(i).click(); await page.waitForTimeout(150); V.parts.push(await text("#part-panel")); }
V.difference = await text("#difference [data-sample]");
V.board = [];
for (let i = 0; i < 5; i++) {
  await page.locator('#board [role="tab"]').nth(i).click();
  await page.waitForTimeout(700);
  const panel = page.locator('#board [role="tabpanel"]:not([hidden]) > div').nth(1);
  V.board.push(lines(await panel.innerText()));
}
await page.evaluate(() => { window.__craftarcBeatMs = 600000; });
await page.click('#top [data-cta="watch"]');
await page.waitForSelector("#story[open]");
V.story = [];
for (let i = 0; i < 5; i++) {
  await page.locator('#story [role="tab"]').nth(i).click();
  await page.waitForTimeout(150);
  V.story.push(lines(await page.locator("#story [data-beat] > div").first().innerText()).filter((l) => !/^Beat \d/i.test(l)));
}
await page.keyboard.press("Escape");
await page.click('header [data-cta="header"]');
await page.waitForSelector("#briefing[open]");
await page.click("#bf-submit");
V.formErrors = await page.$$eval("#briefing-form [id$='-err'], #bf-status", (els) => els.map((e) => e.textContent.trim()).filter(Boolean));
await page.keyboard.press("Escape");
V.footer = await page.evaluate(() => {
  const f = document.querySelector(".site-footer");
  return {
    sub: f.querySelector(".footer-sub").textContent.trim(),
    tagline: f.querySelector(".footer-tagline").textContent.trim(),
    family: f.querySelector(".footer-family").textContent.trim(),
    social: [...f.querySelectorAll(".footer-social a")].map((a) => a.getAttribute("aria-label")),
    cols: [...f.querySelectorAll(".footer-cols > div")].map((c) => ({ head: c.querySelector(".footer-head").textContent.trim(), links: [...c.querySelectorAll("a")].map((a) => a.textContent.trim()) })),
    bottom: [...f.querySelectorAll(".footer-bottom p")].map((p) => p.textContent.trim()),
  };
});

// ---------------------------------------------------------------- the document
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const p = (s) => `<p>${esc(s)}</p>`;
const ul = (a) => `<ul>${a.map((x) => `<li>${esc(x)}</li>`).join("")}</ul>`;
const kv = (k, v) => `<p class="kv"><span>${esc(k)}</span>${esc(v)}</p>`;
const words = (a) => a.filter((l) => !/^[\d.,%:+\s]+$/.test(l) && !/^FY\d\d$/.test(l) && !/^(ILLUSTRATIVE SAMPLE DATA|Illustrative Sample Data)$/.test(l));
const onScreen = (a, note = "On screen in the visual (illustrative sample data)") => `<div class="vis"><p class="vis-h">${esc(note)}</p><p class="vis-b">${words(a).map(esc).join("<span class='sep'> · </span>")}</p></div>`;
const table = (head, rows) => `<table><thead><tr>${head.map((h) => `<th>${esc(h)}</th>`).join("")}</tr></thead><tbody>${rows.map((r) => `<tr>${r.map((c) => `<td>${esc(c)}</td>`).join("")}</tr>`).join("")}</tbody></table>`;
const sec = (n, title, body) => `<section><h2>${n ? `<span class="n">${n}</span>` : ""}${esc(title)}</h2>${body}</section>`;

const H = C.HERO, U = C.URGENCY, PR = C.PROMISES, CY = C.CYCLE, D = C.DIFFERENCE, B = C.BOARD, T = C.TRUST, SU = C.SETUP, F = C.FINAL, M = C.MODAL;
const body = [
  sec("", "Page and navigation", [
    kv("Browser tab title", C.META.title), kv("Search description", C.META.description),
    kv("Navigation links", C.NAV.map((n) => n.label).join(" · ")), kv("Header button", C.CTA.primary),
    kv("Standard word", `${C.STANDARD_WORD} (switches every "What ${C.STANDARD_WORD} Looks Like" on the page)`),
  ].join("")),
  sec("1", "Hero", [
    `<h3 class="big">${esc(H.h1)}</h3>`, `<p class="sub">${esc(H.sub)}</p>`, p(H.resolution.join(" ")),
    kv("Buttons", `${C.CTA.primary} · ${C.CTA.watch}`),
    `<h4>${esc(H.previewTitle)}</h4>`, onScreen(V.hero),
    `<h4>The 60-second story (storyboard until the film is ready)</h4>`,
    `<ol>${C.STORY_BEATS.map((b, i) => `<li><strong>${esc(b.title)}.</strong> ${esc(b.line)}${V.story[i] ? `<div class="vis-inline">On screen: ${words(V.story[i].filter((l) => l !== b.line && l !== b.title)).map(esc).join(" · ")}</div>` : ""}</li>`).join("")}</ol>`,
  ].join("")),
  sec("2", "Urgency strip", [
    `<p class="label">${esc(U.label)}</p>`,
    U.stats.map((s) => `<div class="stat"><p class="stat-v">${esc(s.value)}</p>${p(s.text)}<p class="src">Source: ${esc(s.source)}<br>${esc(s.href)}</p></div>`).join(""),
  ].join("")),
  sec("3", "Three promises", [
    `<p class="label">${esc(PR.eyebrow)}</p>`, `<h3>${esc(PR.h2)}</h3>`,
    PR.cards.map((c, i) => `<h4>${esc(c.title)}</h4>${p(c.summary)}${ul(c.outcomes)}${onScreen(V.promises[i])}`).join(""),
  ].join("")),
  sec("4", "The four-part cycle", [
    `<p class="label">${esc(CY.eyebrow)}</p>`, `<h3>${esc(CY.h2)}</h3>`, p(CY.lede),
    kv("Center of the diagram", `${CY.agent.line1}, ${CY.agent.line2.toLowerCase()}`),
    CY.parts.map((pt, i) => `<h4>Part ${pt.n}: ${esc(pt.title)}${pt.status ? ` <span class="tag">${esc(pt.status)}</span>` : ""}</h4>${p(pt.body)}${onScreen(V.parts[i])}`).join(""),
  ].join("")),
  sec("5", "Forms vs conversation", [
    `<p class="label">${esc(D.eyebrow)}</p>`, `<h3>${esc(D.h2)}</h3>`, p(D.sub), onScreen(V.difference),
    table(D.table.head.map((h) => h || "Topic"), D.table.rows),
  ].join("")),
  sec("6", "Board view", [
    `<p class="label">${esc(B.eyebrow)}</p>`, `<h3>${esc(B.h2)}</h3>`,
    kv("Badges", `${B.sampleBadge} · ${B.status}`), kv(B.insightLabel, B.insight),
    S.boardTabs.map((t, i) => `<h4>${esc(t.label)}</h4>${kv("Question", t.question)}<p><strong>${esc(t.headline)}</strong> ${esc(t.body)}</p>${onScreen(V.board[i], "On screen in the chart (illustrative sample data)")}`).join(""),
    kv("Footnote", B.footnote),
  ].join("")),
  sec("7", "Trust", [
    `<p class="label">${esc(T.eyebrow)}</p>`, `<h3>${esc(T.h2)}</h3>`,
    T.pillars.map((x) => `<p><strong>${esc(x.title)}</strong> ${esc(x.body)}</p>`).join(""),
    `<h4>Decision flow diagram</h4>`, ul(T.flow.map((x) => `${x.title}: ${x.sub}`)),
  ].join("")),
  sec("8", "Proof and setup", [
    `<p class="label">${esc(SU.eyebrow)}</p>`, `<h3>${esc(SU.h2)}</h3>`,
    `<h4>${esc(SU.proof.title)}</h4>${p(SU.proof.body)}`, `<h4>${esc(SU.setup.title)}</h4>${p(SU.setup.body)}`,
    `<h4>Setup steps</h4><ol>${SU.steps.map((s) => `<li>${esc(s)}</li>`).join("")}</ol>`,
  ].join("")),
  sec("9", "Final call to action", [`<h3>${esc(F.h2)}</h3>`, p(F.sub), kv("Button", C.CTA.final)].join("")),
  sec("", "Briefing form", [
    `<h3>${esc(M.title)}</h3>`, p(M.intro),
    kv("Fields", Object.values(M.fields).join(" · ")), kv("Button", C.CTA.submit), kv("Privacy line", M.privacy),
    kv("When fields are missing", V.formErrors.join(" ")),
    kv("Thank-you", `${M.thanksTitle} ${M.thanksBody}`),
  ].join("")),
  sec("", "Footer (unchanged from the earlier site)", [
    kv("Brand line", V.footer.sub), kv("Tagline", V.footer.tagline), kv("Family", V.footer.family),
    kv("Social", V.footer.social.join(" · ")),
    V.footer.cols.map((c) => kv(c.head, c.links.join(" · "))).join(""),
    V.footer.bottom.map((b) => p(b)).join(""),
  ].join("")),
  sec("", "Appendix: the illustrative sample data", [
    p("These numbers are made up, as in the Concept Memo. They show what each view reveals and are labeled \"Illustrative Sample Data\" on the site."),
    `<h4>Gap to target, % of each level</h4>`, table(["Level", "Below", "At", "Above"], S.gapToTarget.map((r) => [r.level, r.below, r.at, r.above])),
    `<h4>Trajectory, % at or above target</h4>`, table(S.trajectory.map((r) => r.year), [S.trajectory.map((r) => r.pct)]),
    p(`Last year's ${S.cohortFlow.total} below target: ${S.cohortFlow.movedUp} moved up, ${S.cohortFlow.stayedBelow} stayed below, ${S.cohortFlow.left} left.`),
    `<h4>Competencies in focus, % below target</h4>`, table(["Competency", "Kind", "Below target"], S.competencies.map((r) => [r.name, r.kind, `${r.below}%`])),
    p(`Partners at or above target on the emerging competencies: ${S.partnersOnEmerging}%.`),
    `<h4>Managing out</h4>`, p(`${S.managingOut.longBelow} below target for 3+ years (${S.managingOut.noAction} with no action recorded). Median time to a decision: ${S.managingOut.medianMonths} months.`),
    table(["Year", "Non-regretted exits", "Regretted exits"], S.managingOut.exits.map((r) => [r.year, r.nonRegretted, r.regretted])),
    `<h4>Development efforts</h4>`, table(["Lever", "% of hours", "Growth (pts)"], S.levers.map((r) => [r.lever, r.hours, r.growth])),
    table(["Levers used", "Growth (pts)"], S.leverCombos.map((r) => [r.levers, r.growth])),
    `<h4>Bench depth (hero view and Part 4)</h4>`, table(["Level", "Above", "At", "Below"], S.benchDepth.map((r) => [r.level, r.above, r.at, r.below])),
    `<h4>Slate of successors (hero view)</h4>`, table(["Role", "Ready now", "Ready in 3 years", "Ready in 5 to 7 years"], S.successorSlate.map((r) => [r.role, r.now, r.three, r.fiveToSeven])),
    `<h4>Framework targets (Part 1), 1 Developing to 4 Expert</h4>`, table(["Competency", ...S.LEVELS], S.frameworkTargets.map((r) => [r.name + (r.emerging ? " (emerging)" : ""), ...r.targets])),
  ].join("")),
].join("");

const css = fs.readFileSync(path.join(OUT, fs.readFileSync(path.join(OUT, "index.html"), "utf8").match(/href="(\/_next\/static\/css\/[^"]+)"/)[1]), "utf8");
const faces = (css.match(/@font-face\{[^}]+\}/g) || []).join("\n");
const fam = (n) => ({ Inter: "Inter", Instrument_Serif: '"Instrument Serif"' })[n] || "sans-serif";
const html = `<!doctype html><html lang="en-US"><head><meta charset="utf-8"><title>CraftArc website content</title><style>
${faces}
@page { size: A4; margin: 18mm 16mm 18mm 16mm; }
body { font-family: ${fam("Inter")}, system-ui, sans-serif; color: #0f172a; font-size: 10.5pt; line-height: 1.5; margin: 0; }
.cover { border-bottom: 2px solid #0f172a; padding-bottom: 12px; margin-bottom: 18px; }
.cover h1 { font-family: ${fam("Instrument_Serif")}, Georgia, serif; font-weight: 400; font-size: 30pt; margin: 0 0 4px; letter-spacing: -0.01em; }
.cover p { margin: 2px 0; color: #475569; }
section { break-inside: auto; margin: 0 0 16px; }
h2 { font-size: 14pt; margin: 18px 0 8px; padding-top: 10px; border-top: 1px solid #e2e8f0; break-after: avoid; }
h2 .n { display: inline-block; min-width: 22px; color: #475569; font-weight: 500; }
h3 { font-size: 12.5pt; margin: 6px 0 6px; break-after: avoid; }
h3.big { font-family: ${fam("Instrument_Serif")}, Georgia, serif; font-weight: 400; font-size: 20pt; line-height: 1.15; }
h4 { font-size: 10.5pt; margin: 12px 0 4px; break-after: avoid; }
p { margin: 0 0 6px; }
.sub { color: #475569; font-size: 12pt; }
.label { font-size: 8pt; letter-spacing: 0.12em; text-transform: uppercase; color: #475569; margin: 4px 0 2px; }
.kv { display: grid; grid-template-columns: 150px 1fr; gap: 10px; }
.kv span { color: #475569; font-weight: 600; }
ul, ol { margin: 2px 0 8px 18px; padding: 0; } li { margin: 2px 0; }
.vis { border: 1px dashed #cbd5e1; background: #f8fafc; border-radius: 6px; padding: 6px 10px; margin: 4px 0 10px; break-inside: avoid; }
.vis-h { font-size: 7.5pt; letter-spacing: 0.1em; text-transform: uppercase; color: #64748b; margin: 0 0 3px; }
.vis-b { font-size: 9pt; color: #334155; margin: 0; }
.vis-inline { font-size: 8.5pt; color: #64748b; margin-top: 2px; }
.sep { color: #94a3b8; }
.stat { border-left: 3px solid #0f172a; padding: 2px 0 2px 10px; margin: 8px 0; break-inside: avoid; }
.stat-v { font-family: ${fam("Instrument_Serif")}, Georgia, serif; font-size: 20pt; line-height: 1; margin: 0 0 4px; }
.src { font-size: 8.5pt; color: #475569; word-break: break-all; }
.tag { font-size: 7.5pt; font-weight: 600; color: #92400e; background: #fffbeb; border: 1px solid #fde68a; border-radius: 10px; padding: 1px 6px; vertical-align: middle; }
table { border-collapse: collapse; width: 100%; margin: 4px 0 10px; font-size: 9pt; break-inside: avoid; }
th, td { border: 1px solid #e2e8f0; padding: 4px 6px; text-align: left; vertical-align: top; font-variant-numeric: tabular-nums; }
th { background: #f8fafc; font-weight: 600; }
</style></head><body>
<div class="cover"><h1>CraftArc website content</h1>
<p>Every word on the website, section by section, in page order, as published from commit ${esc(commit)} on ${new Date().toLocaleDateString("en-US", { day: "numeric", month: "long", year: "numeric" })}.</p>
<p>Copy comes from website/src/content/copy.ts. Text inside the product visuals is read from the built site in every tab and state.</p></div>
${body}
</body></html>`;

const outHtml = path.join(ROOT, "docs", "CraftArc_Website_Content.html");
const outPdf = path.join(ROOT, "docs", "CraftArc_Website_Content.pdf");
fs.writeFileSync(outHtml, html);
const doc = await browser.newPage();
await doc.goto(BASE + "/");
await doc.setContent(html, { waitUntil: "load" });
await doc.evaluate(() => document.fonts.ready);
await doc.pdf({
  path: outPdf, format: "A4", printBackground: true, preferCSSPageSize: true,
  displayHeaderFooter: true, headerTemplate: "<span></span>",
  footerTemplate: `<div style="font-size:8px;color:#64748b;width:100%;padding:0 16mm;display:flex;justify-content:space-between;"><span>CraftArc website content</span><span><span class="pageNumber"></span> of <span class="totalPages"></span></span></div>`,
});
await browser.close();
server.close();
console.log(`wrote ${path.relative(ROOT, outPdf)} and ${path.relative(ROOT, outHtml)}`);
