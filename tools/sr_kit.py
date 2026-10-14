"""Stone & Rose ad toolkit: grade, crop, cards, scrim, audio synth. No client data in here."""
import numpy as np, subprocess, wave, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_SEMI = HERE + '/fonts/CG-Semi600.ttf'
FONT_ITAL = HERE + '/fonts/CG-Italic600.ttf'
FONT_MONO = HERE + '/fonts/Plex500.ttf'
OFFWHITE = (238, 232, 226)
ROSE = (201, 143, 114)
FPS = 30
SR = 44100

# ---------- grade ----------
def make_lut():
    x = np.arange(256) / 255.0
    lifted = x ** 0.90                      # lift shadows so turf does not crush on phones
    curve = lifted + 0.06 * np.sin((lifted - 0.5) * np.pi) * 0.5   # gentle contrast
    curve = np.clip(curve, 0, 1)
    lut = np.stack([np.clip(curve * 1.025, 0, 1), curve, np.clip(curve * 0.965, 0, 1)], axis=1)
    return (lut * 255 + 0.5).astype(np.uint8)
LUT = make_lut()
def grade(fr):
    out = np.empty_like(fr)
    for c in range(3):
        out[..., c] = LUT[fr[..., c], c]
    return out

# ---------- source reading ----------
def read_shot(src, t_in, dur):
    """yield RGB uint8 1080x1920 frames at FPS for [t_in, t_in+dur)."""
    n = int(round(dur * FPS))
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', f'{t_in:.4f}', '-i', src, '-t', f'{dur + 0.1:.4f}',
                          '-vf', f'fps={FPS}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                         stdout=subprocess.PIPE)
    size = 1920 * 1080 * 3
    for i in range(n):
        buf = p.stdout.read(size)
        if len(buf) < size:
            break
        yield np.frombuffer(buf, np.uint8).reshape(1080, 1920, 3)
    p.stdout.close(); p.kill(); p.wait()

def one_frame(src, t):
    p = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.4f}', '-i', src, '-frames:v', '1',
                        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    return np.frombuffer(p.stdout, np.uint8).reshape(1080, 1920, 3)

def interp(kf, t):
    ts = [k[0] for k in kf]; vs = [k[1] for k in kf]
    return float(np.interp(t, ts, vs))

def crop_box(shot, ratio, t):
    W0 = 608 if ratio == '9x16' else 864
    kf = shot['cx'][ratio]
    zz = shot['z'][ratio] if isinstance(shot['z'], dict) else shot['z']
    z0, z1 = zz if isinstance(zz, tuple) else (1.0, zz)
    z = z0 + (z1 - z0) * min(1, max(0, t / shot['dur']))
    w, h = W0 / z, 1080 / z
    cx = interp(kf, t)
    x0 = min(max(cx - w / 2, 0), 1920 - w)
    return (x0, 0.0, x0 + w, h)

def render_crop(fr, box, ratio):
    out = (1080, 1920) if ratio == '9x16' else (1080, 1350)
    im = Image.fromarray(fr).resize(out, Image.LANCZOS, box=box)
    return np.asarray(im)

# ---------- text ----------
def tracked(draw, xy, text, font, fill, track):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + track
    return x

def tracked_width(draw, text, font, track):
    return sum(draw.textlength(c, font=font) + track for c in text) - track

def fit_font(path, runs_text, max_w, size):
    d = ImageDraw.Draw(Image.new('RGB', (10, 10)))
    while size > 40:
        f = ImageFont.truetype(path, size)
        if d.textlength(runs_text, font=f) <= max_w:
            return size
        size -= 2
    return size

