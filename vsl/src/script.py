"""CraftArc VSL: the single source of truth for words and pictures.

Every sentence has:
  cap   the caption text (written English, British spelling, no dashes)
  say   what the voice reads (spelled for pronunciation; defaults to cap)
  claim the claims-ledger ID(s) the sentence rests on (docs/Claims_Ledger.md)
plus the visual for that sentence. Scenes follow the Hormozi VSL order
captured in the CraftArc VSL Fact Set: hook, epiphany, pain, solution,
demo, proof, offer, risk reversal, urgency, call to action.

Screen coordinates are pixels in vsl/assets/screens/clean/*.png.
"""

STEPS = ["Launch", "Self-review", "Contributors", "Feedback", "Development plan"]

SCENES = [
    # ------------------------------------------------------------------ 1 HOOK
    {
        "id": "hook", "kind": "kinetic", "label": "Hook",
        "sentences": [
            {"cap": "If you are building your firm's next partners, here is how to review them on evidence.",
             "claim": ["N01", "L11"], "kicker": "For private equity leaders", "big": "Build your next partners on evidence.", "small": ""},
            {"cap": "One private equity firm spent 60 to 100 hours of senior time trying to make a general AI assistant run its reviews.",
             "claim": ["L01"], "kicker": "One private equity firm spent", "big": "60 to 100 hours", "accent": True,
             "small": "of senior time trying to make a general AI assistant run its leadership reviews"},
            {"cap": "Then it gave up. Here is what it did instead.", "claim": ["L01"], "big": "Then it gave up.",
             "small": "Here is what it did instead."},
        ],
    },
    # ------------------------------------------------------------- 2 EPIPHANY
    {
        "id": "epiphany", "kind": "doc", "label": "The story",
        "sentences": [
            {"cap": "The firm had done the hard part.", "claim": ["L02"], "doc_state": "blank"},
            {"cap": "Its COO had written down, on one page, what a great senior deal professional does.",
             "say": "Its C.O.O. had written down, on one page, what a great senior deal professional does.",
             "claim": ["L02"], "doc_state": "page"},
            {"cap": "But a framework on paper cannot interview anyone, gather evidence or write a review.",
             "claim": ["L03"], "doc_state": "gaps"},
        ],
    },
    # ----------------------------------------------------------------- 3 PAIN
    {
        "id": "pain", "kind": "kinetic", "label": "Two questions",
        "sentences": [
            {"cap": "Ask yourself. Do your principals know where they stand on each competency today?",
             "claim": ["N02"], "kicker": "Ask yourself", "big": "Do your principals know where they stand on each competency?", "small": ""},
            {"cap": "And could you show the evidence behind your next partner-readiness call?",
             "claim": ["N02"], "kicker": "Ask yourself", "big": "Could you show the evidence behind your next partner-readiness call?", "small": ""},
        ],
    },
    # -------------------------------------------------------------- 4 INSIGHT
    {
        "id": "insight", "kind": "logo", "label": "The insight",
        "sentences": [
            {"cap": "We believe your framework is the asset.", "claim": ["N03"], "kicker": "We believe", "big": "Your framework is the asset.", "small": ""},
            {"cap": "It needs a system that interviews your people, gathers the evidence and drafts the write-up.",
             "claim": ["N03"], "big": "It needs a system that runs it.",
             "small": "It interviews your people, gathers the evidence and drafts the write-up."},
            {"cap": "That is why we built CraftArc.", "say": "That is why we built Craft Arc.", "claim": ["N03"], "big": "", "small": "", "logo": True},
            {"cap": "CraftArc runs your review cycle on your own competency framework, written in plain English.",
             "say": "Craft Arc runs your review cycle on your own competency framework, written in plain English.",
             "claim": ["L05"], "big": "It runs on your own framework.", "small": "Your roles, competencies and steps, written in plain English."},
        ],
    },
    # ----------------------------------------------------------------- 5 DEMO
    {
        "id": "self", "kind": "screen", "label": "Self-review with an AI coach", "step": 1,
        "sentences": [
            {"cap": "In the self-review, an AI coach interviews each person against your competencies.",
             "claim": ["L08"], "img": "03_my_reviews.png", "focus": (20, 100, 1900, 560), "hl": [(1205, 425, 1295, 520)],
             "chip": "Self-review: your turn"},
            {"cap": "People can talk to the agent by voice or text, and in the self-review the coach asks for whatever is missing.",
             "claim": ["L08", "L09"], "img": "04_survey_roster.png", "focus": (0, 420, 545, 870), "hl": [(372, 742, 534, 822)],
             "chip": "Voice or text"},
        ],
    },
    {
        "id": "contrib", "kind": "screen", "label": "Contributor interviews", "step": 2,
        "sentences": [
            {"cap": "Colleagues who worked with each person then give AI-led interviews about what they saw first-hand.",
             "claim": ["L10"], "img": "04_survey_roster.png", "focus": (548, 250, 1919, 862), "pad": 0, "hl": [(563, 705, 1882, 862)],
             "chip": "Every contributor, tracked"},
            {"cap": "The agent grades every fact as directly observed, hearsay or third party.",
             "claim": ["L11"], "img": "04_survey_roster.png", "focus": (548, 250, 1919, 862), "pad": 0, "hl": [],
             "overlay": "grades"},
        ],
    },
    {
        "id": "coverage", "kind": "screen", "label": "Coverage, checked", "step": 2,
        "sentences": [
            {"cap": "The agent checks coverage for every competency and flags the gaps before you complete the survey.",
             "claim": ["L12"], "img": "05_survey_coverage.png", "focus": (548, 170, 1919, 782), "pad": 0, "hl": [(563, 300, 1888, 362)],
             "chip": "Coverage by competency"},
            {"cap": "Here, it warns that nobody who saw the banker meetings has been heard on sourcing.",
             "claim": ["L12"], "img": "05_survey_coverage.png", "focus": (1080, 300, 1900, 690), "hl": [(1614, 368, 1886, 540)],
             "chip": "Gap flagged before close"},
        ],
    },
    {
        "id": "writeup", "kind": "screen", "label": "Coordinator feedback", "step": 3,
        "sentences": [
            {"cap": "Then it drafts the Executive Committee writeup, the note to the person and the scorecard.",
             "say": "Then it drafts the Executive Committee write-up, the note to the person, and the scorecard.",
             "claim": ["L13"], "img": "06_performance_review.png", "focus": (0, 100, 1900, 915), "hl": [(46, 325, 516, 530)],
             "chip": "Three documents, drafted"},
            {"cap": "Here, the writeup opens by naming the question the evidence could not answer.",
             "say": "Here, the write-up opens by naming the question the evidence could not answer.",
             "claim": ["L14"], "img": "06_performance_review.png", "focus": (700, 180, 1760, 700), "hl": [(802, 430, 1643, 668)],
             "chip": "Honest about gaps"},
            {"cap": "The evaluation coordinator runs each review and owns the final wording.",
             "claim": ["L15"], "img": "06_performance_review.png", "focus": (0, 520, 1000, 915), "hl": [(140, 862, 425, 888)],
             "chip": "You own the final wording"},
        ],
    },
    # ------------------------------------------------------------------ 6 FAQ
    {
        "id": "faq", "kind": "kinetic", "label": "Questions partners ask",
        "sentences": [
            {"cap": "The AI does not decide where someone stands. Your evaluation coordinator forms the view with the agent, from graded facts.",
             "claim": ["L23"], "kicker": "What partners ask us", "big": "The AI does not decide where someone stands.",
             "small": "Your evaluation coordinator forms the view with the agent, from graded facts."},
            {"cap": "The coach never nags. If someone does not want to answer, it asks once or twice and then lets them go.",
             "claim": ["L18"], "kicker": "What partners ask us", "big": "The coach never nags.",
             "small": "If someone does not want to answer, it asks once or twice and then lets them go."},
        ],
    },
    # ---------------------------------------------------------------- 7 PROOF
    {
        "id": "proof", "kind": "proof", "label": "Proof",
        "sentences": [
            {"cap": "The firm that gave up on its AI assistant then signed a 24-month licence, and now runs its senior deal team on CraftArc.",
             "say": "The firm that gave up on its AI assistant then signed a 24-month licence, and now runs its senior deal team on Craft Arc.",
             "claim": ["L01", "P01", "P02"], "card": 0},
            {"cap": "We built it with that firm's COO, who designed the framework.",
             "say": "We built it with that firm's C.O.O., who designed the framework.",
             "claim": ["P03"], "card": 1},
            {"cap": "Our founder, Dash, worked at McKinsey, Microsoft and Siemens, and builds AI agents for private equity deal teams.",
             "claim": ["P04"], "card": 2},
        ],
    },
    # ---------------------------------------------------------------- 8 OFFER
    {
        "id": "offer", "kind": "offer", "label": "How firms start",
        "sentences": [
            {"cap": "You start with your senior deal team only, which keeps the disruption low.",
             "claim": ["O01"], "item": 0},
            {"cap": "Participants and evaluators are unlimited, and contributors are never charged.",
             "claim": ["O03"], "item": 1},
            {"cap": "If we miss a stage we agreed to deliver and do not fix it, you can leave, and we refund your prepaid fees pro rata.",
             "claim": ["O04"], "item": 2},
            {"cap": "It works best when leadership commits to running the cycle. If that commitment is not there yet, we will say so.",
             "claim": ["O06"], "item": 2},
        ],
    },
    # ------------------------------------------------------------------ 9 CTA
    {
        "id": "cta", "kind": "cta", "label": "Next step",
        "sentences": [
            {"cap": "If your next review cycle starts in the new year, plan it now.", "claim": ["U01"]},
            {"cap": "Book a demo, bring your competency framework, and we will talk through how it would run on CraftArc.",
             "say": "Book a demo, bring your competency framework, and we will talk through how it would run on Craft Arc.",
             "claim": ["C01"]},
            {"cap": "This voice is AI generated.", "claim": ["D01"]},
        ],
    },
]

