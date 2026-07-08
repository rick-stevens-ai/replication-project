"""
Independent replication of Grover (2005) "A different kind of quantum search",
arXiv:quant-ph/0503205.

Implements:
  - Standard Grover amplitude amplification (phase-π selective inversions):
        Q = -I_s U^-1 I_t U    applied to |s> (or, equivalently, U I_s U^-1 I_t U
        with global signs consistent with the paper's convention).
  - New π/3 phase-shift recursion:
        U_0 = U
        U_{m+1} = U_m R_s U_m^dagger R_t U_m
    where R_s, R_t apply phase e^{iπ/3} to |s> and |t> respectively (identity elsewhere).

Prediction of the paper (Section 4):
    ||U_{m,ts}||^2 = 1 - epsilon^(3^m),  where epsilon = 1 - ||U_ts||^2.
    Number of queries q_m of the operator U grows as q_m = (3^{m+1} - 1)/2
    (each recursion triples query count from the m-1 level + 1 more base call in the sandwich).
    In terms of queries:  ||U_{m,ts}||^2 = 1 - epsilon^(2 q_m + 1).

We reproduce, for a small database N=16 with M=1 marked element:
  * The success probability trajectory of standard Grover vs iteration k (oscillates).
  * The success probability at each recursion level m of the π/3 algorithm
    (monotone convergence, exact triple-exponent scaling of the failure probability).

We test the formal identity  P_success(m) = 1 - (1 - P_0)^(3^m)  where P_0 = ||U_ts||^2
by direct statevector simulation of the recursively-constructed operator U_m.

Everything is pure numpy statevector — no external quantum backend needed. This is
correct because the paper's algorithm and its analysis are dimension-independent; the
2D subspace argument only requires exact linear algebra.

Author: Kukla, 2026-07-06
"""
from __future__ import annotations
import json
import os
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


HERE = Path(__file__).resolve().parent
EVIDENCE = HERE.parent / "report" / "evidence"
EVIDENCE.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------------
# Operator constructors
# ------------------------------------------------------------------

def hadamard(n: int) -> np.ndarray:
    """N=2^n dimensional Walsh-Hadamard operator."""
    H1 = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
    W = H1
    for _ in range(n - 1):
        W = np.kron(W, H1)
    return W


def phase_shift(N: int, index: int, phi: float) -> np.ndarray:
    """R_x: apply e^{i phi} to |index>, identity elsewhere."""
    R = np.eye(N, dtype=complex)
    R[index, index] = np.exp(1j * phi)
    return R


def selective_inversion(N: int, index: int) -> np.ndarray:
    """I_x: apply -1 to |index>, identity elsewhere. Equivalent to phi = pi."""
    return phase_shift(N, index, np.pi)


# ------------------------------------------------------------------
# Algorithms
# ------------------------------------------------------------------

def standard_grover_trajectory(n: int, target: int, n_iters: int):
    """Standard Grover amplitude amplification on N=2^n starting from |0>.
    Returns list of success probabilities P(target) after k = 0, 1, ..., n_iters
    applications of Q = U I_s U^dagger I_t U, where U = W (Hadamard).

    We follow the textbook Grover operator on |s> = W|0> (uniform superposition):
        G = W I_0 W I_t     (this is the standard form).
    Equivalently G = (2|s><s| - I) O_t.
    """
    N = 2 ** n
    W = hadamard(n)
    I0 = selective_inversion(N, 0)   # phase flip |0>
    It = selective_inversion(N, target)

    # Grover iterate
    G = W @ I0 @ W @ It
    # Note: many sign conventions differ by a global -1, which does not affect
    # measurement probabilities. This convention matches Nielsen & Chuang and
    # the paper's amplitude-amplification Q.

    s = W @ np.eye(N, dtype=complex)[:, 0]  # |s> = W|0>

    probs = []
    state = s.copy()
    probs.append(abs(state[target]) ** 2)
    for _ in range(n_iters):
        state = G @ state
        probs.append(abs(state[target]) ** 2)
    return probs


