#!/usr/bin/env python3
"""
LET-dependent extension audit for Friedland, Kundrat & Jacob (2012).

The 2012 paper's central qualitative claim is that with ONE parameter set
(NHEJ rate constants + labile-site amplitude + complex-DSB processing
capacity), increasing LET should:

  (i)  increase the slow-component fraction (more complex DSB),
  (ii) increase the long-term residual unrejoined fraction (24 h),
  (iii) push the effective slow-component half-time upward (saturation
        of complex-lesion processing capacity).

We cannot run PARTRAC (proprietary, Helmholtz). We instead drive the same
two-component+labile-site analytical model from smoke_friedland2012.py with
a Hill-style LET sweep on the *complex-DSB fraction* f_c:

    f_c(LET) = f_c_max * LET^h / (K^h + LET^h)

then:
  - f (fast frac)      = 1 - f_c(LET)
  - k_slow_eff         = k_slow_base * (1 - f_c(LET))   # capacity saturation
  - A_labile           = A0 + alpha * f_c(LET)

and we check that as LET ranges from 0.3 keV/um (~Co-60 gamma) to ~150
keV/um (Fe-ion regime), the qualitative ordering (i)-(iii) is monotone.

This is NOT a quantitative reproduction of any specific PARTRAC table or
figure. It is a behavioural audit: does the analytical skeleton support
the LET trends the paper claims?
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "results"
FIG = ROOT / "figures"
OUT.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)


def model(t, f, k_f, k_s, A_lab, k_lab):
    base = (1.0 - A_lab) * (f * np.exp(-k_f * t) + (1.0 - f) * np.exp(-k_s * t))
    labile = A_lab * (1.0 - np.exp(-k_lab * t)) * np.exp(-k_s * t)
    return base + labile


def complex_frac(LET, fc_max=0.55, K=40.0, h=1.6):
    """Hill-type rise of complex-DSB fraction with LET (keV/um)."""
    return fc_max * (LET**h) / (K**h + LET**h)


def main():
    LETs = np.array([0.3, 1.0, 3.0, 10.0, 30.0, 60.0, 100.0, 150.0])  # keV/um
    # base low-LET rates: take Co60 fit from the smoke run
    k_fast = 0.0364   # 1/min  (t1/2 ~19 min)
    k_slow_base = 0.00174  # 1/min (t1/2 ~ 6.6 h)
    A0 = 0.017
    alpha = 0.10
    k_lab = 0.05

    t = np.array([0, 15, 30, 60, 120, 240, 480, 1440.0])

    rows = []
    for L in LETs:
        fc = complex_frac(L)
        f_fast = 1.0 - fc
        k_slow_eff = k_slow_base * (1.0 - 0.85 * fc)  # capacity saturation
        A_lab = min(0.3, A0 + alpha * fc)
        F = model(t, f_fast, k_fast, k_slow_eff, A_lab, k_lab)
        rows.append({
            "LET_keV_per_um": float(L),
            "f_complex": float(fc),
            "f_fast": float(f_fast),
            "k_slow_eff_per_min": float(k_slow_eff),
            "t_half_slow_min": float(math.log(2) / k_slow_eff),
            "A_labile": float(A_lab),
            "F_at_t_min": {float(ti): float(Fi) for ti, Fi in zip(t, F)},
            "residual_24h": float(F[-1]),
        })

    # Tests of the paper's qualitative claims
    slow_fracs = [r["f_complex"] for r in rows]
    residuals = [r["residual_24h"] for r in rows]
    t_half_slow = [r["t_half_slow_min"] for r in rows]

    def monotone_nondecreasing(xs, tol=1e-9):
        return all(b - a >= -tol for a, b in zip(xs, xs[1:]))

    checks = {
        "T1_complex_fraction_monotone_in_LET": monotone_nondecreasing(slow_fracs),
        "T2_residual24h_monotone_in_LET":      monotone_nondecreasing(residuals),
        "T3_slow_halftime_monotone_in_LET":    monotone_nondecreasing(t_half_slow),
        "T4_low_LET_residual_lt_5pct":         residuals[0] < 0.05,
        "T5_high_LET_residual_gt_15pct":       residuals[-1] > 0.15,
        "T6_high_LET_slow_halftime_gt_3x_low": t_half_slow[-1] > 3.0 * t_half_slow[0],
    }
    n_pass = sum(checks.values())

    out = {
        "paper": "Friedland Kundrat Jacob 2012",
        "doi": "10.3109/09553002.2011.611404",
        "model": "analytical two-component + labile + Hill(LET) on f_complex and k_slow capacity",
        "params": {
            "k_fast_per_min": k_fast,
            "k_slow_base_per_min": k_slow_base,
            "A0": A0,
            "alpha": alpha,
            "k_labile_per_min": k_lab,
            "fc_max": 0.55, "K_keV_per_um": 40.0, "Hill_h": 1.6,
        },
        "rows": rows,
        "checks": {k: bool(v) for k, v in checks.items()},
        "verdict": f"{n_pass}/{len(checks)} LET-trend checks pass",
        "status": "PASS" if n_pass == len(checks) else "PARTIAL",
        "notes": [
            "Hill parameters (fc_max, K, h) are NOT extracted from the closed paper.",
            "They are smoke values chosen to span the LET regime in published high-LET tables.",
            "This audit verifies the analytical scaffold supports the paper's LET trends, not the absolute numbers.",
        ],
    }

    out_path = OUT / "let_sweep_results.json"
    out_path.write_text(json.dumps(out, indent=2))

    # Plot
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
        ax[0].plot(LETs, [r["f_complex"] for r in rows], "o-", label="complex DSB frac")
        ax[0].plot(LETs, [r["residual_24h"] for r in rows], "s-", label="24-h residual")
        ax[0].set_xscale("log")
        ax[0].set_xlabel("LET (keV/um)")
        ax[0].set_ylabel("fraction")
        ax[0].legend(); ax[0].grid(True, alpha=0.3)
        ax[0].set_title("LET-dependence of complex DSB & residual")

        ax[1].plot(LETs, [r["t_half_slow_min"] for r in rows], "d-", color="tab:purple")
        ax[1].set_xscale("log"); ax[1].set_yscale("log")
        ax[1].set_xlabel("LET (keV/um)")
        ax[1].set_ylabel("effective slow t1/2 (min)")
        ax[1].grid(True, alpha=0.3, which="both")
        ax[1].set_title("Slow-component half-time (capacity saturation)")
        fig.tight_layout()
        fig.savefig(FIG / "let_sweep.png", dpi=140)
        plt.close(fig)
    except Exception as e:
        out["figure_error"] = repr(e)
        out_path.write_text(json.dumps(out, indent=2))

    print(json.dumps(out, indent=2))
    return 0 if out["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
