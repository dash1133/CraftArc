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

const PE = "private-equity.html";
const BOOK = "book-a-demo.html";
const INDUSTRY_PAGES = [PE, "professional-services.html", "financial-services.html", "healthcare-life-sciences.html", "technology.html", "manufacturing-industrial.html"];
const PAGES = ["", ...INDUSTRY_PAGES, "about.html", BOOK];

async function openPage({ viewport = { width: 1366, height: 900 }, config = TEST_CONFIG(), query = "", device, path = "" } = {}) {
  const ctx = await browser.newContext(device || { viewport });
  const page = await ctx.newPage();
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });
  // Fonts come from Google in production; block them so tests run offline.
  await page.route(/fonts\.(googleapis|gstatic)\.com/, (r) => r.fulfill({ status: 200, contentType: "text/css", body: "" }));
  await page.route("**/config.js", (r) => r.fulfill({ contentType: "text/javascript", body: config }));
  await page.goto(`${BASE}/${path}${query}`, { waitUntil: "load" });
  return { ctx, page, errors };
}

async function fillValid(page, over = {}) {
  const v = { name: "Alex Morgan", email: "alex.morgan@examplecapital.com", firm: "Example Capital", role: "coo", industry: "private_equity",
    aum: "2to5b", team: "10to25", timing: "q1_2027", framework: "yes", message: "We review 22 senior people.", ...over };
  await page.fill("#name", v.name);
  await page.fill("#email", v.email);
  await page.fill("#firm", v.firm);
  await page.selectOption("#role", v.role);
  if (v.timing) await page.selectOption("#timing", v.timing);
  if (v.industry || v.aum || v.team || v.framework || v.message) await page.evaluate(() => { document.getElementById("more").open = true; });
  if (v.industry) await page.selectOption("#industry", v.industry);
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
  const { ctx, page } = await openPage({ path: PE });
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
  assert(await page.locator(".site-header .btn-primary").isVisible(), "header Book a demo visible on a phone");
  await page.screenshot({ path: path.join(SHOTS, "mobile-full.png"), fullPage: true });
  const book = await openPage({ path: BOOK, viewport: { width: 390, height: 844 } });
  const box = await book.page.locator("#submit").boundingBox();
  assert(box && box.width > 300 && box.height >= 44, "submit button is a good tap target");
  await book.ctx.close();
  await ctx.close();
});

await test("tablet (820px): no sideways scroll", async () => {
  const { ctx, page } = await openPage({ viewport: { width: 820, height: 1180 } });
  const sw = await page.evaluate(() => document.documentElement.scrollWidth);
  assert(sw <= 820, `page is ${sw}px wide at 820px`);
  await ctx.close();
});

await test("header 'Book a demo' opens the Book a demo page, with the form in view", async () => {
  const { ctx, page } = await openPage();
  await Promise.all([page.waitForURL(/book-a-demo\.html/), page.click(".site-header .btn-primary")]);
  assert(await page.locator("#lead-form").isVisible(), "form visible");
  const top = await page.evaluate(() => document.getElementById("lead-form").getBoundingClientRect().top);
  assert(top > 0 && top < 900, `form starts in the first screen (${top}px)`);
  await ctx.close();
});

await test("every 'Book a demo' link on every page goes to the Book a demo page, and the wording never changes", async () => {
  for (const p of PAGES) {
    const { ctx, page } = await openPage({ path: p });
    const ctas = await page.$$eval("a.btn-primary", (els) => els.map((a) => ({ text: a.textContent.trim(), href: a.getAttribute("href") })));
    assert(ctas.length >= 1, `/${p} has a primary button`);
    for (const c of ctas) {
      eq(c.text, "Book a demo", `primary button wording on /${p}`);
      assert(c.href.startsWith("book-a-demo.html"), `/${p} button goes to the Book a demo page (${c.href})`);
    }
    eq(await page.locator(".hero a.btn-primary").count(), ["", BOOK, "about.html"].includes(p) ? 0 : 1, `primary buttons in the hero of /${p}`);
    await ctx.close();
  }
});


