#!/usr/bin/env python3
"""Make figures comparing replicated dose-response to paper Tables 2/3 and Fig 9."""
import csv
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SUMMARY = ROOT / "results" / "dose_response" / "summary.csv"
FIG_DIR = ROOT / "figures"
FIG_DIR.mkdir(exist_ok=True)

rows = list(csv.DictReader(SUMMARY.open()))
by_p = {}
for r in rows:
    by_p.setdefault(r["particle"], []).append(r)

# --- Paper Table 2: 280 kVp x-ray AG1522 fibroblasts (Cornforth & Bedford 1987) ---
paper_xray = {
    "dose": [1, 2, 4, 6, 9],
    "dic_invitro":   [0.038, 0.053, 0.250, 0.792, 1.31],
    "tot_invitro":   [0.19,  0.309, 0.946, 1.97,  3.49],
    "dic_insilico":  [0.10,  0.27,  0.79,  1.51,  2.23],
    "dic_insilico_e": [0.04, 0.09,  0.09,  0.11,  0.16],
    "tot_insilico":  [0.24,  0.46,  1.51,  2.56,  4.99],
    "tot_insilico_e": [0.05, 0.08,  0.12,  0.16,  0.18],
}

# --- Paper Table 3: 3.5 MeV alpha AG1522 (Cornforth et al 2002) ---
paper_alpha = {
    "dose": [0.6, 1.1, 1.7, 2.2],
    "dic_invitro":   [0.296, 0.667, 0.983, 1.170],
    "tot_invitro":   [1.074, 1.957, 2.750, 3.857],
    "dic_insilico":  [0.48,  0.94,  1.38,  1.79],
    "dic_insilico_e": [0.07, 0.05,  0.04,  0.04],
    "tot_insilico":  [1.07,  2.08,  3.04,  3.90],
    "tot_insilico_e": [0.03, 0.04,  0.03,  0.03],
}


def floats(rs, key):
    return np.array([float(r[key]) for r in rs])


# Figure 1: Electron dicentrics & total aberrations vs dose
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
e = by_p["electron"]
d = floats(e, "dose_Gy")

ax = axes[0]
ax.errorbar(d, floats(e, "dicentrics_mean"), yerr=floats(e, "dicentrics_sem"),
            fmt="o-", label="This rep (CherryRd, n=30/dose, dummy lib)", color="blue")
ax.plot(paper_xray["dose"], paper_xray["dic_invitro"], "rs--", label="Paper in-vitro (Cornforth 1987)")
ax.errorbar(paper_xray["dose"], paper_xray["dic_insilico"], yerr=paper_xray["dic_insilico_e"],
            fmt="g^--", label="Paper in-silico (Lim 2026)")
ax.set_xlabel("Dose (Gy)")
ax.set_ylabel("Dicentrics per cell")
ax.set_title("Electron (280 kVp x-ray surrogate)")
ax.legend(fontsize=8)
ax.grid(alpha=0.3)

ax = axes[1]
ax.errorbar(d, floats(e, "total_aberr_mean"), yerr=floats(e, "total_aberr_sem"),
            fmt="o-", label="This rep", color="blue")
ax.plot(paper_xray["dose"], paper_xray["tot_invitro"], "rs--", label="Paper in-vitro")
ax.errorbar(paper_xray["dose"], paper_xray["tot_insilico"], yerr=paper_xray["tot_insilico_e"],
            fmt="g^--", label="Paper in-silico")
ax.set_xlabel("Dose (Gy)")
ax.set_ylabel("Total lethal aberrations per cell")
ax.set_title("Electron — Table 2 comparison")
ax.legend(fontsize=8)
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(FIG_DIR / "fig_electron_table2.png", dpi=150)
plt.close()

# Figure 2: Alpha
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
a = by_p["alpha"]
d = floats(a, "dose_Gy")

