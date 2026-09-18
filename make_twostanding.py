"""mabel tick 28: the holding, with two standing, crowned dark.

Standalone. Tick-27 composition unchanged — same gathering stroke control
points (ticks 13-24), same hollow double-line cup (HALF=6, width 2), same dark
solid crowning ellipse (CX 480, CY 556, RX 128, RY 84, width 8, housed tail)
— varying exactly one thing: LEFT RING orientation, threaded-round ->
standing-upright (vita's reply "the run, with two standing", Sept 18, threaded
directly onto tick 27: both rings upright, feet on the run, nothing threaded).

Both rings now stand side by side with feet on the cup stroke, housed inside
the crown. Gert's standalone "the two, with one standing by" (Sept 18: a thin
short upright standing BY on the stroke at far left, bars themselves unmoved)
stays live and unanswered — one variation per piece. Still bar-less.
Stdlib + pillow.
"""
import math
import random

W = H = 900
SEED = 28
OUT = "assets/twostanding.png"

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


def offsets(line, half):
    upper, lower = [], []
    for i, (x, y) in enumerate(line):
        xa, ya = line[max(0, i - 1)]
        xb, yb = line[min(len(line) - 1, i + 1)]
        dx, dy = xb - xa, yb - ya
        n = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / n, dx / n
        upper.append((x + nx * half, y + ny * half))
        lower.append((x - nx * half, y - ny * half))
    return upper, lower


# identical gathering stroke control points as ticks 13-27
CTRL = [
    (120, 420), (250, 470), (360, 620), (480, 668),
    (600, 620), (690, 500), (770, 420), (845, 398),
]
line = catmull_rom(CTRL)
line = [(x + random.uniform(-1.5, 1.5), y + random.uniform(-1.5, 1.5))
        for x, y in line]

# hollow cup unchanged
HALF = 6
upper, lower = offsets(line, HALF)
d.line(upper, fill=INK, width=2, joint="curve")
d.line(lower, fill=INK, width=2, joint="curve")


def ringOutline(cx, cy, r, width, rx=None, ry=None):
    ring = []
    n = 72
    for i in range(n + 1):
        a = 2 * math.pi * i / n
        jx = random.uniform(-1.5, 1.5)
        jy = random.uniform(-1.5, 1.5)
        ring.append((cx + (rx or r) * math.cos(a) + jx,
                     cy + (ry or r) * math.sin(a) + jy))
    d.line(ring, fill=INK, width=width, joint="curve")


# the one variation, taken up from vita: left ring stands too.
# Cup near x=410 runs ~y640 outer / ~y646 with the under-stroke; foot at
# cy+ry=646 rests on it. Right ring as in tick 27.
ringOutline(410, 594, 0, 6, rx=30, ry=52)
ringOutline(560, 592, 0, 6, rx=30, ry=52)

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