# Visual copy that is not spoken.
PROOF_CARDS = [
    ("Tried it themselves first", "One firm signed a 24-month licence.", "It first spent 60 to 100 hours on a do-it-yourself AI attempt. Its principals, MDs and partners now take part."),
    ("Built with practitioners", "We designed it with the firm's COO.", "Eight to ten client interviews shaped how each competency is weighted and probed."),
    ("Who built it", "Bibhudatta \"Dash\", founder", "Dash worked at McKinsey, Microsoft and Siemens, and founded AgenticPM."),
]
OFFER_ITEMS = [
    ("Start with your senior deal team", "Begin with the principals, MDs and partners only. The disruption stays low."),
    ("Unlimited users", "Participants and evaluators are unlimited. Contributors are never charged."),
    ("Exit right", "If we miss a stage we agreed to deliver and do not fix it, you can leave with a pro rata refund."),
]
GRADES = [("Directly observed", (34, 197, 94)), ("Hearsay", (245, 158, 11)), ("Third party", (148, 163, 184))]
CTA = {"intro": ("If your next cycle starts in the new year,", "plan it now."),
       "title": "Book a demo", "sub": "Bring your competency framework. We will talk through how it would run on CraftArc.",
       "url": "",  # set the website address here once the domain is live
       "fine": "Product screens use sample data. Voiceover is AI generated."}

