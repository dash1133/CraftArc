"""Copy checks for the website and the VSL, against Dash's writing rules and the
claims ledger. Run:  python website/tests/copy_lint.py

Errors fail the run. Warnings are for a human to read (for example the one
deliberate "not X but Y" contrast the rules allow).
"""
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "vsl" / "src"))
import script as vsl  # noqa: E402

BANNED_WORDS = [
    "delve", "leverage", "unlock", "seamless", "robust", "game-changer", "game changer", "landscape", "navigate",
    "tapestry", "elevate", "empower", "harness", "cutting-edge", "transformative", "synergy", "paradigm", "journey",
    "realm", "supercharge", "turbo-charge", "in today's fast-paced world", "it's worth noting", "let's dive in",
    "in conclusion", "at the end of the day", "thrilled", "humbled", "guaranteed", "100%", "revolutionary",
    "best-in-class", "world-class", "ai decides", "replace your",
]
# AI-writing fingerprints from Dash's edit-pass checklist (dash-writing, part A). Each is an error.
FINGERPRINTS = [
    (r"[\u2014\u2013\u2012\u2015]", "A1 em or en dash"),
    (r"\s--\s", "A1 double hyphen used as a dash"),
    (r"\bit'?s not (just )?[^.,]{1,40}, it'?s\b", "A2 'it's not X, it's Y' framing"),
    (r"\bnot just\b", "A2 'not just' framing"),
    (r"\b(the result|the kicker|the catch|the twist|the answer|why does this matter|what does this mean)\?", "A5 set-up question answered straight away"),
    (r"\bhere'?s (the thing|the kicker|the catch|why)\b", "A6 colon teaser"),
    (r"[\u2192\u2190\u21d2\u27f6\u279c\u2794]", "A7 arrow in prose"),
    (r"\b(could|might|may) potentially\b|\bmay help to\b|\bcan help to\b", "A9 stacked hedge"),
    (r"\bin (today's|this) (fast-paced|ever-changing|rapidly evolving)\b", "A4 stock phrase"),
    (r"!", "exclamation mark (not in Dash's voice)"),
]

# Must never reach public copy (fact set: [Internal], [To build], unapproved price, confidential client detail).
FORBIDDEN = [
    "bcp", "candida", "$35", "$50", "35,000", "50,000", "$2k", "163", "stage 2", "trend", "email and chat",
    "assessment centre", "95%", "succession economy", "seven domains", "32 skills", "two central tests",
    "firm-wide insight", "calibration across", "managing out", "pulse check", "baseline framework", "sandbox",
]
# American spelling (Dash, 22 Nov 2026). Each British form maps to the American one.
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
    "enrol": "enroll", "fulfil": "fulfill", "practise": "practice",
}
# ASD-STE100 (Simplified Technical English), the measurable parts, adapted for marketing copy.
STE_MAX_DESCRIPTIVE = 25   # rule 4.x: descriptive sentences, 25 words at most
STE_MAX_PROCEDURAL = 20    # rule 5.x: procedural (instruction) sentences, 20 words at most
STE_MAX_PARAGRAPH = 6      # rule 6.x: paragraphs, 6 sentences at most
IMPERATIVE_STARTS = ("book", "bring", "write", "see", "read", "watch", "choose", "enter", "please", "tell", "ask",
                     "start", "set", "add", "remove", "run", "check", "confirm", "send", "call", "email", "request")
PASSIVE = re.compile(r"\b(is|are|was|were|be|been|being)\s+(\w+ed|\w+en)\s+by\b", re.I)
# Every number in public copy must be one of these, each traced to the claims ledger or the page itself.
ALLOWED_NUMBERS = {
    "60": "L01", "100": "L01", "350": "L01", "24": "P02", "2": "video length / $2B band",
    "1": "step 1 / $1B band", "3": "step 3", "4": "step 4", "5": "step 5 / $5B band", "10": "$10B band / team size",
    "25": "L24 (about 25 minutes per conversation) / team size band",
    "4,000": "R1", "800": "R1", "1970": "R1", "2017": "R1", "2019": "R2", "2026": "copyright year", "70": "G1", "82": "G2", "2015": "G1, G2", "26": "team size band", "50": "team size band", "2027": "form timing options",
}


