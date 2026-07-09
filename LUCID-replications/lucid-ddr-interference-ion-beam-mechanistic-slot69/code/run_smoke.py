"""
LUCID slot 69 smoke driver.

Runs:
  (1) Photon SF curves for the five Liew 2019 Table 1 cell lines (no DDRi).
  (2) Photon SF curves for H460 + H1437 under three ATM-inhibitor RSF
      values (Liew 2019 Table 3). Checks the headline qualitative behaviour
      (DDRi steepens the curve).
  (3) LET sweep at SF=10% for H460 with and without ATMi-500nM, showing
      the headline mechanistic claim of the 2021 IJROBP paper:
      *the RBE-gain from DDRi shrinks with LET*.

Outputs:
  results/smoke_summary.json
  results/photon_survival_no_ddri.csv
  results/photon_survival_atmi.csv
  results/let_sweep_ddri.csv
  figures/photon_no_ddri.png
  figures/photon_atmi.png
  figures/let_sweep_rbe_ratio.png
"""
from __future__ import annotations
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RESULTS = ROOT / "results"
FIGS = ROOT / "figures"
LOGS = ROOT / "logs"
for p in (RESULTS, FIGS, LOGS):
    p.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(HERE))
from universe_smoke import (  # noqa: E402
    CellLine, LIEW2019_CELLS, LIEW2019_ATMI_RSF,
    survival_curve_photon, lq_alpha_beta_from_universe,
    survival_photon, rbe_at_survival,
)

T0 = time.time()
SUMMARY = {"slot": 69, "doi": "10.1016/j.ijrobp.2021.09.048",
           "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}

# ---------------------------------------------------------------------------
# (1) Photon SF curves, no DDRi — validate the GLOBLE/UNIVERSE backbone
# ---------------------------------------------------------------------------
doses = np.array([0.5, 1, 2, 3, 4, 5, 6, 8, 10], dtype=float)
print("[1] Photon SF curves, no DDRi (Liew 2019 Table 1 cells)...")
sf_matrix = np.zeros((len(LIEW2019_CELLS), len(doses)))
ab_table = []
for i, (name, cell) in enumerate(LIEW2019_CELLS.items()):
    sf = survival_curve_photon(doses, cell, n_iter=4000, seed=42 + i)
    sf_matrix[i, :] = sf
    a, b = lq_alpha_beta_from_universe(cell, dose_range=(1, 2, 4, 6, 8),
                                       n_iter=4000, seed=42 + i)
    ab_table.append((name, a, b, a / max(b, 1e-9)))
    print(f"  {name:6s}: SF@2Gy={sf[2]:.3f}  SF@6Gy={sf[5]:.3f}  "
          f"alpha={a:.3f} Gy^-1  beta={b:.4f} Gy^-2  alpha/beta={a/max(b,1e-9):.2f} Gy")

with open(RESULTS / "photon_survival_no_ddri.csv", "w") as fh:
    fh.write("cell_line," + ",".join(f"SF_{d:g}Gy" for d in doses) + "\n")
    for (name, _), sf in zip(LIEW2019_CELLS.items(), sf_matrix):
        fh.write(name + "," + ",".join(f"{x:.5f}" for x in sf) + "\n")

with open(RESULTS / "lq_fits.csv", "w") as fh:
    fh.write("cell_line,alpha_Gy-1,beta_Gy-2,alpha_over_beta_Gy\n")
    for name, a, b, ab in ab_table:
        fh.write(f"{name},{a:.5f},{b:.6f},{ab:.3f}\n")

fig, ax = plt.subplots(figsize=(6.5, 5))
for (name, _), sf in zip(LIEW2019_CELLS.items(), sf_matrix):
    ax.semilogy(doses, sf, "-o", label=name)
ax.set_xlabel("Dose (Gy)")
ax.set_ylabel("Surviving fraction")
ax.set_title("UNIVERSE photon survival — Liew 2019 normoxia cells")
ax.set_ylim(1e-3, 1.2)
ax.grid(True, which="both", alpha=0.3)
ax.legend(loc="lower left", fontsize=9)
fig.tight_layout()
fig.savefig(FIGS / "photon_no_ddri.png", dpi=130)
plt.close(fig)

SUMMARY["photon_no_ddri"] = {
    "doses_Gy": doses.tolist(),
    "cells": list(LIEW2019_CELLS.keys()),
    "sf_at_2Gy": {n: float(sf_matrix[i, 2]) for i, n in enumerate(LIEW2019_CELLS)},
    "sf_at_6Gy": {n: float(sf_matrix[i, 5]) for i, n in enumerate(LIEW2019_CELLS)},
    "lq_fits": {name: {"alpha_Gy-1": a, "beta_Gy-2": b, "alpha_over_beta_Gy": ab}
                for (name, a, b, ab) in ab_table},
}

# ---------------------------------------------------------------------------
# (2) Photon + DDRi — Liew 2019 Table 3 RSF values for H460 + H1437
# ---------------------------------------------------------------------------
print("\n[2] Photon SF curves under ATM-inhibitor (Liew 2019 Table 3)...")
ddri_doses = np.array([0.5, 1, 2, 3, 4, 5, 6], dtype=float)
atmi_results = {}
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), sharey=True)
for ax, (name, conds) in zip(axes, LIEW2019_ATMI_RSF.items()):
    base = LIEW2019_CELLS[name]
    atmi_results[name] = {"doses_Gy": ddri_doses.tolist(), "by_condition": {}}
    for label, rsf in conds.items():
        cell = CellLine(name, base.K_iDSB, base.K_cDSB, RSF=rsf)
        sf = survival_curve_photon(ddri_doses, cell, n_iter=4000, seed=hash(name+label) & 0xFFFF)
        ax.semilogy(ddri_doses, sf, "-o", label=f"{label} (RSF={rsf:.2f})")
        atmi_results[name]["by_condition"][label] = {
            "RSF": rsf, "sf": [float(x) for x in sf],
        }
        print(f"  {name} {label} (RSF={rsf:.2f}): SF@2Gy={sf[2]:.3f}  SF@6Gy={sf[-1]:.3f}")
    ax.set_xlabel("Dose (Gy)")
    ax.set_title(f"{name} + ATM inhibitor")
    ax.set_ylim(1e-4, 1.2)
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(loc="lower left", fontsize=8)
axes[0].set_ylabel("Surviving fraction")
fig.suptitle("UNIVERSE + DDRi (RSF on K_iDSB) — Liew 2019 Table 3")
fig.tight_layout()
fig.savefig(FIGS / "photon_atmi.png", dpi=130)
plt.close(fig)

