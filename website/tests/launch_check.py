"""Go or no-go for publishing the website. Run: python3 website/tests/launch_check.py

Fails while anything that must not go live is still in place: placeholder proof,
an unconnected lead form, or unapproved offer wording. It is meant to fail
until Dash supplies the real proof.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = sorted(ROOT.glob("*.html"))
html = "\n".join(p.read_text() for p in PAGES)  # every page of the site
config = (ROOT / "config.js").read_text()

checks = []
ph = re.findall(r'data-placeholder|class="[^"]*\bplaceholder\b', html)
by_page = {p.name: len(re.findall(r'data-placeholder', p.read_text())) for p in PAGES}
left = ", ".join(f"{k} ({v})" for k, v in by_page.items() if v)
checks.append(("No placeholders left (proof slots, homepage video, sector pages)", not ph, f"still in: {left}"))
endpoint = re.search(r'leadEndpoint:\s*"([^"]*)"', config).group(1)
email = re.search(r'leadEmail:\s*"([^"]*)"', config).group(1)
checks.append(("Lead form is connected", bool(endpoint or email), "set leadEndpoint or leadEmail in config.js"))
checks.append(("Leads arrive without the visitor's email app", bool(endpoint),
               "only leadEmail is set, so the form opens the visitor's email app; set leadEndpoint (for example Formspree)"))
for term in ("fixed for four years", "build-out", "three to four meetings", "small number of firms"):
    checks.append((f'Unapproved term absent: "{term}"', term not in html.lower(), "remove it from index.html"))
checks.append(("Search indexing allowed (noindex removed)", 'name="robots" content="noindex"' not in html,
               "remove the robots noindex meta tag from every page"))
video = ROOT / "assets" / "video" / "craftarc-vsl-720p.mp4"
checks.append(("Video file present", video.exists() and video.stat().st_size > 1_000_000, "copy the 720p render"))

hard_fail = False
for name, ok, fix in checks:
    soft = name.startswith("Leads arrive without")
    status = "PASS" if ok else ("WARN" if soft else "FAIL")
    hard_fail |= (not ok and not soft)
    print(f"{status:5} {name}" + ("" if ok else f"  ->  {fix}"))
print("\nREADY TO LAUNCH" if not hard_fail else "\nNOT READY TO LAUNCH")
sys.exit(1 if hard_fail else 0)