def pi3_recursion_operator(U: np.ndarray, R_s: np.ndarray, R_t: np.ndarray, m: int):
    """Build U_m by explicit recursion (Eq. 3 in the paper).

    U_0 = U
    U_{m+1} = U_m R_s U_m^dagger R_t U_m

    Returns U_m.
    """
    Um = U.copy()
    for _ in range(m):
        Umd = Um.conj().T
        Um = Um @ R_s @ Umd @ R_t @ Um
    return Um


def query_count(m: int) -> int:
    """Number of applications of the base operator U inside U_m.

    q_0 = 1
    q_{m+1} = 3 * q_m  (three U_m's in the sandwich)
    => q_m = 3^m
    But each U_m includes both U and U^dagger applications; total *oracle* calls
    on the base level is 3^m calls to U plus interleaved (3^m - 1)/2 calls to U^dagger
    when we unroll to base level. In the paper's convention (Section 4), the base
    query count is q_m = (3^{m+1} - 1)/2 (counting BOTH U and U^dagger, since each is
    one oracle call). We report both, but the theoretical prediction the paper
    states is: failure probability epsilon^(3^m) after level m.
    """
    return 3 ** m


# ------------------------------------------------------------------
# Experiment
# ------------------------------------------------------------------

def main():
    n = 4                     # 4 qubits, N=16
    N = 2 ** n
    target = 5                # arbitrary marked state
    print(f"[run] N={N}, target index={target}, single marked element.")

    # --- Standard Grover ---
    n_iters = 12
    grover_probs = standard_grover_trajectory(n, target, n_iters)
    print("\nStandard Grover success probabilities vs iteration k:")
    for k, p in enumerate(grover_probs):
        print(f"  k={k:2d}  P(target)={p:.6f}")

    # --- π/3 recursion ---
    W = hadamard(n)
    R_s = phase_shift(N, 0, np.pi / 3)      # |s> corresponds to |0> here (before W applied)
    R_t = phase_shift(N, target, np.pi / 3)

    # In the paper, R_s acts on the "source" state used inside the sandwich
    # (see Eq. 1: U R_s U^dagger R_t U|s>). The relevant "source" for the
    # W-based construction is |0>, since U = W maps |0> -> uniform superposition.
    # So R_s = phase shift on |0>, R_t = phase shift on target. This matches
    # the "New algorithm" paragraph in Section 5 of the paper.

    U = W
    # Base success probability = |<t|U|0>|^2 = 1/N for uniform superposition
    P0_theory = 1.0 / N
    Uts = (U @ np.eye(N, dtype=complex)[:, 0])[target]
    P0 = abs(Uts) ** 2
    epsilon0 = 1 - P0
    print(f"\nBase probability P0 = |U_ts|^2 = {P0:.6f} (theory 1/N = {P0_theory:.6f})")
    print(f"Base epsilon = 1 - P0 = {epsilon0:.6f}")

    print("\nπ/3 phase-shift recursion (measured vs theoretical prediction 1 - eps^(3^m)):")
    m_max = 4
    pi3_results = []
    zero_ket = np.eye(N, dtype=complex)[:, 0]
    for m in range(m_max + 1):
        Um = pi3_recursion_operator(U, R_s, R_t, m)
        state = Um @ zero_ket
        p_measured = abs(state[target]) ** 2
        p_theory = 1 - epsilon0 ** (3 ** m)
        q = query_count(m)
        print(f"  m={m}  q(U-calls)={q:5d}  P(target)={p_measured:.10f}   "
              f"1 - eps^(3^m) = {p_theory:.10f}   |diff|={abs(p_measured - p_theory):.2e}")
        pi3_results.append({
            "m": m,
            "queries_U_calls": q,
            "P_target_measured": float(p_measured),
            "P_target_theoretical": float(p_theory),
            "abs_error": float(abs(p_measured - p_theory)),
        })

    # --- Save numeric evidence ---
    numeric = {
        "N": N,
        "target_index": target,
        "M_marked": 1,
        "base_probability_P0": float(P0),
        "base_epsilon": float(epsilon0),
        "standard_grover_probs": [float(x) for x in grover_probs],
        "standard_grover_max_prob": float(max(grover_probs)),
        "standard_grover_argmax_iter": int(np.argmax(grover_probs)),
        "pi3_recursion": pi3_results,
    }
    out_json = EVIDENCE / "numeric_results.json"
    out_json.write_text(json.dumps(numeric, indent=2))
    print(f"\n[save] numeric results -> {out_json}")

    # --- Figure: probability trajectory ---
    fig, ax = plt.subplots(figsize=(9, 5.5))
    k_vals = np.arange(len(grover_probs))
    ax.plot(k_vals, grover_probs, "o-", color="#1f77b4", label="Standard Grover  (oscillates)")
    ax.axhline(1.0, ls=":", color="gray", alpha=0.5)

    # π/3 vs number of queries (U-calls), plotted on same iteration axis (approx.)
    # Show as steps at query count.
    q_vals = [r["queries_U_calls"] for r in pi3_results]
    p_vals = [r["P_target_measured"] for r in pi3_results]
    ax.plot(q_vals, p_vals, "s--", color="#d62728", markersize=10,
            label=r"$\pi/3$ recursion  (monotone $\to 1$)")

    for m, q, p in zip(range(m_max + 1), q_vals, p_vals):
        ax.annotate(f"m={m}", (q, p), textcoords="offset points", xytext=(6, -14),
                    fontsize=9, color="#d62728")

    ax.set_xlabel("Number of oracle queries (calls to $U$)")
    ax.set_ylabel(r"Success probability $P(|t\rangle)$")
    ax.set_title(f"Grover (2005) π/3-phase-shift recursion vs standard Grover\n"
                 f"N={N}, single marked element (target index {target})")
    ax.set_xlim(-0.5, max(q_vals) + 2)
    ax.set_ylim(-0.02, 1.05)
    ax.grid(alpha=0.3)
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig_path = EVIDENCE / "fig_probability_trajectory.png"
    fig.savefig(fig_path, dpi=160)
    print(f"[save] figure -> {fig_path}")
    plt.close(fig)

    # --- Figure 2: log-scale failure probability, showing triple-exponent scaling ---
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ms = np.arange(m_max + 1)
    fail_meas = [1 - r["P_target_measured"] for r in pi3_results]
    fail_theory = [epsilon0 ** (3 ** m) for m in ms]
    ax.semilogy(ms, fail_meas, "s-", color="#d62728", markersize=10, label="measured $1 - P$")
    ax.semilogy(ms, fail_theory, "x--", color="black", markersize=12,
                label=r"$\epsilon^{3^m}$ prediction")
    ax.set_xlabel("Recursion level $m$")
    ax.set_ylabel("Failure probability (log scale)")
    ax.set_title(f"π/3 recursion: failure probability collapses as $\\epsilon^{{3^m}}$\n"
                 f"(base $\\epsilon$ = 1 - 1/N = {epsilon0:.4f})")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig2_path = EVIDENCE / "fig_failure_scaling.png"
    fig.savefig(fig2_path, dpi=160)
    print(f"[save] figure -> {fig2_path}")
    plt.close(fig)

    # --- Monotonicity sanity check ---
    diffs = np.diff([r["P_target_measured"] for r in pi3_results])
    all_monotone = bool((diffs >= -1e-12).all())
    print(f"\n[check] π/3 recursion monotone non-decreasing? {all_monotone}")
    (EVIDENCE / "monotonicity_check.txt").write_text(
        f"successive P(target) differences: {diffs.tolist()}\n"
        f"monotone_non_decreasing = {all_monotone}\n"
    )

    print("\nDone.")


if __name__ == "__main__":
    main()
