#!/usr/bin/env python3
"""Ad A (outdoor builders). Structure: three-beat list.
usage: build_ad_a.py SRC OUTDIR preview|audio|render9|render45|bumper"""
import sys, os, subprocess, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sr_kit import *

SRC, OUT, MODE = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(OUT, exist_ok=True)
CANVAS = {'9x16': (1080, 1920), '4x5': (1080, 1350)}
CTA = [[('Send us your next', 'n')], [('outdoor ', 'n'), ('plan.', 'a')]]
URL = 'stoneandrosellc.com'

# crop keyframes: (t_rel, hero centre x in source px). Reason per shot in SHOTLIST.md
MAIN_SHOTS = [
    dict(id='H',  src=15.2, dur=2.8, z=1.0, cx={'9x16': [(0, 770), (1.0, 690), (2.8, 695)],  '4x5': [(0, 860), (1.0, 790), (2.8, 800)]}),
    dict(id='B1', src=10.0, dur=4.0, z=1.05, cx={'9x16': [(0, 665), (1.8, 820), (4.0, 915)],   '4x5': [(0, 765), (1.8, 860), (4.0, 960)]}),
    dict(id='B2', src=63.4, dur=2.6, z={'9x16': (1.0, 1.03), '4x5': (1.06, 1.09)}, cx={'9x16': [(0, 736), (2.6, 722)], '4x5': [(0, 760), (2.6, 745)]}),
    dict(id='B3', src=45.2, dur=3.4, z=1.06, cx={'9x16': [(0, 990), (3.4, 1150)],             '4x5': [(0, 1000), (3.4, 1150)]}),
    dict(id='E',  src=48.6, dur=2.5, z=1.03, cx={'9x16': [(0, 1100), (2.5, 1100)],            '4x5': [(0, 1100), (2.5, 1100)]}),
]
# cards: (shot index, t_in, t_out) in ad time. hook is hard-in at 0.
MAIN_CARDS = [
    dict(k='hook', label='ARIZONA OUTDOOR BUILDERS', lines=[[('Selling yards', 'n')], [('off a ', 'n'), ('sketch?', 'a')]], t=(0.0, 1.5), hard=True, shot='H', size=118, lab=46),
    dict(k='three', label='THREE THINGS', lines=[[('A sketch', 'n')], [("can't ", 'a'), ('show.', 'n')]], t=(1.5, 2.8), shot='H'),
    dict(k='b1', label='01 / PLACEMENT', lines=[[('Where it ', 'n'), ('sits.', 'a')]], t=(2.8, 6.8), shot='B1'),
    dict(k='b2', label='02 / FLOW', lines=[[('How the yard', 'n')], [('connects.', 'a')]], t=(6.8, 9.4), shot='B2'),
    dict(k='b3', label='03 / THE UPSELL', lines=[[('The fire pit', 'n')], [('they ', 'n'), ('skip.', 'a')]], t=(9.4, 12.8), shot='B3', y={'9x16': 600, '4x5': 470}),
]
END_T = 12.8

BUMPER_SHOTS = [
    dict(id='H',  src=15.2, dur=2.2, z=1.0, cx={'9x16': [(0, 770), (1.0, 690), (2.2, 695)], '4x5': [(0, 860), (2.2, 800)]}),
    dict(id='B1', src=10.0, dur=1.8, z=1.03, cx={'9x16': [(0, 665), (1.8, 820)],             '4x5': [(0, 765), (1.8, 860)]}),
    dict(id='E',  src=48.8, dur=2.0, z=1.03, cx={'9x16': [(0, 1100), (2.0, 1100)],           '4x5': [(0, 1100), (2.0, 1100)]}),
]
BUMPER_CARDS = [
    dict(k='hook', label='ARIZONA OUTDOOR BUILDERS', lines=[[('Selling yards', 'n')], [('off a ', 'n'), ('sketch?', 'a')]], t=(0.0, 2.2), hard=True, shot='H'),
    dict(k='pay', label='SHOW IT FIRST', lines=[[('Where it ', 'n'), ('sits.', 'a')]], t=(2.2, 4.0), shot='B1'),
]
BUMPER_END_T = 4.0

def linework(im):
    g = Image.fromarray(im).convert('L').filter(ImageFilter.GaussianBlur(1.4))
    a = np.asarray(g, dtype=np.float32)
    gx = np.zeros_like(a); gy = np.zeros_like(a)
    gx[:, 1:-1] = a[:, 2:] - a[:, :-2]; gy[1:-1, :] = a[2:, :] - a[:-2, :]
    m = np.hypot(gx, gy)
    e = np.clip((m - 7) / 22.0, 0, 1)
    bg = np.array([22, 17, 15], np.float32); ln = np.array([226, 214, 200], np.float32)
    return (bg * (1 - e[..., None]) + ln * e[..., None]).astype(np.uint8)

