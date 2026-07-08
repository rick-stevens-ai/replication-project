#!/usr/bin/env python
"""
Independent replication of Suzuki et al. 2019 (arXiv:1904.10246)
"Amplitude Estimation without Phase Estimation" - MLAE.

Reproduces Fig. 2 central claim: error-vs-#queries scaling for
  - Classical random sampling (m_k = 0 for all k)   -> expected slope -0.5
  - LIS (m_k = k)                                    -> expected slope -0.75
  - EIS (m_k = 2^{k-1}, m_0 = 0)                     -> expected slope -1.0 (Heisenberg)

Design:
  Amplitude a encoded via 1-qubit A = R_y(2*theta_a), theta_a = arcsin(sqrt(a)).
  Then |Psi> = A|0> = sqrt(1-a)|0> + sqrt(a)|1>. Good state = |1>.
  Grover/amplitude-amplification operator Q on 1 qubit for this A is
        Q = -A S_0 A^{-1} S_chi
  where S_chi flips sign of |1> (good) and S_0 flips sign of |0>.
  After m applications of Q on |Psi> the probability of measuring |1> is
        p_m(theta) = sin^2((2m+1)*theta_a)   (Brassard et al. 2002)
  This is exactly the statistical model used in Suzuki et al. Eq. (5).

We run the *real* Qiskit circuit at each m via qiskit-aer, collect h_k hits out
of N_shot shots, then maximize the joint log-likelihood
        L(theta) = sum_k [ h_k log(sin^2((2m_k+1)theta)) +
                          (N_k - h_k) log(cos^2((2m_k+1)theta)) ]
via brute-force fine grid + local golden-section polish (mirrors the paper's
"modified brute-force search").

Repeats T=200 trials per (M, sequence) point, computes RMSE across trials,
and least-squares fits log(err) vs log(Nq) for slope gamma.

Runtime target: minutes on CPU. All sim; no fabrication.
"""

import argparse
import json
import math
import os
import sys
import time
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


# ---------------------------------------------------------------------------
# Circuit construction
# ---------------------------------------------------------------------------

def build_A(theta_a: float) -> QuantumCircuit:
    """|Psi> = A|0> = cos(theta)|0> + sin(theta)|1>. So R_y(2*theta_a)."""
    qc = QuantumCircuit(1, name="A")
    qc.ry(2.0 * theta_a, 0)
    return qc


def build_Q(theta_a: float) -> QuantumCircuit:
    """
    Grover iterate Q = -A S_0 A^dagger S_chi  on 1 qubit.
    S_chi = Z on qubit 0 (flip sign of |1> = good state).
    S_0   = 2|0><0| - I  (up to global -1) implemented as X Z X.
    Overall global phase (-1) is unobservable but does not matter for
    probability sin^2((2m+1)theta).
    """
    qc = QuantumCircuit(1, name="Q")
    # S_chi: flip sign of |1> good state
    qc.z(0)
    # A^dagger
    qc.ry(-2.0 * theta_a, 0)
    # S_0: 2|0><0| - I  =  X Z X  (up to global phase)
    qc.x(0)
    qc.z(0)
    qc.x(0)
    # A
    qc.ry(2.0 * theta_a, 0)
    return qc


def build_measure_circuit(theta_a: float, m: int) -> QuantumCircuit:
    """Full circuit: A followed by m applications of Q, then measure."""
    qc = QuantumCircuit(1, 1)
    qc.compose(build_A(theta_a), qubits=[0], inplace=True)
    Q = build_Q(theta_a)
    for _ in range(m):
        qc.compose(Q, qubits=[0], inplace=True)
    qc.measure(0, 0)
    return qc


# ---------------------------------------------------------------------------
# Sampling from real Aer simulator (with transpile cache)
# ---------------------------------------------------------------------------

_TQC_CACHE: dict = {}

def get_transpiled(sim: AerSimulator, theta_a: float, m: int):
    """Cache transpiled circuits keyed by (theta_a rounded, m). Transpile
    dominates runtime otherwise; theta_a is fixed within a run so this is
    safe and preserves 'real qiskit-aer simulation of the real circuit'."""
    key = (round(theta_a, 12), m)
    tqc = _TQC_CACHE.get(key)
    if tqc is None:
        qc = build_measure_circuit(theta_a, m)
        tqc = transpile(qc, sim, optimization_level=0)
        _TQC_CACHE[key] = tqc
    return tqc


