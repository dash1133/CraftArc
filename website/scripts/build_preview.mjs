// Builds the preview website: one self-contained HTML file for a claude.ai Artifact, so the site can be
// reviewed without Vercel. Same components, copy, styles, fonts and footer as the live site.
// Run after `npm run build` (it reuses the compiled CSS and fonts in out/):  npm run preview:build
// Writes preview/dist/CraftArc_Website.html (not committed). Publish that file to the artifact URL in README.md.
import { build } from "esbuild";
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const SITE = join(dirname(fileURLToPath(import.meta.url)), "..");
const OUT = join(SITE, "out");
const DIST = join(SITE, "preview", "dist");
if (!existsSync(join(OUT, "index.html"))) {
  console.error("No build found: run `npm run build` first.");
  process.exit(1);
}

const page = readFileSync(join(OUT, "index.html"), "utf8");
const htmlClass = (page.match(/<html[^>]*class="([^"]+)"/) || [])[1] || "";

// The compiled site CSS (Tailwind, the design tokens, the footer's CSS), with every font embedded.
const cssFiles = [...page.matchAll(/<link rel="stylesheet" href="(\/_next\/static\/css\/[^"]+)"/g)].map((m) => m[1]);
let css = cssFiles.map((f) => readFileSync(join(OUT, f), "utf8")).join("\n");
css = css.replace(/url\((\/_next\/static\/media\/[^)]+\.woff2)\)/g, (_, f) =>
  `url(data:font/woff2;base64,${readFileSync(join(OUT, f)).toString("base64")})`);

// The logo, embedded (the navbar and the footer both use it).
const logo = `data:image/svg+xml;base64,${readFileSync(join(SITE, "public", "assets", "img", "logo-mark.svg")).toString("base64")}`;

// The live lead settings, so the form behaves as it does on the site.
const config = readFileSync(join(SITE, "public", "config.js"), "utf8");

const result = await build({
  entryPoints: [join(SITE, "preview", "entry.tsx")],
  bundle: true,
  write: false,
  minify: true,
  format: "iife",
  target: "es2020",
  jsx: "automatic",
  define: { "process.env.NODE_ENV": '"production"' },
  alias: { "@": join(SITE, "src") },
  logLevel: "error",
});
let js = result.outputFiles[0].text
  .replaceAll("/assets/img/logo-mark.svg", logo)
  .replaceAll("assets/img/logo-mark.svg", logo)
  .replaceAll("</script", "<\\/script");

// Artifact page contract: content only (the host adds the doctype, head and body), a <title> near the top,
// a sticky header that clears the phone's safe area, and an explicit background.
const html = `<title>CraftArc Website</title>
<style>
${css}
/* preview only: the artifact host's phone safe area */
header.sticky { top: env(safe-area-inset-top, 0px); }
body::before { content: ""; position: fixed; inset: 0 0 auto; height: env(safe-area-inset-top, 0px); z-index: 50; background: #fff; }
body { background: #fff; }
</style>
<script>document.documentElement.lang = "en-US"; document.documentElement.className += " ${htmlClass}";</script>
<script>${config}</script>
<div id="craftarc-root"></div>
<script>${js}</script>
`;

mkdirSync(DIST, { recursive: true });
const file = join(DIST, "CraftArc_Website.html");
writeFileSync(file, html);
console.log(`preview: wrote ${file} (${(html.length / 1024).toFixed(0)} KB, ${cssFiles.length} stylesheet, fonts and logo embedded)`);
