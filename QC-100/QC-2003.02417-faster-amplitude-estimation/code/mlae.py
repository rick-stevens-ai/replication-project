"""Maximum Likelihood Amplitude Estimation (MLAE) — Suzuki et al 2019 (arXiv:1904.10246).

Canonical exponentially-incremental sequence:
  m_k = 2^(k-1) for k=1..M   (m_0 = 0 with the initial Nshot0 measurements)
For each m_k perform Nshot Bernoulli trials and count h_k = #(good outcomes).
Likelihood:
  L(theta) = prod_k [ sin^2((2 m_k + 1) theta) ]^h_k * [ cos^2((2 m_k + 1) theta) ]^(Nshot - h_k)
Log-likelihood is maximised over theta in [0, pi/2] (grid search then refine).

For attenuated encoding compatible with FAE:
  a in [0, 1], theta = arcsin(a/4), theta in [0, 0.252].
We fix the search interval [0, 0.4] (safely covers 0.252 for a up to 1).

Norac accounting: same as FAE — sum_k m_k * Nshot_k oracle calls (m_0 term = 0).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
from scipy.optimize import minimize_scalar

from oracle import exact_prob_good_after_Qm, theta_true


@dataclass
class MLAEResult:
    theta_hat: float
    a_hat: float
    norac: int
    M: int
    N_shot: int
    theta_true: float
    a_true: float
    theta_error: float
    a_error: float


def run_mlae(a: float, M: int, N_shot: int = 100, seed: int = 0) -> MLAEResult:
    """Run MLAE with exponential sequence m_k = 2^(k-1), k=1..M, plus m_0 = 0.

    Returns theta_hat maximising the joint likelihood over [0, 0.4] (the paper's attenuated range).
    """
    rng = np.random.default_rng(seed)

    # Sequence: m_0 = 0, m_k = 2^(k-1) for k=1..M
    ms: List[int] = [0] + [2 ** (k - 1) for k in range(1, M + 1)]
    hs: List[int] = []
    norac = 0
    for m in ms:
        p_good = exact_prob_good_after_Qm(a, m)
        h = int(rng.binomial(N_shot, p_good))
        hs.append(h)
        norac += m * N_shot  # m=0 contributes 0

    # Negative log-likelihood
    def neg_log_L(theta: float) -> float:
        total = 0.0
        for m, h in zip(ms, hs):
            angle = (2 * m + 1) * theta
            sin2 = math.sin(angle) ** 2
            cos2 = math.cos(angle) ** 2
            # Small floor to avoid log(0)
            sin2 = max(sin2, 1e-300)
            cos2 = max(cos2, 1e-300)
            total += h * math.log(sin2) + (N_shot - h) * math.log(cos2)
        return -total

    # Coarse grid over [0, 0.4] then refine
    grid = np.linspace(1e-6, 0.4, 4001)
    values = [neg_log_L(float(t)) for t in grid]
    idx = int(np.argmin(values))
    t0 = float(grid[idx])
    lo = max(1e-9, grid[max(idx - 1, 0)])
    hi = float(grid[min(idx + 1, len(grid) - 1)])
    res = minimize_scalar(neg_log_L, bracket=(lo, t0, hi), method="brent",
                          options={"xtol": 1e-10})
    theta_hat = float(res.x)
    if not (0.0 <= theta_hat <= math.pi / 2):
        theta_hat = t0

    a_hat = 4.0 * math.sin(theta_hat)
    th_t = theta_true(a)
    return MLAEResult(
        theta_hat=theta_hat,
        a_hat=a_hat,
        norac=norac,
        M=M,
        N_shot=N_shot,
        theta_true=th_t,
        a_true=a,
        theta_error=abs(theta_hat - th_t),
        a_error=abs(a_hat - a),
    )


if __name__ == "__main__":
    for a in [0.1, 0.2, 0.3, 0.4]:
        for M in [3, 4, 5, 6, 7]:
            res = run_mlae(a, M, N_shot=100, seed=42)
            print(f"a={a} M={M}  a_hat={res.a_hat:.6f}  err={res.a_error:.4e}  Norac={res.norac:.3e}")
        print()