def run_shots(sim: AerSimulator, theta_a: float, m: int, n_shots: int,
              seed: int) -> int:
    """Return number of '1' outcomes out of n_shots for circuit A Q^m."""
    tqc = get_transpiled(sim, theta_a, m)
    result = sim.run(tqc, shots=n_shots, seed_simulator=seed).result()
    counts = result.get_counts()
    return counts.get('1', 0)


# ---------------------------------------------------------------------------
# Maximum likelihood estimator
# ---------------------------------------------------------------------------

def neg_log_likelihood(theta, ms, hs, ns):
    """
    Combined negative log-likelihood over all rounds k.
    p_k(theta) = sin^2((2 m_k + 1) theta)
    L_k(h_k; theta) = p_k^h_k (1 - p_k)^(N_k - h_k)
    Total: sum_k [ h_k log(p_k) + (N_k - h_k) log(1 - p_k) ]
    """
    eps = 1e-15
    ll = 0.0
    for m, h, n in zip(ms, hs, ns):
        arg = (2 * m + 1) * theta
        p = math.sin(arg) ** 2
        if p < eps:
            p = eps
        elif p > 1 - eps:
            p = 1 - eps
        ll += h * math.log(p) + (n - h) * math.log(1 - p)
    return -ll


def mle_theta(ms, hs, ns, grid_n=4000):
    """
    Global max of joint likelihood by fine brute-force grid on theta in
    (0, pi/2), then a tight refinement grid around the best point.
    Returns theta_hat in (0, pi/2).
    """
    theta_grid = np.linspace(1e-6, math.pi / 2 - 1e-6, grid_n)
    best_ll = math.inf
    best_theta = theta_grid[0]
    for th in theta_grid:
        nll = neg_log_likelihood(th, ms, hs, ns)
        if nll < best_ll:
            best_ll = nll
            best_theta = th
    # Refine
    dtheta = math.pi / (2 * grid_n)
    fine = np.linspace(max(1e-9, best_theta - 4 * dtheta),
                       min(math.pi / 2 - 1e-9, best_theta + 4 * dtheta),
                       2000)
    for th in fine:
        nll = neg_log_likelihood(th, ms, hs, ns)
        if nll < best_ll:
            best_ll = nll
            best_theta = th
    return best_theta


# ---------------------------------------------------------------------------
# Sequences
# ---------------------------------------------------------------------------

def lis(M: int):
    """m_0=0, m_1=1, ..., m_M=M.  Number of rounds = M+1."""
    return [k for k in range(M + 1)]


def eis(M: int):
    """m_0=0, m_1=1, m_2=2, m_3=4, ..., m_M = 2^(M-1) for M>=1."""
    seq = [0]
    for k in range(1, M + 1):
        seq.append(2 ** (k - 1))
    return seq


def classical(M: int):
    """m_k = 0 for all k (classical sampling)."""
    return [0] * (M + 1)


def n_queries(seq, n_shot):
    return sum(n_shot * (2 * m + 1) for m in seq)


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def run_experiment(theta_a: float, a: float, sequence_name: str, seq_fn,
                   Ms, n_shot: int, n_trials: int, sim, base_seed: int):
    """Return dict with rows [M, Nq, RMSE_a, RMSE_theta, per-trial errors]."""
    rows = []
    for M in Ms:
        seq = seq_fn(M)
        Nq = n_queries(seq, n_shot)
        errors_a = []
        errors_theta = []
        t0 = time.time()
        for trial in range(n_trials):
            hs = []
            ns = []
            for k, m in enumerate(seq):
                seed = base_seed + 10007 * trial + 97 * k + hash(sequence_name) % 1000
                seed = seed & 0x7FFFFFFF
                h = run_shots(sim, theta_a, m, n_shot, seed)
                hs.append(h)
                ns.append(n_shot)
            theta_hat = mle_theta(seq, hs, ns)
            a_hat = math.sin(theta_hat) ** 2
            errors_a.append(a_hat - a)
            errors_theta.append(theta_hat - theta_a)
        errors_a = np.array(errors_a)
        errors_theta = np.array(errors_theta)
        rmse_a = float(np.sqrt(np.mean(errors_a ** 2)))
        rmse_theta = float(np.sqrt(np.mean(errors_theta ** 2)))
        elapsed = time.time() - t0
        rows.append({
            "M": M,
            "Nq": Nq,
            "n_shot": n_shot,
            "n_trials": n_trials,
            "sequence": sequence_name,
            "rmse_a": rmse_a,
            "rmse_theta": rmse_theta,
            "elapsed_s": elapsed,
        })
        print(f"    [{sequence_name} M={M:2d}] Nq={Nq:8d}  RMSE(a)={rmse_a:.4e}  "
              f"RMSE(theta)={rmse_theta:.4e}  ({elapsed:.1f}s)",
              flush=True)
    return rows


