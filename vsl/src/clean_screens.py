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
from PIL import Image, ImageDraw, ImageFilter, ImageFont

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


def line_end_from(img, x, y0, y1, bg, gap=30, limit=None):
    """First x after which the text line on rows y0..y1 has `gap` blank columns."""
    a = np.asarray(img.crop((x, y0, limit or img.width, y1)).convert("RGB")).astype(int)
    ink = (np.abs(a - np.array(bg)).sum(axis=2) > 150).any(axis=0)
    last, blank = 0, 0
    for i, v in enumerate(ink):
        if v:
            last, blank = i, 0
        else:
            blank += 1
            if blank >= gap:
                break
    return x + last + 1


def ink_columns(img, x0, x1, y0, y1, bg, thresh=150):
    a = np.asarray(img.crop((x0, y0, x1, y1)).convert("RGB")).astype(int)
    return (np.abs(a - np.array(bg)).sum(axis=2) > thresh).any(axis=0)


def cap_height_font(img, box, weight, bg):
    """Font sized so its cap height matches the name's first capital letter."""
    x0, y0, x1, y1 = box
    a = np.asarray(img.crop((x0, y0 - 4, x0 + 7, y1 + 4)).convert("RGB")).astype(int)
    rows = np.where((np.abs(a - np.array(bg)).sum(axis=2) > 150).any(axis=1))[0]
    cap = rows[-1] - rows[0] + 1
    ref = ImageFont.truetype(font_path(weight), 100)
    hb = ref.getbbox("H")
    return ImageFont.truetype(font_path(weight), cap * 100 / (hb[3] - hb[1])), y0 - 4 + rows[-1] + 1


def token_end(img, box, bg):
    """Right ink edge of the OCR word, widened to take in faint anti-aliased columns."""
    x0, y0, x1, y1 = box
    cols = ink_columns(img, x1 - 3, x1 + 5, y0 - 2, y1 + 3, bg, thresh=30)
    end = x1 - 3
    for i, v in enumerate(cols):
        if v:
            end = x1 - 3 + i
        elif x1 - 3 + i > x1:
            break
    return end


def replace_name(img, name, box, token, old, new, weight="regular", limit=None):
    """Redraw the OCR word `token` (for example "Parth's") with `new` in place of
    `old`, and slide the rest of the line so the gap after the word is kept."""
    x0, y0, x1, y1 = box
    colour = ink_color(img, box)
    bg = bg_color(img, (max(x0 - 6, 0), y0, x0 - 1, y1))
    font, base = cap_height_font(img, box, weight, bg)
    end = token_end(img, box, bg)
    new_token = new + token[len(old):]
    nb = font.getbbox(new_token, anchor="ls")
    delta = (x0 + (nb[2] - nb[0]) - 1) - end
    ry0, ry1 = int(y0 - 3), int(base + font.size * 0.3)
    line_end = line_end_from(img, end + 1, ry0, ry1, bg, limit=limit)
    strip = img.crop((end + 1, ry0, line_end + 2, ry1))
    erase(img, (x0 - 1, ry0, line_end + 2 + max(delta, 0), ry1), bg)
    img.paste(strip, (end + 1 + delta, ry0))
    draw(img, x0 - nb[0], base, new_token, font, colour)
    EDIT_LOG.append(f"{name}: '{token}' -> '{new_token}' at ({x0}, {y0})")


NAMES = {"Parth": "Arjun", "Nishritha": "Anushka", "Karan": "Varun"}


def rename_all(img, name, hits):
    """hits: (old name, OCR token, ink box, weight), found with Tesseract on the cleaned screen."""
    for old, token, box, weight in hits:
        replace_name(img, name, box, token, old, NAMES[old], weight)


def blur(img, name, box, why):
    region = img.crop(box).filter(ImageFilter.GaussianBlur(5))
    img.paste(region, box[:2])
    EDIT_LOG.append(f"{name}: blurred {box} ({why})")


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
        ["Principal review FY26", "Senior team review FY26"],
        ["FY26 annual review", "H1 2026 review", "Deal team review"],
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
    EDIT_LOG.append(f"{name}: to-do cycle chips redrawn (test names removed). New chip names, all invented sample "
                    f"cycle names: {', '.join(l for row in labels for l in row)}")


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
    draw(img, 405, base, " and Varun: done, so 2 of 5 are done.", f, col)
    EDIT_LOG.append(f"{n}: 'Nishritha Employee and Nishritha Evaluator' -> 'Nishritha and Varun'")
    # "Nishritha Employee has completed" -> "Nishritha has completed"
    delete_span(img, 856, 880, 181, 258, 700)
    EDIT_LOG.append(f"{n}: 'Nishritha Employee has completed' -> 'Nishritha has completed'")
    rename_all(img, n, [
        ("Nishritha", "Nishritha", (340, 774, 404, 786), "regular"),
        ("Nishritha", "Nishritha", (117, 860, 181, 872), "regular"),
    ])


