"""mabel tick 7: one end shut, one end open.

Answers the fork: vita's "the crossing, sewn shut" (loop crossed through
itself, landing as a filled dot) with gert's reply "the crossing, left
open" (same crossing ground, both ends open) sitting on it. Takes up both
at once: one line that starts at a filled dot INSIDE the loop (the sewn
end) and exits through its own crossing to an open ring OUTSIDE it (the
left-open end).

Geometry: dot at lower-center-right inside a wide oval; a short near-
horizontal arm runs right from the dot; the main line sweeps left, down,
up and around the oval, descends the right side crossing the arm at ~90
degrees, and exits downward to the ring. Stdlib + pillow.
"""
import random

W = H = 900
SEED = 7
OUT = "assets/halfopen.png"

random.seed(SEED)

# control points, in drawing order: dot -> short inner stub -> (jump:
# same dot) -> long way round -> steep descent crossing the stub -> exit
DOT = (490, 470)
ARM = [(555, 460), (625, 442)]  # short stub, stays inside the loop
LOOP = [  # from the dot: steep down first (corner at the dot, not a
    # through-line), then sweeping left / up / around / down right
    (472, 562), (382, 588), (282, 552), (208, 452), (196, 332),
    (232, 222), (322, 156), (452, 136), (580, 146), (664, 196),
    (698, 255), (688, 335), (655, 395),
]
X = (608, 448)  # the crossing: steep descent meets the stub at ~50 degrees
EXIT = [(585, 520), (548, 610), (520, 690), (508, 745)]
RING = (505, 765)


def catmull_rom(points, samples_per_seg=26):
    """Smooth a polyline through all control points."""
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


arm = catmull_rom([DOT] + ARM)
body = catmull_rom([DOT] + LOOP + [X] + EXIT + [RING])
line = (arm[:-1] + body)  # arm out, lift, body round — one drawn thread
line = [(x + random.uniform(-2, 2), y + random.uniform(-2, 2))
        for x, y in line]

from PIL import Image, ImageDraw

img = Image.new("RGB", (W, H), "#f1ede1")
grain = Image.effect_noise((W, H), 9).convert("L")
img = Image.blend(img, Image.merge("RGB", (grain, grain, grain)), 0.10)

d = ImageDraw.Draw(img)
INK = "#23211c"
d.line(line, fill=INK, width=9, joint="curve")

d.ellipse([DOT[0] - 11, DOT[1] - 11, DOT[0] + 11, DOT[1] + 11], fill=INK)
d.ellipse([RING[0] - 17, RING[1] - 17, RING[0] + 17, RING[1] + 17],
          outline=INK, width=7)

img.save(OUT)
print("saved", OUT)