await test("stated video length matches the real video", async () => {
  const { ctx, page } = await openPage({ path: PE });
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

await test("no page carries unapproved offer terms, the client's name or a first-client figure", async () => {
  for (const p of PAGES) {
    const html = fs.readFileSync(path.join(ROOT, p || "index.html"), "utf8").toLowerCase();
    for (const t of ["fixed for four years", "build-out", "three to four meetings", "small number of firms", "data-pending",
      "brightstar", "60 to 100", "350 lines", "24-month"]) {
      assert(!html.includes(t), `/${p} source contains "${t}"`);
    }
  }
});

await test("placeholder proof is visibly labelled so it cannot pass as a real result", async () => {
  const { ctx, page } = await openPage({ path: PE });
  const blocks = await page.evaluate(() => [...document.querySelectorAll(".proof-slot")].map((el) => ({
    badge: el.querySelector(".ph-badge") && el.querySelector(".ph-badge").offsetParent !== null ? el.querySelector(".ph-badge").textContent : "",
  })));
  assert(blocks.length > 0, "placeholder cards present (remove this test once real proof replaces them)");
  assert(blocks.every((b) => /placeholder/i.test(b.badge)), "every placeholder card shows a visible Placeholder badge");
  const text = await page.evaluate(() => [...document.querySelectorAll(".proof-slot")].map((el) => el.innerText).join(" "));
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
    } else if (l.href.startsWith("mailto:")) {
      eq(l.href, "mailto:dash@craftarc.ai", "contact link");
    } else {
      const res = await fetch(`${BASE}/${l.href.split("#")[0]}`);
      eq(res.status, 200, `internal footer link ${l.href} loads`);
    }
  }
  assert(f.links.some((l) => l.href.includes("legal/privacy-policy")) && f.links.some((l) => l.href.includes("trust.agenticprivatemarkets.ai")), "legal links present");
  await ctx.close();
});

await test("product screens enlarge in a viewer and close with Escape", async () => {
  const { ctx, page } = await openPage({ path: PE });
  const btn = page.locator("#proof .zoom").nth(2);
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
  const { ctx, page } = await openPage({ path: BOOK });
  eq(await page.evaluate(() => document.getElementById("more").open), false, "optional section closed");
  const visible = await page.evaluate(() => [...document.querySelectorAll("#lead-form input, #lead-form select, #lead-form textarea")]
    .filter((el) => !el.closest(".hp") && el.type !== "checkbox" && el.checkVisibility({ contentVisibilityAuto: true, visibilityProperty: true }))
    .map((el) => el.id));
  eq(visible.join(","), "name,email,firm,role,timing", "visible fields");
  await ctx.close();
});


await test("every page loads cleanly: one h1, no console errors, images load, no sideways scroll on a phone", async () => {
  for (const path of PAGES) {
    const { ctx, page, errors } = await openPage({ path, viewport: { width: 390, height: 844 } });
    eq(await page.locator("h1").count(), 1, `h1 count on /${path}`);
    await page.evaluate(async () => { for (const i of document.images) { i.loading = "eager"; } await new Promise((r) => setTimeout(r, 500)); });
    const bad = await page.evaluate(() => [...document.images].filter((i) => !i.closest("dialog")).filter((i) => !i.complete || i.naturalWidth === 0).map((i) => i.src));
    eq(bad.length, 0, `broken images on /${path}: ${bad.join(", ")}`);
    const sw = await page.evaluate(() => document.documentElement.scrollWidth);
    assert(sw <= 390, `/${path} is ${sw}px wide at 390px`);
    const missing = await page.evaluate(() => [...document.querySelectorAll('a[href^="#"]')].map((a) => a.getAttribute("href")).filter((h) => h.length > 1 && !document.querySelector(h)));
    eq(missing.length, 0, `missing anchors on /${path}: ${missing.join(", ")}`);
    eq(errors.length, 0, `console errors on /${path}: ${errors.join(" | ")}`);
    await ctx.close();
  }
});

await test("captions are not shown twice: the caption track is off by default because captions are burned in", async () => {
  const { ctx, page } = await openPage({ path: PE });
  const t = await page.evaluate(() => { const tr = document.querySelector("video track"); return { def: tr.default, mode: tr.track.mode }; });
  eq(t.def, false, "track has no default attribute");
  assert(t.mode !== "showing", "track not showing on load");
  await ctx.close();
});

await test("homepage hero plays the existing video, badged as a placeholder, and the private equity page keeps it", async () => {
  const { ctx, page } = await openPage();
  eq(await page.locator("video").count(), 1, "one video on the homepage, in the hero");
  eq(await page.locator(".hero video source").getAttribute("src"), "assets/video/craftarc-vsl-720p.mp4", "the existing video, unchanged");
  const cap = page.locator(".hero figcaption");
  assert((await cap.getAttribute("data-placeholder")) !== null, "marked as a placeholder for the launch check");
  assert(/placeholder/i.test(await cap.innerText()), "placeholder badge shown");
  const t = await page.evaluate(() => { const tr = document.querySelector(".hero video track"); return { def: tr.default, mode: tr.track.mode }; });
  eq(t.def, false, "caption track off by default (captions are burned in)");
  const pe = await openPage({ path: PE });
  eq(await pe.page.locator("video source").getAttribute("src"), "assets/video/craftarc-vsl-720p.mp4", "PE page plays the existing video");
  await pe.ctx.close();
  await ctx.close();
});

