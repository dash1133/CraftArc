"""Rebuild the homepage's main content from Dash's content v5 (22 Nov 2026).

Keeps the existing head, header (Industries menu), lead form, footer and viewer, and
replaces the story sections. Copy follows CLAUDE.md item 2 (American spelling, ASD-STE100
limits, one term per concept). Run once:  python3 tools/build_home_v5.py
After this, edit website/index.html directly.
"""
import re
from pathlib import Path

W = Path(__file__).resolve().parents[1] / "website"
page = (W / "index.html").read_text()

ICON = {
    "mic": '<rect x="9" y="2.5" width="6" height="11.5" rx="3"/><path d="M5.5 12a6.5 6.5 0 0 0 13 0"/><path d="M12 18.5v3M8.5 21.5h7"/>',
    "person_gear": '<circle cx="9" cy="7" r="4"/><path d="M2.5 21a7 7 0 0 1 9.5-6.5"/><circle cx="17.5" cy="17.5" r="2.6"/><path d="M17.5 13.2v1.5M17.5 20.3v1.5M13.2 17.5h1.5M20.3 17.5h1.5M14.5 14.5l1 1M19.5 19.5l1 1M14.5 20.5l1-1M19.5 15.5l1-1"/>',
    "people": '<circle cx="9" cy="7" r="4"/><path d="M2 21a7 7 0 0 1 14 0"/><path d="M15 3.3a4 4 0 0 1 0 7.4M18 14.2A7 7 0 0 1 22 21"/>',
    "document": '<path d="M6 2.5h8l5 5v14H6z"/><path d="M14 2.5v5h5M9 12h7M9 16h7"/>',
    "checklist": '<rect x="3" y="3.5" width="6" height="6" rx="1.2"/><path d="M12.5 6.5H21M12.5 12H21M3.5 17l2 2 3.5-3.5M12.5 18H21"/>',
    "chart": '<path d="M3 20h18"/><path d="M5 16l4.5-5 3.5 3 6-7"/><path d="M15 7h4v4"/>',
    "chat": '<path d="M4 5h11a2 2 0 0 1 2 2v6a2 2 0 0 1-2 2H9l-4 3v-3H4a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2z"/><path d="M17 9h3a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-1v3l-3-3h-4"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5"/>',
    "spark": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 16l.8 2.2L22 19l-2.2.8L19 22l-.8-2.2L16 19l2.2-.8z"/>',
    "scale": '<path d="M12 3v18M5 21h14"/><path d="M5 7h14"/><path d="M5 7l-3 7a3 3 0 0 0 6 0zM19 7l-3 7a3 3 0 0 0 6 0z"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
    "gauge": '<path d="M4 18a8 8 0 1 1 16 0"/><path d="M12 18l4-6"/><circle cx="12" cy="18" r="1.4"/>',
    "search": '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/>',
    "gear": '<circle cx="12" cy="12" r="3"/><path d="M12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3M5.3 5.3l2.1 2.1M16.6 16.6l2.1 2.1M5.3 18.7l2.1-2.1M16.6 7.4l2.1-2.1"/>',
    "flag": '<path d="M5 21V4"/><path d="M5 4h11l-2 4 2 4H5"/>',
    "play": '<circle cx="12" cy="12" r="9"/><path d="M10 8.5v7l6-3.5z"/>',
    "route": '<path d="M4 19a8 8 0 0 1 16 0" stroke-dasharray="2.5 3"/><circle cx="4" cy="19" r="1.8"/><circle cx="20" cy="19" r="1.8"/><path d="M12 3v6M9 6l3 3 3-3"/>',
    "calendar": '<rect x="3" y="4.5" width="18" height="16" rx="2.5"/><path d="M3 9.5h18M8 2.5v4M16 2.5v4"/><path d="M8 14h3"/>',
    "exit": '<path d="M14 3H6a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h8"/><path d="M11 12h10M17 8l4 4-4 4"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "bank": '<path d="M3 9.5L12 4l9 5.5"/><path d="M5 10v8M9.5 10v8M14.5 10v8M19 10v8"/><path d="M3 20.5h18"/>',
    "health": '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/><path d="M12 9.5v5M9.5 12h5"/>',
    "chip": '<rect x="6" y="6" width="12" height="12" rx="2"/><rect x="9.5" y="9.5" width="5" height="5" rx="1"/><path d="M9 3v3M15 3v3M9 18v3M15 18v3M3 9h3M3 15h3M18 9h3M18 15h3"/>',
    "factory": '<path d="M3 20.5V10l5 3V10l5 3V10l5 3V5h3v15.5z"/><path d="M7 17h2M11 17h2M15 17h2"/>',
    "briefcase": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a1.5 1.5 0 0 1 1.5-1.5h3A1.5 1.5 0 0 1 15 5v2"/><path d="M3 12.5h18"/>',
}


