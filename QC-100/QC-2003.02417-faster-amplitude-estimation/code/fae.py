"""Faster Amplitude Estimation (FAE) — Nakaji 2020, arXiv:2003.02417 Algorithm 1.

Uses the real Grover operator Q built in oracle.py to compute the exact
probability of the good state after Q^m, then samples N_shot Bernoulli draws
(this is what a real statevector simulator would give for a projective measurement).

Norac accounting (per paper Section 2.3): number of Q calls.
  - Each COS(m, N_shot) call uses N_shot copies of Q^m|Psi'>, i.e. m*N_shot applications of Q.
  - We tally these across the whole run.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable, List, Optional, Tuple

import numpy as np

from oracle import exact_prob_good_after_Qm, theta_true


# ---------- Chernoff interval per paper eq (8) ---------- #

def chernoff_interval(c_m: float, N_shot: int, delta_c: float) -> Tuple[float, float]:
    """Given estimate c_m, return (c_min, c_max) confidence interval."""
    half = math.sqrt(math.log(2.0 / delta_c) * 12.0 / N_shot)
    c_max = min(1.0, c_m + half)
    c_min = max(-1.0, c_m - half)
    return c_min, c_max


def cos_estimate(a: float, m: int, N_shot: int, rng: np.random.Generator) -> float:
    """COS(m, N_shot): Nshot Bernoulli measurements of state after Q^m, return c_m = 1 - 2*N11/Nshot.

    Uses exact statevector-derived probability of |11>, then samples binomially.
    """
    p_good = exact_prob_good_after_Qm(a, m)
    N11 = int(rng.binomial(N_shot, p_good))
    return 1.0 - 2.0 * (N11 / N_shot)


def _atan_extended(s: float, c: float) -> float:
    """Extended arctangent from paper eq (9). We use math.atan2 which is equivalent."""
    if c == 0.0 and s == 0.0:
        return 0.0
    return math.atan2(s, c)


# ---------- FAE Algorithm 1 ---------- #

@dataclass
class FAEResult:
    theta_hat: float
    a_hat: float
    norac: int  # total Q calls
    ell: int
    j0: int
    reached_second_stage: bool
    theta_true: float
    a_true: float
    theta_error: float
    a_error: float


def run_fae(a: float, ell: int, delta_c: float = 0.01, seed: int = 0) -> FAEResult:
    """Run Faster Amplitude Estimation per Nakaji 2020 Algorithm 1."""
    rng = np.random.default_rng(seed)

    N_shot_1st = int(math.ceil(1944.0 * math.log(2.0 / delta_c)))
    N_shot_2nd = int(math.ceil(972.0 * math.log(2.0 / delta_c)))

    theta_min = 0.0
    theta_max = 0.252
    first_stage = True
    j0 = ell
    nu = 0.0
    norac = 0

    for j in range(1, ell + 1):
        m = 2 ** (j - 1)

        if first_stage:
            c = cos_estimate(a, m, N_shot_1st, rng)
            norac += m * N_shot_1st
            c_min, c_max = chernoff_interval(c, N_shot_1st, delta_c)

            # theta_max, theta_min per eq (10)
            theta_max = math.acos(c_min) / (2 ** (j + 1) + 2)
            theta_min = math.acos(c_max) / (2 ** (j + 1) + 2)

            if (2 ** (j + 1)) * theta_max >= (3.0 * math.pi / 8.0) and j < ell:
                j0 = j
                nu = (2 ** j0) * (theta_max + theta_min)  # estimate of 2^(j0+1) theta
                first_stage = False

        else:
            # Second stage
            c_a = cos_estimate(a, m, N_shot_2nd, rng)
            norac += m * N_shot_2nd

            m_extra = 2 ** (j - 1) + 2 ** (j0 - 1)  # index for extra cos measurement
            c_b = cos_estimate(a, m_extra, N_shot_2nd, rng)
            norac += m_extra * N_shot_2nd

            sin_nu = math.sin(nu)
            if abs(sin_nu) < 1e-12:
                # Degenerate; skip update (rare)
                continue
            s = (c_a * math.cos(nu) - c_b) / sin_nu
            # Clip to [-1, 1] for safety
            s = max(-1.0, min(1.0, s))
            c_clipped = max(-1.0, min(1.0, c_a))

            rho = _atan_extended(s, c_clipped)  # in (-pi, pi]

            # Determine nj: paper eq (25)
            # nj = floor( (1/2pi) * ((2^(j+1)+2)*theta_max_{j-1} - rho + pi/3) )
            n_j = math.floor(((2 ** (j + 1) + 2) * theta_max - rho + math.pi / 3.0) / (2.0 * math.pi))

            theta_min = (2.0 * math.pi * n_j + rho - math.pi / 3.0) / (2 ** (j + 1) + 2)
            theta_max = (2.0 * math.pi * n_j + rho + math.pi / 3.0) / (2 ** (j + 1) + 2)

    theta_hat = 0.5 * (theta_min + theta_max)
    # a = 4 sin(theta) since we attenuated
    a_hat = 4.0 * math.sin(theta_hat)

    th_t = theta_true(a)
    return FAEResult(
        theta_hat=theta_hat,
        a_hat=a_hat,
        norac=norac,
        ell=ell,
        j0=j0,
        reached_second_stage=(j0 < ell),
        theta_true=th_t,
        a_true=a,
        theta_error=abs(theta_hat - th_t),
        a_error=abs(a_hat - a),
    )


if __name__ == "__main__":
    for a in [0.1, 0.2, 0.3, 0.4]:
        for ell in [3, 4, 5, 6]:
            res = run_fae(a, ell, delta_c=0.01, seed=42)
            print(f"a={a} ell={ell}  a_hat={res.a_hat:.6f}  err={res.a_error:.4e}  "
                  f"Norac={res.norac:.3e}  j0={res.j0}  2ndStage={res.reached_second_stage}")
        print()
