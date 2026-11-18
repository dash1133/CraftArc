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
            {"cap": "One private equity firm spent 60 to 100 hours of senior time trying to make a general AI assistant run its leadership reviews.",
             "claim": ["L01"], "kicker": "One private equity firm spent", "big": "60 to 100 hours", "small": "of senior time trying to make a general AI assistant run its leadership reviews"},
            {"cap": "Then it gave up.", "claim": ["L01"], "big": "Then it gave up.", "small": ""},
            {"cap": "If you are building your firm's next partners, here is what that firm did instead.",
             "claim": ["N01"], "big": "Building your firm's next partners?", "small": "Here is what that firm did instead."},
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
            {"cap": "The AI assistant could not hold the framework, and what the team built could not be shared.",
             "claim": ["L01"], "doc_state": "gaps"},
        ],
    },
    # ----------------------------------------------------------------- 3 PAIN
    {
        "id": "pain", "kind": "kinetic", "label": "Two questions",
        "sentences": [
            {"cap": "Ask yourself. Do your principals know where they stand on each competency today?",
             "claim": ["N02"], "big": "Do your principals know where they stand on each competency?", "small": "", "kicker": "Ask yourself"},
            {"cap": "And does their feedback reach them in time for the next deal?",
             "claim": ["N02"], "big": "Does their feedback reach them in time for the next deal?", "small": "", "kicker": "Ask yourself"},
        ],
    },
    # -------------------------------------------------------------- 4 INSIGHT
    {
        "id": "insight", "kind": "logo", "label": "The insight",
        "sentences": [
            {"cap": "Your framework is the asset.", "claim": ["N03"], "big": "Your framework is the asset.", "small": ""},
            {"cap": "It needs a system that interviews your people, gathers the evidence and drafts the write-up.",
             "claim": ["N03", "L05"], "big": "It needs a system that runs it.", "small": "It interviews your people, gathers the evidence and drafts the write-up."},
            {"cap": "That is why we built CraftArc.", "say": "That is why we built Craft Arc.", "claim": ["N03"], "big": "", "small": "", "logo": True},
        ],
    },
    # ----------------------------------------------------------------- 5 DEMO
    {
        "id": "home", "kind": "screen", "label": "Your framework, in plain English", "step": None,
        "sentences": [
            {"cap": "CraftArc runs your review cycle on your own competency framework, written in plain English.",
             "say": "Craft Arc runs your review cycle on your own competency framework, written in plain English.",
             "claim": ["L05"], "img": "01_home.png", "focus": (0, 0, 1919, 913), "hl": [(75, 228, 1067, 586)],
             "chip": "One home for every role"},
        ],
    },
    {
        "id": "steps", "kind": "screen", "label": "Five steps per person", "step": 0,
        "sentences": [
            {"cap": "Each person moves through five steps, from launching the review to a development plan.",
             "claim": ["L07"], "img": "02_my_people.png", "focus": (20, 100, 1900, 460), "hl": [(840, 278, 1830, 400)],
             "chip": "Five steps, tracked per person"},
        ],
    },
    {
        "id": "self", "kind": "screen", "label": "Self-review with an AI coach", "step": 1,
        "sentences": [
            {"cap": "In the self-review, an AI coach interviews each person against your competencies.",
             "claim": ["L08"], "img": "03_my_reviews.png", "focus": (20, 180, 1900, 560), "hl": [(1205, 425, 1295, 520)],
             "chip": "Self-review: your turn"},
            {"cap": "They answer by voice or text, and the coach asks for whatever is missing.",
             "claim": ["L08", "L09"], "img": "04_survey_roster.png", "focus": (0, 420, 545, 870), "hl": [(372, 742, 534, 822)],
             "chip": "Voice or text"},
        ],
    },
    {
        "id": "contrib", "kind": "screen", "label": "Contributor interviews", "step": 2,
        "sentences": [
            {"cap": "Contributors give anonymous interviews about what they saw first-hand.",
             "claim": ["L10"], "img": "04_survey_roster.png", "focus": (548, 250, 1919, 862), "pad": 0, "hl": [(563, 705, 1882, 862)],
             "chip": "Anonymous, AI-led interviews"},
            {"cap": "Every fact is graded as directly observed, hearsay or third party.",
             "claim": ["L11"], "img": "04_survey_roster.png", "focus": (548, 600, 1450, 870), "hl": [(750, 705, 1262, 862)],
             "chip": "Facts, graded by source"},
        ],
    },
    {
        "id": "coverage", "kind": "screen", "label": "Coverage, checked", "step": 2,
        "sentences": [
            {"cap": "Before the interviews close, the agent checks coverage for every competency.",
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
            {"cap": "If the evidence cannot answer a question, the writeup says so at the top.",
             "say": "If the evidence cannot answer a question, the write-up says so at the top.",
             "claim": ["L14"], "img": "06_performance_review.png", "focus": (700, 180, 1760, 700), "hl": [(802, 430, 1643, 668)],
             "chip": "Honest about gaps"},
            {"cap": "Your evaluation coordinator owns the final wording.",
             "claim": ["L15"], "img": "06_performance_review.png", "focus": (0, 520, 1000, 915), "hl": [(140, 862, 425, 888)],
             "chip": "You own the final wording"},
        ],
    },
    # ---------------------------------------------------------------- 6 PROOF
    {
        "id": "proof", "kind": "proof", "label": "Proof",
        "sentences": [
            {"cap": "That firm now runs its senior deal team on CraftArc, from principals to partners.",
             "say": "That firm now runs its senior deal team on Craft Arc, from principals to partners.",
             "claim": ["P01"], "card": 0},
            {"cap": "It signed a 24-month licence, and we built CraftArc with its COO, who designed the framework.",
             "say": "It signed a 24-month licence, and we built Craft Arc with its C.O.O., who designed the framework.",
             "claim": ["P02", "P03"], "card": 1},
            {"cap": "Our founder, Dash, worked at McKinsey, Microsoft and Siemens, and builds AI agents for private equity deal teams.",
             "claim": ["P04"], "card": 2},
        ],
    },
    # ---------------------------------------------------------------- 7 OFFER
    {
        "id": "offer", "kind": "offer", "label": "How firms start",
        "sentences": [
            {"cap": "You start with your senior deal team, and an implementation consultant adapts the framework to your firm.",
             "claim": ["O01", "O02"], "item": 0},
            {"cap": "One flat annual fee covers every participant and evaluator, contributors never pay, and there is no build-out fee.",
             "claim": ["O03"], "item": 1},
            {"cap": "If we miss a delivery stage and do not fix it, you can leave and we refund your prepaid fees pro rata.",
             "claim": ["O04"], "item": 2},
        ],
    },
    # ------------------------------------------------------------------ 8 CTA
    {
        "id": "cta", "kind": "cta", "label": "Next step",
        "sentences": [
            {"cap": "If your next review cycle starts in the new year, plan it now.", "claim": ["U01"]},
            {"cap": "Book a demo, bring your competency framework, and we will show you how it runs on CraftArc.",
             "say": "Book a demo, bring your competency framework, and we will show you how it runs on Craft Arc.",
             "claim": ["C01"]},
            {"cap": "This video's voice is AI generated.", "claim": ["D01"]},
        ],
    },
]

# Visual copy that is not spoken.
PROOF_CARDS = [
    ("Live today", "A mid-tier private equity firm runs its senior deal team on CraftArc", "Principals, MDs and partners"),
    ("Built with a PE COO", "24-month licence. Framework designed by the firm's COO", "The firm tried the do-it-yourself AI route first"),
    ("Who built it", "Founder: Bibhudatta \"Dash\"", "Ex-McKinsey, Microsoft and Siemens. Founder of AgenticPM"),
]
OFFER_ITEMS = [
    ("Start with your senior deal team", "An implementation consultant adapts your framework, language and steps"),
    ("One flat annual fee", "Unlimited participants and evaluators. Contributors never pay. No build-out fee"),
    ("Exit right", "Miss a delivery stage and do not fix it: you leave, with prepaid fees refunded pro rata"),
]
CTA = {"title": "Book a demo", "sub": "Bring your competency framework. We will show you how it runs on CraftArc.",
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
