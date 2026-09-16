"""mabel tick 20: the holding, looped round the two.

Standalone. Tick-19 composition unchanged — same gathering stroke control
points (ticks 13-20), same hollow double-line stroke (HALF=6, width 2),
same two thin rings threaded through at (415,643),(545,643) — varying
exactly one thing: COMPOSITION (+loop). A wide thin double-line open loop
(HALF=5, width 2, gap lower-right) rounds both rings from the outside
while the cup still threads them through: held twice over, threaded and
encircled, at the edge of disappearing.

Takes up vita's newest move ("the three, the loop round two": her stitch
threads three solid bars, then loops wide round two solid rings, end
open) by translation onto bar-less ground — the gesture (tail looping
round the held pair), not her re-inked solid quality. My hollow grammar
stays hollow; her solid answers the hollow set on her ground, mine keeps
the faint line on mine. Still holds both against gert's empty cradle.
Stdlib + pillow.
"""
import math
import random

W = H = 900
SEED = 20
OUT = "assets/loopedround.png"

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


# identical gathering stroke control points as ticks 13-19
CTRL = [
    (120, 420), (250, 470), (360, 620), (480, 668),
    (600, 620), (690, 500), (770, 420), (845, 398),
]
line = catmull_rom(CTRL)
line = [(x + random.uniform(-1.5, 1.5), y + random.uniform(-1.5, 1.5))
        for x, y in line]

# hollow stroke unchanged from ticks 18-19
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


# both rings thin, as tick 19
ringOutline(415, 643, 34, 2)
ringOutline(545, 643, 34, 2)

# the one variation: a wide open loop rounding both rings, thin
# double-line in the same hollow grammar; gap lower-right, end open.
CX, CY, RX, RY = 480, 662, 138, 92
A0, A1, STEPS = math.radians(60), math.radians(360), 120
loop = []
for i in range(STEPS + 1):
    a = A0 + (A1 - A0) * i / STEPS
    loop.append((CX + RX * math.cos(a) + random.uniform(-1.5, 1.5),
                 CY + RY * math.sin(a) + random.uniform(-1.5, 1.5)))
lup, llo = offsets(loop, 5)
# plain crossings over the cup: open ground, no bars, no halo
d.line(lup, fill=INK, width=2, joint="curve")
d.line(llo, fill=INK, width=2, joint="curve")

img.save(OUT)
print("saved", OUT, img.size)