def linework_wipe(im, p):
    """flat line drawing resolves into the render, left to right (edge-filtered frame, no cartoon filter)."""
    H, W = im.shape[:2]; lw = linework(im)
    p = p * p * (3 - 2 * p)
    xb = -120 + (W + 240) * p
    xs = np.arange(W, dtype=np.float32)
    k = np.clip((xb - xs) / 120.0, 0, 1)[None, :, None]     # 1 = render, 0 = drawing
    return (im * k + lw * (1 - k)).astype(np.uint8)

def layout(ratio):
    W, H = CANVAS[ratio]
    if ratio == '9x16':
        return dict(y_label=276, size=100)
    return dict(y_label=190, size=100)

def end_layer(ratio):
    W, H = CANVAS[ratio]
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    yc = 560 if ratio == '9x16' else 330
    wm = 'STONE & ROSE'; f = ImageFont.truetype(FONT_SEMI, 86); tr = 14
    w = tracked_width(d, wm, f, tr); tracked(d, ((W - w) / 2, yc), wm, f, OFFWHITE + (255,), tr)
    d.rectangle([W / 2 - 70, yc + 112, W / 2 + 70, yc + 115], fill=ROSE + (255,))
    cta, bbox = build_card((W, H), None, CTA, size=96, y_label=yc + 170, center=True)
    layer = Image.alpha_composite(layer, cta)
    fm = ImageFont.truetype(FONT_MONO, 48); d = ImageDraw.Draw(layer)
    uy = bbox[3] + 40; uw = tracked_width(d, URL, fm, 3)
    tracked(d, ((W - uw) / 2, uy), URL, fm, OFFWHITE + (255,), 3)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(layer.split()[3].filter(ImageFilter.GaussianBlur(9)).point(lambda v: int(v * .55)))
    return Image.alpha_composite(sh, layer), (60, yc - 20, W - 60, uy + 60)

def prep_cards(cards, shots, ratio, src):
    lay = layout(ratio); res = []
    by = {s['id']: s for s in shots}
    for c in cards:
        layer, bbox = build_card(CANVAS[ratio], c['label'], c['lines'], size=c.get('size', lay['size']), y_label=c.get('y', {}).get(ratio, lay['y_label']), label_size=c.get('lab'))
        sh = by[c['shot']]
        # worst-case luma over the card's life, measured on cropped+graded frame
        Ls = []
        shot_t0 = sum(s['dur'] for s in shots[:shots.index(sh)])
        for tt in np.linspace(c['t'][0], c['t'][1] - 0.05, 3):
            tr = min(max(tt - shot_t0, 0), sh['dur'] - 0.05)
            fr = one_frame(SRC, sh['src'] + tr)
            cr = grade(render_crop(fr, crop_box(sh, ratio, tr), ratio))
            Ls.append(luma_in(cr, bbox))
        L = max(Ls); res.append(dict(c=c, layer=layer, scr=scrim(CANVAS[ratio], bbox, strength_for(L)), L=L, bbox=bbox))
        print(f"[luma] {ratio} card {c['k']}: text-box luma {L:.0f} -> scrim {strength_for(L):.2f}", flush=True)
    return res

WIPE = 0.9
def compose_frame(fr, shot, ratio, t_rel, t_ad, cards, end, end_t, dim_end):
    im = grade(render_crop(fr, crop_box(shot, ratio, t_rel), ratio))
    if shot['id'] == 'H' and t_rel < WIPE:
        im = linework_wipe(im, t_rel / WIPE)
    if t_ad >= end_t:
        f = im.astype(np.float32) * (0.56 if dim_end else 1.0)
        H = im.shape[0]
        g = np.linspace(0.0, 1.0, H, dtype=np.float32)[:, None, None]
        f = f * (1 - 0.25 * (1 - np.abs(g - 0.45) * 2).clip(0, 1) * 0)  # no extra vignette
        im = f.astype(np.uint8)
        a = card_alpha(t_ad, end_t, 1e9)
        lay, bbox = end
        scr = scrim(CANVAS[ratio], bbox, 0.50)
        return apply_card(im, lay, scr, a, dy=int(10 * (1 - a)))
    for cd in cards:
        c = cd['c']
        if c['t'][0] <= t_ad < c['t'][1]:
            a = card_alpha(t_ad, c['t'][0], c['t'][1], hard_in=c.get('hard', False))
            im = apply_card(im, cd['layer'], cd['scr'], a, dy=0 if c.get('hard') else int(10 * (1 - a)))
    return im

