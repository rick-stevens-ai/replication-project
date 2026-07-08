"""Amplitude-estimation algorithms: IQAE and ChebAE.

Both implemented per Rall & Fuller 2022 (arXiv:2207.08628), Section 3.
- IQAE reproduces Grinko et al. 2019 (odd Chebyshev polys only, θ-space).
- ChebAE (Empirical Claim 18) uses a-space, all-degree Chebyshev, and a
  tuned early/late cutoff (parameter ν).

Sampling primitive:
    A single "coin toss" from polynomial T_d(a) returns 1 with probability |T_d(a)|^2.
    Query cost per toss is d (queries to Z_Pi).  (In the physical Grover circuit
    with k iterations, d = 2k+1; we count d oracle queries per toss.)

We statistically simulate the coin using numpy Bernoulli sampling with
p = T_d(a)^2, which matches what the Grover statevector circuit would give
(verified in grover_statevector_check.py to machine precision).
"""
from __future__ import annotations
import math
from dataclasses import dataclass, field
from typing import Tuple, Callable

import numpy as np
from scipy.stats import beta as beta_dist  # for Clopper-Pearson


# ---------- Clopper-Pearson confidence interval on a binomial proportion ----------

def clopper_pearson(nheads: int, nflips: int, alpha: float) -> Tuple[float, float]:
    """(1-alpha) Clopper-Pearson CI on the binomial success probability p.

    lo = Beta.ppf(alpha/2,       k,   n-k+1)
    hi = Beta.ppf(1-alpha/2,     k+1, n-k)
    """
    if nflips == 0:
        return 0.0, 1.0
    if nheads == 0:
        lo = 0.0
    else:
        lo = beta_dist.ppf(alpha/2.0, nheads, nflips - nheads + 1)
    if nheads == nflips:
        hi = 1.0
    else:
        hi = beta_dist.ppf(1.0 - alpha/2.0, nheads + 1, nflips - nheads)
    return float(lo), float(hi)


def clopper_pearson_max_halfwidth(N: int, alpha: float) -> float:
    """Maximum half-width of a (1-alpha) CP interval over all k in [0..N] (worst case at k=N/2)."""
    k = N // 2
    lo, hi = clopper_pearson(k, N, alpha)
    return (hi - lo) / 2.0


# ---------- Chebyshev of first kind ----------

def T(d: int, a: float) -> float:
    """Chebyshev polynomial of the first kind: T_d(a) = cos(d * arccos(a))."""
    # Numerically stable for a in [0,1]
    if a >= 1.0:
        return 1.0
    if a <= -1.0:
        return (-1.0) ** d
    return math.cos(d * math.acos(a))


def sample_Td_squared(d: int, a: float, N: int, rng: np.random.Generator) -> int:
    """Sample N Bernoulli(|T_d(a)|^2) tosses; return number of heads."""
    p = T(d, a) ** 2
    # numpy binomial handles this efficiently
    return int(rng.binomial(N, p))


# ---------- IQAE (Grinko et al. 2019, as re-described in Rall-Fuller Sec 3) ----------
#
# IQAE works in theta-space: finds largest odd K_i such that K_i*[theta_min,theta_max]
# is contained in one half-period of cos, samples T_{K_i}, converts CI back.
# Implementation follows Grinko et al. Algorithm 1 (standard reference impl).

@dataclass
class RunResult:
    a_hat: float
    a_lo: float
    a_hi: float
    total_queries_Zpi: int
    max_depth: int
    n_iters: int
    correct: bool


def _find_next_K_iqae(K_prev: int, amin: float, amax: float, r_min: float = 2.0):
    """Find largest odd K such that |T_K(a)|^2 is monotone on [amin,amax] and K >= r_min * K_prev.
    Returns K (may equal K_prev if no improvement).
    """
    theta_min = math.acos(amax)
    theta_max = math.acos(amin)
    if theta_max <= theta_min:
        return K_prev
    K_upper = max(1, int(math.floor(math.pi / (2.0 * (theta_max - theta_min)))))
    # ensure odd
    if K_upper % 2 == 0:
        K_upper -= 1
    K = K_upper
    K_min = max(1, int(math.ceil(r_min * K_prev)))
    if K_min % 2 == 0:
        K_min += 1
    while K >= K_min:
        if math.floor(2*K*theta_min/math.pi) == math.floor(2*K*theta_max/math.pi):
            return K
        K -= 2
    return K_prev


