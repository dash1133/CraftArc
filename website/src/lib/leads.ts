// Lead handling for the briefing form: first-touch attribution, fit scoring and delivery.
// Delivery: JSON POST to leadEndpoint when it is set in public/config.js, otherwise a filled-in
// email to leadEmail. With neither, the form says it is not connected (it never drops a lead silently).

export type LeadInput = { name: string; role: string; company: string; email: string; message: string };

type Config = { leadEndpoint?: string; leadEmail?: string; personalEmailDomains?: string[] };

declare global {
  interface Window {
    CRAFTARC_CONFIG?: Config;
    dataLayer?: Record<string, unknown>[];
    __craftarcNavigate?: (href: string) => void;
    __craftarc?: { scoreLead: typeof scoreLead };
  }
}

export const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const ATTR_KEYS = ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "gclid", "li_fat_id"];

export function config(): Config {
  return (typeof window !== "undefined" && window.CRAFTARC_CONFIG) || {};
}

/** First touch is kept for the session, so a visitor keeps their campaign tags after moving around. */
export function readAttribution(): Record<string, string> {
  if (typeof window === "undefined") return {};
  try {
    const stored = window.sessionStorage.getItem("craftarc_attr");
    if (stored) return JSON.parse(stored);
  } catch {
    /* storage blocked: attribution still works for this page view */
  }
  const params = new URLSearchParams(window.location.search);
  const out: Record<string, string> = {};
  for (const k of ATTR_KEYS) {
    const v = params.get(k);
    if (v) out[k] = v.slice(0, 200);
  }
  out.referrer = document.referrer || "";
  out.landing_page = window.location.pathname + window.location.search;
  try {
    window.sessionStorage.setItem("craftarc_attr", JSON.stringify(out));
  } catch {
    /* ignore */
  }
  return out;
}

export function emailType(email: string): "work" | "personal" {
  const domain = (email.split("@")[1] || "").toLowerCase();
  return (config().personalEmailDomains || []).includes(domain) ? "personal" : "work";
}

/** Fit with the CraftArc buyer: business leaders first (memo: sell to business leaders, not HR). */
export function scoreLead(d: { role: string; email_type: string; message: string; company: string; email: string }) {
  const role = d.role.toLowerCase();
  let score = 5;
  if (/\b(ceo|chief executive|founder|president|managing partner|chair|board|director of the board)\b/.test(role)) score = 50;
  else if (/\b(coo|cfo|chief|managing director|partner|general manager|head of)\b/.test(role)) score = 35;
  else if (/\b(vp|vice president|director|principal)\b/.test(role)) score = 25;
  else if (/\b(hr|talent|people|learning|l&d)\b/.test(role)) score = 15;
  if (d.email_type === "work") score += 30;
  if (d.message.trim().length >= 20) score += 10;
  const domain = (d.email.split("@")[1] || "").toLowerCase().split(".")[0];
  if (domain && d.company.toLowerCase().replace(/[^a-z0-9]/g, "").includes(domain.replace(/[^a-z0-9]/g, ""))) score += 10;
  score = Math.max(0, Math.min(100, score));
  return { fit_score: score, priority: score >= 70 ? "hot" : score >= 45 ? "warm" : "nurture" };
}

export function buildLead(input: LeadInput) {
  const email_type = emailType(input.email);
  const s = scoreLead({ ...input, email_type });
  return {
    ...input,
    email_type,
    ...s,
    source: "craftarc-website",
    page: window.location.href.split("#")[0],
    submitted_at: new Date().toISOString(),
    ...readAttribution(),
  };
}

export function mailtoHref(lead: ReturnType<typeof buildLead>, to: string) {
  const lines = [
    `Name: ${lead.name}`, `Role: ${lead.role}`, `Company: ${lead.company}`, `Email: ${lead.email}`, "", lead.message,
  ];
  return `mailto:${encodeURIComponent(to)}?subject=${encodeURIComponent(`CraftArc briefing request: ${lead.company}`)}&body=${encodeURIComponent(lines.join("\n"))}`;
}

export function track(event: string, data: Record<string, unknown> = {}) {
  if (typeof window === "undefined") return;
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({ event, ...data });
}