def fit_slope(rows, xkey="Nq", ykey="rmse_a"):
    xs = np.array([r[xkey] for r in rows], dtype=float)
    ys = np.array([r[ykey] for r in rows], dtype=float)
    if np.any(ys <= 0):
        mask = ys > 0
        xs, ys = xs[mask], ys[mask]
    logx = np.log10(xs)
    logy = np.log10(ys)
    slope, intercept = np.polyfit(logx, logy, 1)
    return float(slope), float(intercept)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--a", type=float, default=1.0/48.0,
                        help="Target amplitude a (default 1/48 as in paper Fig 2 lower-right)")
    parser.add_argument("--n-shot", type=int, default=100)
    parser.add_argument("--n-trials", type=int, default=200)
    parser.add_argument("--Ms-lis", type=int, nargs="+",
                        default=[3, 5, 8, 12, 16, 22, 30])
    parser.add_argument("--Ms-eis", type=int, nargs="+",
                        default=[3, 4, 5, 6, 7, 8, 9])
    parser.add_argument("--Ms-classical", type=int, nargs="+",
                        default=[3, 8, 22, 60, 160, 400])
    parser.add_argument("--seed", type=int, default=20260703)
    parser.add_argument("--out", type=str, required=True)
    args = parser.parse_args()

    a = args.a
    theta_a = math.asin(math.sqrt(a))
    print(f"Target a = {a:.6f}  theta_a = {theta_a:.6f} rad", flush=True)
    sim = AerSimulator()

    all_rows = []

    print("[CLASSICAL] (m_k = 0)", flush=True)
    rows_c = run_experiment(theta_a, a, "classical", classical,
                            args.Ms_classical, args.n_shot, args.n_trials,
                            sim, args.seed)
    all_rows.extend(rows_c)

    print("[LIS]  m_k = k", flush=True)
    rows_l = run_experiment(theta_a, a, "LIS", lis,
                            args.Ms_lis, args.n_shot, args.n_trials,
                            sim, args.seed + 1)
    all_rows.extend(rows_l)

    print("[EIS]  m_k = 2^(k-1) for k>=1, m_0=0", flush=True)
    rows_e = run_experiment(theta_a, a, "EIS", eis,
                            args.Ms_eis, args.n_shot, args.n_trials,
                            sim, args.seed + 2)
    all_rows.extend(rows_e)

    # Slope fits (in a, as the paper reports "estimation error")
    slope_c, _ = fit_slope(rows_c)
    slope_l, _ = fit_slope(rows_l)
    slope_e, _ = fit_slope(rows_e)

    summary = {
        "a": a,
        "theta_a": theta_a,
        "n_shot": args.n_shot,
        "n_trials": args.n_trials,
        "slopes": {
            "classical": slope_c,
            "LIS": slope_l,
            "EIS": slope_e,
        },
        "paper_slopes_a=1/48": {
            "classical": -0.50,
            "LIS": -0.76,
            "EIS": -0.95,
        },
        "rows": all_rows,
    }

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w") as fh:
        json.dump(summary, fh, indent=2)

    print("\n=== SLOPES (log RMSE_a  vs  log Nq) ===")
    print(f"  Classical : ours = {slope_c:+.3f}   paper = -0.50")
    print(f"  LIS       : ours = {slope_l:+.3f}   paper = -0.76")
    print(f"  EIS       : ours = {slope_e:+.3f}   paper = -0.95 (Heisenberg ~= -1)")
    print(f"\nWrote {args.out}")


if __name__ == "__main__":
    main()
