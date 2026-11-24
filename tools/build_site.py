"""Builds every page of the CraftArc website from one source (S1000D: shared parts live in one place).

Source: CraftArc Website Guidance (Dash, 24 Nov 2026). Lines the guidance marks Approved are used word for
word. Everything else is a draft that carries a visible badge and a data-placeholder attribute, so
website/tests/launch_check.py blocks the launch until Dash approves it.

Run:   python3 tools/build_site.py           writes website/*.html
       python3 tools/build_site.py --check   fails if a page differs from this source (edit here, not in the HTML)
"""
import sys
from html import escape
from pathlib import Path

SITE = Path(__file__).resolve().parents[1] / "website"

# ------------------------------------------------------------------ approved copy (guidance, word for word)
HERO_Q = "Can you tell how close each leader is to their next role?"
HERO_A = "CraftArc can. Know where every leader stands, and keep every one of them growing toward their next role."
HERO_TIME = "All without blocking days of leadership time."
PROBLEM = ("Every board wants to know the depth of its leadership bench, and who should move up or move out.",
           "Most companies cannot answer either question.")
PROBLEM_SUPPORT = "The craft stays in a few heads."
METHOD = ("Great organizations grow their next leaders on purpose.",
          "Built on the best practices of leading management consulting firms, CraftArc defines what good looks like at each leadership level.")
PROOF = "We have just come out of stealth with our first paying client, a private equity firm."
START_HEAD = "Up and running before your next review cycle."
WHO_LINE = "If that commitment is not there yet, we will say so."

# Badge wording. Every draft shows one, so a draft cannot pass as approved copy.
B_APPROVED_COPY = "Draft placeholder, until CraftArc Approved Copy arrives"
B_NEEDS_APPROVAL = "Draft placeholder, needs Dash's approval"
B_TAG = "Tag wording needs approval"

# ------------------------------------------------------------------ icons
ICON = {
    "pe": '<path d="M3 20h18"/><path d="M5 16l4.5-5 3.5 3 6-7"/><path d="M15 7h4v4"/>',
    "fs": '<path d="M3 9.5L12 4l9 5.5"/><path d="M5 10v8M9.5 10v8M14.5 10v8M19 10v8"/><path d="M3 20.5h18"/>',
    "hls": '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/><path d="M12 9.5v5M9.5 12h5"/>',
    "tech": '<rect x="6" y="6" width="12" height="12" rx="2"/><rect x="9.5" y="9.5" width="5" height="5" rx="1"/><path d="M9 3v3M15 3v3M9 18v3M15 18v3M3 9h3M3 15h3M18 9h3M18 15h3"/>',
    "mfg": '<path d="M3 20.5V10l5 3V10l5 3V10l5 3V5h3v15.5z"/><path d="M7 17h2M11 17h2M15 17h2"/>',
    "ps": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a1.5 1.5 0 0 1 1.5-1.5h3A1.5 1.5 0 0 1 15 5v2"/><path d="M3 12.5h18"/>',
    "know": '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/>',
    "grow": '<path d="M3 20h18"/><path d="M5 16l4.5-5 3.5 3 6-7"/><path d="M15 7h4v4"/>',
    "time": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
    "cockpit": '<rect x="3" y="4" width="18" height="13" rx="2"/><path d="M7 13l3-3 2.5 2L17 8"/><path d="M8 21h8M12 17v4"/>',
    "cycle": '<path d="M20 12a8 8 0 0 1-13.7 5.7"/><path d="M4 12a8 8 0 0 1 13.7-5.7"/><path d="M18 3v4h-4M6 21v-4h4"/>',
    "arc": '<path d="M4 19a8 8 0 0 1 16 0" stroke-dasharray="2.5 3"/><circle cx="4" cy="19" r="1.8"/><circle cx="20" cy="19" r="1.8"/><path d="M12 3v6M9 6l3 3 3-3"/>',
    "agent": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 16l.8 2.2L22 19l-2.2.8L19 22l-.8-2.2L16 19l2.2-.8z"/>',
    "search": '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/>',
    "doc": '<path d="M6 2.5h8l5 5v14H6z"/><path d="M14 2.5v5h5M9 12h7M9 16h7"/>',
    "gear": '<circle cx="12" cy="12" r="3"/><path d="M12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3M5.3 5.3l2.1 2.1M16.6 16.6l2.1 2.1M5.3 18.7l2.1-2.1M16.6 7.4l2.1-2.1"/>',
    "flag": '<path d="M5 21V4"/><path d="M5 4h11l-2 4 2 4H5"/>',
    "play": '<circle cx="12" cy="12" r="9"/><path d="M10 8.5v7l6-3.5z"/>',
    "person": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
}


def tile(name, extra=""):
    cls = "tile" + (" " + extra if extra else "")
    return f'<span class="{cls}" aria-hidden="true"><svg viewBox="0 0 24 24" focusable="false">{ICON[name]}</svg></span>'


def badge(text):
    return f'<span class="ph-badge">{escape(text)}</span>'


