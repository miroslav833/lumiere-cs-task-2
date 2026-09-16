#!/usr/bin/env python3
"""Task 2 figure: branch predictor accuracy, instruction mix, instruction count.

Writes fig.svg and fig.html next to this script. Render with headless Chrome at
3000 x 2240. Every plotted value sits on a drawn gridline.
"""
import math, os, json

W, H = 3000, 2240
FONT = "Liberation Sans, Arial, Helvetica, sans-serif"
TICK = 34
AXIS = 38
PLAB = 44
MAJOR = "#9a9a9a"
MINOR = "#d4d4d4"
FRAME = "#1a1a1a"

out = []
def w(s): out.append(s)

def px(v):  # half-pixel snap for crisp 1-2 px strokes
    return round(v) + 0.5

def text(x, y, s, size=TICK, anchor="middle", weight="normal", rotate=None, baseline="middle"):
    tr = f' transform="rotate({rotate} {x} {y})"' if rotate is not None else ""
    w(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
      f'text-anchor="{anchor}" dominant-baseline="{baseline}" fill="{FRAME}"{tr}>{s}</text>')

def hline(x0, x1, y, color, sw):
    w(f'<line x1="{x0}" y1="{px(y)}" x2="{x1}" y2="{px(y)}" stroke="{color}" stroke-width="{sw}"/>')

def vline(x, y0, y1, color, sw):
    w(f'<line x1="{px(x)}" y1="{y0}" x2="{px(x)}" y2="{y1}" stroke="{color}" stroke-width="{sw}"/>')

def frame(x0, y0, x1, y1):
    w(f'<rect x="{px(x0)}" y="{px(y0)}" width="{round(x1)-round(x0)}" height="{round(y1)-round(y0)}" '
      f'fill="none" stroke="{FRAME}" stroke-width="3"/>')

# ---------------------------------------------------------------- data
# Panel (a): accuracy (percent) vs global history length (bits)
HIST = [2, 4, 6, 8, 10, 12, 14, 16]
GSHARE = [86, 88, 90, 91, 92, 93, 93, 92]
TOURN  = [90, 92, 93, 94, 95, 95, 96, 96]
A_Y0, A_Y1 = 80, 100

# Panel (b): stacked instruction mix, bottom to top: ALU, load/store, cond branch, other
WORK = ["A", "B", "C", "D", "E"]
MIX = {  # cumulative boundaries, percent
    "A": [46, 72, 86, 100],
    "B": [38, 62, 84, 100],
    "C": [34, 70, 80, 100],
    "D": [42, 60, 84, 100],
    "E": [50, 68, 88, 100],
}
CAT = ["Integer ALU", "Load and store", "Conditional branch", "Other"]
FILL = ["#ffffff", "#d0d0d0", "#8a8a8a", "#3a3a3a"]

# Panel (c): dynamic instruction count, units of 1e9, log axis 0.01 .. 10
IC = {"A": 0.3, "B": 8, "C": 0.06, "D": 2, "E": 4}
C_LO, C_HI = 0.01, 10

# ---------------------------------------------------------------- geometry
A = dict(x0=215, y0=140, x1=1380, y1=940)
B = dict(x0=1660, y0=140, x1=2820, y1=940)
C = dict(x0=215, y0=1215, x1=2820, y1=2015)

def lin(v, lo, hi, p0, p1):
    return p0 + (v - lo) / (hi - lo) * (p1 - p0)

truth = {}