await test("homepage copy is industry-neutral outside the industries and proof sections", async () => {
  const { ctx, page } = await openPage();
  const text = await page.evaluate(() => {
    const main = document.querySelector("main").cloneNode(true);
    main.querySelectorAll("#industries, #proof, #case, .proofline, .proof-strip, .how-more, .video-placeholder, .mega").forEach((el) => el.remove());
    return main.innerText;
  });
  const hits = text.match(/\b(funds?|deal team|buyout|investment judgement|assets under management|partners ask)\b/gi) || [];
  eq(hits.length, 0, `PE-specific words on the homepage: ${hits.join(", ")}`);
  await ctx.close();
});

await test("homepage follows the website guidance: twelve sections in order", async () => {
  const { ctx, page } = await openPage();
  const ids = await page.$$eval("main > section", (els) => els.map((e) => e.id));
  eq(ids.join(","), "top,claims,problem,method,solution,how,proof,industries,start,who,faq,book", "section order");
  await ctx.close();
});

await test("hero: the question is the largest text, text on the left, the video on the right, no button in the body", async () => {
  const { ctx, page } = await openPage({ viewport: { width: 1440, height: 900 } });
  const r = await page.evaluate(() => {
    const px = (el) => parseFloat(getComputedStyle(el).fontSize);
    const all = [...document.querySelectorAll("main *")].filter((e) => !e.closest("video, svg") && [...e.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim()));
    const h1 = document.querySelector(".hero h1"), a = document.querySelector(".hero-answer"), t = document.querySelector(".hero-time span");
    const copy = document.querySelector(".hero-split-copy").getBoundingClientRect(), vid = document.querySelector(".hero video").getBoundingClientRect();
    return { h1: px(h1), a: px(a), t: px(t), max: Math.max(...all.map(px)), q: h1.textContent, aTop: a.getBoundingClientRect().top, h1Bottom: h1.getBoundingClientRect().bottom,
      buttons: document.querySelectorAll(".hero .btn").length, copyRight: copy.right, vidLeft: vid.left, vidBottom: vid.bottom };
  });
  eq(r.q, "Can you tell how close each leader is to their next role?", "approved question");
  eq(r.h1, r.max, "the question is the largest text on the page");
  assert(r.h1 > r.a && r.a > r.t, `sizes step down: ${r.h1} > ${r.a} > ${r.t}`);
  assert(r.aTop >= r.h1Bottom, "answer sits under the question");
  assert(r.copyRight <= r.vidLeft, "text on the left, video on the right");
  assert(r.vidBottom <= 900, "the whole video is in the first screen");
  eq(r.buttons, 0, "no button in the hero body: the header carries Book a demo");
  assert(await page.locator(".site-header .btn-primary").isVisible(), "header Book a demo visible");
  await ctx.close();
  const m = await openPage({ viewport: { width: 390, height: 844 } });
  const order = await m.page.evaluate(() => document.querySelector(".hero h1").getBoundingClientRect().top < document.querySelector(".hero video").getBoundingClientRect().top);
  assert(order, "on a phone the question comes first, then the video");
  await m.ctx.close();
});

await test("three claims: Know, Grow and Without the time, equal blocks, three outcomes each, each linked to its module", async () => {
  const { ctx, page } = await openPage();
  const c = await page.$$eval(".claim", (els) => els.map((e) => ({ name: e.querySelector(".claim-name").textContent.trim(),
    outcomes: e.querySelectorAll(".outcomes li").length, link: e.querySelector(".delivered a").getAttribute("href"), w: Math.round(e.getBoundingClientRect().width) })));
  eq(c.map((x) => x.name).join(" | "), "Know | Grow | Without the time", "claim names");
  assert(c.every((x) => x.outcomes === 3), "three outcomes each");
  eq(c.map((x) => x.link).join(" "), "#cockpit #development-arc #review-cycle", "delivered-by links");
  assert(Math.max(...c.map((x) => x.w)) - Math.min(...c.map((x) => x.w)) <= 2, "equal width");
  for (const x of c) assert(await page.evaluate((h) => !!document.querySelector(h), x.link), `${x.link} exists`);
  await ctx.close();
});