# ------------------------------------------------------------------ industries (guidance order, section 8)
# Each industry page changes only two things (guidance): the roles and leadership levels named, and the proof.
INDUSTRIES = [
    dict(slug="private-equity", name="Private Equity and VC", icon="pe", status="live", value="private_equity",
         card="Grow your next partners on purpose. Our first paying client is a private equity firm.",
         q="Can you tell how close each principal and managing director is to partner?",
         a="CraftArc can. Know where every principal and managing director stands, and keep every one of them growing toward partner.",
         key_roles="each partner seat", next_role="partner",
         subs=[("private-equity", "Private Equity", "live", "Our first paying client is a private equity firm."),
               ("venture-capital", "Venture Capital", "soon", "CraftArc for venture capital partners and investment teams. This section is in development."),
               ("investment-banks", "Investment Banks", "soon", "CraftArc for investment banking leaders. This section is in development.")]),
    dict(slug="professional-services", name="Professional Services", icon="ps", status="next", value="professional_services",
         card="Know how close each senior manager and senior associate is to making partner.",
         q="Can you tell how close each senior manager and senior associate is to making partner?",
         a="CraftArc can. Know where every candidate stands, and keep every one of them growing toward partner.",
         key_roles="each partner seat", next_role="partner",
         subs=[("consulting", "Consulting", "soon", ""), ("law", "Law", "soon", ""), ("accounting", "Accounting", "soon", "")]),
    dict(slug="financial-services", name="Financial Services", icon="fs", status="soon", value="financial_services",
         card="Know how close each director is to becoming your next managing director.",
         q="Can you tell how close each director is to becoming your next managing director?",
         a="CraftArc can. Know where every director stands, and keep every one of them growing toward managing director.",
         key_roles="each managing director seat", next_role="managing director",
         subs=[("banking", "Banking & Capital Markets", "soon", ""), ("asset-management", "Asset & Investment Management", "soon", ""),
               ("insurance", "Insurance", "soon", "")]),
    dict(slug="healthcare-life-sciences", name="Healthcare and Life Sciences", icon="hls", status="soon", value="healthcare_life_sciences",
         card="Know how close each leader is to becoming your next division head.",
         q="Can you tell how close each leader is to becoming your next division head?",
         a="CraftArc can. Know where every leader stands, and keep every one of them growing toward division head.",
         key_roles="each division head role", next_role="division head",
         subs=[("providers", "Health Systems & Providers", "soon", ""), ("pharma", "Pharma & Biotech", "soon", ""), ("medtech", "MedTech", "soon", "")]),
    dict(slug="technology", name="Technology", icon="tech", status="soon", value="technology",
         card="Know how close each engineering leader is to becoming your next CTO.",
         q="Can you tell how close each engineering leader is to becoming your next CTO?",
         a="CraftArc can. Know where every engineering leader stands, and keep every one of them growing toward CTO.",
         key_roles="each engineering leadership role", next_role="CTO",
         subs=[("software", "Software & SaaS", "soon", ""), ("it-services", "IT Services", "soon", ""), ("telecom", "Telecom", "soon", "")]),
    dict(slug="manufacturing-industrial", name="Manufacturing and Industrial", icon="mfg", status="soon", value="manufacturing_industrial",
         card="Know how close each plant manager is to becoming your next VP of Operations.",
         q="Can you tell how close each plant manager is to becoming your next VP of Operations?",
         a="CraftArc can. Know where every plant manager stands, and keep every one of them growing toward VP of Operations.",
         key_roles="each plant manager and operations role", next_role="VP of Operations",
         subs=[("industrial-manufacturing", "Industrial Manufacturing", "soon", ""), ("energy", "Energy & Utilities", "soon", ""),
               ("automotive", "Automotive", "soon", "")]),
]
STATUS_LABEL = {"live": "Live", "next": "Coming next", "soon": "Coming soon"}
HOME_TOKENS = dict(key_roles="each key role", next_role="their next role")

# ------------------------------------------------------------------ shared page parts


def head(title, description, extra=""):
    return f"""<!doctype html>
<html lang="en-US">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description)}">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(description)}">
  <meta property="og:type" content="website">
  <meta property="og:image" content="assets/video/poster.jpg">
  <meta name="theme-color" content="#0b1633">
  <meta name="robots" content="noindex"><!-- remove at launch; launch_check.py fails while it is here -->
  <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
  <script src="config.js"></script>
  <script src="app.js" defer></script>{extra}
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
"""


def mega(current=""):
    cols = []
    for ind in INDUSTRIES:
        cur = ' aria-current="page"' if ind["slug"] == current else ""
        subs = "".join(f'<li><a href="{ind["slug"]}.html#{sid}">{escape(name)}</a></li>' for sid, name, _, _ in ind["subs"])
        orange = "orange" if ind["icon"] in ("hls", "ps") else ""
        cols.append(f'<li class="mega-col"><a class="mega-ind" href="{ind["slug"]}.html"{cur}>{tile(ind["icon"], orange)}'
                    f'<strong>{escape(ind["name"])}</strong></a><ul>{subs}</ul></li>')
    return "".join(cols)


def header(current=""):
    return f"""
  <header class="site-header">
    <div class="wrap header-inner">
      <a class="brand" href="index.html" aria-label="CraftArc home">
        <img src="assets/img/logo-mark.svg" alt="" width="36" height="36">
        <span class="wordmark"><span class="w-craft">CRAFT</span> <span class="w-arc">ARC</span></span>
      </a>
      <nav class="nav" aria-label="Main">
        <button class="nav-menu" type="button" aria-expanded="false" aria-controls="industries-menu">Industries <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></button>
        <a href="index.html#how">How it works</a>
        <a href="index.html#faq">FAQ</a>
        <a href="about.html">About</a>
      </nav>
      <a class="btn btn-primary btn-sm" href="book-a-demo.html" data-cta="header">Book a demo</a>
    </div>
    <div class="mega" id="industries-menu" hidden>
      <div class="wrap mega-inner">
        <div class="mega-label"><p>Industries</p><span class="bar" aria-hidden="true"></span></div>
        <ul class="mega-list">{mega(current)}</ul>
      </div>
    </div>
  </header>
"""


