"""Render the CraftArc VSL from script.py, the cleaned screens and the voiceover.

  python vsl/src/render_vsl.py            full render -> vsl/build/CraftArc_VSL_1080p.mp4
  python vsl/src/render_vsl.py --stills   one still per sentence -> vsl/build/stills/
  python vsl/src/render_vsl.py --web      also write the 720p web cut and poster

Needs: Pillow, numpy, ffmpeg on PATH, and vsl/build/{vo.wav,timeline.json}
from make_voiceover.py.
"""
import json
import math
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from script import CTA, GRADES, OFFER_ITEMS, PROOF_CARDS, SCENES, STEPS, caption_chunks  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
SCREENS = ROOT / "assets" / "screens" / "clean"
W, H, FPS = 1920, 1080, 30

NAVY = (11, 22, 51)
NAVY2 = (22, 40, 88)
BLUE = (36, 93, 229)
LOGO_BLUE = (25, 86, 223)
ORANGE = (245, 130, 32)
SLATE_BG = (241, 245, 249)
INK = (15, 23, 42)
MUTED = (100, 116, 139)
SOFT = (203, 213, 225)
WHITE = (255, 255, 255)

FONTS = Path("/usr/share/fonts/opentype/inter")
F = {
    "display_bold": "InterDisplay-Bold.otf",
    "display_semi": "InterDisplay-SemiBold.otf",
    "bold": "Inter-Bold.otf",
    "semi": "Inter-SemiBold.otf",
    "medium": "Inter-Medium.otf",
    "regular": "Inter-Regular.otf",
}

# screen window geometry
WX0, WY0, WX1, WY1 = 120, 150, 1800, 900
DW, DH = WX1 - WX0, WY1 - WY0
ASPECT = DW / DH


@lru_cache(maxsize=None)
def font(name, size):
    return ImageFont.truetype(str(FONTS / F[name]), size)


def ease(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def lerp(a, b, t):
    return a + (b - a) * t


def lerp_box(a, b, t):
    return tuple(lerp(p, q, t) for p, q in zip(a, b))


# ----------------------------------------------------------------- helpers
def wrap(text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = f"{cur} {w}".strip()
        if fnt.getlength(test) <= max_w or not cur:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, lines, fnt, cx, top, fill, line_h, align="center", alpha=1.0, x_left=None):
    y = top
    for ln in lines:
        if align == "center":
            draw.text((cx, y), ln, font=fnt, fill=fill + (int(255 * alpha),), anchor="ma")
        else:
            draw.text((x_left, y), ln, font=fnt, fill=fill + (int(255 * alpha),), anchor="la")
        y += line_h
    return y


def vertical_gradient(top, bottom):
    g = Image.new("RGB", (1, H))
    for y in range(H):
        g.putpixel((0, y), tuple(int(lerp(a, b, y / (H - 1))) for a, b in zip(top, bottom)))
    return g.resize((W, H))


@lru_cache(maxsize=None)
def navy_bg():
    bg = vertical_gradient(NAVY, (8, 15, 36)).convert("RGBA")
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([W * 0.15, -H * 0.55, W * 0.85, H * 0.55], fill=NAVY2 + (150,))
    glow = glow.filter(ImageFilter.GaussianBlur(160))
    return Image.alpha_composite(bg, glow)


@lru_cache(maxsize=None)
def light_bg():
    return vertical_gradient((248, 250, 252), (232, 238, 246)).convert("RGBA")


@lru_cache(maxsize=None)
def logo_icon(size):
    s = size * 4
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * 0.24), fill=LOGO_BLUE)

    def hexagon(r, **kw):
        c = s / 2
        pts = [(c + r * math.cos(math.radians(60 * i - 90)), c + r * math.sin(math.radians(60 * i - 90))) for i in range(6)]
        d.polygon(pts, **kw)

    hexagon(s * 0.30, fill=(255, 255, 255, 235))
    hexagon(s * 0.235, fill=LOGO_BLUE)
    hexagon(s * 0.19, fill=ORANGE)
    hexagon(s * 0.13, fill=LOGO_BLUE)
    d.ellipse([s / 2 - s * 0.05, s / 2 - s * 0.05, s / 2 + s * 0.05, s / 2 + s * 0.05], fill=WHITE)
    return im.resize((size, size), Image.LANCZOS)


