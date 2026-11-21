// End-to-end tests for the CraftArc landing page, with special care on the lead form.
// Run: node website/tests/e2e.mjs   (uses the pre-installed Playwright library, no test runner)
// It serves website/ on a local port with a mock lead endpoint that records every POST.
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const SHOTS = path.join(ROOT, "tests", "screenshots");
fs.mkdirSync(SHOTS, { recursive: true });

// ---------------------------------------------------------------- server
const leads = [];
let failNext = 0;
const TYPES = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".svg": "image/svg+xml",
  ".png": "image/png", ".webp": "image/webp", ".jpg": "image/jpeg", ".mp4": "video/mp4", ".vtt": "text/vtt" };
const server = http.createServer((req, res) => {
  const url = new URL(req.url, "http://x");
  if (url.pathname === "/api/lead") {
    if (req.method === "OPTIONS") { res.writeHead(204); return res.end(); }
    let body = "";
    req.on("data", (c) => (body += c));
    req.on("end", () => {
      if (failNext > 0) { failNext--; res.writeHead(500); return res.end("fail"); }
      leads.push({ headers: req.headers, body: JSON.parse(body) });
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end('{"ok":true}');
    });
    return;
  }
  const file = path.join(ROOT, decodeURIComponent(url.pathname === "/" ? "/index.html" : url.pathname));
  if (!file.startsWith(ROOT) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) { res.writeHead(404); return res.end(); }
  const stat = fs.statSync(file);
  const type = TYPES[path.extname(file)] || "application/octet-stream";
  const range = req.headers.range;
  if (range) {
    const [a, b] = range.replace("bytes=", "").split("-");
    const start = parseInt(a, 10), end = b ? parseInt(b, 10) : stat.size - 1;
    res.writeHead(206, { "Content-Type": type, "Content-Range": `bytes ${start}-${end}/${stat.size}`, "Accept-Ranges": "bytes", "Content-Length": end - start + 1 });
    return fs.createReadStream(file, { start, end }).pipe(res);
  }
  res.writeHead(200, { "Content-Type": type, "Content-Length": stat.size, "Accept-Ranges": "bytes" });
  fs.createReadStream(file).pipe(res);
});
await new Promise((r) => server.listen(0, "127.0.0.1", r));
const BASE = `http://127.0.0.1:${server.address().port}`;

// ---------------------------------------------------------------- harness
const results = [];
async function test(name, fn) {
  try { await fn(); results.push({ name, ok: true }); console.log(`  PASS  ${name}`); }
  catch (e) { results.push({ name, ok: false, err: e.message }); console.log(`  FAIL  ${name}\n        ${e.message}`); }
}
function assert(cond, msg) { if (!cond) throw new Error(msg); }
function eq(a, b, msg) { if (a !== b) throw new Error(`${msg}: expected ${JSON.stringify(b)}, got ${JSON.stringify(a)}`); }

const browser = await chromium.launch();
const TEST_CONFIG = (extra = {}) => `window.CRAFTARC_CONFIG = ${JSON.stringify({
  leadEndpoint: `${BASE}/api/lead`, leadEmail: "", personalEmailDomains: ["gmail.com", "outlook.com"], ...extra })};`;

async function openPage({ viewport = { width: 1366, height: 900 }, config = TEST_CONFIG(), query = "", device } = {}) {
  const ctx = await browser.newContext(device || { viewport });
  const page = await ctx.newPage();
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });
  // Fonts come from Google in production; block them so tests run offline.
  await page.route(/fonts\.(googleapis|gstatic)\.com/, (r) => r.fulfill({ status: 200, contentType: "text/css", body: "" }));
  await page.route("**/config.js", (r) => r.fulfill({ contentType: "text/javascript", body: config }));
  await page.goto(`${BASE}/${query}`, { waitUntil: "load" });
  return { ctx, page, errors };
}