FOOTER = """
  <footer class="site-footer">
    <div class="wrap footer-top">
      <div class="footer-brand">
        <a class="footer-logo" href="index.html" aria-label="CraftArc home">
          <img src="assets/img/logo-mark.svg" alt="" width="52" height="52">
          <span class="footer-lockup"><span class="wordmark"><span class="w-craft">CRAFT</span> <span class="w-arc">ARC</span></span><span class="footer-sub">Agentic leadership development</span></span>
        </a>
        <p class="footer-tagline">We help organizations grow their <span class="hl">next leaders</span> on purpose</p>
        <p class="footer-family">Part of the <a href="https://agenticprivatemarkets.ai/" target="_blank" rel="noopener">AgenticPM</a> family</p>
        <ul class="footer-social" aria-label="Follow AgenticPM">
          <li><a class="soc-yt" href="https://www.youtube.com/@AgenticPrivateMarkets" target="_blank" rel="noopener" aria-label="AgenticPM on YouTube"><svg viewBox="0 0 28 20" aria-hidden="true"><rect width="28" height="20" rx="5" fill="#FF0000"/><path d="M11 5.5v9l8-4.5z" fill="#fff"/></svg><span>YouTube</span></a></li>
          <li><a class="soc-li" href="https://www.linkedin.com/company/agenticprivatemarkets/" target="_blank" rel="noopener" aria-label="AgenticPM on LinkedIn"><svg viewBox="0 0 20 20" aria-hidden="true"><rect width="20" height="20" rx="3.5" fill="#0A66C2"/><path d="M4.6 7.6h2.6V16H4.6zM5.9 3.6a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3zM8.9 7.6h2.5v1.2c.4-.7 1.3-1.4 2.6-1.4 2.7 0 3.2 1.8 3.2 4.1V16h-2.6v-4c0-1 0-2.2-1.4-2.2s-1.6 1-1.6 2.1V16H8.9z" fill="#fff"/></svg><span>LinkedIn</span></a></li>
          <li><a class="soc-x" href="https://x.com/AgenticPvtMkts" target="_blank" rel="noopener" aria-label="AgenticPM on X"><svg viewBox="0 0 20 20" aria-hidden="true"><rect width="20" height="20" rx="4" fill="#000"/><path d="M5 4.5h3.1l2.4 3.4 2.9-3.4h1.3L11.1 8.9l4.1 6.6h-3.1l-2.7-3.9-3.3 3.9H4.8l4.1-4.8z" fill="#fff"/></svg></a></li>
        </ul>
      </div>
      <nav class="footer-cols" aria-label="Footer">
        <div>
          <p class="footer-head">Product</p>
          <ul>
            <li><a href="index.html#cockpit">Leadership Cockpit</a></li>
            <li><a href="index.html#review-cycle">Review Cycle</a></li>
            <li><a href="index.html#development-arc">Development Arc</a></li>
            <li><a href="index.html#how">How it works</a></li>
          </ul>
        </div>
        <div>
          <p class="footer-head">Company</p>
          <ul>
            <li><a href="about.html">About CraftArc</a></li>
            <li><a href="https://agenticprivatemarkets.ai/blogs" target="_blank" rel="noopener">Resources</a></li>
            <li><a href="mailto:dash@craftarc.ai">Contact</a></li>
          </ul>
        </div>
        <div>
          <p class="footer-head">Get Started</p>
          <ul>
            <li><a href="book-a-demo.html" data-cta="footer">Book a demo</a></li>
            <li><a href="private-equity.html#video">Watch the video</a></li>
            <li><a href="index.html#faq">FAQ</a></li>
          </ul>
        </div>
        <div>
          <p class="footer-head">Legal</p>
          <ul>
            <li><a href="https://agenticprivatemarkets.ai/legal/terms-of-service" target="_blank" rel="noopener">Terms of Service</a></li>
            <li><a href="https://agenticprivatemarkets.ai/legal/privacy-policy" target="_blank" rel="noopener">Privacy Policy</a></li>
            <li><a href="https://trust.agenticprivatemarkets.ai" target="_blank" rel="noopener">Trust Center</a></li>
          </ul>
        </div>
      </nav>
    </div>
    <div class="wrap footer-bottom" id="privacy">
      <p><strong>Privacy.</strong> We use the details you send only to reply to your request and to arrange a demo. We do not sell them. Product screens show sample data and a sample conversation, and the video voiceover is AI generated.</p>
      <p class="copyright">&copy; 2026 CraftArc, part of the AgenticPM family. All rights reserved.</p>
    </div>
  </footer>
"""

VIEWER = """
  <dialog class="viewer" id="viewer" aria-label="Enlarged product screen">
    <div class="viewer-bar"><p></p><button type="button" data-close>Close</button></div>
    <img alt="">
  </dialog>
"""


def page(title, description, current, main, viewer=False):
    return (head(title, description) + header(current) + '\n  <main id="main">\n' + main + "  </main>\n"
            + FOOTER + (VIEWER if viewer else "") + "</body>\n</html>\n")


# ------------------------------------------------------------------ shared modules (sections)


def hero(q, a, cta_href, crumbs="", eyebrow="", draft=False):
    crumb = f'\n        <p class="crumbs">{crumbs}</p>' if crumbs else ""
    eb = f'\n        <p class="eyebrow">{escape(eyebrow)}</p>' if eyebrow else ""
    mark = f'\n        <p class="hero-draft" data-placeholder>{badge(B_NEEDS_APPROVAL + ": industry wording")}</p>' if draft else ""
    return f"""    <!-- 1 HERO (approved): the question, the answer, the time line, one button -->
    <section class="hero hero-q" id="top">
      <div class="wrap hero-q-inner">{crumb}{eb}{mark}
        <h1>{escape(q)}</h1>
        <p class="hero-answer">{escape(a)}</p>
        <p class="hero-time">{tile("time")}<span>{escape(HERO_TIME)}</span></p>
        <a class="btn btn-primary btn-lg" href="{cta_href}" data-cta="hero">Book a demo</a>
      </div>
    </section>

"""


