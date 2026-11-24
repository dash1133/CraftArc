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
DATE = "24 November 2026"

B, P, A = "Launch blocker", "Before launch", "After launch"

GROUPS = [
    ("Dash, founder", "Decisions and approvals only you can give.", [
        ("Send CraftArc Approved Copy", "The master document the website guidance points to. Its sections 1, 3, 4 and the eight Review Cycle steps replace the drafts on the homepage, the industry pages and the About page, word for word.", B),
        ("Approve or reword the Leadership Cockpit tag", "The site shows \"Not yet live\" on the Cockpit. Approve it, reword it, or decide to leave the Cockpit off the homepage for now (guidance gap 1).", B),
        ("Approve the drafted copy", "How you start steps, Who it is for, the seven FAQ answers, the Book a demo line and form fields, the industry cards and the industry page heroes (guidance gaps 3, 4 and 5). Each shows a draft badge on the site.", B),
        ("Write the founder note for the About page", "A short note beside the elevator pitch (guidance gap 6). The site shows your content v5 note as a stand-in.", B),
        ("Confirm the Development Arc status", "The guidance calls it partly live. Say which parts are live, so its card matches (claims ledger flag 11).", B),
        ("Confirm the public pricing position", "\"Leaders and evaluation coordinators are unlimited, colleagues who give feedback are never charged\" is the stance you want, as the FAQ draft says.", P),
        ("Decide on Investment Banks", "The menu keeps Investment Banks under Private Equity and VC, marked coming soon (claims ledger flag 14).", P),
        ("Record the voiceover in your own voice", "At least the founder line, so the spoken AI-voice disclosure can go.", A),
    ]),
    ("Anchor client relationship", "The private equity firm that is the first paying client. The site never names it.", [
        ("Get one result or one quote, with written consent", "Fills the proof slot on the homepage and the Private Equity and VC page (guidance gap 2).", B),
        ("Confirm the demo framework is not theirs", "The competency names on the screens (Deal Sourcing & Origination, Investment Judgment, Portfolio Value Creation) are not from their confidential framework.", B),
        ("Ask whether they will take reference calls", "A yes or no, and a contact if yes.", A),
    ]),
    ("Engineering", "Website, deployment and lead handling.", [
        ("Confirm the Vercel deployment", "craftarc-website.vercel.app shows the homepage from main, and the craftarc.ai domain points to it.", B),
        ("Swap in approved copy as it arrives", "Edit tools/build_site.py, remove each draft badge, run the build and the checklist in CLAUDE.md.", B),
        ("Connect a lead endpoint", "A form service (for example Formspree) forwards to dash@craftarc.ai, set as leadEndpoint in website/config.js, so leads arrive without the visitor's email app.", P),
        ("Swap in the new product video", "Replace the homepage placeholder and the Private Equity and VC video after the revamp, and update the stated length.", P),
        ("Remove noindex and run the launch check", "Delete the robots noindex tag in tools/build_site.py and run website/tests/launch_check.py until it prints READY TO LAUNCH.", B),
        ("Add analytics", "Google Tag Manager or the LinkedIn Insight Tag reads the lead_submitted and cta_click events the site already sends.", A),
    ]),
    ("Product", "The app, the demo and the screens the site shows.", [
        ("Make the demo ready", "A demo instance you can run live on a prospect's leadership levels, so the Book a demo copy can promise it.", P),
        ("Confirm how anonymity works in small teams", "What \"colleagues can give feedback anonymously\" means in practice when a write-up cites a colleague's role.", P),
        ("Provide industry-neutral product screens", "Sample data that is not private equity, for the homepage and the industry pages.", P),
        ("Build the Leadership Cockpit", "The slate of successors, with ready now, ready in 3 years and ready in 5 to 7 years. Then the \"Not yet live\" tag comes off.", A),
    ]),
    ("Marketing and content", "Video, industry copy and reviews.", [
        ("Revamp the product video", "A new film that follows the eight Review Cycle steps and the guidance's terms (development commitments, evaluation coordinator, 360-degree dialogues).", P),
        ("Test the drafts with CEO readers", "Run the drafted industry copy and the solution section past real CEOs. docs/CEO_Reader_Test.md has the simulated first round.", P),
        ("Cut a 60 to 90 second version for LinkedIn", "A short cut of the new video with captions.", A),
    ]),
    ("Legal and compliance", "Policies and the claims the site makes.", [
        ("Confirm the footer legal links cover CraftArc", "AgenticPM's Terms of Service, Privacy Policy and Trust Center apply to CraftArc, or CraftArc versions are published and the links swapped.", B),
        ("Publish a full privacy notice", "Replaces the short statement in the footer, and covers the demo form.", B),
        ("Review the \"general AI assistant\" FAQ answer", "Confirm the comparison is acceptable as worded.", P),
        ("Add cookie consent if analytics go live", "Consent banner and settings in line with the analytics Engineering adds.", A),
    ]),
]

LIVE = [
    "Website: rebuilt to the CraftArc Website Guidance. Twelve-section homepage, About and Book a demo pages, six industry pages, every page generated from one source.",
    "Lead form: on the Book a demo page, with the industry preset from each industry page. Attribution, scoring and email fallback to dash@craftarc.ai. 45 browser tests pass.",
    "Video: the 2 minute 13 second private equity film, beside the eight steps on the Private Equity and VC page, until the revamp.",
    "Claims ledger: approved lines, drafts and withdrawn claims traced for issue 010.",
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
