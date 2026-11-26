"""Copy checks for the CraftArc website, against Dash's writing rules, the build instructions and the
claims ledger. Reads the built pages (website/out/*.html), so run `npm run build` in website/ first.

Run:  python3 website/tests/copy_lint.py            (errors fail the run, warnings are for a human)
      python3 website/tests/copy_lint.py --self-test (proves every check still fires)

Text inside an element marked data-sample is illustrative sample data: it is checked for writing
rules, but not against the number allowlist. Text inside data-placeholder is listed as a warning.
"""
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
OUT = SITE / "out"

BANNED_WORDS = [
    "delve", "leverage", "unlock", "seamless", "robust", "game-changer", "game changer", "landscape", "navigate",
    "tapestry", "elevate", "empower", "harness", "cutting-edge", "transformative", "synergy", "paradigm", "journey",
    "realm", "supercharge", "turbo-charge", "in today's fast-paced world", "it's worth noting", "let's dive in",
    "in conclusion", "at the end of the day", "thrilled", "humbled", "guaranteed", "100%", "revolutionary",
    "best-in-class", "world-class", "ai decides", "replace your",
]
# AI-writing fingerprints from Dash's edit-pass checklist (dash-writing, part A). Each is an error.
FINGERPRINTS = [
    (r"[—–‒―]", "A1 em or en dash"),
    (r"\s--\s", "A1 double hyphen used as a dash"),
    (r"\bit'?s not (just )?[^.,]{1,40}, it'?s\b", "A2 'it's not X, it's Y' framing"),
    (r"\bnot just\b", "A2 'not just' framing"),
    (r"\b(the result|the kicker|the catch|the twist|the answer|why does this matter|what does this mean)\?", "A5 set-up question answered straight away"),
    (r"\bhere'?s (the thing|the kicker|the catch|why)\b", "A6 colon teaser"),
    (r"[→←⇒⟶➜➔]|->", "A7 arrow in prose"),
    (r"\b(could|might|may) potentially\b|\bmay help to\b|\bcan help to\b", "A9 stacked hedge"),
    (r"\bin (today's|this) (fast-paced|ever-changing|rapidly evolving)\b", "A4 stock phrase"),
    (r"!", "exclamation mark (not in Dash's voice)"),
]
# Never in public copy: the client's name, confidential or internal detail, prices.
FORBIDDEN = [
    "bcp", "brightstar", "candida", "$35", "$50", "35,000", "50,000", "$2,000", "$2k", "chatgpt", "stage 2",
    "succession economy", "seven domains", "32 skills", "sandbox",
]
# The build instructions and the memo (Dash, 25 and 26 Nov 2026): rules for the words. (pattern, message, case_sensitive)
RULES = [
    (r"\b(the agent|ai|craftarc|the platform)\s+(decides|makes (the|every) (call|decision)|promotes|fires)\b",
     "never imply the AI makes employment decisions: people make every call", False),
    (r"\bmove up\b(?! or move out)", "always the pair 'move up or move out'", False),
    (r"\bbased on evidence\b(?!, not opinion)", "always in full: 'based on evidence, not opinion'", False),
    (r"\bsenior time\b", "say 'leadership time' (one term per concept)", False),
    (r"\bself-reviews?\b", "say 'self-assessment'", False),
    (r"\b360[- ]?(reviews?|surveys?)\b", "say '360-degree dialogues'", False),
    (r"\bpredict", "never write that CraftArc predicts when a leader will be ready", False),
    (r"\bappraisal\b|\bratings? tools?\b", "never position CraftArc as (or against) an appraisal or ratings tool", False),
    (r"\bsome (companies|organizations|firms)\b|\bmany (companies |organizations |firms )?struggle", "no hedges ('some companies', 'many struggle')", False),
    (r"\b60 to 100\b|\b350 lines\b|\b24-month\b|\b(eight|8) to (ten|10) (client )?interviews\b", "no result or figure from the first client", False),
    (r"\bdo-it-yourself\b|\bDIY\b", "never mention the client's do-it-yourself attempt", False),
]
# Lines from the build instructions that must appear word for word.
SPEC_LINES = [
    "Can you tell if your company has a gap in leadership depth?",
    "What are the risks associated with your current leadership profile?",
    "Other tools collect forms. CraftArc holds the conversation.",
    "A live portfolio of your leadership bench.",
    "The firm is building depth at Principal and MD level. The real risk is the Partner layer: behind on the new competencies, slow to be acted on, and short of the development that works best.",
    "Know your bench before your next review cycle.",
    "See the live platform and walk through a sample board pack.",
    "Live and in production at a private equity firm.",
]
BRITISH_SPELLINGS = {
    "organisation": "organization", "organise": "organize", "judgement": "judgment", "licence": "license",
    "colour": "color", "behaviour": "behavior", "centre": "center", "programme": "program", "favourite": "favorite",
    "labour": "labor", "modelled": "modeled", "modelling": "modeling", "analyse": "analyze", "optimise": "optimize",
    "prioritise": "prioritize", "recognise": "recognize", "realise": "realize", "summarise": "summarize",
    "anonymise": "anonymize", "anonymised": "anonymized", "standardise": "standardize", "customise": "customize",
    "minimise": "minimize", "maximise": "maximize", "emphasise": "emphasize", "specialise": "specialize",
    "honour": "honor", "favour": "favor", "neighbour": "neighbor", "endeavour": "endeavor", "catalogue": "catalog",
    "travelling": "traveling", "cancelled": "canceled", "defence": "defense", "offence": "offense", "ageing": "aging",
    "whilst": "while", "amongst": "among", "learnt": "learned", "spelt": "spelled", "grey": "gray", "cheque": "check",
    "enrol": "enroll", "fulfil": "fulfill", "practise": "practice", "candour": "candor",
}
STE_MAX_DESCRIPTIVE = 25   # ASD-STE100: descriptive sentences, 25 words at most
STE_MAX_PROCEDURAL = 20    # instructions, 20 words at most
STE_MAX_PARAGRAPH = 6      # paragraphs, 6 sentences at most
IMPERATIVE_STARTS = ("book", "bring", "write", "see", "read", "watch", "choose", "enter", "please", "tell", "ask",
                     "start", "set", "add", "remove", "run", "check", "confirm", "send", "call", "email", "request", "schedule")
