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
# Must never reach public copy (fact set: [Internal], [To build], unapproved price, confidential client detail).
FORBIDDEN = [
    "brightstar", "bcp", "candida", "$35", "$50", "35,000", "50,000", "$2k", "163", "stage 2", "trend", "email and chat",
    "assessment centre", "95%", "succession economy", "seven domains", "32 skills", "two central tests",
    "firm-wide insight", "calibration across", "managing out", "pulse check", "baseline framework", "sandbox",
]
US_SPELLINGS = {
    "color": "colour", "organization": "organisation", "organize": "organise", "behavior": "behaviour",
    "analyze": "analyse", "optimize": "optimise", "judgment": "judgement", "center": "centre", "license": "licence",
    "program": "programme", "favorite": "favourite", "labor": "labour", "modeled": "modelled", "prioritize": "prioritise",
}
# Every number in public copy must be one of these, each traced to the claims ledger or the page itself.
ALLOWED_NUMBERS = {
    "60": "L01", "100": "L01", "350": "L01", "24": "P02", "2": "video length / $2B band",
    "1": "step 1 / $1B band", "3": "step 3", "4": "step 4", "5": "step 5 / $5B band", "10": "$10B band / team size",
    "25": "L24 (about 25 minutes per conversation) / team size band",
    "4,000": "R1", "800": "R1", "1970": "R1", "2017": "R1", "2019": "R2", "2026": "copyright year", "26": "team size band", "50": "team size band", "2027": "form timing options",
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
        if tag in ("script", "style"):
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
        if tag in ("script", "style"):
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
    g.feed((ROOT / "website" / "index.html").read_text())
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
        for w in BANNED_WORDS:
            if re.search(r"(?<![a-z])" + re.escape(w) + r"(?![a-z])", low):
                errors.append(f"[banned word '{w}'] {where}: {t[:90]}")
        for w in FORBIDDEN:
            if re.search(r"(?<![a-z0-9])" + re.escape(w) + r"(?![a-z0-9])", low):
                errors.append(f"[forbidden claim '{w}'] {where}: {t[:90]}")
        for us, gb in US_SPELLINGS.items():
            # proper names keep their own spelling (the AgenticPM "Trust Center" page)
            if re.search(r"\b" + us + r"(s|d|ing)?\b", low.replace("trust center", "")):
                errors.append(f"[US spelling '{us}', use '{gb}'] {where}: {t[:90]}")
        for n in re.findall(r"(?<![\w.])\d+(?:,\d{3})*", t):
            if n not in ALLOWED_NUMBERS and where != "site pending":
                errors.append(f"[number '{n}' not in the claims ledger] {where}: {t[:90]}")
        if re.search(r"\bnot just\b", low) or re.search(r"\bnot\b[^.]{0,50}\bbut\b", low):
            warnings.append(f"[contrast framing, check it is deliberate] {where}: {t[:90]}")
        for s in sentences(t):
            n_words = len(s.split())
            if n_words > 25 and where in ("site", "site pending", "vsl caption"):
                errors.append(f"[sentence of {n_words} words, max 25] {where}: {s[:90]}")

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


if __name__ == "__main__":
    main()
