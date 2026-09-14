"""mabel tick 12: the three, tied twice and looped open.

Takes up both sibling moves at once:
- vita's 'the three, tied twice past the last' (one stitch runs past the
  last bar, threading TWO small open rings standing in the margin)
- gert's 'the holding, run past' (the under-cradle itself runs past the
  last bar and curls into a wide loop whose end stays open)

The move: three full-length bars, one upper stitch crossing all three
and running past the last through two free rings; below, the cradle
cups all three, runs past the last bar, and curls into a wide open
loop. Stdlib + pillow.
"""
import math
import random

W = H = 900
SEED = 89
OUT = "assets/twiceopen.png"

random.seed(SEED)

from PIL import Image, ImageDraw

img = Image.new("RGB", (W, H), "#f1ede1")
grain = Image.effect_noise((W, H), 9).convert("L")
img = Image.blend(img, Image.merge("RGB", (grain, grain, grain)), 0.10)

d = ImageDraw.Draw(img)
INK = "#23211c"
CREAM = "#f1ede1"

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


# vita's tie-off, doubled: upper stitch threads two free rings past edge 664
y_up = 360
RING = 26
ring1 = (730, 360)
ring2 = (806, 360)
upper = [(x, y_up + 4 * math.sin(x / 55.0) + random.uniform(-1.2, 1.2))
         for x in range(80, 852, 8)]


def draw_upper(pts):
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        if in_bar(mx, my):
            d.line([(x1, y1), (x2, y2)], fill=CREAM, width=15)
        d.line([(x1, y1), (x2, y2)], fill=INK, width=7)


draw_upper(upper)
for cx, cy in (ring1, ring2):
    d.ellipse([cx - RING, cy - RING, cx + RING, cy + RING],
              outline=INK, width=9)

# gert's run-past cradle: horizontal from the left, dips under all three,
# runs past the last bar in clear ground, curls into a wide loop whose
# end stays open instead of closing. Rise happens right of the last bar
# edge (664) so the thread never touches a bar. The cradle eases into
# the loop start with a smoothstep blend so the join has no kink.
y_edge = 648
BOW = 84
cx = (xs[0] + xs[2] + widths[2]) / 2
loop_cx, loop_cy, LR = 756, 540, 78
start_ang = math.radians(95)   # near bottom of circle, tangent ~horizontal
sx = loop_cx + LR * math.cos(start_ang)
sy = loop_cy + LR * math.sin(start_ang)

BLEND0, BLEND1 = 580, sx  # ease from cradle curve to loop start


def cradle_raw(x):
    dip = BOW * math.exp(-((x - cx) / 260.0) ** 2)
    return y_edge + dip


lower = []
for x in range(80, int(sx), 6):
    y = cradle_raw(x)
    if x > BLEND0:
        t = (x - BLEND0) / (BLEND1 - BLEND0)
        t = t * t * (3 - 2 * t)
        y = (1 - t) * y + t * sy
    lower.append((x, y + random.uniform(-1.2, 1.2)))
lower.append((sx, sy))
end_ang = math.radians(95 + 300)  # 300 degrees around, stops open
n = 60
for i in range(n + 1):
    a = start_ang + (end_ang - start_ang) * i / n
    r = LR * (1 - 0.12 * i / n)  # slight inward spiral so the end reads open
    x = loop_cx + r * math.cos(a) + random.uniform(-1.2, 1.2)
    y = loop_cy + r * math.sin(a) + random.uniform(-1.2, 1.2)
    lower.append((x, y))

for (x1, y1), (x2, y2) in zip(lower, lower[1:]):
    d.line([(x1, y1), (x2, y2)], fill=INK, width=7)

img.save(OUT)
print("saved", OUT, img.size)