await test("solution: the Leadership Cockpit sits above the other two, tagged as not yet live, and the agent runs along the bottom", async () => {
  const { ctx, page } = await openPage();
  const r = await page.evaluate(() => {
    const box = (s) => document.querySelector(s).getBoundingClientRect();
    const tag = document.querySelector("#cockpit .tag-soon");
    return { cockpit: box("#cockpit").bottom, rc: box("#review-cycle").top, da: box("#development-arc").top, agentTop: box(".agent-band").top,
      lowest: Math.max(box("#review-cycle").bottom, box("#development-arc").bottom), tag: tag && tag.textContent, tagMarked: tag && tag.hasAttribute("data-placeholder"),
      names: [...document.querySelectorAll(".module h3")].map((h) => h.textContent) };
  });
  eq(r.names.join(" | "), "Leadership Cockpit | Review Cycle | Development Arc", "module names, capitalized");
  assert(r.cockpit <= r.rc && r.cockpit <= r.da, "Cockpit above the Review Cycle and the Development Arc");
  assert(r.agentTop >= r.lowest, "agent band under all three");
  eq(r.tag, "Not yet live", "Cockpit tag shown");
  assert(r.tagMarked, "tag wording is marked as needing approval");
  await ctx.close();
});

await test("how it works: eight steps, and the video stays in view while the reader scrolls (desktop), below the steps on a phone", async () => {
  eq(await (await openPage()).page.locator("#how .steps li").count(), 8, "eight steps on the homepage");
  const { ctx, page } = await openPage({ path: PE, viewport: { width: 1440, height: 900 } });
  eq(await page.locator("#how .steps li").count(), 8, "eight steps on the private equity page");
  await page.evaluate(() => document.getElementById("step-7").scrollIntoView({ block: "center", behavior: "instant" }));
  await page.waitForTimeout(200);
  const v = await page.evaluate(() => { const b = document.querySelector("#how video").getBoundingClientRect(); return { top: b.top, bottom: b.bottom }; });
  assert(v.top >= 0 && v.bottom <= 900, `video in view at step 7 (${Math.round(v.top)} to ${Math.round(v.bottom)})`);
  await ctx.close();
  const m = await openPage({ path: PE, viewport: { width: 390, height: 844 } });
  const order = await m.page.evaluate(() => document.querySelector("#how .steps").getBoundingClientRect().top < document.querySelector("#how video").getBoundingClientRect().top);
  assert(order, "steps first, then the video, on a phone");
  await m.ctx.close();
});

await test("homepage: the onboarding, FAQ and proof follow the guidance", async () => {
  const { ctx, page } = await openPage();
  eq(await page.locator(".start-steps li").count(), 4, "four onboarding steps");
  const qs = await page.$$eval("#faq summary", (els) => els.map((e) => e.textContent.trim()));
  eq(qs.join(" | "), ["Who decides where a leader stands?", "Who sees the conversations?", "How do we introduce the agent so people do not feel watched?",
    "Will it fit our own roles and leadership levels?", "Why not build this with a general AI assistant?", "How much leadership time does it take?", "What does it cost?"].join(" | "), "the seven questions CEOs asked");
  const slot = page.locator("#proof .proof-slot");
  assert((await slot.getAttribute("data-placeholder")) !== null, "proof slot is a marked placeholder");
  eq(await page.locator(".ind-status").allTextContents().then((t) => t.join(",")), "Live,Coming next,Coming soon,Coming soon,Coming soon,Coming soon", "industry status chips in order");
  await ctx.close();
});

await test("industry pages reuse the homepage's three claims and solution, changing only the role words", async () => {
  const norm = async (p) => {
    const { ctx, page } = await openPage({ path: p });
    const out = await page.evaluate(() => ["#claims", "#solution"].map((s) => {
      const el = document.querySelector(s).cloneNode(true);
      el.querySelectorAll("[data-token]").forEach((t) => { t.textContent = "TOKEN"; });
      return el.innerHTML.replace(/\s+/g, " ");
    }));
    const tokens = await page.$$eval("[data-token]", (els) => [...new Set(els.map((e) => e.textContent))]);
    await ctx.close();
    return { out, tokens };
  };
  const home = await norm("");
  for (const p of INDUSTRY_PAGES) {
    const ind = await norm(p);
    eq(ind.out[0], home.out[0], `three claims on /${p}`);
    eq(ind.out[1], home.out[1], `solution on /${p}`);
    assert(ind.tokens.join() !== home.tokens.join(), `/${p} names its own roles (${ind.tokens.join(", ")})`);
  }
});