VOICE = {"voice": "af_heart", "speed": 1.0, "lang": "en-us"}
TIMING = {"scene_lead": 0.25, "gap": 0.24, "scene_tail": 0.35}


def all_sentences():
    for si, sc in enumerate(SCENES):
        for ti, s in enumerate(sc["sentences"]):
            yield si, ti, sc, s


def spoken(s):
    return s.get("say", s["cap"])


if __name__ == "__main__":
    n = sum(len(spoken(s).split()) for _, _, _, s in all_sentences())
    print(f"{n} spoken words, about {n / 155 * 60:.0f}s at 155 wpm")


def _balanced(words, k):
    """Split words into k runs of roughly equal character length."""
    total = sum(len(w) + 1 for w in words)
    groups, cur, acc = [], [], 0
    for i, w in enumerate(words):
        cur.append(w)
        acc += len(w) + 1
        left_groups = k - len(groups) - 1
        if left_groups > 0 and acc >= total * (len(groups) + 1) / k and len(words) - i - 1 >= left_groups:
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    return groups


def caption_chunks(text, max_chars=64):
    """Caption cues for one sentence: a list of cues, each a list of one or two
    balanced lines no longer than max_chars. Never leaves a lone word behind."""
    import re
    glued = re.sub(r"(\d+) to (\d+)", "\\1\u00a0to\u00a0\\2", text)  # keep "60 to 100" on one line
    words = glued.split(" ")
    n_lines = max(1, -(-len(text) // max_chars))
    while True:
        cues = []
        for g in _balanced(words, -(-n_lines // 2)):
            line = " ".join(g)
            cues.append([line] if len(line) <= max_chars else [" ".join(x) for x in _balanced(g, 2)])
        if all(len(ln) <= max_chars for c in cues for ln in c):
            return [[ln.replace("\u00a0", " ") for ln in c] for c in cues]
        n_lines += 1
