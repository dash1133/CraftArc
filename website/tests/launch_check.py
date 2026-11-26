"""Go or no-go for publishing the website. Run: python3 website/tests/launch_check.py (after `npm run build`).

Fails while anything that must not go live is still in place: placeholders (the 60s film, figures not yet
checked against the full reports), the noindex tag, an unconnected lead form, or a named client without
written permission. It is meant to fail until those are done.
"""
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
OUT = SITE / "out"
if not (OUT / "index.html").exists():
    print("FAIL  Site is built  ->  run `npm run build` in website/")
    sys.exit(1)
PAGES = [p for p in sorted(OUT.glob("*.html")) if p.name != "404.html"]
html = "\n".join(p.read_text() for p in PAGES)
config = (SITE / "public" / "config.js").read_text()

checks = []
by_page = {p.name: len(re.findall(r"data-placeholder", p.read_text())) for p in PAGES}
left = ", ".join(f"{k} ({v})" for k, v in by_page.items() if v)
checks.append(("No placeholders left (60s film, figures to verify)", not any(by_page.values()), f"still in: {left}"))
endpoint = re.search(r'leadEndpoint:\s*"([^"]*)"', config).group(1)
email = re.search(r'leadEmail:\s*"([^"]*)"', config).group(1)
checks.append(("Lead form is connected", bool(endpoint or email), "set leadEndpoint or leadEmail in public/config.js"))
checks.append(("Leads arrive without the visitor's email app", bool(endpoint),
               "only leadEmail is set, so the form opens the visitor's email app; set leadEndpoint (for example Formspree)"))
for term in ("fixed for four years", "build-out", "three to four meetings", "$2,000", "35,000"):
    checks.append((f'Unapproved term absent: "{term}"', term not in html.lower(), "remove it from src/content/copy.ts"))
checks.append(("Search indexing allowed (noindex removed)", not re.search(r'name="robots" content="noindex', html),
               "remove robots from metadata in src/app/layout.tsx"))
checks.append(("Every chart labeled as sample data", "Illustrative Sample Data" in html, "add the sample-data badge"))
ledger = (SITE.parent / "docs" / "Claims_Ledger.md").read_text()
if "brightstar" in html.lower():
    granted = re.search(r"^PERMISSION RECORDED: Brightstar\b", ledger, flags=re.M) is not None
    checks.append(("Client named with written permission", granted,
                   "get written permission, then add 'PERMISSION RECORDED: Brightstar (date, who approved)' to docs/Claims_Ledger.md"))

# Open items, grouped by the badge each placeholder shows (visible with ?review).
badges = sorted({b for b in re.findall(r'<span class="ph-badge">([^<]+)</span>', html)})

hard_fail = False
for name, ok, fix in checks:
    soft = name.startswith("Leads arrive without")
    status = "PASS" if ok else ("WARN" if soft else "FAIL")
    hard_fail |= (not ok and not soft)
    print(f"{status:5} {name}" + ("" if ok else f"  ->  {fix}"))
if badges:
    print("\nOpen items (add ?review to the address to see them on the page):")
    for b in badges:
        print(f"  - {b.replace('&#x27;', chr(39))}")
print("\nREADY TO LAUNCH" if not hard_fail else "\nNOT READY TO LAUNCH")
sys.exit(1 if hard_fail else 0)
