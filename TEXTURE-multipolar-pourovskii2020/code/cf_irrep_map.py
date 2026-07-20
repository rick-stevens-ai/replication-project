#!/usr/bin/env python3
"""
Map the full LLW irrep sequence vs x for J=9/2 with W<0, to show that
the paper's reported x=-0.54 lies in the window giving the observed
Gamma8(GS) - Gamma8 - Gamma6 ordering, and to locate the boundaries.

Also cross-check against the INS-inferred x=-0.48 (Amoretti 1992).
"""
import numpy as np
from cf_j92 import stevens_operators

F4, F6 = 60.0, 13860.0
def O4(S): return S["O40"] + 5.0*S["O44"]
def O6(S): return S["O60"] - 21.0*S["O64"]
def H_llw(W,x,J=4.5):
    S=stevens_operators(J); return W*(x*O4(S)/F4 + (1-abs(x))*O6(S)/F6)

def scheme(W,x):
    ev=np.sort(np.linalg.eigvalsh(H_llw(W,x)).real); ev-=ev[0]
    groups=[]; cur=[ev[0]]
    for e in ev[1:]:
        if abs(e-cur[-1])<1e-3: cur.append(e)
        else: groups.append((float(np.mean(cur)),len(cur))); cur=[e]
    groups.append((float(np.mean(cur)),len(cur)))
    return groups

def seq(groups):
    return "-".join({2:"D",4:"Q"}[g] for _,g in groups)

print("="*72)
print("LLW irrep sequence vs x (W<0) for J=9/2")
print("  Q=Gamma8 quartet, D=Gamma6/7 doublet.  Paper target: Q-Q-D at x=-0.54")
print("="*72)
prev=None
for x in np.linspace(-1.0,1.0,81):
    s=seq(scheme(-1.0,x))
    if s!=prev:
        print(f"  x >= {x:+.3f} : {s}")
        prev=s

print("\nSpecific points:")
for x in (-0.54,-0.48):
    g=scheme(-1.0,x); s=seq(g)
    # fix scale to 68 meV excited-Q if pattern is Q-Q-...
    excQ=next((e for e,d in g[1:] if d==4),None)
    scale = 68.0/excQ if excQ else 1.0
    line=", ".join(f"{e*scale:.0f}meV[{ 'Q' if d==4 else 'D'}]" for e,d in g)
    print(f"  x={x:+.3f}: seq={s}  scheme(scaled to 68meV excQ): {line}")
    print(f"     -> Gamma8 ground quartet: {'YES' if g[0][1]==4 else 'NO'};"
          f" first-excited Gamma8: {'YES' if len(g)>1 and g[1][1]==4 else 'NO'}")
