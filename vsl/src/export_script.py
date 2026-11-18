"""Write vsl/VSL_Script.md from script.py and build/timeline.json, so the script
document always matches the rendered video. Run after make_voiceover.py."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from script import CTA, OFFER_ITEMS, PROOF_CARDS, SCENES  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def mmss(t):
    return f"{int(t // 60)}:{t % 60:04.1f}"


def visual(sc, s):
    k = sc["kind"]
    if k in ("kinetic", "logo"):
        if s.get("logo"):
            return "Logo reveal: CRAFT ARC, agentic leadership development"
        parts = [p for p in (s.get("kicker"), s.get("big"), s.get("small")) if p]
        return "Big type on navy: " + " / ".join(f'"{p}"' for p in parts)
    if k == "doc":
        return {"blank": "A blank page appears", "page": "The one page fills in: \"What great looks like\"",
                "gaps": "Beside it: what a page cannot do, then what the do-it-yourself attempt cost"}[s["doc_state"]]
    if k == "screen":
        if s.get("overlay") == "grades":
            return f'Screen `{s["img"]}` dimmed, with a designed card (not product UI): "Every fact carries its source": Directly observed, Hearsay, Third party'
        return f'Screen `{s["img"]}`, camera on {s["focus"]}, spotlight on {s["hl"]}, label "{s["chip"]}"'
    if k == "proof":
        c = PROOF_CARDS[s["card"]]
        return f'Proof card {s["card"] + 1}: "{c[0]}", "{c[1]}", "{c[2]}"'
    if k == "offer":
        c = sc.get("items", OFFER_ITEMS)[s["item"]]
        return f'Row {s["item"] + 1}: "{c[0]}", "{c[1]}"'
    if k == "stat":
        if s.get("source"):
            return f'Evidence card: "{s["big"]}", "{s["small"]}". Source on screen: {s["source"]}'
        return f'Big type: "{s["big"]}"'
    if k == "arcproblem":
        return {"craft": 'An arc of empty competency nodes marked "?": "The craft. Never written down."',
                "arc": 'A marker stalls at the start of the arc: "The arc. Never traced."',
                "late": 'The arc fades: "The feedback. Once a year. Too late to use."'}[s["state"]]
    if k == "journey":
        stp = s.get("step")
        if stp is None:
            return "Five step icons appear along an arc: self-evaluation, design the feedback, contributor interviews, the memo, development plan"
        if stp == "all":
            return 'All five icons light up and the arc fills orange: "Every leader knows where they stand."'
        return f'Step {stp + 1} icon lights up. Agent says (sample dialogue): "{s["bubble"]}"'
    if k == "cta":
        return f'End card: "{CTA["title"]}", "{CTA["sub"]}", fine print "{CTA["fine"]}"'
    return ""


def main():
    tl = json.loads((ROOT / "build" / "timeline.json").read_text())
    by = {(s["scene"], s["idx"]): s for s in tl["sentences"]}
    words = sum(s["words"] for s in tl["sentences"])
    out = [
        "# CraftArc VSL: script and storyboard",
        "",
        f"Generated from `vsl/src/script.py` and the voiceover timeline. Runtime **{mmss(tl['duration'])}**, "
        f"{words} spoken words ({words / tl['duration'] * 60:.0f} words a minute). "
        "Claim IDs refer to `docs/Claims_Ledger.md`.",
        "",
        "Structure from Dash's brief (18 Nov 2026): the question and the research evidence, the problem "
        "(the craft and the arc), introducing CraftArc, why it works, five conversations told as a dialogue, the next step.",
        "",
    ]
    for si, sc in enumerate(SCENES):
        a = tl["scenes"][si]
        out += [f"## {si + 1}. {sc['label']} ({mmss(a['start'])} to {mmss(a['end'])})", "",
                "| Time | Voiceover | On screen | Claims |", "|---|---|---|---|"]
        for ti, s in enumerate(sc["sentences"]):
            t = by[(si, ti)]
            out.append(f"| {mmss(t['start'])} | {s['cap']} | {visual(sc, s)} | {', '.join(s['claim'])} |")
        out.append("")
    (ROOT / "VSL_Script.md").write_text("\n".join(out))
    print("wrote", ROOT / "VSL_Script.md")


if __name__ == "__main__":
    main()
