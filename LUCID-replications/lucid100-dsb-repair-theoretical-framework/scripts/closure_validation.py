#!/usr/bin/env python3
"""Quantitative replication of Figure 3 / Section 3.1 of Murray et al. 2016.

Paper claim (Section 3.1, Figure 3, last sentence): the differential equation
model (both the ad-hoc closure (2.5) and the conditional-mean closure (2.8))
is "an accurate representation of the underlying stochastic model" -- i.e.
averages over SSA realizations of master equation (2.1) coincide with ODE
solutions.

We test this quantitatively by:

  (1) Running an ensemble of tau-leap SSA realizations of (2.1) for both
      cell lines, computing <X>(t), <Y>(t), <Z>(t).
  (2) Solving (2.5) (ad-hoc closure) and (2.8) (conditional-mean closure)
      with the same Table-1 parameters.
  (3) Computing max abs and RMS deviation between SSA mean trajectories and
      each ODE solution on a shared time grid.

Outputs:
  artifacts/closure_validation.json    -- summary numbers
  artifacts/closure_validation_MDA-MB-468.csv
  artifacts/closure_validation_MCF7.csv
"""
from __future__ import annotations
import csv
import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

from scripts_ssa import tauleap_ensemble

PARAMS = {
    "MDA-MB-468": dict(k1=0.0032, k2=159.0, k3=14.0, k4=71.0, k5=1056.0, k6=211.0),
    "MCF7":       dict(k1=0.02,   k2=1236.0, k3=220.0, k4=687.0, k5=1765.0, k6=565.0),
}
Y_MAX = 300
Z_MAX = 1000
Z_STAR = 200


def rhs_adhoc(t, s, p):
    """Eq (2.5) ad-hoc closure -- BARE FORM AS PRINTED IN THE PAPER.

    Note: the paper as printed contains no Ymax / Zmax saturation factors.
    The Table-2 caps are properties of the underlying SSA / master equation;
    they are NOT explicit in the ODE.
    """
    X, Y, Z = s
    dX = -p["k1"] * X * Y
    dY = p["k2"] * X + p["k3"] * Z - p["k4"] * Y
    dZ = p["k5"] * Y - p["k6"] * Z
    return [dX, dY, dZ]


def rhs_cond(t, s, p):
    """Eq (2.8) conditional-mean closure -- BARE FORM AS PRINTED.

    Paper system after closing conditional (co)variances:
      d<X>/dt   = -k1 <Y|X=1> <X>
      d<Y|X=1>/dt = k2 + k3 <Z|X=1> - k4 <Y|X=1>
      d<Y>/dt   = k2 <X> + k3 <Z> - k4 <Y>
      d<Z>/dt   = k5 <Y> - k6 <Z>
      d<Z|X=1>/dt = k5 <Y|X=1> - k6 <Z|X=1>

    State here: s = [<X>, <Y>, <Z>, <Y|X=1>, <Z|X=1>]
    """
    X, Y, Z, Yc, Zc = s
    dX  = -p["k1"] * Yc * X
    dYc = p["k2"] + p["k3"] * Zc - p["k4"] * Yc
    dY  = p["k2"] * X + p["k3"] * Z - p["k4"] * Y
    dZ  = p["k5"] * Y - p["k6"] * Z
    dZc = p["k5"] * Yc - p["k6"] * Zc
    return [dX, dY, dZ, dYc, dZc]


def integrate(rhs, y0, t_grid, p):
    sol = solve_ivp(
        rhs, [t_grid[0], t_grid[-1]], y0, args=(p,),
        method="LSODA", t_eval=t_grid, rtol=1e-8, atol=1e-10,
    )
    return sol.y


