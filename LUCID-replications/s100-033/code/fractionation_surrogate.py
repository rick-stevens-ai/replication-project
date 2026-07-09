#!/usr/bin/env python3
"""s100-033 lightweight surrogate.

Goal: test the qualitative claims of Liu et al. (PMB 2021,
doi 10.1088/1361-6560/abd4f9, "RADCELL") without re-implementing
Geant4 + CompuCell3D.

We use a logistic-growth + linear-quadratic (LQ) per-fraction kill model.
The CPM-specific 30.37% number and the "5 Gy/5fx exceeds control"
contact-inhibition effect are NOT in scope -- we only check that:

  (a) growth-rate is monotone decreasing in total dose
      across the six dose schemes of Fig. 6a
      (5,10,15,20,25,30 Gy / 5 fx),
  (b) at equal total dose (40 Gy), 2 fractions kill more cells
      than 5 fractions, with a percent difference in the
      neighborhood of the paper's 30.37% claim (Fig. 7a).

Outputs:
  figures/fig_fractionation.png
  figures/fig_40Gy_hyper_vs_hypo.png
  evidence/surrogate_numbers.json
"""
from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "figures"
EVI = ROOT / "evidence"
FIG.mkdir(exist_ok=True)
EVI.mkdir(exist_ok=True)


# ---- model parameters ---------------------------------------------------
# 1 MCS = 1 min (paper Sec 3.4). All time below is in MCS.
TOTAL_MCS = 17000           # matches the Sec 3.5 hyperfractionation case
DT = 1                      # MCS

# Logistic growth: dN/dt = r N (1 - N/K)
# Calibrated by eye to give roughly the no-dose growth shape of Fig. 4a/6a:
# starts ~80 cells at t=0, grows several-fold by 14000 MCS.
N0 = 80.0
K = 1500.0                  # carrying capacity in cells
R = 4.0e-4                  # /MCS  (~0.4/hr typical)

# LQ kill per fraction. The paper does not give an explicit (alpha, beta)
# because it is a CPM-coupled state-transition model, not LQ. We use
# reasonable tumor-like values: alpha = 0.10 Gy^-1, beta = 0.020 Gy^-2.
ALPHA = 0.10
BETA = 0.020

# Geometric factor: a single planar 50 um microbeam hits only a strip of
# the tumor in the paper's single-beam example (Sec 3.5.2/3). Lattice is
# 50x50 voxels (200x200 um) wide; a 50 um beam directly irradiates ~25%
# of cell COMs. Cells outside the beam strip receive only scatter dose.
# We model this with an effective hit fraction f_hit; cells outside are
# largely spared. Equivalent to surviving fraction =
#    (1 - f_hit) + f_hit * exp(-(a*d + b*d^2))
F_HIT_SINGLE_BEAM = 0.30


@dataclass
class DoseSchedule:
    name: str
    fractions: list  # list of (mcs, dose_per_fraction_Gy)


def lq_survival(dose_per_fx_Gy: float, f_hit: float = F_HIT_SINGLE_BEAM) -> float:
    s_irr = float(np.exp(-(ALPHA * dose_per_fx_Gy + BETA * dose_per_fx_Gy ** 2)))
    return (1.0 - f_hit) + f_hit * s_irr


def simulate(schedule: DoseSchedule, total_mcs: int = TOTAL_MCS) -> np.ndarray:
    """Return cell-count time series N[0..total_mcs] for the given schedule."""
    t = np.arange(0, total_mcs + 1, dtype=float)
    N = np.empty_like(t)
    N[0] = N0
    sched = dict(schedule.fractions)  # mcs -> dose_per_fx
    for k in range(1, len(t)):
        # logistic step
        Nk = N[k - 1]
        Nk = Nk + DT * R * Nk * (1.0 - Nk / K)
        # apply any dose due at this MCS
        if (k in sched):
            Nk *= lq_survival(sched[k])
        N[k] = max(Nk, 0.0)
    return t, N


# ---- 1) six dose schemes of Fig. 6a -------------------------------------
# Doses 5..30 Gy in 5 fractions delivered at 1000, 5000, 7000, 9000, 11000 MCS.
FX_TIMES_6 = [1000, 5000, 7000, 9000, 11000]

dose_schemes = []
for total_Gy in [0, 5, 10, 15, 20, 25, 30]:
    per_fx = total_Gy / 5.0
    sched = DoseSchedule(
        name=f"{total_Gy} Gy / 5 fx",
        fractions=[(t, per_fx) for t in FX_TIMES_6],
    )
    dose_schemes.append(sched)

fig, ax = plt.subplots(figsize=(8, 5))
results_6 = {}
for s in dose_schemes:
    t, N = simulate(s, total_mcs=14000)
    ax.plot(t, N, label=s.name, linewidth=1.3)
    results_6[s.name] = {
        "N_at_14000": float(N[-1]),
        "N_at_1000": float(N[1000]),
        "kill_fraction": 1.0 - float(N[-1]) / float(N[1000]) if N[1000] > 0 else None,
    }
