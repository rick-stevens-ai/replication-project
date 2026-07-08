#!/usr/bin/env python3
"""
Replication of Suzuki et al. (2020), "Amplitude estimation without phase estimation".

Classical statevector model: the algorithm's 2D good/bad subspace is exact.
We simulate Q^m |Psi> -> sin((2m+1) theta_a) |good>, sample Bernoulli outcomes,
combine likelihoods over a schedule {m_k}, and MLE-recover theta_a.

We reproduce Fig. 2 qualitatively: error vs N_queries for
  - classical (m_k=0 for all k)              expected slope ~ -1/2
  - LIS (m_k = 0,1,2,...,M)                  expected slope ~ -3/4
  - EIS (m_k = 0, 2^0, 2^1, ..., 2^(M-1))    expected slope ~ -1   (Heisenberg-like)

N_shot = 100 per circuit (matches paper Sec. 3.3).
Trials = 200 per (schedule, M) point.
Targets: a in {2/3, 1/3, 1/6, 1/12, 1/24, 1/48}.

Outputs: results.json with full scaling data, plus a PNG figure if matplotlib
is present (best-effort; not required for the audit).
"""

from __future__ import annotations

import json
import math
import os
import time
from dataclasses import dataclass, asdict
from typing import List, Sequence, Tuple

import numpy as np

# -----------------------------------------------------------------------------
# Core algorithm
# -----------------------------------------------------------------------------

def good_prob(m: int, theta_a: float) -> float:
    """Probability of measuring |good> after Q^m |Psi>."""
    return math.sin((2 * m + 1) * theta_a) ** 2


def sample_h(rng: np.random.Generator, m_list: Sequence[int], N_k: int,
             theta_a_true: float) -> np.ndarray:
    """Sample h_k ~ Binomial(N_k, sin^2((2m_k+1)theta_a)) for each k."""
    h = np.empty(len(m_list), dtype=np.int64)
    for i, m in enumerate(m_list):
        p = good_prob(m, theta_a_true)
        h[i] = rng.binomial(N_k, p)
    return h


def neg_log_likelihood_grid(theta_grid: np.ndarray, m_arr: np.ndarray,
                            h_arr: np.ndarray, N_k: int) -> np.ndarray:
    """Vectorized -log L(h; theta) on a theta grid.

    L_k = sin^2((2m+1)theta)^h * cos^2((2m+1)theta)^(N-h)
    ln L_k = h * ln(sin^2(...)) + (N-h) * ln(cos^2(...))
    """
    # shape: (G, K)
    angles = np.outer(theta_grid, 2 * m_arr + 1)
    s2 = np.sin(angles) ** 2
    c2 = 1.0 - s2
    # numerical floor
    eps = 1e-300
    s2 = np.clip(s2, eps, 1.0)
    c2 = np.clip(c2, eps, 1.0)
    ln_s2 = np.log(s2)
    ln_c2 = np.log(c2)
    log_L = h_arr * ln_s2 + (N_k - h_arr) * ln_c2  # broadcast over G
    log_L_total = log_L.sum(axis=1)  # (G,)
    return -log_L_total


def mle_theta(m_list: Sequence[int], h: np.ndarray, N_k: int,
              coarse_pts: int = 4001, refine_pts: int = 2001,
              refine_window: float = None) -> float:
    """Brute-force MLE over [0, pi/2] then refine around best grid point.

    For EIS at large M, the likelihood is multi-modal (period pi/(2*m_max+1));
    coarse grid must resolve each lobe. We then do a local fine refinement.
    """
    m_arr = np.asarray(m_list, dtype=np.int64)
    h_arr = np.asarray(h, dtype=np.int64)
    max_freq = float(2 * m_arr.max() + 1)

    # Coarse global scan: ensure ~20 points per lobe of the highest-freq term
    # lobe width ~ pi / max_freq; total range pi/2 -> need ~ 10 * max_freq pts
    pts_needed = int(20 * max_freq) + 1
    coarse_pts = max(coarse_pts, min(pts_needed, 200001))
    theta_coarse = np.linspace(1e-6, math.pi / 2 - 1e-6, coarse_pts)
    nll = neg_log_likelihood_grid(theta_coarse, m_arr, h_arr, N_k)
    i_star = int(np.argmin(nll))
    theta_star = float(theta_coarse[i_star])

    # Local refinement: ~3 coarse-grid spacings on each side
    spacing = (math.pi / 2) / (coarse_pts - 1)
    if refine_window is None:
        refine_window = 3.0 * spacing
    lo = max(1e-9, theta_star - refine_window)
    hi = min(math.pi / 2 - 1e-9, theta_star + refine_window)
    theta_fine = np.linspace(lo, hi, refine_pts)
    nll_fine = neg_log_likelihood_grid(theta_fine, m_arr, h_arr, N_k)
    j = int(np.argmin(nll_fine))
    return float(theta_fine[j])


