import math
def hp(plateau, x0, y0, x1, y1):
    t = (math.log(plateau / 2) - math.log(y0)) / (math.log(y1) - math.log(y0))
    return x0 * (x1 / x0) ** t
base = hp(80, 4, 30, 16, 50); print("GTFA %.6f KB" % base)
for n, v in [("plateau 70", hp(70, 4, 30, 16, 50)), ("plateau 90", hp(90, 4, 30, 16, 50)),
             ("16 KB marker 40", 16.0), ("16 KB marker 60", hp(80, 4, 30, 16, 60)),
             ("4 KB marker 20", hp(80, 4, 20, 16, 50)), ("4 KB marker 40", 4.0),
             ("plateau 70 and 16 KB 40", hp(70, 4, 30, 16, 40)),
             ("linear interpolation (method error)", 4 + 12 * (40 - 30) / (50 - 30)),
             ("Link C by mistake", hp(30, 4, 9, 16, 20)), ("Link B by mistake", hp(8, 64, 0.5, 256, 2))]:
    print("%-38s %8.3f %+7.1f%%" % (n, v, 100 * (v / base - 1)))
