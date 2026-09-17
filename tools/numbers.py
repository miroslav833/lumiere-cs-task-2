import math, itertools
SIZES=[4**k for k in range(11)]  # bytes
KB=1024
C={"A":[0.008,0.03,0.1,0.5,2,8,30,50,60,80,90],
   "B":[0.005,0.02,0.08,0.3,1,3,6,7,8,8,8],
   "C":[0.003,0.01,0.05,0.2,0.8,2,9,30,40,60,60],
   "D":[0.004,0.007,0.04,0.4,0.6,4,5,6,7,7,7]}
def size80(vals):
    """smallest size where the log-log polyline reaches 0.8 * last value, in KB"""
    thr=0.8*vals[-1]
    for i in range(len(vals)-1):
        y0,y1=vals[i],vals[i+1]
        if y1>=thr and y0<thr:
            t=(math.log(thr)-math.log(y0))/(math.log(y1)-math.log(y0))
            return SIZES[i]*(SIZES[i+1]/SIZES[i])**t/KB
        if y0>=thr: return SIZES[i]/KB
    return None
def answer(c):
    s={k:size80(v) for k,v in c.items()}
    return max(s.values())/min(s.values()), s
base,s=answer(C); print("sizes KB", {k:round(v,4) for k,v in s.items()}, "GTFA %.6f"%base)
# every single-marker slip to a neighbouring minor gridline, on the markers that matter (4 KB .. 1 MB)
def neigh(v):
    m=v/10**math.floor(math.log10(v)); d=10**math.floor(math.log10(v))
    out=[]
    if m>1: out.append((m-1)*d)
    else: out.append(0.9*d)
    if m<9: out.append((m+1)*d)
    else: out.append(10*d)
    return out
inside=[]
for link in "ABCD":
    for k in range(6,11):
        for nv in neigh(C[link][k]):
            c={kk:list(vv) for kk,vv in C.items()}; c[link][k]=nv
            a,_=answer(c); dev=100*(a/base-1)
            tag="unchanged" if abs(dev)<1e-9 else ("INSIDE 2%" if abs(dev)<2 else "")
            if tag: inside.append((link,SIZES[k]//KB,nv,round(a,3),round(dev,2),tag))
            print("%s %6d KB %5g -> %4g : %8.3f %+7.2f%% %s"%(link,SIZES[k]//KB,C[link][k],nv,a,dev,tag))
print("\nslips that leave the answer unchanged or inside 2 percent:")
for r in inside: print(r)