def draw_logo(canvas, x, y, icon, on_dark, tagline=True, alpha=1.0):
    """Icon + CRAFT ARC wordmark (+ tagline). (x, y) is the icon's top-left."""
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    layer.alpha_composite(logo_icon(icon), (int(x), int(y)))
    d = ImageDraw.Draw(layer)
    size = int(icon * 0.5)
    f = font("bold", size)
    tx = x + icon * 1.28
    ty = y + icon * (0.10 if tagline else 0.24)
    craft_col = WHITE if on_dark else (31, 41, 55)
    spacing = size * 0.16
    cx = tx
    for ch in "CRAFT":
        d.text((cx, ty), ch, font=f, fill=craft_col)
        cx += f.getlength(ch) + spacing
    cx += size * 0.35
    for ch in "ARC":
        d.text((cx, ty), ch, font=f, fill=ORANGE)
        cx += f.getlength(ch) + spacing
    if tagline:
        ft = font("medium", max(int(icon * 0.2), 9))
        tag_col = (148, 163, 184) if on_dark else (100, 116, 139)
        cx2 = tx
        for ch in "AGENTIC LEADERSHIP DEVELOPMENT":
            d.text((cx2, y + icon * 0.66), ch, font=ft, fill=tag_col)
            cx2 += ft.getlength(ch) + icon * 0.045
    if alpha < 1:
        a = layer.getchannel("A").point(lambda v: int(v * alpha))
        layer.putalpha(a)
    canvas.alpha_composite(layer)


# ----------------------------------------------------------------- timeline
TL = json.loads((BUILD / "timeline.json").read_text())
DURATION = TL["duration"]
SENT = {}
for s in TL["sentences"]:
    SENT.setdefault(s["scene"], []).append(s)
SCENE_T = [(sc["start"], sc["end"]) for sc in TL["scenes"]]


def locate(t):
    for si, (a, b) in enumerate(SCENE_T):
        if a <= t < b:
            break
    else:
        si = len(SCENE_T) - 1
    sents = SENT[si]
    ti = 0
    for i, s in enumerate(sents):
        if t >= s["start"] - 0.12:
            ti = i
    return si, ti


# ----------------------------------------------------------------- captions
def draw_caption(canvas, t, si):
    kind = SCENES[si]["kind"]
    if kind in ("kinetic", "logo", "cta"):
        return
    for s in SENT[si]:
        if s["start"] - 0.05 <= t <= s["end"] + 0.15:
            chunks = caption_chunks(s["cap"])
            total = sum(len(" ".join(c)) for c in chunks)
            c0 = s["start"]
            for c in chunks:
                c1 = c0 + (s["end"] - s["start"]) * len(" ".join(c)) / total
                if c0 - 0.05 <= t <= c1 + 0.15:
                    _caption(canvas, c)
                    return
                c0 = c1


def _caption(canvas, lines):
    f = font("semi", 36)
    lw = max(f.getlength(ln) for ln in lines)
    ph = len(lines) * 48 + 26
    pw = lw + 60
    x0, y1 = (W - pw) / 2, 1054
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([x0, y1 - ph, x0 + pw, y1], radius=18, fill=(10, 16, 35, 215))
    y = y1 - ph + 14
    for ln in lines:
        d.text((W / 2, y), ln, font=f, fill=WHITE + (255,), anchor="ma")
        y += 48
    canvas.alpha_composite(layer)


