"""
Independent replication of:
  Roland & Cerf, "Quantum Search by Local Adiabatic Evolution",
  arXiv:quant-ph/0107015 (2001).

Headline claim we test:
  With H(s) = (1-s) H0 + s Hm, H0 = I - |psi0><psi0|, Hm = I - |m><m|,
    LINEAR (global-adiabatic) schedule  s(t) = t/T   requires   T ~ N   to reach p_success >= 1/2
    LOCAL adiabatic schedule (Eq. 18)                 requires   T ~ sqrt(N)
  In log-log we expect slopes ~1.0 (linear) and ~0.5 (local).

Method:
  - Work in the 2D "Grover" invariant subspace {|m>, |psi0_perp>} (the dynamics stays here since
    H0 and Hm both preserve it and initial state |psi0> lies in it). This is exact and lets us
    integrate up to N = O(1e6) if we want; we still confirm the 2D reduction agrees with the full
    N-dim statevector at small N.

  - Integrate the Schrodinger equation with scipy.integrate.solve_ivp (RK45 / DOP853).

  - For each schedule and each N, find T_star = smallest T achieving p_success >= 0.5.
    Do a bisection on T over a broad bracket, using the analytical predictions as anchors.

  - Fit log T_star vs log N by least-squares -> slope.

Free tools only, no LLM calls.
"""

from __future__ import annotations

import json
import math
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


# ------------------------- 2D reduced dynamics -------------------------
# In the invariant subspace with basis |m> and |m_perp> (the normalized projection of |psi0>
# onto the orthogonal complement of |m>), we have:
#   |psi0>       = a|m> + b|m_perp>,  a = 1/sqrt(N),  b = sqrt(1 - 1/N)
#   H0 = I - |psi0><psi0|
#   Hm = I - |m><m|
# In the {|m>, |m_perp>} basis, H(s) = (1-s)H0 + s Hm is a 2x2 real symmetric matrix.
#
# Compute H0 and Hm in that basis explicitly.

def H_of_s_2d(s: float, N: int) -> np.ndarray:
    a = 1.0 / math.sqrt(N)           # <m|psi0>
    b = math.sqrt(1.0 - 1.0 / N)     # <m_perp|psi0>
    # |psi0><psi0| in basis {|m>,|m_perp>} =
    #   [[a^2, a*b],
    #    [a*b, b^2]]
    P0 = np.array([[a * a, a * b],
                   [a * b, b * b]], dtype=float)
    # |m><m| in basis {|m>,|m_perp>} = [[1,0],[0,0]]
    Pm = np.array([[1.0, 0.0],
                   [0.0, 0.0]], dtype=float)
    I = np.eye(2)
    return (1.0 - s) * (I - P0) + s * (I - Pm)


# Schedules ----------------------------------------------------------------
def schedule_linear(t: float, T: float, N: int) -> float:
    return min(1.0, max(0.0, t / T))


def schedule_local(t: float, T: float, N: int) -> float:
    """
    Invert Eq. (18) of Roland-Cerf:
      t = (N / (2 eps sqrt(N-1))) * [ arctan(sqrt(N-1)(2s-1)) + arctan(sqrt(N-1)) ]

    epsilon is chosen so that s(T) = 1 exactly. Setting s=1 in Eq.(18):
      T = (N / (2 eps sqrt(N-1))) * ( 2 arctan(sqrt(N-1)) )
    so
      eps = (N / (T sqrt(N-1))) * arctan(sqrt(N-1))

    Given T and N, compute eps, then invert to get s(t):
      arctan(sqrt(N-1)(2s-1)) = (2 eps sqrt(N-1) t)/N  -  arctan(sqrt(N-1))
      s = 0.5 + tan(...) / (2 sqrt(N-1))
    """
    if t <= 0.0:
        return 0.0
    if t >= T:
        return 1.0
    r = math.sqrt(N - 1.0)
    A = math.atan(r)
    eps = (N / (T * r)) * A
    arg = (2.0 * eps * r * t) / N - A
    s = 0.5 + math.tan(arg) / (2.0 * r)
    if s < 0.0:
        return 0.0
    if s > 1.0:
        return 1.0
    return s


# Schrodinger RHS ----------------------------------------------------------
def make_rhs_2d(N: int, T: float, schedule_fn):
    def rhs(t, y):
        s = schedule_fn(t, T, N)
        H = H_of_s_2d(s, N)
        # y = [re_a, im_a, re_b, im_b] representing psi = a|m> + b|m_perp>
        a = y[0] + 1j * y[1]
        b = y[2] + 1j * y[3]
        psi = np.array([a, b], dtype=complex)
        dpsi = -1j * (H @ psi)
        return [dpsi[0].real, dpsi[0].imag, dpsi[1].real, dpsi[1].imag]
    return rhs


