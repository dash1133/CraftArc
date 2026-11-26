"use client";

import { createContext, useCallback, useContext, useEffect, useRef, useState } from "react";
import { X } from "lucide-react";
import { CTA, MODAL } from "@/content/copy";
import { EMAIL_RE, buildLead, config, mailtoHref, readAttribution, scoreLead, track, type LeadInput } from "@/lib/leads";

type Ctx = { open: (from: string) => void };
const BriefingContext = createContext<Ctx>({ open: () => {} });
export const useBriefing = () => useContext(BriefingContext);

/** Wraps the page so any primary call to action can open the briefing form. ?briefing=open opens it on arrival. */
export function BriefingProvider({ children }: { children: React.ReactNode }) {
  const dlg = useRef<HTMLDialogElement>(null);
  const opener = useRef<HTMLElement | null>(null);
  const [isOpen, setOpen] = useState(false);

  const open = useCallback((from: string) => {
    opener.current = document.activeElement as HTMLElement | null;
    track("cta_click", { cta: from });
    setOpen(true);
  }, []);

  useEffect(() => {
    readAttribution(); // keep the first touch for the session, whatever page section the visitor lands on
    window.__craftarc = { scoreLead };
    if (new URLSearchParams(window.location.search).get("briefing") === "open") setOpen(true);
  }, []);

  useEffect(() => {
    const d = dlg.current;
    if (!d) return;
    if (isOpen && !d.open) {
      d.showModal();
      requestAnimationFrame(() => d.querySelector<HTMLInputElement>("#bf-name")?.focus());
    } else if (!isOpen && d.open) {
      d.close();
    }
  }, [isOpen]);

  const close = useCallback(() => {
    setOpen(false);
    opener.current?.focus?.();
  }, []);

  return (
    <BriefingContext.Provider value={{ open }}>
      {children}
      <dialog
        ref={dlg}
        id="briefing"
        aria-modal="true"
        aria-labelledby="bf-title"
        onCancel={(e) => { e.preventDefault(); close(); }}
        onClick={(e) => { if (e.target === dlg.current) close(); }}
        className="w-[min(560px,calc(100vw-32px))] rounded-2xl border border-line bg-white p-0 text-ink shadow-2xl"
      >
        <BriefingForm onClose={close} />
      </dialog>
    </BriefingContext.Provider>
  );
}

type Errors = Partial<Record<keyof LeadInput, string>>;