def tile(name, cls=""):
    return f'<span class="tile{(" " + cls) if cls else ""}" aria-hidden="true"><svg viewBox="0 0 24 24" focusable="false">{ICON[name]}</svg></span>'


def svg(name):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">{ICON[name]}</svg>'


GALLUP_70 = "https://www.gallup.com/workplace/236570/managers-account-70-variance-employee-engagement.aspx"
GALLUP_82 = "https://www.gallup.com/workplace/231593/state-american-manager-report.aspx"

promises = [
    ("chart", "", "Know where each leader stands", "See where every leader stands against what their role and their next role demand, all in one view. Trace each one's arc from cycle to cycle."),
    ("chat", "", "Have the conversation that matters", "Walk into each development dialogue with first-hand evidence from the people who work with them, already gathered and drafted."),
    ("target", "orange", "Keep every leader on track", "A coach helps each leader turn feedback into a few clear goals and keep them in view. Development does not get lost in the shuffle."),
]
cycle = [
    ("mic", "Self-evaluation", "Each leader reflects on their work with the coach, by voice or text, in about 25 minutes."),
    ("people", "Feedback", "The agent interviews the colleagues who saw the work first-hand, and gathers what they saw in one place."),
    ("chat", "Development dialogue", "You and each leader sit down with a drafted write-up and talk about what will make them better."),
    ("checklist", "Development plan", "Each leader names a few goals, and the coach helps them keep those goals in view."),
]
changed = [
    "Colleagues give feedback in an anonymous conversation with the agent, by voice or text, instead of filling in a form.",
    "Every piece of feedback is first-hand, graded by source and mapped to the firm's own framework.",
    "Evaluation coordinators get a drafted write-up for each leader and walk into the development dialogue prepared.",
    "The firm started with its senior investment team and plans to extend CraftArc across the firm.",
]
convs = [
    ("mic", "Self-evaluation", "The agent talks with each person for their self-evaluation, by voice or text, in about 25 minutes, and asks for whatever is missing.", "To get started, what have you worked on over the period?"),
    ("person_gear", "Design the feedback", "It helps the evaluation coordinator choose who should speak to each competency, and flags the gaps before the survey goes out.", "Nobody who saw the client launch is on the list yet. Shall we add someone who did?"),
    ("people", "Contributor interviews", "It speaks with each contributor and gathers what they saw first-hand in one place, graded by source.", "Tell me about a decision you saw Sam make on the launch. What did you see first-hand?"),
    ("document", "Prepare the dialogue", "It drafts the memo for your leadership team, a note to the person and a scorecard. The evaluation coordinator walks into the development dialogue prepared and owns the final wording.", "I'm drafting the review documents now. I'll let you know as each one is ready."),
    ("checklist", "Development plan", "It helps each person turn the dialogue into a few goals of their own, and keep them in view between review cycles.", "Which of these goals would you like to start with?"),
]
why = [
    ("document", "", "Your craft, framed with experts", "We bring the expertise to frame your competency model with you, so what great looks like is finally written down."),
    ("spark", "", "No administrative burden", "An AI agent holds the conversations, gathers the feedback in one place and drafts the write-ups. Nobody chases surveys or collates comments."),
    ("scale", "", "A fair read on every leader", "Every view rests on what people saw first-hand, graded by source, so you can explain each decision about a leader."),
    ("clock", "orange", "Leaders' time back", "Your senior leaders spend their time developing people instead of chasing feedback."),
]
industries = [
    ("private-equity.html", "Private Markets", "chart", "", "", ["Private Equity", "Venture Capital", "Investment Banks"],
     "Grow your next partners. CraftArc runs development for the senior investment team at Brightstar Capital Partners."),
    ("financial-services.html", "Financial Services", "bank", "", "Coming soon", ["Banking & Capital Markets", "Asset & Investment Management", "Insurance"], ""),
    ("healthcare-life-sciences.html", "Healthcare & Life Sciences", "health", "orange", "Coming soon", ["Health Systems & Providers", "Pharma & Biotech", "MedTech"], ""),
    ("technology.html", "Technology", "chip", "", "Coming soon", ["Software & SaaS", "IT Services", "Telecom"], ""),
    ("manufacturing-industrial.html", "Manufacturing & Industrial", "factory", "", "Coming soon", ["Industrial Manufacturing", "Energy & Utilities", "Automotive"], ""),
    ("professional-services.html", "Professional Services", "briefcase", "orange", "Coming soon", ["Consulting", "Law", "Accounting"], ""),
]
start = [
    ("search", "We assess where you are", "We look at how you develop leaders today: your roles, your framework if you have one, and how your reviews run."),
    ("document", "We write down your craft with you", "We frame your competency model with you, role by role, in plain English."),
    ("gear", "We set up CraftArc", "We load your roles, competencies and steps, and set who sees what."),
    ("flag", "You run your next cycle", "Your senior leaders go first, so the disruption stays low. Then you extend it to more leaders."),
]
faq = [
    ("Who decides where someone sits on each competency?", "Your evaluation coordinator does. The interviews gather graded facts, and the coordinator forms the view with the agent, which maps each example to the competencies in your framework."),
    ("Who sees the conversations?", "Your organization decides. Only the person and their evaluation coordinator see a self-evaluation. Contributor interviews can be anonymous, and transcripts are stored securely."),
    ("How do we introduce the agent so people do not feel watched?", "Introduce it as a coach. Each person's first conversation is their own self-evaluation. Contributors speak only about what they saw first-hand, and the coach never nags."),
    ("We use our own roles, competencies and steps. Will it fit?", "Everything specific to your organization is written in plain English, including roles, competencies and steps, so CraftArc adapts to it without code."),
    ("Why not build this with a general AI assistant?", "CraftArc holds your framework in plain English, and it gives every role one home and five tracked steps. It grades every fact by source and checks coverage before the survey goes out. Brightstar tried the do-it-yourself route first, and then chose CraftArc."),
    ("How long is each conversation?", "Each conversation with the coach takes about 25 minutes, by voice or text. Leaders who coordinate reviews or give contributor interviews will have more than one."),
    ("Will it disrupt the review process we already run?", "You start with your senior leaders only, which keeps the disruption low. When it is working, you extend it to more leaders."),
    ("What does it cost?", "Participants and evaluation coordinators are unlimited, and contributors are never charged. We quote the fee after a short call about your team and your framework."),
]

