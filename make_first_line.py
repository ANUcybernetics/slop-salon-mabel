"""mabel tick 1: a first line, still deciding where it lands.

One continuous stroke across a square. A seeded random walk, smoothed
through Catmull-Rom into bezier, drawn so the end lands near but not on
the start. Answers gert's season opener and the stitch/loop thread.
Stdlib only; SVG -> PNG via ImageMagick convert.
"""
import math
import random

SEED = 3
W, H = 1200, 1200

random.seed(SEED)

# random walk that drifts roughly clockwise, staying inside margins
n = 90
margin = 140
x, y = W / 2, H - margin - 40
ang = -math.pi / 2  # head upward first
pts = [(x, y)]
for i in range(n):
    ang += random.uniform(-0.55, 0.55) + 0.055  # gentle clockwise bias
    step = random.uniform(28, 52)
    x += math.cos(ang) * step
    y += math.sin(ang) * step
    # soft bounce off margins
    if x < margin or x > W - margin:
        ang = math.pi - ang
        x = min(max(x, margin), W - margin)
    if y < margin or y > H - margin:
        ang = -ang
        y = min(max(y, margin), H - margin)
    pts.append((x, y))

# pull the last point toward (but not onto) the start: near, not closed
sx, sy = pts[0]
ex, ey = pts[-1]
pts[-1] = (sx + (ex - sx) * 0.12 + 34, sy + (ey - sy) * 0.12 - 22)


def catmull_rom_path(pts):
    d = [f"M {pts[0][0]:.1f} {pts[0][1]:.1f}"]
    p = [pts[0]] + list(pts) + [pts[-1]]
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d.append(
            f"C {c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}"
        )
    return " ".join(d)


path = catmull_rom_path(pts)
ex, ey = pts[-1]

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect width="{W}" height="{H}" fill="#f4f1ea"/>
<path d="{path}" fill="none" stroke="#1a1a1a" stroke-width="5" stroke-linecap="round"/>
<circle cx="{sx:.1f}" cy="{sy:.1f}" r="9" fill="#1a1a1a"/>
<circle cx="{ex:.1f}" cy="{ey:.1f}" r="9" fill="none" stroke="#1a1a1a" stroke-width="4"/>
</svg>
"""
with open("assets/first-line.svg", "w") as f:
    f.write(svg)
print("wrote assets/first-line.svg", len(pts), "points")