# Save a long-form CSV
with open(RESULTS / "photon_survival_atmi.csv", "w") as fh:
    fh.write("cell_line,condition,RSF," + ",".join(f"SF_{d:g}Gy" for d in ddri_doses) + "\n")
    for name, conds in atmi_results.items():
        for label, d in conds["by_condition"].items():
            fh.write(f"{name},{label},{d['RSF']:.3f},"
                     + ",".join(f"{x:.5f}" for x in d["sf"]) + "\n")
SUMMARY["photon_atmi"] = atmi_results

# Headline check: ratio SF(DDRi)/SF(noDDRi) should drop monotonically with dose
# and with RSF -- the basic DDRi steepening expected by the paper.
ratios = {}
for name, conds in LIEW2019_ATMI_RSF.items():
    base_sf = np.array(atmi_results[name]["by_condition"]["DMSO"]["sf"])
    for label, rsf in conds.items():
        if label == "DMSO":
            continue
        dd_sf = np.array(atmi_results[name]["by_condition"][label]["sf"])
        ratios[f"{name}_{label}"] = (dd_sf / base_sf).tolist()
SUMMARY["sf_ratio_ddri_over_noddri"] = ratios

# ---------------------------------------------------------------------------
# (3) Headline mechanistic test of the 2021 IJROBP paper:
#     RBE_DDRi / RBE_noDDRi as a function of LET. Expectation: this ratio
#     should DECREASE as LET rises (DDRi loses effectiveness at high LET).
# ---------------------------------------------------------------------------
print("\n[3] LET sweep — RBE_DDRi / RBE_noDDRi as a function of LET (headline test)...")
lets = np.array([2.0, 5.0, 10.0, 20.0, 30.0, 50.0, 80.0, 120.0], dtype=float)
base = LIEW2019_CELLS["H460"]
ddri = CellLine("H460", base.K_iDSB, base.K_cDSB, RSF=4.21)  # ATMi 500 nM