HERO_VIDEO = """<figure class="video-card hero-video-card">
            <video controls preload="metadata" playsinline poster="assets/video/poster.jpg" aria-label="CraftArc video, placeholder until the new product video is ready">
              <source src="assets/video/craftarc-vsl-720p.mp4" type="video/mp4">
              <track kind="captions" src="assets/video/craftarc-vsl.vtt" srclang="en" label="English (also burned into the video)">
              Your browser cannot play this video. <a href="assets/video/craftarc-vsl-720p.mp4">Download it here.</a>
            </video>
            <figcaption data-placeholder><span class="ph-badge">Placeholder video</span> The private equity film, until the new product video is ready.</figcaption>
          </figure>"""


def home_hero():
    """Homepage hero (Dash, 24 Nov 2026): approved lines on the left, the video on the right, no button in the body."""
    return f"""    <!-- 1 HERO (approved copy): the question, the answer and the time line, beside the video -->
    <section class="hero hero-split" id="top">
      <div class="wrap hero-split-grid">
        <div class="hero-split-copy">
          <h1>{escape(HERO_Q)}</h1>
          <p class="hero-answer">{escape(HERO_A)}</p>
          <p class="hero-time">{tile("time")}<span>{escape(HERO_TIME)}</span></p>
        </div>
        <div class="hero-split-media" id="hero-video">
          {HERO_VIDEO}
        </div>
      </div>
    </section>

"""


def claims(t):
    kr = f'<span data-token="key-roles">{escape(t["key_roles"])}</span>'
    nr = f'<span data-token="next-role">{escape(t["next_role"])}</span>'
    blocks = [
        ("know", "Know", "", f"Know where every leader stands.",
         [f"Your leadership team's slate of successors for {kr}: ready now, ready in 3 years, ready in 5 to 7 years.",
          "A clear answer on who should move up or move out.",
          "Every view based on evidence, not opinion."],
         "cockpit", "Leadership Cockpit", True),
        ("grow", "Grow", "", f"Keep every leader growing toward {nr}.",
         ["A written standard for what good looks like at each leadership level.",
          "Development commitments that each leader owns.",
          "Progress on those commitments, tracked through the year."],
         "development-arc", "Development Arc", False),
        ("time", "Without the time", "orange", HERO_TIME,
         ["The agent runs every self-evaluation and every 360-degree dialogue.",
          "The agent drafts the write-ups for the evaluation coordinator.",
          "Each conversation with the agent takes about 25 minutes, by voice or text."],
         "review-cycle", "Review Cycle", False),
    ]
    out = []
    for key, name, col, claim, outcomes, mod_id, mod_name, soon in blocks:
        lis = "".join(f"<li>{o}</li>" for o in outcomes)
        tag = f' <span class="tag-soon" data-placeholder title="{B_TAG}">Not yet live</span>' if soon else ""
        out.append(f"""          <article class="claim" id="claim-{key}">
            <p class="claim-name">{tile(key, col)}<span>{escape(name)}</span></p>
            <h3>{claim}</h3>
            <ul class="outcomes">{lis}</ul>
            <p class="delivered">Delivered by the <a href="#{mod_id}">{mod_name}</a>{tag}</p>
          </article>""")
    return f"""    <!-- 2 THREE CLAIMS (approved). Claims and outcomes come from Approved Copy section 3. -->
    <section class="section claims" id="claims">
      <div class="wrap">
        <h2 class="sr-only">What CraftArc delivers</h2>
        <p class="draft-note" data-placeholder>{badge(B_APPROVED_COPY + ", section 3")}</p>
        <div class="claims-grid">
{chr(10).join(out)}
        </div>
      </div>
    </section>

"""


def problem():
    return f"""    <!-- 3 THE PROBLEM (approved): a statement, not a section -->
    <section class="section statement" id="problem">
      <div class="wrap narrow">
        <h2>{escape(PROBLEM[0])}</h2>
        <p class="statement-2">{escape(PROBLEM[1])}</p>
        <p class="statement-support">{escape(PROBLEM_SUPPORT)}</p>
      </div>
    </section>

"""


def method():
    steps = "".join(f'<rect x="{20 + i * 78}" y="{150 - i * 34}" width="70" height="{30 + i * 34}" rx="8" class="lvl lvl-{i}"/>'
                    f'<circle cx="{55 + i * 78}" cy="{132 - i * 34}" r="7" class="mark"/>' for i in range(4))
    return f"""    <!-- 4 THE METHOD (approved) -->
    <section class="section method" id="method">
      <div class="wrap method-grid">
        <div>
          <p class="kicker">The method</p>
          <h2>{escape(METHOD[0])}</h2>
          <p class="method-text">{escape(METHOD[1])}</p>
        </div>
        <svg class="ladder" viewBox="0 0 340 200" aria-hidden="true" focusable="false">
          <defs><linearGradient id="ladgrad" x1="0" x2="1"><stop offset="0" stop-color="#245de5"/><stop offset="0.6" stop-color="#7c5cff"/><stop offset="1" stop-color="#f58220"/></linearGradient></defs>
          {steps}
          <path d="M55 132 L133 98 L211 64 L289 30" fill="none" stroke="url(#ladgrad)" stroke-width="3" stroke-dasharray="6 7" stroke-linecap="round"/>
        </svg>
      </div>
    </section>

"""


