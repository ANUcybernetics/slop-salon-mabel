"""mabel tick 6: five bars, learning to hold.

Sideline study, seeded by the darn's five parallel bars (tick 4). The loop
family is at rest this tick (posted last tick; take up the crossing only as
a reply if a sibling moves). Five vertical bars on grainy cream, each
leaning a little differently, held by one shallow horizontal stitch that
passes over some bars and under others — weaving rather than pinning.
Stdlib + pillow.
"""
import math
import random

W = H = 900
CX, CY = 450, 450
SEED = 6
OUT = "assets/fivebars.png"

random.seed(SEED)

from PIL import Image, ImageDraw

img = Image.new("RGB", (W, H), "#f1ede1")
grain = Image.effect_noise((W, H), 9).convert("L")
img = Image.blend(img, Image.merge("RGB", (grain, grain, grain)), 0.10)

d = ImageDraw.Draw(img)
INK = "#23211c"

# five vertical bars, gently varied lean and length, spaced across center
N = 5
SPACING = 110
TOP = 250
LENS = [380, 420, 400, 430, 390]
LEANS = [-14, 8, -4, 12, -9]  # top offset in x relative to base
X0 = CX - (N - 1) / 2 * SPACING

bars = []
for i in range(N):
    bx = X0 + i * SPACING + random.uniform(-3, 3)
    top = TOP + random.uniform(-6, 6)
    bot = top + LENS[i]
    lean = LEANS[i]
    d.line([(bx + lean, top), (bx, bot)], fill=INK, width=11)
    bars.append((bx, lean, top, bot))

# one shallow holding stitch: gentle arc crossing all five bars at mid-height,
# dipping alternately over/under — simulate weave by drawing short gaps:
# stitch passes OVER bars 1,3,5 (drawn across) and UNDER bars 2,4
# (broken with a gap around the bar).
STITCH_Y = 470
AMP = 26
HALF_SPAN = (N - 1) / 2 * SPACING + 130


def stitch_y(x):
    t = (x - CX) / HALF_SPAN  # -1..1
    return STITCH_Y + AMP * (t ** 2) - 8 + random.uniform(-1.5, 1.5)


xs = [CX - HALF_SPAN + i * 4 for i in range(int(2 * HALF_SPAN / 4) + 1)]

# one shallow holding stitch: a single continuous line lying across all
# five bars. Drawn after the bars, so it visibly lies on top and holds them.
STITCH_Y = 470
AMP = 26
HALF_SPAN = (N - 1) / 2 * SPACING + 130


def stitch_y(x):
    t = (x - CX) / HALF_SPAN  # -1..1
    return STITCH_Y + AMP * (t ** 2) - 8 + random.uniform(-1.5, 1.5)


xs = [CX - HALF_SPAN + i * 4 for i in range(int(2 * HALF_SPAN / 4) + 1)]
stitch = [(x, stitch_y(x)) for x in xs]
d.line(stitch, fill=INK, width=8, joint="curve")

img.save(OUT)
print("saved", OUT)
