#!/usr/bin/env python3
"""Validity check. Gridlines are found in image.png by scanning. Marker centres are found as ink
blobs in markers_only.png, a render of the same script with nothing but the markers. Each marker
centre must sit on the gridline crossing for its size and value."""
import json, math, os
from PIL import Image
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
im = Image.open(f"{root}/image.png").convert("L"); px = im.load()
mo = Image.open(f"{root}/markers_only.png").convert("L"); mp = mo.load()
W, H = im.size; S = 2
L, T, R, B = 150 * S, 50 * S, 1440 * S, 880 * S
truth = json.load(open(f"{here}/truth.json"))
def groups(idx, gap=1):
    g = []
    for i in idx:
        if g and i - g[-1][-1] <= gap: g[-1].append(i)
        else: g.append([i])
    return [sum(r) / len(r) for r in g]
# gridline census, light grey ink only, sampled in a column and row clear of everything else
def grey(x, y): return 120 < px[x, y] < 235
hrows = groups([y for y in range(T - 3, B + 3) if sum(grey(x, y) for x in (L + 30, L + 700, L + 1200, R - 30)) >= 3])
vcols = groups([x for x in range(L + 2, R + 3) if sum(grey(x, y) for y in (B - 30, B - 600, B - 900, T + 250, T + 400)) >= 3])
print(f"{len(hrows)} horizontal gridlines (expect 46), {len(vcols)} vertical (expect 20 beyond the axis)")
def row_of(v):  # nearest census row to the value, and its distance in px
    y = B - (B - T) * (math.log10(v) + 3) / 5.0
    r = min(hrows, key=lambda q: abs(q - y)); return r, abs(r - y)
def col_of(s):
    x = L + (R - L) * math.log2(s) / 20.0
    if s == 1: return L, 0.0
    c = min(vcols, key=lambda q: abs(q - x)); return c, abs(c - x)
# blobs in markers-only image
vis = [[False] * H for _ in range(0)]
seen = set(); blobs = []
for y in range(H):
    for x in range(W):
        if mp[x, y] < 128 and (x, y) not in seen:
            stack = [(x, y)]; seen.add((x, y)); pts = []
            while stack:
                cx, cy = stack.pop(); pts.append((cx, cy))
                for nx, ny in ((cx+1,cy),(cx-1,cy),(cx,cy+1),(cx,cy-1)):
                    if 0 <= nx < W and 0 <= ny < H and mp[nx, ny] < 128 and (nx, ny) not in seen:
                        seen.add((nx, ny)); stack.append((nx, ny))
            xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
            blobs.append(((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, len(pts)))
print(f"{len(blobs)} marker blobs found (expect 33)")
ok = True
for name, (gx, gy, v) in truth.items():
    link, size = name.split(":"); size = int(size)
    c, dc = col_of(size); r, dr = row_of(v)
    bx, by, n = min(blobs, key=lambda b: (b[0] - c) ** 2 + (b[1] - r) ** 2)
    off = math.hypot(bx - c, by - r)
    good = off <= 1.5 and dc <= 1.5 and dr <= 1.5; ok &= good
    print(f"{'OK ' if good else 'BAD'} {link} {size:>8} B  value {v:<6} crossing ({c:.1f},{r:.1f}) marker ({bx:.1f},{by:.1f}) off {off:.2f} px")
print("ALL MARKERS ON THEIR CROSSINGS" if ok else "PROBLEM")
