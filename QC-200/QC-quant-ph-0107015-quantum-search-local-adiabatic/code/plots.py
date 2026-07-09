"""Generate log-log scaling plot from results.json"""
import json, math
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent.parent
r = json.loads((HERE / "report/evidence/results.json").read_text())

lin = [x for x in r["T_star_results"] if x["schedule"] == "linear"]
loc = [x for x in r["T_star_results"] if x["schedule"] == "local"]

Ns_l = np.array([x["N"] for x in lin])
Ts_l = np.array([x["T_star"] for x in lin])
Ns_o = np.array([x["N"] for x in loc])
Ts_o = np.array([x["T_star"] for x in loc])

fig, ax = plt.subplots(figsize=(7, 5))
ax.loglog(Ns_l, Ts_l, "o-", label=f"Linear schedule (fit slope {r['fits']['linear']['slope']:.3f})")
ax.loglog(Ns_o, Ts_o, "s-", label=f"Local-adiabatic schedule (fit slope {r['fits']['local']['slope']:.3f})")

# reference lines
xs = np.array([Ns_l.min(), Ns_l.max()])
ax.loglog(xs, xs, "k--", alpha=0.4, label="~ N (reference)")
ax.loglog(xs, np.sqrt(xs) * (Ts_o[0] / math.sqrt(Ns_o[0])), "k:", alpha=0.4, label=r"$\sim \sqrt{N}$ (reference)")

ax.set_xlabel("N (database size)")
ax.set_ylabel(r"$T^\ast$  (evolution time to reach $p_{\rm succ} \geq 1/2$)")
ax.set_title("Roland-Cerf (2001) replication: adiabatic Grover scaling")
ax.legend()
ax.grid(True, which="both", alpha=0.3)
fig.tight_layout()
fig.savefig(HERE / "report/evidence/scaling.png", dpi=140)
fig.savefig(HERE / "report/evidence/scaling.pdf")
print("wrote scaling.png / scaling.pdf")

# Also plot p_success(T) curves at N=64 for both schedules
fig2, ax2 = plt.subplots(figsize=(7, 5))
import sys
sys.path.insert(0, str(HERE / "code"))
from adiabatic_search import success_prob

N = 64
T_max_lin = 3.0 * N
T_max_loc = 3.0 * (math.pi / 2) * math.sqrt(N)
Ts_lin = np.linspace(0.5, T_max_lin, 25)
Ts_loc = np.linspace(0.5, T_max_loc, 25)
ps_lin = [success_prob(N, T, "linear") for T in Ts_lin]
ps_loc = [success_prob(N, T, "local") for T in Ts_loc]
ax2.plot(Ts_lin, ps_lin, "o-", label="linear")
ax2.plot(Ts_loc, ps_loc, "s-", label="local-adiabatic")
ax2.axhline(0.5, color="k", ls="--", alpha=0.5, label="p = 1/2 target")
ax2.set_xlabel("Total evolution time T")
ax2.set_ylabel(r"$p_{\rm succ}$ at $t=T$")
ax2.set_title(f"Success probability vs T at N={N}")
ax2.legend()
ax2.grid(True, alpha=0.3)
fig2.tight_layout()
fig2.savefig(HERE / "report/evidence/p_vs_T_N64.png", dpi=140)
print("wrote p_vs_T_N64.png")
