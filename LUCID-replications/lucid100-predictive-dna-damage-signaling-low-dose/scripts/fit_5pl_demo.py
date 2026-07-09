#!/usr/bin/env python3
"""
5PL (five-parameter logistic, asymmetric sigmoidal) fitter smoke test.

Park et al. 2024 fit Fig 1B dose-response curves to an "asymmetrical sigmoidal,
five-parameter curve" (5PL):

    y(x) = D + (A - D) / (1 + (x / C) ** B) ** G

where A = lower asymptote, D = upper asymptote, B = Hill slope, C = inflection
EC50, G = asymmetry. We have no underlying data (paper deposits none and PMC
figure-image scrape is out of scope for first pass), so this smoke synthesises
a noisy ATM-like activation curve, fits it, and asserts parameter recovery.

Run:
    python3 scripts/fit_5pl_demo.py

Exit code: 0 = within tolerance; non-zero = fitter broken.
"""
from __future__ import annotations

import sys

import numpy as np
from scipy.optimize import curve_fit


def five_pl(x, A, B, C, D, G):
    # Guard against negative or zero x — replace zeros with small epsilon
    # to keep (x/C)**B finite.
    x = np.where(x <= 0, 1e-9, x)
    return D + (A - D) / (1.0 + (x / C) ** B) ** G


def main() -> int:
    rng = np.random.default_rng(seed=20260609)
    # Truth: lower=0.05, slope=1.4, EC50=0.4 Gy, upper=1.0, asymmetry=0.7
    true = dict(A=0.05, B=1.4, C=0.4, D=1.0, G=0.7)
    # Paper uses 12 dose points in 0..2 Gy
    x = np.linspace(0.01, 2.0, 12)
    y_true = five_pl(x, **true)
    y = y_true + rng.normal(0.0, 0.03, size=x.shape)

    p0 = [0.0, 1.0, 0.5, 1.0, 1.0]
    bounds = ([-0.5, 0.1, 1e-4, 0.0, 0.1], [1.0, 10.0, 5.0, 5.0, 10.0])
    popt, pcov = curve_fit(five_pl, x, y, p0=p0, bounds=bounds, maxfev=20000)
    perr = np.sqrt(np.diag(pcov))

    names = ["A", "B", "C", "D", "G"]
    print("5PL fit on synthetic ATM-like dose response (12 points, σ_noise=0.03):")
    for n, v, e in zip(names, popt, perr):
        print(f"  {n} = {v: .4f} ± {e:.4f}   (truth {true[n]:.4f})")

    ec50_err = abs(popt[2] - true["C"]) / true["C"]
    print(f"EC50 fractional error: {ec50_err:.3f}")
    assert ec50_err < 0.15, f"EC50 recovery off by {ec50_err:.2%}"
    print("PASS — 5PL fitter recovers EC50 within 15%.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
