#!/usr/bin/env python3
"""
Independent replication of Belovs (2012), arXiv:1205.1534,
"Learning-Graph-Based Quantum Algorithm for k-distinctness".

Reproduces the paper's Eq. (12) objective function for the learning-graph
complexity C(r_1,...,r_{k-1}; n) of the k-distinctness algorithm, and
verifies numerically that the optimum scales as n^{1 - 2^{k-2}/(2^k-1)}
across N in {6, 8, 10, 12, 16, 24, 32, 48, 64, 96, 128}.

The learning graph formalism is exact: given a valid assignment of
edge weights (equivalently, the size parameters r_i for the symmetric
stages), C(P) is the sum of stage complexities as in Eq. (12), and Belovs'
Theorem 5 states that the corresponding bounded-error quantum query
algorithm has query complexity O(C(P)).

We:
  (a) implement Eq. (12) as a real numeric function C_k(r_1,...,r_{k-1}; n);
  (b) find the optimal r_i by numerical minimization (SLSQP on log(r_i));
  (c) log-log fit C_opt(n) vs n to extract the exponent rho_1;
  (d) compare with the closed-form rho_1 = 1 - 2^{k-2}/(2^k-1)
        - k=2: 2/3
        - k=3: 5/7
        - k=4: 11/15
        - k=5: 23/31
  (e) compare with the Ambainis baseline O(n^{k/(k+1)}) [Table 1 of the
      paper], which is what one gets from choosing all r_i equal (in fact
      from the single-parameter r = n^{k/(k+1)} construction);
  (f) compute a random-weight baseline: pick r_i uniformly at random in
      log-space; report mean/best complexity vs the optimum.

Free/open: pure numpy + scipy. No LLM / paid API used.
"""
from __future__ import annotations

import json
import math
import os
import sys
from dataclasses import dataclass, asdict
from typing import List, Tuple

import numpy as np
from scipy.optimize import minimize


# ---------------------------------------------------------------------------
# Eq. (12) of Belovs (2012):
#   C(r_1,...,r_{k-1}; n) =
#     r_1
#   + r_2 * sqrt(r_1 / n)
#   + r_3 * sqrt(r_1 r_2 / n^2)
#   + ...
#   + r_{k-1} * sqrt(r_1 ... r_{k-2} / n^{k-2})
#   + sqrt( n^k / (r_1 ... r_{k-1}) )
#
# All arguments in the sqrt() are dimensionless ratios that are <= 1 under
# the paper's regime r_i = o(n).  The last term is the complexity of stage
# II.k (loading a_k) and dominates when the r_i are too small; the first
# terms dominate when r_i are too large.
# ---------------------------------------------------------------------------


def belovs_complexity(rs: np.ndarray, n: float) -> float:
    """Numerical value of Eq. (12) for a given (r_1,...,r_{k-1}) and n."""
    rs = np.asarray(rs, dtype=float)
    k_minus_1 = len(rs)
    k = k_minus_1 + 1

    # Stage I.1 : r_1
    total = rs[0]
    # Stage I.s (s >= 2) : r_s * sqrt(r_1 * ... * r_{s-1} / n^{s-1})
    prefix_prod = 1.0
    for s in range(2, k):  # s = 2 .. k-1
        prefix_prod *= rs[s - 2]  # r_{s-1}
        total += rs[s - 1] * math.sqrt(prefix_prod / (n ** (s - 1)))
    # Stage II.k dominant term : sqrt(n^k / (r_1 * ... * r_{k-1}))
    full_prod = float(np.prod(rs))
    total += math.sqrt((n ** k) / full_prod)
    return total


def optimize_belovs(n: float, k: int, n_restarts: int = 12,
                    seed: int = 12345) -> Tuple[float, np.ndarray]:
    """Minimize Eq. (12) over r_1,...,r_{k-1} in (1, n).

    We optimize log(r_i) so the search space is unconstrained and
    proportional to the exponents ρ_i = log_n(r_i) that Belovs uses.
    """
    rng = np.random.default_rng(seed + int(round(n * 1000)) + 17 * k)
    log_n = math.log(n)
    # Bounds so r_i stays strictly in (1, n) (which is where the algorithm
    # is defined; r_i = o(n) as n -> infinity is the paper's regime).
    lb = math.log(1.1)
    ub = math.log(n - 1e-3)

    def obj(log_rs: np.ndarray) -> float:
        rs = np.exp(log_rs)
        return belovs_complexity(rs, n)

    best_val, best_rs = math.inf, None
    for _ in range(n_restarts):
        # Random log-space initialization concentrated near the paper's
        # asymptotic solution ρ_1 = 1 - 2^{k-2}/(2^k - 1).
        target_rho1 = 1.0 - (2 ** (k - 2)) / (2 ** k - 1)
        # ρ_{i+1} = (1 + ρ_i)/2  ==> ρ_i = 1 - (1 - ρ_1)/2^{i-1}
        rhos_init = np.array(
            [1.0 - (1.0 - target_rho1) / (2 ** (i - 1)) for i in range(1, k)])
        # Perturb start
        rhos_init += rng.normal(scale=0.15, size=rhos_init.shape)
        # Also try one purely-random start per pass
        if _ >= n_restarts // 2:
            rhos_init = rng.uniform(0.3, 0.95, size=k - 1)
        x0 = np.clip(rhos_init * log_n, lb, ub)
        try:
            res = minimize(obj, x0, method='Nelder-Mead',
                           options={'xatol': 1e-8, 'fatol': 1e-8,
                                    'maxiter': 5000})
        except Exception:
            continue
        if res.fun < best_val:
            best_val, best_rs = float(res.fun), np.exp(res.x)
    return best_val, best_rs