def initial_state_2d(N: int) -> np.ndarray:
    a = 1.0 / math.sqrt(N)
    b = math.sqrt(1.0 - 1.0 / N)
    return np.array([a, 0.0, b, 0.0], dtype=float)


def success_prob(N: int, T: float, schedule: str,
                 rtol: float = 1e-9, atol: float = 1e-11,
                 method: str = "DOP853") -> float:
    if schedule == "linear":
        schedule_fn = schedule_linear
    elif schedule == "local":
        schedule_fn = schedule_local
    else:
        raise ValueError(schedule)

    rhs = make_rhs_2d(N, T, schedule_fn)
    y0 = initial_state_2d(N)
    # Use adaptive step; max_step keeps us from stepping over rapid s-variations near s=1/2 for local
    sol = solve_ivp(rhs, (0.0, T), y0, method=method, rtol=rtol, atol=atol,
                    max_step=T / 200.0, dense_output=False, t_eval=[T])
    y = sol.y[:, -1]
    a = y[0] + 1j * y[1]
    # |<m|psi(T)>|^2 = |a|^2
    return float(abs(a) ** 2)


# 2D vs full-N sanity check ------------------------------------------------
def full_state_check(N: int, T: float, schedule: str) -> float:
    """Do it in full N-dim Hilbert space (no reduction) to confirm the 2D reduction."""
    if schedule == "linear":
        schedule_fn = schedule_linear
    else:
        schedule_fn = schedule_local
    # Basis: computational basis, marked state = index 0
    m = 0
    psi0 = np.ones(N, dtype=complex) / math.sqrt(N)

    ket_m = np.zeros(N, dtype=complex); ket_m[m] = 1.0
    P0 = np.outer(psi0, psi0.conj())
    Pm = np.outer(ket_m, ket_m.conj())
    I = np.eye(N, dtype=complex)

    def rhs(t, y):
        s = schedule_fn(t, T, N)
        H = (1 - s) * (I - P0) + s * (I - Pm)
        dpsi = -1j * (H @ y)
        return dpsi

    sol = solve_ivp(rhs, (0.0, T), psi0, method="DOP853",
                    rtol=1e-9, atol=1e-11, max_step=T / 200.0, t_eval=[T])
    psi_T = sol.y[:, -1]
    return float(abs(psi_T[m]) ** 2)


# T* bisection -------------------------------------------------------------
@dataclass
class TStarResult:
    N: int
    schedule: str
    T_star: float
    p_at_T_star: float
    T_lo: float
    p_lo: float
    T_hi: float
    p_hi: float
    n_iter: int
    seconds: float


def find_T_star(N: int, schedule: str, target: float = 0.5,
                T_lo_init: float | None = None,
                T_hi_init: float | None = None,
                tol_rel: float = 0.01,
                max_iter: int = 30) -> TStarResult:
    """Bisection to find the smallest T such that p_success(T) >= target."""
    t_start = time.time()

    # Anchor initial bracket to the paper's own predictions with generous safety factors.
    if schedule == "linear":
        T_anchor = float(N)                # T ~ N / eps, eps ~ 1
        T_lo = T_lo_init if T_lo_init else 0.5 * T_anchor
        T_hi = T_hi_init if T_hi_init else 8.0 * T_anchor
    else:  # local
        T_anchor = (math.pi / 2.0) * math.sqrt(N)   # eps = 1
        T_lo = T_lo_init if T_lo_init else 0.25 * T_anchor
        T_hi = T_hi_init if T_hi_init else 8.0 * T_anchor

    p_lo = success_prob(N, T_lo, schedule)
    p_hi = success_prob(N, T_hi, schedule)

    # Expand upper bound if not yet succeeding
    grow_iters = 0
    while p_hi < target and grow_iters < 10:
        T_hi *= 2.0
        p_hi = success_prob(N, T_hi, schedule)
        grow_iters += 1
    # Contract lower bound if it already succeeds
    shrink_iters = 0
    while p_lo >= target and shrink_iters < 10:
        T_lo *= 0.5
        p_lo = success_prob(N, T_lo, schedule)
        shrink_iters += 1

    if p_hi < target:
        raise RuntimeError(f"Could not bracket target for N={N}, schedule={schedule}")

    n = 0
    while (T_hi - T_lo) / T_hi > tol_rel and n < max_iter:
        T_mid = 0.5 * (T_lo + T_hi)
        p_mid = success_prob(N, T_mid, schedule)
        if p_mid >= target:
            T_hi = T_mid
            p_hi = p_mid
        else:
            T_lo = T_mid
            p_lo = p_mid
        n += 1

    return TStarResult(
        N=N, schedule=schedule,
        T_star=T_hi, p_at_T_star=p_hi,
        T_lo=T_lo, p_lo=p_lo,
        T_hi=T_hi, p_hi=p_hi,
        n_iter=n, seconds=time.time() - t_start,
    )


