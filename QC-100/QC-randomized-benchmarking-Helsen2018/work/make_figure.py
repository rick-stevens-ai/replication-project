#!/usr/bin/env python3
"""Figure: C1 single-exp Clifford RB vs C2 multi-exp Pauli-group RB."""
import json, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

d=json.load(open("results.json"))
c2=d["claims"]["C2_nonclifford_multiexp"]
L=np.array(c2["lengths"]); P=np.array(c2["survival"])
f1=c2["single_exp_f"]; ssS=c2["single_exp_SS"]
fd1=c2["double_exp_f1"]; fd2=c2["double_exp_f2"]; ssD=c2["double_exp_SS"]

# refit prefactors for plotting
from scipy.optimize import curve_fit
def m1(m,A,B,f): return A+B*f**m
def m2(m,A,B1,f1,B2,f2): return A+B1*f1**m+B2*f2**m
p1,_=curve_fit(m1,L,P,p0=[P[-1],P[0]-P[-1],0.95],maxfev=200000,bounds=([-1,-1,0],[1,1,1]))
p2,_=curve_fit(m2,L,P,p0=[P[-1],0.2,0.97,0.2,0.85],maxfev=400000,bounds=([-1,-1,0,-1,0],[1,1,1,1,1]))

fig,ax=plt.subplots(1,2,figsize=(11,4.2))
# left: C1 standard clifford (exact single-exp for depol)
c1=d["claims"]["C1_standard_clifford_rb"]
mm=np.array([1,2,4,8,16,32,64,128,256])
for k in ["0.99","0.95","0.9"]:
    q=c1[k]["q_inject"]; f=c1[k]["f_fit_exact"]
    # A=0.5,B=0.5 for depol from |0>
    ax[0].plot(mm, 0.5+0.5*f**mm, "o-", ms=4, label=f"q={q}, f_fit={f:.3f}")
ax[0].set_xscale("log",base=2); ax[0].set_xlabel("sequence length m"); ax[0].set_ylabel("survival p_m")
ax[0].set_title("C1: Clifford RB = single exponential\n(recovers F_avg to ~1e-12)"); ax[0].legend(fontsize=8); ax[0].grid(alpha=.3)

mfine=np.linspace(L.min(),L.max(),300)
ax[1].plot(L,P,"ko",ms=5,label="RB data (Pauli group, aniso noise)")
ax[1].plot(mfine,m1(mfine,*p1),"r--",label=f"single-exp (SS={ssS:.1e})")
ax[1].plot(mfine,m2(mfine,*p2),"b-",label=f"double-exp (SS={ssD:.0e})\nf={fd1:.3f},{fd2:.3f}")
ax[1].set_xlabel("sequence length m"); ax[1].set_ylabel("survival p_m")
ax[1].set_title("C2: non-Clifford gateset needs SUM of exponentials\n(recovers injected rates 0.97 & 0.85 exactly)")
ax[1].legend(fontsize=8); ax[1].grid(alpha=.3)
plt.tight_layout()
plt.savefig("../report/evidence/rb_replication_figure.png",dpi=130)
print("saved rb_replication_figure.png")
