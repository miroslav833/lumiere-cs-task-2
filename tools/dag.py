#!/usr/bin/env python3
"""Attempt 7: task graph with per-edge communication delays, static list scheduling on P processors.
Priority = bottom level (computation only). Each task goes to the processor with the earliest start
(ties: lowest index); start = max(processor free, max over preds of finish + (delay if other
processor else 0)); no insertion. Answer = total communication cost of the schedule = sum of the
delays of the edges whose endpoints sit on different processors.
`python3 dag.py` prints the ground truth and the sensitivity table for SEED;
`python3 dag.py search` scans seeds."""
import random, sys, itertools
P = 4
N = 20
LAYERS = [3, 4, 4, 4, 3, 2]
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 0

def make_graph(seed):
    rng = random.Random(seed)
    layer_of, nodes = {}, []
    k = 1
    for li, cnt in enumerate(LAYERS):
        for _ in range(cnt):
            layer_of[k] = li; nodes.append(k); k += 1
    w = {v: rng.randint(2, 9) for v in nodes}
    edges = set()
    by_layer = [[v for v in nodes if layer_of[v] == li] for li in range(len(LAYERS))]
    for li in range(1, len(LAYERS)):
        for v in by_layer[li]:
            npred = rng.choice([1, 2, 2, 3])
            cands = [u for lj in range(max(0, li - 3), li) for u in by_layer[lj]]
            for u in rng.sample(cands, min(npred, len(cands))): edges.add((u, v))
    for li in range(len(LAYERS) - 1):
        for u in by_layer[li]:
            if not any(e[0] == u for e in edges):
                lj = rng.randint(li + 1, min(li + 2, len(LAYERS) - 1)); edges.add((u, rng.choice(by_layer[lj])))
    for _ in range(4):
        li = rng.randint(0, len(LAYERS) - 3); u = rng.choice(by_layer[li]); v = rng.choice(by_layer[li + 2] + by_layer[min(li + 3, len(LAYERS) - 1)])
        edges.add((u, v))
    edges = sorted(edges)
    c = {e: rng.randint(1, 9) for e in edges}
    return nodes, w, edges, c, layer_of

def schedule(nodes, w, edges, c, P=P):
    succ = {v: [] for v in nodes}; pred = {v: [] for v in nodes}
    for u, v in edges: succ[u].append(v); pred[v].append(u)
    bl = {}
    for v in sorted(nodes, reverse=True):
        bl[v] = w[v] + max([bl[s] for s in succ[v]], default=0)
    order = sorted(nodes, key=lambda v: (-bl[v], v))
    free = [0] * P; proc, start, finish = {}, {}, {}
    for v in order:
        best = None
        for p in range(P):
            ready = max([finish[u] + (0 if proc[u] == p else c[(u, v)]) for u in pred[v]], default=0)
            st = max(free[p], ready)
            if best is None or st < best[0]: best = (st, p)
        st, p = best
        proc[v], start[v], finish[v] = p, st, st + w[v]; free[p] = finish[v]
    comm = sum(c[(u, v)] for u, v in edges if proc[u] != proc[v])
    return dict(bl=bl, order=order, proc=proc, start=start, finish=finish, makespan=max(finish.values()),
                sumC=sum(finish.values()), comm=comm)

def perturbations(nodes, w, edges, c, layer_of):
    out = []
    for e in edges:
        c2 = dict(c); del c2[e]; out.append(("drop %d->%d" % e, [x for x in edges if x != e], w, c2))
    for u, v in itertools.combinations(nodes, 2):
        if (u, v) not in c and layer_of[u] < layer_of[v]:
            for d in (1, 5, 9):
                c2 = dict(c); c2[(u, v)] = d; out.append(("add %d->%d (%d)" % (u, v, d), edges + [(u, v)], w, c2))
    for e in edges:
        for d in (-1, 1):
            if 1 <= c[e] + d <= 9:
                c2 = dict(c); c2[e] += d; out.append(("c%d->%d%+d" % (e[0], e[1], d), edges, w, c2))
    for v in nodes:
        for d in (-1, 1):
            w2 = dict(w); w2[v] += d; out.append(("w%d%+d" % (v, d), edges, w2, c))
    return out

def sensitivity(nodes, w, edges, c, layer_of, key="comm"):
    base = schedule(nodes, w, edges, c)[key]
    groups = {"drop": [0, 0], "add": [0, 0], "c": [0, 0], "w": [0, 0]}; same = []
    for name, e2, w2, c2 in perturbations(nodes, w, edges, c, layer_of):
        g = name.split()[0][0] if not name.startswith(("drop", "add")) else name.split()[0]
        val = schedule(nodes, w2, e2, c2)[key]; groups[g][1] += 1
        if val == base: groups[g][0] += 1; same.append(name)
    return base, groups, same

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "search":
        rows = []
        for seed in range(1, 2500):
            nodes, w, edges, c, layer_of = make_graph(seed)
            if not (34 <= len(edges) <= 42): continue
            base, g, same = sensitivity(nodes, w, edges, c, layer_of)
            rows.append((g["drop"][0], g["c"][0] / g["c"][1], g["add"][0] / g["add"][1], g["w"][0], seed, len(edges), base))
        rows.sort()
        for r in rows[:15]: print("drop-insens %d  c-insens %.2f  add-insens %.2f  w-insens %d  seed %d  edges %d  answer %d" % r)
    else:
        nodes, w, edges, c, layer_of = make_graph(SEED)
        r = schedule(nodes, w, edges, c)
        print("seed", SEED, "nodes", len(nodes), "edges", len(edges))
        print("weights", w)
        print("edges", {e: c[e] for e in edges})
        print("bottom levels", r["bl"])
        for v in r["order"]:
            print("T%-2d w=%d bl=%2d -> P%d start %2d finish %2d" % (v, w[v], r["bl"][v], r["proc"][v] + 1, r["start"][v], r["finish"][v]))
        print("makespan", r["makespan"], "sumC", r["sumC"], "total communication cost", r["comm"])
        base, g, same = sensitivity(nodes, w, edges, c, layer_of)
        print("answer", base, "insensitive:", g, same)