# Main --------------------------------------------------------------------
def main(out_dir: str) -> None:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    log_path = out / "run.log"
    log_f = open(log_path, "w")

    def log(msg):
        print(msg)
        log_f.write(msg + "\n")
        log_f.flush()

    log(f"# Roland-Cerf 2001 replication run, python={sys.version.split()[0]}, numpy={np.__version__}")

    # ---- Sanity: 2D reduction matches full-N at small N ----
    log("\n## Sanity: full-N vs 2D reduced dynamics")
    log(f"{'N':>4} {'schedule':>8} {'T':>10} {'p_full':>10} {'p_2d':>10} {'|diff|':>10}")
    sanity = []
    for N in [4, 8, 16]:
        for schedule in ["linear", "local"]:
            T = (math.pi / 2.0) * math.sqrt(N) if schedule == "local" else 2.0 * N
            p_full = full_state_check(N, T, schedule)
            p_2d = success_prob(N, T, schedule)
            log(f"{N:>4} {schedule:>8} {T:>10.4f} {p_full:>10.6f} {p_2d:>10.6f} {abs(p_full-p_2d):>10.2e}")
            sanity.append({"N": N, "schedule": schedule, "T": T,
                           "p_full": p_full, "p_2d": p_2d,
                           "diff": abs(p_full - p_2d)})

    # ---- T_star vs N for both schedules ----
    Ns = [8, 16, 32, 64, 128, 256, 512, 1024, 2048]
    results = []
    log("\n## T* bisection")
    log(f"{'N':>6} {'schedule':>8} {'T*':>12} {'p@T*':>10} {'iters':>6} {'sec':>6}")
    for N in Ns:
        for schedule in ["linear", "local"]:
            res = find_T_star(N, schedule)
            log(f"{N:>6} {schedule:>8} {res.T_star:>12.4f} {res.p_at_T_star:>10.6f} {res.n_iter:>6d} {res.seconds:>6.2f}")
            results.append({
                "N": N, "schedule": schedule,
                "T_star": res.T_star, "p_at_T_star": res.p_at_T_star,
                "n_iter": res.n_iter, "seconds": res.seconds,
            })

    # ---- Log-log fit ----
    def fit_slope(pairs):
        x = np.log(np.array([p["N"] for p in pairs]))
        y = np.log(np.array([p["T_star"] for p in pairs]))
        # y = m x + c
        m, c = np.polyfit(x, y, 1)
        # residuals
        yhat = m * x + c
        ss_res = float(np.sum((y - yhat) ** 2))
        ss_tot = float(np.sum((y - y.mean()) ** 2))
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
        return float(m), float(c), r2

    lin = [r for r in results if r["schedule"] == "linear"]
    loc = [r for r in results if r["schedule"] == "local"]
    m_lin, c_lin, r2_lin = fit_slope(lin)
    m_loc, c_loc, r2_loc = fit_slope(loc)

    log("\n## Log-log fits: log(T*) = m log(N) + c")
    log(f"linear : slope = {m_lin:.4f}   intercept = {c_lin:.4f}   R^2 = {r2_lin:.5f}   (paper predicts ~1.0)")
    log(f"local  : slope = {m_loc:.4f}   intercept = {c_loc:.4f}   R^2 = {r2_loc:.5f}   (paper predicts ~0.5)")

    summary = {
        "paper": {
            "arxiv": "quant-ph/0107015",
            "authors": ["Jérémie Roland", "Nicolas J. Cerf"],
            "title": "Quantum Search by Local Adiabatic Evolution",
        },
        "sanity_2D_vs_full": sanity,
        "T_star_results": results,
        "fits": {
            "linear":  {"slope": m_lin, "intercept": c_lin, "R2": r2_lin,
                        "paper_predicted_slope": 1.0},
            "local":   {"slope": m_loc, "intercept": c_loc, "R2": r2_loc,
                        "paper_predicted_slope": 0.5},
        },
        "target_success_prob": 0.5,
        "Ns": Ns,
    }
    with open(out / "results.json", "w") as f:
        json.dump(summary, f, indent=2)
    log(f"\nwrote {out/'results.json'}")

    # ---- Verdict ----
    tol = 0.10
    ok_lin = abs(m_lin - 1.0) <= tol
    ok_loc = abs(m_loc - 0.5) <= tol
    verdict = "REPLICATED" if (ok_lin and ok_loc) else ("PARTIAL" if (ok_lin or ok_loc) else "CONTRADICTED")
    log(f"\nVERDICT: {verdict}  (linear slope err = {abs(m_lin-1.0):.3f}, local slope err = {abs(m_loc-0.5):.3f}, tol={tol})")

    log_f.close()


if __name__ == "__main__":
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "evidence"
    main(out_dir)