class TextGrab(HTMLParser):
    BLOCK = {"p", "li", "h1", "h2", "h3", "summary", "figcaption", "label", "option", "button", "a", "title"}

    def __init__(self):
        super().__init__()
        self.skip = 0
        self.stack = []
        self.blocks = []
        self.cur = []
        self.attrs_text = []
        self.pending_tag = None
        self.pending = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style", "svg"):  # svg text is diagram labels, not copy
            self.skip += 1
        for k in ("alt", "aria-label", "content", "title"):
            if a.get(k) and (tag != "meta" or a.get("name") == "description" or a.get("property", "").startswith("og:")):
                if k == "content" and tag == "meta" and a.get("property") == "og:type":
                    continue
                if k == "content" and tag == "meta" and a.get("property") == "og:image":
                    continue
                self.attrs_text.append(a[k])
        if tag in self.BLOCK:
            self.flush()
            self.stack.append(tag)
        if "data-pending" in a or "data-placeholder" in a:
            self.flush()
            self.pending_tag = tag

    def handle_endtag(self, tag):
        if tag in ("script", "style", "svg"):
            self.skip -= 1
        if tag in self.BLOCK:
            self.flush()
        if tag == self.pending_tag:
            self.pending_tag = None

    def handle_data(self, data):
        if not self.skip:
            self.cur.append(data)

    def flush(self):
        t = re.sub(r"\s+", " ", "".join(self.cur)).strip()
        if t:
            (self.pending if self.pending_tag else self.blocks).append(t)
        self.cur = []


def site_text():
    g = TextGrab()
    for page in sorted((ROOT / "website").glob("*.html")):  # every page of the site
        g.feed(page.read_text())
        g.flush()
    return ([html.unescape(b) for b in g.blocks], [html.unescape(a) for a in g.attrs_text],
            [html.unescape(p) for p in g.pending])


def vsl_text():
    out = []
    for sc in vsl.SCENES:
        for s in sc["sentences"]:
            out.append(("caption", s["cap"]))
            for k in ("big", "small", "kicker", "chip", "source", "bubble"):
                if s.get(k):
                    out.append((k, s[k]))
        out.append(("scene label", sc["label"]))
    for card in vsl.PROOF_CARDS:
        out += [("proof card", c) for c in card]
    for item in vsl.OFFER_ITEMS:
        out += [("offer item", c) for c in item]
    out += [("cta", vsl.CTA[k]) for k in ("title", "sub", "fine")] + [("cta", " ".join(vsl.CTA["intro"]))]
    return out


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def main():
    errors, warnings = [], []
    tl = ROOT / "vsl" / "build" / "timeline.json"
    if tl.exists():  # the stated video length is allowed, and only the real one
        mins, secs = divmod(int(json.loads(tl.read_text())["duration"]), 60)  # players round down
        ALLOWED_NUMBERS.setdefault(str(mins), "video length")
        ALLOWED_NUMBERS.setdefault(str(secs), "video length")
    blocks, attrs, pending = site_text()
    items = ([("site", b) for b in blocks] + [("site attr", a) for a in attrs] + [("site pending", p) for p in pending]
             + [("vsl " + k, t) for k, t in vsl_text()])
    for p in pending:
        warnings.append(f"[placeholder, blocked by launch_check.py] {p[:90]}")

    for where, t in items:
        low = t.lower()
        if "—" in t or "–" in t:
            errors.append(f"[dash] {where}: {t[:90]}")
        if re.search(r"\s-\s", t):
            errors.append(f"[spaced hyphen used as a dash] {where}: {t[:90]}")
        if ";" in t:
            errors.append(f"[semicolon] {where}: {t[:90]}")
        for pat, label in FINGERPRINTS:
            if re.search(pat, t, flags=re.I):
                errors.append(f"[{label}] {where}: {t[:90]}")
        for w in BANNED_WORDS:
            if re.search(r"(?<![a-z])" + re.escape(w) + r"(?![a-z])", low):
                errors.append(f"[banned word '{w}'] {where}: {t[:90]}")
        for w in FORBIDDEN:
            if re.search(r"(?<![a-z0-9])" + re.escape(w) + r"(?![a-z0-9])", low):
                errors.append(f"[forbidden claim '{w}'] {where}: {t[:90]}")
        for gb, us in BRITISH_SPELLINGS.items():
            if re.search(r"\b" + gb + r"(s|d|ing)?\b", low):
                msg = f"[British spelling '{gb}', use '{us}'] {where}: {t[:90]}"
                # The rendered video's burned-in captions cannot change without a re-render (CLAUDE.md item 7).
                (warnings if where.startswith("vsl") else errors).append(msg + (" (video: needs a re-render)" if where.startswith("vsl") else ""))
        if where.startswith("site") and PASSIVE.search(t):
            warnings.append(f"[STE: passive voice, prefer active] {where}: {t[:90]}")
        sents = sentences(t)
        if where.startswith("site") and len(sents) > STE_MAX_PARAGRAPH:
            errors.append(f"[STE: paragraph of {len(sents)} sentences, max {STE_MAX_PARAGRAPH}] {where}: {t[:90]}")
        for n in re.findall(r"(?<![\w.])\d+(?:,\d{3})*", t):
            if n not in ALLOWED_NUMBERS and where != "site pending":
                errors.append(f"[number '{n}' not in the claims ledger] {where}: {t[:90]}")
        if re.search(r"\bnot\b[^.]{0,50}\bbut\b", low):
            warnings.append(f"[contrast framing, check it is deliberate] {where}: {t[:90]}")
        for s in sents:
            n_words = len(s.split())
            if where not in ("site", "site pending", "vsl caption"):
                continue
            procedural = s.lower().startswith(IMPERATIVE_STARTS)
            limit = STE_MAX_PROCEDURAL if procedural else STE_MAX_DESCRIPTIVE
            if n_words > limit:
                kind = "procedural" if procedural else "descriptive"
                errors.append(f"[STE: {kind} sentence of {n_words} words, max {limit}] {where}: {s[:90]}")

    # Spoken word count and pace (Dash: 150 to 160 words a minute is his pace).
    spoken = sum(len(vsl.spoken(s).split()) for _, _, _, s in vsl.all_sentences())
    report = {"errors": errors, "warnings": warnings, "checked_items": len(items), "vsl_spoken_words": spoken}
    if tl.exists():
        d = json.loads(tl.read_text())["duration"]
        report["vsl_runtime_s"] = d
        report["vsl_wpm"] = round(spoken / d * 60)
    out = ROOT / "website" / "tests" / "copy-lint-results.json"
    out.write_text(json.dumps(report, indent=1))
    print(f"copy lint: {len(items)} items checked, {len(errors)} errors, {len(warnings)} warnings, "
          f"{spoken} spoken VSL words" + (f", {report['vsl_runtime_s']:.0f}s" if "vsl_runtime_s" in report else ""))
    for e in errors:
        print("  ERROR", e)
    for w in warnings:
        print("  WARN ", w)
    sys.exit(1 if errors else 0)


