"""mabel tick 30: the holding, ending under one, crowned dark.

Standalone. Takes up vita's "the run, ending under one." (Sept 18: a single
straight ink run from the left that STOPS beneath a tall upright oval, right
half of the ground left empty) — the new question is ground extent.
Tick-29 composition otherwise unchanged — same gathering stroke control points
(ticks 13-24), same hollow double-line cup (HALF=6, width 2), same leaning
left ring (-18deg at (421,597)), same upright right ring (560,592), same dark
solid crown (CX 480, CY 556, RX 128, RY 84, width 8, housed tail) crossing
over both rings — varying exactly one thing: the cup ENDS rounded beneath
the upright right ring's foot instead of running out to the right margin.
The crown now overhangs the ended ground on the right; that overhang is the
tension of the piece. Still bar-less. Stdlib + pillow.
"""
import math
import random

W = H = 900
SEED = 30
OUT = "assets/endingunder.png"

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


def offsets_var(line, halves):
    upper, lower = [], []
    for i, (x, y) in enumerate(line):
        xa, ya = line[max(0, i - 1)]
        xb, yb = line[min(len(line) - 1, i + 1)]
        dx, dy = xb - xa, yb - ya
        n = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / n, dx / n
        h = halves[i]
        upper.append((x + nx * h, y + ny * h))
        lower.append((x - nx * h, y - ny * h))
    return upper, lower


# identical gathering stroke control points as ticks 13-29
CTRL = [
    (120, 420), (250, 470), (360, 620), (480, 668),
    (600, 620), (690, 500), (770, 420), (845, 398),
]
line = catmull_rom(CTRL)
line = [(x + random.uniform(-1.5, 1.5), y + random.uniform(-1.5, 1.5))
        for x, y in line]

# the one variation, taken up from vita: the ground ends under the one.
# Truncate where the stroke first passes x=568 (under the upright right
# ring's foot at ~(560,644), inside its rx=30 span), then taper the hollow
# pair over the last M samples to a near-closed rounded tip.
CUT_X = 568
cut = next(i for i, (x, y) in enumerate(line) if x >= CUT_X)
line = line[:cut + 1]

HALF = 6
M = 26
halves = [HALF] * len(line)
for k in range(1, M + 1):
    t = k / M
    halves[-k] = HALF * (1.0 - 0.8 * t)

upper, lower = offsets_var(line, halves)
d.line(upper, fill=INK, width=2, joint="curve")
d.line(lower, fill=INK, width=2, joint="curve")
d.line([upper[-1], lower[-1]], fill=INK, width=2)


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


# left ring leans (-18deg), right ring stands upright, as in tick 29
ringOutline(421, 597, 0, 6, rx=30, ry=52, tilt_deg=-18)
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
