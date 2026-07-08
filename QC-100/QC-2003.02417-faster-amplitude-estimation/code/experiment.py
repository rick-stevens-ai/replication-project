"""Main replication experiment for Nakaji 2020 (arXiv:2003.02417).

For each amplitude a in {0.1, 0.2, 0.3, 0.4}:
  - Run FAE for a range of ell values, many trials each.
  - Run MLAE for a range of M values, many trials each.
For each (algorithm, a, ell/M), record:
  - median Norac (varies mildly for FAE because j0 can vary run-to-run)
  - 95th-percentile amplitude error epsilon_95 (matches paper's methodology in Sec 3)

Then fit log10(Norac) = -log10(eps) + b  (i.e. Norac = 10^b / eps  = C/eps)
and report the fitted prefactor C = 10^b for each algorithm and each a.

Paper's central claim (C1): FAE achieves near-Heisenberg scaling (slope 1 in that log-log fit)
with a SMALLER prefactor C than MLAE (which is [13] in the paper's refs).

Outputs JSON+CSV to report/evidence/.
"""

from __future__ import annotations

import csv
import json
import math
import os
import sys
import time
from typing import Dict, List, Tuple

import numpy as np

# Ensure local imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fae import run_fae
from mlae import run_mlae


EVIDENCE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "report", "evidence"))
os.makedirs(EVIDENCE_DIR, exist_ok=True)


def pct95(vals: List[float]) -> float:
    return float(np.percentile(vals, 95))


def run_fae_sweep(a: float, ell_values: List[int], n_trials: int, delta_c: float = 0.01,
                  base_seed: int = 1000) -> List[Dict]:
    rows = []
    for ell in ell_values:
        errs, noracs, j0s, second_stages = [], [], [], []
        for t in range(n_trials):
            seed = base_seed + hash((a, ell, t)) % (2 ** 31)
            r = run_fae(a, ell, delta_c=delta_c, seed=seed)
            errs.append(r.a_error)
            noracs.append(r.norac)
            j0s.append(r.j0)
            second_stages.append(int(r.reached_second_stage))
        row = dict(
            algo="FAE",
            a=a,
            ell=ell,
            n_trials=n_trials,
            eps_p95=pct95(errs),
            eps_median=float(np.median(errs)),
            eps_mean=float(np.mean(errs)),
            eps_max=float(np.max(errs)),
            norac_median=float(np.median(noracs)),
            norac_mean=float(np.mean(noracs)),
            j0_mode=int(np.bincount(j0s).argmax()),
            fraction_second_stage=float(np.mean(second_stages)),
        )
        rows.append(row)
        print(f"  FAE  a={a} ell={ell}  eps_p95={row['eps_p95']:.4e}  "
              f"Norac_med={row['norac_median']:.3e}  frac2nd={row['fraction_second_stage']:.2f}")
    return rows


def run_mlae_sweep(a: float, M_values: List[int], n_trials: int, N_shot: int = 100,
                   base_seed: int = 2000) -> List[Dict]:
    rows = []
    for M in M_values:
        errs, noracs = [], []
        for t in range(n_trials):
            seed = base_seed + hash((a, M, t)) % (2 ** 31)
            r = run_mlae(a, M, N_shot=N_shot, seed=seed)
            errs.append(r.a_error)
            noracs.append(r.norac)
        row = dict(
            algo="MLAE",
            a=a,
            M=M,
            N_shot=N_shot,
            n_trials=n_trials,
            eps_p95=pct95(errs),
            eps_median=float(np.median(errs)),
            eps_mean=float(np.mean(errs)),
            eps_max=float(np.max(errs)),
            norac_median=float(np.median(noracs)),
            norac_mean=float(np.mean(noracs)),
        )
        rows.append(row)
        print(f"  MLAE a={a} M={M}  eps_p95={row['eps_p95']:.4e}  Norac={row['norac_median']:.3e}")
    return rows


def fit_prefactor(rows: List[Dict]) -> Tuple[float, float, float]:
    """Fit log10(Norac) = -slope * log10(eps) + b. Return (slope, C=10^b, r^2).
    Heisenberg scaling has slope = 1 (i.e. Norac ~ 1/eps).
    """
    x = np.log10([r["eps_p95"] for r in rows])
    y = np.log10([r["norac_median"] for r in rows])
    if len(x) < 2:
        return float("nan"), float("nan"), float("nan")
    # Least-squares fit of y = -slope * x + b   =>   y = m*x + b with m = -slope
    A = np.vstack([x, np.ones_like(x)]).T
    m, b = np.linalg.lstsq(A, y, rcond=None)[0]
    slope = -float(m)
    C = float(10 ** b)
    yhat = m * x + b
    ss_res = float(np.sum((y - yhat) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    return slope, C, r2


def main():
    t0 = time.time()
    a_values = [0.1, 0.2, 0.3, 0.4]
    fae_ells = [3, 4, 5, 6, 7]   # ell=7 -> ~1.5e6 Norac, still fast
    mlae_Ms = [4, 5, 6, 7, 8, 9] # M=9 -> ~5e4 Norac at Nshot=100
    n_trials_fae = 100
    n_trials_mlae = 200
    N_shot_mlae = 100

    all_rows: List[Dict] = []
    fits: List[Dict] = []

    for a in a_values:
        print(f"\n=== a = {a} ===")
        fae_rows = run_fae_sweep(a, fae_ells, n_trials_fae)
        mlae_rows = run_mlae_sweep(a, mlae_Ms, n_trials_mlae, N_shot=N_shot_mlae)
        all_rows.extend(fae_rows)
        all_rows.extend(mlae_rows)

        slope_f, C_f, r2_f = fit_prefactor(fae_rows)
        slope_m, C_m, r2_m = fit_prefactor(mlae_rows)
        fits.append(dict(a=a,
                         FAE_slope=slope_f, FAE_prefactor_C=C_f, FAE_R2=r2_f,
                         MLAE_slope=slope_m, MLAE_prefactor_C=C_m, MLAE_R2=r2_m,
                         ratio_MLAE_over_FAE_prefactor=(C_m / C_f) if C_f > 0 else float("nan")))
        print(f"  FIT FAE : slope={slope_f:.3f}  C={C_f:.3e}  R^2={r2_f:.3f}")
        print(f"  FIT MLAE: slope={slope_m:.3f}  C={C_m:.3e}  R^2={r2_m:.3f}")
        print(f"  MLAE_prefactor / FAE_prefactor = {C_m / C_f:.2f}x")

    # Save
    csv_path = os.path.join(EVIDENCE_DIR, "sweep_raw.csv")
    keys = sorted({k for r in all_rows for k in r.keys()})
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in all_rows:
            w.writerow(r)
    print(f"\nWrote raw sweep -> {csv_path}")

    fit_path = os.path.join(EVIDENCE_DIR, "fits.json")
    with open(fit_path, "w") as f:
        json.dump({"fits": fits, "elapsed_sec": time.time() - t0,
                   "n_trials_fae": n_trials_fae, "n_trials_mlae": n_trials_mlae,
                   "N_shot_mlae": N_shot_mlae}, f, indent=2)
    print(f"Wrote fits    -> {fit_path}")
    print(f"\nElapsed: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
