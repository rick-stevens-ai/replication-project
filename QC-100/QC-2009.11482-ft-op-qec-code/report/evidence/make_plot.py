#!/usr/bin/env python3
"""Log-log plot of Bacon-Shor [[9,1,3]] Z-memory sim results."""
import json
import sys
from pathlib import Path

import numpy as np

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ImportError:
    print("matplotlib not installed; skipping plot")
    sys.exit(0)

data_path = Path(__file__).parent.parent / "data" / "results.json"
with open(data_path) as f:
    r = json.load(f)

p = np.array(r["p_values"])
ft = np.array(r["ft_logical"])
nft = np.array(r["non_ft_logical"])
un = np.array(r["unencoded_logical"])

# Guard log10 of zero: replace 0 with a tiny value for plotting.
def safe(y):
    return np.where(y > 0, y, 1 / (2 * r["shots"]))

fig, ax = plt.subplots(figsize=(7, 5.5))
ax.loglog(p, safe(ft), "o-", label="FT Bacon-Shor [[9,1,3]] (2 anc, ordered CX)")
ax.loglog(p, safe(nft), "s--", label="Non-FT Bacon-Shor (amplified ancilla noise)")
ax.loglog(p, safe(un), "^-.", label="Unencoded single qubit")

# Reference lines: p (slope 1) and p^2 (slope 2), passing through the mid-range
pmid = 0.005
ax.loglog(
    p, pmid * (p / pmid), color="gray", lw=0.8, ls=":", label=r"$\propto p$"
)
ax.loglog(
    p, pmid * (p / pmid) ** 2, color="gray", lw=0.8, ls="--", label=r"$\propto p^2$"
)

ax.set_xlabel("Physical error rate $p$ (depolarizing per op)")
ax.set_ylabel("Logical error rate $p_L$ (per experiment)")
ax.set_title(
    f"Bacon-Shor [[9,1,3]] Z-memory  rounds={r['rounds']}  shots={r['shots']:,}\n"
    f"Replication baseline for arXiv:2009.11482 (Egan et al. 2020)"
)
ax.grid(True, which="both", alpha=0.3)
ax.legend(loc="lower right", fontsize=8)

# Slope annotations
if "ft_slope_low_p" in r:
    txt = (
        f"low-p log-log slopes:\n"
        f"  FT       : {r['ft_slope_low_p']:.2f}\n"
        f"  Non-FT   : {r['non_ft_slope_low_p']:.2f}\n"
        f"  Unencoded: {r['unencoded_slope_low_p']:.2f}"
    )
    ax.text(0.02, 0.98, txt, transform=ax.transAxes, va="top",
            fontsize=9, family="monospace",
            bbox=dict(facecolor="white", alpha=0.85, boxstyle="round,pad=0.4"))

out_png = Path(__file__).parent.parent / "report" / "evidence" / "logical_error_curve.png"
out_png.parent.mkdir(parents=True, exist_ok=True)
plt.tight_layout()
plt.savefig(out_png, dpi=150)
print(f"Wrote {out_png}")