# ----------------------------------------------------------------- kinetic
def render_kinetic(canvas, t, si, ti):
    sc = SCENES[si]
    d = ImageDraw.Draw(canvas)
    for i, s in enumerate(sc["sentences"]):
        st = SENT[si][i]
        nxt = SENT[si][i + 1]["start"] if i + 1 < len(SENT[si]) else SCENE_T[si][1] + 1
        a_in = ease((t - st["start"] + 0.12) / 0.45)
        a_out = 1 - ease((t - nxt + 0.12) / 0.25)
        a = a_in * a_out
        if a <= 0.01:
            continue
        if s.get("logo"):
            reveal_logo(canvas, t - st["start"])
            continue
        big, small, kicker = s.get("big", ""), s.get("small", ""), s.get("kicker", "")
        size = 150 if s.get("accent") else (96 if len(big) < 40 else 80)
        fb = font("display_bold", size)
        lines = wrap(big, fb, 1500)
        lh = int(size * 1.14)
        fs = font("regular", 40)
        slines = wrap(small, fs, 1400) if small else []
        block_h = len(lines) * lh + (len(slines) * 54 + 34 if slines else 0) + (70 if kicker else 0)
        top = 500 - block_h / 2 + (1 - a_in) * 30
        layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        if kicker:
            ld.text((W / 2, top), kicker.upper(), font=font("semi", 30), fill=ORANGE + (int(255 * a),), anchor="ma")
            top += 70
        col = ORANGE if s.get("accent") else WHITE
        y = text_block(ld, lines, fb, W / 2, top, col, lh, alpha=a)
        if slines:
            text_block(ld, slines, fs, W / 2, y + 34, SOFT, 54, alpha=a)
        canvas.alpha_composite(layer)
    del d


def reveal_logo(canvas, dt):
    a = ease(dt / 0.6)
    icon = int(lerp(120, 150, ease(dt / 1.2)))
    total_w = icon * 1.28 + icon * 0.5 * 9.2
    x = (W - total_w) / 2
    draw_logo(canvas, x, 470 - icon / 2, icon, on_dark=True, alpha=a)


# ----------------------------------------------------------------- doc scene
def render_doc(canvas, t, si, ti):
    st = SENT[si]
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    # the one page
    a_page = ease((t - st[0]["start"]) / 0.5)
    px0, py0, pw, ph = 330, 150, 520, 700
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle([px0 + 10, py0 + 24, px0 + pw + 10, py0 + ph + 24], 18, fill=(0, 0, 0, int(120 * a_page)))
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(24)))
    d.rounded_rectangle([px0, py0, px0 + pw, py0 + ph], 18, fill=WHITE + (int(255 * a_page),))
    d.text((px0 + 44, py0 + 50), "What great looks like", font=font("display_bold", 34), fill=INK + (int(255 * a_page),))
    d.text((px0 + 44, py0 + 100), "Senior deal professional", font=font("medium", 22), fill=MUTED + (int(255 * a_page),))
    a_lines = ease((t - st[1]["start"]) / 1.2) if len(st) > 1 else 0
    widths = [0.86, 0.72, 0.9, 0.64, 0.8, 0.7, 0.88, 0.6, 0.76, 0.84, 0.58]
    for i, wf in enumerate(widths):
        k = ease(a_lines * len(widths) - i)
        y = py0 + 170 + i * 44 + (18 if i in (4, 8) else 0)
        x1 = px0 + 44 + (pw - 88) * wf * k
        if k > 0:
            col = (191, 219, 254) if i in (0, 4, 8) else (226, 232, 240)
            d.rounded_rectangle([px0 + 44, y, x1, y + 16], 8, fill=col + (int(255 * a_page),))
    d.text((px0 + pw / 2, py0 + ph + 40), "One page", font=font("semi", 28), fill=SOFT + (int(255 * a_page),), anchor="ma")
    # right side: what the page cannot do, then what the DIY attempt cost
    rx = 1000
    if len(st) > 2 and t >= st[2]["start"] - 0.1:
        third = len(st) > 3 and t >= st[3]["start"] - 0.1
        title = "What the DIY attempt cost" if third else "What a page cannot do"
        items = (["60 to 100 hours of senior time", "About 350 lines of instructions", "No process the firm could run"]
                 if third else ["Interview your people", "Gather the evidence", "Write the review"])
        base = st[3]["start"] if third else st[2]["start"]
        a_t = ease((t - base + 0.1) / 0.4)
        d.text((rx, 250), title.upper(), font=font("semi", 28), fill=ORANGE + (int(255 * a_t),))
        for i, it in enumerate(items):
            k = ease((t - base - 0.25 - i * 0.45) / 0.4)
            if k <= 0:
                continue
            y = 330 + i * 120 + (1 - k) * 20
            cx, cy, r = rx + 30, y + 30, 28
            if third:
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(245, 130, 32, int(60 * k)), outline=ORANGE + (int(255 * k),), width=3)
                d.text((cx, cy), "!", font=font("bold", 32), fill=ORANGE + (int(255 * k),), anchor="mm")
            else:
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(239, 68, 68, int(50 * k)), outline=(248, 113, 113, int(255 * k)), width=3)
                o = 11
                d.line([cx - o, cy - o, cx + o, cy + o], fill=(254, 202, 202, int(255 * k)), width=4)
                d.line([cx - o, cy + o, cx + o, cy - o], fill=(254, 202, 202, int(255 * k)), width=4)
            d.text((rx + 84, cy), it, font=font("display_semi", 44), fill=WHITE + (int(255 * k),), anchor="lm")
    canvas.alpha_composite(layer)


