"""Analyze the benchmark: fit power-law slope in the clean regime (before floating-point floor)."""

import json
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

d = json.loads(Path("../report/evidence/02_benchmark_N4_t1.json").read_text())
r_vals = np.array(d["r_values"], dtype=float)

print(f"{'method':22s}  {'2m_expected':>12s}  {'slope_fit':>10s}  {'||a||_1':>8s}  {'||k||_1':>7s}  {'min_err':>10s}")
print("-" * 90)

# Fit slope in the "clean" regime where err > 1e-11 (floating point floor)
summary_rows = []
for name, info in d["methods"].items():
    errs = np.array(info["errors"], dtype=float)
    order = info.get("order_2m", None)
    # Use points with err between 1e-11 and 1e-1
    mask = (errs > 1e-11) & (errs < 1e-1) & np.isfinite(errs)
    slope = None
    if mask.sum() >= 3:
        lr = np.log(r_vals[mask])
        le = np.log(errs[mask])
        p = np.polyfit(lr, le, 1)
        slope = p[0]
    cond = info.get("cond_a_1", 1.0)
    kn = info.get("k_1", 1)
    print(f"{name:22s}  {order!s:>12s}  {slope if slope is not None else 'nan':>10}  "
          f"{cond:8.4f}  {kn:7d}  {min(errs):.3e}")
    summary_rows.append((name, order, slope, cond, kn, float(min(errs))))

# Save as JSON for the report
import json as J
out = {
    "note": "slope_fit is negative; error ~ r^slope, so ideal slope = -(2m).",
    "rows": [
        {"method": n, "order_2m": o, "slope_fit": s, "cond_a_1": c, "k_1": k, "min_err": e}
        for (n, o, s, c, k, e) in summary_rows
    ],
}
Path("../report/evidence/03_slopes.json").write_text(J.dumps(out, indent=2))
print("\nWrote 03_slopes.json")

# ---- Figure: err vs r for a few representative methods
fig, ax = plt.subplots(1, 1, figsize=(7, 5.5))
plot_methods = [
    ("U2", "s-", "k"),
    ("U4", "d-", "gray"),
    ("chin_m3", "^-", "gold"),
    ("chin_m5", "^-", "orange"),
    ("paper_table_m3", "o-", "steelblue"),
    ("paper_table_m5", "o-", "royalblue"),
    ("paper_table_m6", "o-", "navy"),
]
for name, style, color in plot_methods:
    if name not in d["methods"]:
        continue
    errs = np.array(d["methods"][name]["errors"], dtype=float)
    lbl = f"{name} (2m={d['methods'][name].get('order_2m','?')})"
    ax.loglog(r_vals, errs, style, color=color, label=lbl, markersize=5)

ax.set_xlabel(r"number of steps $r = t/\Delta$")
ax.set_ylabel(r"operator-norm error $\|U_{\rm approx}(t) - e^{-iHt}\|_2$")
ax.set_title(f"1D Heisenberg N={d['N']}, t={d['t']}: Trotter vs multiproduct formulas")
ax.grid(True, which="both", ls=":", alpha=0.5)
ax.legend(loc="best", fontsize=8)
ax.set_ylim(1e-15, 10)
fig.tight_layout()
fig.savefig("../report/evidence/fig_convergence.png", dpi=130)
print("Wrote fig_convergence.png")

# ---- Figure: ||a||_1 vs order for Chin vs well-conditioned families
fig2, ax2 = plt.subplots(figsize=(6.5, 5))
for family in ["chin", "rounded_int", "paper_table"]:
    xs, ys = [], []
    for name, info in d["methods"].items():
        if name.startswith(family + "_m"):
            xs.append(info["order_2m"])
            ys.append(info["cond_a_1"])
    if xs:
        xs, ys = zip(*sorted(zip(xs, ys)))
        ax2.semilogy(xs, ys, "o-", label=family)
ax2.set_xlabel("integrator order 2m")
ax2.set_ylabel(r"condition number $\|\vec a\|_1$")
ax2.set_title("Condition-number scaling: Chin (exponential) vs well-conditioned")
ax2.grid(True, which="both", ls=":", alpha=0.5)
ax2.legend()
fig2.tight_layout()
fig2.savefig("../report/evidence/fig_condition.png", dpi=130)
print("Wrote fig_condition.png")