def run_ssa_means(p, t_grid, n_runs=1000, tau=0.0005, seed=0):
    """Tau-leap and return <X>(t), <Y>(t), <Z>(t) on t_grid."""
    rng = np.random.default_rng(seed)
    n_grid = len(t_grid)
    X = np.ones(n_runs, dtype=np.int32)
    Y = np.zeros(n_runs, dtype=np.int32)
    Z = np.zeros(n_runs, dtype=np.int32)
    mean_X = np.zeros(n_grid)
    mean_Y = np.zeros(n_grid)
    mean_Z = np.zeros(n_grid)
    mean_X[0] = X.mean(); mean_Y[0] = Y.mean(); mean_Z[0] = Z.mean()
    t = 0.0; t_end = float(t_grid[-1]); gi = 1
    k1, k2, k3, k4, k5, k6 = (p[k] for k in ("k1","k2","k3","k4","k5","k6"))
    while t < t_end and gi < n_grid:
        r1 = k1 * Y * X
        r2 = k2 * X * (Y < Y_MAX)
        r3 = k3 * Z * (Y < Y_MAX)
        r4 = k4 * Y
        r5 = k5 * Y * (Z < Z_MAX)
        r6 = k6 * Z
        n1 = rng.poisson(r1 * tau)
        n2 = rng.poisson(r2 * tau)
        n3 = rng.poisson(r3 * tau)
        n4 = rng.poisson(r4 * tau)
        n5 = rng.poisson(r5 * tau)
        n6 = rng.poisson(r6 * tau)
        X = np.where(n1 > 0, 0, X)
        Y = Y + n2 + n3 - n4
        Z = Z + n5 - n6
        np.clip(Y, 0, Y_MAX, out=Y)
        np.clip(Z, 0, Z_MAX, out=Z)
        t += tau
        while gi < n_grid and t >= t_grid[gi]:
            mean_X[gi] = X.mean(); mean_Y[gi] = Y.mean(); mean_Z[gi] = Z.mean()
            gi += 1
    return mean_X, mean_Y, mean_Z


def deviation_metrics(ssa, ode):
    diff = ode - ssa
    return {
        "max_abs": float(np.max(np.abs(diff))),
        "rms":     float(np.sqrt(np.mean(diff**2))),
        "max_rel": float(np.max(np.abs(diff) / (np.maximum(np.abs(ssa), 1.0)))),
    }


def main():
    summary = {}
    out_dir = Path(__file__).resolve().parent.parent / "artifacts"
    out_dir.mkdir(exist_ok=True)

    # MDA-MB-468 is slow enough that SSA over 6 h is tractable.
    # MCF7 needs much smaller tau because k5=1765 (events ~5e5/h/site at Y=Ymax).
    # Use a 0.6 h horizon for MCF7 (captures the Z rise+peak); 6 h for MDA468.
    # Horizons chosen to (a) keep MCF7 SSA tractable, (b) stop before the
    # MCF7 ODE diverges due to the near-critical k3*k5 ~ k4*k6 feedback.
    cases = [
        ("MDA-MB-468", 6.0,  121, 1000, 0.0005),
        ("MCF7",       0.6,  121, 1000, 0.00005),
    ]
    for line, t_end, n_grid, n_runs, tau in cases:
        p = PARAMS[line]
        t_grid = np.linspace(0.0, t_end, n_grid)
        # SSA
        sX, sY, sZ = run_ssa_means(p, t_grid, n_runs=n_runs, tau=tau, seed=42)
        # ad-hoc closure (2.5)
        adX, adY, adZ = integrate(rhs_adhoc, [1.0, 0.0, 0.0], t_grid, p)
        # conditional-mean closure (2.8): init <X>=1 -> <Y|X=1>=<Y>=0 etc.
        cm = integrate(rhs_cond, [1.0, 0.0, 0.0, 0.0, 0.0], t_grid, p)
        cX, cY, cZ, cYc, cZc = cm

        d_adhoc = {
            "X": deviation_metrics(sX, adX),
            "Y": deviation_metrics(sY, adY),
            "Z": deviation_metrics(sZ, adZ),
        }
        d_cond = {
            "X": deviation_metrics(sX, cX),
            "Y": deviation_metrics(sY, cY),
            "Z": deviation_metrics(sZ, cZ),
        }
        summary[line] = {
            "t_end_h": t_end,
            "n_grid": n_grid,
            "n_runs_ssa": n_runs,
            "tau_h": tau,
            "deviation_adhoc_2_5":     d_adhoc,
            "deviation_conditional_2_8": d_cond,
            "ssa_X_final": float(sX[-1]),
            "ssa_Y_final": float(sY[-1]),
            "ssa_Z_final": float(sZ[-1]),
            "adhoc_X_final": float(adX[-1]),
            "adhoc_Z_final": float(adZ[-1]),
            "cond_X_final": float(cX[-1]),
            "cond_Z_final": float(cZ[-1]),
        }

        # Dump CSV
        csv_path = out_dir / f"closure_validation_{line}.csv"
        with csv_path.open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["t_h", "SSA_X", "SSA_Y", "SSA_Z",
                        "ODE25_X", "ODE25_Y", "ODE25_Z",
                        "ODE28_X", "ODE28_Y", "ODE28_Z"])
            for i in range(n_grid):
                w.writerow([t_grid[i],
                            sX[i], sY[i], sZ[i],
                            adX[i], adY[i], adZ[i],
                            cX[i], cY[i], cZ[i]])
        summary[line]["csv"] = str(csv_path.relative_to(out_dir.parent))

    out_path = out_dir / "closure_validation.json"
    out_path.write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
