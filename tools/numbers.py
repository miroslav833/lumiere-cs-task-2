import math
def pt(frac, plateau, x0, y0, x1, y1):
    """message size where the curve reaches frac * plateau, log-log interpolation between (x0,y0) and (x1,y1)"""
    t = (math.log(frac * plateau) - math.log(y0)) / (math.log(y1) - math.log(y0))
    return x0 * (x1 / x0) ** t
# attempt 3: link A = 30 @4KB, 50 @16KB, 60 @64KB, 80 @256KB, 90 @1MB; link C = 40 @16KB, 80 @64KB, 60 @256KB, 60 @1MB
# asked: 80 percent of link A's asymptotic bandwidth
base = pt(0.8, 90, 64, 60, 256, 80); print("GTFA %.6f KB" % base)
for n, v in [("64 KB marker taken from link C (80): thr 72 between 50 and 80", pt(0.8, 90, 16, 50, 64, 80)),
             ("256 KB marker taken from link C (60): thr 72 between 60@256K and 90@1M", pt(0.8, 90, 256, 60, 1024, 90)),
             ("link C followed entirely (plateau 60, thr 48, between 40 and 80)", pt(0.8, 60, 16, 40, 64, 80)),
             ("plateau 90 read as 100 (thr 80, the 256 KB marker)", 256.0),
             ("plateau 90 read as 80 (thr 64)", pt(0.8, 80, 64, 60, 256, 80)),
             ("64 KB marker 60 read as 50", pt(0.8, 90, 64, 50, 256, 80)),
             ("64 KB marker 60 read as 70", pt(0.8, 90, 64, 70, 256, 80)),
             ("256 KB marker 80 read as 90", pt(0.8, 90, 64, 60, 256, 90)),
             ("256 KB marker 80 read as 70 (thr 72 above 70, between 70 and 90)", pt(0.8, 90, 256, 70, 1024, 90)),
             ("linear interpolation (method error)", 64 + 192 * (72 - 60) / (80 - 60)),
             ("half-power point by habit (thr 45, between 30 and 50)", pt(0.5, 90, 4, 30, 16, 50))]:
    print("%-72s %8.3f %+7.1f%%" % (n, v, 100 * (v / base - 1)))