await test("industries menu: six industries, eighteen sub-sectors, no status labels, opens and closes, every link lands", async () => {
  const { ctx, page } = await openPage();
  assert(await page.locator("#industries-menu").isHidden(), "menu starts closed");
  await page.click(".nav-menu");
  assert(await page.locator("#industries-menu").isVisible(), "menu opens");
  eq(await page.getAttribute(".nav-menu", "aria-expanded"), "true", "aria-expanded");
  const names = await page.$$eval(".mega-ind strong", (els) => els.map((e) => e.textContent.trim()));
  eq(names.join(" | "), "Private Equity and VC | Professional Services | Financial Services | Healthcare and Life Sciences | Technology | Manufacturing and Industrial", "industries in the guidance's order");
  const subs = await page.$$eval(".mega-col ul a", (els) => els.map((e) => e.getAttribute("href")));
  eq(subs.length, 18, "sub-sector links");
  eq(await page.locator("#industries-menu .mega-live").count(), 0, "no 'Live today' label in the menu");
  const peSubs = await page.$$eval('.mega-col:first-child ul a', (els) => els.map((e) => e.textContent.trim()));
  eq(peSubs.join(" | "), "Private Equity | Venture Capital | Investment Banks", "PE group sub-sectors");
  await page.keyboard.press("Escape");
  assert(await page.locator("#industries-menu").isHidden(), "Escape closes the menu");
  for (const href of [...new Set([...(await page.$$eval(".mega-ind", (els) => els.map((e) => e.getAttribute("href")))), ...subs])]) {
    const [file, hash] = href.split("#");
    const p2 = await ctx.newPage();
    await p2.route(/fonts\.(googleapis|gstatic)\.com/, (r) => r.fulfill({ status: 200, contentType: "text/css", body: "" }));
    const res = await p2.goto(`${BASE}/${file}`);
    eq(res.status(), 200, `${file} loads`);
    if (hash) assert(await p2.evaluate((h) => !!document.getElementById(h), hash), `${href} has a target`);
    await p2.close();
  }
  await ctx.close();
});

await test("mobile: the industries menu is reachable from the header", async () => {
  const { ctx, page } = await openPage({ viewport: { width: 390, height: 844 } });
  assert(await page.locator(".nav-menu").isVisible(), "Industries button visible on a phone");
  await page.click(".nav-menu");
  assert(await page.locator(".mega-ind").first().isVisible(), "menu items visible");
  await ctx.close();
});

await test("Book a demo form: an industry page presets the industry, and the visitor's choice is sent", async () => {
  const before = leads.length;
  const { ctx, page } = await openPage({ path: BOOK, query: "?industry=financial_services" });
  eq(await page.inputValue("#industry"), "financial_services", "industry preset from the link");
  assert(await page.locator("#aum-field").isHidden(), "AUM is only asked of private equity");
  await page.fill("#name", "Riya Shah");
  await page.fill("#email", "riya@exampletech.com");
  await page.fill("#firm", "Example Tech");
  await page.selectOption("#role", "talent_hr");
  await page.selectOption("#timing", "q1_2027");
  await page.evaluate(() => { document.getElementById("more").open = true; });
  await page.selectOption("#industry", "technology");
  await page.check("#consent");
  await page.click("#submit");
  await page.waitForSelector("#thanks:not([hidden])");
  eq(leads.length, before + 1, "lead stored");
  const b = leads[leads.length - 1].body;
  eq(b.industry, "technology", "industry");
  eq(b.aum, "", "no AUM outside private equity");
  await ctx.close();
});

await test("private equity page sends its visitors to the form tagged as private equity, with the AUM question", async () => {
  const before = leads.length;
  const { ctx, page } = await openPage({ path: PE });
  const href = await page.getAttribute(".hero .btn-primary", "href");
  eq(href, "book-a-demo.html?industry=private_equity", "hero button carries the industry");
  await page.click(".hero .btn-primary");
  await page.waitForURL(/book-a-demo/);
  await page.evaluate(() => { document.getElementById("more").open = true; });
  assert(await page.locator("#aum-field").isVisible(), "AUM asked of private equity");
  await fillValid(page, { industry: "" });
  await page.click("#submit");
  await page.waitForSelector("#thanks:not([hidden])");
  eq(leads[leads.length - 1].body.industry, "private_equity", "industry from the link");
  eq(leads[leads.length - 1].body.aum, "2to5b", "AUM sent");
  eq(leads.length, before + 1, "one lead");
  await ctx.close();
});

