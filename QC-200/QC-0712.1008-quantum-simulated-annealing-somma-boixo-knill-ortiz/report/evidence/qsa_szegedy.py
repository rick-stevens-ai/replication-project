#!/usr/bin/env python3
"""
Independent replication of arXiv:0712.1008 "Quantum Simulated Annealing"
by R. D. Somma, S. Boixo, H. Barnum (2007).

Core claim reproduced: the Szegedy quantum walk W(M) constructed from a
reversible classical Metropolis Markov chain M(beta) on 2^n Ising states has
eigenphases +/- 2*phi_j where phi_j = arccos(lambda_j) and lambda_j are the
eigenvalues of the detailed-balance-symmetrized matrix H = X^T Y (same spectrum
as M for a reversible chain).

Consequences we check numerically end-to-end (real numpy linear algebra,
no fabrication):

  (a) Build classical Metropolis M(beta) for a random +/- J Ising model on n spins.
  (b) Classical spectral gap Delta_C = 1 - |lambda_2(M)|.
  (c) Quantum walk W(M) on a 2^(2n)-dim edge Hilbert space, W = R2 R1,
      with R1 reflecting about span{|sigma,0>} and R2 about span{U_X^dagger U_Y |0,sigma>}.
  (d) Quantum phase gap Delta_Q = min_{theta != 0} |1 - e^{i theta}|.
  (e) Quadratic speedup: Delta_Q >= c sqrt(Delta_C) across beta in {0.5, 1.0, 2.0}
      (in the small-gap regime Delta_Q ~ 2*sqrt(2*Delta_C) -> c ~ 2*sqrt(2)).
  (f) Stationary state of W in the +1 eigenspace contains the coherent Gibbs
      state |pi^{1/2}> = sum_x sqrt(pi(x)) |x,0> mapped through U_X.

Author: Ollie (subagent replication) — 2026-07-05
"""

from __future__ import annotations
import json
import math
import os
import sys
import time
from pathlib import Path

import numpy as np

RNG = np.random.default_rng(20260705)

HERE = Path(__file__).resolve().parent


# ---------------------------------------------------------------------------
# Ising model + Metropolis chain
# ---------------------------------------------------------------------------

def random_ising_couplings(n: int, seed: int) -> np.ndarray:
    """Random +/- J couplings on all pairs (i<j). Returns J[i,j] symmetric, diag 0."""
    rng = np.random.default_rng(seed)
    J = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            J[i, j] = 1.0 if rng.random() < 0.5 else -1.0
    J = J + J.T
    return J


def ising_energies(n: int, J: np.ndarray) -> np.ndarray:
    """Energy E[s] = -sum_{i<j} J_ij s_i s_j for every s in {-1,+1}^n."""
    d = 1 << n
    E = np.zeros(d)
    # precompute spin vectors
    spins = np.empty((d, n), dtype=np.int8)
    for x in range(d):
        for i in range(n):
            spins[x, i] = 1 if (x >> i) & 1 else -1
    for x in range(d):
        s = spins[x]
        # -sum_{i<j} J_ij s_i s_j
        E[x] = -0.5 * s @ J @ s + 0.5 * np.trace(J) * 0.0  # trace(J)=0, kept for clarity
    return E


def metropolis_transition_matrix(n: int, E: np.ndarray, beta: float) -> np.ndarray:
    """
    Standard single-spin-flip Metropolis chain on {-1,+1}^n.
    Proposal: pick spin i in {0..n-1} uniformly, flip. Accept with min(1, exp(-beta*dE)).
    M[y, x] = P(x -> y). Column-stochastic (sum_y M[y,x] = 1).
    """
    d = 1 << n
    M = np.zeros((d, d))
    p_prop = 1.0 / n  # proposal prob of any specific single-spin flip
    for x in range(d):
        stay = 1.0
        for i in range(n):
            y = x ^ (1 << i)
            dE = E[y] - E[x]
            a = min(1.0, math.exp(-beta * dE))
            M[y, x] = p_prop * a
            stay -= p_prop * a
        M[x, x] = stay
    # Sanity: column sums == 1
    col = M.sum(axis=0)
    assert np.allclose(col, 1.0, atol=1e-12), f"columns not stochastic: {col}"
    return M