arc_svg = '''<svg class="arc-art" viewBox="0 0 400 260" role="img" aria-label="An arc of competencies, each marked with a question mark, from the craft to the arc">
            <defs><linearGradient id="arcgrad" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#245de5"/><stop offset="0.5" stop-color="#7c5cff"/><stop offset="1" stop-color="#f58220"/></linearGradient></defs>
            <path d="M30 210 A 170 170 0 0 1 370 210" fill="none" stroke="url(#arcgrad)" stroke-width="4" stroke-dasharray="7 9" stroke-linecap="round"/>
            <g class="q"><circle cx="30" cy="210" r="17"/><text x="30" y="216">?</text></g>
            <g class="q"><circle cx="71" cy="105" r="17"/><text x="71" y="111">?</text></g>
            <g class="q"><circle cx="146" cy="49" r="17"/><text x="146" y="55">?</text></g>
            <g class="q"><circle cx="254" cy="49" r="17"/><text x="254" y="55">?</text></g>
            <g class="q"><circle cx="329" cy="105" r="17"/><text x="329" y="111">?</text></g>
            <g class="q"><circle cx="370" cy="210" r="17"/><text x="370" y="216">?</text></g>
            <text class="lab" x="30" y="252">THE CRAFT</text>
            <text class="lab" x="370" y="252">THE ARC</text>
          </svg>'''

