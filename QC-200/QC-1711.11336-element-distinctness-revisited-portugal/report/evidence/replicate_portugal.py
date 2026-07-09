#!/usr/bin/env python3
"""
Independent replication of Portugal (2017) "Element Distinctness Revisited"
   arXiv:1711.11336v3, 13 Jun 2018.

Reproducible core (what the paper actually claims, per pdftotext of the PDF):
  - The element k-distinctness quantum algorithm (Ambainis-style, restated in
    the staggered-quantum-walk framework on graph Gamma).
  - The algorithm's dynamics is INVARIANT on a (2k+1)-dimensional subspace
    spanned by the vectors |eta_l^j> (Eq. 7). Everything can therefore be
    computed with (2k+1)x(2k+1) matrices u_alpha, u_beta, R.
  - Optimal main-block repetitions:      t1 = round(pi*sqrt(r)/4)
                                          r  = round(N^(k/(k+1))).
  - Optimal walk steps in subroutine:    t2 = round(pi*sqrt(r)/(2*sqrt(k))).
  - Success probability psucc -> 1 - O(r^{-1/k}) as N grows.
  - For k=2: query count = O(N^(2/3)), which is Ambainis' seminal result.

Reproduction strategy:
  For k = 2 (standard element-distinctness), we build u_alpha, u_beta on the
  5-dimensional subspace using Eqs. (8) and (9) from the paper, build the
  reduced conditional-phase-flip R = I - 2 |k,0><k,0| (Eq. 10), build the
  initial state |psi_0> using Eq. (11), and simulate the full algorithm
  |psi_final> = (u_beta u_alpha)^{t2} R  applied  t1  times.

  We record:
    - success probability at each of several N values,
    - t1(N), t2(N) and the total query count Q(N) = r + t1*t2 (approximately;
      paper says "r + pi^2 r / (4 sqrt(k))" for the O() estimate),
    - the empirical log-log slope of Q vs N (should approach 2/3).

  We also implement the classical O(N^2) brute-force baseline to confirm
  correctness of the "problem instance": each random list has exactly one
  collision pair, and the brute-force baseline finds it.

The (2k+1)-reduction is the mathematically correct simulation for this
algorithm: the algorithm exactly preserves the subspace, so simulating the
5-dim reduction is IDENTICAL to running the full 2^m-qubit circuit for
purposes of computing success probability. This is the whole point of the
paper's Theorem 3.1 (Section 3) and is what makes the classical simulation
tractable at arbitrary N (rather than being limited to tiny N by the
combinatorial explosion of the full C(N,r)*(N-r)*M^{r+1} Hilbert space).
"""

from __future__ import annotations

import json
import math
import time
from pathlib import Path
from typing import Any

import numpy as np

RNG = np.random.default_rng(20260705)
OUT = Path(__file__).resolve().parent


# ---------------------------------------------------------------------------
# 1) Problem-instance generator + classical baseline
# ---------------------------------------------------------------------------


def make_instance_with_one_collision(N: int, rng: np.random.Generator = RNG) -> np.ndarray:
    """Return a length-N int array with EXACTLY ONE colliding index pair (k=2)."""
    # Use a large enough alphabet that random samples are distinct with high prob,
    # then plant exactly one collision.
    alphabet = 10 * N * N
    while True:
        a = rng.integers(low=0, high=alphabet, size=N)
        if len(set(a.tolist())) == N:
            break  # start from all-distinct
    i, j = rng.choice(N, size=2, replace=False)
    a[j] = a[i]
    return a


def classical_bruteforce(a: np.ndarray) -> tuple[int, int] | None:
    """O(N^2) baseline: return (i, j) with i < j such that a[i] == a[j], else None."""
    N = len(a)
    for i in range(N):
        for j in range(i + 1, N):
            if a[i] == a[j]:
                return (i, j)
    return None


# ---------------------------------------------------------------------------
# 2) Reduced (2k+1)-dim matrices u_alpha, u_beta, R (Portugal 2017, Eqs. 8-10)
# ---------------------------------------------------------------------------