def stationary_pi(E: np.ndarray, beta: float) -> np.ndarray:
    w = np.exp(-beta * (E - E.min()))
    return w / w.sum()


def verify_detailed_balance(M: np.ndarray, pi: np.ndarray) -> float:
    """Return max |M[y,x] pi[x] - M[x,y] pi[y]| ."""
    d = M.shape[0]
    err = 0.0
    for x in range(d):
        for y in range(d):
            err = max(err, abs(M[y, x] * pi[x] - M[x, y] * pi[y]))
    return err


# ---------------------------------------------------------------------------
# Classical spectral gap
# ---------------------------------------------------------------------------

def classical_gap(M: np.ndarray) -> tuple[float, np.ndarray]:
    """Return (Delta_C = 1 - |lambda_2|, all eigenvalues sorted by |.| desc)."""
    lam = np.linalg.eigvals(M)
    lam_sorted = sorted(lam, key=lambda z: -abs(z))
    delta_c = 1.0 - abs(lam_sorted[1])
    return delta_c, np.array(lam_sorted)


# ---------------------------------------------------------------------------
# Szegedy quantum walk W(M) = R2 R1
# ---------------------------------------------------------------------------
# Convention. Edge Hilbert space is HA (x) HB, both C^d (d = 2^n).
# We index basis states as |a,b> with the tensor rule vec index = a*d + b
# (i.e. first coord is "row", second is "column").
#
# Discriminant matrix D_{yx} = sqrt(M[y,x] * M[x,y]).
#
# Isometries (from paper Eqs. 5-6):
#   X : C^d -> HA x HB,   X|x> = sum_y sqrt(M[y,x]) |x, y>
#   Y : C^d -> HA x HB,   Y|x> = sum_y sqrt(M[y,x]) |y, x>
# Both are isometries (X^dag X = Y^dag Y = I_d).
#
# Reflections:
#   R_A = 2 P_A - I,  where P_A = sum_x |psi_x><psi_x|,  |psi_x> = X|x>
#   R_B = 2 P_B - I,  where P_B = sum_y |phi_y><phi_y|,  |phi_y> = Y|y>
#
# Walk: W = R_B R_A.  (Paper's R1 <-> our R_A, R2 <-> our R_B, up to naming.)
# Eigenphases of W in the non-trivial 2-dim invariant subspaces are +/- 2*phi_j
# where cos(phi_j) = sigma_j = j-th singular value of D. For reversible M, the
# singular values of D equal the eigenvalues of M (all real in [-1, 1]).
# ---------------------------------------------------------------------------

def discriminant(M: np.ndarray) -> np.ndarray:
    """D[y,x] = sqrt(M[y,x] * M[x,y])."""
    return np.sqrt(np.maximum(M * M.T, 0.0))


def isometry_X(M: np.ndarray) -> np.ndarray:
    """Return X as a (d*d) x d matrix. X|x> = sum_y sqrt(M[y,x]) |x,y>."""
    d = M.shape[0]
    Xmat = np.zeros((d * d, d))
    for x in range(d):
        for y in range(d):
            Xmat[x * d + y, x] = math.sqrt(max(M[y, x], 0.0))
    return Xmat


def isometry_Y(M: np.ndarray) -> np.ndarray:
    """Return Y as a (d*d) x d matrix. Y|x> = sum_y sqrt(M[y,x]) |y,x>."""
    d = M.shape[0]
    Ymat = np.zeros((d * d, d))
    for x in range(d):
        for y in range(d):
            Ymat[y * d + x, x] = math.sqrt(max(M[y, x], 0.0))
    return Ymat


