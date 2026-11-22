"""Build the CraftArc launch to-do list as HTML and PDF.

Edit TASKS below, then run:  python3 docs/todo/build_todo.py
Writes docs/CraftArc_Launch_ToDo.html and docs/CraftArc_Launch_ToDo.pdf (A4, via the
pre-installed Chromium). Sources point to docs/Claims_Ledger.md (flags), docs/Review_Report.md
and website/tests/launch_check.py.
"""
import html
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_HTML = ROOT / "docs" / "CraftArc_Launch_ToDo.html"
OUT_PDF = ROOT / "docs" / "CraftArc_Launch_ToDo.pdf"
DATE = "22 November 2026"

B, P, A = "Launch blocker", "Before launch", "After launch"

GROUPS = [
    ("Dash, founder", "Decisions and approvals only you can give.", [
        ("Supply the live firm's first-cycle result", "A real figure, such as the self-review completion rate or senior hours saved, fills the proof slot on the private equity page.", B),
        ("Supply an approved client quote", "A quote with the person's name and role, and their written permission to use it.", B),
        ("Confirm the exit right is a standard term", "The refund-if-we-miss term holds for every new client, not only the first one.", P),
        ("Confirm the public pricing position", "\"Participants and evaluators are unlimited, contributors are never charged\" is the stance you want, which rules out per-person pricing.", P),
        ("Give leader hours per full cycle", "One number covering the self-review, contributor interviews and coordinator time, for the FAQ.", P),
        ("Decide the \"tracks progress\" wording", "Keep it as your commitment, or add \"within the year\" until cross-cycle trends ship in Stage 2 (June 2027).", P),
        ("Approve the sector page template", "Template agreed in the next session, then copy approved for each of the five sector pages.", P),
        ("Confirm the six to eight week onboarding promise", "Delivery can take a new client from first meeting to a ready cycle in six to eight weeks, as the homepage now promises.", P),
        ("Record the voiceover in your own voice", "At least the founder line, so the spoken AI-voice disclosure can go.", A),
    ]),
    ("Anchor client relationship", "Permissions from the private equity firm whose story the site tells.", [
        ("Get Brightstar's written permission to be named", "Written approval to name Brightstar Capital Partners and tell its story on the site (the do-it-yourself attempt, the 24-month license, building it with their COO, and the plan to extend across the firm). Record it in the claims ledger so the launch check passes.", B),
        ("Confirm the demo framework is not theirs", "The competency names on the screens (Deal Sourcing & Origination, Investment Judgment, Portfolio Value Creation) are not from their confidential framework.", B),
        ("Ask whether they will take reference calls", "A yes or no, and a contact if yes.", A),
    ]),
    ("Engineering", "Website, deployment and lead handling.", [
        ("Confirm the Vercel deployment", "craftarc-website.vercel.app shows the homepage from main, and the craftarc.ai domain points to it.", B),
        ("Connect a lead endpoint", "A form service (for example Formspree) forwards to dash@craftarc.ai, set as leadEndpoint in website/config.js, so leads arrive without the visitor's email app.", P),
        ("Swap in the homepage overview video", "Replace the placeholder on index.html when Marketing delivers the video.", P),
        ("Build the five sector pages", "Financial Services, Healthcare & Life Sciences, Technology, Manufacturing & Industrial and Professional Services, from the approved template.", P),
        ("Remove noindex and run the launch check", "Delete the robots noindex tag from every page and run website/tests/launch_check.py until it prints READY TO LAUNCH.", B),
        ("Add analytics", "Google Tag Manager or the LinkedIn Insight Tag reads the lead_submitted and cta_click events the site already sends.", A),
    ]),
    ("Product", "The app, the demo and the screens the site shows.", [
        ("Make the sample-firm demo ready", "A demo instance you can run live, so the call to action can promise \"we will show you\" rather than \"talk through\".", P),
        ("Confirm how anonymity works in small teams", "What \"anonymised as your firm chooses\" means in practice when a writeup cites a contributor's role.", P),
        ("Provide industry-neutral product screens", "Sample data that is not private equity, for the homepage and the sector pages.", P),
        ("Capture a real self-review conversation", "Replace the four sample turns on the self-review screen with a real, anonymised exchange.", A),
    ]),
    ("Marketing and content", "Video, sector copy and reviews.", [
        ("Produce the industry-neutral overview video", "A short film for the homepage placeholder, built the same way as the private equity video.", P),
        ("Research evidence for each sector", "One or two sourced findings per industry, traced in the claims ledger the way the Gallup figures are.", P),
        ("Write the five sector pages", "Copy for each industry and its three sub-sectors, in the approved template and Dash's writing style.", P),
        ("Re-run the three reviews", "The simulated Hormozi lens, the buyer persona and the claims check, on the new homepage and the private equity page.", P),
        ("Cut a 60 to 90 second version for LinkedIn", "A short cut of the private equity video with captions.", A),
    ]),
    ("Legal and compliance", "Policies and the claims the site makes.", [
        ("Confirm the footer legal links cover CraftArc", "AgenticPM's Terms of Service, Privacy Policy and Trust Center apply to CraftArc, or CraftArc versions are published and the links swapped.", B),
        ("Publish a full privacy notice", "Replaces the short statement in the footer, and covers the demo form.", B),
        ("Review the \"general AI assistant\" line", "The anchor story stands in for a named AI assistant. Confirm the wording is acceptable.", P),
        ("Add cookie consent if analytics go live", "Consent banner and settings in line with the analytics Engineering adds.", A),
    ]),
]