PASSIVE = re.compile(r"\b(is|are|was|were|be|been|being)\s+(\w+ed|\w+en)\s+by\b", re.I)
# Numbers in public copy outside sample data. Each traces to docs/Claims_Ledger.md (section "Next.js rebuild").
ALLOWED_NUMBERS = {
    "1": "U01 (1 in 4), U03 (1/3+), M01 (1 AI agent), Part 1",
    "2": "M02 (2 emerging competencies), Part 2",
    "3": "U03, W04 (ready in 3 years), M02 (3 levels), Part 3",
    "4": "U01 (1 in 4), M01 (four parts), Part 4",
    "5": "W04 (ready in 5 to 7 years), M02 (5 traditional competencies)",
    "7": "W04 (ready in 5 to 7 years), M02 (7 competencies)",
    "17": "U02", "60": "U02 (60% of directors and CEOs), H01 (the 60s story)",
    "25": "L24 (about 25 minutes per conversation)", "360": "M03 (the term 360-degree dialogues)",
    "01": "setup step number", "02": "setup step number", "03": "setup step number",
    "2026": "copyright year and source dates",
}


VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "summary", "figcaption", "label", "option", "button", "a", "title", "dt", "dd",
         "th", "td", "div", "span", "section", "article", "header", "footer", "main", "nav", "ol", "ul", "table", "tr", "dialog", "form", "aside"}