def basis_index(l: int, j: int, k: int) -> int:
    """Map (l, j) with 0 <= l <= k, j in {0,1}, excluding (l=k, j=1), to 0..2k."""
    # ordering: (0,0),(0,1),(1,0),(1,1),...,(k-1,0),(k-1,1),(k,0)  -> 2k+1 vecs
    if l == k and j == 1:
        raise ValueError("state (l=k, j=1) is excluded (eta_k^1 is empty)")
    return 2 * l + j


def _delta(a: int, b: int) -> int:
    return 1 if a == b else 0


def build_u_alpha(N: int, r: int, k: int) -> np.ndarray:
    """Matrix elements from Eq. (8) of Portugal (2017)."""
    d = 2 * k + 1
    A = np.zeros((d, d), dtype=np.float64)
    valid = [(l, j) for l in range(k + 1) for j in (0, 1) if not (l == k and j == 1)]
    for lp, jp in valid:
        ip = basis_index(lp, jp, k)
        for l, j in valid:
            i = basis_index(l, j, k)
            # first term: (-1)^j (1 - 2(k-l)/(N-r)) delta_{ll'} delta_{jj'}
            term1 = 0.0
            if _delta(l, lp) and _delta(j, jp):
                term1 = ((-1) ** j) * (1.0 - 2.0 * (k - l) / (N - r))
            # second term: 2 sqrt(k-l)/(N-r) sqrt(1 - (k-l)/(N-r))
            #              * delta_{ll'} * delta_{j xor 1, j'}
            term2 = 0.0
            if _delta(l, lp) and _delta(j ^ 1, jp):
                q = (k - l) / (N - r)
                if q >= 0 and (1.0 - q) >= 0:
                    term2 = 2.0 * math.sqrt(max(q, 0.0)) * math.sqrt(max(1.0 - q, 0.0))
            A[ip, i] = term1 + term2
    return A


def build_u_beta(N: int, r: int, k: int) -> np.ndarray:
    """Matrix elements from Eq. (9) of Portugal (2017).

    Element:
        <l', j'| u_beta | l, j> = (-1)^j (1 - 2(l+j)/(r+1)) delta_{ll'} delta_{jj'}
          + 2 sqrt((l+j)/(r+1)) sqrt(1 - (l+j)/(r+1))
            * delta_{l - (-1)^{j'}, l'} * delta_{1 xor j, j'}
    """
    d = 2 * k + 1
    B = np.zeros((d, d), dtype=np.float64)
    valid = [(l, j) for l in range(k + 1) for j in (0, 1) if not (l == k and j == 1)]
    for lp, jp in valid:
        ip = basis_index(lp, jp, k)
        for l, j in valid:
            i = basis_index(l, j, k)
            # first term (diagonal in (l, j))
            term1 = 0.0
            if _delta(l, lp) and _delta(j, jp):
                term1 = ((-1) ** j) * (1.0 - 2.0 * (l + j) / (r + 1))
            # second term (off-diagonal). Reading Eq. (9) LITERALLY as
            #   delta_{l - (-1)^{j'}, l'} * delta_{1 xor j, j'}
            # gives a NON-symmetric (and hence non-unitary) matrix, which
            # contradicts the paper's own statement that u_beta is unitary AND
            # Hermitian. The unique index rule that makes u_beta Hermitian and
            # respects (l+j) = (l'+j') (required for the same q = (l+j)/(r+1)
            # in both directions of the reflection) is:
            #     l' = l - (-1)^{j}   (i.e. l' = l-1 if j=0, l' = l+1 if j=1)
            # This is the symmetric reading that matches the coloring-of-the
            # -clique-graph tessellation Eq. (3-4). Almost certainly a typo
            # (j' vs. j) in the printed equation of arXiv:1711.11336v3.
            term2 = 0.0
            l_target = l - ((-1) ** j)  # l - (-1)^{j}  (see note above)
            if _delta(l_target, lp) and _delta(1 ^ j, jp):
                q = (l + j) / (r + 1)
                if 0 <= q <= 1:
                    term2 = 2.0 * math.sqrt(q) * math.sqrt(1.0 - q)
            B[ip, i] = term1 + term2
    return B


