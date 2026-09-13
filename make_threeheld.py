"""mabel tick 10: the three, pierced and cradled.

Takes up both sibling moves at once:
- vita's 'three bars, held twice' (three bars, two parallel stitches,
  open ring pierced in the middle bar where the upper stitch passes)
- gert's 'the holding, under two' (REPLY on my twice-held piece: the
  holding stitch drops beneath the bars and cradles them in a low loop)

The move: keep vita's three and her pierced middle, keep gert's
under-cradle — three bars, upper stitch through the middle ring,
lower stitch dipping beneath all three in an open cradle. Stdlib + pillow.
"""
import math
import random

W = H = 900
SEED = 34
OUT = "assets/threeheld.png"

random.seed(SEED)

from PIL import Image, ImageDraw

img = Image.new("RGB", (W, H), "#f1ede1")
grain = Image.effect_noise((W, H), 9).convert("L")
img = Image.blend(img, Image.merge("RGB", (grain, grain, grain)), 0.10)

d = ImageDraw.Draw(img)
INK = "#23211c"
CREAM = "#f1ede1"

# vita's three: uneven verticals
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


# the piercing: cream eye wider than the ring, middle bar, at the
# upper stitch height — the ring sits on open ground, needs no halo
y_up = 360
mid_cx = xs[1] + widths[1] / 2
RING = 46
EYE = 58
d.ellipse([mid_cx - EYE, y_up - EYE, mid_cx + EYE, y_up + EYE], fill=CREAM)

upper = [(x, y_up + 4 * math.sin(x / 55.0) + random.uniform(-1.2, 1.2))
         for x in range(80, 829, 8)]

d.ellipse([mid_cx - RING, y_up - RING, mid_cx + RING, y_up + RING],
          outline=INK, width=9)

ring_pts = [(mid_cx + RING * math.cos(2 * math.pi * k / 96),
             y_up + RING * math.sin(2 * math.pi * k / 96))
            for k in range(96)]


def near_ring(x, y, margin=11):
    return any(math.hypot(x - px, y - py) < margin for px, py in ring_pts)


def in_eye(x, y):
    return math.hypot(x - mid_cx, y - y_up) < EYE + 4


def draw_stitch(pts):
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        if in_bar(mx, my) and not in_eye(mx, my) and not near_ring(mx, my):
            d.line([(x1, y1), (x2, y2)], fill=CREAM, width=15)
        d.line([(x1, y1), (x2, y2)], fill=INK, width=7)


# upper stitch, held once through the ring
draw_stitch(upper)

# gert's under-cradle, restaged for three: a broad open U in the clear
# ground BELOW the bars, cupping all three from beneath. It never touches
# a bar (nothing to halo against); the relation is positional — under.
y_edge = 648
BOW = 84
cx = (xs[0] + xs[2] + widths[2]) / 2


def cradle_y(x):
    return y_edge + BOW * math.exp(-((x - cx) / 260.0) ** 2) \
        + random.uniform(-1.2, 1.2)


lower = [(x, cradle_y(x)) for x in range(80, 829, 8)]
draw_stitch(lower)

img.save(OUT)
print("saved", OUT, img.size)
