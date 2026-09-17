#!/usr/bin/env python3
"""Half-power figure: effective bandwidth vs message size for three links, one log-log panel.
x: message size, 1 B to 1 MB, labelled at every power of 4, minor vertical lines at the other powers of 2.
y: bandwidth in Gb/s, 0.001 to 100, decades labelled, minors 2..9. Every marker sits on a gridline crossing.
SVG 1500x1000, rendered by headless Chrome at 2x -> 3000x2000."""
import math, json, os, subprocess
MARKERS_ONLY = os.environ.get("MARKERS_ONLY") == "1"
W, H = 1500, 1000
FONT = "DejaVu Sans, Liberation Sans, Arial, sans-serif"
MAJOR = "#8c8c8c"; MINOR = "#c8c8c8"; INK = "#000000"
P = dict(l=150, t=50, r=1440, b=880)
SIZES = [4 ** k for k in range(11)]                     # 1 B .. 1 MB
LABELS = ["1 B", "4 B", "16 B", "64 B", "256 B", "1 KB", "4 KB", "16 KB", "64 KB", "256 KB", "1 MB"]
CURVES = {
    "Link A": [0.008, 0.03, 0.1, 0.5, 2, 8, 30, 50, 60, 80, 90],
    "Link B": [0.005, 0.02, 0.08, 0.3, 1, 3, 6, 7, 8, 8, 8],
    "Link C": [0.003, 0.01, 0.05, 0.2, 0.8, 2, 9, 40, 80, 60, 60],
}
def xs(v): return P["l"] + (P["r"] - P["l"]) * math.log2(v) / 20.0
def ys(v): return P["b"] - (P["b"] - P["t"]) * (math.log10(v) + 3) / 5.0
out = []
def add(s):
    if MARKERS_ONLY and not (s.startswith("<circle") or s.startswith("<rect x=") or s.startswith("<polygon")): return
    out.append(s)
def text(x, y, s, size=22, anchor="middle", rot=False):
    tr = f' transform="rotate(-90 {x} {y})"' if rot else ""
    add(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" fill="{INK}" text-anchor="{anchor}"{tr}>{s}</text>')
def line(x1, y1, x2, y2, col, w=1.0):
    add(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{col}" stroke-width="{w}"/>')
# grid
for k in range(21):
    x = xs(2 ** k); major = k % 2 == 0
    line(x, P["t"], x, P["b"], MAJOR if major else MINOR, 1.0)
    if major: text(x, P["b"] + 30, LABELS[k // 2], 20)
for d in range(-3, 3):
    for m in range(1, 10):
        v = m * 10 ** d
        if v > 100: break
        y = ys(v); major = m == 1
        line(P["l"], y, P["r"], y, MAJOR if major else MINOR, 1.0)
        if major: text(P["l"] - 12, y + 7, ("%g" % v), 20, "end")
# curves
R = 5.0
def marker(kind, x, y):
    if kind == "circle": add(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{R}" fill="{INK}"/>')
    elif kind == "square": add(f'<rect x="{x-R:.2f}" y="{y-R:.2f}" width="{2*R}" height="{2*R}" fill="#ffffff" stroke="{INK}" stroke-width="1.6"/>')
    else:
        h = R * 1.35
        add(f'<polygon points="{x:.2f},{y-h:.2f} {x+h:.2f},{y:.2f} {x:.2f},{y+h:.2f} {x-h:.2f},{y:.2f}" fill="{INK}"/>')
KIND = {"Link A": "circle", "Link B": "square", "Link C": "diamond"}
truth = {}
for name, vals in CURVES.items():
    pts = [(xs(s), ys(v)) for s, v in zip(SIZES, vals)]
    add('<polyline fill="none" stroke="%s" stroke-width="1.6" points="%s"/>' % (INK, " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)))
    for (x, y), s, v in zip(pts, SIZES, vals):
        marker(KIND[name], x, y); truth[f"{name}:{s}"] = [round(x, 3), round(y, 3), v]
# frame, titles
line(P["l"], P["t"], P["l"], P["b"], INK, 1.5); line(P["l"], P["b"], P["r"], P["b"], INK, 1.5)
text(P["l"] - 95, (P["t"] + P["b"]) / 2, "Effective bandwidth (Gb/s)", 24, rot=True)
text((P["l"] + P["r"]) / 2, P["b"] + 72, "Message size", 24)
# legend, bottom right, inside the frame
lx, ly = P["r"] - 250, P["b"] - 130
if MARKERS_ONLY: lx = -1000
add(f'<rect x="{lx-20}" y="{ly-30}" width="220" height="118" fill="#ffffff" stroke="{INK}" stroke-width="1.0"/>')
for i, name in enumerate(CURVES):
    y = ly + i * 36
    line(lx, y, lx + 50, y, INK, 1.6); marker(KIND[name], lx + 25, y); text(lx + 66, y + 7, name, 20, "start")
svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n<rect width="{W}" height="{H}" fill="#ffffff"/>\n' + "\n".join(out) + "\n</svg>"
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
open(f"{here}/fig.svg", "w").write(svg)
open(f"{here}/fig.html", "w").write(f'<html><body style="margin:0;background:#fff"><img src="fig.svg" width="{W}" height="{H}"></body></html>')
json.dump(truth, open(f"{here}/truth.json", "w"), indent=1)
subprocess.run([os.environ.get("CHROME", "google-chrome"), "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                f"--user-data-dir={here}/.chrome", "--force-device-scale-factor=2", f"--window-size={W},{H}",
                f"--screenshot={root}/" + ("markers_only.png" if MARKERS_ONLY else "image.png"), f"file://{here}/fig.html"], check=True, capture_output=True, timeout=120)
print("rendered", "markers_only.png" if MARKERS_ONLY else "image.png")