def build_R(k: int) -> np.ndarray:
    """Reduced conditional-phase-flip R = I - 2 |k,0><k,0|  (Eq. 10)."""
    d = 2 * k + 1
    R = np.eye(d, dtype=np.float64)
    ik0 = basis_index(k, 0, k)
    R[ik0, ik0] = -1.0
    return R


def build_psi0(N: int, r: int, k: int) -> np.ndarray:
    """Reduced initial state (Eq. 11):
       |psi_0> = (1/sqrt(C(N,r)(N-r))) sum_{l,j} sqrt(|eta_l^j|) |l, j>.
    |eta_l^j| = C(k,l) C(N-k, r-l) (N-r-k+l)   for j=0
             = C(k,l) C(N-k, r-l) (k-l)        for j=1  (with l != k)

    Computed in log-space to avoid overflow for large N.
    """
    from math import lgamma

    def log_comb(n: int, k_: int) -> float:
        if k_ < 0 or k_ > n:
            return float("-inf")
        return lgamma(n + 1) - lgamma(k_ + 1) - lgamma(n - k_ + 1)

    d = 2 * k + 1
    log_total = log_comb(N, r) + math.log(N - r)
    v = np.zeros(d, dtype=np.float64)
    for l in range(k + 1):
        for j in (0, 1):
            if l == k and j == 1:
                continue
            if l > k or r - l < 0 or r - l > N - k:
                continue
            log_eta = log_comb(k, l) + log_comb(N - k, r - l)
            if j == 0:
                if N - r - k + l <= 0:
                    continue
                log_eta += math.log(N - r - k + l)
            else:
                if k - l <= 0:
                    continue
                log_eta += math.log(k - l)
            # amplitude = sqrt(|eta|) / sqrt(total) = exp(0.5 * (log|eta| - log_total))
            v[basis_index(l, j, k)] = math.exp(0.5 * (log_eta - log_total))
    return v


# ---------------------------------------------------------------------------
# 3) Full algorithm on the reduced subspace
# ---------------------------------------------------------------------------


def r_optimal(N: int, k: int) -> int:
    """r = nearest integer to N^{k/(k+1)}.  (Paper text, top of Sec 2.1.)"""
    r = int(round(N ** (k / (k + 1))))
    # Ensure r is in a valid range (must have some marked structure)
    r = max(r, k + 1)  # need at least k+1 for a k-collision to fit in S U {y}
    r = min(r, N - k - 1)  # need k < N - r
    return r


def t1_optimal(r: int) -> int:
    return max(1, int(round(math.pi * math.sqrt(r) / 4.0)))


def t2_optimal(r: int, k: int) -> int:
    return max(1, int(round(math.pi * math.sqrt(r) / (2.0 * math.sqrt(k)))))


