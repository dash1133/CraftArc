// Fails if website/out was not built from the current sources (run `npm run build` in website/ and commit out/).
import { existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { buildId } from "../build-id.mjs";

const SITE = join(dirname(fileURLToPath(import.meta.url)), "..");
const id = buildId();
const ok = existsSync(join(SITE, "out", "_next", "static", id));
console.log(ok ? `build is fresh: website/out matches the sources (${id})` : `STALE BUILD: website/out does not match the sources (expected ${id}). Run npm run build in website/ and commit website/out.`);
process.exit(ok ? 0 : 1);