FINGERPRINT_SAMPLES = {
    "A1 em or en dash": "Leaders grow \u2014 and so do firms.",
    "A1 double hyphen used as a dash": "Leaders grow -- and so do firms.",
    "A2 'it's not X, it's Y' framing": "It's not a tool, it's a partner.",
    "A2 'not just' framing": "This is not just software.",
    "A5 set-up question answered straight away": "The result? Faster reviews.",
    "A6 colon teaser": "Here's the thing: reviews are slow.",
    "A7 arrow in prose": "Read more \u2192",
    "A9 stacked hedge": "It could potentially help.",
    "A4 stock phrase": "In today's fast-paced world, leaders matter.",
    "exclamation mark (not in Dash's voice)": "Book now!",
}


def self_test():
    """Prove every fingerprint check still fires, and a clean sentence passes."""
    failed = [label for label, text in FINGERPRINT_SAMPLES.items()
              if label not in [l for p, l in FINGERPRINTS if re.search(p, text, flags=re.I)]]
    clean = "CraftArc helps every leader trace their arc, competency by competency."
    if [l for p, l in FINGERPRINTS if re.search(p, clean, flags=re.I)]:
        failed.append("clean sentence was flagged")
    # American spelling and ASD-STE100 checks
    if not re.search(r"\borganisation(s|d|ing)?\b", "our organisations grow"):
        failed.append("British spelling check")
    long_instruction = "Book a demo " + "and bring your framework " * 5
    if not (long_instruction.lower().startswith(IMPERATIVE_STARTS) and len(long_instruction.split()) > STE_MAX_PROCEDURAL):
        failed.append("STE procedural sentence limit")
    if len(sentences("One. Two. Three. Four. Five. Six. Seven.")) <= STE_MAX_PARAGRAPH:
        failed.append("STE paragraph limit")
    if not PASSIVE.search("The memo is drafted by the agent."):
        failed.append("STE passive voice check")
    total = len(FINGERPRINT_SAMPLES) + 4
    print(f"self-test: {total - len(failed)} of {total} checks fire (AI fingerprints, American spelling, ASD-STE100)"
          + ("" if not failed else f", FAILED: {failed}"))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    self_test() if "--self-test" in sys.argv else main()