# ----------------------------------------------------------------- screens
@lru_cache(maxsize=None)
def screen(name):
    return Image.open(SCREENS / name).convert("RGB")


def fit_aspect(box, img_size, pad=0.04):
    x0, y0, x1, y1 = box
    w, h = (x1 - x0) * (1 + pad), (y1 - y0) * (1 + pad)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    if w / h < ASPECT:
        w = h * ASPECT
    else:
        h = w / ASPECT
    iw, ih = img_size
    # keep the view inside the image where possible
    if w <= iw:
        cx = min(max(cx, w / 2), iw - w / 2)
    if h <= ih:
        cy = min(max(cy, h / 2), ih - h / 2)
    return (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)


def expand(box, f):
    x0, y0, x1, y1 = box
    cx, cy, w, h = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) * f, (y1 - y0) * f
    return (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)


def view(img, cam):
    return img.transform((DW, DH), Image.EXTENT, cam, resample=Image.BICUBIC, fillcolor=SLATE_BG)


@lru_cache(maxsize=None)
def window_mask():
    m = Image.new("L", (DW, DH), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, DW - 1, DH - 1], 18, fill=255)
    return m


@lru_cache(maxsize=None)
def screen_base(si):
    base = light_bg().copy()
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([WX0 + 4, WY0 + 18, WX1 + 4, WY1 + 22], 22, fill=(15, 23, 42, 70))
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(26)))
    draw_logo(base, WX0, 40, 46, on_dark=False, tagline=False)
    sc = SCENES[si]
    d = ImageDraw.Draw(base)
    d.line([WX0 + 300, 42, WX0 + 300, 86], fill=SOFT, width=2)
    d.text((WX0 + 326, 64), sc["label"], font=font("display_bold", 34), fill=INK, anchor="lm")
    step = sc.get("step")
    # step rail
    rx0, rx1, ry = 1010, 1780, 62
    xs = [lerp(rx0, rx1, i / (len(STEPS) - 1)) for i in range(len(STEPS))]
    d.line([xs[0], ry, xs[-1], ry], fill=SOFT, width=3)
    if step is not None:
        d.line([xs[0], ry, xs[step], ry], fill=BLUE, width=3)
    for i, x in enumerate(xs):
        if step is not None and i < step:
            d.ellipse([x - 9, ry - 9, x + 9, ry + 9], fill=BLUE)
        elif step is not None and i == step:
            d.ellipse([x - 15, ry - 15, x + 15, ry + 15], fill=(219, 234, 254))
            d.ellipse([x - 10, ry - 10, x + 10, ry + 10], fill=BLUE)
        else:
            d.ellipse([x - 9, ry - 9, x + 9, ry + 9], fill=WHITE, outline=SOFT, width=3)
        col = INK if step == i else MUTED
        d.text((x, ry + 26), STEPS[i], font=font("semi" if step == i else "medium", 17), fill=col, anchor="ma")
    return base


def scene_cams(si):
    sc = SCENES[si]
    cams = []
    for s in sc["sentences"]:
        img = screen(s["img"])
        cams.append(fit_aspect(s["focus"], img.size, s.get("pad", 0.04)))
    return cams