def solution(t):
    kr = f'<span data-token="key-roles">{escape(t["key_roles"])}</span>'
    return f"""    <!-- 5 THE SOLUTION (approved, not yet tested with CEOs). Text from Approved Copy section 4. -->
    <section class="section solution" id="solution">
      <div class="wrap">
        <p class="kicker">The solution</p>
        <div class="draft-block" data-placeholder>
          {badge(B_APPROVED_COPY + ", section 4")}
          <h2>Three modules, one agent</h2>
          <p class="section-lede">The Review Cycle runs each leader's evaluation. The Development Arc keeps each leader growing through the year. The Leadership Cockpit, now in development, will give the CEO and the board one view of the bench.</p>
        </div>
        <div class="sol-diagram">
          <article class="module module-top" id="cockpit">
            <div class="module-head">{tile("cockpit")}<h3>Leadership Cockpit</h3><span class="tag-soon" data-placeholder title="{B_TAG}">Not yet live</span></div>
            <p class="mod-label">Who uses it</p>
            <p>The CEO, the leadership team and the board.</p>
            <p class="mod-label">What the agent will do</p>
            <p>Keep the slate of successors your leadership team sets for {kr}. Each slate shows who is ready now, ready in 3 years and ready in 5 to 7 years.</p>
          </article>
          <article class="module" id="review-cycle">
            <div class="module-head">{tile("cycle")}<h3>Review Cycle</h3></div>
            <p class="mod-label">Who uses it</p>
            <p>Each leader, the colleagues who give feedback and the evaluation coordinator who runs the review.</p>
            <p class="mod-label">What the agent does</p>
            <p>Runs each self-evaluation and each 360-degree dialogue, then drafts the write-ups against your own standard for each level.</p>
          </article>
          <article class="module" id="development-arc">
            <div class="module-head">{tile("arc", "orange")}<h3>Development Arc</h3></div>
            <p class="mod-label">Who uses it</p>
            <p>Each leader and their evaluation coordinator.</p>
            <p class="mod-label">What the agent does</p>
            <p>Turns the write-ups into development commitments, and helps each leader track them through the year.</p>
          </article>
          <div class="agent-band">{tile("agent")}<p><strong>The CraftArc agent</strong> runs the Review Cycle and the Development Arc, and will run the Leadership Cockpit. It interviews, grades the evidence by source and drafts the write-ups. The evaluation coordinator owns the final wording.</p></div>
        </div>
      </div>
    </section>

"""


STEPS = [
    ("Launch the cycle", "The agent tells each leader and their evaluation coordinator that the cycle has begun."),
    ("Self-evaluation", "The agent interviews each leader about their work, by voice or text, in about 25 minutes."),
    ("Choose who gives feedback", "The agent checks that someone saw each competency first-hand, and flags any gap before the dialogues start."),
    ("360-degree dialogues", "The agent talks with each colleague in confidence, and grades every fact by its source."),
    ("Prepare the dialogue", "The agent drafts the write-ups: the memo for the Executive Committee, a note to the leader and a scorecard."),
    ("Prepare the leader", "The agent walks each leader through their own write-up before the development dialogue."),
    ("Development commitments", "The agent turns the write-ups into a short list of development commitments that the leader owns."),
    ("Track progress", "The agent helps each leader track their development commitments through the year, on their phone."),
]

PE_VIDEO = """<figure class="video-card">
            <video controls preload="metadata" playsinline poster="assets/video/poster.jpg" aria-label="CraftArc video, 2 minutes 13 seconds">
              <source src="assets/video/craftarc-vsl-720p.mp4" type="video/mp4">
              <track kind="captions" src="assets/video/craftarc-vsl.vtt" srclang="en" label="English (also burned into the video)">
              Your browser cannot play this video. <a href="assets/video/craftarc-vsl-720p.mp4">Download it here.</a>
            </video>
            <figcaption>2 minutes 13 seconds. Captions on. The voiceover is AI generated.</figcaption>
          </figure>
          <p class="video-note" data-placeholder>""" + badge("Video revamp in progress") + """ This video tells an earlier version of the story. A new video that follows these steps is in production.</p>"""

HOME_VIDEO = f"""<figure class="video-card video-placeholder" data-placeholder>
            <div class="vp-stage">
              <span class="tile big" aria-hidden="true"><svg viewBox="0 0 24 24" focusable="false">{ICON["play"]}</svg></span>
              <p class="vp-title">Product video coming soon</p>
              <p class="vp-sub">A short film of the Review Cycle, step by step.</p>
              <a class="btn btn-ghost btn-sm" href="private-equity.html#video" data-cta="pe-video">Watch the private equity video</a>
            </div>
            <figcaption><span class="ph-badge">Placeholder, replace before launch</span></figcaption>
          </figure>"""


def how(video_html):
    lis = "\n".join(f'          <li id="step-{i}"><h3>{escape(n)}</h3><p>{escape(l)}</p></li>' for i, (n, l) in enumerate(STEPS, 1))
    return f"""    <!-- 6 HOW IT WORKS (approved): the eight Review Cycle steps beside the product video -->
    <section class="section how-steps" id="how">
      <div class="wrap">
        <p class="kicker">How it works</p>
        <div class="draft-block" data-placeholder>
          {badge(B_APPROVED_COPY + ", the eight steps")}
          <h2>Inside the Review Cycle</h2>
        </div>
        <div class="how-grid">
          <ol class="steps">
{lis}
          </ol>
          <div class="how-media" id="video">
          {video_html}
          </div>
        </div>
      </div>
    </section>

"""


SCREENS = [
    ("07_self_review.webp", "step2_selfreview", 940, 485, "The self-evaluation conversation with the agent, by voice", "The self-evaluation, in the product. Sample conversation."),
    ("05_survey_coverage.webp", "step3_coverage", 1352, 410, "Feedback coverage by competency, with a gap flagged where nobody saw the banker meetings", "Coverage by competency, with a gap flagged. Sample data, some text blurred."),
    ("04_survey_roster.webp", "step3_roster", 1371, 612, "The colleagues who give feedback, each with their vantage point and a summary of their dialogue", "The 360-degree dialogues, in one place. Sample data."),
    ("06_performance_review.webp", "proof_writeup", 885, 440, "A memo for the Executive Committee drafted by the agent, naming the question the evidence could not answer", "A drafted memo for the Executive Committee. Sample data."),
    ("02_my_people.webp", "step5_people", 1880, 340, "Each leader's progress through the cycle, in one view", "Every leader's progress, in one view. Sample data."),
]


