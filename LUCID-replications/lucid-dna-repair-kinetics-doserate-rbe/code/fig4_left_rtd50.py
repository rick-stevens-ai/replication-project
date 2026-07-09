"""
Reproduce Figure 4 LEFT panel and Table 3 R_TD50 column from Liew et al. 2022.

Strategy (fast, no nested bisection):

  We want R_TD50(rate) := D_eff(D_ref_rate=3.75) / D_eff(rate)  at fixed
  surviving fraction S* (effect level).

  Since R_TD50 ~ 1 within ~6%, we use a one-point + Taylor approximation
  per dose-rate:
    1) Compute S(D0, rate)  with D0 = reference TD50 (20 Gy single fr,
       12 Gy per-fraction for 2 Fr).
    2) Compute S(D0+dD, rate) with dD = 1 Gy.
    3) Estimate the local sensitivity  k(rate) := -d ln S / d D  evaluated
       at D0.  Then D_eff(S*; rate) = D0 + (ln S(D0,rate) - ln S*) / k(rate).
       This is exact for an LQ curve when D0 is close to D_eff, and the
       approximation error is O((D_eff-D0)^2 * d^2 lnS/dD^2).
    4) R_TD50 = D_eff(S*; 3.75) / D_eff(S*; rate).

  S* is set so that D_eff(S*; 3.75 Gy/min) == 20 Gy (1Fr) or 12 Gy (2Fr).
  In practice we take S* := S(20, 3.75) directly: then D_eff(S*; 3.75) = 20
  by construction and R_TD50 = 20 / D_eff(S*; rate).
"""

import os
import sys
import json
import time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from universe_photon import (
    RSC_REPAIR, survival_photon
)

OUT_DIR = os.path.abspath(os.path.join(HERE, "..", "results"))
os.makedirs(OUT_DIR, exist_ok=True)

# Reference dose rate
DREF = 3.75   # Gy/min

# Effect-level doses
D0_1FR = 20.0     # Gy (Karger 2003: TD50 single fraction RSC photon ~20 Gy)
D0_2FR = 12.0     # Gy (TD50 per fraction two-fraction ~12 Gy)

N_ITER = 600      # per call; ~5s on this machine

def loc_eff(D0, rate, dD=1.0, n_iter=N_ITER, rng_seed=2026):
    """
    Return (S(D0,rate), k) where k = -d ln S / d D evaluated near D0.
    Uses a finite difference on log-survival between D0 and D0+dD.
    """
    rng1 = np.random.default_rng(rng_seed)
    rng2 = np.random.default_rng(rng_seed + 1)
    s0 = survival_photon(D0,      rate, RSC_REPAIR, n_iter=n_iter, rng=rng1)
    s1 = survival_photon(D0 + dD, rate, RSC_REPAIR, n_iter=n_iter, rng=rng2)
    # protect against log(0)
    s0 = max(s0, 1e-6)
    s1 = max(s1, 1e-6)
    k = -(np.log(s1) - np.log(s0)) / dD
    return s0, k


def deff_for_S(S_star, S0, k, D0):
    """Solve  S* = S0 * exp(-k*(D-D0))  for D."""
    return D0 + (np.log(S0) - np.log(S_star)) / k


# ---------------- 1-fraction set ----------------
print("=== 1-fraction (D_ref=20 Gy at 3.75 Gy/min) ===", flush=True)
t = time.time()
S0_ref_1Fr, k_ref_1Fr = loc_eff(D0_1FR, DREF, n_iter=2000)
print(f"  S(20, 3.75) = {S0_ref_1Fr:.4f}   local k = {k_ref_1Fr:.4f} /Gy   "
      f"({time.time()-t:.1f}s)", flush=True)
S_STAR_1FR = S0_ref_1Fr   # by construction this fixes D_eff(S*, 3.75)=20

# ---------------- 2-fraction set ----------------
print("\n=== 2-fractions (D_ref=12 Gy/fr at 3.75 Gy/min) ===", flush=True)
t = time.time()
S0_ref_2Fr, k_ref_2Fr = loc_eff(D0_2FR, DREF, n_iter=2000)
print(f"  S(12, 3.75) = {S0_ref_2Fr:.4f}   local k = {k_ref_2Fr:.4f} /Gy   "
      f"({time.time()-t:.1f}s)", flush=True)
S_STAR_2FR = S0_ref_2Fr

# ---------------- Compute D_eff and R_TD50 over the rate grid ---------
GRID = [3.75, 6, 7, 8, 9, 10, 11, 14, 18, 31, 41, 42, 53, 100.0]