w(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
w(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')

# ================================================================ panel (a)
P = A
text(P["x0"] + 30, P["y0"] - 60, "(a)", PLAB, "middle", "bold")
# minors every 1, majors every 5
for v in range(A_Y0, A_Y1 + 1):
    y = lin(v, A_Y0, A_Y1, P["y1"], P["y0"])
    if v % 5 == 0:
        hline(P["x0"], P["x1"], y, MAJOR, 2)
        text(P["x0"] - 22, y, str(v), TICK, "end")
    else:
        hline(P["x0"], P["x1"], y, MINOR, 1.5)
for hv in HIST:
    x = lin(hv, HIST[0], HIST[-1], P["x0"], P["x1"])
    vline(x, P["y0"], P["y1"], MAJOR, 2)
    text(x, P["y1"] + 38, str(hv), TICK)
frame(P["x0"], P["y0"], P["x1"], P["y1"])
text((P["x0"] + P["x1"]) / 2, P["y1"] + 105, "Global history length (bits)", AXIS)
text(P["x0"] - 150, (P["y0"] + P["y1"]) / 2, "Prediction accuracy (%)", AXIS, rotate=-90)

def series(vals, marker):
    pts = []
    for hv, v in zip(HIST, vals):
        x = lin(hv, HIST[0], HIST[-1], P["x0"], P["x1"])
        y = lin(v, A_Y0, A_Y1, P["y1"], P["y0"])
        pts.append((x, y))
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    w(f'<polyline points="{d}" fill="none" stroke="{FRAME}" stroke-width="3"/>')
    for (x, y) in pts:
        if marker == "circle":
            w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="12" fill="{FRAME}" stroke="{FRAME}" stroke-width="3"/>')
        else:
            w(f'<rect x="{x-11:.1f}" y="{y-11:.1f}" width="22" height="22" fill="#ffffff" stroke="{FRAME}" stroke-width="3"/>')
    return pts

pa_g = series(GSHARE, "circle")
pa_t = series(TOURN, "square")
truth["a_gshare_px"] = pa_g
truth["a_tourn_px"] = pa_t
# legend, bottom right inside the plot, away from the data
lx, ly = P["x1"] - 330, P["y1"] - 120
w(f'<rect x="{lx-20}" y="{ly-40}" width="330" height="110" fill="#ffffff" stroke="{FRAME}" stroke-width="2"/>')
w(f'<line x1="{lx}" y1="{ly}" x2="{lx+60}" y2="{ly}" stroke="{FRAME}" stroke-width="3"/>')
w(f'<circle cx="{lx+30}" cy="{ly}" r="12" fill="{FRAME}" stroke="{FRAME}" stroke-width="3"/>')
text(lx + 80, ly, "gshare", TICK, "start")
w(f'<line x1="{lx}" y1="{ly+55}" x2="{lx+60}" y2="{ly+55}" stroke="{FRAME}" stroke-width="3"/>')
w(f'<rect x="{lx+19}" y="{ly+44}" width="22" height="22" fill="#ffffff" stroke="{FRAME}" stroke-width="3"/>')
text(lx + 80, ly + 55, "tournament", TICK, "start")

# ================================================================ panel (b)
P = B
text(P["x0"] + 30, P["y0"] - 60, "(b)", PLAB, "middle", "bold")
for v in range(0, 101, 2):
    y = lin(v, 0, 100, P["y1"], P["y0"])
    if v % 10 == 0:
        hline(P["x0"], P["x1"], y, MAJOR, 2)
        text(P["x0"] - 22, y, str(v), TICK, "end")
    else:
        hline(P["x0"], P["x1"], y, MINOR, 1.5)
n = len(WORK)
slot = (P["x1"] - P["x0"]) / n
bw = slot * 0.56
truth["b_boundaries_px"] = {}
for i, name in enumerate(WORK):
    cx = P["x0"] + slot * (i + 0.5)
    lo = 0
    rows = []
    for k, hi in enumerate(MIX[name]):
        y_hi = px(lin(hi, 0, 100, P["y1"], P["y0"]))
        y_lo = px(lin(lo, 0, 100, P["y1"], P["y0"]))
        w(f'<rect x="{cx-bw/2:.1f}" y="{y_hi:.1f}" width="{bw:.1f}" height="{y_lo-y_hi:.1f}" '
          f'fill="{FILL[k]}" stroke="{FRAME}" stroke-width="3"/>')
        rows.append(y_hi)
        lo = hi
    truth["b_boundaries_px"][name] = rows
    text(cx, P["y1"] + 38, name, TICK)
frame(P["x0"], P["y0"], P["x1"], P["y1"])
text((P["x0"] + P["x1"]) / 2, P["y1"] + 105, "Workload", AXIS)
text(P["x0"] - 150, (P["y0"] + P["y1"]) / 2, "Dynamic instruction mix (%)", AXIS, rotate=-90)
# legend row under the axis title
lx = P["x0"] - 40
ly = P["y1"] + 175
gap = [0, 310, 665, 1085]
for k, name in enumerate(CAT):
    x = lx + gap[k]
    w(f'<rect x="{x}" y="{ly-18}" width="44" height="36" fill="{FILL[k]}" stroke="{FRAME}" stroke-width="2"/>')
    text(x + 60, ly, name, TICK, "start")

# ================================================================ panel (c)
P = C
text(P["x0"] + 30, P["y0"] - 60, "(c)", PLAB, "middle", "bold")
def logy(v):
    return lin(math.log10(v), math.log10(C_LO), math.log10(C_HI), P["y1"], P["y0"])
labels = {0.01: "0.01", 0.02: "0.02", 0.04: "0.04", 0.06: "0.06", 0.08: "0.08",
          0.1: "0.1", 0.2: "0.2", 0.4: "0.4", 0.6: "0.6", 0.8: "0.8",
          1: "1", 2: "2", 4: "4", 6: "6", 8: "8", 10: "10"}
grid_rows = {}
for dec in (-2, -1, 0):
    for m in range(1, 10):
        v = m * 10 ** dec
        y = logy(v)
        grid_rows[round(v, 4)] = y
        if m == 1:
            hline(P["x0"], P["x1"], y, MAJOR, 2)
        else:
            hline(P["x0"], P["x1"], y, MINOR, 1.5)
y = logy(10); grid_rows[10] = y
hline(P["x0"], P["x1"], y, MAJOR, 2)
for v, s in labels.items():
    text(P["x0"] - 22, logy(v), s, TICK, "end")
slot = (P["x1"] - P["x0"]) / n
bw = slot * 0.5
truth["c_bartop_px"] = {}
for i, name in enumerate(WORK):
    cx = P["x0"] + slot * (i + 0.5)
    yt = px(logy(IC[name]))
    w(f'<rect x="{cx-bw/2:.1f}" y="{yt:.1f}" width="{bw:.1f}" height="{P["y1"]-yt:.1f}" '
      f'fill="#c8c8c8" stroke="{FRAME}" stroke-width="3"/>')
    truth["c_bartop_px"][name] = yt
    text(cx, P["y1"] + 38, name, TICK)
frame(P["x0"], P["y0"], P["x1"], P["y1"])
text((P["x0"] + P["x1"]) / 2, P["y1"] + 105, "Workload", AXIS)
text(P["x0"] - 150, (P["y0"] + P["y1"]) / 2,
     'Dynamic instruction count (10<tspan baseline-shift="super" font-size="26">9</tspan> instructions)',
     AXIS, rotate=-90)
truth["c_grid_rows"] = grid_rows

w('</svg>')

here = os.path.dirname(os.path.abspath(__file__))
svg = "\n".join(out)
open(os.path.join(here, "fig.svg"), "w").write(svg)
open(os.path.join(here, "fig.html"), "w").write(
    '<html><head><meta charset="utf-8"></head><body style="margin:0;background:#fff">' + svg + '</body></html>')
json.dump(truth, open(os.path.join(here, "truth.json"), "w"), indent=1)
print("ok")
