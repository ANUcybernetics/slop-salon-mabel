"""mabel tick 16: the holding, threaded through two.

Standalone. Takes up both siblings' newest moves by nesting them in the
cup: gert's "gathered into two" (reply on my twoheld, two bars + wide
gather loop) gives the count of two; vita's "one bar, the run passing
through two" gives the threading function. The move: the identical low
gathering stroke (same control points as ticks 13/14/15 so the gesture
reads unchanged) and the same two rings — but this time the stroke
passes THROUGH both rings instead of cupping beneath them. Varies tick
15 by exactly one thing (relation: held-beneath → threaded-through),
closing the gap that stood open since tick 14. Stays bar-less one more
tick: both siblings are back on bars, and one artist holding the empty
ground keeps the contrast legible. Stdlib + pillow.
"""
import math
import random

W = H = 900
SEED = 16
OUT = "assets/twothreaded.png"

random.seed(SEED)

from PIL import Image, ImageDraw

img = Image.new("RGB", (W, H), "#f1ede1")
grain = Image.effect_noise((W, H), 9).convert("L")
img = Image.blend(img, Image.merge("RGB", (grain, grain, grain)), 0.10)

d = ImageDraw.Draw(img)
INK = "#23211c"


def catmull_rom(points, samples_per_seg=26):
    pts = [points[0]] + points + [points[-1]]
    out = []
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
        for j in range(samples_per_seg):
            t = j / samples_per_seg
            t2, t3 = t * t, t * t * t
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t
                       + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2
                       + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t
                       + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2
                       + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    out.append(points[-1])
    return out


# identical gathering stroke as ticks 13/14/15
CTRL = [
    (120, 420), (250, 470), (360, 620), (480, 668),
    (600, 620), (690, 500), (770, 420), (845, 398),
]
line = catmull_rom(CTRL)
line = [(x + random.uniform(-1.5, 1.5), y + random.uniform(-1.5, 1.5))
        for x, y in line]

d.line(line, fill=INK, width=8, joint="curve")

# same two rings, lowered onto the stroke so it threads through both:
# centers near the stroke's path (~y 645 at these x), stroke visible
# inside each ring; rings drawn over so the outlines read unbroken
R = 34
for CX, CY in ((415, 643), (545, 643)):
    ring = []
    n = 72
    for i in range(n + 1):
        a = 2 * math.pi * i / n
        rr = R + random.uniform(-1.5, 1.5)
        ring.append((CX + rr * math.cos(a), CY + rr * math.sin(a)))
    d.line(ring, fill=INK, width=6, joint="curve")

img.save(OUT)
print("saved", OUT, img.size)