def compute_curve(S_star, D_ref_eff, D0, label):
    print(f"\n--- {label} (S* = {S_star:.4f}, D_ref_eff = {D_ref_eff:.2f} Gy) ---", flush=True)
    rows = []
    for r in GRID:
        t = time.time()
        s_r, k_r = loc_eff(D0, r, n_iter=N_ITER, rng_seed=4242 + int(r * 100))
        D_eff_r = deff_for_S(S_star, s_r, k_r, D0)
        R = D_ref_eff / D_eff_r
        rows.append({"dose_rate_Gy_per_min": float(r),
                     "S_at_D0": float(s_r),
                     "k_per_Gy": float(k_r),
                     "D_eff_at_S_star_Gy": float(D_eff_r),
                     "R_TD50": float(R)})
        print(f"  rate={r:>6.2f}  S(D0,rate)={s_r:.4f}  k={k_r:.4f}/Gy  "
              f"D_eff={D_eff_r:6.3f} Gy  R_TD50={R:6.4f}  ({time.time()-t:.1f}s)",
              flush=True)
    return rows

D_ref_eff_1Fr = D0_1FR
D_ref_eff_2Fr = D0_2FR
rows_1Fr = compute_curve(S_STAR_1FR, D_ref_eff_1Fr, D0_1FR, "1-fraction R_TD50 curve")
rows_2Fr = compute_curve(S_STAR_2FR, D_ref_eff_2Fr, D0_2FR, "2-fraction R_TD50 curve")

# ---------------- Compare with paper Table 3 ----------------
paper_table3 = {
    "1Fr_proton":  {11: 1.042, 18: 1.051, 42: 1.059, 53: 1.061},
    "2Fr_proton":  {8: 1.022, 14: 1.031, 31: 1.038, 41: 1.040},
    "1Fr_helium":  {11: 1.042, 10: 1.041, 9: 1.036},
    "2Fr_helium":  {8: 1.022, 7: 1.018, 6: 1.015},
}

def compare(rows, paper_subset, label):
    print(f"\n=== Comparison vs paper Table 3: {label} ===", flush=True)
    diffs = []
    for rate, R_paper in paper_subset.items():
        r_match = next((row for row in rows
                        if abs(row["dose_rate_Gy_per_min"] - rate) < 1e-6), None)
        if r_match is None:
            print(f"  rate={rate}: NO MATCH IN OUR GRID", flush=True)
            continue
        R_ours = r_match["R_TD50"]
        rel = (R_ours - R_paper) / R_paper * 100
        diffs.append(rel)
        print(f"  rate={rate:>3d}  paper R_TD50={R_paper:.3f}   "
              f"ours={R_ours:.4f}   rel.diff={rel:+.2f}%", flush=True)
    mad = float(np.mean(np.abs(diffs))) if diffs else float("nan")
    print(f"  MAD vs paper: {mad:.2f}%", flush=True)
    return mad

comparisons = {}
comparisons["1Fr_proton_rates"] = compare(rows_1Fr, paper_table3["1Fr_proton"], "1Fr proton rates")
comparisons["2Fr_proton_rates"] = compare(rows_2Fr, paper_table3["2Fr_proton"], "2Fr proton rates")
comparisons["1Fr_helium_rates"] = compare(rows_1Fr, paper_table3["1Fr_helium"], "1Fr helium rates")
comparisons["2Fr_helium_rates"] = compare(rows_2Fr, paper_table3["2Fr_helium"], "2Fr helium rates")

results = {
    "params": {
        "K_iDSB": RSC_REPAIR.K_iDSB,
        "K_cDSB": RSC_REPAIR.K_cDSB,
        "T_iDSB_half_min": RSC_REPAIR.T_iDSB_half,
        "T_cDSB_half_min": RSC_REPAIR.T_cDSB_half,
        "alpha_DSB": 30.0,
        "n_domains": RSC_REPAIR.n_domains,
        "n_steps": 100,
        "D_ref_dose_rate_Gy_per_min": DREF,
        "n_iter_per_call": N_ITER,
    },
    "calibration": {
        "S_star_1Fr": S_STAR_1FR,
        "S_star_2Fr": S_STAR_2FR,
        "k_ref_1Fr_per_Gy": k_ref_1Fr,
        "k_ref_2Fr_per_Gy": k_ref_2Fr,
    },
    "rows_1Fr": rows_1Fr,
    "rows_2Fr": rows_2Fr,
    "paper_table3": paper_table3,
    "comparisons_MAD_percent": comparisons,
}

with open(os.path.join(OUT_DIR, "rtd50_results.json"), "w") as f:
    json.dump(results, f, indent=2)
print(f"\nWrote {OUT_DIR}/rtd50_results.json", flush=True)