def build_card(canvas, label, lines, size=104, x=90, y_label=300, y_head=366, center=False, label_size=None):
    """lines: list of list of (text, 'n'|'a'). Returns (RGBA layer, bbox)."""
    W, H = canvas
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    max_w = W - 2 * x
    # fit headline size to longest line
    longest = max((''.join(t for t, _ in ln) for ln in lines), key=len)
    size = fit_font(FONT_SEMI, longest, max_w, size)
    lab_size = label_size or max(int(size * 0.40), 38)   # label >= 0.36x headline
    fl = ImageFont.truetype(FONT_MONO, lab_size)
    track = lab_size * 0.16
    top = y_label
    if label:
        lw = tracked_width(d, label, fl, track)
        lx = (W - lw) / 2 if center else x
        tracked(d, (lx, y_label), label, fl, ROSE if False else OFFWHITE + (230,), track)
        y_head_eff = y_label + lab_size + 34
    else:
        y_head_eff = y_label
    y = y_head_eff
    fs, fi = ImageFont.truetype(FONT_SEMI, size), ImageFont.truetype(FONT_ITAL, size)
    for ln in lines:
        widths = [d.textlength(t, font=(fi if s == 'a' else fs)) for t, s in ln]
        cx = (W - sum(widths)) / 2 if center else x
        for (t, s), w in zip(ln, widths):
            d.text((cx, y), t, font=(fi if s == 'a' else fs), fill=(ROSE if s == 'a' else OFFWHITE) + (255,))
            cx += w
        y += int(size * 1.02)
    tb = layer.split()[3].getbbox()
    bbox = (tb[0] - 30, tb[1] - 20, tb[2] + 30, tb[3] + 20)
    # soft shadow (not a panel)
    a = layer.split()[3]
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sh.putalpha(a.filter(ImageFilter.GaussianBlur(9)).point(lambda v: int(v * 0.55)))
    comp = Image.alpha_composite(sh, layer)
    return comp, bbox

def scrim(canvas, bbox, strength):
    W, H = canvas
    y0, y1 = bbox[1] - 130, bbox[3] + 230
    ys = np.arange(H, dtype=np.float32)
    up = np.clip((ys - y0) / 130.0, 0, 1); dn = np.clip((y1 - ys) / 230.0, 0, 1)
    prof = (up * dn); prof = prof * prof * (3 - 2 * prof)
    xs = np.arange(W, dtype=np.float32)
    xl = np.clip((xs - (bbox[0] - 220)) / 220.0, 0, 1); xr = np.clip(((bbox[2] + 300) - xs) / 300.0, 0, 1)
    px = xl * xr; px = px * px * (3 - 2 * px)
    return (prof[:, None] * px[None, :] * strength).astype(np.float32)[:, :, None]  # H x W x 1

def luma_in(frame, bbox):
    x0, y0, x1, y1 = [int(v) for v in bbox]
    z = frame[max(y0, 0):y1, max(x0, 0):x1].astype(np.float32)
    return float((0.2126 * z[..., 0] + 0.7152 * z[..., 1] + 0.0722 * z[..., 2]).mean())

def strength_for(L):
    return float(0.22 + 0.38 * np.clip((L - 60) / 130.0, 0, 1))

def apply_card(frame, layer_rgba, scr, alpha, dy=0):
    f = frame.astype(np.float32)
    f = f * (1 - scr * alpha) + np.array([12, 9, 8], np.float32) * (scr * alpha)
    lay = np.asarray(layer_rgba).astype(np.float32)
    if dy:
        lay = np.roll(lay, int(dy), axis=0)
    a = (lay[..., 3:4] / 255.0) * alpha
    f = f * (1 - a) + lay[..., :3] * a
    return np.clip(f, 0, 255).astype(np.uint8)

def card_alpha(t, tin, tout, hard_in=False, fade=0.22):
    a_in = 1.0 if hard_in else min(1.0, max(0.0, (t - tin) / fade))
    a_out = min(1.0, max(0.0, (tout - t) / fade))
    return min(a_in, a_out)

# ---------- audio synth ----------
def _env_exp(n, tau): return np.exp(-np.arange(n) / (tau * SR))

def lowpass(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); s = 0.0
    for i in range(len(x)):
        s = (1 - a) * x[i] + a * s; y[i] = s
    return y

def lp_fast(x, fc):
    # block FFT-free fast one-pole via cumulative trick (vectorised using scipy-free approach)
    a = np.exp(-2 * np.pi * fc / SR)
    n = len(x); y = np.empty(n); s = 0.0
    # process in python loop on decimated chunks is slow; use ffmpeg-free numpy filter via lfilter equivalent
    from numpy.lib.stride_tricks import sliding_window_view
    k = int(max(1, min(400, np.log(1e-3) / np.log(a))))
    kern = (1 - a) * a ** np.arange(k)
    return np.convolve(x, kern)[:n]