# -----------------------------------------------------------------------------
# Schedules & query counts
# -----------------------------------------------------------------------------

def schedule_classical(M: int) -> List[int]:
    # M+1 circuits, all with m_k = 0
    return [0] * (M + 1)


def schedule_LIS(M: int) -> List[int]:
    # m_k = k, k = 0..M
    return list(range(M + 1))


def schedule_EIS(M: int) -> List[int]:
    # m_0 = 0, m_k = 2^(k-1) for k >= 1
    if M == 0:
        return [0]
    return [0] + [2 ** (k - 1) for k in range(1, M + 1)]


def total_queries(m_list: Sequence[int], N_k: int) -> int:
    return int(N_k * sum(2 * m + 1 for m in m_list))


# -----------------------------------------------------------------------------
# Experiment driver
# -----------------------------------------------------------------------------

@dataclass
class RunCfg:
    schedule_name: str
    M: int
    N_shot: int
    n_trials: int


def run_trials(target_a: float, cfg: RunCfg, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    theta_true = math.asin(math.sqrt(target_a))

    if cfg.schedule_name == "classical":
        m_list = schedule_classical(cfg.M)
    elif cfg.schedule_name == "LIS":
        m_list = schedule_LIS(cfg.M)
    elif cfg.schedule_name == "EIS":
        m_list = schedule_EIS(cfg.M)
    else:
        raise ValueError(cfg.schedule_name)

    Nq = total_queries(m_list, cfg.N_shot)
    a_hats = np.empty(cfg.n_trials)

    # classical case has closed-form MLE; use it for speed and exactness
    if cfg.schedule_name == "classical":
        for t in range(cfg.n_trials):
            h = sample_h(rng, m_list, cfg.N_shot, theta_true)
            phat = float(h.sum()) / float(cfg.N_shot * len(m_list))
            phat = min(max(phat, 0.0), 1.0)
            a_hats[t] = phat
    else:
        for t in range(cfg.n_trials):
            h = sample_h(rng, m_list, cfg.N_shot, theta_true)
            theta_hat = mle_theta(m_list, h, cfg.N_shot)
            a_hats[t] = math.sin(theta_hat) ** 2

    errors = a_hats - target_a
    rmse = float(math.sqrt(np.mean(errors ** 2)))
    bias = float(np.mean(errors))
    return {
        "schedule": cfg.schedule_name,
        "M": cfg.M,
        "N_shot": cfg.N_shot,
        "n_trials": cfg.n_trials,
        "target_a": target_a,
        "m_list": list(map(int, m_list)),
        "N_queries": int(Nq),
        "rmse": rmse,
        "bias": bias,
        "a_hat_mean": float(np.mean(a_hats)),
        "a_hat_std": float(np.std(a_hats)),
        # Cramer-Rao lower bound: sigma >= sqrt(a(1-a) / I_total)
        "crb": float(
            math.sqrt(target_a * (1 - target_a)
                      / (cfg.N_shot * sum((2 * m + 1) ** 2 for m in m_list)))
        ),
    }


def fit_slope(log_x: np.ndarray, log_y: np.ndarray) -> Tuple[float, float]:
    """Least-squares slope of log_y vs log_x."""
    A = np.vstack([log_x, np.ones_like(log_x)]).T
    slope, intercept = np.linalg.lstsq(A, log_y, rcond=None)[0]
    return float(slope), float(intercept)


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    out_json = os.path.join(here, "results.json")

    target_as = [2 / 3, 1 / 3, 1 / 6, 1 / 12, 1 / 24, 1 / 48]
    N_shot = 100
    n_trials = 200

    # Choose M ranges so total queries roughly span 10^2 - 10^5 (paper Fig. 2 range)
    # Classical: Nq = N_shot * (M+1) -> M up to ~999 for Nq=1e5; pick a sparse log set
    classical_Ms = [1, 3, 9, 29, 99, 299, 999]
    # LIS: Nq = N_shot * (M+1)^2 -> M up to ~31 for Nq=1e5
    LIS_Ms = [1, 2, 3, 5, 8, 12, 20, 31]
    # EIS: Nq ~ N_shot * (2^M ish). M=10 -> Nq ~ ~1.1e5
    EIS_Ms = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    n_trials_eis_big = 100   # large-M EIS is the slowest, halve trials for M>=9

    t0 = time.time()
    runs: List[dict] = []
    seed_base = 20260626

    for a in target_as:
        # classical
        for M in classical_Ms:
            cfg = RunCfg("classical", M, N_shot, n_trials)
            runs.append(run_trials(a, cfg, seed=seed_base + hash((a, "C", M)) % (2**31)))
        # LIS
        for M in LIS_Ms:
            cfg = RunCfg("LIS", M, N_shot, n_trials)
            runs.append(run_trials(a, cfg, seed=seed_base + hash((a, "L", M)) % (2**31)))
        # EIS
        for M in EIS_Ms:
            nt = n_trials_eis_big if M >= 9 else n_trials
            cfg = RunCfg("EIS", M, N_shot, nt)
            runs.append(run_trials(a, cfg, seed=seed_base + hash((a, "E", M)) % (2**31)))
        elapsed = time.time() - t0
        print(f"[a={a:.5f}] runs={len(runs):3d}  elapsed={elapsed:6.1f}s")

    # Fit scaling exponents for a=1/48 (paper's reported slopes)
    slopes = {}
    a_ref = 1 / 48
    for sched in ("classical", "LIS", "EIS"):
        pts = [(r["N_queries"], r["rmse"]) for r in runs
               if r["schedule"] == sched and abs(r["target_a"] - a_ref) < 1e-9
               and r["N_queries"] >= 1000 and r["N_queries"] <= 1e5]
        if len(pts) >= 2:
            xs = np.array([p[0] for p in pts], dtype=float)
            ys = np.array([p[1] for p in pts], dtype=float)
            slope, intercept = fit_slope(np.log(xs), np.log(ys))
            slopes[sched] = {
                "slope": slope,
                "intercept": intercept,
                "n_points": len(pts),
                "Nq_range": [float(xs.min()), float(xs.max())],
                "paper_slope": {"classical": -0.50, "LIS": -0.76, "EIS": -0.95}[sched],
            }

    payload = {
        "paper": "Suzuki et al. 2020, Amplitude estimation without phase estimation",
        "target_as": target_as,
        "N_shot": N_shot,
        "n_trials": n_trials,
        "classical_Ms": classical_Ms,
        "LIS_Ms": LIS_Ms,
        "EIS_Ms": EIS_Ms,
        "runs": runs,
        "scaling_fit_a_1over48": slopes,
        "wallclock_sec": time.time() - t0,
    }

    with open(out_json, "w") as fh:
        json.dump(payload, fh, indent=2)
    print(f"Wrote {out_json}  ({os.path.getsize(out_json)} bytes)")

    # Optional figure
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(7, 5))
        colors = {"classical": "tab:blue", "LIS": "tab:red", "EIS": "k"}
        markers = {"classical": "s", "LIS": "^", "EIS": "o"}
        for sched in ("classical", "LIS", "EIS"):
            pts = [(r["N_queries"], r["rmse"]) for r in runs
                   if r["schedule"] == sched and abs(r["target_a"] - a_ref) < 1e-9]
            pts.sort()
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            ax.loglog(xs, ys, marker=markers[sched], color=colors[sched],
                      linestyle="none", label=sched)
            # CRB line
            crbs = [(r["N_queries"], r["crb"]) for r in runs
                    if r["schedule"] == sched and abs(r["target_a"] - a_ref) < 1e-9]
            crbs.sort()
            ax.loglog([p[0] for p in crbs], [p[1] for p in crbs],
                      color=colors[sched], linestyle="--", alpha=0.5)
        ax.set_xlabel("Number of queries $N_q$")
        ax.set_ylabel(r"Estimation error $\hat{\varepsilon}$ (RMSE on $a$)")
        ax.set_title(f"Suzuki et al. 2020 Fig. 2 replication, a=1/48, N_shot={N_shot}")
        ax.legend()
        ax.grid(True, which="both", alpha=0.3)
        fig.tight_layout()
        fig.savefig(os.path.join(here, "fig_scaling_a1_48.png"), dpi=140)
        print("Wrote fig_scaling_a1_48.png")
    except Exception as e:
        print(f"(matplotlib skipped: {e})")


if __name__ == "__main__":
    main()
