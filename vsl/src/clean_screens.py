"""Clean the six CraftArc app screenshots for marketing use.

What it changes (demo data only, never features or layout):
  * the signed-in user in the header (a real staff name) becomes a fictional
    "Daniel Shaw, Partner";
  * test cycle names ("ARC H1 2026 - TESTING", "Test Review Cycle", ...) become
    neutral cycle names;
  * test-account suffixes ("Parth 1", "Nishritha 2", "Karan 1",
    "Nishritha Employee") become plain first names.

Every edit is listed in EDIT_LOG and written to clean/EDITS.md so the change
is auditable. Run:  python vsl/src/clean_screens.py
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "assets" / "screens" / "raw"
OUT = ROOT / "assets" / "screens" / "clean"
FONT_DIR = Path("/usr/share/fonts/opentype/inter")
WEIGHTS = {
    "regular": "Inter-Regular.otf",
    "medium": "Inter-Medium.otf",
    "semibold": "Inter-SemiBold.otf",
    "bold": "Inter-Bold.otf",
    "light": "Inter-Light.otf",
}
EDIT_LOG = []


def font_path(weight):
    p = FONT_DIR / WEIGHTS[weight]
    if not p.exists():
        raise FileNotFoundError(p)
    return str(p)


def fit_font(ref_text, ref_width, weight):
    """Font whose rendering of ref_text is ref_width pixels wide (ink box)."""
    lo, hi = 6.0, 60.0
    for _ in range(30):
        mid = (lo + hi) / 2
        f = ImageFont.truetype(font_path(weight), mid)
        x0, _, x1, _ = f.getbbox(ref_text)
        if x1 - x0 < ref_width:
            lo = mid
        else:
            hi = mid
    return ImageFont.truetype(font_path(weight), (lo + hi) / 2)


def ink_color(img, box):
    a = np.asarray(img.crop(box).convert("RGB")).reshape(-1, 3).astype(int)
    return tuple(int(v) for v in a[a.sum(1).argmin()])


def bg_color(img, box):
    a = np.asarray(img.crop(box).convert("RGB")).reshape(-1, 3)
    vals, counts = np.unique(a, axis=0, return_counts=True)
    return tuple(int(v) for v in vals[counts.argmax()])


def erase(img, box, color=None):
    color = color or bg_color(img, box)
    ImageDraw.Draw(img).rectangle([box[0], box[1], box[2] - 1, box[3] - 1], fill=color)


def draw(img, x, baseline, text, font, color, anchor="ls"):
    ImageDraw.Draw(img).text((x, baseline), text, font=font, fill=color, anchor=anchor)


def delete_span(img, y0, y1, x_from, x_to, line_end, bg=None):
    """Remove columns [x_from, x_to) of a text line by sliding the rest left."""
    bg = bg or bg_color(img, (x_from, y0, line_end, y1))
    strip = img.crop((x_to, y0, line_end, y1))
    erase(img, (x_from, y0, line_end, y1), bg)
    img.paste(strip, (x_from, y0))


def replace_word(img, name, box, ref_text, new_text, weight, baseline=None, color=None, bg=None):
    """Erase the ink box of ref_text and draw new_text in a matched font."""
    x0, y0, x1, y1 = box
    font = fit_font(ref_text, x1 - x0, weight)
    color = color or ink_color(img, box)
    erase(img, (x0 - 1, y0 - 2, x1 + 2, y1 + 3), bg)
    # ink top of ref_text sits at y0; baseline = y0 - bbox_top offset
    top = font.getbbox(ref_text, anchor="ls")[1]
    base = baseline if baseline is not None else y0 - top
    lx = x0 - font.getbbox(new_text, anchor="ls")[0]
    draw(img, lx, base, new_text, font, color)
    EDIT_LOG.append(f"{name}: '{ref_text}' -> '{new_text}'")
    return font, base


def header_user(img, name, top):
    """Signed-in user block (avatar, name, role, chevron) at the header right."""
    erase(img, (1724, top - 6, 1892, top + 38), (255, 255, 255))
    d = ImageDraw.Draw(img)
    cx, cy, r = 1745.5, top + 16.5, 17
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(24, 42, 79))
    draw(img, cx, cy + 1, "D", ImageFont.truetype(font_path("semibold"), 15), (255, 255, 255), anchor="mm")
    draw(img, 1772, top + 13, "Daniel Shaw", fit_font("Parth Yadav", 81, "semibold"), (41, 42, 46))
    draw(img, 1772, top + 31, "Partner", fit_font("Partner, India", 76, "regular"), (69, 85, 108))
    # chevron
    d.line([(1869, top + 13), (1874.5, top + 18.5), (1880, top + 13)], fill=(55, 65, 81), width=2)
    EDIT_LOG.append(f"{name}: header user 'Parth Yadav / Partner, India' (or 'Parth 1 / Principal') -> 'Daniel Shaw / Partner'")


def avatar_initials(img, name, center, new, size=12, color=None, circle_bg=None):
    cx, cy = center
    circle_bg = circle_bg or img.getpixel((int(cx) - 11, int(cy)))[:3]
    color = color or (71, 85, 105)
    erase(img, (int(cx - 11), int(cy - 7), int(cx + 12), int(cy + 8)), circle_bg)
    draw(img, cx, cy + 0.5, new, ImageFont.truetype(font_path("semibold"), size), color, anchor="mm")
    EDIT_LOG.append(f"{name}: avatar initials -> '{new}'")


def chips(img, name):
    """Redraw the cycle chips in the home screen's to-do panel."""
    region = (1146, 180, 1890, 296)
    erase(img, region, (255, 255, 255))
    d = ImageDraw.Draw(img)
    f = fit_font("Spotlight FY26", 97, "medium")
    labels = [
        ["Spotlight FY26", "Elevate FY25", "Partner track H2 2026"],
        ["Principal review FY26", "Standard nine-step journey"],
        ["FY26 annual review", "Mid-year pulse 2026", "Deal team review"],
    ]
    active = "Deal team review"
    y = 186
    for row in labels:
        x = 1151
        for lab in row:
            w = f.getbbox(lab)[2] - f.getbbox(lab)[0]
            box = [x, y, x + w + 30, y + 30]
            if lab == active:
                d.rounded_rectangle(box, 15, fill=(36, 93, 229))
                draw(img, x + 15, y + 20, lab, fit_font("Spotlight FY26", 97, "semibold"), (255, 255, 255))
            else:
                d.rounded_rectangle(box, 15, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
                draw(img, x + 15, y + 20, lab, f, (30, 41, 59))
            x = box[2] + 8
        y += 38
    EDIT_LOG.append(f"{name}: to-do cycle chips redrawn with neutral cycle names (test names removed)")


def clean_home(img):
    n = "01_home"
    header_user(img, n, 40)
    replace_word(img, n, (303, 140, 409, 162), "Parth 1.", "Daniel.", "bold")
    chips(img, n)
    avatar_initials(img, n, (1168.5, 382), "DS", size=13)
    replace_word(img, n, (1196, 366, 1245, 378), "Parth 1", "Daniel Shaw", "regular")
    replace_word(img, n, (97, 687, 268, 706), "FY25 - Cycle Test", "Elevate FY25", "semibold", bg=(240, 249, 255))
    # "...feedback for Nishritha Employee and Nishritha Evaluator: done, ..." -> "... for Nishritha and Karan: done, ..."
    f = fit_font("Eval.coordinator feedback for Nishritha", 404 - 117, "regular")
    col = ink_color(img, (117, 774, 404, 789))
    erase(img, (405, 770, 900, 795), (255, 255, 255))
    base = 774 - f.getbbox("Eval.coordinator", anchor="ls")[1]
    draw(img, 405, base, " and Karan: done, so 2 of 5 are done.", f, col)
    EDIT_LOG.append(f"{n}: 'Nishritha Employee and Nishritha Evaluator' -> 'Nishritha and Karan'")
    # "Nishritha Employee has completed" -> "Nishritha has completed"
    delete_span(img, 856, 880, 181, 258, 700)
    EDIT_LOG.append(f"{n}: 'Nishritha Employee has completed' -> 'Nishritha has completed'")


def clean_my_people(img):
    n = "02_my_people"
    header_user(img, n, 40)
    avatar_initials(img, n, (71, 377), "P", size=13)
    erase(img, (140, 366, 152, 386), (255, 255, 255))
    EDIT_LOG.append(f"{n}: 'Parth 1' -> 'Parth'")


def clean_my_reviews(img):
    n = "03_my_reviews"
    header_user(img, n, 39)
    titles = [
        ((54, 297, 298, 311), "ARC H1 2026 - TESTING (Latest)", "Spotlight FY26"),
        ((54, 456, 285, 470), "ARC H1 2026 - TESTING (New)", "Partner track H2 2026"),
        ((54, 615, 236, 627), "ARC H1 2026 - TESTING", "FY26 annual review"),
    ]
    for box, old, new in titles:
        replace_word(img, n, box, old, new, "semibold")
    # coordinators: "Parth 1" -> "Karan" (rows 1-3), "Nishritha Employee" -> "Nishritha" (row 4)
    for y in (298, 457, 616):
        replace_word(img, n, (790, y, 841, y + 12), "Parth 1", "Karan", "semibold")
        avatar_initials(img, n, (763.5, y + 18), "K", size=12)
    erase(img, (857, 772, 940, 794), (255, 255, 255))
    EDIT_LOG.append(f"{n}: 'Nishritha Employee' -> 'Nishritha'")
    avatar_initials(img, n, (763.5, 793), "N", size=12)
    # status circles showing whose turn it is
    for cy, new in ((451, "K"), (609, "K"), (767, "N")):
        d = ImageDraw.Draw(img)
        d.ellipse([1422, cy - 9, 1441, cy + 9], fill=(255, 255, 255))
        draw(img, 1431.5, cy + 0.5, new, ImageFont.truetype(font_path("semibold"), 12), (37, 99, 235), anchor="mm")
        EDIT_LOG.append(f"{n}: turn indicator initials -> '{new}'")


def clean_roster(img):
    n = "04_survey_roster"
    header_user(img, n, 43)
    delete_span(img, 180, 204, 304, 320, 425)
    delete_span(img, 470, 494, 223, 239, 425)
    EDIT_LOG.append(f"{n}: chat 'Nishritha 2' -> 'Nishritha' (2 places)")
    # "...file from Nishritha 2." -> "...file from Nishritha."
    erase(img, (1099, 610, 1125, 632), (255, 255, 255))
    f = fit_font("Nishritha", 1098 - 1034, "regular")
    draw(img, 1099, 614 - f.getbbox("Nishritha", anchor="ls")[1], ".", f, ink_color(img, (1034, 614, 1098, 626)))
    erase(img, (642, 780, 660, 800), (255, 255, 255))
    EDIT_LOG.append(f"{n}: status and roster 'Nishritha 2' -> 'Nishritha'")


def clean_coverage(img):
    n = "05_survey_coverage"
    header_user(img, n, 40)
    delete_span(img, 177, 201, 304, 320, 425)
    delete_span(img, 467, 491, 223, 239, 425)
    erase(img, (994, 594, 1012, 614), (255, 255, 255))
    erase(img, (994, 811, 1012, 831), (255, 255, 255))
    delete_span(img, 377, 397, 1425, 1439, 1600)
    delete_span(img, 594, 618, 1551, 1566, 1600)
    delete_span(img, 811, 835, 1425, 1439, 1600)
    delete_span(img, 634, 657, 1732, 1743, 1860)
    EDIT_LOG.append(f"{n}: 'Nishritha 2' -> 'Nishritha' (7 places), 'Karan 1' -> 'Karan'")


def clean_review(img):
    n = "06_performance_review"
    header_user(img, n, 40)
    delete_span(img, 382, 408, 847, 859, 1110)
    EDIT_LOG.append(f"{n}: 'Parth 1 | Principal' -> 'Parth | Principal'")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = {
        "01_home.png": clean_home,
        "02_my_people.png": clean_my_people,
        "03_my_reviews.png": clean_my_reviews,
        "04_survey_roster.png": clean_roster,
        "05_survey_coverage.png": clean_coverage,
        "06_performance_review.png": clean_review,
    }
    for fname, fn in jobs.items():
        img = Image.open(RAW / fname).convert("RGB")
        fn(img)
        img.save(OUT / fname, optimize=True)
    (OUT / "EDITS.md").write_text(
        "# Screenshot edits\n\nDemo data relabelled for marketing use. No UI, feature or layout was changed.\n\n"
        + "\n".join(f"- {line}" for line in EDIT_LOG)
        + "\n"
    )
    print("\n".join(EDIT_LOG))


if __name__ == "__main__":
    main()