def cam_at(si, ti, t):
    sc, st = SCENES[si], SENT[si]
    cams = scene_cams(si)
    s = sc["sentences"][ti]
    start = st[ti]["start"]
    same_img = ti > 0 and sc["sentences"][ti - 1]["img"] == s["img"]
    drift = expand(cams[ti], 1 - 0.025 * ease((t - start) / max(st[ti]["end"] - start, 1)))
    if ti == 0 or not same_img:
        k = ease((t - (SCENE_T[si][0] if ti == 0 else start - 0.15)) / 1.3)
        return lerp_box(expand(cams[ti], 1.10), drift, k)
    k = ease((t - start + 0.15) / 0.9)
    prev_end = expand(cams[ti - 1], 1 - 0.025)
    return lerp_box(prev_end, drift, k)


def to_display(box, cam):
    sx, sy = DW / (cam[2] - cam[0]), DH / (cam[3] - cam[1])
    return ((box[0] - cam[0]) * sx, (box[1] - cam[1]) * sy, (box[2] - cam[0]) * sx, (box[3] - cam[1]) * sy)


def render_window(si, ti, t):
    s = SCENES[si]["sentences"][ti]
    cam = cam_at(si, ti, t)
    win = view(screen(s["img"]), cam).convert("RGBA")
    st = SENT[si][ti]
    nxt = SENT[si][ti + 1]["start"] if ti + 1 < len(SENT[si]) else SCENE_T[si][1] + 1
    a = ease((t - st["start"] - 0.55) / 0.35) * (1 - ease((t - nxt + 0.25) / 0.2))
    chip_pos = None
    if a > 0.01 and s.get("hl"):
        dim = Image.new("L", (DW, DH), int(80 * a))
        md = ImageDraw.Draw(dim)
        boxes = [to_display(b, cam) for b in s["hl"]]
        for b in boxes:
            md.rounded_rectangle([b[0] - 8, b[1] - 8, b[2] + 8, b[3] + 8], 14, fill=0)
        shade = Image.new("RGBA", (DW, DH), (15, 23, 42, 255))
        shade.putalpha(dim)
        win.alpha_composite(shade)
        od = ImageDraw.Draw(win)
        for b in boxes:
            od.rounded_rectangle([b[0] - 8, b[1] - 8, b[2] + 8, b[3] + 8], 14, outline=BLUE + (int(255 * a),), width=5)
        chip_pos = boxes[0]
    return win, a, chip_pos


def draw_chip(canvas, text, box, a, below=False):
    f = font("semi", 30)
    tw = f.getlength(text)
    pw, ph = tw + 44, 54
    x = WX0 + box[0] - 8
    y = WY0 + box[1] - 8 - ph - 12
    if below or y < WY0 + 8:
        y = WY0 + box[3] + 8 + 14
    if y + ph > WY1 - 8:
        y = WY0 + box[1] + 8
        x = WX0 + box[0] + 8
    x = min(max(x, WX0 + 12), WX1 - pw - 12)
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([x, y + (1 - a) * 10, x + pw, y + ph + (1 - a) * 10], 27, fill=BLUE + (int(255 * a),))
    d.text((x + pw / 2, y + ph / 2 + (1 - a) * 10), text, font=f, fill=WHITE + (int(255 * a),), anchor="mm")
    canvas.alpha_composite(layer)


def render_screen(canvas, t, si, ti):
    canvas.alpha_composite(screen_base(si))
    sc = SCENES[si]
    win, a, chip_box = render_window(si, ti, t)
    st = SENT[si][ti]
    if ti > 0 and sc["sentences"][ti - 1]["img"] != sc["sentences"][ti]["img"]:
        k = ease((t - st["start"] + 0.2) / 0.45)
        if k < 1:
            prev, _, _ = render_window(si, ti - 1, st["start"] - 0.2)
            win = Image.blend(prev, win, k)
    canvas.paste(win, (WX0, WY0), window_mask())
    if chip_box is not None and a > 0.01:
        draw_chip(canvas, sc["sentences"][ti]["chip"], chip_box, a, below=sc["sentences"][ti].get("chip_below", False))
    if sc["sentences"][ti].get("overlay") == "grades":
        draw_grades(canvas, t, si, ti)