async function fillValid(page, over = {}) {
  const v = { name: "Alex Morgan", email: "alex.morgan@examplecapital.com", firm: "Example Capital", role: "coo",
    aum: "2to5b", team: "10to25", timing: "q1_2027", framework: "yes", message: "We review 22 senior people.", ...over };
  await page.fill("#name", v.name);
  await page.fill("#email", v.email);
  await page.fill("#firm", v.firm);
  await page.selectOption("#role", v.role);
  if (v.timing) await page.selectOption("#timing", v.timing);
  if (v.aum || v.team || v.framework || v.message) await page.evaluate(() => { document.getElementById("more").open = true; });
  if (v.aum) await page.selectOption("#aum", v.aum);
  if (v.team) await page.selectOption("#team", v.team);
  if (v.framework) await page.selectOption("#framework", v.framework);
  if (v.message) await page.fill("#message", v.message);
  await page.check("#consent");
  return v;
}

console.log(`\nCraftArc website tests against ${BASE}\n`);

// ---------------------------------------------------------------- page
await test("page loads with no console errors and one h1", async () => {
  const { ctx, page, errors } = await openPage();
  eq(await page.locator("h1").count(), 1, "h1 count");
  assert((await page.title()).includes("CraftArc"), "title mentions CraftArc");
  const desc = await page.getAttribute('meta[name="description"]', "content");
  assert(desc && desc.length > 60 && desc.length < 170, `meta description length ${desc && desc.length}`);
  await page.waitForTimeout(300);
  eq(errors.length, 0, `console errors ${errors.join(" | ")}`);
  await page.screenshot({ path: path.join(SHOTS, "desktop-full.png"), fullPage: true });
  await ctx.close();
});

await test("every image has alt text and loads", async () => {
  const { ctx, page } = await openPage();
  await page.evaluate(async () => {
    for (const img of document.images) { img.loading = "eager"; img.scrollIntoView(); }
    await new Promise((r) => setTimeout(r, 800));
  });
  const bad = await page.evaluate(() => [...document.images]
    .filter((i) => !i.closest("dialog"))
    .filter((i) => !i.hasAttribute("alt") || (i.closest("figure") && !i.alt) || !i.complete || i.naturalWidth === 0)
    .map((i) => i.currentSrc || i.src));
  const unsized = await page.evaluate(() => [...document.querySelectorAll("main img")].filter((i) => !i.getAttribute("width")).map((i) => i.src));
  eq(unsized.length, 0, `images without width and height (layout shift) ${unsized.join(", ")}`);
  eq(bad.length, 0, `broken or alt-less images ${bad.join(", ")}`);
  await ctx.close();
});

await test("video has a source, poster and captions, and its metadata loads", async () => {
  const { ctx, page } = await openPage();
  const info = await page.evaluate(async () => {
    const v = document.querySelector("video");
    if (v.readyState < 1) await new Promise((r) => { v.addEventListener("loadedmetadata", r, { once: true }); setTimeout(r, 8000); });
    const track = v.querySelector("track");
    return { duration: v.duration, poster: v.poster, track: track && track.getAttribute("src"), w: v.videoWidth, h: v.videoHeight };
  });
  assert(info.duration > 60 && info.duration < 300, `video duration ${info.duration}`);
  eq(info.w, 1280, "video width");
  assert(info.poster.endsWith("poster.jpg"), "poster set");
  const vtt = await (await fetch(`${BASE}/${info.track}`)).text();
  assert(vtt.startsWith("WEBVTT") && vtt.split("-->").length > 20, "captions file has cues");
  const poster = await fetch(info.poster);
  eq(poster.status, 200, "poster loads");
  await ctx.close();
});

await test("every in-page link points at an existing section", async () => {
  const { ctx, page } = await openPage();
  const missing = await page.evaluate(() => [...document.querySelectorAll('a[href^="#"]')]
    .map((a) => a.getAttribute("href")).filter((h) => h.length > 1 && !document.querySelector(h)));
  eq(missing.length, 0, `missing anchors ${missing.join(", ")}`);
  await ctx.close();
});

