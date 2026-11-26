// End-to-end tests for the CraftArc website (Next.js static export in website/out).
// Run: node website/tests/e2e.mjs   after `npm run build` in website/ (check_all.sh does both).
// Serves out/ on a local port with a mock lead endpoint that records every POST.
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const SITE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const ROOT = path.join(SITE, "out");
const SHOTS = path.join(SITE, "tests", "screenshots");
fs.mkdirSync(SHOTS, { recursive: true });
if (!fs.existsSync(path.join(ROOT, "index.html"))) { console.error("No build found: run `npm run build` in website/ first."); process.exit(1); }

// ---------------------------------------------------------------- server
const leads = [];
let failNext = 0;
const TYPES = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".svg": "image/svg+xml", ".woff2": "font/woff2", ".txt": "text/plain", ".json": "application/json" };
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
  res.writeHead(200, { "Content-Type": TYPES[path.extname(file)] || "application/octet-stream" });
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

async function openPage({ viewport = { width: 1366, height: 900 }, config = TEST_CONFIG(), query = "", path: p = "", reducedMotion } = {}) {
  const ctx = await browser.newContext({ viewport, reducedMotion });
  const page = await ctx.newPage();
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });
  await page.route(/fonts\.(googleapis|gstatic)\.com/, (r) => r.fulfill({ status: 200, contentType: "text/css", body: "" }));
  await page.route("**/config.js", (r) => r.fulfill({ contentType: "text/javascript", body: config }));
  await page.goto(`${BASE}/${p}${query}`, { waitUntil: "load" });
  await page.waitForFunction(() => document.readyState === "complete");
  await page.waitForTimeout(250); // hydration
  return { ctx, page, errors };
}

async function openForm(page) {
  await page.click('header [data-cta="header"]');
  await page.waitForSelector("#briefing[open]");
}

async function fillValid(page, over = {}) {
  const v = { name: "Alex Morgan", role: "CEO", company: "Example Industrial", email: "alex.morgan@exampleindustrial.com", message: "We want a read on our top 40 leaders.", ...over };
  await page.fill("#bf-name", v.name);
  await page.fill("#bf-role", v.role);
  await page.fill("#bf-company", v.company);
  await page.fill("#bf-email", v.email);
  if (v.message) await page.fill("#bf-message", v.message);
  return v;
}

console.log(`\nCraftArc website tests against ${BASE}\n`);

// ---------------------------------------------------------------- page
await test("page loads with no console errors, one h1 and the spec's headline", async () => {
  const { ctx, page, errors } = await openPage();
  eq(await page.locator("h1").count(), 1, "h1 count");
  eq((await page.textContent("h1")).trim(), "Can you tell if your company has a gap in leadership depth?", "h1 text");
  assert((await page.title()).includes("CraftArc"), "title mentions CraftArc");
  const desc = await page.getAttribute('meta[name="description"]', "content");
  assert(desc && desc.length > 60 && desc.length < 170, `meta description length ${desc && desc.length}`);
  const robots = await page.getAttribute('meta[name="robots"]', "content");
  assert(/noindex/.test(robots || ""), "kept out of search engines until launch");
  eq(errors.length, 0, `console errors ${errors.join(" | ")}`);
  await page.screenshot({ path: path.join(SHOTS, "desktop-full.png"), fullPage: true });
  await ctx.close();
});

await test("no photos, screenshots or video: every visual is drawn in code", async () => {
  const { ctx, page } = await openPage();
  const raster = await page.$$eval("img", (els) => els.map((i) => i.getAttribute("src")).filter((s) => !/\.svg$/.test(s || "")));
  eq(raster.length, 0, `raster images ${raster.join(", ")}`);
  eq(await page.locator("main video").count(), 0, "no video element on load");
  assert((await page.locator("main svg").count()) > 15, "inline SVG visuals present");
  await ctx.close();
});

await test("nine sections in the spec's order", async () => {
  const { ctx, page } = await openPage();
  const ids = await page.$$eval("main > section", (els) => els.map((e) => e.id));
  eq(ids.join(","), "top,why-now,promises,how,difference,board,trust,setup,final", "section order");
  await ctx.close();
});

