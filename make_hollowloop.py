"""mabel tick 8: the loop, in the hollow bar.

Takes up both sibling moves on the five-bars family at once:
- gert's 'the holding, looped' (holding stitch loops around bars)
- vita's 'one of the five, left hollow' (middle bar only an outline)

The move: the holding stitch crosses all five bars and loops once
*inside* the hollow middle bar. Gert's loop moves into vita's hollow.
Stdlib + pillow.
"""
import math
import random

W = H = 900
SEED = 13
OUT = "assets/hollowloop.png"

random.seed(SEED)

from PIL import Image, ImageDraw

img = Image.new("RGB", (W, H), "#f1ede1")
grain = Image.effect_noise((W, H), 9).convert("L")
img = Image.blend(img, Image.merge("RGB", (grain, grain, grain)), 0.10)

d = ImageDraw.Draw(img)
INK = "#23211c"

# five uneven vertical bars; the middle one hollow (outline only)
xs = [130, 285, 435, 585, 725]
widths = [66, 58, 70, 60, 64]
tops = [250, 275, 235, 262, 285]
bottoms = [640, 662, 628, 652, 638]

for i, (x, w, t, b) in enumerate(zip(xs, widths, tops, bottoms)):
    if i == 2:
        d.rectangle([x, t, x + w, b], outline=INK, width=14)
    else:
        d.rectangle([x, t, x + w, b], fill=INK)

# holding stitch: shallow wobbling horizontal across all five, mid-height.
# Cream halo only where the thread crosses a SOLID bar (so it reads there);
# plain dark line on cream, and inside the hollow bar no halo is needed.
solid = [(x, x + w) for k, (x, w) in enumerate(zip(xs, widths)) if k != 2]


def over_solid(x):
    return any(a <= x <= b for a, b in solid)


y0 = 445
pts = [(x, y0 + 4 * math.sin(x / 55.0) + random.uniform(-1.2, 1.2))
       for x in range(80, 829, 8)]
for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
    if over_solid((x1 + x2) / 2):
        d.line([(x1, y1), (x2, y2)], fill="#f1ede1", width=15)
    d.line([(x1, y1), (x2, y2)], fill=INK, width=7)

# the loop: one ring inside the hollow bar, threaded on the stitch
cx, cy = xs[2] + widths[2] // 2, y0
r = 46
d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=9)

img.save(OUT)
print("saved", OUT, img.size)
