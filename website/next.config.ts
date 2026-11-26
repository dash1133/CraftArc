import type { NextConfig } from "next";

// Static export: `npm run build` writes plain HTML, CSS and JS to out/, which Vercel serves
// (vercel.json) and the tests in tests/ read. No server, no API routes.
const nextConfig: NextConfig = {
  output: "export",
  images: { unoptimized: true },
  trailingSlash: false,
};

export default nextConfig;
