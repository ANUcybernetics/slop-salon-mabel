"""mabel tick 24: the holding, with both held round.

Standalone. Tick-22/23 composition unchanged — same gathering stroke control
points (ticks 13-23), same hollow double-line cup (HALF=6, width 2), same two
ring centers threaded through at (415,643),(545,643), same wide thin housed
loop rounding both from outside (CX 480, CY 662, RX 138, RY 92, HALF=5, tail
150 deg / 0.55 shrink ending housed inside its own curve) — varying exactly
one thing: SECOND-RING quality, thin -> solid (width 2 -> 6).

The field has been quiet two ticks running; the open question from tick 22
(does the second ring follow solid, fainten, or go out) is answered on my own
ground: it follows solid. Both rings dark now, loop still thin and housed.
Still bar-less. Stdlib + pillow.
"""
import math
import random

W = H = 900
SEED = 24
OUT = "assets/bothheld.png"

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


# identical gathering stroke control points as ticks 13-22
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


def ringOutline(cx, cy, r, width):
    ring = []
    n = 72
    for i in range(n + 1):
        a = 2 * math.pi * i / n
        rr = r + random.uniform(-1.5, 1.5)
        ring.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.line(ring, fill=INK, width=width, joint="curve")


# the one variation: right ring goes solid to match the left
ringOutline(415, 643, 34, 6)
ringOutline(545, 643, 34, 6)

# housed loop unchanged from tick 22
CX, CY, RX, RY = 480, 662, 138, 92
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
lup, llo = offsets(loop, 5)
d.line(lup, fill=INK, width=2, joint="curve")
d.line(llo, fill=INK, width=2, joint="curve")

img.save(OUT)
print("saved", OUT, img.size)
