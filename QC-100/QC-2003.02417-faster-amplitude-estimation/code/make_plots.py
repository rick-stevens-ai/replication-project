"""Generate Fig-3-style plots (log-log Norac vs 1/epsilon) for FAE and MLAE."""

import csv
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
EVIDENCE_DIR = os.path.normpath(os.path.join(HERE, "..", "report", "evidence"))

with open(os.path.join(EVIDENCE_DIR, "sweep_raw.csv")) as f:
    rows = list(csv.DictReader(f))

# Convert numeric
for r in rows:
    for k in list(r.keys()):
        try:
            r[k] = float(r[k]) if r[k] != "" else None
        except ValueError:
            pass

a_values = sorted({r["a"] for r in rows if r["a"] is not None})

with open(os.path.join(EVIDENCE_DIR, "fits.json")) as f:
    fit_data = json.load(f)
fits_by_a = {f["a"]: f for f in fit_data["fits"]}

fig, axes = plt.subplots(2, 2, figsize=(10, 8))
for idx, a in enumerate(a_values):
    ax = axes[idx // 2][idx % 2]
    fae = [r for r in rows if r["algo"] == "FAE" and r["a"] == a]
    mla = [r for r in rows if r["algo"] == "MLAE" and r["a"] == a]
    fae_eps = np.array([r["eps_p95"] for r in fae])
    fae_nor = np.array([r["norac_median"] for r in fae])
    mla_eps = np.array([r["eps_p95"] for r in mla])
    mla_nor = np.array([r["norac_median"] for r in mla])

    ax.loglog(1.0 / fae_eps, fae_nor, "go", label="FAE (this work)")
    ax.loglog(1.0 / mla_eps, mla_nor, "rs", label="MLAE (Suzuki 2019)")

    # Fit lines
    fit = fits_by_a[a]
    xs = np.logspace(np.log10(min(1 / fae_eps.min(), 1 / mla_eps.min())) - 0.1,
                     np.log10(max(1 / fae_eps.max(), 1 / mla_eps.max())) + 0.1, 100)
    # Line: N = C * (1/eps)^slope
    ax.loglog(xs, fit["FAE_prefactor_C"] * xs ** fit["FAE_slope"],
              "g-", alpha=0.7, label=f"FAE fit: slope={fit['FAE_slope']:.2f}")
    ax.loglog(xs, fit["MLAE_prefactor_C"] * xs ** fit["MLAE_slope"],
              "r--", alpha=0.7, label=f"MLAE fit: slope={fit['MLAE_slope']:.2f}")

    ax.set_xlabel("1 / ε")
    ax.set_ylabel("N_orac (median)")
    ax.set_title(f"a = {a}")
    ax.grid(True, which="both", ls=":", alpha=0.5)
    ax.legend(fontsize=8, loc="lower right")

plt.suptitle("QC-100 replication of Nakaji 2020 (arXiv:2003.02417) Fig. 3\n"
             "FAE vs MLAE, ε = 95th-percentile amplitude error over trials", fontsize=11)
plt.tight_layout()
out_path = os.path.join(EVIDENCE_DIR, "fig3_replication.png")
plt.savefig(out_path, dpi=120)
print(f"Saved {out_path}")

# Also make a text summary table
summary = []
for a in a_values:
    fae = [r for r in rows if r["algo"] == "FAE" and r["a"] == a]
    mla = [r for r in rows if r["algo"] == "MLAE" and r["a"] == a]
    fit = fits_by_a[a]
    summary.append({
        "a": a,
        "FAE_ell_min": min(r["ell"] for r in fae if r.get("ell") is not None),
        "FAE_ell_max": max(r["ell"] for r in fae if r.get("ell") is not None),
        "FAE_eps_min": min(r["eps_p95"] for r in fae),
        "FAE_eps_max": max(r["eps_p95"] for r in fae),
        "FAE_norac_max": max(r["norac_median"] for r in fae),
        "FAE_slope": fit["FAE_slope"],
        "FAE_R2": fit["FAE_R2"],
        "MLAE_eps_min": min(r["eps_p95"] for r in mla),
        "MLAE_norac_max": max(r["norac_median"] for r in mla),
        "MLAE_slope": fit["MLAE_slope"],
        "MLAE_R2": fit["MLAE_R2"],
    })

with open(os.path.join(EVIDENCE_DIR, "summary.json"), "w") as f:
    json.dump(summary, f, indent=2)
print("Wrote summary.json")
