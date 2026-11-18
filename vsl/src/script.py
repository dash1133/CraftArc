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
    # ------------------------------------------------------------- 1 THE QUESTION
    {
        "id": "question", "kind": "kinetic", "label": "The question",
        "sentences": [
            {"cap": "What separates the great funds from the mediocre ones?",
             "claim": ["N04"], "kicker": "For private equity leaders", "big": "What separates the great funds from the mediocre ones?", "small": ""},
            {"cap": "It is not investment judgement alone. It is how they grow their next set of leaders.",
             "claim": ["N04"], "kicker": "Not investment judgement alone", "big": "How they grow their next set of leaders.", "accent": True, "small": ""},
        ],
    },
    # ------------------------------------------------------------- 2 THE EVIDENCE
    {
        "id": "evidence", "kind": "stat", "label": "The evidence",
        "sentences": [
            {"cap": "Judgement lives in people. In a study of nearly 4,000 buyout managers, the individual mattered about four times as much as the firm in explaining returns.",
             "claim": ["R1"], "big": "About 4x",
             "small": "how much more the individual manager mattered than the firm in explaining buyout returns",
             "source": "Braun, Dorau, Jenkinson and Urban, working paper. Nearly 4,000 managers at about 800 firms, 1970 to 2017."},
            {"cap": "And when senior partners leave, raising the next fund gets harder.",
             "claim": ["R2"], "big": "Partners leave",
             "small": "and raising the next fund gets harder",
             "source": "Ivashina and Lerner, Journal of Financial Economics, 2019."},
            {"cap": "Leadership is what turns a fund into an institution.",
             "claim": ["N04"], "big": "Leadership turns a fund into an institution.", "small": "", "source": ""},
        ],
    },
    # ------------------------------------------------------------- 3 THE PROBLEM
    {
        "id": "problem", "kind": "arcproblem", "label": "The problem",
        "sentences": [
            {"cap": "Yet most private equity firms have never written down their craft, what it takes to lead an investment fund, competency by competency.",
             "claim": ["N05"], "state": "craft"},
            {"cap": "And few help each leader trace their arc, the progress they make on every competency their craft demands.",
             "claim": ["N05"], "state": "arc"},
            {"cap": "So the craft stays in a few heads, and feedback arrives once a year, too late to use.",
             "claim": ["N05"], "state": "late"},
        ],
    },
    # ------------------------------------------------------------- 4 INTRODUCING
    {
        "id": "introducing", "kind": "logo", "label": "Introducing CraftArc",
        "sentences": [
            {"cap": "That is why we built CraftArc, to help funds build their next set of leaders.",
             "say": "That is why we built Craft Arc, to help funds build their next set of leaders.",
             "claim": ["N03"], "big": "", "small": "", "logo": True},
            {"cap": "It tracks how each leader is progressing, on investment judgement and on fit with your people and culture.",
             "claim": ["L05"], "kicker": "It tracks each leader's progress", "big": "Investment judgement. Fit with your people and culture.", "small": ""},
        ],
    },
    {
        "id": "team", "kind": "screen", "label": "Your whole senior team", "step": None,
        "sentences": [
            {"cap": "And it gives you one view of your whole senior team, person by person.",
             "claim": ["L07"], "img": "02_my_people.png", "focus": (20, 100, 1900, 460), "hl": [(36, 225, 1885, 436)],
             "chip": "Your senior team, in one view"},
        ],
    },
    # ------------------------------------------------------------- 5 WHY IT WORKS
    {
        "id": "why", "kind": "offer", "label": "Why it works",
        "kicker": "WHY IT WORKS", "title": "Your partners grow leaders. The agent does the rest.",
        "items": [
            ("Your craft, framed with experts", "We frame your competency model with you, so what great looks like is written down."),
            ("No administrative burden", "The agent holds the conversations, gathers feedback in one place and drafts the write-ups."),
            ("Plans people own", "Each person owns their development plan and tracks it through the year."),
            ("Partners' time back", "Your partners spend their time grooming leaders instead of chasing feedback."),
        ],
        "sentences": [
            {"cap": "Here is why it works. First, we bring the expertise to frame your competency model with you, so your craft is finally written down.",
             "claim": ["P07"], "item": 0},
            {"cap": "Second, it removes the administrative burden. An AI agent holds the conversations, gathers the feedback in one place and drafts the write-ups.",
             "claim": ["L08", "L10", "L13"], "item": 1},
            {"cap": "Third, each person owns their development plan and tracks it.", "claim": ["L21"], "item": 2},
            {"cap": "So your partners spend their time grooming leaders instead of chasing feedback.", "claim": ["N03"], "item": 3},
        ],
    },
    # ------------------------------------------------------------- 6 HOW, AS A DIALOGUE
    {
        "id": "journey", "kind": "journey", "label": "Five conversations",
        "sentences": [
            {"cap": "The agent is an expert in conversation. Here is how a cycle unfolds.", "claim": ["L08"], "step": None},
            {"cap": "It talks with each person for their self-evaluation, by voice or text, in about 25 minutes.",
             "claim": ["L08", "L24"], "step": 0, "bubble": "To get started, what have you worked on over the period?"},
            {"cap": "It helps the evaluator design the feedback interviews, so the right people speak to each competency.",
             "claim": ["L17", "L12"], "step": 1, "bubble": "Nobody who saw the banker meetings is on the list yet. Shall we add someone who did?"},
            {"cap": "It speaks with each contributor, and gathers what they saw first-hand in one place.",
             "claim": ["L10", "L11"], "step": 2, "bubble": "Tell me about a call you saw Arjun make on Atlas. What did you see first-hand?"},
            {"cap": "It drafts the memo for your Executive Committee, and the evaluator owns the final wording.",
             "claim": ["L13", "L15"], "step": 3, "bubble": "I'm drafting the review documents now. I'll let you know as each one is ready."},
            {"cap": "And it helps each person build their own development plan, then track it through the year.",
             "claim": ["L21"], "step": 4, "bubble": "Which of these goals would you like to start with?"},
            {"cap": "Five conversations make one arc, and every leader knows where they stand.", "claim": ["N03"], "step": "all"},
        ],
    },
    # ------------------------------------------------------------- 7 NEXT STEP
    {
        "id": "cta", "kind": "cta", "label": "Next step",
        "sentences": [
            {"cap": "If your next review cycle starts in the new year, now is the time to set it up.", "claim": ["U01"]},
            {"cap": "To book a demo, write to dash@craftarc.ai.", "say": "To book a demo, write to dash, at craft arc dot A I.", "claim": ["C01"]},
            {"cap": "This voice is AI generated.", "claim": ["D01"]},
        ],
    },
]

STEP_NAMES = ["Self-evaluation", "Design the feedback", "Contributor interviews", "The memo", "Development plan"]
STEP_ICONS = ["mic", "person_gear", "people", "document", "checklist"]

# Kept for the renderer's older scene types.
PROOF_CARDS = []
OFFER_ITEMS = []
GRADES = [("Directly observed", (34, 197, 94)), ("Hearsay", (245, 158, 11)), ("Third party", (148, 163, 184))]
CTA = {"intro": ("If your next cycle starts in the new year,", "set it up now."),
       "title": "Book a demo",
       "sub": "Write to dash@craftarc.ai, and bring your competency framework.",
       "url": "dash@craftarc.ai",
       "fine": "Product screens and agent dialogue use sample data. Voiceover is AI generated."}

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
