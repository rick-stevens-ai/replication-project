"""make_figs.py — figures for the replication report (writes to ../report/)."""
import os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sdw_meanfield as M

PI = np.pi
REP = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "report"))
os.makedirs(REP, exist_ok=True)

# Fig 1: self-consistent SDW gap h(U) at n=1 (Neel)
tp = (1.0, 0.0, 0.0, 0.0)
Us = np.linspace(0.5, 8.0, 14)
hv = [M.self_consistent_h(tp, U, 0.0, (PI, PI), 1.0, nk=120, T=0.03,
                          h0=0.5*U, mix=0.4, itmax=200) for U in Us]
fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
ax[0].plot(Us, hv, "o-", color="crimson")
ax[0].set_xlabel("Hubbard $U/t_1$"); ax[0].set_ylabel("SDW gap $h=2UN_0$")
ax[0].set_title("(a) Self-consistent Néel gap, $n=1$")
ax[0].grid(alpha=.3)

# Fig 1b: SDW bands along Gamma-X-M-Gamma for Neel gapped state
def path(pts, n=120):
    seg=[]
    for a,b in zip(pts[:-1], pts[1:]):
        seg.append(np.linspace(a,b,n))
    return np.vstack(seg)
G=(0,0); X=(PI,0); Mp=(PI,PI)
kp = path([G,X,Mp,G], 100)
Em, Ep = M.bands(kp[:,0], kp[:,1], tp, mu=0.0, h=2.0, theta=0.0, K=(PI,PI))
ax[1].plot(Em, color="navy"); ax[1].plot(Ep, color="darkorange")
ax[1].axhline(0, color="k", lw=.5, ls=":")
ax[1].set_title("(b) SDW bands (Néel, $h=2$)")
ax[1].set_ylabel("$E_{k,\\pm}$"); ax[1].set_xlabel("$\\Gamma$–X–M–$\\Gamma$")
ax[1].set_xticks([0,100,200,300]); ax[1].set_xticklabels(["$\\Gamma$","X","M","$\\Gamma$"])
ax[1].grid(alpha=.3)
fig.tight_layout()
fig.savefig(os.path.join(REP, "fig_sdw.png"), dpi=140)
print("wrote fig_sdw.png")