for ft in FX_TIMES_6:
    ax.axvline(ft, color="grey", alpha=0.25, linestyle=":")
ax.set_xlabel("MCS (≈ minutes)")
ax.set_ylabel("Proliferating tumor cells")
ax.set_title(
    "Surrogate of paper Fig. 6a: logistic + LQ\n"
    f"(α={ALPHA} Gy⁻¹, β={BETA} Gy⁻², r={R}/MCS, K={int(K)})"
)
ax.legend(fontsize=8, loc="best")
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(FIG / "fig_fractionation.png", dpi=140)
plt.close(fig)


# ---- 2) 40 Gy hyper vs hypo (Fig. 7a) -----------------------------------
# Hyper: 40 Gy in 5 fx at 12000,13000,14000,15000,16000
# Hypo:  40 Gy in 2 fx at 12000,16000
HYPER = DoseSchedule(
    name="40 Gy / 5 fx (hyper)",
    fractions=[(t, 8.0) for t in [12000, 13000, 14000, 15000, 16000]],
)
HYPO = DoseSchedule(
    name="40 Gy / 2 fx (hypo)",
    fractions=[(t, 20.0) for t in [12000, 16000]],
)
NOIRR = DoseSchedule(name="0 Gy (control)", fractions=[])

fig, ax = plt.subplots(figsize=(8, 5))
results_40 = {}
N_at_irradiation = None
N_at_end = {}
for s in [NOIRR, HYPER, HYPO]:
    t, N = simulate(s, total_mcs=17000)
    ax.plot(t, N, label=s.name, linewidth=1.4)
    N_at_end[s.name] = float(N[-1])
    if s.name.startswith("0"):
        results_40["control_at_12000"] = float(N[12000])
        N_at_irradiation = float(N[12000])
    results_40[s.name] = {
        "N_at_12000": float(N[12000]),
        "N_at_17000": float(N[-1]),
    }
ax.axvline(12000, color="red", alpha=0.4, linestyle=":")
ax.axvline(16000, color="red", alpha=0.4, linestyle=":")
ax.set_xlabel("MCS (≈ minutes)")
ax.set_ylabel("Proliferating tumor cells")
ax.set_title("Surrogate of paper Fig. 7a: 40 Gy hyper vs hypo fractionation")
ax.legend(fontsize=9)
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(FIG / "fig_40Gy_hyper_vs_hypo.png", dpi=140)
plt.close(fig)

# Compute the paper's "30.37% higher tumor cell loss" stat.
# Paper: hypofractionated leads to 30.37% higher loss vs hyperfractionated.
# Loss is reduction relative to the would-be-without-irradiation level.
N0_irr = results_40["control_at_12000"]
loss_hyper = N0_irr - results_40["40 Gy / 5 fx (hyper)"]["N_at_17000"]
loss_hypo = N0_irr - results_40["40 Gy / 2 fx (hypo)"]["N_at_17000"]
# Express the same way the paper writes the comparison.
pct_diff = (loss_hypo - loss_hyper) / loss_hyper * 100.0 if loss_hyper > 0 else None

results_40["loss_hyper_cells"] = loss_hyper
results_40["loss_hypo_cells"] = loss_hypo
results_40["hypo_minus_hyper_pct"] = pct_diff
results_40["paper_value_pct"] = 30.37

out = {
    "scheme_6Gy_sweep": results_6,
    "scheme_40Gy_hyper_vs_hypo": results_40,
    "model_params": {
        "alpha_inv_Gy": ALPHA,
        "beta_inv_Gy2": BETA,
        "r_per_MCS": R,
        "K_cells": K,
        "N0_cells": N0,
        "total_MCS": TOTAL_MCS,
    },
    "notes": [
        "Surrogate only; not CPM. Paper's 30.37% is from a CC3D-CPM run.",
        "Sign and order of magnitude of hyper/hypo comparison are the diagnostic.",
        "5 Gy/5fx exceeding control (Fig. 6a) is a CPM contact-inhibition effect "
        "and is NOT expected to reproduce in a pure logistic surrogate.",
    ],
}

(EVI / "surrogate_numbers.json").write_text(json.dumps(out, indent=2))

# Console summary
print("=== s100-033 surrogate summary ===")
print(f"Control at MCS=12000: {N0_irr:.1f} cells")
print(f"40Gy/5fx (hyper) final: {results_40['40 Gy / 5 fx (hyper)']['N_at_17000']:.2f} cells  (loss {loss_hyper:.2f})")
print(f"40Gy/2fx (hypo)  final: {results_40['40 Gy / 2 fx (hypo)']['N_at_17000']:.2f} cells  (loss {loss_hypo:.2f})")
print(f"Hypo-vs-hyper extra loss = {pct_diff:+.2f}%   (paper: +30.37%)")
print()
print("6-scheme sweep, final cell count at MCS=14000:")
for k, v in results_6.items():
    print(f"  {k:20s}  N(14000)={v['N_at_14000']:7.2f}  kill_fraction={v['kill_fraction']}")
print()
print(f"Figures: {FIG}")
print(f"Numbers: {EVI}/surrogate_numbers.json")