await test("mobile (390px): no sideways scroll, CTA and form usable", async () => {
  const { ctx, page } = await openPage({ viewport: { width: 390, height: 844 } });
  const sw = await page.evaluate(() => document.documentElement.scrollWidth);
  assert(sw <= 390, `page is ${sw}px wide at 390px`);
  assert(await page.locator(".hero .btn-primary").isVisible(), "hero CTA visible");
  const box = await page.locator("#submit").boundingBox();
  assert(box && box.width > 300 && box.height >= 44, "submit button is a good tap target");
  await page.screenshot({ path: path.join(SHOTS, "mobile-full.png"), fullPage: true });
  await ctx.close();
});

await test("tablet (820px): no sideways scroll", async () => {
  const { ctx, page } = await openPage({ viewport: { width: 820, height: 1180 } });
  const sw = await page.evaluate(() => document.documentElement.scrollWidth);
  assert(sw <= 820, `page is ${sw}px wide at 820px`);
  await ctx.close();
});

await test("header 'Book a demo' scrolls to the form", async () => {
  const { ctx, page } = await openPage();
  // Reduced motion makes the jump instant (the page honours it), so the check
  // tests the anchor and the sticky-header offset, not animation timing.
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.click(".site-header .btn-primary");
  await page.waitForFunction(() => window.scrollY > 0);
  await page.waitForTimeout(300);
  const top = await page.evaluate(() => document.getElementById("book").getBoundingClientRect().top);
  assert(top >= 0 && top < 120, `form section top at ${top}`);
  const headerBottom = await page.evaluate(() => document.querySelector(".site-header").getBoundingClientRect().bottom);
  const formTop = await page.evaluate(() => document.querySelector("#book .kicker").getBoundingClientRect().top);
  assert(formTop > headerBottom, "section heading is not hidden under the sticky header");
  await ctx.close();
});


await test("stated video length matches the real video", async () => {
  const { ctx, page } = await openPage();
  const r = await page.evaluate(async () => {
    const v = document.querySelector("video");
    if (v.readyState < 1) await new Promise((res) => { v.addEventListener("loadedmetadata", res, { once: true }); setTimeout(res, 8000); });
    return { d: v.duration, cap: document.querySelector(".video-card figcaption").textContent, label: v.getAttribute("aria-label") };
  });
  const m = r.cap.match(/(\d+) minutes (\d+) seconds/);
  assert(m, "caption states the length");
  const stated = Number(m[1]) * 60 + Number(m[2]);
  assert(Math.abs(stated - r.d) < 1.5, `stated ${stated}s, real ${r.d.toFixed(1)}s`);
  assert(r.label.includes(`${m[1]} minutes ${m[2]} seconds`), "aria-label matches");
  await ctx.close();
});

await test("unapproved offer terms are not in the page, and approved lines can be added from config", async () => {
  const html = fs.readFileSync(path.join(ROOT, "index.html"), "utf8").toLowerCase();
  for (const t of ["fixed for four years", "build-out", "three to four meetings", "small number of firms", "data-pending"]) {
    assert(!html.includes(t), `page source contains "${t}"`);
  }
  const { ctx, page } = await openPage({ config: TEST_CONFIG({ extraOfferItems: ["Approved test line.", "<b>not html</b>"] }) });
  const items = await page.evaluate(() => [...document.querySelectorAll("#offer-stack li")].map((li) => li.innerHTML));
  assert(items.includes("Approved test line."), "approved line added");
  assert(items.includes("&lt;b&gt;not html&lt;/b&gt;"), "config text is escaped, never injected as HTML");
  await ctx.close();
});

