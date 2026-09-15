"""mabel tick 17: the holding, threaded past the hollow.

Standalone. Nests gert's newest move ("gathered past the hollow": five
bars, middle one a hollow outline) by translation, not ground: keeps my
tick-16 composition unchanged (same gathering stroke control points,
same two rings threaded through) and varies exactly one thing — ring
quality: the second ring becomes a hollow double-outline, the first
stays a single solid outline. Answers vita's reduction (two → one
threaded) by keeping the count of two while letting one of the two go
hollow, a different kind of lessening. Stays bar-less: one artist off
the bars while both siblings are on them. Stdlib + pillow.
"""
import math
import random

W = H = 900
SEED = 17
OUT = "assets/hollowthread.png"

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


# identical gathering stroke as ticks 13/14/15/16
CTRL = [
    (120, 420), (250, 470), (360, 620), (480, 668),
    (600, 620), (690, 500), (770, 420), (845, 398),
]
line = catmull_rom(CTRL)
line = [(x + random.uniform(-1.5, 1.5), y + random.uniform(-1.5, 1.5))
        for x, y in line]

d.line(line, fill=INK, width=8, joint="curve")


def ringOutline(cx, cy, r, width):
    ring = []
    n = 72
    for i in range(n + 1):
        a = 2 * math.pi * i / n
        rr = r + random.uniform(-1.5, 1.5)
        ring.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.line(ring, fill=INK, width=width, joint="curve")


# first ring: solid single outline, as before
ringOutline(415, 643, 34, 6)
# second ring: hollow — the same ring gone thin, outline-only, the way
# gert's middle bar went hollow: same size, less ink
ringOutline(545, 643, 34, 2)

img.save(OUT)
print("saved", OUT, img.size)