LIVE = [
    "Website: homepage from content v5, Private Markets page with the video, six-industry menu, light design, AgenticPM-style footer.",
    "Lead form: validation, scoring, attribution and email fallback to dash@craftarc.ai. 38 browser tests pass.",
    "Video: 2 minute 13 second private equity film with captions, on the private equity page.",
    "Claims ledger: every figure on the site traced to its source.",
]

PILL = {B: "blocker", P: "before", A: "after"}


def esc(s):
    return html.escape(s, quote=False)


def build_html():
    counts = {k: sum(1 for _, _, ts in GROUPS for t in ts if t[2] == k) for k in (B, P, A)}
    total = sum(counts.values())
    logo = (ROOT / "website" / "assets" / "img" / "logo-mark.svg").read_text()
    summary_rows = "".join(
        f"<tr><td>{esc(g)}</td><td>{sum(1 for t in ts if t[2] == B)}</td><td>{sum(1 for t in ts if t[2] == P)}</td>"
        f"<td>{sum(1 for t in ts if t[2] == A)}</td><td class='blank'></td></tr>" for g, _, ts in GROUPS)
    sections, n = [], 0
    for g, desc, ts in GROUPS:
        rows = ""
        for title, done, pri in ts:
            n += 1
            rows += (f"<tr><td class='box'><span></span></td><td class='num'>{n}</td>"
                     f"<td><strong>{esc(title)}</strong><div class='done'>Done when: {esc(done)}</div></td>"
                     f"<td><span class='pill {PILL[pri]}'>{esc(pri)}</span></td><td class='blank'></td></tr>")
        sections.append(f"""
      <section class="group">
        <div class="ghead"><h2>{esc(g)}</h2><p>{esc(desc)}</p></div>
        <table class="tasks">
          <thead><tr><th></th><th>#</th><th>Task</th><th>Priority</th><th>Assigned to</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </section>""")
    live = "".join(f"<li>{esc(x)}</li>" for x in LIVE)
    return f"""<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8"><title>CraftArc launch to-do list</title>
<style>
  @page {{ size: A4; margin: 16mm 14mm 16mm 14mm; }}
  * {{ box-sizing: border-box; }}
  body {{ font-family: Inter, Arial, sans-serif; color: #0f172a; font-size: 9.6pt; line-height: 1.4; margin: 0; }}
  .top {{ display: flex; align-items: center; justify-content: space-between; border-bottom: 3px solid; border-image: linear-gradient(90deg, #245de5, #7c5cff, #f58220) 1; padding-bottom: 10px; margin-bottom: 14px; }}
  .brand {{ display: flex; align-items: center; gap: 10px; }}
  .brand svg {{ width: 34px; height: 34px; }}
  .wordmark {{ font-weight: 800; letter-spacing: 0.18em; font-size: 12pt; }}
  .wordmark b {{ color: #f58220; }}
  .meta {{ text-align: right; color: #64748b; font-size: 8.5pt; }}
  h1 {{ font-size: 20pt; margin: 0 0 4px; letter-spacing: -0.02em; }}
  .lede {{ color: #3b4a61; margin: 0 0 12px; max-width: 160mm; }}
  .cols {{ display: grid; grid-template-columns: 1.1fr 1fr; gap: 12px; margin-bottom: 14px; }}
  .card {{ border: 1px solid #e3e8f2; border-radius: 8px; padding: 10px 12px; background: #f6f8fc; }}
  .card h3 {{ margin: 0 0 6px; font-size: 9.5pt; text-transform: uppercase; letter-spacing: 0.08em; color: #f58220; }}
  .card ul {{ margin: 0; padding-left: 14px; }}
  .card li {{ margin: 2px 0; }}
  table {{ width: 100%; border-collapse: collapse; }}
  .summary th, .summary td {{ text-align: left; padding: 3px 4px; border-bottom: 1px solid #e3e8f2; font-size: 8.8pt; }}
  .summary th {{ color: #64748b; font-weight: 600; }}
  .legend {{ display: flex; gap: 14px; margin: 0 0 10px; font-size: 8.5pt; color: #3b4a61; align-items: center; }}
  .group {{ margin: 0 0 11px; break-inside: auto; }}
  .ghead {{ display: flex; align-items: baseline; gap: 10px; border-left: 4px solid #245de5; padding-left: 8px; margin-bottom: 6px; break-after: avoid; }}
  .ghead h2 {{ font-size: 12.5pt; margin: 0; }}
  .ghead p {{ margin: 0; color: #64748b; font-size: 8.8pt; }}
  .tasks th {{ text-align: left; font-size: 8pt; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; padding: 4px; border-bottom: 1.5px solid #cbd5e1; }}
  .tasks td {{ padding: 4.5px 4px; border-bottom: 1px solid #e3e8f2; vertical-align: top; }}
  .tasks tr {{ break-inside: avoid; }}
  .tasks td.box {{ width: 18px; }}
  .tasks td.box span {{ display: inline-block; width: 11px; height: 11px; border: 1.3px solid #94a3b8; border-radius: 2px; margin-top: 2px; }}
  .tasks td.num {{ width: 20px; color: #64748b; }}
  .tasks td:nth-child(4) {{ width: 92px; }}
  td.blank {{ width: 34mm; border-bottom: 1px solid #94a3b8 !important; }}
  .done {{ color: #3b4a61; font-size: 8.4pt; margin-top: 2px; }}
  .pill {{ display: inline-block; border-radius: 999px; padding: 2px 8px; font-size: 7.6pt; font-weight: 700; white-space: nowrap; }}
  .pill.blocker {{ background: #fee2e2; color: #991b1b; }}
  .pill.before {{ background: #e3ecff; color: #1a47b8; }}
  .pill.after {{ background: #f1f5f9; color: #475569; }}
  .foot {{ margin-top: 10px; color: #64748b; font-size: 8pt; border-top: 1px solid #e3e8f2; padding-top: 6px; }}
</style></head>
<body>
  <div class="top">
    <div class="brand">{logo}<span class="wordmark">CRAFT <b>ARC</b></span></div>
    <div class="meta">Launch to-do list<br>{DATE}</div>
  </div>
  <h1>CraftArc website and video: launch to-do list</h1>
  <p class="lede">{total} tasks, grouped by who owns them. Write a name in "Assigned to" and share this page with each owner. Launch blockers must be done before the site is made public, and the launch check in website/tests/launch_check.py enforces the ones that live on the site.</p>
  <div class="cols">
    <div class="card"><h3>Live now</h3><ul>{live}</ul></div>
    <div class="card"><h3>By owner</h3>
      <table class="summary"><thead><tr><th>Owner</th><th>Blockers</th><th>Before</th><th>After</th><th>Assigned to</th></tr></thead><tbody>{summary_rows}
      <tr><td><strong>Total</strong></td><td><strong>{counts[B]}</strong></td><td><strong>{counts[P]}</strong></td><td><strong>{counts[A]}</strong></td><td></td></tr></tbody></table>
    </div>
  </div>
  <div class="legend"><span class="pill blocker">{B}</span> must be done before going public <span class="pill before">{P}</span> should be done before going public <span class="pill after">{A}</span> can follow the launch</div>
  {''.join(sections)}
  <p class="foot">Sources: docs/Claims_Ledger.md (flags), docs/Review_Report.md (Needs Dash) and website/tests/launch_check.py. Generated from docs/todo/build_todo.py.</p>
</body></html>"""


def main():
    OUT_HTML.write_text(build_html())
    js = f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://{OUT_HTML}', {{ waitUntil: 'load' }});
  await p.pdf({{ path: '{OUT_PDF}', format: 'A4', printBackground: true, preferCSSPageSize: true,
    displayHeaderFooter: true, headerTemplate: '<span></span>',
    footerTemplate: '<div style="font-size:7pt;color:#94a3b8;width:100%;text-align:center;font-family:Arial">CraftArc launch to-do list, {DATE}. Page <span class="pageNumber"></span> of <span class="totalPages"></span></div>' }});
  await b.close();
}})();"""
    subprocess.run(["node", "-e", js], check=True)
    print("wrote", OUT_HTML, "and", OUT_PDF)


if __name__ == "__main__":
    main()