def clean_my_people(img):
    n = "02_my_people"
    header_user(img, n, 40)
    avatar_initials(img, n, (71, 377), "A", size=13)
    erase(img, (140, 366, 152, 386), (255, 255, 255))
    EDIT_LOG.append(f"{n}: 'Parth 1' -> 'Parth'")
    rename_all(img, n, [("Parth", "Parth", (101, 371, 139, 382), "semibold")])


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
        replace_word(img, n, (790, y, 841, y + 12), "Parth 1", "Kabir", "semibold")
        avatar_initials(img, n, (763.5, y + 18), "K", size=12)
    erase(img, (857, 772, 940, 794), (255, 255, 255))
    EDIT_LOG.append(f"{n}: 'Nishritha Employee' -> 'Nishritha'")
    avatar_initials(img, n, (763.5, 793), "A", size=12)
    rename_all(img, n, [("Nishritha", "Nishritha", (791, 774, 857, 786), "semibold")])
    replace_word(img, n, (54, 774, 261, 789), "Standard nine-step journey", "Senior team review FY26", "semibold")
    # status circles showing whose turn it is
    for cy, new in ((451, "K"), (609, "K"), (767, "A")):
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
    rename_all(img, n, [
        ("Nishritha", "Nishritha", (233, 184, 304, 197), "regular"),
        ("Parth", "Parth", (1084, 402, 1121, 413), "regular"),
        ("Nishritha", "Nishritha", (152, 474, 223, 487), "regular"),
        ("Nishritha", "Nishritha.", (1035, 614, 1102, 627), "regular"),
        ("Nishritha", "Nishritha", (574, 784, 641, 796), "semibold"),
        ("Nishritha", "Nishritha,", (1023, 784, 1091, 799), "regular"),
        ("Parth", "Parth", (835, 808, 872, 819), "regular"),
        ("Parth", "Parth", (1158, 808, 1195, 819), "regular"),
    ])


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
    rename_all(img, n, [
        ("Nishritha", "Nishritha", (233, 181, 304, 194), "regular"),
        ("Nishritha", "Nishritha", (1361, 381, 1425, 393), "regular"),
        ("Parth", "Parth's", (1361, 450, 1412, 461), "regular"),
        ("Nishritha", "Nishritha", (152, 471, 223, 484), "regular"),
        ("Parth", "Parth's", (744, 501, 795, 512), "regular"),
        ("Nishritha", "Nishritha", (929, 598, 993, 610), "regular"),
        ("Parth", "Parth", (1094, 598, 1131, 610), "regular"),
        ("Nishritha", "Nishritha,", (1488, 598, 1555, 613), "regular"),
        ("Parth", "Parth", (1361, 644, 1398, 655), "regular"),
        ("Karan", "Karan,", (1691, 639, 1736, 653), "regular"),
        ("Parth", "Parth", (723, 694, 760, 706), "regular"),
        ("Nishritha", "Nishritha", (929, 815, 993, 827), "regular"),
        ("Parth", "Parth", (1094, 815, 1131, 827), "regular"),
        ("Nishritha", "Nishritha", (1361, 815, 1425, 827), "regular"),
    ])
    for box in ((595, 450, 886, 542), (595, 667, 886, 759)):
        blur(img, n, box, "lines of inquiry may come from a client's confidential framework")


def clean_review(img):
    n = "06_performance_review"
    header_user(img, n, 40)
    delete_span(img, 382, 408, 847, 859, 1110)
    EDIT_LOG.append(f"{n}: 'Parth 1 | Principal' -> 'Parth | Principal'")
    rename_all(img, n, [
        ("Parth", "Parth", (1102, 124, 1139, 135), "regular"),
        ("Parth", "Parth", (804, 386, 846, 400), "regular"),
        ("Parth", "Parth", (173, 413, 212, 424), "semibold"),
        ("Parth", "Parth", (157, 567, 199, 580), "regular"),
    ])
    for box in ((1001, 504, 1042, 518), (932, 580, 973, 594)):  # inside the red panel: stop before its border
        replace_name(img, n, box, "Parth", "Parth", "Arjun", "regular", limit=1636)
    blur(img, n, (560, 686, 1890, 905), "the writeup body below the summary quotes a client's framework language")


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
        "# Screenshot edits\n\nSample data relabelled for marketing use: test names and a real staff name replaced with "
        "invented names, and two areas blurred. No UI, feature or layout was changed.\n\n"
        + "\n".join(f"- {line}" for line in EDIT_LOG)
        + "\n"
    )
    print("\n".join(EDIT_LOG))


if __name__ == "__main__":
    main()
