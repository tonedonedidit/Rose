#!/usr/bin/env python3
"""Render a faceless Short from a JSON spec: free local voice + motion-graphic scenes + captions.

    python3 studio/tools/render.py studio/specs/<id>.json [--out studio/output/<id>.mp4] [--check]

Voice: Kokoro-82M (Apache-2.0) via kokoro-onnx, runs locally, $0.
Visuals: procedural motion graphics drawn with Pillow (no stock, no licences needed).
Music: an original low drone synthesised with ffmpeg (no copyright claims).
Setup (once): python3 studio/tools/setup_assets.py
Spec format: see studio/tools/SPEC.md
"""
import argparse
import json
import math
import os
import random
import re
import subprocess
import sys
import tempfile

import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
ASSETS = os.environ.get("STUDIO_ASSETS", os.path.expanduser("~/.cache/studio-tts"))
FONT = {
    "serif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "sans": "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf",
    "sans_mid": "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf",
    "mono": "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf",
}
_font_cache = {}


def font(kind, size):
    key = (kind, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(FONT[kind], size)
    return _font_cache[key]


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def ease_out(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3


def seg(p, a, b):
    """Progress of p inside window [a, b], clamped 0..1."""
    return min(max((p - a) / max(b - a, 1e-6), 0.0), 1.0)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_center(draw, y, text, fnt, fill, max_w=900, spacing=1.15, stroke=0, stroke_fill=(0, 0, 0)):
    lines = wrap(draw, text, fnt, max_w)
    lh = fnt.size * spacing
    for i, ln in enumerate(lines):
        tw = draw.textlength(ln, font=fnt)
        draw.text(((W - tw) / 2, y + i * lh), ln, font=fnt, fill=fill,
                  stroke_width=stroke, stroke_fill=stroke_fill)
    return y + len(lines) * lh


# ---------------------------------------------------------------- voice

def split_sentences(text):
    parts = re.split(r"(?<=[.!?:])\s+", text.strip())
    return [p for p in parts if p]


def synth(spec, scenes, tmp):
    from kokoro_onnx import Kokoro
    k = Kokoro(os.path.join(ASSETS, "kokoro-v1.0.onnx"), os.path.join(ASSETS, "voices-v1.0.bin"))
    voice, speed = spec.get("voice", "am_michael"), spec.get("speed", 0.95)
    sr = 24000
    gap = np.zeros(int(sr * spec.get("sentence_gap", 0.12)), dtype=np.float32)
    audio, words, t = [], [], 0.0
    for sc in scenes:
        sc["start"] = t
        for sent in split_sentences(sc["say"]):
            a, sr = k.create(sent, voice=voice, speed=speed, lang=spec.get("lang", "en-us"))
            a = a.astype(np.float32)
            # trim leading/trailing silence so word timing estimates line up
            nz = np.where(np.abs(a) > 0.01)[0]
            if len(nz):
                a = a[max(nz[0] - 600, 0):nz[-1] + 1200]
            dur = len(a) / sr
            toks = sent.split()
            weights = [len(re.sub(r"\W", "", w)) + 2 + (4 if re.search(r"[,.;:!?]$", w) else 0) for w in toks]
            tot, acc = sum(weights), 0.0
            for w, wt in zip(toks, weights):
                ws = t + dur * acc / tot
                acc += wt
                words.append({"w": w, "s": ws, "e": t + dur * acc / tot, "sent_end": False})
            words[-1]["sent_end"] = True
            audio += [a, gap]
            t += dur + len(gap) / sr
        pad = sc.get("pad", 0.25)
        audio.append(np.zeros(int(sr * pad), dtype=np.float32))
        t += pad
        sc["end"] = t
    wav = np.concatenate(audio)
    path = os.path.join(tmp, "voice.wav")
    sf.write(path, wav, sr)
    return path, words, t


# ---------------------------------------------------------------- scenes
# each: fn(img, draw, p, sc, accent) where p = 0..1 progress through the scene

def bg_spot(img, cx, cy, r, color=(60, 52, 44), strength=1.0):
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).ellipse([cx - r, cy - r, cx + r, cy + r], fill=int(255 * strength))
    mask = mask.filter(ImageFilter.GaussianBlur(r * 0.45))
    img.paste(Image.new("RGB", (W, H), color), (0, 0), mask)


def s_title(img, d, p, sc, ac):
    bg_spot(img, W // 2, H // 2 - 150, 520, (40, 36, 32))
    txt = sc.get("text", "")
    n = int(len(txt) * ease_out(seg(p, 0.0, 0.55)))
    y = text_center(d, 640, txt[:n], font("serif", 92), (238, 232, 220), max_w=920)
    if sc.get("sub"):
        a = int(255 * seg(p, 0.45, 0.65))
        text_center(d, max(y, 1000) + 30, sc["sub"], font("mono", 54), ac + (a,))


def s_black(img, d, p, sc, ac):
    img.paste((0, 0, 0), (0, 0, W, H))
    a = int(255 * seg(p, 0.05, 0.25))
    text_center(d, 760, sc.get("text", ""), font("serif", 84), ac + (a,), max_w=900)


def s_silhouette(img, d, p, sc, ac):
    flick = 0.85 + 0.15 * math.sin(p * 40) * (1 if random.random() > 0.9 else 0.3)
    bg_spot(img, W // 2, 820, 560, (70, 62, 52), flick)
    cx, top = W // 2, 430
    # hood + shoulders
    d.ellipse([cx - 210, top, cx + 210, top + 470], fill=(14, 13, 12))
    d.polygon([(cx - 420, 1420), (cx - 260, 900), (cx + 260, 900), (cx + 420, 1420)], fill=(14, 13, 12))
    d.ellipse([cx - 120, top + 150, cx + 120, top + 400], fill=(4, 4, 4))
    # sunglasses glint
    d.rectangle([cx - 95, top + 245, cx - 15, top + 280], fill=(30, 30, 30))
    d.rectangle([cx + 15, top + 245, cx + 95, top + 280], fill=(30, 30, 30))
    a = int(255 * seg(p, 0.2, 0.45))
    if sc.get("label"):
        lbl = sc["label"]
        f = font("mono", 50)
        tw = d.textlength(lbl, font=f)
        d.rectangle([(W - tw) / 2 - 24, 1470, (W + tw) / 2 + 24, 1550], outline=ac + (a,), width=4)
        d.text(((W - tw) / 2, 1482), lbl, font=f, fill=ac + (a,))
    if sc.get("sub"):
        text_center(d, 1585, sc["sub"], font("mono", 40), (200, 190, 175, a))


def s_counter(img, d, p, sc, ac):
    bg_spot(img, W // 2, 700, 500, (36, 32, 28))
    n = int(sc.get("number", 0))
    shown = round(n * ease_out(seg(p, 0.05, 0.45)))
    f = font("sans", 300)
    s = str(shown)
    d.text(((W - d.textlength(s, font=f)) / 2, 300), s, font=f, fill=ac)
    text_center(d, 640, sc.get("label", ""), font("mono", 58), (230, 222, 210))
    # grid of n marks appearing in sequence
    cols = 4 if n <= 16 else 8
    sz, gapx = 120, 40
    gw = cols * sz + (cols - 1) * gapx
    x0, y0 = (W - gw) // 2, 800
    marked = set(sc.get("marked", []))
    for i in range(n):
        if seg(p, 0.05 + 0.4 * i / max(n, 1), 0.1 + 0.4 * i / max(n, 1)) <= 0:
            continue
        r, c = divmod(i, cols)
        x, y = x0 + c * (sz + gapx), y0 + r * (sz + gapx)
        col = (200, 60, 50) if (i + 1) in marked and p > 0.55 else (70, 64, 56)
        d.rectangle([x, y, x + sz, y + sz], outline=ac, width=4, fill=col)
    if sc.get("second"):
        a = int(255 * seg(p, 0.55, 0.7))
        text_center(d, 1500, sc["second"], font("sans", 84), (220, 70, 60, a))


def paper(d, box, color=(226, 218, 200), lines=14, seed=1, highlight=(), hl_p=0.0, ac=(232, 163, 61)):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=color)
    rnd = random.Random(seed)
    lh = (y1 - y0 - 120) / max(lines, 1)
    for i in range(lines):
        y = y0 + 80 + i * lh
        w = (x1 - x0 - 100) * rnd.uniform(0.55, 0.98)
        if i in highlight and hl_p > 0:
            d.rectangle([x0 + 44, y - 8, x0 + 50 + w * hl_p, y + 22], fill=ac)
        d.rectangle([x0 + 50, y, x0 + 50 + w, y + 14], fill=(70, 64, 56))


def s_newspaper(img, d, p, sc, ac):
    bg_spot(img, W // 2, 900, 600, (40, 36, 32))
    sc_e = 0.75 + 0.25 * ease_out(seg(p, 0, 0.3))
    pw, ph = int(760 * sc_e), int(980 * sc_e)
    layer = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rectangle([0, 0, pw, ph], fill=(232, 226, 212))
    mf = font("serif", int(70 * sc_e))
    mast = sc.get("masthead", "THE DAILY PAPER")
    ld.text(((pw - ld.textlength(mast, font=mf)) / 2, 30 * sc_e), mast, font=mf, fill=(20, 20, 20))
    ld.line([30, 120 * sc_e, pw - 30, 120 * sc_e], fill=(20, 20, 20), width=4)
    if sc.get("date"):
        df = font("mono", int(30 * sc_e))
        ld.text((40 * sc_e, 132 * sc_e), sc["date"], font=df, fill=(40, 40, 40))
    rnd = random.Random(3)
    for col in range(3):
        cx = 40 * sc_e + col * (pw - 60 * sc_e) / 3
        for i in range(30):
            y = 200 * sc_e + i * 28 * sc_e
            ld.rectangle([cx, y, cx + (pw / 3 - 50 * sc_e) * rnd.uniform(0.7, 1), y + 10 * sc_e], fill=(90, 86, 80))
    layer = layer.rotate(-4 + 4 * ease_out(seg(p, 0, 0.3)), expand=True, resample=Image.BICUBIC)
    img.paste(layer, ((W - layer.width) // 2, 380 - (layer.height - ph) // 2), layer)
    if sc.get("stamp"):
        a = seg(p, 0.35, 0.45)
        if a > 0:
            f = font("sans", int(120 - 30 * a))
            s = sc["stamp"]
            tw = d.textlength(s, font=f)
            d.rectangle([(W - tw) / 2 - 30, 1400, (W + tw) / 2 + 30, 1420 + f.size + 20], fill=(10, 10, 10))
            d.text(((W - tw) / 2, 1410), s, font=f, fill=ac)


def s_date(img, d, p, sc, ac):
    bg_spot(img, W // 2, 760, 520, (38, 34, 30))
    a = seg(p, 0, 0.12)
    size = int(170 * (1.5 - 0.5 * ease_out(a)))
    f = font("serif", size)
    s = sc.get("date", "")
    lines = wrap(d, s, f, 980)
    y = 620
    for ln in lines:
        d.text(((W - d.textlength(ln, font=f)) / 2, y), ln, font=f, fill=ac + (int(255 * a),))
        y += size * 1.1
    if sc.get("label"):
        text_center(d, y + 40, sc["label"], font("mono", 54), (225, 218, 205, int(255 * seg(p, 0.15, 0.3))))


def s_name(img, d, p, sc, ac):
    bg_spot(img, W // 2, 760, 480, (44, 40, 34))
    cx = W // 2
    d.ellipse([cx - 140, 360, cx + 140, 640], fill=(16, 15, 14))
    d.pieslice([cx - 300, 640, cx + 300, 1180], 180, 360, fill=(16, 15, 14))
    a = int(255 * seg(p, 0.1, 0.3))
    text_center(d, 1000, sc.get("name", ""), font("serif", 96), (240, 234, 222, a))
    if sc.get("role"):
        text_center(d, 1130, sc["role"], font("mono", 52), ac + (a,))


def s_compare(img, d, p, sc, ac):
    bg_spot(img, W // 2, 820, 560, (38, 34, 30))
    hl = sc.get("highlight", [2, 5, 9])
    hp = ease_out(seg(p, 0.3, 0.75))
    paper(d, (70, 420, 520, 1260), (214, 204, 180), seed=4, highlight=hl, hl_p=hp, ac=ac)
    paper(d, (560, 420, 1010, 1260), (232, 226, 212), seed=9, highlight=hl, hl_p=hp, ac=ac)
    lf = font("mono", 40)
    for x, lbl in ((70, sc.get("left", "LETTERS")), (560, sc.get("right", "MANIFESTO"))):
        d.text((x, 350), lbl, font=lf, fill=(220, 212, 198))
    if p > 0.75:
        a = int(255 * seg(p, 0.75, 0.85))
        text_center(d, 1340, sc.get("verdict", "MATCH"), font("sans", 110), ac + (a,))


_STATES = None


def load_states():
    global _STATES
    if _STATES is None:
        with open(os.path.join(ASSETS, "states.geojson")) as fh:
            gj = json.load(fh)
        _STATES = []
        for f in gj["features"]:
            if f["properties"].get("iso_a2") != "US" or f["properties"].get("name") in ("Alaska", "Hawaii"):
                continue
            g = f["geometry"]
            polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
            for poly in polys:
                _STATES.append(poly[0])
    return _STATES


def proj(lon, lat, zoom=1.0, center=(-98.5, 39.5)):
    k = 14.8 * zoom
    x = W / 2 + (lon - center[0]) * k * math.cos(math.radians(39.5))
    y = 820 - (lat - center[1]) * k
    return x, y


def s_map(img, d, p, sc, ac):
    zoom = 1.0 + (sc.get("zoom", 1.6) - 1.0) * ease_out(seg(p, 0.1, 0.7))
    lat, lon = sc["lat"], sc["lon"]
    center = (-98.5 + (lon + 98.5) * ease_out(seg(p, 0.1, 0.7)), 39.5 + (lat - 39.5) * ease_out(seg(p, 0.1, 0.7)))
    for ring in load_states():
        pts = [proj(x, y, zoom, center) for x, y in ring]
        d.polygon(pts, fill=(30, 28, 25), outline=(95, 88, 78))
    px, py = proj(lon, lat, zoom, center)
    drop = ease_out(seg(p, 0.55, 0.7))
    if drop > 0:
        py2 = py - 200 * (1 - drop)
        d.ellipse([px - 26, py2 - 90, px + 26, py2 - 38], fill=ac)
        d.polygon([(px - 22, py2 - 58), (px + 22, py2 - 58), (px, py2)], fill=ac)
        r = 30 + 60 * seg(p, 0.7, 1.0)
        d.ellipse([px - r, py - r / 3, px + r, py + r / 3], outline=ac + (int(255 * (1 - seg(p, 0.7, 1.0))),), width=3)
        text_center(d, 1350, sc.get("label", ""), font("sans", 76), (240, 234, 222, int(255 * seg(p, 0.6, 0.75))))
        if sc.get("sub"):
            text_center(d, 1450, sc["sub"], font("mono", 50), ac + (int(255 * seg(p, 0.65, 0.8)),))


def s_cabin(img, d, p, sc, ac):
    for i in range(0, H, 8):  # night sky gradient
        c = int(10 + 18 * i / H)
        d.rectangle([0, i, W, i + 8], fill=(c, c + 2, c + 8))
    d.ellipse([760, 260, 900, 400], fill=(220, 214, 196))
    rnd = random.Random(7)
    for layer, (col, base, drift) in enumerate((((22, 26, 26), 1150, 30), ((14, 17, 17), 1300, 60), ((8, 10, 10), 1450, 100))):
        off = -drift * p
        for i in range(14):
            x = -100 + i * 95 + rnd.uniform(-20, 20) + off
            h = rnd.uniform(260, 520)
            d.polygon([(x, base), (x + 70, base - h), (x + 140, base)], fill=col)
        d.rectangle([0, base, W, H], fill=col)
    # cabin in a clearing, in front of the tree layers
    cx = 400 - 40 * p
    glow = 170 + int(50 * math.sin(p * 9))
    bg_spot(img, int(cx + 160), 1400, 170, (60, 45, 20), 0.8)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([cx, 1330, cx + 280, 1460], fill=(4, 5, 5))
    d.polygon([(cx - 40, 1336), (cx + 140, 1210), (cx + 320, 1336)], fill=(4, 5, 5))
    d.rectangle([cx + 180, 1365, cx + 235, 1415], fill=(glow, int(glow * 0.7), 40))
    d.rectangle([0, 1460, W, H], fill=(8, 10, 10))
    if sc.get("label"):
        text_center(d, 1520, sc["label"], font("mono", 46), ac + (int(255 * seg(p, 0.15, 0.3)),), max_w=1000)


def s_verdict(img, d, p, sc, ac):
    bg_spot(img, W // 2, 760, 520, (40, 36, 32))
    a = seg(p, 0.05, 0.14)
    if a > 0:
        size = int(118 * (1.6 - 0.6 * ease_out(a)))
        f = font("sans", size)
        s = sc.get("stamp", "GUILTY")
        tw = d.textlength(s, font=f)
        layer = Image.new("RGBA", (int(tw) + 80, size + 80), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.rectangle([4, 4, layer.width - 4, layer.height - 4], outline=(200, 50, 45), width=10)
        ld.text((40, 30), s, font=f, fill=(200, 50, 45))
        layer = layer.rotate(-8, expand=True, resample=Image.BICUBIC)
        img.paste(layer, ((W - layer.width) // 2, 640 - layer.height // 2), layer)
    y = 900
    for i, ln in enumerate(sc.get("lines", [])):
        y = text_center(d, y, ln, font("mono", 58), (230, 222, 210, int(255 * seg(p, 0.3 + 0.12 * i, 0.4 + 0.12 * i)))) + 20


def s_ink(img, d, p, sc, ac):
    paper(d, (90, 300, 990, 1500), (214, 204, 180), lines=0)
    rnd = random.Random(11)
    prog = ease_out(seg(p, 0.0, 0.7))
    rows = 16
    for r in range(rows):
        if r / rows > prog:
            break
        y = 380 + r * 68
        part = min(1.0, (prog - r / rows) * rows)
        x_end = 150 + (760 * rnd.uniform(0.6, 1.0)) * part
        pts = [(x, y + 8 * math.sin(x / 13 + r)) for x in range(150, int(x_end), 6)]
        if len(pts) > 1:
            d.line(pts, fill=(35, 30, 60), width=5)
    fade = seg(p, 0.82, 1.0)
    if fade > 0:
        d.rectangle([0, 0, W, H], fill=(0, 0, 0, int(255 * fade)))


SCENES = {"title": s_title, "black": s_black, "silhouette": s_silhouette, "counter": s_counter,
          "newspaper": s_newspaper, "date": s_date, "name": s_name, "compare": s_compare,
          "map": s_map, "cabin": s_cabin, "verdict": s_verdict, "ink": s_ink}


# ---------------------------------------------------------------- captions + finishing

def caption_chunks(words, max_words=3):
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) >= max_words or w["sent_end"] or re.search(r"[,;:]$", w["w"]):
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    return chunks


def draw_captions(d, t, chunks, ac):
    for ch in chunks:
        if ch[0]["s"] - 0.05 <= t < ch[-1]["e"] + 0.12:
            f = font("sans", 84)
            words = [w["w"].upper() for w in ch]
            space = d.textlength(" ", font=f)
            widths = [d.textlength(w, font=f) for w in words]
            total = sum(widths) + space * (len(words) - 1)
            if total > 980:
                f = font("sans", int(84 * 980 / total))
                widths = [d.textlength(w, font=f) for w in words]
                space = d.textlength(" ", font=f)
                total = sum(widths) + space * (len(words) - 1)
            x = (W - total) / 2
            for wd, wobj, wt in zip(words, ch, widths):
                active = wobj["s"] <= t < wobj["e"] + 0.05
                d.text((x, 1660), wd, font=f, fill=ac if active else (255, 255, 255),
                       stroke_width=7, stroke_fill=(0, 0, 0))
                x += wt + space
            return


def make_vignette():
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    return np.clip(1.15 - 0.55 * r ** 1.6, 0.35, 1.0)[..., None].astype(np.float32)


def music_bed(path, dur):
    # original drone: two low sines + filtered noise, slow swell; no samples, no copyright
    filt = (f"sine=f=55:d={dur}[a];sine=f=82.4:d={dur}[b];anoisesrc=d={dur}:c=brown:a=0.4[n];"
            f"[n]lowpass=f=300[nl];[a][b][nl]amix=inputs=3:weights=1 0.6 0.5,"
            f"tremolo=f=0.15:d=0.5,afade=t=in:d=2,afade=t=out:st={max(dur - 2, 0)}:d=2,volume=0.35[out]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-filter_complex", filt, "-map", "[out]",
                    "-ar", "48000", path], check=True)


def render(spec_path, out, check_only=False, stills=None):
    spec = json.load(open(spec_path))
    ac = hex_rgb(spec.get("accent", "#E8A33D"))
    scenes = spec["scenes"]
    for sc in scenes:
        if sc["type"] not in SCENES:
            sys.exit(f"unknown scene type: {sc['type']}")
    tmp = tempfile.mkdtemp(prefix="render-")
    voice, words, total = synth(spec, scenes, tmp)
    print(f"voice: {total:.1f}s, {len(words)} words, {len(scenes)} scenes")
    if check_only:
        return total
    enc = None
    chunks = caption_chunks(words, spec.get("caption_words", 3))
    vign = make_vignette()
    rng = np.random.default_rng(1)
    grains = [rng.normal(0, 4, (H // 2, W // 2, 1)).astype(np.float32) for _ in range(6)]
    grains = [np.repeat(np.repeat(g, 2, 0), 2, 1) for g in grains]
    base = Image.new("RGB", (W, H), (12, 11, 10))
    silent = os.path.join(tmp, "video.mp4")
    enc_cmd = (["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset",
                            "slow", "-crf", "27", "-tune", "grain", "-pix_fmt", "yuv420p", silent])
    nframes = int(math.ceil(total * FPS))

    def scene_frame(i, t):
        sc = scenes[i]
        p = (t - sc["start"]) / max(sc["end"] - sc["start"], 1e-6)
        img = base.copy()
        d = ImageDraw.Draw(img, "RGBA")
        SCENES[sc["type"]](img, d, min(max(p, 0), 1), sc, ac)
        z = 1.0 + 0.045 * p  # slow camera push
        cw, ch = int(W / z), int(H / z)
        return img.crop(((W - cw) // 2, (H - ch) // 2, (W + cw) // 2, (H + ch) // 2)).resize((W, H), Image.BILINEAR)

    if stills:  # one contact sheet: frame at 60% of each scene, for visual QA
        os.makedirs(stills, exist_ok=True)
        thumbs = []
        for i, sc in enumerate(scenes):
            t = sc["start"] + 0.6 * (sc["end"] - sc["start"])
            img = scene_frame(i, t)
            draw_captions(ImageDraw.Draw(img), t, chunks, ac)
            thumbs.append(img.resize((270, 480)))
        cols = 5
        sheet = Image.new("RGB", (cols * 270, math.ceil(len(thumbs) / cols) * 480), (40, 40, 40))
        for i, th in enumerate(thumbs):
            sheet.paste(th, ((i % cols) * 270, (i // cols) * 480))
        path = os.path.join(stills, f"{spec.get('id', 'video')}-sheet.png")
        sheet.save(path)
        print(f"wrote {path}")
        return total

    enc = subprocess.Popen(list(enc_cmd), stdin=subprocess.PIPE)
    si = 0
    for f in range(nframes):
        t = f / FPS
        while si < len(scenes) - 1 and t >= scenes[si]["end"]:
            si += 1
        img = scene_frame(si, t)
        xf = 0.18
        if si > 0 and t - scenes[si]["start"] < xf and scenes[si]["type"] != "black":
            prev = scene_frame(si - 1, scenes[si - 1]["end"] - 1e-3)
            img = Image.blend(prev, img, (t - scenes[si]["start"]) / xf)
        draw_captions(ImageDraw.Draw(img), t, chunks, ac)
        arr = np.asarray(img, dtype=np.float32) * vign + grains[f % 6]
        enc.stdin.write(np.clip(arr, 0, 255).astype(np.uint8).tobytes())
        if f % 300 == 0:
            print(f"  frame {f}/{nframes}", flush=True)
    enc.stdin.close()
    enc.wait()
    mus = os.path.join(tmp, "music.wav")
    music_bed(mus, total)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", voice, "-i", mus,
                    "-filter_complex",
                    "[1:a]aresample=48000,volume=1.0[v];[2:a]volume=0.12[m];"
                    "[v][m]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,volume=2dB,alimiter=limit=0.89[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", out], check=True)
    print(f"wrote {out}")
    return total


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--out")
    ap.add_argument("--check", action="store_true", help="synthesize voice only and report duration")
    ap.add_argument("--stills", metavar="DIR", help="write a contact sheet (one frame per scene) instead of a video")
    a = ap.parse_args()
    sid = json.load(open(a.spec)).get("id", "video")
    out = a.out or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output", f"{sid}.mp4")
    render(a.spec, out, a.check, a.stills)
