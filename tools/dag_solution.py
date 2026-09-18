#!/usr/bin/env python3
"""Independent re-derivation of the attempt-7 answer, written as the golden solution text.
Reads the graph from dag.make_graph(SEED) but re-implements the scheduling rules from scratch."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dag
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 359
P = 4
nodes, w, edges, c, layer_of = dag.make_graph(SEED)
preds = {v: [] for v in nodes}; succs = {v: [] for v in nodes}
for u, v in edges: preds[v].append(u); succs[u].append(v)
out = []
def step(n, text): out.append(f"Step {n}. {text}")
# Step 1: graph
edge_txt = ", ".join(f"T{u} to T{v} ({c[(u, v)]})" for u, v in edges)
step(1, "Read the graph. The twenty tasks and their execution times are " + ", ".join(f"T{v}: {w[v]}" for v in nodes) +
     ". The thirty five dependency arrows, written as tail to head with the communication delay in brackets, are " + edge_txt + ".")
# Step 2: bottom levels
bl = {}
for v in sorted(nodes, reverse=True):
    bl[v] = w[v] + (max(bl[s] for s in succs[v]) if succs[v] else 0)
bl_txt = []
for v in sorted(nodes, reverse=True):
    if succs[v]:
        bl_txt.append(f"T{v}: {w[v]} + max({', '.join(str(bl[s]) for s in succs[v])}) = {bl[v]}")
    else:
        bl_txt.append(f"T{v}: {w[v]} (no successors)")
step(2, "Compute the bottom level of every task, working from the exit tasks upward: a task's bottom level is its execution time plus the largest bottom level among its successors. " + "; ".join(bl_txt) + ".")
order = sorted(nodes, key=lambda v: (-bl[v], v))
step(3, "Order the tasks by decreasing bottom level, smaller task number first among equals: " + ", ".join(f"T{v} ({bl[v]})" for v in order) + ".")
# placements
free = [0] * P; proc = {}; start = {}; finish = {}
n = 4
for v in order:
    cands = []
    for p in range(P):
        arrivals = []
        for u in preds[v]:
            d = 0 if proc[u] == p else c[(u, v)]
            arrivals.append((u, finish[u] + d, d))
        ready = max([a[1] for a in arrivals], default=0)
        st = max(free[p], ready); cands.append((st, p, arrivals))
    st, p, _ = min(cands, key=lambda x: (x[0], x[1]))
    parts = []
    for cst, cp, arrivals in cands:
        if arrivals:
            arr = ", ".join(f"T{u} at {t}" + (" (same processor)" if d == 0 else f" ({finish[u]} + {d})") for u, t, d in arrivals)
            parts.append(f"P{cp+1}: free at {free[cp]}, data {arr}, start {cst}")
        else:
            parts.append(f"P{cp+1}: free at {free[cp]}, start {cst}")
    tie = sum(1 for cst, cp, _ in cands if cst == st) > 1
    step(n, f"Place T{v} (execution time {w[v]}). " + "; ".join(parts) + f". Earliest start is {st} on P{p+1}" + (" (tie, smaller processor number)" if tie else "") + f", so T{v} runs on P{p+1} from {st} to {st + w[v]}.")
    proc[v], start[v], finish[v] = p, st, st + w[v]; free[p] = finish[v]; n += 1
cross = [(u, v) for u, v in edges if proc[u] != proc[v]]
same = [(u, v) for u, v in edges if proc[u] == proc[v]]
step(n, "Final placement: " + "; ".join(f"P{p+1}: " + ", ".join(f"T{v} [{start[v]}, {finish[v]}]" for v in order if proc[v] == p) for p in range(P)) + f". Makespan {max(finish.values())}.")
n += 1
step(n, "List the arrows whose two tasks are on the same processor, which cost nothing: " + ", ".join(f"T{u} to T{v}" for u, v in same) + ".")
n += 1
total = sum(c[e] for e in cross)
step(n, "Add the delays of the remaining arrows, whose two tasks are on different processors: " + " + ".join(f"{c[e]}" for e in cross) + f" = {total}.")
out.append(f"\nFinal answer: {total}")
text = "\n\n".join(out)
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dag_solution.md"), "w").write(text)
r = dag.schedule(nodes, w, edges, c, P)
print("independent total", total, "dag.py total", r["comm"], "makespan", max(finish.values()), r["makespan"])
print(text)