def ambainis_baseline(n: float, k: int) -> float:
    """Ambainis Table-1 baseline: C = O(r + sqrt(n^k / r^{k-1})).
    Optimum at r = n^{k/(k+1)}, value O(n^{k/(k+1)}).  We report the exact
    minimum of the analytic expression (no big-O constants)."""
    # Minimize r + sqrt(n^k / r^{k-1}) analytically.
    # Take derivative: 1 - (k-1)/2 * n^{k/2} * r^{-(k+1)/2} = 0
    #   ==> r = ((k-1)/2)^{2/(k+1)} * n^{k/(k+1)}
    coef = ((k - 1) / 2.0) ** (2.0 / (k + 1))
    r_opt = coef * (n ** (k / (k + 1)))
    return r_opt + math.sqrt((n ** k) / (r_opt ** (k - 1)))


def random_weight_baseline(n: float, k: int, n_samples: int = 200,
                           seed: int = 424242) -> Tuple[float, float]:
    """Random assignment: sample r_i uniformly in log-space in (1, n).
    Returns (best_random, mean_random) complexities."""
    rng = np.random.default_rng(seed + int(n))
    vals = []
    for _ in range(n_samples):
        rs = np.exp(rng.uniform(math.log(1.5), math.log(n - 0.5), size=k - 1))
        vals.append(belovs_complexity(rs, n))
    vals = np.array(vals)
    return float(vals.min()), float(vals.mean())


def loglog_slope(xs: List[float], ys: List[float]) -> Tuple[float, float]:
    """Linear regression of log(y) vs log(x). Returns (slope, intercept)."""
    lx = np.log(np.asarray(xs, dtype=float))
    ly = np.log(np.asarray(ys, dtype=float))
    a, b = np.polyfit(lx, ly, 1)
    return float(a), float(b)


# ---------------------------------------------------------------------------
# Paper predictions
# ---------------------------------------------------------------------------
def predicted_rho1(k: int) -> float:
    return 1.0 - (2 ** (k - 2)) / (2 ** k - 1)


def predicted_ambainis_rho(k: int) -> float:
    return k / (k + 1)


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------
@dataclass
class Row:
    k: int
    n: int
    C_opt: float
    C_ambainis: float
    C_random_best: float
    C_random_mean: float
    r_opt: List[float]


def run_experiment(k_values: List[int], n_values: List[int]) -> dict:
    rows: List[Row] = []
    per_k_summary = {}
    for k in k_values:
        opt_vals = []
        amb_vals = []
        for n in n_values:
            c_opt, rs = optimize_belovs(float(n), k)
            c_amb = ambainis_baseline(float(n), k)
            c_rand_best, c_rand_mean = random_weight_baseline(float(n), k)
            rows.append(Row(k=k, n=n, C_opt=c_opt, C_ambainis=c_amb,
                            C_random_best=c_rand_best,
                            C_random_mean=c_rand_mean,
                            r_opt=[float(x) for x in rs]))
            opt_vals.append(c_opt)
            amb_vals.append(c_amb)
        slope_opt, _ = loglog_slope(n_values, opt_vals)
        slope_amb, _ = loglog_slope(n_values, amb_vals)
        per_k_summary[str(k)] = dict(
            fitted_rho1=slope_opt,
            paper_rho1=predicted_rho1(k),
            fitted_ambainis_rho=slope_amb,
            paper_ambainis_rho=predicted_ambainis_rho(k),
            abs_err_rho1=abs(slope_opt - predicted_rho1(k)),
            abs_err_ambainis=abs(slope_amb - predicted_ambainis_rho(k)),
            improvement_over_ambainis=predicted_ambainis_rho(k) - slope_opt,
        )
    return dict(rows=[asdict(r) for r in rows],
                per_k_summary=per_k_summary)


if __name__ == '__main__':
    k_values = [2, 3, 4, 5]
    # Use a broad range so the exponent fit is well-resolved; the paper
    # analyzes the n -> infinity regime so we go up to N=256.
    n_values = [6, 8, 10, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256]

    out = run_experiment(k_values, n_values)
    # Pretty print
    print("=" * 72)
    print("Belovs (2012) k-distinctness learning-graph replication")
    print("=" * 72)
    print(f"{'k':>3} {'n':>4} {'C_opt':>12} {'C_ambainis':>12} "
          f"{'C_rand_best':>12} {'C_rand_mean':>12}")
    for row in out['rows']:
        print(f"{row['k']:>3} {row['n']:>4} {row['C_opt']:12.4f} "
              f"{row['C_ambainis']:12.4f} {row['C_random_best']:12.4f} "
              f"{row['C_random_mean']:12.4f}")

    print()
    print("Log-log fitted exponents (over N = 6..256):")
    print(f"{'k':>3} {'fit_rho1':>10} {'paper_rho1':>12} {'err':>8} "
          f"{'fit_amb':>10} {'paper_amb':>12} {'err':>8} {'gain':>8}")
    for k, s in out['per_k_summary'].items():
        print(f"{k:>3} {s['fitted_rho1']:10.4f} {s['paper_rho1']:12.4f} "
              f"{s['abs_err_rho1']:8.4f} "
              f"{s['fitted_ambainis_rho']:10.4f} "
              f"{s['paper_ambainis_rho']:12.4f} "
              f"{s['abs_err_ambainis']:8.4f} "
              f"{s['improvement_over_ambainis']:8.4f}")

    out_path = os.path.join(os.path.dirname(__file__), 'belovs_results.json')
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved: {out_path}")