class TextGrab(HTMLParser):
    """Collects text blocks with a flag for sample data and placeholders, tracking nesting with a stack."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []  # (tag, skip, sample, placeholder)
        self.items = []  # (kind, text)
        self.cur = []

    def state(self):
        return self.stack[-1][1:] if self.stack else (False, False, False)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        skip, sample, ph = self.state()
        skip = skip or tag in ("script", "style", "svg", "noscript", "template")
        sample = sample or "data-sample" in a
        ph = ph or "data-placeholder" in a
        if tag in BLOCK:
            self.flush()
        for k in ("alt", "aria-label", "title"):
            if a.get(k) and not skip:
                self.items.append(("attr", a[k]))
        if tag == "meta" and (a.get("name") == "description" or (a.get("property") or "").startswith("og:d")):
            self.items.append(("attr", a.get("content") or ""))
        if tag not in VOID:
            self.stack.append((tag, skip, sample, ph))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self.stack and self.stack[-1][0] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        if tag in BLOCK:
            self.flush()
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        skip, sample, ph = self.state()
        if not skip:
            self.cur.append((data, sample, ph))

    def flush(self):
        if not self.cur:
            return
        text = re.sub(r"\s+", " ", "".join(d for d, _, _ in self.cur)).strip()
        sample = any(s for _, s, _ in self.cur)
        ph = any(p for _, _, p in self.cur)
        if text:
            self.items.append(("placeholder" if ph else "sample" if sample else "site", text))
        self.cur = []


def pages():
    return [p for p in sorted(OUT.glob("*.html")) if p.name != "404.html"]


def site_items():
    items = []
    for page in pages():
        g = TextGrab()
        g.feed(page.read_text())
        g.flush()
        items += [(kind, html.unescape(t), page.name) for kind, t in g.items]
    return items


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def check(items):
    errors, warnings = [], []
    for kind, t, page in items:
        where = f"{page} {kind}"
        low = t.lower()
        if kind == "placeholder":
            warnings.append(f"[placeholder, blocked by launch_check.py] {t[:90]}")
        if ";" in t:
            errors.append(f"[semicolon] {where}: {t[:90]}")
        if re.search(r"\s-\s", t):
            errors.append(f"[spaced hyphen used as a dash] {where}: {t[:90]}")
        for pat, label in FINGERPRINTS:
            if re.search(pat, t, flags=re.I):
                errors.append(f"[{label}] {where}: {t[:90]}")
        for w in BANNED_WORDS:
            if re.search(r"(?<![a-z])" + re.escape(w) + r"(?![a-z])", low):
                errors.append(f"[banned word '{w}'] {where}: {t[:90]}")
        for w in FORBIDDEN:
            if re.search(r"(?<![a-z0-9])" + re.escape(w) + r"(?![a-z0-9])", low):
                errors.append(f"[forbidden '{w}'] {where}: {t[:90]}")
        for pat, msg, case in RULES:
            if re.search(pat, t, flags=0 if case else re.I):
                errors.append(f"[{msg}] {where}: {t[:90]}")
        for gb, us in BRITISH_SPELLINGS.items():
            if re.search(r"\b" + gb + r"(s|d|ing)?\b", low):
                errors.append(f"[British spelling '{gb}', use '{us}'] {where}: {t[:90]}")
        if PASSIVE.search(t):
            warnings.append(f"[STE: passive voice, prefer active] {where}: {t[:90]}")
        sents = sentences(t)
        if kind != "attr" and len(sents) > STE_MAX_PARAGRAPH:
            errors.append(f"[STE: paragraph of {len(sents)} sentences, max {STE_MAX_PARAGRAPH}] {where}: {t[:90]}")
        if kind not in ("sample", "placeholder"):
            for n in re.findall(r"(?<![\w.])\d+(?:,\d{3})*", t):
                if n not in ALLOWED_NUMBERS:
                    errors.append(f"[number '{n}' not in the claims ledger] {where}: {t[:90]}")
        if re.search(r"\bnot\b[^.]{0,50}\bbut\b", low):
            warnings.append(f"[contrast framing, check it is deliberate] {where}: {t[:90]}")
        if kind == "attr":
            continue
        for s in sents:
            n_words = len(s.split())
            procedural = s.lower().startswith(IMPERATIVE_STARTS)
            limit = STE_MAX_PROCEDURAL if procedural else STE_MAX_DESCRIPTIVE
            if n_words > limit:
                errors.append(f"[STE: {'procedural' if procedural else 'descriptive'} sentence of {n_words} words, max {limit}] {where}: {s[:90]}")
    home = " ".join(t for _, t, page in items if page == "index.html")
    for line in SPEC_LINES:
        if line not in home:
            errors.append(f"[spec line missing or changed on the homepage] {line}")
    return errors, warnings


def main():
    if not (OUT / "index.html").exists():
        print("copy lint: no build found, run `npm run build` in website/ first")
        sys.exit(1)
    items = site_items()
    errors, warnings = check(items)
    report = {"errors": errors, "warnings": warnings, "checked_items": len(items),
              "sample_items": sum(1 for k, _, _ in items if k == "sample")}
    (SITE / "tests" / "copy-lint-results.json").write_text(json.dumps(report, indent=1))
    print(f"copy lint: {len(items)} items checked ({report['sample_items']} sample data), {len(errors)} errors, {len(warnings)} warnings")
    for e in errors:
        print("  ERROR", e)
    for w in warnings:
        print("  WARN ", w)
    sys.exit(1 if errors else 0)


FINGERPRINT_SAMPLES = {
    "A1 em or en dash": "Leaders grow — and so do firms.",
    "A1 double hyphen used as a dash": "Leaders grow -- and so do firms.",
    "A2 'it's not X, it's Y' framing": "It's not a tool, it's a partner.",
    "A2 'not just' framing": "This is not just software.",
    "A5 set-up question answered straight away": "The result? Faster reviews.",
    "A6 colon teaser": "Here's the thing: reviews are slow.",
    "A7 arrow in prose": "Define your standard -> run the cycle.",
    "A9 stacked hedge": "It could potentially help.",
    "A4 stock phrase": "In today's fast-paced world, leaders matter.",
    "exclamation mark (not in Dash's voice)": "Book now!",
}
RULE_SAMPLES = {
    "never imply the AI makes employment decisions: people make every call": "The agent decides who is promoted.",
    "always the pair 'move up or move out'": "Decide who should move up next year.",
    "always in full: 'based on evidence, not opinion'": "Every call is based on evidence.",
    "say 'leadership time' (one term per concept)": "Without blocking days of senior time.",
    "never write that CraftArc predicts when a leader will be ready": "CraftArc predicts when a leader is ready.",
    "no result or figure from the first client": "They spent 60 to 100 hours on it.",
}


def self_test():
    """Prove every check still fires, that a clean sentence passes, and that sample data is exempt from numbers."""
    failed = [label for label, text in FINGERPRINT_SAMPLES.items()
              if label not in [l for p, l in FINGERPRINTS if re.search(p, text, flags=re.I)]]
    for msg, text in RULE_SAMPLES.items():
        if not any(m == msg and re.search(p, text, flags=0 if c else re.I) for p, m, c in RULES):
            failed.append(f"rule: {msg}")
    clean = "The agent gathers evidence and drafts. Evaluators and boards decide."
    if [l for p, l in FINGERPRINTS if re.search(p, clean, flags=re.I)] or [m for p, m, c in RULES if re.search(p, clean, flags=0 if c else re.I)]:
        failed.append("clean sentence was flagged")
    if [m for p, m, c in RULES if re.search(p, "The agent never makes the call. The evaluator does.", flags=re.I)]:
        failed.append("'never makes the call' was flagged")
    g = TextGrab()
    g.feed('<p>We have 99 leaders.</p><div data-sample><p>56% below target.</p></div><p data-placeholder>[slot 42]</p>')
    g.flush()
    errs, _ = check([(k, t, "test.html") for k, t in g.items])
    nums = [e for e in errs if "number" in e]
    if len(nums) != 1 or "99" not in nums[0]:
        failed.append(f"sample-data number exemption ({nums})")
    if not re.search(r"\borganisation(s|d|ing)?\b", "our organisations grow"):
        failed.append("British spelling check")
    if len(sentences("One. Two. Three. Four. Five. Six. Seven.")) <= STE_MAX_PARAGRAPH:
        failed.append("STE paragraph limit")
    if not PASSIVE.search("The memo is drafted by the agent."):
        failed.append("STE passive voice check")
    total = len(FINGERPRINT_SAMPLES) + len(RULE_SAMPLES) + 6
    print(f"self-test: {total - len(failed)} of {total} checks fire (AI fingerprints, word rules, sample data, spelling, ASD-STE100)"
          + ("" if not failed else f", FAILED: {failed}"))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    self_test() if "--self-test" in sys.argv else main()
