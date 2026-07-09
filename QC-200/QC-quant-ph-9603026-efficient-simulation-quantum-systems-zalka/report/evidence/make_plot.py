#!/usr/bin/env python3
"""Log-log plot of Trotter error vs step size, from trotter_results.json."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

here = Path(__file__).resolve().parent
data = json.loads((here / "trotter_results.json").read_text())
rows = data["rows"]

dts = np.array([r["dt"] for r in rows])
eps1 = np.array([r["eps1_frobenius"] for r in rows])
eps2 = np.array([r["eps2_frobenius"] for r in rows])

s1 = data["loglog_fit_order1"]["slope"]
s2 = data["loglog_fit_order2"]["slope"]

fig, ax = plt.subplots(figsize=(6.2, 4.6))
ax.loglog(dts, eps1, "o-", label=f"1st order Trotter  (fit slope={s1:.3f})")
ax.loglog(dts, eps2, "s-", label=f"2nd order Suzuki   (fit slope={s2:.3f})")

# reference lines
dt_ref = np.array([dts.min(), dts.max()])
ax.loglog(dt_ref, eps1[0] * (dt_ref / dts[0]) ** 1,   "--", color="gray",
          alpha=0.6, label=r"$\propto \Delta t$")
ax.loglog(dt_ref, eps2[0] * (dt_ref / dts[0]) ** 2,   ":",  color="gray",
          alpha=0.6, label=r"$\propto \Delta t^2$")

ax.set_xlabel(r"Trotter step $\Delta t = T/K$")
ax.set_ylabel(r"$\| U_{\rm Trotter} - U_{\rm exact} \|_F$")
ax.set_title("Zalka (1996) reproduction: 1D Heisenberg XXX, n=4, T=1")
ax.grid(True, which="both", alpha=0.3)
ax.legend(fontsize=9)
fig.tight_layout()

out = here / "trotter_error_vs_dt.png"
fig.savefig(out, dpi=140)
print(f"wrote {out}")