def run_algorithm(
    N: int,
    k: int = 2,
    t1: int | None = None,
    t2: int | None = None,
) -> dict[str, Any]:
    """Run the reduced-subspace simulation for element k-distinctness.

    Returns a dict with:
      N, k, r, t1, t2, queries_estimate,
      psucc_final           -- probability of measuring a marked S at step t1,
      psucc_by_step         -- list of probabilities at steps 0..t1 (main-block iters),
      phi_k, lambda_theory  -- key spectral quantities for cross-check.
    """
    r = r_optimal(N, k)
    if t1 is None:
        t1 = t1_optimal(r)
    if t2 is None:
        t2 = t2_optimal(r, k)

    A = build_u_alpha(N, r, k)
    B = build_u_beta(N, r, k)
    R = build_R(k)

    # Sanity-check unitarity (real symmetric orthogonal? actually u_alpha, u_beta
    # are supposed to be unitary+hermitian on the reduced subspace).
    dev_A = float(np.max(np.abs(A @ A.T - np.eye(A.shape[0]))))
    dev_B = float(np.max(np.abs(B @ B.T - np.eye(B.shape[0]))))

    U = B @ A  # one step of the quantum walk (u = u_beta u_alpha)
    U_t2 = np.linalg.matrix_power(U, t2)
    step_op = U_t2 @ R  # one main-block iteration

    psi = build_psi0(N, r, k)
    norm0 = float(np.dot(psi, psi))
    ik0 = basis_index(k, 0, k)
    psucc_by_step = [float(psi[ik0] ** 2)]  # amplitude on |k, 0> => probability |k,0>
    for _ in range(t1):
        psi = step_op @ psi
        psucc_by_step.append(float(psi[ik0] ** 2))

    # phi_k from Eq. (19)
    cos_phi_k = 1.0 - 2.0 * k * (N - k + 1) / ((r + 1) * (N - r))
    phi_k = math.acos(max(-1.0, min(1.0, cos_phi_k)))

    return {
        "N": N,
        "k": k,
        "r": r,
        "t1": t1,
        "t2": t2,
        "queries_estimate": r + t1 * t2,   # r for setup + t1*t2 oracle-heavy steps
        "psucc_final": psucc_by_step[-1],
        "psucc_max_seen": max(psucc_by_step),
        "psucc_argmax": int(np.argmax(psucc_by_step)),
        "psi0_norm2": norm0,
        "u_alpha_unitary_dev": dev_A,
        "u_beta_unitary_dev": dev_B,
        "cos_phi_k": cos_phi_k,
        "phi_k": phi_k,
    }


# ---------------------------------------------------------------------------
# 4) Sweep + log-log fit
# ---------------------------------------------------------------------------


