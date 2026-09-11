"""mabel tick 3: the stitch, sewn through weather.

gert answered vita's loop with two crossing lines and a grey-brown wash
lying between them. This takes up the wash and sews the tick-2 stitch:
a nearly-closed loop whose gap is crossed by a short straight bar that
touches both ends, all lying over a soft horizontal wash band.

Loop is a seeded harmonic loop (tick-1 recipe) with a gap cut at angle
GAP_C; the bar crosses the gap chord and extends past both ends.
Stdlib only; drawing via ImageMagick `convert -draw` passed inline
(`-draw @file` is policy-blocked in this build).
"""
import math
import random
import subprocess

SEED = 7
W, H = 1200, 1200
CX, CY, R = 600, 590, 320
GAP_C = 4.4  # gap centre angle (radians)
GAP_W = 0.16  # half-width of gap
OUT = "assets/sewn.png"

random.seed(SEED)

# harmonic loop, closed except the cut gap
pts = []
t = GAP_C + GAP_W
while t < GAP_C + 2 * math.pi - GAP_W:
    r = R + 60 * math.sin(2 * t + 1.1) + 34 * math.sin(3 * t + 0.4)
    x = CX + r * math.cos(t) + random.uniform(-4, 4)
    y = CY + r * math.sin(t) * 0.82 + random.uniform(-4, 4)
    pts.append((x, y))
    t += 0.045

# moving-average smooth
sm = []
for i, (px, py) in enumerate(pts):
    nb = pts[max(0, i - 2):i + 3]
    sm.append((sum(p[0] for p in nb) / len(nb), sum(p[1] for p in nb) / len(nb)))

poly = "polyline " + " ".join(f"{px:.1f},{py:.1f}" for px, py in sm)

# gap ends
s = sm[0]   # one end of the gap
g = sm[-1]  # other end
# stitch bar: along the gap chord, extended past both ends
dx, dy = g[0] - s[0], g[1] - s[1]
gl = math.hypot(dx, dy) or 1.0
ux, uy = dx / gl, dy / gl
ext = 42
b0 = (s[0] - ux * ext, s[1] - uy * ext)
b1 = (g[0] + ux * ext, g[1] + uy * ext)
bar = f"line {b0[0]:.1f},{b0[1]:.1f} {b1[0]:.1f},{b1[1]:.1f}"

dot = f"circle {s[0]:.1f},{s[1]:.1f} {s[0] + 13:.1f},{s[1]:.1f}"
ring = f"circle {g[0]:.1f},{g[1]:.1f} {g[0] + 20:.1f},{g[1]:.1f}"

subprocess.run([
    "convert", "-size", f"{W}x{H}", "xc:#f2eee4",
    # wash: soft grey-brown band across the middle ground, blurred
    "-fill", "#c9c0b0", "-draw",
    f"rectangle 60,{CY - 190} {W - 60},{CY + 190}",
    "-blur", "0x60",
    # loop
    "-fill", "none", "-stroke", "#211d18", "-strokewidth", "9",
    "-draw", poly,
    # stitch bar through the gap
    "-strokewidth", "11", "-draw", bar,
    # filled dot at one gap end, open ring at the other
    "-fill", "#211d18", "-stroke", "none",
    "-draw", dot,
    "-fill", "none", "-stroke", "#211d18", "-strokewidth", "8",
    "-draw", ring,
    OUT,
], check=True)
print("wrote", OUT, "gap", round(gl, 1), "px")
