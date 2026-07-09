"""
Wang 2018 doesn't print the MCDS Y values they actually used as input.
Different MCDS calibrations are common in the literature (5.738 DSB/Gy/Gbp
McMahon 2017 vs ~1.4 DSB/Gy/Gbp older Stewart conventions).

Given the published Table 1 fit parameters and the published D10 = 4.08 Gy
(HSG) and 7.07 Gy (V79) for X-ray, we invert the model to find the Y that
Wang must have used.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.optimize import brentq
from wang2018_model import HSG_PARAMS, V79_PARAMS, cell_survival, cell_alpha_beta

def d10_from_Y(Y, cell):
    LAM = 1.0
    # n_p_perGy ≈ Y in the X-ray limit (lam->0 ⇒ np ≈ n·λ = YD/λ·λ = YD)
    D = np.linspace(0.01, 30.0, 4000)
    S = cell_survival(D, Y, LAM, Y, cell)
    lnS = np.log(S)
    return np.interp(np.log(0.1), lnS[::-1], D[::-1])

def solve_Y_for_D10(target_D10, cell):
    f = lambda Y: d10_from_Y(Y, cell) - target_D10
    return brentq(f, 0.5, 500.0)

print("Inverse-fit Y (X-ray) from paper-reported D10:")
for cell, D10 in [(HSG_PARAMS, 4.08), (V79_PARAMS, 7.07)]:
    Y = solve_Y_for_D10(D10, cell)
    a, b = cell_alpha_beta(Y, 1.0, cell)
    print(f"  {cell.name:>4}: D10={D10} Gy  =>  Y_X = {Y:7.3f} DSB/cell/Gy   "
          f"alpha={a:.4f}  beta={b:.5f}  alpha/beta={a/b:.2f} Gy")
print()
print("Compare to:")
print("  McMahon 2017 calibration: Y_X(HSG, 6 Gbp) = 5.738*6 = 34.43")
print("                            Y_X(V79, 5.6 Gbp) = 5.738*5.6 = 32.13")
print("  Stewart MCDS (older):     Y_X ~ 8-10 DSB/cell/Gy for 6 Gbp")
print()
print("Wang 2018's published Furusawa-fit reference alpha values for X-ray:")
print("  HSG: alpha_X ≈ 0.31 Gy^-1, beta_X ≈ 0.063 Gy^-2  -> alpha/beta ≈ 4.9 Gy")
print("  V79: alpha_X ≈ 0.13 Gy^-1, beta_X ≈ 0.052 Gy^-2  -> alpha/beta ≈ 2.5 Gy")
print("  (These come from many Furusawa LQ fits; SF=0.1 gives D ~ 4.08 / 7.07 Gy.)")
