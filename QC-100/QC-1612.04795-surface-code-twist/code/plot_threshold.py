#!/usr/bin/env python3
"""Plot LER vs p for both regimes and mark the estimated thresholds."""
import json
from pathlib import Path

EV = Path(__file__).resolve().parents[1] / "report" / "evidence"

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ImportError:
    print("matplotlib not installed; skipping plot")
    raise SystemExit(0)

rows = json.loads((EV / "threshold_scan.json").read_text())

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
for ax, regime, thr_paper, thr_ours, title in [
    (axes[0], "A_ideal_syndrome", 0.10, 0.14,
     "Regime A: ideal syndrome, 1 round (depolarizing data noise)"),
    (axes[1], "B_phenomenological", 0.032, 0.038,
     "Regime B: phenomenological, d rounds (data depol + noisy meas)"),
]:
    by_d = {}
    for r in rows:
        if r["regime"] == regime:
            by_d.setdefault(r["d"], []).append((r["p"], r["logical_error_rate"]))
    for d in sorted(by_d):
        pts = sorted(by_d[d])
        ps = [p for p, _ in pts]
        lers = [l for _, l in pts]
        ax.plot(ps, lers, marker="o", label=f"d={d}")
    ax.axvline(thr_paper, color="red", linestyle="--", alpha=0.6,
               label=f"paper ≈ {thr_paper:.3f}")
    ax.axvline(thr_ours, color="green", linestyle=":", alpha=0.6,
               label=f"ours ≈ {thr_ours:.3f}")
    ax.set_xlabel("physical error rate p")
    ax.set_ylabel("logical error rate")
    ax.set_yscale("log")
    ax.set_title(title, fontsize=10)
    ax.legend(loc="lower right", fontsize=8)
    ax.grid(True, alpha=0.3)

fig.suptitle(
    "Rotated surface code — threshold reproduction for Yoder & Kim 2017 (arXiv:1612.04795)",
    fontsize=11,
)
fig.tight_layout()
out = EV / "threshold_plot.png"
fig.savefig(out, dpi=140)
print("wrote", out)