// ---------------------------------------------------------------- leads
await test("lead form: empty submit shows every required error, focuses the first, sends nothing", async () => {
  const before = leads.length;
  const { ctx, page } = await openPage({ path: BOOK });
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
  const { ctx, page } = await openPage({ path: BOOK });
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
  const { ctx, page } = await openPage({ path: BOOK, query: "?utm_source=linkedin&utm_medium=paid&utm_campaign=coo-q1&li_fat_id=abc123" });
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
  const { ctx, page } = await openPage({ path: PE, query: "?utm_source=newsletter&utm_campaign=nov" });
  await page.goto(`${BASE}/${BOOK}`);
  await fillValid(page);
  await page.click("#submit");
  await page.waitForSelector("#thanks:not([hidden])");
  eq(leads.length, before + 1, "one lead");
  eq(leads[leads.length - 1].body.utm_source, "newsletter", "first-touch utm kept");
  await ctx.close();
});

await test("lead form: double click sends one lead only", async () => {
  const before = leads.length;
  const { ctx, page } = await openPage({ path: BOOK });
  await fillValid(page);
  await page.locator("#submit").dblclick();
  await page.waitForSelector("#thanks:not([hidden])");
  await page.waitForTimeout(400);
  eq(leads.length, before + 1, "one lead after double click");
  await ctx.close();
});

await test("lead form: personal email is accepted but tagged and scored lower", async () => {
  const before = leads.length;
  const { ctx, page } = await openPage({ path: BOOK });
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
  const { ctx, page } = await openPage({ path: BOOK });
  const warm = await page.evaluate(() => window.__craftarc.scoreLead({ role: "partner_md", aum: "1to2b", timing: "q2_2027", framework: "draft", team: "10to25", email_type: "work" }));
  eq(warm.priority, "warm", "partner, $1B to $2B, Q2");
  const nurture = await page.evaluate(() => window.__craftarc.scoreLead({ role: "other", aum: "lt1b", timing: "unsure", framework: "no", team: "lt10", email_type: "personal" }));
  eq(nurture.priority, "nurture", "small firm, unsure");
  eq(nurture.fit_score, 7, "nurture score");
  await ctx.close();
});

await test("lead form: only the required fields are needed", async () => {
  const before = leads.length;
  const { ctx, page } = await openPage({ path: BOOK });
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
  const { ctx, page } = await openPage({ path: BOOK });
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
  const { ctx, page } = await openPage({ path: BOOK });
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
  const { ctx, page } = await openPage({ path: BOOK, config: TEST_CONFIG({ leadEndpoint: "http://127.0.0.1:9/api/lead", leadEmail: "demo@example.com" }) });
  await fillValid(page);
  await page.click("#submit");
  await page.waitForFunction(() => document.getElementById("form-status").classList.contains("is-error"));
  assert((await page.textContent("#form-status")).includes("demo@example.com"), "fallback email offered");
  assert(await page.locator("#lead-form").isVisible(), "form still visible");
  await ctx.close();
});

await test("lead form: keyboard only, Enter submits", async () => {
  const before = leads.length;
  const { ctx, page } = await openPage({ path: BOOK });
  await fillValid(page);
  await page.focus("#firm");
  await page.keyboard.press("Enter");
  await page.waitForSelector("#thanks:not([hidden])");
  eq(leads.length, before + 1, "lead stored via keyboard");
  await ctx.close();
});

await test("lead form: with no endpoint and no email it fails loudly, never silently", async () => {
  const before = leads.length;
  const { ctx, page, errors } = await openPage({ path: BOOK, config: TEST_CONFIG({ leadEndpoint: "", leadEmail: "" }) });
  await fillValid(page);
  await page.click("#submit");
  assert((await page.textContent("#form-status")).includes("not connected"), "visitor told");
  assert(errors.some((e) => e.includes("leadEndpoint")), "console error for the site owner");
  eq(leads.length, before, "nothing sent");
  await ctx.close();
});

await test("lead form: with only an email configured it opens a filled-in email", async () => {
  const { ctx, page } = await openPage({ path: BOOK, config: TEST_CONFIG({ leadEndpoint: "", leadEmail: "demo@example.com" }) });
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
  const { ctx, page } = await openPage({ path: BOOK });
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
