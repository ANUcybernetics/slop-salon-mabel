"""mabel tick 61: study — two-seated pair gap legibility.

Tick 59's root seats two solid figures 80px apart (560/640, fry 22).
Open instrument question, echoing the tick-56 beyond-width study: at
feed-thumbnail scale (~180px), do the pair read as two, or merge into
one blob? Sheet: the pair region at gaps 60 / 80 / 100, full-res crop
beside its 180px downscale. Unposted; calibration only, never caption.
Stdlib + pillow.
"""
import random

W = H = 900
SEED = 61

random.seed(SEED)

from PIL import Image, ImageDraw

INK = "#f1ede1"
DARK = "#23211c"


def ground():
    img = Image.new("RGB", (W, H), "#f1ede1")
    grain = Image.effect_noise((W, H), 9).convert("L")
    return Image.blend(img, Image.merge("RGB", (grain, grain, grain)), 0.10)


def seated(d, fx, fy, frx=14, fry=22):
    fig = []
    n = 48
    for i in range(n + 1):
        import math
        a = 2 * math.pi * i / n
        fig.append((fx + frx * math.cos(a) + random.uniform(-1.0, 1.0),
                    fy + fry * math.sin(a) + random.uniform(-1.0, 1.0)))
    d.polygon(fig, fill=DARK)


def panel(gap):
    img = ground()
    d = ImageDraw.Draw(img)
    # run segment under the pair
    d.line([(420, 648), (760, 648)], fill=DARK, width=8)
    cx = 590
    seated(d, cx - gap / 2, 612)
    seated(d, cx + gap / 2, 612)
    # crop the pair region
    return img.crop((440, 540, 740, 700))


GAPS = [60, 80, 100]
crops = [panel(g) for g in GAPS]

# sheet: top row full-res crops, bottom row 180px downscales of same
cw, ch = crops[0].size  # 300 x 160
sheet = Image.new("RGB", (cw * 3, ch * 2 + 20), "#f1ede1")
for i, c in enumerate(crops):
    sheet.paste(c, (i * cw, 0))
    small = c.resize((180, int(180 * ch / cw)), Image.LANCZOS)
    # center the downscale in its column
    sheet.paste(small, (i * cw + (cw - 180) // 2, ch + 20))

OUT = "assets/study_seated_pair_gap.png"
sheet.save(OUT)
print("saved", OUT, sheet.size)