await test("placeholder proof is visibly labelled so it cannot pass as a real result", async () => {
  const { ctx, page } = await openPage();
  const blocks = await page.evaluate(() => [...document.querySelectorAll(".proof-card.placeholder")].map((el) => ({
    badge: el.querySelector(".ph-badge") && el.querySelector(".ph-badge").offsetParent !== null ? el.querySelector(".ph-badge").textContent : "",
  })));
  assert(blocks.length > 0, "placeholder cards present (remove this test once real proof replaces them)");
  assert(blocks.every((b) => /placeholder/i.test(b.badge)), "every placeholder card shows a visible Placeholder badge");
  const text = await page.evaluate(() => [...document.querySelectorAll(".proof-card.placeholder")].map((el) => el.innerText).join(" "));
  assert(!/\b\d+ of \d+\b/.test(text) && text.includes("[") && text.includes("goes here"), "placeholders are visible slots, not invented results");
  const robots = await page.getAttribute('meta[name="robots"]', "content");
  eq(robots, "noindex", "kept out of search engines while placeholders are on the page");
  await ctx.close();
});

await test("footer matches the AgenticPM family layout, and every footer link resolves", async () => {
  const { ctx, page } = await openPage();
  const f = await page.evaluate(() => {
    const footer = document.querySelector(".site-footer");
    const heads = [...footer.querySelectorAll(".footer-head")].map((h) => h.textContent.trim());
    const links = [...footer.querySelectorAll("a[href]")].map((a) => ({ href: a.getAttribute("href"), text: a.textContent.trim() || a.getAttribute("aria-label"), target: a.target, rel: a.rel }));
    return { heads, links, family: footer.querySelector(".footer-family").textContent, privacy: !!footer.querySelector("#privacy"), bg: getComputedStyle(footer).backgroundColor };
  });
  eq(f.heads.join(","), "Product,Company,Get Started,Legal", "column headings");
  assert(/AgenticPM family/.test(f.family), "family line present");
  assert(f.privacy, "consent checkbox's #privacy target lives in the footer");
  eq(f.bg, "rgb(241, 245, 249)", "light slate background, as on agenticprivatemarkets.ai");
  for (const l of f.links) {
    if (l.href.startsWith("#")) {
      const ok = await page.evaluate((h) => !!document.querySelector(h), l.href);
      assert(ok, `in-page footer link ${l.href} has a target`);
    } else if (l.href.startsWith("http")) {
      assert(/^https:\/\//.test(l.href), `external link uses https: ${l.href}`);
      assert(l.target === "_blank" && l.rel.includes("noopener"), `external link opens safely: ${l.href}`);
    } else {
      eq(l.href, "mailto:dash@craftarc.ai", "contact link");
    }
  }
  assert(f.links.some((l) => l.href.includes("legal/privacy-policy")) && f.links.some((l) => l.href.includes("trust.agenticprivatemarkets.ai")), "legal links present");
  await ctx.close();
});

await test("product screens enlarge in a viewer and close with Escape", async () => {
  const { ctx, page } = await openPage();
  const btn = page.locator("#how .zoom").nth(2);
  await btn.scrollIntoViewIfNeeded();
  await btn.click();
  await page.waitForSelector("#viewer[open]");
  const loaded = await page.evaluate(async () => {
    const img = document.querySelector("#viewer img");
    if (!img.complete) await new Promise((r) => img.addEventListener("load", r, { once: true }));
    return { w: img.naturalWidth, alt: img.alt };
  });
  assert(loaded.w > 1800, `full screen loads (${loaded.w}px)`);
  assert(loaded.alt.length > 10, "viewer image has alt text");
  await page.keyboard.press("Escape");
  await page.waitForFunction(() => !document.getElementById("viewer").open);
  await ctx.close();
});

await test("optional questions start folded so the form shows five fields", async () => {
  const { ctx, page } = await openPage();
  eq(await page.evaluate(() => document.getElementById("more").open), false, "optional section closed");
  const visible = await page.evaluate(() => [...document.querySelectorAll("#lead-form input, #lead-form select, #lead-form textarea")]
    .filter((el) => !el.closest(".hp") && el.type !== "checkbox" && el.checkVisibility({ contentVisibilityAuto: true, visibilityProperty: true }))
    .map((el) => el.id));
  eq(visible.join(","), "name,email,firm,role,timing", "visible fields");
  await ctx.close();
});

// ---------------------------------------------------------------- leads
await test("lead form: empty submit shows every required error, focuses the first, sends nothing", async () => {
  const before = leads.length;
  const { ctx, page } = await openPage();
  await page.click("#submit");
  for (const id of ["name", "email", "firm", "role", "consent"]) {
    assert(await page.locator(`#${id}-err`).isVisible(), `${id} error visible`);
    eq(await page.getAttribute(`#${id}`, "aria-invalid"), "true", `${id} aria-invalid`);
  }
  eq(await page.evaluate(() => document.activeElement.id), "name", "focus on first invalid field");
  assert((await page.textContent("#form-status")).includes("check"), "status explains the problem");
  eq(leads.length, before, "no lead sent");
  await page.screenshot({ path: path.join(SHOTS, "form-errors.png"), clip: await page.locator("#lead-form").boundingBox() });
  await ctx.close();
});

await test("lead form: bad email is rejected, and fixing it clears the error", async () => {
  const before = leads.length;
  const { ctx, page } = await openPage();
  await fillValid(page, { email: "alex@nodomain" });
  await page.click("#submit");
  assert(await page.locator("#email-err").isVisible(), "email error visible");
  eq(leads.length, before, "no lead sent");
  await page.fill("#email", "alex@examplecapital.com");
  await page.locator("#email").blur();
  assert(!(await page.locator("#email-err").isVisible()), "email error cleared");
  await ctx.close();
});

await test("lead form: valid submission posts the full lead, scores it hot and thanks the visitor", async () => {
  const before = leads.length;
  const { ctx, page } = await openPage({ query: "?utm_source=linkedin&utm_medium=paid&utm_campaign=coo-q1&li_fat_id=abc123" });
  await page.evaluate(() => { window.dataLayer = []; });
  const v = await fillValid(page);
  await page.click("#submit");
  await page.waitForSelector("#thanks:not([hidden])", { timeout: 5000 });
  eq(leads.length, before + 1, "exactly one lead stored");
  const lead = leads[leads.length - 1];
  eq(lead.headers["content-type"], "application/json", "content type");
  const b = lead.body;
  for (const k of ["name", "email", "firm", "role", "aum", "team", "timing", "framework", "message"]) eq(b[k], v[k], `field ${k}`);
  eq(b.consent, true, "consent");
  eq(b.email_type, "work", "email type");
  eq(b.fit_score, 100, "fit score");
  eq(b.priority, "hot", "priority");
  eq(b.utm_source, "linkedin", "utm_source");
  eq(b.utm_campaign, "coo-q1", "utm_campaign");
  eq(b.li_fat_id, "abc123", "li_fat_id");
  eq(b.source, "craftarc-website", "source");
  assert(!("company_website" in b), "honeypot not sent");
  assert(!Number.isNaN(Date.parse(b.submitted_at)), "timestamp");
  assert(await page.locator("#lead-form").isHidden(), "form hidden after success");
  eq(await page.evaluate(() => document.activeElement.id), "thanks", "focus moves to thank-you");
  const events = await page.evaluate(() => window.dataLayer.map((e) => e.event));
  assert(events.includes("lead_submitted"), "lead_submitted pushed to dataLayer");
  await page.screenshot({ path: path.join(SHOTS, "form-thanks.png"), clip: await page.locator("#book").boundingBox() });
  await ctx.close();
});

await test("lead form: attribution survives moving between pages in the session", async () => {
  const before = leads.length;
  const { ctx, page } = await openPage({ query: "?utm_source=newsletter&utm_campaign=nov" });
  await page.goto(`${BASE}/#book`);
  await fillValid(page);
  await page.click("#submit");
  await page.waitForSelector("#thanks:not([hidden])");
  eq(leads.length, before + 1, "one lead");
  eq(leads[leads.length - 1].body.utm_source, "newsletter", "first-touch utm kept");
  await ctx.close();
});

await test("lead form: double click sends one lead only", async () => {
  const before = leads.length;
  const { ctx, page } = await openPage();
  await fillValid(page);
  await page.locator("#submit").dblclick();
  await page.waitForSelector("#thanks:not([hidden])");
  await page.waitForTimeout(400);
  eq(leads.length, before + 1, "one lead after double click");
  await ctx.close();
});

await test("lead form: personal email is accepted but tagged and scored lower", async () => {
  const before = leads.length;
  const { ctx, page } = await openPage();
  await fillValid(page, { email: "alex.morgan@gmail.com" });
  await page.click("#submit");
  await page.waitForSelector("#thanks:not([hidden])");
  eq(leads.length, before + 1, "lead stored");
  const b = leads[leads.length - 1].body;
  eq(b.email_type, "personal", "email type");
  eq(b.fit_score, 90, "score lowered by 10");
  await ctx.close();
});

await test("lead form: scoring separates warm and nurture leads", async () => {
  const { ctx, page } = await openPage();
  const warm = await page.evaluate(() => window.__craftarc.scoreLead({ role: "partner_md", aum: "1to2b", timing: "q2_2027", framework: "draft", team: "10to25", email_type: "work" }));
  eq(warm.priority, "warm", "partner, $1B to $2B, Q2");
  const nurture = await page.evaluate(() => window.__craftarc.scoreLead({ role: "other", aum: "lt1b", timing: "unsure", framework: "no", team: "lt10", email_type: "personal" }));
  eq(nurture.priority, "nurture", "small firm, unsure");
  eq(nurture.fit_score, 7, "nurture score");
  await ctx.close();
});

await test("lead form: only the required fields are needed", async () => {
  const before = leads.length;
  const { ctx, page } = await openPage();
  await page.fill("#name", "Sam Lee");
  await page.fill("#email", "sam@firm.com");
  await page.fill("#firm", "Firm Partners");
  await page.selectOption("#role", "partner_md");
  await page.check("#consent");
  await page.click("#submit");
  await page.waitForSelector("#thanks:not([hidden])");
  eq(leads.length, before + 1, "lead stored");
  const b = leads[leads.length - 1].body;
  eq(b.aum, "", "aum blank");
  eq(b.priority, "nurture", "unknowns score low");
  await ctx.close();
});

await test("lead form: honeypot filled by a bot sends nothing but looks successful", async () => {
  const before = leads.length;
  const { ctx, page } = await openPage();
  await fillValid(page);
  await page.evaluate(() => { document.getElementById("company_website").value = "http://spam.example"; });
  await page.click("#submit");
  await page.waitForSelector("#thanks:not([hidden])");
  await page.waitForTimeout(300);
  eq(leads.length, before, "bot lead dropped");
  await ctx.close();
});

await test("lead form: server error keeps the visitor's input, explains, and a retry succeeds", async () => {
  const before = leads.length;
  const { ctx, page } = await openPage();
  await fillValid(page);
  failNext = 1;
  await page.click("#submit");
  await page.waitForFunction(() => document.getElementById("form-status").classList.contains("is-error"));
  assert((await page.textContent("#form-status")).includes("not sent"), "error message shown");
  eq(await page.inputValue("#name"), "Alex Morgan", "input kept");
  assert(await page.isEnabled("#submit"), "button re-enabled");
  eq(await page.textContent("#submit"), "Request my demo", "button label restored");
  await page.click("#submit");
  await page.waitForSelector("#thanks:not([hidden])");
  eq(leads.length, before + 1, "retry stored the lead");
  await ctx.close();
});

await test("lead form: network failure is handled the same way", async () => {
  const { ctx, page } = await openPage({ config: TEST_CONFIG({ leadEndpoint: "http://127.0.0.1:9/api/lead", leadEmail: "demo@example.com" }) });
  await fillValid(page);
  await page.click("#submit");
  await page.waitForFunction(() => document.getElementById("form-status").classList.contains("is-error"));
  assert((await page.textContent("#form-status")).includes("demo@example.com"), "fallback email offered");
  assert(await page.locator("#lead-form").isVisible(), "form still visible");
  await ctx.close();
});

await test("lead form: keyboard only, Enter submits", async () => {
  const before = leads.length;
  const { ctx, page } = await openPage();
  await fillValid(page);
  await page.focus("#firm");
  await page.keyboard.press("Enter");
  await page.waitForSelector("#thanks:not([hidden])");
  eq(leads.length, before + 1, "lead stored via keyboard");
  await ctx.close();
});

await test("lead form: with no endpoint and no email it fails loudly, never silently", async () => {
  const before = leads.length;
  const { ctx, page, errors } = await openPage({ config: TEST_CONFIG({ leadEndpoint: "", leadEmail: "" }) });
  await fillValid(page);
  await page.click("#submit");
  assert((await page.textContent("#form-status")).includes("not connected"), "visitor told");
  assert(errors.some((e) => e.includes("leadEndpoint")), "console error for the site owner");
  eq(leads.length, before, "nothing sent");
  await ctx.close();
});

await test("lead form: with only an email configured it opens a filled-in email", async () => {
  const { ctx, page } = await openPage({ config: TEST_CONFIG({ leadEndpoint: "", leadEmail: "demo@example.com" }) });
  await page.evaluate(() => { window.__craftarcNavigate = (h) => { window.__lastMailto = h; }; });
  await fillValid(page);
  await page.click("#submit");
  const url = await page.evaluate(() => window.__lastMailto || "");
  assert(url.startsWith("mailto:demo%40example.com"), `mailto opened: ${url.slice(0, 60)}`);
  const decoded = decodeURIComponent(url);
  assert(decoded.includes("Example Capital") && decoded.includes("alex.morgan@examplecapital.com"), "mail has the lead details");
  assert(await page.locator("#thanks").isVisible(), "thank-you shown");
  assert((await page.textContent("#thanks-msg")).includes("demo@example.com"), "thank-you says the email app should open, and gives the address");
  assert((await page.textContent("#thanks h3")).includes("press send"), "heading asks the visitor to press send");
  await ctx.close();
});

await test("lead form: labels are tied to inputs and the status is announced", async () => {
  const { ctx, page } = await openPage();
  const unlabeled = await page.evaluate(() => [...document.querySelectorAll("#lead-form input, #lead-form select, #lead-form textarea")]
    .filter((el) => el.type !== "hidden" && !document.querySelector(`label[for="${el.id}"]`)).map((el) => el.id));
  eq(unlabeled.length, 0, `unlabelled fields ${unlabeled.join(", ")}`);
  eq(await page.getAttribute("#form-status", "aria-live"), "polite", "live region");
  await ctx.close();
});

await test("production config.js is valid and documents how to connect leads", async () => {
  const src = fs.readFileSync(path.join(ROOT, "config.js"), "utf8");
  assert(src.includes("leadEndpoint") && src.includes("leadEmail"), "keys present");
  const sandbox = {};
  new Function("window", src)(sandbox);
  assert(Array.isArray(sandbox.CRAFTARC_CONFIG.personalEmailDomains), "domains list");
  assert(sandbox.CRAFTARC_CONFIG.leadEmail === "dash@craftarc.ai" || sandbox.CRAFTARC_CONFIG.leadEndpoint, "leads go somewhere");
});

await browser.close();
server.close();
const failed = results.filter((r) => !r.ok);
console.log(`\n${results.length - failed.length} passed, ${failed.length} failed`);
fs.writeFileSync(path.join(ROOT, "tests", "e2e-results.json"), JSON.stringify({ run_at: new Date().toISOString(), results }, null, 1));
process.exit(failed.length ? 1 : 0);