await test("navbar: sticky, four anchor links that land, and Book a Briefing opens the form", async () => {
  const { ctx, page } = await openPage();
  eq(await page.evaluate(() => getComputedStyle(document.querySelector("header")).position), "sticky", "sticky header");
  const links = await page.$$eval('header nav a', (els) => els.map((a) => [a.textContent.trim(), a.getAttribute("href")]));
  eq(links.map((l) => l[0]).join(" | "), "How It Works | Board View | Trust | Setup", "nav labels");
  for (const [, href] of links) assert(await page.evaluate((h) => !!document.querySelector(h), href), `${href} exists`);
  eq((await page.textContent('header [data-cta="header"]')).trim(), "Book a Briefing", "header CTA wording");
  await openForm(page);
  await ctx.close();
});

await test("hero: the question, the sub-question, the resolution and two calls to action", async () => {
  const { ctx, page } = await openPage();
  const t = await page.textContent("#top");
  assert(t.includes("What are the risks associated with your current leadership profile?"), "sub-question");
  assert(t.includes("CraftArc answers both, with evidence, not opinion."), "resolution");
  eq((await page.textContent('#top [data-cta="hero"]')).trim(), "Book a Briefing", "primary CTA");
  assert((await page.textContent('#top [data-cta="watch"]')).includes("Watch the 60s Story"), "secondary CTA");
  assert(await page.locator("#video .sample-badge").isVisible(), "preview is labeled as sample data");
  assert(await page.locator('[data-cta="watch-pill"]').isVisible(), "play pill visible");
  await ctx.close();
});

await test("hero story: opens in a lightbox, plays five beats, steps on click, closes with Escape", async () => {
  const { ctx, page } = await openPage();
  await page.evaluate(() => { window.__craftarcBeatMs = 400; });
  await page.click('#top [data-cta="watch"]');
  await page.waitForSelector("#story[open]");
  await page.waitForFunction(() => Number(document.querySelector("#story [data-beat]").dataset.beat) >= 1, null, { timeout: 4000 });
  await page.click('#story [role="tab"]:nth-child(4)');
  eq(await page.textContent("#story-title"), "Continuous coaching", "jumps to beat 4");
  await page.keyboard.press("Escape");
  await page.waitForFunction(() => !document.getElementById("story").open);
  await page.click('[data-cta="watch-pill"]');
  await page.waitForSelector("#story[open]");
  await page.mouse.click(5, 5); // backdrop
  await page.waitForFunction(() => !document.getElementById("story").open);
  await ctx.close();
});

await test("urgency strip: three figures, each with a source link that opens safely", async () => {
  const { ctx, page } = await openPage();
  const s = await page.$$eval("#why-now a", (els) => els.map((a) => ({ href: a.href, t: a.target, r: a.rel })));
  eq(s.length, 3, "three sources");
  assert(s.every((x) => x.href.startsWith("https://") && x.t === "_blank" && x.r.includes("noopener")), "sources are https and open safely");
  const text = await page.textContent("#why-now");
  for (const v of ["1 in 4", "17%", "1/3+"]) assert(text.includes(v), `figure ${v}`);
  await ctx.close();
});

await test("three promises: Know, Grow and Without the time, each with a visual and three outcomes", async () => {
  const { ctx, page } = await openPage();
  const cards = await page.$$eval("#promises article", (els) => els.map((e) => ({ t: e.querySelector("h3").textContent, n: e.querySelectorAll("ul > li").length, v: !!e.querySelector("[data-sample]") })));
  eq(cards.map((c) => c.t).join(" | "), "Know | Grow | Without the time", "titles");
  assert(cards.every((c) => c.n === 3 && c.v), "three outcomes and a visual each");
  await ctx.close();
});

await test("four-part cycle: Part 1 by default, clicking and arrow keys switch the product frame", async () => {
  const { ctx, page } = await openPage();
  const tabs = page.locator('#how [role="tab"]');
  eq(await tabs.count(), 4, "four parts");
  eq(await tabs.nth(0).getAttribute("aria-selected"), "true", "Part 1 selected");
  assert((await tabs.nth(0).textContent()).includes("Define What Great Looks Like"), "STANDARD_WORD in Part 1");
  assert((await page.textContent("#part-panel")).includes("Part 1: Leadership framework"), "Part 1 frame");
  await tabs.nth(2).click();
  assert((await page.textContent("#part-panel")).includes("Coach check-in"), "Part 3 frame");
  await tabs.nth(2).focus();
  await page.keyboard.press("ArrowDown");
  assert((await page.textContent("#part-panel")).includes("Board pack summary"), "arrow key moves to Part 4");
  assert((await tabs.nth(3).textContent()).includes("In development"), "Part 4 marked as in development");
  await page.click("#how svg g.cursor-pointer >> nth=1");
  assert((await page.textContent("#part-panel")).includes("Evaluator brief"), "diagram node selects Part 2");
  await ctx.close();
});