def audio(kind, path):
    if kind == 'main':
        total = 15.3
        ev = [('tick', 0.0, {'g': .22}), ('tick', 1.5, {}), ('whoosh', 2.8, {'dur': .75, 'g': .55}), ('boom', 2.8, {'g': .95}), ('tick', 2.8, {'g': .3}),
              ('whoosh', 6.8, {'dur': .5, 'g': .28}), ('boom', 6.8, {'g': .38}), ('tick', 6.8, {}),
              ('whoosh', 9.4, {'dur': .5, 'g': .28}), ('boom', 9.4, {'g': .38}), ('tick', 9.4, {}),
              ('crackle', 9.4, {'dur': 3.4, 'g': .22}),
              ('chime', 12.8, {'g': .34}), ('tick', 12.8, {'g': .2})]
    else:
        total = 6.0
        ev = [('tick', 0.0, {'g': .22}), ('whoosh', 2.2, {'dur': .5, 'g': .5}), ('boom', 2.2, {'g': .8}), ('tick', 2.2, {}),
              ('chime', 4.0, {'g': .34}), ('tick', 4.0, {'g': .2})]
    st = synth(total, ev)
    write_wav(path + '.raw.wav', st); master(path + '.raw.wav', path); os.remove(path + '.raw.wav')

def run_render(ratio, shots, cards, end_t, dim_end, total, wav, outfile):
    pc = prep_cards(cards, shots, ratio, SRC); end = end_layer(ratio)
    W, H = CANVAS[ratio]
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-i', wav, '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-maxrate', '10M', '-bufsize', '20M',
                            '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-movflags', '+faststart', '-c:a', 'aac', '-b:a', '192k',
                            '-t', f'{total:.3f}', '-shortest', outfile], stdin=subprocess.PIPE)
    t0 = 0.0; n = 0
    for sh in shots:
        for i, fr in enumerate(read_shot(SRC, sh['src'], sh['dur'])):
            t_rel = i / FPS; t_ad = t0 + t_rel
            enc.stdin.write(compose_frame(fr, sh, ratio, t_rel, t_ad, pc, end, end_t, dim_end).tobytes()); n += 1
        t0 += sh['dur']
    enc.stdin.close(); enc.wait(); print('frames', n, 'done', outfile, flush=True)

def preview():
    """crop audit + safe zone overlay: one frame per shot at start/mid/end, both ratios."""
    tiles = []
    for ratio in ('9x16', '4x5'):
        pc = prep_cards(MAIN_CARDS, MAIN_SHOTS, ratio, SRC); end = end_layer(ratio)
        t0 = 0.0
        for sh in MAIN_SHOTS:
            for frac in (0.04, 0.5, 0.96):
                tr = sh['dur'] * frac; fr = one_frame(SRC, sh['src'] + tr)
                im = compose_frame(fr, sh, ratio, tr, t0 + tr, pc, end, END_T, True)
                pil = Image.fromarray(im); d = ImageDraw.Draw(pil)
                if ratio == '9x16':
                    d.rectangle([65, 270, 1015, 1248], outline=(0, 255, 255), width=3)
                    d.rectangle([853, 1152, 1080, 1920], outline=(255, 0, 255), width=2)
                else:
                    d.line([0, int(1350 * .85), 1080, int(1350 * .85)], fill=(0, 255, 255), width=3)
                d.text((12, 8), f"{ratio} {sh['id']} {t0 + tr:.1f}s", fill=(255, 255, 0))
                tiles.append((ratio, pil))
            t0 += sh['dur']
    for ratio in ('9x16', '4x5'):
        ts = [p for r, p in tiles if r == ratio]; w, h = ts[0].size; sc = 0.33
        sheet = Image.new('RGB', (3 * int(w * sc), 5 * int(h * sc)))
        for i, p in enumerate(ts):
            sheet.paste(p.resize((int(w * sc), int(h * sc))), ((i % 3) * int(w * sc), (i // 3) * int(h * sc)))
        sheet.save(f'{OUT}/preview_{ratio}.jpg', quality=85)
    print('preview ok')

if MODE == 'preview': preview()
elif MODE == 'audio':
    audio('main', f'{OUT}/audio_main.wav'); audio('bumper', f'{OUT}/audio_bumper.wav')
elif MODE == 'render9': run_render('9x16', MAIN_SHOTS, MAIN_CARDS, END_T, True, 15.3, f'{OUT}/audio_main.wav', f'{OUT}/SR_outdoor_builders_9x16.mp4')
elif MODE == 'render45': run_render('4x5', MAIN_SHOTS, MAIN_CARDS, END_T, True, 15.3, f'{OUT}/audio_main.wav', f'{OUT}/SR_outdoor_builders_4x5.mp4')
elif MODE == 'bumper': run_render('9x16', BUMPER_SHOTS, BUMPER_CARDS, BUMPER_END_T, True, 6.0, f'{OUT}/audio_bumper.wav', f'{OUT}/SR_outdoor_builders_6s_9x16.mp4')
