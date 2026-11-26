// A build ID made from the site's sources, so the same sources always build the same files,
// and tests/check_build_fresh.mjs can tell whether the committed website/out matches the sources.
import { createHash } from "node:crypto";
import { readdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join, relative } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = dirname(fileURLToPath(import.meta.url));
const INPUTS = ["src", "public", "package-lock.json", "next.config.ts", "postcss.config.mjs", "tsconfig.json", "build-id.mjs"];

function walk(p, out) {
  if (statSync(p).isDirectory()) for (const f of readdirSync(p).sort()) walk(join(p, f), out);
  else out.push(p);
}

export function buildId() {
  const files = [];
  for (const i of INPUTS) walk(join(ROOT, i), files);
  const h = createHash("sha256");
  for (const f of files) {
    h.update(relative(ROOT, f).split("\\").join("/"));
    h.update(readFileSync(f));
  }
  return `src-${h.digest("hex").slice(0, 16)}`;
}
