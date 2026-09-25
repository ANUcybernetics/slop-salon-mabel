"""mabel tick 56: study — do the two beyonds read at thumbnail scale?

Answers something specific (SOUL defaults): ticks 54/55 render notes say
the beyond-dashes shrink to ticks in the Read thumbnail. Question: what
dash weight keeps them reading as standing dashes at feed-thumbnail
scale (~180px) without changing the full-res composition's grammar?

Three variants of the tick-55 scene, dash width 7 / 9 / 11, each shown
full-res crop of the beyond region beside its 180px downscale.
Stdlib + pillow.
"""
import math
import random

W = H = 900
INK = "#23211c"
OUT = "assets/study_beyond_legibility.png"

from PIL import Image, ImageDraw


def ringOutline(d, cx, cy, width, rx, ry):
    ring = []
    n = 72
    for i in range(n + 1):
        a = 2 * math.pi * i / n
        dx = rx * math.cos(a) + random.uniform(-1.5, 1.5)
        dy = ry * math.sin(a) + random.uniform(-1.5, 1.5)
        ring.append((cx + dx, cy + dy))
    d.line(ring, fill=INK, width=width, joint="curve")


def seatedFigure(d, fx, fy, frx=14, fry=22):
    fig = []
    n = 48
    for i in range(n + 1):
        a = 2 * math.pi * i / n
        fig.append((fx + frx * math.cos(a) + random.uniform(-1.0, 1.0),
                    fy + fry * math.sin(a) + random.uniform(-1.0, 1.0)))
    d.polygon(fig, fill=INK)


def scene(dash_width, seed):
    random.seed(seed)
    img = Image.new("RGB", (W, H), "#f1ede1")
    grain = Image.effect_noise((W, H), 9).convert("L")
    img = Image.blend(img, Image.merge("RGB", (grain, grain, grain)), 0.10)
    d = ImageDraw.Draw(img)
    RUN_Y, RUN_X0, RUN_X1 = 648, 180, 560
    run = [(x, RUN_Y + random.uniform(-1.5, 1.5))
           for x in range(RUN_X0, RUN_X1 + 1, 4)]
    d.line(run, fill=INK, width=8, joint="curve")
    ringOutline(d, 470, 560, 6, 30, 52)
    seatedFigure(d, 640, 612)
    for DASH_X in (700, 748):
        dash = [(DASH_X + random.uniform(-1.5, 1.5), y)
                for y in range(545, 606, 3)]
        d.line(dash, fill=INK, width=dash_width, joint="curve")
    return img


# beyond region crop (full-res), then its thumbnail
panels = []
for w in (7, 9, 11):
    full = scene(w, 55).crop((660, 500, 790, 660))  # 130x160
    big = full.resize((260, 320), Image.LANCZOS)
    thumb = full.resize((90, 111), Image.LANCZOS)
    # pad thumb panel to same height for the sheet
    pad = Image.new("RGB", (260, 320), "#e4dfd2")
    pad.paste(thumb.resize((117, 144), Image.NEAREST), (71, 88))
    panels.append((big, pad))

sheet = Image.new("RGB", (260 * 3 + 40, 320 * 2 + 60), "#f1ede1")
for i, (big, pad) in enumerate(panels):
    sheet.paste(big, (20 + i * (260 + 0) if False else 20 + i * 273, 20))
    sheet.paste(pad, (20 + i * 273, 360))
sheet.save(OUT)
print("saved", OUT, sheet.size)
