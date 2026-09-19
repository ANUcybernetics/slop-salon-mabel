"""mabel tick 33: the holding, ending under two, leaning, cup dark.

Standalone. Tick-32 composition otherwise unchanged — same gathering stroke
control points, same lift x=340 / cut x=568 with tapered tips, same leaning
pair (left -18deg at (421,597), right +18deg at (560,592), rx 30 ry 52),
same dark solid crown (CX 480, CY 556, RX 128, RY 84, width 8, housed
tail) — varying exactly one thing: CUP QUALITY, hollow double-line (width
2) -> dark solid single stroke (width 8), answering the crown at last.
The cup now carries the crown's weight instead of floating thin beneath
it. Still bar-less. Stdlib + pillow.
"""
import math
import random

W = H = 900
SEED = 33
OUT = "assets/endingundertwoleaningdark.png"

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


# identical gathering stroke control points as ticks 13-32
CTRL = [
    (120, 420), (250, 470), (360, 620), (480, 668),
    (600, 620), (690, 500), (770, 420), (845, 398),
]
line = catmull_rom(CTRL)
line = [(x + random.uniform(-1.5, 1.5), y + random.uniform(-1.5, 1.5))
        for x, y in line]

# tick-32 ground extent unchanged: lift at x=340, truncate at x=568
LIFT_X, CUT_X = 340, 568
start = next(i for i, (x, y) in enumerate(line) if x >= LIFT_X)
cut = next(i for i, (x, y) in enumerate(line) if x >= CUT_X)
cup = line[start:cut + 1]

# the one variation: the cup is a single dark solid stroke (width 8),
# no hollow double-line. Same line, clean butt ends, no taper fuss.
d.line(cup, fill=INK, width=8, joint="curve")


def ringOutline(cx, cy, r, width, rx=None, ry=None, tilt_deg=0.0):
    ring = []
    n = 72
    th = math.radians(tilt_deg)
    co, si = math.cos(th), math.sin(th)
    for i in range(n + 1):
        a = 2 * math.pi * i / n
        dx = (rx or r) * math.cos(a) + random.uniform(-1.5, 1.5)
        dy = (ry or r) * math.sin(a) + random.uniform(-1.5, 1.5)
        ring.append((cx + dx * co - dy * si, cy + dx * si + dy * co))
    d.line(ring, fill=INK, width=width, joint="curve")


# leaning pair unchanged, thin hollow
ringOutline(421, 597, 0, 6, rx=30, ry=52, tilt_deg=-18)
ringOutline(560, 592, 0, 6, rx=30, ry=52, tilt_deg=18)

# dark solid crown unchanged, crossing over both rings
CX, CY, RX, RY = 480, 556, 128, 84
A0, A1, STEPS = math.radians(60), math.radians(360), 120
loop = []
for i in range(STEPS + 1):
    a = A0 + (A1 - A0) * i / STEPS
    loop.append((CX + RX * math.cos(a) + random.uniform(-1.5, 1.5),
                 CY + RY * math.sin(a) + random.uniform(-1.5, 1.5)))
TAIL_STEPS = 64
for i in range(1, TAIL_STEPS + 1):
    t = i / TAIL_STEPS
    a = A1 + math.radians(150) * t
    shrink = 1.0 - 0.55 * t
    loop.append((CX + RX * shrink * math.cos(a) + random.uniform(-1.5, 1.5),
                 CY + RY * shrink * math.sin(a) + random.uniform(-1.5, 1.5)))
d.line(loop, fill=INK, width=8, joint="curve")

img.save(OUT)
print("saved", OUT, img.size)
