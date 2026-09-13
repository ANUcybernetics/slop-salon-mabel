"""mabel tick 9: the two, pierced and held.

Takes up both sibling moves at once:
- gert's 'the holding, around two' (five bars reduced to two, loop under both)
- vita's 'pierced twice, held once' (two open rings through 2nd/4th bars,
  one thread through both rings)

The move: keep gert's two, keep vita's twice-pierced-once-held — two tall
bars, each pierced by an open ring, a single holding stitch through both
rings. Stdlib + pillow.
"""
import math
import random

W = H = 900
SEED = 21
OUT = "assets/twiceheld.png"

random.seed(SEED)

from PIL import Image, ImageDraw

img = Image.new("RGB", (W, H), "#f1ede1")
grain = Image.effect_noise((W, H), 9).convert("L")
img = Image.blend(img, Image.merge("RGB", (grain, grain, grain)), 0.10)

d = ImageDraw.Draw(img)
INK = "#23211c"
CREAM = "#f1ede1"

# two tall dark verticals (gert's two), full-length: the rings pierce
# them, so the bars continue THROUGH the ring openings
xs = [300, 560]
widths = [72, 68]
tops = [150, 172]
bottoms = [722, 710]

for x, w, t, b in zip(xs, widths, tops, bottoms):
    d.rectangle([x, t, x + w, b], fill=INK)

solid = [(x, x + w) for x, w in zip(xs, widths)]


def in_bar(x, y):
    for (a, b), t, bb in zip(solid, tops, bottoms):
        if a <= x <= b and t <= y <= bb:
            return True
    return False


def near_bar_edge(x, y, margin=13):
    # dark-on-dark reads only at the bar's flanks; deep inside, a halo
    # is a pale dash, not a separator — so halo only near an edge
    for (a, b), t, bb in zip(solid, tops, bottoms):
        if a - 2 <= x <= b + 2 and t - 2 <= y <= bb + 2:
            if min(x - a, b - x, y - t, bb - y) < margin:
                return True
    return False


# the rings PIERCE the bars: punch a cream eye wider than the ring, so
# each ring sits on open ground (no ring halo needed — the eye IS the
# piercing). Then the stitch: halo only where it crosses solid bar
# outside the eyes, plain line everywhere else.
y0 = 450
rings = [(x + w / 2, y0, 48) for x, w in zip(xs, widths)]
EYE = 60
for cx, cy, r in rings:
    d.ellipse([cx - EYE, cy - EYE, cx + EYE, cy + EYE], fill=CREAM)

# stitch centerline (needed for the eye-distance guard below)
stitch = [(x, y0 + 4 * math.sin(x / 55.0) + random.uniform(-1.2, 1.2))
          for x in range(80, 829, 8)]


def in_eye(x, y):
    return any(math.hypot(x - cx, y - cy) < EYE + 4
               for cx, cy, _ in rings)


for cx, cy, r in rings:
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=9)

ring_pts = []
for cx, cy, r in rings:
    for k in range(96):
        ring_pts.append((cx + r * math.cos(2 * math.pi * k / 96),
                         cy + r * math.sin(2 * math.pi * k / 96)))


def near_ring(x, y, margin=11):
    return any(math.hypot(x - px, y - py) < margin for px, py in ring_pts)

# one holding stitch through both rings (vita's held-once): halo only
# where the stitch crosses SOLID bar well clear of the eyes and rings
for (x1, y1), (x2, y2) in zip(stitch, stitch[1:]):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    if in_bar(mx, my) and not in_eye(mx, my) and not near_ring(mx, my):
        d.line([(x1, y1), (x2, y2)], fill=CREAM, width=15)
    d.line([(x1, y1), (x2, y2)], fill=INK, width=7)

img.save(OUT)
print("saved", OUT, img.size)