def iqae(
    a_true: float,
    epsilon: float,
    delta: float,
    Nshots: int = 100,
    rng: np.random.Generator | None = None,
    max_iters: int = 200,
) -> RunResult:
    """Iterative Quantum Amplitude Estimation (Grinko et al. 2019).

    Confidence-interval approach in theta = arcsin(a) space.
    Returns half-width-<= epsilon estimate of a with prob >= 1-delta (as per paper).
    """
    if rng is None:
        rng = np.random.default_rng()

    amin, amax = 0.0, 1.0
    K = 1
    nheads = 0
    nflips = 0
    # Bound on number of CIs (per paper) - use logr(1/eps) with r=2
    T_bound = max(1, int(np.ceil(np.log2(1.0/max(epsilon, 1e-30)))))
    alpha_per_iter = delta / T_bound

    total_queries = 0
    max_depth = 0
    n_iter = 0
    for it in range(max_iters):
        n_iter += 1
        K_new = _find_next_K_iqae(K, amin, amax, r_min=2.0)
        if K_new > K:
            K = K_new
            nheads, nflips = 0, 0

        d = K
        h = sample_Td_squared(d, a_true, Nshots, rng)
        nheads += h
        nflips += Nshots
        total_queries += Nshots * d
        max_depth = max(max_depth, d)

        pmin, pmax = clopper_pearson(nheads, nflips, alpha_per_iter)
        try:
            new_amin, new_amax = _invert_TK_squared_interval(d, amin, amax, pmin, pmax)
        except Exception:
            new_amin, new_amax = amin, amax

        new_amin = max(new_amin, amin)
        new_amax = min(new_amax, amax)
        if new_amin > new_amax:
            new_amin, new_amax = amin, amax

        amin, amax = new_amin, new_amax

        if amax - amin < 2*epsilon:
            a_hat = 0.5*(amin + amax)
            return RunResult(a_hat, amin, amax, total_queries, max_depth, n_iter,
                             abs(a_hat - a_true) <= epsilon)

    a_hat = 0.5*(amin + amax)
    return RunResult(a_hat, amin, amax, total_queries, max_depth, n_iter,
                     abs(a_hat - a_true) <= epsilon)


# ---------- helper: invert |T_K(a)|^2 in [amin,amax] ----------

def _invert_TK_squared_interval(K: int, amin: float, amax: float,
                                pmin: float, pmax: float) -> Tuple[float, float]:
    """Given that a in [amin,amax] and |T_K(a)|^2 in [pmin,pmax], return refined [a*min, a*max].

    Works only when a -> |T_K(a)|^2 is monotone on [amin, amax].
    If not monotone we fall back to the original interval.
    """
    # Sample T_K on the interval to check monotonicity
    grid = np.linspace(amin, amax, 8)
    vals = np.array([T(K, x)**2 for x in grid])
    increasing = np.all(np.diff(vals) >= -1e-12)
    decreasing = np.all(np.diff(vals) <=  1e-12)
    if not (increasing or decreasing):
        return amin, amax  # not monotone; can't invert cleanly

    # binary-search invert
    def invert(pt):
        pt = max(0.0, min(1.0, pt))
        lo, hi = amin, amax
        for _ in range(60):
            mid = 0.5*(lo+hi)
            v = T(K, mid)**2
            if increasing:
                if v < pt: lo = mid
                else:      hi = mid
            else:  # decreasing
                if v > pt: lo = mid
                else:      hi = mid
        return 0.5*(lo+hi)

    a1 = invert(pmin)
    a2 = invert(pmax)
    lo, hi = min(a1, a2), max(a1, a2)
    return lo, hi


# ---------- ChebAE (Rall-Fuller, Empirical Claim 18) ----------

