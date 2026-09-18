#!/usr/bin/env python3
"""Render the attempt-7 task graph (tools/dag.py, SEED) as SVG -> PNG (3000x2000 via headless Chrome at 2x).
Layout: layers top to bottom, node x-order searched so that no edge passes through a node and every
edge label sits clear of other edges, nodes and labels. Writes tools/dag_layout.json with the geometry."""
import math, json, os, random, subprocess, sys
import decimal, fractions
from PIL import Image, PngImagePlugin   # before tools/ goes on sys.path (tools/numbers.py shadows the stdlib module)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dag
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 359
nodes, w, edges, c, layer_of = dag.make_graph(SEED)
W, H = 1500, 1000
FONT = "DejaVu Sans, Liberation Sans, Arial, sans-serif"
R = 30
NL = len(dag.LAYERS)
ys = [110 + i * (H - 220) / (NL - 1) for i in range(NL)]
by_layer = [[v for v in nodes if layer_of[v] == li] for li in range(NL)]

def seg_dist(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay; L2 = dx * dx + dy * dy
    t = 0 if L2 == 0 else max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / L2))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))

def layout(rng):
    pos = {}
    for li, layer in enumerate(by_layer):
        order = layer[:]; rng.shuffle(order)
        n = len(order); span = 1100
        xs = [W / 2 - span / 2 + span * (i + 0.5) / n + rng.uniform(-60, 60) for i in range(n)]
        for v, x in zip(order, xs): pos[v] = (x, ys[li])
    return pos

def geometry(pos, tpos):
    segs = {}
    for (u, v) in edges:
        (x1, y1), (x2, y2) = pos[u], pos[v]
        d = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / d, (y2 - y1) / d
        ax, ay = x1 + ux * R, y1 + uy * R; bx, by = x2 - ux * (R + 4), y2 - uy * (R + 4)
        t = tpos[(u, v)]; lx, ly = ax + (bx - ax) * t, ay + (by - ay) * t
        segs[(u, v)] = (ax, ay, bx, by, lx, ly)
    return segs

def score(pos, tpos):
    segs = geometry(pos, tpos); bad = 0
    items = list(segs.items())
    for i, (e, (ax, ay, bx, by, lx, ly)) in enumerate(items):
        for v in nodes:
            if v in e: continue
            d = seg_dist(pos[v][0], pos[v][1], ax, ay, bx, by)
            if d < R + 22: bad += 10 + (R + 22 - d)
            dl = math.hypot(lx - pos[v][0], ly - pos[v][1])
            if dl < R + 26: bad += 3 + (R + 26 - dl) / 4
        for f, (cx, cy, dx, dy, mx, my) in items[i + 1:]:
            d1 = seg_dist(lx, ly, cx, cy, dx, dy); d2 = seg_dist(mx, my, ax, ay, bx, by)
            for d in (d1, d2):
                if d < 26: bad += 3 + (26 - d) / 4
            d3 = math.hypot(lx - mx, ly - my)
            if d3 < 40: bad += 3 + (40 - d3) / 4
            if e[0] == f[0] or e[1] == f[1] or e[0] == f[1] or e[1] == f[0]:   # shared endpoint: keep a clear angle
                a1 = math.atan2(by - ay, bx - ax); a2 = math.atan2(dy - cy, dx - cx)
                ang = abs((a1 - a2 + math.pi) % (2 * math.pi) - math.pi); ang = min(ang, math.pi - ang)
                if ang < math.radians(9): bad += 6 + (9 - math.degrees(ang))
    return bad

def perturb(pos, tpos, rng):
    pos = dict(pos); tpos = dict(tpos)
    if rng.random() < 0.7:
        v = rng.choice(nodes); x, y = pos[v]
        if rng.random() < 0.5:
            li = layer_of[v]; u = rng.choice(by_layer[li])
            pos[v], pos[u] = (pos[u][0], y), (x, pos[u][1])
        else:
            pos[v] = (min(W - 120, max(120, x + rng.uniform(-80, 80))), ys[layer_of[v]] + max(-45, min(45, (y - ys[layer_of[v]]) + rng.uniform(-25, 25))))
    else:
        e = rng.choice(edges); tpos[e] = max(0.2, min(0.8, tpos[e] + rng.uniform(-0.15, 0.15)))
    return pos, tpos

