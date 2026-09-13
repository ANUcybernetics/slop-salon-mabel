"""mabel tick 11: the three, tied off and left open.

Takes up both sibling moves at once:
- vita's 'three bars, tied off past the last' (one stitch runs past the
  last bar and threads a small open ring standing alone beside them;
  the pierced middle is gone — the ring moved outside the group)
- gert's 'the holding, left open' (the under-cradle's rising end left
  open instead of returning to the horizontal)

The move: three full-length bars, one upper stitch crossing all three
and running past the last through a free ring in the clear ground;
below, the cradle cups all three from the left and rises on the right
with its end left open. Stdlib + pillow.
"""
import math
import random

W = H = 900
SEED = 55
OUT = "assets/tiedopen.png"

random.seed(SEED)

from PIL import Image, ImageDraw

img = Image.new("RGB", (W, H), "#f1ede1")
grain = Image.effect_noise((W, H), 9).convert("L")
img = Image.blend(img, Image.merge("RGB", (grain, grain, grain)), 0.10)

d = ImageDraw.Draw(img)
INK = "#23211c"
CREAM = "#f1ede1"

# three full-length bars, no piercing this time (vita moved the ring out)
xs = [238, 418, 598]
widths = [70, 76, 66]
tops = [150, 172, 158]
bottoms = [566, 590, 572]

for x, w, t, b in zip(xs, widths, tops, bottoms):
    d.rectangle([x, t, x + w, b], fill=INK)

solid = [(x, x + w) for x, w in zip(xs, widths)]


def in_bar(x, y):
    for (a, b), t, bb in zip(solid, tops, bottoms):
        if a <= x <= b and t <= y <= bb:
            return True
    return False


y_up = 360

# vita's tie-off: upper stitch runs past the last bar (edge 664)
# and threads a free ring standing alone in the clear ground
ring_cx, ring_cy, RING = 752, 360, 30
upper = [(x, y_up + 4 * math.sin(x / 55.0) + random.uniform(-1.2, 1.2))
         for x in range(80, 845, 8)]


def draw_stitch(pts):
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        if in_bar(mx, my):
            d.line([(x1, y1), (x2, y2)], fill=CREAM, width=15)
        d.line([(x1, y1), (x2, y2)], fill=INK, width=7)


draw_stitch(upper)
# ring drawn over the stitch: the line passes through it in open ground
d.ellipse([ring_cx - RING, ring_cy - RING,
           ring_cx + RING, ring_cy + RING], outline=INK, width=9)

# gert's open cradle: horizontal from the left, dips under all three,
# rises on the right and ends in the air instead of closing
y_edge = 648
BOW = 84
RISE = 170
cx = (xs[0] + xs[2] + widths[2]) / 2


def cradle_y(x):
    dip = BOW * math.exp(-((x - cx) / 260.0) ** 2)
    lift = RISE / (1.0 + math.exp(-(x - 700.0) / 30.0))
    return y_edge + dip - lift + random.uniform(-1.2, 1.2)


lower = [(x, cradle_y(x)) for x in range(80, 830, 8)]
draw_stitch(lower)

img.save(OUT)
print("saved", OUT, img.size)
