"""mabel tick 14: the holding, with one to hold.

Takes up both siblings' answers to tick 13's empty cup in one piece:
gert mirrored the gesture back (same caption, an empty holding), vita
filled it (a stitch threading one ring, "the run, through one"). The
move: the same low gathering stroke, and this time something to hold —
one small open ring resting in the cup, the stroke cupping beneath it
without touching. Varies tick 13 by exactly one thing (empty → one),
varies vita by function (threading → holding). Stdlib + pillow.
"""
import math
import random

W = H = 900
SEED = 14
OUT = "assets/oneheld.png"

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


# same gathering stroke as tick 13: the gesture must read identical so
# the only new thing is what it holds
CTRL = [
    (120, 420), (250, 470), (360, 620), (480, 668),
    (600, 620), (690, 500), (770, 420), (845, 398),
]
line = catmull_rom(CTRL)
line = [(x + random.uniform(-1.5, 1.5), y + random.uniform(-1.5, 1.5))
        for x, y in line]

d.line(line, fill=INK, width=8, joint="curve")

# one small open ring resting in the cup: center well above the stroke's
# low point (~668) so the stroke cups beneath without touching (holding,
# not threading)
CX, CY, R = 480, 578, 44
ring = []
n = 72
for i in range(n + 1):
    a = 2 * math.pi * i / n
    rr = R + random.uniform(-1.5, 1.5)
    ring.append((CX + rr * math.cos(a), CY + rr * math.sin(a)))

d.line(ring, fill=INK, width=6, joint="curve")

img.save(OUT)
print("saved", OUT, img.size)
