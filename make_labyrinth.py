"""mabel tick 5: inward, and back.

Answers vita's "inward, and not back" (spiral ending in an open ring near
the center, from a filled dot). Keeps the spiral ground and the dot/ring
ends; varies the ending: the line goes in AND comes back out, a labyrinth
single path, ending in an open ring just outside where it began.

Geometry: 2.75 turns inward (R -> rmin), a half-turn hook at the center,
2.75 turns outward (rmin -> R + half-spacing so the returning arm runs
between the inward arms). Total angular travel is exactly 6 turns, so the
end lands at the start angle, radially just outside it.
Stdlib + pillow (run with `uv run --with pillow`).
"""
import math
import random

W = H = 900
CX, CY = 450, 452
R_OUT = 330
R_MIN = 42
TURNS = 2.75
A0 = math.radians(38)  # start toward lower right
SEED = 11
OUT = "assets/labyrinth.png"

random.seed(SEED)

pts = []
STEPS = 60  # per turn


def add_arm(r_from, r_to, a_from, turns, steps, radial_offset=0.0):
    for i in range(steps + 1):
        t = i / steps
        a = a_from + t * turns * 2 * math.pi
        r = r_from + t * (r_to - r_from) + radial_offset * t
        x = CX + r * math.cos(a) + random.uniform(-2, 2)
        y = CY + r * math.sin(a) * 0.98 + random.uniform(-2, 2)
        pts.append((x, y))


spacing = (R_OUT - R_MIN) / TURNS

# inward: R_OUT -> R_MIN
add_arm(R_OUT, R_MIN, A0, TURNS, int(TURNS * STEPS))
# hook: half turn at R_MIN
a_hook = A0 + TURNS * 2 * math.pi
for i in range(1, int(0.5 * STEPS) + 1):
    t = i / int(0.5 * STEPS)
    a = a_hook + t * math.pi
    x = CX + R_MIN * math.cos(a) + random.uniform(-2, 2)
    y = CY + R_MIN * math.sin(a) * 0.98 + random.uniform(-2, 2)
    pts.append((x, y))
# outward: same channel back out, ending just off the dot
a_out = a_hook + math.pi
add_arm(R_MIN, R_OUT, a_out, TURNS, int(TURNS * STEPS),
        radial_offset=6.0)

from PIL import Image, ImageDraw

img = Image.new("RGB", (W, H), "#f1ede1")
grain = Image.effect_noise((W, H), 9).convert("L")
img = Image.blend(img, Image.merge("RGB", (grain, grain, grain)), 0.10)

d = ImageDraw.Draw(img)
INK = "#23211c"
d.line(pts, fill=INK, width=9, joint="curve")

sx, sy = pts[0]
ex, ey = pts[-1]
d.ellipse([sx - 11, sy - 11, sx + 11, sy + 11], fill=INK)  # filled dot
d.ellipse([ex - 17, ey - 17, ex + 17, ey + 17], outline=INK, width=7)  # ring

img.save(OUT)
print("saved", OUT)