def main() -> None:
    print("=" * 78)
    print("Portugal (2017) 'Element Distinctness Revisited' — independent replication")
    print("arXiv:1711.11336v3   Renato Portugal   LNCC")
    print("=" * 78)

    # Confirm problem generator + classical baseline for N in {6, 9, 12}
    print("\n[Instance + classical baseline check]")
    baseline_results = []
    for N in (6, 9, 12):
        a = make_instance_with_one_collision(N)
        pair = classical_bruteforce(a)
        assert pair is not None, f"Baseline failed to find planted collision for N={N}"
        i, j = pair
        assert a[i] == a[j]
        baseline_results.append({
            "N": N,
            "a": a.tolist(),
            "collision_pair": [int(i), int(j)],
            "collision_value": int(a[i]),
        })
        print(f"  N={N:3d}  planted (i,j)={pair}  value=a[{i}]=a[{j}]={a[i]}  OK")

    # Reduced-subspace simulation across a range of N (k=2 is the classic case).
    print("\n[Reduced-subspace simulation of the element 2-distinctness algorithm]")
    print(f"  {'N':>4}  {'r':>4}  {'t1':>3}  {'t2':>3}  {'Q_est':>6}  "
          f"{'psucc':>8}  {'psucc_max':>10}  {'argmax_t':>8}")
    sweep = []
    N_values = [6, 9, 12, 15, 20, 30, 50, 80, 120, 200, 400, 800, 1500, 3000]
    t0 = time.time()
    for N in N_values:
        res = run_algorithm(N, k=2)
        sweep.append(res)
        print(f"  {res['N']:>4}  {res['r']:>4}  {res['t1']:>3}  {res['t2']:>3}  "
              f"{res['queries_estimate']:>6}  {res['psucc_final']:>8.4f}  "
              f"{res['psucc_max_seen']:>10.4f}  {res['psucc_argmax']:>8}")
    wall = time.time() - t0
    print(f"  ({len(N_values)} points, {wall:.2f}s wall)")

    # Log-log regressions (only from N>=15 -- small N is in the pre-asymptotic
    # regime, r_optimal clamps by min(N-k-1, ...), t1/t2 rounding is coarse).
    fit_pts = [x for x in sweep if x["N"] >= 15]
    logN = np.log(np.array([x["N"] for x in fit_pts]))
    log_r = np.log(np.array([x["r"] for x in fit_pts]))
    log_t1 = np.log(np.array([x["t1"] for x in fit_pts]))
    log_t2 = np.log(np.array([x["t2"] for x in fit_pts]))
    log_Q = np.log(np.array([x["queries_estimate"] for x in fit_pts]))
    slope_r, _ = np.polyfit(logN, log_r, 1)
    slope_t1, _ = np.polyfit(logN, log_t1, 1)
    slope_t2, _ = np.polyfit(logN, log_t2, 1)
    slope_Q, intercept_Q = np.polyfit(logN, log_Q, 1)
    slopes = {
        "log_r_vs_log_N": float(slope_r),          # expected ~ k/(k+1) = 2/3
        "log_t1_vs_log_N": float(slope_t1),        # ~ (1/2) * (2/3) = 1/3
        "log_t2_vs_log_N": float(slope_t2),        # ~ 1/3
        "log_Q_vs_log_N":  float(slope_Q),         # ~ 2/3 (dominant: r + t1*t2)
        "log_Q_intercept": float(intercept_Q),
    }
    print("\n[Log-log slopes (fit for N >= 15)]")
    print(f"  slope of r  vs N   = {slope_r:.4f}   (theory k/(k+1) = 0.6667)")
    print(f"  slope of t1 vs N   = {slope_t1:.4f}   (theory 1/2 * k/(k+1) = 0.3333)")
    print(f"  slope of t2 vs N   = {slope_t2:.4f}   (theory 1/2 * k/(k+1) = 0.3333)")
    print(f"  slope of Q  vs N   = {slope_Q:.4f}   (theory k/(k+1) = 0.6667)")

    # Success-probability asymptote: paper says psucc -> 1 - O(r^{-1/k}).
    print("\n[Success probability asymptotics]")
    for res in sweep[-6:]:
        theory_gap = res["r"] ** (-1.0 / res["k"])
        print(f"  N={res['N']:>4}  psucc={res['psucc_final']:.4f}  "
              f"1-psucc={1 - res['psucc_final']:.4f}  "
              f"r^{{-1/k}}={theory_gap:.4f}   ratio={(1 - res['psucc_final']) / theory_gap:.3f}")

    # Save the full sweep + classical baseline as JSON evidence
    payload = {
        "paper": {
            "arxiv_id": "1711.11336v3",
            "title": "Element Distinctness Revisited",
            "author": "Renato Portugal",
            "institution": "National Laboratory of Scientific Computing (LNCC), Petropolis, Brazil",
            "email": "portugal@lncc.br",
            "date": "June 15, 2018",
        },
        "reproduction_approach": (
            "Simulated the reduced (2k+1)-dim invariant subspace of the algorithm "
            "using the matrices u_alpha and u_beta (Eqs. 8, 9), the reduced "
            "conditional-phase-flip R (Eq. 10), and the initial state |psi_0> "
            "(Eq. 11). This is mathematically identical to the full 2^m-qubit "
            "circuit for the purposes of computing success probability, per the "
            "invariant-subspace argument of Theorem 3.1."
        ),
        "classical_baseline": baseline_results,
        "sweep": sweep,
        "loglog_fit": slopes,
        "seed": 20260705,
        "walltime_seconds": wall,
    }
    with open(OUT / "results.json", "w") as f:
        json.dump(payload, f, indent=2)
    print(f"\nSaved: {OUT / 'results.json'}")

    # Also produce a compact CSV of the sweep
    csv_path = OUT / "sweep.csv"
    with open(csv_path, "w") as f:
        f.write("N,k,r,t1,t2,queries_estimate,psucc_final,psucc_max,psucc_argmax\n")
        for x in sweep:
            f.write(
                f"{x['N']},{x['k']},{x['r']},{x['t1']},{x['t2']},"
                f"{x['queries_estimate']},{x['psucc_final']:.8f},"
                f"{x['psucc_max_seen']:.8f},{x['psucc_argmax']}\n"
            )
    print(f"Saved: {csv_path}")


if __name__ == "__main__":
    main()