let_results = []
for L in lets:
    r = rbe_at_survival(base, ddri, LET_keV_um=float(L), survival_level=0.1, seed=7)
    let_results.append((float(L), r["noDDRi"]["RBE"], r["DDRi"]["RBE"],
                        r["RBE_ratio_DDRi_over_noDDRi"]))
    print(f"  LET={L:6.1f} keV/um  RBE_noDDRi={r['noDDRi']['RBE']:.3f}  "
          f"RBE_DDRi={r['DDRi']['RBE']:.3f}  ratio={r['RBE_ratio_DDRi_over_noDDRi']:.3f}")

with open(RESULTS / "let_sweep_ddri.csv", "w") as fh:
    fh.write("LET_keV_per_um,RBE_noDDRi,RBE_DDRi,RBE_ratio_DDRi_over_noDDRi\n")
    for row in let_results:
        fh.write(",".join(f"{x:.4f}" for x in row) + "\n")

fig, ax = plt.subplots(figsize=(6.5, 4.5))
arr = np.array(let_results)
ax.plot(arr[:, 0], arr[:, 1], "-s", label="RBE (no DDRi)")
ax.plot(arr[:, 0], arr[:, 2], "-o", label="RBE (ATMi 500 nM)")
ax2 = ax.twinx()
ax2.plot(arr[:, 0], arr[:, 3], "--^", color="tab:red",
         label="RBE_DDRi / RBE_noDDRi")
ax.set_xlabel("Dose-averaged LET (keV/µm)")
ax.set_ylabel("RBE at SF=10%")
ax2.set_ylabel("RBE ratio (DDRi/no-DDRi)", color="tab:red")
ax.set_xscale("log")
ax.grid(True, which="both", alpha=0.3)
ax.legend(loc="upper left", fontsize=9)
ax2.legend(loc="upper right", fontsize=9)
ax.set_title("UNIVERSE+DDRi headline mechanism — RBE-ratio falls with LET")
fig.tight_layout()
fig.savefig(FIGS / "let_sweep_rbe_ratio.png", dpi=130)
plt.close(fig)

ratio_series = [r[3] for r in let_results]
peak_idx = int(np.argmax(ratio_series))
highlet_drop = ratio_series[peak_idx] - ratio_series[-1]
SUMMARY["let_sweep"] = {
    "LET_keV_um": [r[0] for r in let_results],
    "RBE_noDDRi": [r[1] for r in let_results],
    "RBE_DDRi": [r[2] for r in let_results],
    "RBE_ratio_DDRi_over_noDDRi": ratio_series,
    "headline_check_RBE_ratio_falls_after_peak": bool(highlet_drop > 0.3),
    "headline_peak_at_LET_keV_um": float(let_results[peak_idx][0]),
    "headline_drop_from_peak_to_max_LET": float(highlet_drop),
}

# ---------------------------------------------------------------------------
# Persist summary
# ---------------------------------------------------------------------------
SUMMARY["elapsed_seconds"] = round(time.time() - T0, 2)
SUMMARY["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
with open(RESULTS / "smoke_summary.json", "w") as fh:
    json.dump(SUMMARY, fh, indent=2)

print(f"\nDone in {SUMMARY['elapsed_seconds']}s. Wrote:")
for p in [RESULTS / "smoke_summary.json", RESULTS / "photon_survival_no_ddri.csv",
          RESULTS / "lq_fits.csv", RESULTS / "photon_survival_atmi.csv",
          RESULTS / "let_sweep_ddri.csv",
          FIGS / "photon_no_ddri.png", FIGS / "photon_atmi.png",
          FIGS / "let_sweep_rbe_ratio.png"]:
    print("  ", p.relative_to(ROOT))