await test("forms vs conversation: the headline and the six-row comparison", async () => {
  const { ctx, page } = await openPage();
  eq((await page.textContent("#difference h2")).trim(), "Other tools collect forms. CraftArc holds the conversation.", "headline");
  const rows = await page.$$eval("#difference tbody th", (els) => els.map((e) => e.textContent));
  eq(rows.join(" | "), "How feedback is gathered | What it captures | The framework | Who writes it up | How it ends | Between reviews", "rows");
  await ctx.close();
});

await test("board view: sample-data badge, key insights and five tabs that each draw a chart", async () => {
  const { ctx, page } = await openPage();
  assert(await page.locator("#board .sample-badge").first().isVisible(), "Illustrative Sample Data badge visible");
  assert((await page.textContent("#board")).includes("The real risk is the Partner layer"), "key insights");
  const tabs = page.locator('#board [role="tab"]');
  eq(await tabs.count(), 5, "five tabs");
  const labels = await tabs.allTextContents();
  eq(labels.join(" | "), "Gap to Target | Trajectory | Competencies in Focus | Managing Out | Development Efforts", "tab labels");
  for (let i = 0; i < 5; i++) {
    await tabs.nth(i).click();
    const panel = page.locator('#board [role="tabpanel"]:not([hidden])');
    await panel.locator("svg.recharts-surface").first().waitFor({ timeout: 5000 });
    eq(await page.locator('#board [role="tabpanel"]:not([hidden])').count(), 1, `one panel at a time (tab ${i + 1})`);
  }
  await tabs.nth(4).focus();
  await page.keyboard.press("ArrowRight");
  eq(await tabs.nth(0).getAttribute("aria-selected"), "true", "arrow keys wrap to the first tab");
  await ctx.close();
});

await test("trust, proof and setup: four pillars, the decision flow, two cards and three steps", async () => {
  const { ctx, page } = await openPage();
  eq(await page.locator("#trust dt").count(), 4, "four pillars");
  assert(await page.locator('#trust svg[role="img"]').isVisible(), "architecture diagram");
  assert((await page.textContent("#trust")).includes("People make every call."), "people decide");
  eq(await page.locator("#setup article").count(), 2, "two cards");
  eq(await page.locator("#setup ol li").count(), 3, "three steps");
  await ctx.close();
});

await test("final call to action opens the briefing form", async () => {
  const { ctx, page } = await openPage();
  eq((await page.textContent('#final [data-cta="final"]')).trim(), "Schedule an Executive Briefing", "wording");
  await page.click('#final [data-cta="final"]');
  await page.waitForSelector("#briefing[open]");
  await ctx.close();
});

// ---------------------------------------------------------------- briefing form
await test("briefing form: accessible dialog, focus on the first field, Escape closes and returns focus", async () => {
  const { ctx, page } = await openPage();
  await page.focus('#top [data-cta="hero"]');
  await page.keyboard.press("Enter");
  await page.waitForSelector("#briefing[open]");
  eq(await page.getAttribute("#briefing", "aria-modal"), "true", "aria-modal");
  assert(await page.getAttribute("#briefing", "aria-labelledby"), "labelled");
  await page.waitForFunction(() => document.activeElement && document.activeElement.id === "bf-name");
  const unlabeled = await page.evaluate(() => [...document.querySelectorAll("#briefing-form input, #briefing-form textarea")]
    .filter((el) => !document.querySelector(`label[for="${el.id}"]`)).map((el) => el.id));
  eq(unlabeled.length, 0, `unlabeled fields ${unlabeled.join(", ")}`);
  await page.keyboard.press("Escape");
  await page.waitForFunction(() => !document.getElementById("briefing").open);
  eq(await page.evaluate(() => document.activeElement.getAttribute("data-cta")), "hero", "focus returns to the button that opened it");
  await ctx.close();
});

await test("briefing form: empty submit shows every required error, focuses the first, sends nothing", async () => {
  const before = leads.length;
  const { ctx, page } = await openPage();
  await openForm(page);
  await page.click("#bf-submit");
  for (const id of ["name", "role", "company", "email"]) {
    assert(await page.locator(`#bf-${id}-err`).isVisible(), `${id} error visible`);
    eq(await page.getAttribute(`#bf-${id}`, "aria-invalid"), "true", `${id} aria-invalid`);
  }
  eq(await page.evaluate(() => document.activeElement.id), "bf-name", "focus on first invalid field");
  assert((await page.textContent("#bf-status")).includes("check"), "status explains the problem");
  eq(leads.length, before, "no lead sent");
  await page.screenshot({ path: path.join(SHOTS, "form-errors.png") });
  await ctx.close();
});