def draw_grades(canvas, t, si, ti):
    """A designed card (not product UI) naming the three evidence grades."""
    st = SENT[si][ti]
    nxt = SENT[si][ti + 1]["start"] if ti + 1 < len(SENT[si]) else SCENE_T[si][1] + 1
    a = ease((t - st["start"] - 0.2) / 0.35) * (1 - ease((t - nxt + 0.25) / 0.2))
    if a <= 0.01:
        return
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([WX0, WY0, WX1, WY1], 18, fill=(15, 23, 42, int(150 * a)))
    cw, ch = 1160, 330
    x0, y0 = (W - cw) / 2, (WY0 + WY1) / 2 - ch / 2 + (1 - a) * 16
    d.rounded_rectangle([x0, y0, x0 + cw, y0 + ch], 24, fill=(255, 255, 255, int(255 * a)))
    d.text((W / 2, y0 + 56), "EVERY FACT CARRIES ITS SOURCE", font=font("semi", 26), fill=ORANGE + (int(255 * a),), anchor="ma")
    f = font("display_semi", 40)
    widths = [f.getlength(g) + 120 for g, _ in GRADES]
    gap = 28
    x = (W - (sum(widths) + gap * (len(GRADES) - 1))) / 2
    for i, (g, col) in enumerate(GRADES):
        k = ease((t - st["start"] - 0.45 - i * 0.3) / 0.35) * a
        yy = y0 + 140
        tint = tuple(int(255 - (255 - c) * 0.16) for c in col)  # opaque pale tint, so nothing shows through
        d.rounded_rectangle([x, yy, x + widths[i], yy + 92], 46, fill=tint + (int(255 * k),), outline=col + (int(255 * k),), width=3)
        d.ellipse([x + 32, yy + 34, x + 56, yy + 58], fill=col + (int(255 * k),))
        d.text((x + 76, yy + 46), g, font=f, fill=INK + (int(255 * k),), anchor="lm")
        x += widths[i] + gap
    d.text((W / 2, y0 + 270), "How each fact in an interview is graded", font=font("regular", 26), fill=MUTED + (int(255 * a),), anchor="ma")
    canvas.alpha_composite(layer)


# ----------------------------------------------------------------- proof
def render_proof(canvas, t, si, ti):
    head = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(head)
    a0 = ease((t - SCENE_T[si][0]) / 0.5)
    d.text((W / 2, 150), "PROOF", font=font("semi", 30), fill=ORANGE + (int(255 * a0),), anchor="ma")
    d.text((W / 2, 200), "Live with a private equity senior deal team", font=font("display_bold", 64),
           fill=WHITE + (int(255 * a0),), anchor="ma")
    canvas.alpha_composite(head)
    cw, chh, gap = 540, 380, 40
    x0 = (W - (3 * cw + 2 * gap)) / 2
    for i, (kicker, title, sub) in enumerate(PROOF_CARDS):
        st = SENT[si][i]["start"]
        k = ease((t - st + 0.1) / 0.5)
        if k <= 0:
            continue
        x, y = x0 + i * (cw + gap), 360 + (1 - k) * 30
        layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.rounded_rectangle([x, y, x + cw, y + chh], 22, fill=(255, 255, 255, int(16 * k)),
                             outline=(255, 255, 255, int(60 * k)), width=2)
        ld.text((x + 40, y + 44), kicker.upper(), font=font("semi", 24), fill=ORANGE + (int(255 * k),))
        yy = y + 96
        for ln in wrap(title, font("display_semi", 38), cw - 80):
            ld.text((x + 40, yy), ln, font=font("display_semi", 38), fill=WHITE + (int(255 * k),))
            yy += 48
        yy += 18
        for ln in wrap(sub, font("regular", 27), cw - 80):
            ld.text((x + 40, yy), ln, font=font("regular", 27), fill=SOFT + (int(255 * k),))
            yy += 38
        canvas.alpha_composite(layer)