function BriefingForm({ onClose }: { onClose: () => void }) {
  const [values, setValues] = useState<LeadInput>({ name: "", role: "", company: "", email: "", message: "" });
  const [errors, setErrors] = useState<Errors>({});
  const [status, setStatus] = useState<{ msg: string; error: boolean }>({ msg: "", error: false });
  const [sending, setSending] = useState(false);
  const [done, setDone] = useState<null | { title: string; body: string }>(null);
  const honeypot = useRef<HTMLInputElement>(null);
  const thanksRef = useRef<HTMLDivElement>(null);

  useEffect(() => { if (done) thanksRef.current?.focus(); }, [done]);

  function validate(v: LeadInput): Errors {
    const e: Errors = {};
    if (v.name.trim().length < 2) e.name = "Please enter your full name.";
    if (v.role.trim().length < 2) e.role = "Please enter your role or title.";
    if (v.company.trim().length < 2) e.company = "Please enter your company.";
    if (!EMAIL_RE.test(v.email.trim())) e.email = "Please enter a valid work email.";
    return e;
  }

  const set = (k: keyof LeadInput) => (ev: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const v = { ...values, [k]: ev.target.value };
    setValues(v);
    if (errors[k]) setErrors({ ...errors, [k]: validate(v)[k] });
  };

  async function submit(ev: React.FormEvent) {
    ev.preventDefault();
    if (sending) return;
    setStatus({ msg: "", error: false });
    if (honeypot.current?.value) { setDone({ title: MODAL.thanksTitle, body: MODAL.thanksBody }); return; }
    const e = validate(values);
    setErrors(e);
    const first = (Object.keys(e) as (keyof LeadInput)[])[0];
    if (first) {
      document.getElementById(`bf-${first}`)?.focus();
      setStatus({ msg: "Please check the highlighted fields.", error: true });
      return;
    }
    const trimmed = Object.fromEntries(Object.entries(values).map(([k, v]) => [k, v.trim()])) as LeadInput;
    const lead = buildLead(trimmed);
    const cfg = config();
    if (!cfg.leadEndpoint) {
      if (cfg.leadEmail) {
        (window.__craftarcNavigate || ((h: string) => { window.location.href = h; }))(mailtoHref(lead, cfg.leadEmail));
        track("lead_submitted", { lead_priority: lead.priority, via: "email" });
        setDone({
          title: "One more step: press send in your email app.",
          body: `Your email app should open with your request filled in. If it did not open, email ${cfg.leadEmail} and we will arrange a time.`,
        });
      } else {
        setStatus({ msg: "Sorry, the form is not connected yet. Please email us instead.", error: true });
        console.error("CraftArc: set leadEndpoint or leadEmail in public/config.js");
      }
      return;
    }
    setSending(true);
    try {
      const res = await fetch(cfg.leadEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(lead),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      track("lead_submitted", { lead_priority: lead.priority });
      setDone({ title: MODAL.thanksTitle, body: MODAL.thanksBody });
    } catch {
      const fallback = cfg.leadEmail ? ` You can also email us at ${cfg.leadEmail}.` : "";
      setStatus({ msg: `Sorry, something went wrong and your request was not sent. Please try again.${fallback}`, error: true });
    } finally {
      setSending(false);
    }
  }

  const field = (k: keyof LeadInput, label: string, type = "text", auto = "") => (
    <div className="mb-4">
      <label htmlFor={`bf-${k}`} className="mb-1.5 block text-sm font-semibold text-ink">
        {label} <span aria-hidden="true" className="text-ink-2">*</span>
      </label>
      <input
        id={`bf-${k}`}
        name={k}
        type={type}
        autoComplete={auto}
        required
        maxLength={160}
        value={values[k]}
        onChange={set(k)}
        onBlur={() => errors[k] && setErrors({ ...errors, [k]: validate(values)[k] })}
        aria-invalid={errors[k] ? true : undefined}
        aria-describedby={errors[k] ? `bf-${k}-err` : undefined}
        className={`h-12 w-full rounded-lg border bg-white px-3.5 text-base text-ink outline-none transition focus:border-ink focus:ring-4 focus:ring-slate-200 ${errors[k] ? "border-risk" : "border-slate-300"}`}
      />
      {errors[k] && <p id={`bf-${k}-err`} className="mt-1.5 text-sm text-red-700">{errors[k]}</p>}
    </div>
  );

  return (
    <div className="relative p-7 sm:p-8">
      <button type="button" onClick={onClose} aria-label="Close" className="absolute right-4 top-4 rounded-md p-2 text-ink-2 hover:bg-canvas hover:text-ink">
        <X size={20} strokeWidth={1.5} />
      </button>
      {done ? (
        <div ref={thanksRef} tabIndex={-1} id="bf-thanks" className="outline-none">
          <h2 className="pr-10 text-2xl font-semibold tracking-tight">{done.title}</h2>
          <p id="bf-thanks-msg" className="mt-3 text-ink-2">{done.body}</p>
        </div>
      ) : (
        <form id="briefing-form" noValidate onSubmit={submit}>
          <h2 id="bf-title" className="pr-10 text-2xl font-semibold tracking-tight">{MODAL.title}</h2>
          <p className="mb-6 mt-2 text-ink-2">{MODAL.intro}</p>
          {field("name", MODAL.fields.name, "text", "name")}
          {field("role", MODAL.fields.role, "text", "organization-title")}
          {field("company", MODAL.fields.company, "text", "organization")}
          {field("email", MODAL.fields.email, "email", "email")}
          <div className="mb-4">
            <label htmlFor="bf-message" className="mb-1.5 block text-sm font-semibold text-ink">{MODAL.fields.message}</label>
            <textarea id="bf-message" name="message" rows={3} maxLength={2000} value={values.message} onChange={set("message")}
              className="w-full rounded-lg border border-slate-300 bg-white px-3.5 py-2.5 text-base text-ink outline-none focus:border-ink focus:ring-4 focus:ring-slate-200" />
          </div>
          <div className="absolute -left-[10000px] h-px w-px overflow-hidden" aria-hidden="true">
            <label htmlFor="bf-website">Leave this field empty</label>
            <input ref={honeypot} id="bf-website" name="company_website" type="text" tabIndex={-1} autoComplete="off" />
          </div>
          <button type="submit" id="bf-submit" disabled={sending}
            className="mt-2 inline-flex h-12 w-full items-center justify-center rounded-lg bg-ink px-5 font-semibold text-white transition hover:bg-slate-800 disabled:cursor-progress disabled:bg-slate-400">
            {sending ? "Sending..." : CTA.submit}
          </button>
          <p className="mt-3 text-xs text-ink-2">{MODAL.privacy} <a href="#privacy" onClick={onClose} className="underline">Privacy</a></p>
          <p id="bf-status" role="status" aria-live="polite" className={`mt-2 min-h-5 text-sm ${status.error ? "text-red-700" : "text-ink-2"}`}>{status.msg}</p>
        </form>
      )}
    </div>
  );
}

/** A button that opens the briefing form. */
export function BriefingButton({ from, children, variant = "dark", className = "" }: { from: string; children: React.ReactNode; variant?: "dark" | "light"; className?: string }) {
  const { open } = useBriefing();
  const styles = variant === "dark"
    ? "bg-ink text-white hover:bg-slate-800"
    : "bg-white text-ink hover:bg-slate-100";
  return (
    <button type="button" data-cta={from} onClick={() => open(from)}
      className={`inline-flex h-11 items-center justify-center rounded-lg px-5 text-[15px] font-semibold transition ${styles} ${className}`}>
      {children}
    </button>
  );
}