await test("briefing form: valid submission posts the lead, scores it and thanks the visitor", async () => {
  const before = leads.length;
  const { ctx, page } = await openPage({ query: "?utm_source=linkedin&utm_medium=paid&utm_campaign=ceo-q1&li_fat_id=abc123" });
  await openForm(page);
  const v = await fillValid(page);
  await page.click("#bf-submit");
  await page.waitForSelector("#bf-thanks", { timeout: 5000 });
  eq(leads.length, before + 1, "exactly one lead stored");
  const lead = leads[leads.length - 1];
  eq(lead.headers["content-type"], "application/json", "content type");
  const b = lead.body;
  for (const k of ["name", "role", "company", "email", "message"]) eq(b[k], v[k], `field ${k}`);
  eq(b.email_type, "work", "email type");
  eq(b.priority, "hot", "a CEO with a work email is a hot lead");
  eq(b.utm_source, "linkedin", "utm_source");
  eq(b.li_fat_id, "abc123", "li_fat_id");
  eq(b.source, "craftarc-website", "source");
  assert(!("company_website" in b), "honeypot not sent");
  assert(!Number.isNaN(Date.parse(b.submitted_at)), "timestamp");
  eq(await page.evaluate(() => document.activeElement.id), "bf-thanks", "focus moves to the thank-you");
  const events = await page.evaluate(() => (window.dataLayer || []).map((e) => e.event));
  assert(events.includes("lead_submitted") && events.includes("cta_click"), "analytics events pushed");
  await page.screenshot({ path: path.join(SHOTS, "form-thanks.png") });
  await ctx.close();
});

await test("briefing form: bad email is rejected, and fixing it clears the error", async () => {
  const before = leads.length;
  const { ctx, page } = await openPage();
  await openForm(page);
  await fillValid(page, { email: "alex@nodomain" });
  await page.click("#bf-submit");
  assert(await page.locator("#bf-email-err").isVisible(), "email error visible");
  eq(leads.length, before, "no lead sent");
  await page.fill("#bf-email", "alex@exampleindustrial.com");
  assert(!(await page.locator("#bf-email-err").isVisible()), "email error cleared");
  await ctx.close();
});

await test("briefing form: honeypot filled by a bot sends nothing but looks successful", async () => {
  const before = leads.length;
  const { ctx, page } = await openPage();
  await openForm(page);
  await fillValid(page);
  await page.evaluate(() => { document.getElementById("bf-website").value = "http://spam.example"; });
  await page.click("#bf-submit");
  await page.waitForSelector("#bf-thanks");
  await page.waitForTimeout(300);
  eq(leads.length, before, "bot lead dropped");
  await ctx.close();
});

await test("briefing form: double click sends one lead only", async () => {
  const before = leads.length;
  const { ctx, page } = await openPage();
  await openForm(page);
  await fillValid(page);
  await page.locator("#bf-submit").dblclick();
  await page.waitForSelector("#bf-thanks");
  await page.waitForTimeout(400);
  eq(leads.length, before + 1, "one lead after double click");
  await ctx.close();
});

await test("briefing form: server error keeps the input, explains, and a retry succeeds", async () => {
  const before = leads.length;
  const { ctx, page } = await openPage();
  await openForm(page);
  await fillValid(page);
  failNext = 1;
  await page.click("#bf-submit");
  await page.waitForFunction(() => document.getElementById("bf-status").textContent.includes("not sent"));
  eq(await page.inputValue("#bf-name"), "Alex Morgan", "input kept");
  eq((await page.textContent("#bf-submit")).trim(), "Request my briefing", "button label restored");
  await page.click("#bf-submit");
  await page.waitForSelector("#bf-thanks");
  eq(leads.length, before + 1, "retry stored the lead");
  await ctx.close();
});

await test("briefing form: network failure offers the fallback email", async () => {
  const { ctx, page } = await openPage({ config: TEST_CONFIG({ leadEndpoint: "http://127.0.0.1:9/api/lead", leadEmail: "demo@example.com" }) });
  await openForm(page);
  await fillValid(page);
  await page.click("#bf-submit");
  await page.waitForFunction(() => document.getElementById("bf-status").textContent.includes("demo@example.com"));
  assert(await page.locator("#briefing-form").isVisible(), "form still visible");
  await ctx.close();
});