def screen(full, stem, w, h, alt, cap):
    a = escape(alt)
    return (f'<figure class="shot-wrap"><button class="zoom shot" type="button" data-full="assets/img/{full}" data-alt="{a}" aria-label="Enlarge: {a}">'
            f'<picture><source srcset="assets/img/{stem}.webp" type="image/webp"><img width="{w}" height="{h}" src="assets/img/{stem}.png" alt="{a}" loading="lazy"></picture>'
            f'<span class="hint" aria-hidden="true">Enlarge</span></button><figcaption class="shot-cap">{escape(cap)}</figcaption></figure>')


def proof_live(gallery=False):
    shots = ""
    if gallery:
        shots = ('\n        <h3 class="gallery-head">In the product</h3>\n        <div class="gallery">'
                 + "".join(screen(*s) for s in SCREENS) + "</div>")
    else:
        shots = "\n        <div class=\"proof-shot\">" + screen(*SCREENS[3]) + "</div>"
    return f"""    <!-- 7 PROOF (approved, with one gap) -->
    <section class="section proof-band" id="proof">
      <div class="wrap">
        <p class="kicker">Proof</p>
        <h2>{escape(PROOF)}</h2>
        <div class="proof-slot" data-placeholder>
          {badge("Placeholder, needs Dash's approval and the client's written consent")}
          <p>[One result or one quote from the first client goes here]</p>
        </div>{shots}
      </div>
    </section>

"""


def proof_soon(ind):
    return f"""    <!-- 7 PROOF: only the Private Equity and VC page has a live client (guidance) -->
    <section class="section proof-band" id="proof">
      <div class="wrap">
        <p class="kicker">Proof</p>
        <div class="draft-block" data-placeholder>
          {badge(B_NEEDS_APPROVAL)}
          <h2>Client results in {escape(ind["name"])} are coming soon.</h2>
          <p class="section-lede">{escape(PROOF)}</p>
        </div>
        <p><a class="btn btn-ghost" href="private-equity.html">See CraftArc in private equity</a></p>
      </div>
    </section>

"""


def industries():
    cards = []
    for ind in INDUSTRIES:
        st = ind["status"]
        orange = "orange" if ind["icon"] in ("hls", "ps") else ""
        subs = "".join(f"<li>{escape(n)}</li>" for _, n, _, _ in ind["subs"])
        cards.append(f'          <a class="card ind-card" href="{ind["slug"]}.html">{tile(ind["icon"], orange)}'
                     f'<span class="ind-status {st}">{STATUS_LABEL[st]}</span><h3>{escape(ind["name"])}</h3>'
                     f'<p>{escape(ind["card"])}</p><ul class="ind-subs">{subs}</ul><span class="ind-more">Read more</span></a>')
    return f"""    <!-- 8 INDUSTRIES (needs approval): proven in private equity first, then professional services, then all industries -->
    <section class="section industries" id="industries">
      <div class="wrap">
        <p class="kicker">Industries</p>
        <div class="draft-block" data-placeholder>
          {badge(B_NEEDS_APPROVAL + ": card copy")}
          <h2>Every organization needs its next leaders. We started in private equity.</h2>
        </div>
        <div class="card-grid">
{chr(10).join(cards)}
        </div>
      </div>
    </section>

"""


def start():
    steps = [
        ("search", "", "We assess where you are", "We look at your leadership levels and at how you review leaders today."),
        ("doc", "", "We write down the standard with you", "We help you write down what good looks like at each leadership level, in your own words."),
        ("gear", "", "We set CraftArc up around your organization", "We load your levels, your standard and your people, and set who sees what."),
        ("flag", "orange", "You run your next cycle", "Your leaders go through their first Review Cycle, and the agent does the legwork."),
    ]
    lis = "\n".join(f'          <li>{tile(i, c)}<h3>{escape(h)}</h3><p>{escape(p)}</p></li>' for i, c, h, p in steps)
    return f"""    <!-- 9 HOW YOU START (approved headline, draft steps from Dash's steer) -->
    <section class="section start" id="start">
      <div class="wrap">
        <p class="kicker">How you start</p>
        <h2>{escape(START_HEAD)}</h2>
        <div class="draft-block" data-placeholder>{badge(B_NEEDS_APPROVAL + ": the four steps")}</div>
        <ol class="start-steps">
{lis}
        </ol>
      </div>
    </section>

"""


def who():
    return f"""    <!-- 10 WHO IT IS FOR (approved line, draft lead-in) -->
    <section class="section who" id="who">
      <div class="wrap narrow">
        <p class="kicker">Who it is for</p>
        <div class="draft-block" data-placeholder>
          {badge(B_NEEDS_APPROVAL)}
          <h2>For CEOs who grow their next leaders on purpose</h2>
          <p class="who-text">CraftArc is for CEOs and leadership teams who want to know where every leader stands. It works when the leadership team commits to a Review Cycle every year, and to a development dialogue with each leader.</p>
        </div>
        <p class="who-line">{escape(WHO_LINE)}</p>
      </div>
    </section>

"""


