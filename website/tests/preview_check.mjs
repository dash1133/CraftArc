// Checks the preview website (preview/dist/CraftArc_Website.html) the way the claude.ai artifact host serves it:
// wrapped in the host's document skeleton, at a nested path, under a strict content security policy,
// with every other network request blocked. Run: node website/tests/preview_check.mjs (after npm run preview:build)
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const SITE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const FILE = path.join(SITE, "preview", "dist", "CraftArc_Website.html");
if (!fs.existsSync(FILE)) { console.error("No preview found: run `npm run preview:build` in website/ first."); process.exit(1); }

const fragment = fs.readFileSync(FILE, "utf8");
const page = `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top);padding-bottom:env(safe-area-inset-bottom)}body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style>
</head><body>${fragment}</body></html>`;
const CSP = "default-src 'none'; script-src 'unsafe-inline' https://cdnjs.cloudflare.com; style-src 'unsafe-inline' https://fonts.googleapis.com; font-src data: https://fonts.gstatic.com; img-src data: blob:; connect-src 'self'";
const server = http.createServer((req, res) => {
  if (req.url.split("?")[0] === "/artifact/preview/index.html") {
    res.writeHead(200, { "Content-Type": "text/html", "Content-Security-Policy": CSP });
    return res.end(page);
  }
  res.writeHead(404); res.end();
});
await new Promise((r) => server.listen(0, "127.0.0.1", r));
const URL_ = `http://127.0.0.1:${server.address().port}/artifact/preview/index.html`;

const results = [];
async function test(name, fn) {
  try { await fn(); results.push(true); console.log(`  PASS  ${name}`); }
  catch (e) { results.push(false); console.log(`  FAIL  ${name}\n        ${e.message}`); }
}
const assert = (c, m) => { if (!c) throw new Error(m); };

const browser = await chromium.launch();
async function open(viewport = { width: 1440, height: 900 }) {
  const ctx = await browser.newContext({ viewport });
  const p = await ctx.newPage();
  const errors = [], requests = [];
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });
  p.on("request", (r) => { if (!r.url().startsWith("data:") && r.url() !== URL_) requests.push(r.url()); });
  await p.goto(URL_, { waitUntil: "load" });
  await p.waitForSelector("#main > section");
  await p.waitForTimeout(400);
  return { ctx, p, errors, requests };
}

console.log(`\nPreview checks (${(fragment.length / 1024).toFixed(0)} KB)\n`);

await test("renders under the artifact's rules: no errors, no outside requests, nothing blocked", async () => {
  const { ctx, p, errors, requests } = await open();
  assert(errors.length === 0, `console errors: ${errors.join(" | ")}`);
  assert(requests.length === 0, `outside requests: ${requests.join(", ")}`);
  assert(fragment.slice(0, 8192).includes("<title>CraftArc Website</title>"), "title in the first 8KB");
  assert(!/<!doctype|<html|<head>|<body/i.test(fragment.replace(/<script>[\s\S]*?<\/script>/g, "")), "no document tags of its own");
  await ctx.close();
});

await test("same page as the live site: the nine sections, the headline and the fonts", async () => {
  const live = fs.readFileSync(path.join(SITE, "out", "index.html"), "utf8");
  const liveIds = [...live.matchAll(/<section[^>]*id="([^"]+)"/g)].map((m) => m[1]).filter((id) => id !== "why-now" || true);
  const { ctx, p } = await open();
  const ids = await p.$$eval("#main > section", (els) => els.map((e) => e.id));
  assert(ids.join(",") === liveIds.join(","), `sections ${ids.join(",")} vs live ${liveIds.join(",")}`);
  assert((await p.textContent("h1")).trim() === "Can you tell if your company has a gap in leadership depth?", "headline");
  const fontOk = await p.evaluate(async () => { await document.fonts.ready; return document.fonts.check("16px Inter") || [...document.fonts].some((f) => f.status === "loaded"); });
  assert(fontOk, "embedded fonts load");
  await ctx.close();
});

await test("footer is the live footer, with links pointed at this page", async () => {
  const { ctx, p } = await open();
  const f = await p.evaluate(() => ({
    heads: [...document.querySelectorAll(".footer-head")].map((h) => h.textContent.trim()).join(","),
    bg: getComputedStyle(document.querySelector(".site-footer")).backgroundColor,
    local: [...document.querySelectorAll(".site-footer a[href^='#']")].map((a) => a.getAttribute("href")),
  }));
  assert(f.heads === "Product,Company,Get Started,Legal", "footer headings");
  assert(f.bg === "rgb(241, 245, 249)", "footer background");
  for (const h of f.local) assert(await p.evaluate((x) => !!document.getElementById(x.slice(1)), h), `${h} lands on this page`);
  await ctx.close();
});

await test("everything works: story player, four parts, board tabs and charts, briefing form", async () => {
  const { ctx, p, errors } = await open();
  await p.evaluate(() => { window.__craftarcBeatMs = 300; });
  await p.click('[data-cta="watch-pill"]');
  await p.waitForSelector("#story[open]");
  await p.waitForFunction(() => Number(document.querySelector("#story [data-beat]").dataset.beat) >= 1, null, { timeout: 4000 });
  await p.keyboard.press("Escape");
  await p.locator('#how [role="tab"]').nth(2).click();
  assert((await p.textContent("#part-panel")).includes("Coach check-in"), "part 3 frame");
  for (let i = 0; i < 5; i++) {
    await p.locator('#board [role="tab"]').nth(i).click();
    await p.locator('#board [role="tabpanel"]:not([hidden]) svg.recharts-surface').first().waitFor({ timeout: 5000 });
  }
  await p.click('header [data-cta="header"]');
  await p.waitForSelector("#briefing[open]");
  await p.click("#bf-submit");
  assert(await p.locator("#bf-name-err").isVisible(), "form validation");
  assert(errors.length === 0, `console errors: ${errors.join(" | ")}`);
  await p.screenshot({ path: path.join(SITE, "preview", "dist", "preview-form.png") });
  await ctx.close();
});

await test("desktop and phone: no sideways scroll", async () => {
  for (const width of [1440, 390]) {
    const { ctx, p } = await open({ width, height: 900 });
    const sw = await p.evaluate(() => document.documentElement.scrollWidth);
    assert(sw <= width, `${sw}px wide at ${width}px`);
    await p.screenshot({ path: path.join(SITE, "preview", "dist", `preview-${width}.png`), fullPage: width === 390 });
    await ctx.close();
  }
});

await browser.close();
server.close();
const failed = results.filter((r) => !r).length;
console.log(`\n${results.length - failed} passed, ${failed} failed`);
process.exit(failed ? 1 : 0);