await test("briefing form: with only an email configured it opens a filled-in email", async () => {
  const { ctx, page } = await openPage({ config: TEST_CONFIG({ leadEndpoint: "", leadEmail: "demo@example.com" }) });
  await page.evaluate(() => { window.__craftarcNavigate = (h) => { window.__lastMailto = h; }; });
  await openForm(page);
  await fillValid(page);
  await page.click("#bf-submit");
  await page.waitForSelector("#bf-thanks");
  const url = await page.evaluate(() => window.__lastMailto || "");
  assert(url.startsWith("mailto:demo%40example.com"), `mailto opened: ${url.slice(0, 60)}`);
  assert(decodeURIComponent(url).includes("Example Industrial"), "mail has the lead details");
  assert((await page.textContent("#bf-thanks")).includes("press send"), "asks the visitor to press send");
  await ctx.close();
});

await test("briefing form: with no endpoint and no email it fails loudly, never silently", async () => {
  const before = leads.length;
  const { ctx, page, errors } = await openPage({ config: TEST_CONFIG({ leadEndpoint: "", leadEmail: "" }) });
  await openForm(page);
  await fillValid(page);
  await page.click("#bf-submit");
  assert((await page.textContent("#bf-status")).includes("not connected"), "visitor told");
  assert(errors.some((e) => e.includes("leadEndpoint")), "console error for the site owner");
  eq(leads.length, before, "nothing sent");
  await ctx.close();
});

await test("lead scoring favors business leaders over HR, and personal email scores lower", async () => {
  const { ctx, page } = await openPage();
  const s = await page.evaluate(() => ({
    ceo: window.__craftarc.scoreLead({ role: "Chief Executive Officer", email_type: "work", message: "", company: "Acme", email: "a@acme.com" }),
    hr: window.__craftarc.scoreLead({ role: "HR Manager", email_type: "personal", message: "", company: "Acme", email: "a@gmail.com" }),
  }));
  eq(s.ceo.priority, "hot", "CEO, work email");
  eq(s.hr.priority, "nurture", "HR, personal email");
  await ctx.close();
});

await test("attribution survives a reload in the same session", async () => {
  const before = leads.length;
  const { ctx, page } = await openPage({ query: "?utm_source=newsletter&utm_campaign=nov" });
  await page.goto(`${BASE}/`);
  await page.waitForTimeout(250);
  await openForm(page);
  await fillValid(page);
  await page.click("#bf-submit");
  await page.waitForSelector("#bf-thanks");
  eq(leads.length, before + 1, "one lead");
  eq(leads[leads.length - 1].body.utm_source, "newsletter", "first-touch utm kept");
  await ctx.close();
});

await test("?briefing=open opens the form on arrival", async () => {
  const { ctx, page } = await openPage({ query: "?briefing=open" });
  await page.waitForSelector("#briefing[open]");
  await ctx.close();
});

// ---------------------------------------------------------------- footer (Dash: never change it)
await test("footer is byte-for-byte the footer the site had before the rebuild", async () => {
  const { ctx, page } = await openPage();
  const norm = (h) => h.replace(/&copy;/g, "©").replace(/>\s+</g, "><").replace(/\s+/g, " ").trim();
  const live = norm(await page.evaluate(() => document.querySelector(".site-footer").outerHTML));
  // Parse the snapshot in the browser too, so both sides are serialized the same way.
  const raw = fs.readFileSync(path.join(SITE, "tests", "footer.snapshot.html"), "utf8");
  const snap = norm(await page.evaluate((h) => { const t = document.createElement("template"); t.innerHTML = h.trim(); return t.content.firstElementChild.outerHTML; }, raw));
  eq(live === snap, true, "footer markup matches tests/footer.snapshot.html");
  const f = await page.evaluate(() => ({
    heads: [...document.querySelectorAll(".footer-head")].map((h) => h.textContent.trim()),
    bg: getComputedStyle(document.querySelector(".site-footer")).backgroundColor,
    cols: getComputedStyle(document.querySelector(".footer-cols")).gridTemplateColumns.split(" ").length,
  }));
  eq(f.heads.join(","), "Product,Company,Get Started,Legal", "column headings");
  eq(f.bg, "rgb(241, 245, 249)", "light slate background");
  eq(f.cols, 4, "four link columns on desktop");
  await ctx.close();
});