main = f'''  <main id="main">
    <!-- HERO -->
    <section class="hero hero-v5" id="top">
      <div class="wrap hv5-grid">
        <div class="hv5-copy">
          <p class="eyebrow">Agentic leadership development</p>
          <h1>Know where every leader stands, and keep every one of them growing.</h1>
          <p class="lede">CraftArc gives you a clear read on each of your leaders, a better conversation about their growth, and a plan each one stays focused on. An AI agent does the legwork, so your leaders spend their time on the people.</p>
          <div class="cta-row">
            <a class="btn btn-primary" href="#book" data-cta="hero">Book a demo</a>
            <a class="btn btn-ghost" href="#case" data-cta="case">See the Brightstar story</a>
          </div>
          <p class="proofline">Live today at Brightstar Capital Partners. Modeled on how the best management consulting firms develop and select their leaders.</p>
          <p class="timeline-note">{svg("clock")}<span>Ready for your next review cycle in six to eight weeks.</span></p>
        </div>
        <ol class="promise-stack">{"".join(f"""
          <li class="promise-card">{tile(ic, cls)}<div><h3>{t}</h3><p>{body}</p></div></li>""" for ic, cls, t, body in promises)}
        </ol>
      </div>
    </section>

    <!-- EACH CYCLE -->
    <section class="section cycle" id="cycle">
      <div class="wrap">
        <p class="kicker">Each cycle</p>
        <h2>From self-evaluation to a plan each leader owns</h2>
        <ol class="cycle-blocks">{"".join(f"""
          <li class="cycle-block"><span class="cycle-num">{i}</span>{tile(ic, "orange" if i == 4 else "")}<h3>{t}</h3><p>{body}</p></li>""" for i, (ic, t, body) in enumerate(cycle, 1))}
        </ol>
      </div>
    </section>

    <!-- CASE STUDY -->
    <section class="section case" id="case">
      <div class="wrap">
        <p class="kicker">Case study</p>
        <h2>How Brightstar Capital Partners grows its next partners</h2>
        <div class="case-grid">
          <div class="case-story">
            <p class="case-firm">{tile("chart")}<span><strong>Brightstar Capital Partners</strong><small>Private equity</small></span></p>
            <p class="case-lede">Brightstar Capital Partners, a private equity firm, runs development for its managing directors and partners on CraftArc. We built it with the firm's COO, who designed its competency framework.</p>
            <p>Brightstar had written down what it takes to lead at the firm, role by role. It tried a do-it-yourself AI assistant first, then signed a 24-month license for CraftArc. Eight to ten client interviews shaped how each competency is weighted and probed.</p>
            <div class="case-slot" data-placeholder><span class="ph-badge">Placeholder, replace before launch</span><p>[Result or quote from Brightstar goes here]</p></div>
          </div>
          <div class="case-changes">
            <h3>What has changed</h3>
            <ul class="check-list">{"".join(f"<li>{c}</li>" for c in changed)}</ul>
            <figure class="shot-wrap case-shot"><button class="zoom shot" type="button" data-full="assets/img/06_performance_review.webp" data-alt="A memo drafted by the CraftArc agent, sample data" aria-label="Enlarge: a memo drafted by the CraftArc agent"><picture><source srcset="assets/img/proof_writeup.webp" type="image/webp"><img width="885" height="440" src="assets/img/proof_writeup.png" alt="A memo drafted by the agent, opening with the question the evidence could not answer" loading="lazy"></picture><span class="hint" aria-hidden="true">Enlarge</span></button><figcaption class="shot-cap">A drafted memo, in the product. Sample data, not Brightstar's.</figcaption></figure>
          </div>
        </div>
      </div>
    </section>

    <!-- INTRODUCING CRAFTARC -->
    <section class="section intro-v5" id="craftarc">
      <div class="wrap">
        <p class="kicker">Introducing CraftArc</p>
        <h2>One platform that holds your craft, and one agent that runs the cycle</h2>
        <div class="intro-grid">
          <div>
            <p class="intro-text">CraftArc holds your competency framework in plain English, and its agent holds every conversation in the cycle. You see each leader's progress in one place, and you own every word that reaches them.</p>
            <ul class="chip-list">
              <li>{tile("mic")}<span><strong>Self-evaluation</strong><small>About 25 minutes, by voice or text</small></span></li>
              <li>{tile("people")}<span><strong>Gap flagged</strong><small>Before the feedback survey goes out</small></span></li>
              <li>{tile("document", "orange")}<span><strong>Write-up drafted</strong><small>Your evaluation coordinator owns the final wording</small></span></li>
            </ul>
          </div>
          <figure class="video-card video-placeholder" id="video" data-placeholder>
            <div class="vp-stage">
              {tile("play", "big")}
              <p class="vp-title">Overview video coming soon</p>
              <p class="vp-sub">A short film on how CraftArc works in any organization.</p>
              <a class="btn btn-ghost btn-sm" href="private-equity.html#video" data-cta="pe-video">Watch the private equity video</a>
            </div>
            <figcaption><span class="ph-badge">Placeholder, replace before launch</span></figcaption>
          </figure>
        </div>
      </div>
    </section>

    <!-- HOW IT WORKS -->
    <section class="section how" id="how">
      <div class="wrap">
        <p class="kicker">How it works</p>
        <h2>Inside each cycle: five conversations, one arc</h2>
        <p class="section-lede">The agent holds every conversation behind the four blocks above. The agent lines below are sample dialogue.</p>
        <ol class="arc-row" aria-hidden="true">{"".join(f'<li style="--i:{i}"><span class="tile big">{svg(ic)}</span><span class="tile-label">{t}</span></li>' for i, (ic, t, _, _) in enumerate(convs))}</ol>
        <div class="conv-grid">{"".join(f"""
          <article class="conv-card" id="conv-{i}">
            <div class="conv-head">{tile(ic, "orange" if i == 5 else "")}<div><p class="step-num">Conversation {i}</p><h3>{t}</h3></div></div>
            <p>{body}</p>
            <div class="agent-line"><span class="agent-avatar" aria-hidden="true"><img src="assets/img/logo-mark.svg" alt="" width="28" height="28"></span><p><span class="agent-name">CraftArc Agent</span>{line}</p></div>
          </article>""" for i, (ic, t, body, line) in enumerate(convs, 1))}
        </div>
        <p class="how-more"><a class="btn btn-ghost" href="private-equity.html#how">See every screen in the private equity walkthrough</a></p>
      </div>
    </section>

    <!-- WHY IT WORKS -->
    <section class="section why" id="why">
      <div class="wrap">
        <p class="kicker">Why it works</p>
        <h2>Your leaders grow leaders. The agent does the rest.</h2>
        <ol class="why-list">{"".join(f"<li>{tile(ic, cls)}<div><h3>{t}</h3><p>{body}</p></div></li>" for ic, cls, t, body in why)}</ol>
      </div>
    </section>

    <!-- WHY IT MATTERS -->
    <section class="section evidence" id="evidence">
      <div class="wrap">
        <p class="kicker">Why it matters</p>
        <h2>What separates great organizations from the rest? It is how they grow their next set of leaders.</h2>
        <div class="stat-grid">
          <article class="stat">
            <div class="stat-head">{tile("people")}<p class="stat-big">At least 70%</p></div>
            <p>Gallup estimates that managers account for at least 70% of the variance in employee engagement across business units.</p>
            <p class="source">Gallup, State of the American Manager, 2015. <a href="{GALLUP_70}" rel="noopener" target="_blank">Read the Gallup summary</a>.</p>
          </article>
          <article class="stat">
            <div class="stat-head">{tile("gauge", "orange")}<p class="stat-big">82%</p></div>
            <p>Gallup finds that companies fail to choose the candidate with the right talent for a manager role 82% of the time.</p>
            <p class="source">Gallup, State of the American Manager, 2015. <a href="{GALLUP_82}" rel="noopener" target="_blank">Read the Gallup report page</a>.</p>
          </article>
        </div>
        <div class="matters-grid">
          <ul class="problem-points">
            <li>{tile("document")}<span>Most organizations have never written down their craft: what it takes to lead in their business, competency by competency.</span></li>
            <li>{tile("calendar")}<span>So the craft stays in a few heads, and feedback arrives once a year, too late to use.</span></li>
            <li>{tile("exit", "orange")}<span>When those leaders retire or move on, the craft leaves with them.</span></li>
          </ul>
          {arc_svg}
        </div>
      </div>
    </section>

    <!-- INDUSTRIES -->
    <section class="section industries" id="industries">
      <div class="wrap">
        <p class="kicker">Industries</p>
        <h2>For organizations whose leaders carry the craft</h2>
        <div class="card-grid">{"".join(f"""
          <a class="card ind-card" href="{href}">{tile(ic, cls)}{f'<span class="ind-status">{status}</span>' if status else ''}<h3>{name}</h3>{f'<p>{desc}</p>' if desc else ''}<ul class="ind-subs">{"".join(f"<li>{s}</li>" for s in subs)}</ul><span class="ind-more">Read more</span></a>""" for href, name, ic, cls, status, subs, desc in industries)}
        </div>
      </div>
    </section>

    <!-- HOW ORGANIZATIONS START. Approved extra offer lines come from config.js (extraOfferItems). -->
    <section class="section start" id="start">
      <div class="wrap">
        <p class="kicker">How organizations start</p>
        <h2>Ready for your next cycle in six to eight weeks</h2>
        <p class="section-lede">We come in, work alongside your team, and hand you a cycle that is ready to run.</p>
        <ol class="start-steps">{"".join(f"""
          <li>{tile(ic, "orange" if i == 4 else "")}<p class="step-num">Step {i}</p><h3>{t}</h3><p>{body}</p></li>""" for i, (ic, t, body) in enumerate(start, 1))}
        </ol>
        <div class="start-grid" id="offer">
          <div>
            <h3>What you get</h3>
            <ul class="stack" id="offer-stack">
              <li>The CraftArc platform, running on your framework, roles and steps.</li>
              <li>An AI coach for self-evaluations and contributor interviews, by voice or text.</li>
              <li>Draft write-ups for every person, owned by your evaluation coordinator.</li>
              <li>Participants and evaluation coordinators are unlimited, so you can extend CraftArc from your senior leaders to every manager. Contributors are never charged.</li>
            </ul>
            <a class="btn btn-primary" href="#book" data-cta="offer">Book a demo</a>
          </div>
          <div class="start-boxes">
            <article class="box">{tile("user")}<div><h3>From the founder</h3><p>I worked at McKinsey, Microsoft and Siemens, and I founded AgenticPM, which builds AI agents for private markets. I modeled CraftArc on how the best management consulting firms develop and select their leaders.</p><p class="box-sign">Bibhudatta "Dash"</p></div></article>
            <article class="box">{tile("exit", "orange")}<div><h3 id="guarantee-title">Our commitment</h3><p>If we miss a stage we agreed to deliver and do not fix it, you can leave, and we refund your prepaid fees pro rata.</p></div></article>
            <article class="box">{tile("people")}<div><h3>Who it is for</h3><p>It is for organizations whose leaders want to build their next set of leaders. It is also for leadership teams that need a clear, fair read on the people they rely on. It works best when leadership commits to running the cycle. If that commitment is not there yet, we will say so.</p></div></article>
          </div>
        </div>
      </div>
    </section>

    <!-- FAQ -->
    <section class="section faq" id="faq">
      <div class="wrap narrow">
        <p class="kicker">FAQ</p>
        <h2>Questions leaders ask us</h2>{"".join(f"""
        <details>
          <summary>{q}</summary>
          <p>{a}</p>
        </details>""" for q, a in faq)}
      </div>
    </section>

'''

start_i = page.index("  <main id=\"main\">")
book_i = page.index("    <!-- CALL TO ACTION AND LEAD FORM -->")
page = page[:start_i] + main + page[book_i:]

# book copy (v5)
old_book = re.search(r'          <p>If your next review cycle starts in the new year, this is the quarter to plan it\..*?</p>', page).group(0)
page = page.replace(old_book, "          <p>If your next review cycle starts in the new year, this is the quarter to plan it. If you need a clear read on your leaders sooner, tell us and we will talk through how to start. Bring your competency framework, and we will show you how it would run on CraftArc.</p>")

# head
page = re.sub(r"<title>[^<]*</title>", "<title>CraftArc | Know where every leader stands</title>", page, count=1)
page = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Know where every leader stands, and keep every one of them growing. CraftArc\'s AI agent runs the cycle. Live today at Brightstar Capital Partners.">', page, count=1)
page = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="CraftArc | Know where every leader stands">', page, count=1)
page = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="A clear read on each of your leaders, a better conversation about their growth, and a plan each one stays focused on.">', page, count=1)
(W / "index.html").write_text(page)
print("homepage rebuilt from content v5")
