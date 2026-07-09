"""
Test the headline quantitative claims of Wang et al. 2018 using the model
implementation and the paper's own Table 1 fit parameters.

Headline numbers from the paper we want to reproduce:

  (A) X-ray survival curves for HSG and V79 — R^2 = 0.9991 (HSG), 0.9986 (V79)
      and SF=10% doses:  D10(HSG, X-ray) = 4.08 Gy,  D10(V79, X-ray) = 7.07 Gy.

  (B) alpha/beta trend with LET — alpha/beta in low-LET limit.

  (C) For X-ray, model collapses to LQ-like form (since np small, lam_p->1).

Inputs needed:
  Y for X-ray.  Wang 2018 uses MCDS-derived Y. Canonical published low-LET
  DSB yield (McMahon 2017 / Stewart 2011) is 5.738 DSB/Gy/Gbp.
  HSG nucleus DNA content = 6.0   Gbp -> Y_X(HSG) = 34.43 DSB/cell/Gy
  V79 nucleus DNA content = 5.6   Gbp -> Y_X(V79) = 32.13 DSB/cell/Gy
  lam_p(X-ray) -> 1  (paper's limit)
  n_p_perGy(X-ray) -> Y         (from eqs 5,6 with lam->0)
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from wang2018_model import (
    HSG_PARAMS, V79_PARAMS,
    cell_survival, cell_alpha_beta,
    survival, alpha_beta, eta_of_lambda_p,
)

# ------------- low-LET (X-ray) inputs from MCDS canonical literature ----------
DSB_PER_GY_PER_GBP = 5.738            # McMahon 2017 Sci Rep Table 1
HSG_GBP = 6.0                          # paper: human DNA content 6 Gbp
V79_GBP = 5.6                          # paper: hamster DNA content 5.6 Gbp

Y_X_HSG = DSB_PER_GY_PER_GBP * HSG_GBP    # ~34.43
Y_X_V79 = DSB_PER_GY_PER_GBP * V79_GBP    # ~32.13

LAM_P_XRAY = 1.0
NP_PER_GY_XRAY_HSG = Y_X_HSG / LAM_P_XRAY
NP_PER_GY_XRAY_V79 = Y_X_V79 / LAM_P_XRAY


def d10_from_curve(D, S):
    """Find dose at SF=0.1 by linear interp on log(S)."""
    lnS = np.log(S)
    target = np.log(0.1)
    # find bracketing pair
    idx = np.where(np.diff(np.sign(lnS - target)) != 0)[0]
    if len(idx) == 0:
        return np.nan
    i = idx[0]
    x1, x2 = D[i], D[i+1]
    y1, y2 = lnS[i], lnS[i+1]
    return x1 + (target - y1) * (x2 - x1) / (y2 - y1)


def main():
    D = np.linspace(0.01, 15.0, 1500)

    print("="*72)
    print("Wang et al. 2018 headline claim verification")
    print("="*72)

    # ---------------- (A) X-ray survival curves ---------------------------
    print("\n[A] X-ray survival (low-LET limit: lam_p -> 1, n_p/D = Y)")
    for cell, Y_x, np_x in [(HSG_PARAMS, Y_X_HSG, NP_PER_GY_XRAY_HSG),
                             (V79_PARAMS, Y_X_V79, NP_PER_GY_XRAY_V79)]:
        S = cell_survival(D, Y_x, LAM_P_XRAY, np_x, cell)
        d10 = d10_from_curve(D, S)
        a, b = cell_alpha_beta(Y_x, LAM_P_XRAY, cell)
        ab = a / b if b else np.inf
        # SF2 for X-ray (commonly reported)
        S2 = cell_survival(np.array([2.0]), Y_x, LAM_P_XRAY, np_x, cell)[0]
        print(f"  {cell.name:>4}  Y_X={Y_x:6.2f}  alpha={a:7.4f} Gy^-1  "
              f"beta={b:8.5f} Gy^-2  alpha/beta={ab:6.2f} Gy  "
              f"D10={d10:5.2f} Gy  SF2={S2:6.4f}")

    print("\n  Paper claims (Results, 'Biological parameters of different cell types'):")
    print("    D10(HSG, X-ray) = 4.08 Gy   (from experimental survival curve)")
    print("    D10(V79, X-ray) = 7.07 Gy   (from experimental survival curve)")

    # ---------------- (B) low-LET LQ alpha,beta values --------------------
    print("\n[B] Low-LET (lam_p->1) closed-form alpha,beta from eqs (18,19)")
    print("    These should match Wang's Fig 2c,d fit alpha/beta for X-ray.")
    for cell, Y_x in [(HSG_PARAMS, Y_X_HSG), (V79_PARAMS, Y_X_V79)]:
        a, b = cell_alpha_beta(Y_x, LAM_P_XRAY, cell)
        print(f"  {cell.name:>4}: alpha={a:.4f} Gy^-1   beta={b:.5f} Gy^-2   "
              f"alpha/beta={a/b:.2f} Gy")

    # ---------------- (C) High-LET behaviour (eta limit) ------------------
    print("\n[C] eta(lam_p) limits — paper eq (8)")
    for cell in [HSG_PARAMS, V79_PARAMS]:
        e1  = eta_of_lambda_p(1.0,  cell.eta_lp_to_1, cell.eta_lp_to_inf)
        einf= eta_of_lambda_p(1e6,  cell.eta_lp_to_1, cell.eta_lp_to_inf)
        print(f"  {cell.name:>4}: eta(lam_p=1)   = {e1:.4e}   "
              f"(Table 1: {cell.eta_lp_to_1:.4e})")
        print(f"        eta(lam_p=inf) = {einf:.4e}   "
              f"(Table 1: {cell.eta_lp_to_inf:.4e})")

    # ---------------- (D) alpha/beta increases with LET -------------------
    print("\n[D] alpha/beta vs lam_p  (paper claim: alpha/beta increases with LET)")
    print("    HSG cell:")
    for lp in [1.0, 2.0, 5.0, 10.0, 20.0, 50.0]:
        # at high LET, Y also increases — but we test analytic alpha/beta(Y, lam_p)
        # using a flat Y for clarity:
        a, b = cell_alpha_beta(35.0, lp, HSG_PARAMS)
        print(f"      lam_p={lp:5.1f}  alpha={a:6.3f}  beta={b:8.5f}  "
              f"alpha/beta={a/b:7.2f} Gy")

    # ---------------- (E) Overkill / clustering at high LET ---------------
    print("\n[E] Verify clustering / overkill convergence with lam_p")
    from wang2018_model import P_track, P_contribution
    for lp in [0.5, 1.0, 5.0, 20.0, 100.0]:
        pt = P_track(lp, HSG_PARAMS.xi)
        pc = P_contribution(lp, HSG_PARAMS.zeta)
        print(f"      lam_p={lp:6.1f}  P_track={pt:.4f}  P_contribution={pc:.4f}")

    print("\n" + "="*72)


if __name__ == "__main__":
    main()
