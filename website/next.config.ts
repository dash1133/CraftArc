import type { NextConfig } from "next";
import { buildId } from "./build-id.mjs";

// Static export: `npm run build` writes plain HTML, CSS and JS to out/. The built site is committed,
// and Vercel only serves website/out (vercel.json): nothing is installed or built on Vercel.
// The build ID comes from the sources, so a rebuild of unchanged sources changes no files.
const nextConfig: NextConfig = {
  output: "export",
  images: { unoptimized: true },
  trailingSlash: false,
  generateBuildId: async () => buildId(),
};

export default nextConfig;