def synth(total, events, seed=7):
    """events: list of (kind, t, params). Returns stereo float array."""
    rng = np.random.default_rng(seed)
    n = int(total * SR); L = np.zeros(n); R = np.zeros(n)
    t = np.arange(n) / SR
    # pad: warm A-minor stack, slow tremolo, fade in/out
    pad = np.zeros(n)
    for f, g in [(110.0, 1.0), (164.81, 0.7), (220.0, 0.6), (261.63, 0.45), (329.63, 0.35)]:
        for det in (-0.6, 0.0, 0.7):
            pad += g * np.sin(2 * np.pi * (f + det) * t + rng.uniform(0, 6.28))
    pad *= (0.8 + 0.2 * np.sin(2 * np.pi * 0.11 * t))
    fade = np.clip(t / 1.2, 0, 1) * np.clip((total - t) / 1.4, 0, 1)
    pad = pad / np.abs(pad).max() * 0.16 * fade
    L += pad; R += np.roll(pad, 40)
    def add(sig, t0, pan=0.0):
        i0 = int(t0 * SR); i1 = min(n, i0 + len(sig))
        if i0 >= n or i1 <= i0: return
        s = sig[:i1 - i0]
        L[i0:i1] += s * (1 - max(pan, 0)); R[i0:i1] += s * (1 + min(pan, 0))
    for kind, t0, p in events:
        if kind == 'tick':      # card-in tick
            m = int(0.06 * SR); tt = np.arange(m) / SR
            s = (np.sin(2 * np.pi * 2200 * tt) * 0.5 + rng.standard_normal(m) * 0.25) * _env_exp(m, 0.008)
            add(s * p.get('g', 0.28), t0)
        elif kind == 'whoosh':  # rising filtered noise ending at t0
            d = p['dur']; m = int(d * SR); x = rng.standard_normal(m)
            lo = lp_fast(x, 900); hi = lp_fast(x, 6000)
            ramp = np.linspace(0, 1, m) ** 2.2
            s = (lo * (1 - ramp) + hi * ramp) * ramp
            add(s / np.abs(s).max() * p['g'], t0 - d)
        elif kind == 'boom':
            m = int(1.6 * SR); tt = np.arange(m) / SR
            f = 38 + 70 * np.exp(-tt / 0.12)
            s = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env_exp(m, 0.45)
            s += lp_fast(rng.standard_normal(m), 400) * _env_exp(m, 0.15) * 1.2
            add(s / np.abs(s).max() * p['g'], t0)
        elif kind == 'chime':
            m = int(2.6 * SR); tt = np.arange(m) / SR; s = np.zeros(m)
            for f, g in [(880, 1), (1320, 0.5), (1760, 0.3), (2637, 0.12)]:
                s += g * np.sin(2 * np.pi * f * tt) * _env_exp(m, 0.7)
            add(s / np.abs(s).max() * p['g'], t0)
        elif kind == 'crackle':  # fire: sparse clicks + low bed
            d = p['dur']; m = int(d * SR); bed = lp_fast(rng.standard_normal(m), 260) * 0.5
            bed *= np.clip(np.arange(m) / (0.4 * SR), 0, 1) * np.clip((m - np.arange(m)) / (0.4 * SR), 0, 1)
            seg = bed * p['g'] * 0.6
            for _ in range(int(d * 26)):
                i = rng.integers(0, m - 800); l = int(rng.uniform(0.002, 0.012) * SR)
                c = rng.standard_normal(l) * _env_exp(l, 0.003) * rng.uniform(0.2, 1.0)
                seg[i:i + l] += c * p['g']
            add(seg, t0, pan=rng.uniform(-0.3, 0.3))
    out = np.stack([L, R], axis=1)
    return out

def write_wav(path, st):
    pcm = (np.clip(st, -1, 1) * 32767).astype('<i2')
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

def master(in_wav, out_wav, I=-14.0, TP=-2.0):
    """two-pass loudnorm to I LUFS; TP ceiling leaves headroom so the AAC encode stays under -1 dBFS."""
    import json, re
    comp = in_wav + '.comp.wav'   # tame the boom so the integrated level can rise without busting the peak ceiling
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', in_wav, '-af', 'acompressor=threshold=-20dB:ratio=3.5:attack=4:release=140:makeup=2', comp], check=True)
    in_wav = comp
    r = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', in_wav, '-af',
                        f'loudnorm=I={I}:TP={TP}:LRA=7:print_format=json', '-f', 'null', '-'], capture_output=True, text=True)
    m = json.loads(re.search(r'\{[^{}]*"input_i"[^{}]*\}', r.stderr, re.S).group(0))
    af = (f"loudnorm=I={I}:TP={TP}:LRA=7:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', in_wav, '-af', af, '-ar', str(SR), out_wav], check=True)
