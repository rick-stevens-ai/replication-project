"""
Refit TLK parameters to SF.csv + FAR.csv (HSGc-C5) using scipy.optimize.

This implements the same task the paper performed with Ceres Solver:
nonlinear least squares minimization of joint SF + relative FAR residuals.

beta1 is fixed to 0 (paper convention: simple DSBs don't kill).
Sigma1, Sigma2 are taken from the paper's Geant4-DNA simulation (Section 3.2).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import least_squares

from tlk_model import (
    sf_at_dose, far_curve, sigmas_for,
    SIGMA1_0MM, SIGMA1_32MM, SIGMA2_0MM, SIGMA2_32MM,
)

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "supplement"
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)


def _load():
    sf = pd.read_csv(DATA / "SF.csv", skipinitialspace=True)
    sf.columns = [c.strip() for c in sf.columns]
    sf["Cell"] = sf["Cell"].str.strip()
    sf = sf[sf["Cell"] == "HSG"].copy()
    sf["PMMA"] = sf["PMMAthick[mm]"].astype(int)
    sf["Dose"] = sf["Dose(Gy)"].astype(float)
    sf["SF"] = sf["SF"].astype(float)
    sf["StdDev"] = sf["StdDev"].astype(float).clip(lower=1e-4)
    sf = sf[sf["Dose"] > 0].reset_index(drop=True)

    far = pd.read_csv(DATA / "FAR.csv", skipinitialspace=True)
    far.columns = [c.strip() for c in far.columns]
    far["Cell"] = far["Cell"].str.strip()
    far = far[far["Cell"] == "HSG"].copy()
    far["PMMA"] = far["PMMAthick[mm]"].astype(int)
    far["Dose"] = far["Dose(Gy)"].astype(float)
    far["time"] = far["time(h)"].astype(float)
    far["FAR"] = far["FAR(%)"].astype(float)
    far = far.sort_values(["PMMA", "Dose", "time"]).reset_index(drop=True)
    return sf, far


def _unpack(x: np.ndarray) -> dict:
    # log-space for positive-only params lam1, lam2, eta
    lam1, lam2, log10_eta, beta2, gamma = x
    return dict(
        lam1=float(lam1),
        lam2=float(lam2),
        eta=float(10 ** log10_eta),
        beta1=0.0,
        beta2=float(beta2),
        gamma=float(gamma),
    )


def residuals(x: np.ndarray, sf: pd.DataFrame, far: pd.DataFrame,
              w_sf: float = 1.0, w_far: float = 1.0) -> np.ndarray:
    params = _unpack(x)

    sf_res = []
    for _, row in sf.iterrows():
        s1, s2 = sigmas_for(int(row["PMMA"]))
        pred = sf_at_dose(row["Dose"], params, s1, s2)
        # Compare in log10 space (SF spans 2 decades) weighted by relative error.
        if pred <= 0:
            pred = 1e-12
        sf_res.append(w_sf * (np.log10(pred) - np.log10(row["SF"])))

    far_res = []
    for (pmma, dose), grp in far.groupby(["PMMA", "Dose"]):
        s1, s2 = sigmas_for(int(pmma))
        times = grp["time"].to_numpy()
        meas = grp["FAR"].to_numpy()
        pred = far_curve(float(dose), params, s1, s2, times)
        far_res.extend(w_far * (pred - meas))

    return np.concatenate([np.asarray(sf_res), np.asarray(far_res)])


def main():
    sf, far = _load()
    print(f"SF rows: {len(sf)}   FAR rows: {len(far)}")

    # Initial guess: paper's Table 1
    x0 = np.array([3.36, 0.01, np.log10(4.58e-6), 2.75e-2, 0.39])
    bounds = (
        np.array([0.1,    1e-4, -10.0, 1e-4, 1e-3]),
        np.array([50.0,   5.0,   -2.0, 1.0,  1.0]),
    )

    res = least_squares(
        residuals, x0, args=(sf, far),
        bounds=bounds, method="trf", x_scale="jac",
        max_nfev=400, verbose=2,
    )
    fitted = _unpack(res.x)
    print("Fit success:", res.success, "  cost:", res.cost, "  nfev:", res.nfev)
    print("Fitted params:", json.dumps(fitted, indent=2))

    out = {
        "fitted_params": fitted,
        "paper_table1": dict(
            lam1=3.36, lam2=0.99e-2, eta=4.58e-6, beta1=0.0, beta2=2.75e-2, gamma=0.39,
        ),
        "fit_diagnostics": {
            "success": bool(res.success),
            "cost": float(res.cost),
            "nfev": int(res.nfev),
            "n_residuals": int(res.fun.size),
            "rmse_residual": float(np.sqrt(np.mean(res.fun ** 2))),
        },
        "sigmas_used": {
            "PMMA_0mm": {"Sigma1": SIGMA1_0MM, "Sigma2": SIGMA2_0MM},
            "PMMA_32mm": {"Sigma1": SIGMA1_32MM, "Sigma2": SIGMA2_32MM},
        },
    }
    (RESULTS / "refit.json").write_text(json.dumps(out, indent=2))
    print("Wrote results/refit.json")


if __name__ == "__main__":
    main()
