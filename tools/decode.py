#!/usr/bin/env python3
"""Read every plotted value back out of image.png and compare with the ground truth."""
import math, sys
from PIL import Image

im = Image.open(sys.argv[1] if len(sys.argv) > 1 else "image.png").convert("RGB")
px = im.load()

def dark(p, t=90):   # frame / data ink
    return p[0] < t and p[1] < t and p[2] < t
def grey(p):        # gridline ink, either weight
    return 140 < p[0] < 235 and abs(p[0]-p[1]) < 6 and abs(p[1]-p[2]) < 6

def gridrows(x, y0, y1):
    rows = [y for y in range(y0, y1) if grey(px[x, y])]
    # merge adjacent rows
    out = []
    for y in rows:
        if out and y - out[-1][-1] <= 1: out[-1].append(y)
        else: out.append([y])
    return [sum(r)/len(r) for r in out]

def dark_rows(x, y0, y1):
    return [y for y in range(y0, y1) if dark(px[x, y])]

def runs(ys):
    out = []
    for y in ys:
        if out and y - out[-1][-1] <= 1: out[-1].append(y)
        else: out.append([y])
    return out

ok = True
def check(label, got, want, tol):
    global ok
    flag = abs(got - want) <= tol
    ok &= flag
    print(f"{'OK ' if flag else 'BAD'} {label}: read {got:.4f} want {want}")

# ---------------- panel (a): frame 215..1380 x 140..940, y 80..100 linear
A = dict(x0=215, y0=140, x1=1380, y1=940)
def a_val(y): return 100 - (y - A["y0"]) / (A["y1"] - A["y0"]) * 20
g = gridrows(A["x0"] + 40, A["y0"] + 3, A["y1"] - 3)
print(f"panel (a): {len(g)} horizontal gridlines found (expect 19 interior), spacing {(g[-1]-g[0])/(len(g)-1):.2f} px")
HIST = [2, 4, 6, 8, 10, 12, 14, 16]
GSHARE = [86, 88, 90, 91, 92, 93, 93, 92]
TOURN  = [90, 92, 93, 94, 95, 95, 96, 96]
for hv, gs, tn in zip(HIST, GSHARE, TOURN):
    x = round(A["x0"] + (hv - 2) / 14 * (A["x1"] - A["x0"]))
    # scan a column 3 px left of the vertical gridline: filled circle gives a long dark run,
    # open square gives two short runs 22 px apart
    col = dark_rows(x - 3, A["y0"] + 2, A["y1"] - 2)
    rs = [r for r in runs(col) if len(r) >= 2]
    # circle: run length ~ 24 ; square: two runs of ~3 separated by ~19
    circ = [r for r in rs if len(r) >= 18]
    sq = [r for r in rs if 2 <= len(r) <= 6]
    if circ:
        yc = (circ[0][0] + circ[0][-1]) / 2
        check(f"(a) gshare @ {hv}", a_val(yc), gs, 0.06)
    else:
        print("BAD (a) no circle at", hv); ok = False
    if len(sq) >= 2:
        # pick the pair separated by ~19-22 px
        best = None
        for i in range(len(sq)):
            for j in range(i+1, len(sq)):
                d = sq[j][0] - sq[i][-1]
                if 15 <= d <= 24 and best is None:
                    best = ((sq[i][0] + sq[j][-1]) / 2)
        if best is not None:
            check(f"(a) tournament @ {hv}", a_val(best), tn, 0.06)
        else:
            print("BAD (a) no square pair at", hv, [ (r[0], len(r)) for r in sq]); ok = False
    else:
        print("BAD (a) no square at", hv); ok = False

# ---------------- panel (b): frame 1660..2820 x 140..940, y 0..100
B = dict(x0=1660, y0=140, x1=2820, y1=940)
def b_val(y): return 100 - (y - B["y0"]) / (B["y1"] - B["y0"]) * 100
g = gridrows(B["x0"] + 12, B["y0"] + 3, B["y1"] - 3)
print(f"panel (b): {len(g)} horizontal gridlines found (expect 49 interior), spacing {(g[-1]-g[0])/(len(g)-1):.2f} px")
MIX = {"A": [46, 72, 86, 100], "B": [38, 62, 84, 100], "C": [34, 70, 80, 100],
       "D": [42, 60, 84, 100], "E": [50, 68, 88, 100]}
slot = (B["x1"] - B["x0"]) / 5
for i, name in enumerate("ABCDE"):
    cx = round(B["x0"] + slot * (i + 0.5))
    col = dark_rows(cx, B["y0"] + 4, B["y1"] - 1)
    rs = runs(col)
    # runs of ~3 px are the segment edges; the dark 'Other' fill (0x3a) is a long run at the top
    edges = [ (r[0]+r[-1])/2 for r in rs if len(r) <= 5 ]
    # the Other fill is dark: its top edge coincides with the frame at 100, its bottom edge is a stroke,
    # the long run covers the whole segment, so recover the boundary at its bottom
    longs = [r for r in rs if len(r) > 5]
    if longs:
        edges.append(longs[0][-1] - 1.5)
    edges = sorted(edges)
    vals = sorted([b_val(e) for e in edges])
    want = sorted(MIX[name][:-1])
    for v, wv in zip(vals, want):
        check(f"(b) {name} boundary", v, wv, 0.15)
    if len(vals) != 3:
        print("BAD (b) edge count", name, vals); ok = False

# ---------------- panel (c): frame 215..2820 x 1215..2015, log 0.01..10
C = dict(x0=215, y0=1215, x1=2820, y1=2015)
def c_val(y): return 10 ** (1 - (y - C["y0"]) / (C["y1"] - C["y0"]) * 3)
g = gridrows(C["x0"] + 12, C["y0"] + 3, C["y1"] - 3)
print(f"panel (c): {len(g)} horizontal gridlines found (expect 26 interior)")
IC = {"A": 0.3, "B": 8, "C": 0.06, "D": 2, "E": 4}
slot = (C["x1"] - C["x0"]) / 5
for i, name in enumerate("ABCDE"):
    cx = round(C["x0"] + slot * (i + 0.5))
    col = dark_rows(cx, C["y0"] + 4, C["y1"] - 1)
    top = runs(col)[0]
    yt = (top[0] + top[-1]) / 2
    check(f"(c) {name} bar top", c_val(yt), IC[name], IC[name] * 0.003)
# gap between the 8 and 7 gridlines, and 8 and 9, in pixel rows
def cy(v): return C["y0"] + (1 - math.log10(v)) / 3 * (C["y1"] - C["y0"])
print(f"panel (c) rows: 10 at {cy(10):.1f}, 9 at {cy(9):.1f}, 8 at {cy(8):.1f}, 7 at {cy(7):.1f}, 6 at {cy(6):.1f}")
print("ALL OK" if ok else "PROBLEMS FOUND")
