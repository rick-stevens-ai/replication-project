#!/usr/bin/env python3
"""Analyse FLUPS convergence sweep — fit log-log slope to L2 error vs h."""
import glob, math, os, sys, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.expanduser(
    "~/Dropbox/REPLICATE-PROJECT/PDE-replications/flups-poisson/results"
)
SCENARIOS = [
    ("unb_chat2", "Unbounded, CHAT2 (k=0)",
     "Caprace et al.: 2nd-order"),
    ("unb_hej4", "Unbounded, HEJ4 (k=3)",
     "Caprace et al.: 4th-order (Hejlesen regularised)"),
    ("per_chat2", "Periodic, CHAT2 (k=0)",
     "Caprace et al.: spectral / round-off"),
]


def load(scenario):
    rows = []
    for fp in sorted(glob.glob(f"{ROOT}/{scenario}/data/*.txt")):
        for ln in open(fp):
            parts = ln.split()
            if len(parts) < 3:
                continue
            rows.append((int(parts[0]), float(parts[1]), float(parts[2])))
    rows.sort()
    return rows


def fit(rows):
    if len(rows) < 2:
        return None, None, None
    N = np.array([r[0] for r in rows], dtype=float)
    h = 1.0 / N  # unit cube
    L2 = np.array([r[1] for r in rows], dtype=float)
    Linf = np.array([r[2] for r in rows], dtype=float)
    # ignore L2 entries that are near machine eps
    mask = L2 > 1e-13
    if mask.sum() >= 2:
        coeffs = np.polyfit(np.log(h[mask]), np.log(L2[mask]), 1)
        slope_l2 = coeffs[0]
    else:
        slope_l2 = float("nan")  # round-off limited
    mask = Linf > 1e-13
    if mask.sum() >= 2:
        coeffs = np.polyfit(np.log(h[mask]), np.log(Linf[mask]), 1)
        slope_linf = coeffs[0]
    else:
        slope_linf = float("nan")
    return h, L2, Linf, slope_l2, slope_linf


summary = []
fig, ax = plt.subplots(figsize=(7, 5))

for label, name, claim in SCENARIOS:
    rows = load(label)
    if not rows:
        print(f"{label}: NO DATA")
        continue
    h, L2, Linf, sl2, slinf = fit(rows)
    ax.loglog(h, np.maximum(L2, 1e-17), marker="o", label=f"{name}  slope={sl2:.2f}")
    summary.append({
        "scenario": label, "name": name, "claim": claim,
        "N":   [int(1/hi) for hi in h],
        "L2":  [float(x) for x in L2],
        "Linf":[float(x) for x in Linf],
        "fit_order_L2":   float(sl2),
        "fit_order_Linf": float(slinf),
    })

# reference slopes
h_ref = np.array([1/100, 1/10])
ax.loglog(h_ref, 1e-1*h_ref**2, "k--", alpha=0.4, label="ref slope 2")
ax.loglog(h_ref, 1e-1*h_ref**4, "k:",  alpha=0.4, label="ref slope 4")
ax.set_xlabel("h = 1/N")
ax.set_ylabel("L2 error")
ax.set_title("FLUPS convergence — unit-cube Poisson, Caprace-style sweep")
ax.legend(fontsize=8, loc="lower right")
ax.grid(True, which="both", alpha=0.3)
fig.tight_layout()
out_png = os.path.join(ROOT, "convergence.png")
fig.savefig(out_png, dpi=140)
print(f"wrote {out_png}")

with open(os.path.join(ROOT, "summary.json"), "w") as f:
    json.dump(summary, f, indent=2)
print(f"wrote {ROOT}/summary.json")

print("\n=== SUMMARY ===")
for s in summary:
    print(f"\n{s['name']}  [{s['claim']}]")
    print(f"   fit L2 slope   = {s['fit_order_L2']:.3f}")
    print(f"   fit Linf slope = {s['fit_order_Linf']:.3f}")
    for n, l2, li in zip(s["N"], s["L2"], s["Linf"]):
        print(f"      N={n:4d}   L2={l2:.4e}   Linf={li:.4e}")