# ----------------------------------------------------------------- offer
def render_offer(canvas, t, si, ti):
    canvas.alpha_composite(light_bg())
    a0 = ease((t - SCENE_T[si][0]) / 0.5)
    draw_logo(canvas, 160, 70, 50, on_dark=False, tagline=False)
    head = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(head)
    d.text((160, 220), "HOW FIRMS START", font=font("semi", 30), fill=ORANGE + (int(255 * a0),))
    d.text((160, 262), "Low disruption, and a way out if we miss", font=font("display_bold", 60), fill=INK + (int(255 * a0),))
    canvas.alpha_composite(head)
    for i, (title, sub) in enumerate(OFFER_ITEMS):
        st = SENT[si][i]["start"]
        k = ease((t - st + 0.1) / 0.45)
        if k <= 0:
            continue
        y = 410 + i * 170 + (1 - k) * 20
        layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.rounded_rectangle([160, y, 1760, y + 140], 20, fill=(255, 255, 255, int(255 * k)), outline=(226, 232, 240, int(255 * k)), width=2)
        col = ORANGE if i == 2 else BLUE
        cx, cy = 230, y + 70
        ld.ellipse([cx - 32, cy - 32, cx + 32, cy + 32], fill=col + (int(255 * k),))
        ld.line([(cx - 13, cy + 1), (cx - 3, cy + 11), (cx + 15, cy - 11)], fill=WHITE + (int(255 * k),), width=6, joint="curve")
        ld.text((300, y + 34), title, font=font("display_bold", 40), fill=INK + (int(255 * k),))
        ld.text((300, y + 88), sub, font=font("regular", 29), fill=(71, 85, 105, int(255 * k)))
        canvas.alpha_composite(layer)


# ----------------------------------------------------------------- cta
def render_cta(canvas, t, si, ti):
    st = SENT[si]
    a1 = ease((t - st[1]["start"] + 0.1) / 0.5) if len(st) > 1 else 0
    # first line: the timing message, large, then it gives way to the call to action
    a_intro = ease((t - SCENE_T[si][0]) / 0.5) * (1 - a1)
    if a_intro > 0.01:
        intro = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        di = ImageDraw.Draw(intro)
        di.text((W / 2, 400), CTA["intro"][0], font=font("display_semi", 56), fill=SOFT + (int(255 * a_intro),), anchor="ma")
        di.text((W / 2, 490), CTA["intro"][1], font=font("display_bold", 120), fill=ORANGE + (int(255 * a_intro),), anchor="ma")
        canvas.alpha_composite(intro)
    a0 = a1
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.text((W / 2, 250), "PLAN NEXT YEAR'S CYCLE NOW", font=font("semi", 32), fill=ORANGE + (int(255 * a0),), anchor="ma")
    d.text((W / 2, 330), CTA["title"], font=font("display_bold", 128), fill=WHITE + (int(255 * max(a1, 0.0)),), anchor="ma")
    for i, ln in enumerate(wrap(CTA["sub"], font("regular", 40), 1300)):
        d.text((W / 2, 500 + i * 56), ln, font=font("regular", 40), fill=SOFT + (int(255 * a1),), anchor="ma")
    canvas.alpha_composite(layer)
    draw_logo(canvas, (W - 520) / 2, 650, 80, on_dark=True, tagline=True, alpha=a1)
    if CTA.get("url"):
        url = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        ImageDraw.Draw(url).text((W / 2, 790), CTA["url"], font=font("semi", 40), fill=WHITE + (int(255 * a1),), anchor="ma")
        canvas.alpha_composite(url)
    a2 = ease((t - st[2]["start"] + 0.1) / 0.4) if len(st) > 2 else 0
    fine = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(fine).text((W / 2, 880), CTA["fine"], font=font("regular", 26), fill=(148, 163, 184, int(255 * a2)), anchor="ma")
    canvas.alpha_composite(fine)


RENDER = {"kinetic": render_kinetic, "logo": render_kinetic, "doc": render_doc, "screen": render_screen,
          "proof": render_proof, "offer": render_offer, "cta": render_cta}