FAQ = [
    ("Who decides where a leader stands?",
     "Your people do. The agent gathers the evidence and drafts the write-ups. The evaluation coordinator and your leadership team make every call."),
    ("Who sees the conversations?",
     "Your organization decides. Only the leader and their evaluation coordinator see a self-evaluation. Colleagues can give feedback anonymously, and the agent stores every transcript securely."),
    ("How do we introduce the agent so people do not feel watched?",
     "Introduce it as part of the Review Cycle, with a clear start and end. Each leader's first conversation is their own self-evaluation. Colleagues speak only about what they saw first-hand."),
    ("Will it fit our own roles and leadership levels?",
     "Yes. We help you write down the standard for each of your leadership levels, in your own words. CraftArc runs on that standard, with no code."),
    ("Why not build this with a general AI assistant?",
     "A general AI assistant answers one person at a time. CraftArc runs the whole Review Cycle for every leader, against one standard. It holds the conversations, grades the evidence and drafts the write-ups."),
    ("How much leadership time does it take?",
     "Each conversation with the agent takes about 25 minutes, by voice or text. The agent drafts the write-ups, so leaders give their time to the development dialogue."),
    ("What does it cost?",
     "We quote the fee after a short call about your organization and your leadership levels. Leaders and evaluation coordinators are unlimited, and colleagues who give feedback are never charged."),
]


def faq():
    items = "\n".join(f"        <details>\n          <summary>{escape(q)}</summary>\n          <p>{escape(a)}</p>\n        </details>" for q, a in FAQ)
    return f"""    <!-- 11 FAQ (questions from CEO testing, draft answers) -->
    <section class="section faq" id="faq">
      <div class="wrap narrow">
        <p class="kicker">FAQ</p>
        <h2>Questions CEOs ask us</h2>
        <div class="draft-block" data-placeholder>{badge(B_NEEDS_APPROVAL + ": the answers")}</div>
{items}
      </div>
    </section>

"""


def book_cta(href):
    return f"""    <!-- 12 BOOK A DEMO (needs approval): one button, repeated from the hero -->
    <section class="section book book-cta" id="book">
      <div class="wrap narrow">
        <p class="kicker">Book a demo</p>
        <div class="draft-block" data-placeholder>
          {badge(B_NEEDS_APPROVAL)}
          <h2>Bring the question your board keeps asking.</h2>
          <p class="section-lede">We will show you how CraftArc answers it.</p>
        </div>
        <a class="btn btn-primary btn-lg" href="{href}" data-cta="book">Book a demo</a>
      </div>
    </section>

"""


def subsectors(ind):
    cards = []
    for sid, name, st, text in ind["subs"]:
        text = text or f"CraftArc for leaders in {name}. This section is in development."
        label = STATUS_LABEL["live" if st == "live" else "soon"]
        cards.append(f'<article class="card sub-card" id="{sid}"><p class="ind-status {st}">{label}</p><h3>{escape(name)}</h3><p>{escape(text)}</p></article>')
    return f"""    <!-- SUB-SECTORS: menu targets -->
    <section class="section subsectors" id="sub-sectors">
      <div class="wrap">
        <p class="kicker">{escape(ind["name"])}</p>
        <div class="sub-grid">{"".join(cards)}</div>
      </div>
    </section>

"""


# ------------------------------------------------------------------ the lead form (Book a demo page only)
FORM = """        <form class="lead-form" id="lead-form" novalidate>
          <div class="field">
            <label for="name">Full name <span aria-hidden="true">*</span></label>
            <input id="name" name="name" type="text" autocomplete="name" required maxlength="120">
            <p class="err" id="name-err" hidden></p>
          </div>
          <div class="field">
            <label for="email">Work email <span aria-hidden="true">*</span></label>
            <input id="email" name="email" type="email" autocomplete="email" required maxlength="160">
            <p class="err" id="email-err" hidden></p>
          </div>
          <div class="field">
            <label for="firm">Organization <span aria-hidden="true">*</span></label>
            <input id="firm" name="firm" type="text" autocomplete="organization" required maxlength="160">
            <p class="err" id="firm-err" hidden></p>
          </div>
          <div class="field">
            <label for="role">Your role <span aria-hidden="true">*</span></label>
            <select id="role" name="role" required>
              <option value="">Choose one</option>
              <option value="managing_partner">CEO, managing partner or business head</option>
              <option value="coo">COO or chief of staff</option>
              <option value="partner_md">Senior leader</option>
              <option value="talent_hr">Head of talent or HR</option>
              <option value="other">Other</option>
            </select>
            <p class="err" id="role-err" hidden></p>
          </div>
          <div class="field">
            <label for="timing">When does your next review cycle start?</label>
            <select id="timing" name="timing">
              <option value="">Choose one</option>
              <option value="q1_2027">January to March 2027</option>
              <option value="q2_2027">April to June 2027</option>
              <option value="later">Later</option>
              <option value="unsure">Not sure</option>
            </select>
          </div>
          <details class="more" id="more">
            <summary>Tell us more (optional, helps us prepare)</summary>
            <div class="field-row">
              <div class="field">
                <label for="industry">Industry</label>
                <select id="industry" name="industry">
                  <option value="">Choose one</option>
""" + "".join(f'                  <option value="{i["value"]}">{escape(i["name"][0] + i["name"][1:].lower().replace("vc", "VC"))}</option>\n' for i in INDUSTRIES) + """                  <option value="other">Other</option>
                </select>
              </div>
              <div class="field">
                <label for="team">Leaders in scope</label>
                <select id="team" name="team">
                  <option value="">Choose one</option>
                  <option value="lt10">Under 10</option>
                  <option value="10to25">10 to 25</option>
                  <option value="26to50">26 to 50</option>
                  <option value="gt50">Over 50</option>
                </select>
              </div>
            </div>
            <div class="field" id="aum-field" hidden>
              <label for="aum">Assets under management</label>
              <select id="aum" name="aum">
                <option value="">Choose one</option>
                <option value="lt1b">Under $1B</option>
                <option value="1to2b">$1B to $2B</option>
                <option value="2to5b">$2B to $5B</option>
                <option value="5to10b">$5B to $10B</option>
                <option value="gt10b">Over $10B</option>
              </select>
            </div>
            <div class="field">
              <label for="framework">Have you written down what good looks like at each leadership level?</label>
              <select id="framework" name="framework">
                <option value="">Choose one</option>
                <option value="yes">Yes</option>
                <option value="draft">In draft</option>
                <option value="no">Not yet</option>
              </select>
            </div>
            <div class="field">
              <label for="message">Anything we should know?</label>
              <textarea id="message" name="message" rows="3" maxlength="2000"></textarea>
            </div>
          </details>
          <div class="hp" aria-hidden="true">
            <label for="company_website">Leave this field empty</label>
            <input id="company_website" name="company_website" type="text" tabindex="-1" autocomplete="off">
          </div>
          <div class="field check">
            <input id="consent" name="consent" type="checkbox" required>
            <label for="consent">I agree that CraftArc may use these details to reply to this request. <a href="#privacy">Privacy</a></label>
            <p class="err" id="consent-err" hidden></p>
          </div>
          <button class="btn btn-primary btn-block" type="submit" id="submit">Request my demo</button>
          <p class="form-status" id="form-status" role="status" aria-live="polite"></p>
        </form>

        <div class="thanks" id="thanks" hidden tabindex="-1">
          <h3>Thank you. Your request is in.</h3>
          <p id="thanks-msg">We will email you to arrange a time. If you have written down what good looks like at each leadership level, have it to hand.</p>
        </div>
"""