def _find_next_cheb(amin: float, amax: float) -> int:
    """Return the largest d such that |T_d(a)|^2 is invertible (monotone) on [amin,amax].

    |T_d(a)|^2 = cos^2(d*arccos(a)) has extrema where d*theta = k*pi/2 (i.e. every half-
    period of cos^2 is pi/(2d) in theta-space).  Monotone iff floor(2*d*theta/pi) is
    constant across theta in [arccos(amax), arccos(amin)].
    (This is the exact criterion from the paper's step-3 pseudocode:
     floor(2*d*theta_min/pi) == floor(2*d*theta_max/pi).)
    """
    theta_min = math.acos(amax)
    theta_max = math.acos(amin)
    if theta_max <= theta_min:
        return 1
    # start from a generous upper bound: half-period of cos^2 is pi/(2d),
    # so we need d*(theta_max - theta_min) <= pi/2  =>  d <= pi/(2*(theta_max-theta_min))
    d = max(1, int(math.floor(math.pi / (2.0 * (theta_max - theta_min)))))
    while d >= 1:
        if math.floor(2*d*theta_min/math.pi) == math.floor(2*d*theta_max/math.pi):
            return d
        d -= 1
    return 1


def chebae(
    a_true: float,
    epsilon: float,
    delta: float,
    r: float = 2.0,
    Nshots: int = 100,
    nu: float = 8.0,
    rng: np.random.Generator | None = None,
    max_iters: int = 500,
) -> RunResult:
    """ChebAE (Rall-Fuller 2022, Section 3, Empirical Claim 18)."""
    if rng is None:
        rng = np.random.default_rng()

    T_bound = max(1, int(np.ceil(math.log(1.0/max(2*epsilon, 1e-30), r))))
    alpha_per_iter = delta / T_bound

    # Max CP error (worst case) at Nshots
    eps_pmax = clopper_pearson_max_halfwidth(Nshots, alpha_per_iter)

    amin, amax = 0.0, 1.0
    nheads, nflips = 0, 0
    d = 1
    total_queries = 0
    max_depth = 0
    n_iter = 0

    for it in range(max_iters):
        n_iter += 1

        d_new = _find_next_cheb(amin, amax)
        if d_new >= r * d:
            d = d_new
            nheads, nflips = 0, 0

        # Early vs late test
        denom = abs(T(d, amax) - T(d, amin))
        interval_width = amax - amin
        late = False
        if denom > 1e-15:
            if eps_pmax * (interval_width / denom) <= epsilon * nu:
                late = True

        if late:
            n = 1
        else:
            n = Nshots
        h = sample_Td_squared(d, a_true, n, rng)
        nheads += h
        nflips += n
        total_queries += n * d
        max_depth = max(max_depth, d)

        pmin, pmax = clopper_pearson(nheads, nflips, alpha_per_iter)
        try:
            new_amin, new_amax = _invert_TK_squared_interval(d, amin, amax, pmin, pmax)
        except Exception:
            new_amin, new_amax = amin, amax

        new_amin = max(new_amin, amin)
        new_amax = min(new_amax, amax)
        if new_amin > new_amax:
            new_amin, new_amax = amin, amax

        amin, amax = new_amin, new_amax

        if amax - amin < 2*epsilon:
            a_hat = 0.5*(amin + amax)
            return RunResult(a_hat, amin, amax, total_queries, max_depth, n_iter,
                             abs(a_hat - a_true) <= epsilon)

    a_hat = 0.5*(amin + amax)
    return RunResult(a_hat, amin, amax, total_queries, max_depth, n_iter,
                     abs(a_hat - a_true) <= epsilon)


if __name__ == "__main__":
    # quick sanity check
    rng = np.random.default_rng(42)
    a = 0.5
    eps = 1e-3
    delta = 0.05

    print("Sanity: single run each")
    r_iqae = iqae(a, eps, delta, rng=rng)
    print(f"  IQAE  : a_hat={r_iqae.a_hat:.6f}  QΠ={r_iqae.total_queries_Zpi:>8d}  iters={r_iqae.n_iters}  correct={r_iqae.correct}")

    r_cheb = chebae(a, eps, delta, rng=rng)
    print(f"  ChebAE: a_hat={r_cheb.a_hat:.6f}  QΠ={r_cheb.total_queries_Zpi:>8d}  iters={r_cheb.n_iters}  correct={r_cheb.correct}")