ax = axes[0]
ax.errorbar(d, floats(a, "dicentrics_mean"), yerr=floats(a, "dicentrics_sem"),
            fmt="o-", label="This rep (CherryRd, n=30/dose, dummy lib)", color="blue")
ax.plot(paper_alpha["dose"], paper_alpha["dic_invitro"], "rs--", label="Paper in-vitro (Cornforth 2002)")
ax.errorbar(paper_alpha["dose"], paper_alpha["dic_insilico"], yerr=paper_alpha["dic_insilico_e"],
            fmt="g^--", label="Paper in-silico (Lim 2026)")
ax.set_xlabel("Dose (Gy)")
ax.set_ylabel("Dicentrics per cell")
ax.set_title("Alpha (3.5 MeV 238Pu surrogate)")
ax.legend(fontsize=8)
ax.grid(alpha=0.3)

ax = axes[1]
ax.errorbar(d, floats(a, "total_aberr_mean"), yerr=floats(a, "total_aberr_sem"),
            fmt="o-", label="This rep", color="blue")
ax.plot(paper_alpha["dose"], paper_alpha["tot_invitro"], "rs--", label="Paper in-vitro")
ax.errorbar(paper_alpha["dose"], paper_alpha["tot_insilico"], yerr=paper_alpha["tot_insilico_e"],
            fmt="g^--", label="Paper in-silico")
ax.set_xlabel("Dose (Gy)")
ax.set_ylabel("Total lethal aberrations per cell")
ax.set_title("Alpha — Table 3 comparison")
ax.legend(fontsize=8)
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(FIG_DIR / "fig_alpha_table3.png", dpi=150)
plt.close()

# Figure 3: Survival fraction for all three particles
fig, ax = plt.subplots(1, 1, figsize=(7, 5))
colors = {"electron": "tab:blue", "proton": "tab:orange", "alpha": "tab:red"}
for p, color in colors.items():
    if p not in by_p:
        continue
    rs = by_p[p]
    d = floats(rs, "dose_Gy")
    sf = floats(rs, "surviving_fraction")
    se = floats(rs, "surviving_fraction_sem")
    ax.errorbar(d, sf, yerr=se, fmt="o-", color=color, label=p)
ax.set_yscale("log")
ax.set_ylim(0.01, 1.2)
ax.set_xlabel("Dose (Gy)")
ax.set_ylabel("Surviving fraction")
ax.set_title("Per-particle survival (this replication, dummy library, n=30/dose)")
ax.legend()
ax.grid(alpha=0.3, which="both")
plt.tight_layout()
plt.savefig(FIG_DIR / "fig_survival.png", dpi=150)
plt.close()

# Figure 4: DSB yield per Gy (paper Fig 9 sanity check)
fig, ax = plt.subplots(1, 1, figsize=(7, 5))
for p, color in colors.items():
    if p not in by_p:
        continue
    rs = by_p[p]
    d = floats(rs, "dose_Gy")
    yld = floats(rs, "mean_DSBs_per_cell") / d
    ax.plot(d, yld, "o-", color=color, label=f"{p} (this rep)")
# Paper Fig 9 plateaus (high-energy):
ax.axhline(34, ls="--", color="tab:blue", alpha=0.5, label="paper plateau e- 34")
ax.axhline(43, ls="--", color="tab:orange", alpha=0.5, label="paper plateau p 43")
ax.axhline(65, ls="--", color="tab:red", alpha=0.5, label="paper plateau alpha 65")
ax.set_xlabel("Dose (Gy)")
ax.set_ylabel("DSBs per cell per Gy")
ax.set_title("DSB yield vs dose (vs paper Fig 9 plateaus)")
ax.legend(fontsize=8)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(FIG_DIR / "fig_dsb_yield.png", dpi=150)
plt.close()

print("Wrote figures to", FIG_DIR)
for f in sorted(FIG_DIR.glob("*.png")):
    print(" ", f.name, f.stat().st_size, "bytes")
