#!/usr/bin/env python3
"""Generate the paper-comparison plot analogous to Fig 4(a) of Takita et al. 2016."""
import json
from pathlib import Path

import numpy as np

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAVE_MPL = True
except ImportError:
    HAVE_MPL = False

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "report/evidence/results_main.json").read_text())

if not HAVE_MPL:
    print("matplotlib not installed; skipping plot.")
    raise SystemExit(0)

fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharex=True, sharey=True)
for ax, stab in zip(axes, ("Sz", "Sx")):
    # Use flag encoding + single noise (best FT demonstration)
    rows_flag = data["results"]["flag"]["single"][stab]
    rows_cat = data["results"]["cat"]["single"][stab]

    ps = [r["p"] for r in rows_flag if r["p"] > 0]
    bare = [r["bare_p_err"] for r in rows_flag if r["p"] > 0]
    La_flag = [r["err_La"] for r in rows_flag if r["p"] > 0]
    Lb_flag = [r["err_Lb"] for r in rows_flag if r["p"] > 0]
    La_cat = [r["err_La"] for r in rows_cat if r["p"] > 0]
    Lb_cat = [r["err_Lb"] for r in rows_cat if r["p"] > 0]

    ax.loglog(ps, bare, "k-", label="physical qubit (bare)", linewidth=2)
    ax.loglog(ps, La_flag, "b-o", label="La (flag encoding, FT)", markersize=6)
    ax.loglog(ps, Lb_flag, "b--s", label="Lb (flag encoding, NFT)", markersize=6, alpha=0.8)
    ax.loglog(ps, La_cat, "r-o", label="La (cat encoding, non-FT)", markersize=4, alpha=0.6)
    ax.loglog(ps, Lb_cat, "r--s", label="Lb (cat encoding)", markersize=4, alpha=0.6)

    # reference p and p^2 slopes
    p_arr = np.array(ps)
    ax.loglog(p_arr, 0.3 * p_arr, "gray", linestyle=":", alpha=0.5, label=r"$\propto p$")
    ax.loglog(p_arr, 0.7 * p_arr**2, "gray", linestyle="-.", alpha=0.5, label=r"$\propto p^2$")

    ax.set_xlabel("physical error rate p")
    ax.set_ylabel("logical / physical error probability")
    ax.set_title(f"|00>_L prep + {stab} stabilizer measurement")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(loc="lower right", fontsize=7)

plt.suptitle(
    "Replication of Takita+2016 [[4,2,2]] FT error detection (arXiv:1611.06946) — Stim simulation",
    fontsize=12,
)
plt.tight_layout()
out = ROOT / "report/evidence/fig4_replication.png"
plt.savefig(out, dpi=150)
print(f"Wrote {out}")
