import type { Metadata } from "next";
import { Inter, Instrument_Serif } from "next/font/google";
import Script from "next/script";
import { META } from "@/content/copy";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter", display: "swap" });
const serif = Instrument_Serif({ subsets: ["latin"], weight: "400", variable: "--font-instrument", display: "swap" });

export const metadata: Metadata = {
  title: META.title,
  description: META.description,
  icons: { icon: "/assets/img/favicon.svg" },
  // Keep the site out of search engines until launch; launch_check.py fails while this is here.
  robots: { index: false, follow: false },
  openGraph: { title: META.title, description: META.description, type: "website" },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en-US" className={`${inter.variable} ${serif.variable}`}>
      <head>
        {/* Review mode: ?review shows the placeholder badges that visitors never see. */}
        <script
          dangerouslySetInnerHTML={{
            __html: 'if (/[?&]review(=|&|$)/.test(location.search)) document.documentElement.classList.add("review");',
          }}
        />
      </head>
      <body>
        {/* Where leads go: edit public/config.js (no rebuild needed). */}
        <Script src="/config.js" strategy="beforeInteractive" />
        {children}
      </body>
    </html>
  );
}
