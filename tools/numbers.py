import math
SIZES = [4 ** k for k in range(11)]
CURVES = {"A": [0.008, 0.03, 0.1, 0.5, 2, 8, 40, 50, 60, 80, 90],
          "B": [0.005, 0.02, 0.08, 0.3, 1, 3, 6, 7, 8, 8, 8],
          "C": [0.003, 0.01, 0.05, 0.2, 0.8, 4, 20, 40, 70, 60, 60],
          "D": [0.002, 0.008, 0.03, 0.1, 0.4, 2, 4, 6, 7, 7, 7]}
def pt(frac, vals):
    """smallest message size where the polyline reaches frac * (value at 1 MB); log-log interpolation"""
    tgt = frac * vals[-1]
    for (x0, y0), (x1, y1) in zip(zip(SIZES, vals), list(zip(SIZES, vals))[1:]):
        if y0 < tgt <= y1:
            t = math.log(tgt / y0) / math.log(y1 / y0); return x0 * (x1 / x0) ** t
    raise ValueError("level never reached")
def answer(curves):
    p = 1.0
    for v in curves.values(): p *= pt(0.8, v) / pt(0.5, v)
    return p
if __name__ == "__main__":
    base = answer(CURVES)
    for k, v in CURVES.items():
        a, b = pt(0.8, v), pt(0.5, v)
        print("%s plateau %-3g x80 %9.6g KB  x50 %9.6g KB  ratio %.6g" % (k, v[-1], a / 1024, b / 1024, a / b))
    print("GTFA %.6f -> %.3g" % (base, base))
    minors = sorted(set(round(m * 10 ** d, 4) for d in range(-3, 3) for m in range(1, 10)))
    n = 0
    for k in CURVES:
        for i, s in enumerate(SIZES):
            v = CURVES[k][i]; j = minors.index(v); hit = False
            for nv in [minors[j - 1]] + ([minors[j + 1]] if minors[j + 1] <= 100 else []):
                c2 = {kk: list(vv) for kk, vv in CURVES.items()}; c2[k][i] = nv
                try: a = answer(c2); d = 100 * (a / base - 1)
                except ValueError: a, d = None, float("nan")
                if a is None or abs(d) > 0.05:
                    hit = True; print("%s %8d B %-4g read as %-4g -> %-6s %+7.1f%%" % (k, s, v, nv, ("%.4g" % a) if a else "n/a", d))
            n += hit
    print("critical markers:", n)
    # method errors
    def lin(frac, vals):
        tgt = frac * vals[-1]
        for (x0, y0), (x1, y1) in zip(zip(SIZES, vals), list(zip(SIZES, vals))[1:]):
            if y0 < tgt <= y1: return x0 + (x1 - x0) * (tgt - y0) / (y1 - y0)
    p = 1.0
    for v in CURVES.values(): p *= lin(0.8, v) / lin(0.5, v)
    print("linear interpolation instead of log-log: %.4g %+.1f%%" % (p, 100 * (p / base - 1)))
    p = 1.0
    for k, v in CURVES.items():
        pk = max(v) if k == "C" else v[-1]; vv = list(v); vv[-1] = pk
        p *= pt(0.8, vv) / pt(0.5, vv)
    print("link C asymptote taken as its 70 peak: %.4g %+.1f%%" % (p, 100 * (p / base - 1)))
    s = sum(pt(0.8, v) / pt(0.5, v) for v in CURVES.values())
    print("sum instead of product: %.4g" % s)
