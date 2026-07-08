#!/usr/bin/env python3
"""Generate log-log error-vs-r plot."""
import json, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

here = Path(__file__).resolve().parent.parent
data = json.loads((here / "results/trotter_strang_scaling.json").read_text())
rows = data["rows"]
r = np.array([x["r"] for x in rows])
op_tr = np.array([x["op_err_trotter"] for x in rows])
op_st = np.array([x["op_err_strang"]  for x in rows])
st_tr = np.array([x["state_err_trotter"] for x in rows])
st_st = np.array([x["state_err_strang"]  for x in rows])

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

for ax, (a, b, la, lb, sa, sb, title) in zip(axes, [
    (op_tr, op_st, "Trotter (op-norm)", "Strang (op-norm)",
     data["fits"]["op_norm_trotter"]["slope"], data["fits"]["op_norm_strang"]["slope"],
     "Operator-norm error"),
    (st_tr, st_st, "Trotter (state |+>^n)", "Strang (state |+>^n)",
     data["fits"]["state_trotter"]["slope"], data["fits"]["state_strang"]["slope"],
     "State error on |+>^n"),
]):
    ax.loglog(r, a, "o-", label=f"{la}: slope={sa:+.3f}")
    ax.loglog(r, b, "s-", label=f"{lb}: slope={sb:+.3f}")
    # Reference lines
    ax.loglog(r, a[0] * (r / r[0]) ** -1.0, "--", color="gray", alpha=0.6, label="ref slope -1")
    ax.loglog(r, b[0] * (r / r[0]) ** -2.0, ":",  color="gray", alpha=0.6, label="ref slope -2")
    ax.set_xlabel("Trotter steps r")
    ax.set_ylabel("Error")
    ax.set_title(title)
    ax.legend(fontsize=8, loc="lower left")
    ax.grid(True, which="both", alpha=0.3)

fig.suptitle("Trotter (1st) & Strang (2nd) splitting error vs r — 4-site TFIM, t=1.0\nReplicating arXiv:2312.08044 predicted scalings", fontsize=11)
fig.tight_layout()
out = here / "results/err_vs_r.png"
fig.savefig(out, dpi=140, bbox_inches="tight")
print(f"wrote {out}")