best = None
rng = random.Random(7)
for trial in range(300):
    pos = layout(rng); tpos = {e: rng.uniform(0.3, 0.7) for e in edges}
    s = score(pos, tpos)
    if best is None or s < best[0]: best = (s, pos, tpos)
s, pos, tpos = best
T = 30.0
for it in range(20000):
    p2, t2 = perturb(pos, tpos, rng); s2 = score(p2, t2)
    if s2 <= s or rng.random() < math.exp((s - s2) / T):
        pos, tpos, s = p2, t2, s2
        if s < best[0]: best = (s, dict(pos), dict(tpos))
    T = max(0.5, T * 0.9997)
    if best[0] == 0: break
s, pos, tpos = best
print("layout score", s, "after", it + 1, "iterations")
segs = geometry(pos, tpos)
# crossings count (for the record)
def cross(a, b):
    (ax, ay, bx, by) = a[:4]; (cx, cy, dx, dy) = b[:4]
    def o(px, py, qx, qy, rx, ry): return (qx - px) * (ry - py) - (qy - py) * (rx - px)
    return (o(ax, ay, bx, by, cx, cy) * o(ax, ay, bx, by, dx, dy) < 0) and (o(cx, cy, dx, dy, ax, ay) * o(cx, cy, dx, dy, bx, by) < 0)
es = list(segs.items()); nc = sum(1 for i in range(len(es)) for j in range(i + 1, len(es)) if cross(es[i][1], es[j][1]))
print("edges", len(edges), "crossings", nc)
out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
       f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
       '<defs><marker id="ah" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto" markerUnits="userSpaceOnUse">'
       '<path d="M0,0 L10,5 L0,10 z" fill="#000"/></marker></defs>']
for e, (ax, ay, bx, by, lx, ly) in segs.items():
    out.append(f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="#000" stroke-width="1.5" marker-end="url(#ah)"/>')
for e, (ax, ay, bx, by, lx, ly) in segs.items():
    out.append(f'<rect x="{lx-11:.1f}" y="{ly-11:.1f}" width="22" height="22" fill="#fff" stroke="#000" stroke-width="0.8"/>')
    out.append(f'<text x="{lx:.1f}" y="{ly+6:.1f}" font-family="{FONT}" font-size="17" text-anchor="middle" fill="#000">{c[e]}</text>')
for v in nodes:
    x, y = pos[v]
    out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{R}" fill="#fff" stroke="#000" stroke-width="2"/>')
    out.append(f'<text x="{x:.1f}" y="{y-3:.1f}" font-family="{FONT}" font-size="17" font-weight="bold" text-anchor="middle" fill="#000">T{v}</text>')
    out.append(f'<text x="{x:.1f}" y="{y+16:.1f}" font-family="{FONT}" font-size="16" text-anchor="middle" fill="#000">{w[v]}</text>')
out.append(f'<text x="{W/2}" y="{H-28}" font-family="{FONT}" font-size="20" text-anchor="middle" fill="#000">'
           'Task graph: node = task (name, execution time in cycles); arrow = data dependency (label = communication delay in cycles)</text>')
out.append('</svg>')
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
open(f"{here}/dag_fig.svg", "w").write("\n".join(out))
open(f"{here}/dag_fig.html", "w").write(f'<html><body style="margin:0;background:#fff"><img src="dag_fig.svg" width="{W}" height="{H}"></body></html>')
json.dump({"pos": {str(k): v for k, v in pos.items()}, "labels": {"%d-%d" % e: s[4:6] for e, s in segs.items()}}, open(f"{here}/dag_layout.json", "w"), indent=1)
subprocess.run([os.environ.get("CHROME", "google-chrome"), "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                f"--user-data-dir={here}/.chrome", "--force-device-scale-factor=2", f"--window-size={W},{H+120}",
                f"--screenshot={root}/image.png", f"file://{here}/dag_fig.html"], check=True, capture_output=True, timeout=120)
im = Image.open(f"{root}/image.png"); im = im.crop((0, 0, 2 * W, 2 * H)); im.save(f"{root}/image.png")
print("rendered image.png", im.size)