await test("every footer link resolves: anchors on the page, pages that redirect, external links that open safely", async () => {
  const { ctx, page } = await openPage();
  const links = await page.$$eval(".site-footer a[href]", (els) => els.map((a) => ({ href: a.getAttribute("href"), target: a.target, rel: a.rel })));
  for (const l of links) {
    if (l.href.startsWith("http")) {
      assert(l.href.startsWith("https://") && l.target === "_blank" && l.rel.includes("noopener"), `external link opens safely: ${l.href}`);
    } else if (l.href.startsWith("mailto:")) {
      eq(l.href, "mailto:dash@craftarc.ai", "contact link");
    } else {
      const [file, hash] = l.href.split("#");
      const res = await fetch(`${BASE}/${file}`);
      eq(res.status, 200, `${file || "index.html"} loads`);
      if (hash && (file === "" || file === "index.html")) assert(await page.evaluate((h) => !!document.getElementById(h), hash), `#${hash} exists on the page`);
    }
  }
  await ctx.close();
});

await test("old page addresses from the footer land on the right part of the single page", async () => {
  const cases = [
    ["book-a-demo.html", (u) => u.searchParams.get("briefing") === "open"],
    ["private-equity.html", (u) => u.hash === "#video"],
    ["about.html", (u) => u.hash === "#setup"],
  ];
  for (const [p, ok] of cases) {
    const { ctx, page } = await openPage({ path: p, query: "?utm_source=footer-test" });
    await page.waitForURL((u) => !u.pathname.endsWith(".html") || u.pathname.endsWith("index.html"), { timeout: 5000 });
    const u = new URL(page.url());
    assert(ok(u), `${p} lands correctly (${page.url()})`);
    eq(u.searchParams.get("utm_source"), "footer-test", `${p} keeps campaign tags`);
    if (p === "book-a-demo.html") await page.waitForSelector("#briefing[open]");
    await ctx.close();
  }
});

// ---------------------------------------------------------------- layout, review mode, safety
await test("phones (375 and 390) and tablets (820): no sideways scroll, form fits the screen", async () => {
  for (const width of [375, 390, 820]) {
    const { ctx, page } = await openPage({ viewport: { width, height: 844 } });
    const sw = await page.evaluate(() => document.documentElement.scrollWidth);
    assert(sw <= width, `page is ${sw}px wide at ${width}px`);
    if (width === 390) {
      await page.screenshot({ path: path.join(SHOTS, "mobile-full.png"), fullPage: true });
      await openForm(page);
      const box = await page.locator("#briefing").boundingBox();
      assert(box.width <= width && box.x >= 0, "form dialog fits the screen");
      const sb = await page.locator("#bf-submit").boundingBox();
      assert(sb.height >= 44, "submit button is a good tap target");
    }
    await ctx.close();
  }
});

await test("review mode: visitors see no placeholder labels, ?review shows them", async () => {
  const pub = await openPage();
  eq(await pub.page.$$eval(".ph-badge", (els) => els.filter((e) => e.offsetParent !== null).length), 0, "no labels for visitors");
  assert((await pub.page.locator("[data-placeholder]").count()) > 0, "placeholders are still marked for the launch check");
  await pub.ctx.close();
  const rv = await openPage({ query: "?review" });
  assert((await rv.page.$$eval(".ph-badge", (els) => els.filter((e) => e.offsetParent !== null).length)) > 0, "labels shown in review mode");
  await rv.ctx.close();
});

await test("every sample-data visual sits under an Illustrative Sample Data label", async () => {
  const { ctx, page } = await openPage();
  const missing = await page.evaluate(() => {
    const frames = [...document.querySelectorAll("#video, #part-panel, #board")];
    return frames.filter((f) => !f.querySelector(".sample-badge")).map((f) => f.id);
  });
  eq(missing.length, 0, `frames without the label: ${missing.join(", ")}`);
  await ctx.close();
});

await test("the page never names the first client, its figures or a price", async () => {
  const html = fs.readFileSync(path.join(ROOT, "index.html"), "utf8").toLowerCase();
  for (const t of ["brightstar", "60 to 100", "350 lines", "24-month", "$35", "35,000", "$2,000", "chatgpt"]) {
    assert(!html.includes(t), `page contains "${t}"`);
  }
});

await test("production config.js is valid and documents how to connect leads", async () => {
  const src = fs.readFileSync(path.join(SITE, "public", "config.js"), "utf8");
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
fs.writeFileSync(path.join(SITE, "tests", "e2e-results.json"), JSON.stringify({ run_at: new Date().toISOString(), results }, null, 1));
process.exit(failed.length ? 1 : 0);