# ------------------------------------------------------------------ pages

DESC_HOME = ("Can you tell how close each leader is to their next role? CraftArc can. "
             "Know where every leader stands, without blocking days of leadership time.")


def home():
    main = (home_hero() + claims(HOME_TOKENS) + problem() + method() + solution(HOME_TOKENS)
            + how(HOME_VIDEO) + proof_live() + industries() + start() + who() + faq() + book_cta("book-a-demo.html"))
    return page("CraftArc | Know where every leader stands", DESC_HOME, "", main, viewer=True)


def industry(ind):
    crumbs = f'<a href="index.html">CraftArc</a> <span aria-hidden="true">/</span> Industries <span aria-hidden="true">/</span> {escape(ind["name"])}'
    href = f'book-a-demo.html?industry={ind["value"]}'
    live = ind["status"] == "live"
    main = (hero(ind["q"], ind["a"], href, crumbs, ind["name"], draft=True) + subsectors(ind) + claims(ind) + solution(ind)
            + (how(PE_VIDEO) if live else "") + (proof_live(gallery=True) if live else proof_soon(ind)) + book_cta(href))
    desc = f'{ind["q"]} CraftArc can, without blocking days of leadership time.'
    return page(f'CraftArc | {ind["name"]}', desc, ind["slug"], main, viewer=live)


def about():
    main = f"""    <section class="hero page-hero" id="top">
      <div class="wrap">
        <p class="crumbs"><a href="index.html">CraftArc</a> <span aria-hidden="true">/</span> About</p>
        <p class="eyebrow">About CraftArc</p>
        <h1>We help CEOs grow their next leaders on purpose.</h1>
        <p class="draft-note" data-placeholder>{badge(B_NEEDS_APPROVAL + ": page headline")}</p>
      </div>
    </section>

    <section class="section about" id="pitch">
      <div class="wrap about-grid">
        <div class="pitch" data-placeholder>
          {badge("Placeholder: the elevator pitch from Approved Copy, section 1, goes here word for word")}
          <p class="pitch-text">{escape(HERO_A)} {escape(METHOD[1])}</p>
          <p class="pitch-note">Stand-in built only from approved lines in the website guidance.</p>
        </div>
        <aside class="box founder" id="founder" data-placeholder>
          {tile("person")}
          <div>
            {badge("Placeholder: founder note, Dash to write")}
            <h2>From the founder</h2>
            <p>I worked at McKinsey, Microsoft and Siemens, and I founded AgenticPM, which builds AI agents for private markets. I modeled CraftArc on how the best management consulting firms develop and select their leaders.</p>
            <p class="box-sign">Bibhudatta "Dash"</p>
          </div>
        </aside>
      </div>
      <div class="wrap">
        <p class="about-proof">{escape(PROOF)}</p>
      </div>
    </section>

""" + book_cta("book-a-demo.html")
    return page("CraftArc | About", "CraftArc helps CEOs know where every leader stands, and keep every one of them growing toward their next role.",
                "", main)


def book_page():
    main = f"""    <section class="hero page-hero book-page" id="book">
      <div class="wrap book-grid">
        <div class="book-copy">
          <p class="crumbs"><a href="index.html">CraftArc</a> <span aria-hidden="true">/</span> Book a demo</p>
          <h1>Book a demo</h1>
          <div class="draft-block" data-placeholder>
            {badge(B_NEEDS_APPROVAL + ": the line and the form fields")}
            <p class="lede">Tell us who you are, and we will email you to arrange a time.</p>
          </div>
          <p class="hero-time">{tile("time")}<span>{escape(HERO_TIME)}</span></p>
        </div>
{FORM}      </div>
    </section>

"""
    return page("CraftArc | Book a demo", "Book a demo of CraftArc. Know where every leader stands, without blocking days of leadership time.",
                "", main)


def build():
    pages = {"index.html": home(), "about.html": about(), "book-a-demo.html": book_page()}
    for ind in INDUSTRIES:
        pages[f'{ind["slug"]}.html'] = industry(ind)
    return pages


def main():
    pages = build()
    if "--check" in sys.argv:
        stale = [n for n, html in pages.items() if not (SITE / n).exists() or (SITE / n).read_text() != html]
        print("build_site: pages match the source" if not stale else f"build_site: these pages differ from tools/build_site.py: {', '.join(stale)}")
        sys.exit(1 if stale else 0)
    for n, html in pages.items():
        (SITE / n).write_text(html)
    print(f"build_site: wrote {len(pages)} pages: {', '.join(pages)}")


if __name__ == "__main__":
    main()