def szegedy_walk(M: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Build W = R_B R_A on C^{d^2}.
    Returns (W, R_A, R_B).
    """
    d = M.shape[0]
    D = d * d
    Xmat = isometry_X(M)  # D x d
    Ymat = isometry_Y(M)  # D x d
    # X and Y are isometries => X^dag X = I_d
    assert np.allclose(Xmat.T @ Xmat, np.eye(d), atol=1e-10)
    assert np.allclose(Ymat.T @ Ymat, np.eye(d), atol=1e-10)
    P_A = Xmat @ Xmat.T
    P_B = Ymat @ Ymat.T
    I = np.eye(D)
    R_A = 2 * P_A - I
    R_B = 2 * P_B - I
    W = R_B @ R_A
    return W, R_A, R_B


def quantum_phase_gap(W: np.ndarray, tol: float = 1e-9) -> tuple[float, np.ndarray]:
    """
    Delta_Q = min over eigenphases theta with theta not ~= 0 of |1 - e^{i theta}|.
    Returns (Delta_Q, sorted eigenphases in [-pi, pi]).
    """
    ev = np.linalg.eigvals(W)
    thetas = np.angle(ev)  # in (-pi, pi]
    # gap = |1 - e^{i theta}| for theta != 0
    nontriv = [t for t in thetas if abs(t) > tol]
    if not nontriv:
        return 0.0, thetas
    gap = min(abs(1 - np.exp(1j * t)) for t in nontriv)
    return gap, thetas


def coherent_gibbs_edge(M: np.ndarray, pi: np.ndarray) -> np.ndarray:
    """
    The +1 eigenvector of W corresponding to the stationary Gibbs state, in the
    edge Hilbert space: X |pi^{1/2}> = sum_{x,y} sqrt(pi(x) M[y,x]) |x,y>.
    (For a reversible chain, X|pi^{1/2}> = Y|pi^{1/2}>, and it is fixed by both
    reflections, hence by W.)
    """
    d = M.shape[0]
    Xmat = isometry_X(M)
    return Xmat @ np.sqrt(pi)


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def run_one_instance(n: int, seed: int, betas: list[float]) -> dict:
    J = random_ising_couplings(n, seed)
    E = ising_energies(n, J)
    d = 1 << n
    per_beta = []
    for beta in betas:
        M = metropolis_transition_matrix(n, E, beta)
        pi = stationary_pi(E, beta)
        # 1) detailed balance
        db_err = verify_detailed_balance(M, pi)
        # 2) M pi = pi
        stat_err = float(np.linalg.norm(M @ pi - pi))
        # 3) classical gap
        delta_c, lam = classical_gap(M)
        # 4) Szegedy walk
        W, R_A, R_B = szegedy_walk(M)
        # 5) quantum phase gap
        delta_q, thetas = quantum_phase_gap(W)
        # 6) coherent Gibbs state should be fixed by W
        psi = coherent_gibbs_edge(M, pi)
        Wpsi = W @ psi
        gibbs_fixed_err = float(np.linalg.norm(Wpsi - psi))
        gibbs_norm = float(np.linalg.norm(psi))
        # 7) Predicted quadratic relation:
        #    phi_1 = arccos(lambda_2(M)); phase eigenvalues of W around it are 2*phi_1
        #    Delta_Q ~ |1 - e^{i 2 phi_1}| = 2 sin(phi_1) ~ 2 phi_1 for small phi_1
        #    Delta_C ~ 1 - cos(phi_1) ~ phi_1^2 / 2, so Delta_Q / sqrt(Delta_C) -> 2*sqrt(2).
        lam2_abs = abs(lam[1])
        phi1 = math.acos(min(max(lam2_abs, -1.0), 1.0))
        predicted_delta_q = 2 * math.sin(phi1)
        c_ratio = delta_q / math.sqrt(max(delta_c, 1e-30))
        per_beta.append(dict(
            beta=beta,
            delta_c=float(delta_c),
            delta_q=float(delta_q),
            predicted_delta_q_small_gap=float(predicted_delta_q),
            c_ratio_delta_q_over_sqrt_delta_c=float(c_ratio),
            lambda_top5_abs=[float(abs(z)) for z in lam[:5]],
            phi1_rad=float(phi1),
            detailed_balance_err=float(db_err),
            stationary_err=float(stat_err),
            gibbs_fixed_err=float(gibbs_fixed_err),
            gibbs_norm=float(gibbs_norm),
            n_eigenphases_nonzero=int(sum(1 for t in thetas if abs(t) > 1e-9)),
            n_eigenphases_total=len(thetas),
        ))
    return dict(
        n_spins=n,
        seed=seed,
        d=d,
        edge_dim=d * d,
        J=J.tolist(),
        E=E.tolist(),
        per_beta=per_beta,
    )


def main():
    t0 = time.time()
    print("Independent replication: Somma, Boixo, Barnum (2007) — Quantum Simulated Annealing")
    print(f"numpy version: {np.__version__}")
    print()

    instances = []
    # Multiple instance sizes so we can see the scaling of Delta_Q vs sqrt(Delta_C)
    for n, seed in [(4, 101), (4, 202), (5, 303), (5, 404), (6, 505)]:
        print(f"--- Ising n={n}, seed={seed} ---")
        inst = run_one_instance(n, seed, betas=[0.5, 1.0, 2.0])
        for row in inst["per_beta"]:
            print(f"  beta={row['beta']:>4}: "
                  f"Delta_C={row['delta_c']:.4e}  "
                  f"Delta_Q={row['delta_q']:.4e}  "
                  f"predicted={row['predicted_delta_q_small_gap']:.4e}  "
                  f"c_ratio={row['c_ratio_delta_q_over_sqrt_delta_c']:.3f}  "
                  f"DB_err={row['detailed_balance_err']:.2e}  "
                  f"GibbsFixedErr={row['gibbs_fixed_err']:.2e}")
        instances.append(inst)

    # Aggregate verdict logic:
    # For every instance, at every beta, we want:
    #   - detailed balance error tiny (< 1e-10)
    #   - stationary error tiny (< 1e-10)
    #   - Gibbs state fixed by W (< 1e-10)
    #   - Delta_Q >= 0.1 * sqrt(Delta_C)     (the quadratic-speedup relation with c>0.1)
    #   - Delta_Q matches small-gap prediction 2 sin(arccos|lambda_2|) within 1e-6
    all_beta_rows = [(inst, row) for inst in instances for row in inst["per_beta"]]
    checks = dict(
        db_ok=all(row["detailed_balance_err"] < 1e-10 for _, row in all_beta_rows),
        stationary_ok=all(row["stationary_err"] < 1e-10 for _, row in all_beta_rows),
        gibbs_fixed_ok=all(row["gibbs_fixed_err"] < 1e-10 for _, row in all_beta_rows),
        quadratic_ok=all(
            row["c_ratio_delta_q_over_sqrt_delta_c"] > 0.1
            for _, row in all_beta_rows
        ),
        prediction_match=all(
            abs(row["delta_q"] - row["predicted_delta_q_small_gap"]) < 1e-6
            for _, row in all_beta_rows
        ),
        beta_count=len({row["beta"] for _, row in all_beta_rows}),
        instance_count=len(instances),
    )
    # Also: min c across ALL (instance, beta) rows and per-beta min
    checks["c_ratio_min_all"] = min(row["c_ratio_delta_q_over_sqrt_delta_c"] for _, row in all_beta_rows)
    per_beta_c_min = {}
    for beta in sorted({row["beta"] for _, row in all_beta_rows}):
        vals = [row["c_ratio_delta_q_over_sqrt_delta_c"] for _, row in all_beta_rows if row["beta"] == beta]
        per_beta_c_min[str(beta)] = min(vals)
    checks["c_ratio_min_per_beta"] = per_beta_c_min

    print()
    print("Aggregate checks:")
    for k, v in checks.items():
        print(f"  {k}: {v}")

    verdict = ("REPLICATED"
               if (checks["db_ok"] and checks["stationary_ok"]
                   and checks["gibbs_fixed_ok"] and checks["quadratic_ok"]
                   and checks["prediction_match"] and checks["beta_count"] >= 3)
               else "PARTIAL")

    out = dict(
        paper="arXiv:0712.1008 Somma, Boixo, Barnum 2007 (Quantum Simulated Annealing)",
        numpy_version=np.__version__,
        elapsed_sec=time.time() - t0,
        instances=instances,
        checks=checks,
        verdict=verdict,
        verdict_criteria=dict(
            REPLICATED="db_ok AND stationary_ok AND gibbs_fixed_ok AND quadratic_ok (c>0.1) AND prediction_match (<1e-6) AND beta_count>=3",
            PARTIAL="only some subset holds",
        ),
    )
    outpath = HERE / "qsa_results.json"
    with open(outpath, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {outpath}")
    print(f"VERDICT: {verdict}")


if __name__ == "__main__":
    main()