DARK = ("kinetic", "logo", "doc", "proof", "cta")


def push_in(canvas, z):
    """Slow camera push-in, so text scenes never sit perfectly still."""
    if z <= 1.0001:
        return canvas
    w, h = W / z, H / z
    box = ((W - w) / 2, (H - h) / 2, (W + w) / 2, (H + h) / 2)
    return canvas.transform((W, H), Image.EXTENT, box, resample=Image.BILINEAR)


def compose(si, t):
    kind = SCENES[si]["kind"]
    _, ti = locate(t)
    ti = min(ti, len(SENT[si]) - 1)
    canvas = navy_bg().copy() if kind in DARK else light_bg().copy()
    RENDER[kind](canvas, t, si, ti)
    if kind != "screen":  # screen scenes already move with their own camera
        a, b = SCENE_T[si]
        canvas = push_in(canvas, 1 + 0.04 * min(max((t - a) / (b - a), 0), 1))
    return canvas


def frame(t):
    si, _ = locate(t)
    canvas = compose(si, t)
    a, _ = SCENE_T[si]
    if si > 0 and t - a < 0.3:  # cross-fade from the previous scene's last frame
        canvas = Image.blend(compose(si - 1, a - 0.001), canvas, ease((t - a) / 0.3))
    draw_caption(canvas, t, si)
    return canvas


def stills():
    out = BUILD / "stills"
    out.mkdir(parents=True, exist_ok=True)
    paths = []
    for s in TL["sentences"]:
        t = min(s["end"] - 0.2, s["start"] + 1.6)
        p = out / f"s{s['scene']:02d}_{s['idx']:02d}.png"
        frame(t).convert("RGB").save(p)
        paths.append(p)
    # contact sheet
    th = [Image.open(p).resize((480, 270), Image.LANCZOS) for p in paths]
    cols = 4
    rows = math.ceil(len(th) / cols)
    sheet = Image.new("RGB", (cols * 490 + 10, rows * 280 + 10), (40, 40, 40))
    for i, im in enumerate(th):
        sheet.paste(im, (10 + (i % cols) * 490, 10 + (i // cols) * 280))
    sheet.save(BUILD / "contact_sheet.png")
    print(f"{len(paths)} stills, contact sheet at {BUILD / 'contact_sheet.png'}")


def render(web=False, t0=0.0, t1=None):
    t1 = DURATION if t1 is None else t1
    excerpt = t0 > 0 or t1 < DURATION
    out = BUILD / ("excerpt.mp4" if excerpt else "CraftArc_VSL_1080p.mp4")
    n = int(math.ceil((t1 - t0) * FPS))
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-ss", f"{t0:.3f}", "-i", str(BUILD / "vo.wav"),
           "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000",
           "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-tune", "stillimage",
           "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-shortest", str(out)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(frame(t0 + i / FPS).convert("RGB").tobytes())
        if i % 300 == 0:
            print(f"frame {i}/{n}", flush=True)
    p.stdin.close()
    if p.wait() != 0:
        raise SystemExit("ffmpeg failed")
    print("wrote", out)
    if web and not excerpt:
        web_out = BUILD / "CraftArc_VSL_720p.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(out), "-vf", "scale=1280:720:flags=lanczos",
                        "-c:v", "libx264", "-preset", "slow", "-crf", "26", "-pix_fmt", "yuv420p", "-c:a", "aac",
                        "-b:a", "128k", "-movflags", "+faststart", str(web_out)], check=True)
        poster_t = TL["scenes"][0]["start"] + 3.0
        frame(poster_t).convert("RGB").resize((1280, 720), Image.LANCZOS).save(BUILD / "poster.jpg", quality=88)
        print("wrote", web_out, "and poster.jpg")


if __name__ == "__main__":
    if "--stills" in sys.argv:
        stills()
    elif "--range" in sys.argv:  # QA excerpt: --range 100 120
        i = sys.argv.index("--range")
        render(t0=float(sys.argv[i + 1]), t1=float(sys.argv[i + 2]))
    else:
        render(web="--web" in sys.argv)
