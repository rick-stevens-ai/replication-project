#!/usr/bin/env python3
"""
Independent replication of Grover 2005, "A different kind of quantum search"
(arXiv:quant-ph/0503205).

Reproduces the paper's core quantitative claim:

  If |<t|U|s>|^2 = 1 - eps, then after applying the recursive
  pi/3-phase-shift transformation

     U_{m+1} = U_m R_s U_m^dagger R_t U_m,   U_0 = U

  we have  |<t|U_m|s>|^2 = 1 - eps^(3^m).

  (In terms of queries q_m = (3^(m+1)-1)/2, the failure prob
   scales as eps^(2 q_m + 1).)

We build the algorithm in Qiskit with a real statevector simulator and:

  1) Standard Grover on N=16 (n=4 qubits) with 1 marked state: show the
     success probability OSCILLATES with iteration count k = 1..12.
  2) Grover's pi/3 fixed-point recursion of depths m=0..3 for N=16: show
     the success probability MONOTONICALLY converges to 1 as
     P_m = 1 - eps^(3^m), where eps = 1 - 1/N.

  3) Repeat for N=64 (n=6 qubits) and confirm the pi/3 curve tracks
     1 - (63/64)^(3^m) to <1e-10 (statevector, no shot noise).

Outputs (all saved to the sibling directory):
  - standard_grover_probs.json
  - pi3_fixedpoint_probs.json
  - convergence.png       (P(k) vs k, standard Grover + pi/3 fixed-point)
  - convergence_data.csv
"""

import json
import os
import numpy as np
from math import pi, cos, sin
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, Operator

HERE = os.path.dirname(os.path.abspath(__file__))


# ---------- Building blocks ----------

def hadamard_all(qc: QuantumCircuit, n: int):
    for q in range(n):
        qc.h(q)


def phase_flip_on_state(n: int, target_index: int, phase: float) -> Operator:
    """Selective phase shift by `phase` on the computational-basis state
    `target_index` (of an n-qubit register). Returns a full 2^n x 2^n operator."""
    dim = 1 << n
    mat = np.eye(dim, dtype=complex)
    mat[target_index, target_index] = np.exp(1j * phase)
    return Operator(mat)


def build_U(n: int) -> Operator:
    """The paper's U = Walsh-Hadamard on n qubits (drives |0> -> |+>^n)."""
    qc = QuantumCircuit(n)
    hadamard_all(qc, n)
    return Operator(qc)


def apply_op(sv: Statevector, op: Operator) -> Statevector:
    return sv.evolve(op)


def marked_success_prob(sv: Statevector, target_index: int) -> float:
    amps = sv.data
    return float(np.abs(amps[target_index]) ** 2)


# ---------- Standard Grover with k oracle+diffusion iterations ----------

def standard_grover_prob(n: int, target_index: int, k_iters: int) -> float:
    """Statevector-exact success probability after k Grover iterations
    with a single marked state at index `target_index`. Grover iteration
    Q = -H^n R_0 H^n R_t (with R_t, R_0 = pi phase flip on |t>, |0>)."""
    dim = 1 << n
    U = build_U(n)  # Walsh-Hadamard
    Rt_pi = phase_flip_on_state(n, target_index, pi)
    R0_pi = phase_flip_on_state(n, 0, pi)

    # Initial state: |s> = H^n |0>
    sv = Statevector.from_int(0, dims=dim)
    sv = apply_op(sv, U)

    # One Grover step: R_t, then U R_0 U^dagger  ==  the standard oracle+diffusion.
    # (Global phases irrelevant to probabilities.)
    Udag = U.adjoint()
    for _ in range(k_iters):
        sv = apply_op(sv, Rt_pi)
        sv = apply_op(sv, Udag)
        sv = apply_op(sv, R0_pi)
        sv = apply_op(sv, U)

    return marked_success_prob(sv, target_index)


# ---------- pi/3 fixed-point recursion: U_{m+1} = U_m R_s U_m^dag R_t U_m ----------

def pi3_fixedpoint_U(n: int, target_index: int, m: int) -> Operator:
    """Recursively build U_m from the paper: U_0 = W (Walsh-Hadamard),
    U_{m+1} = U_m R_s U_m^dagger R_t U_m, with R_s, R_t = pi/3 phase shift
    on |s>=|0> and |t>=|target_index> respectively."""
    theta = pi / 3.0
    Rt = phase_flip_on_state(n, target_index, theta)
    Rs = phase_flip_on_state(n, 0, theta)

    U = build_U(n)  # U_0
    for _ in range(m):
        Udag = U.adjoint()
        # Order (right-to-left in matrix mult, so this reads U_m R_s U_m^dag R_t U_m
        # applied to |s> from the right):
        #    new = U_m * R_s * U_m^dag * R_t * U_m
        new_U = U.compose(Rt).compose(Udag).compose(Rs).compose(U)
        # Operator.compose(B) returns  B * self  (B applied after self) by default.
        # We want the composed operator that ACTS as U_m R_s U_m^dag R_t U_m,
        # which as a matrix is U_m R_s U_m^dag R_t U_m.
        # Applying `self.compose(B)` yields B @ self. So chain-of-composes gives
        # (((U).compose(Rt)).compose(Udag)).compose(Rs)).compose(U)
        # = U @ Rs @ Udag @ Rt @ U      as a matrix. ✓
        U = new_U
    return U


def pi3_fixedpoint_prob(n: int, target_index: int, m: int) -> float:
    dim = 1 << n
    U_m = pi3_fixedpoint_U(n, target_index, m)
    sv = Statevector.from_int(0, dims=dim)
    sv = apply_op(sv, U_m)
    return marked_success_prob(sv, target_index)


# ---------- Main experiment ----------

def main():
    results = {}

    # ---- N = 16, standard Grover oscillation ----
    n = 4
    N = 1 << n
    target = 5  # arbitrary marked index
    eps = 1.0 - 1.0 / N
    print(f"\n=== N={N}, target index {target}, eps=1-1/N={eps:.6f} ===")

    ks = list(range(0, 13))
    grover_probs = [standard_grover_prob(n, target, k) for k in ks]
    print("Standard Grover P(k):")
    for k, p in zip(ks, grover_probs):
        print(f"  k={k:2d}  P={p:.6f}")

    results["N16_standard_grover"] = {
        "k": ks, "P": grover_probs,
    }

    # ---- N = 16, pi/3 fixed-point recursion ----
    ms = [0, 1, 2, 3]
    pi3_probs = [pi3_fixedpoint_prob(n, target, m) for m in ms]
    pi3_theory = [1.0 - eps ** (3 ** m) for m in ms]
    print("\npi/3 fixed-point P(m):  (sim vs theory 1 - eps^(3^m))")
    for m, ps, pt in zip(ms, pi3_probs, pi3_theory):
        q = (3 ** (m + 1) - 1) // 2
        print(f"  m={m}  queries={q:3d}   sim P={ps:.10f}   theory P={pt:.10f}   diff={ps-pt:+.2e}")

    results["N16_pi3_fixedpoint"] = {
        "m": ms,
        "queries": [(3 ** (m + 1) - 1) // 2 for m in ms],
        "P_sim": pi3_probs,
        "P_theory": pi3_theory,
    }

    # ---- N = 64, pi/3 fixed-point recursion (bigger test of the 1 - eps^(3^m) law) ----
    n2 = 6
    N2 = 1 << n2
    target2 = 42
    eps2 = 1.0 - 1.0 / N2
    print(f"\n=== N={N2}, target index {target2}, eps=1-1/N={eps2:.6f} ===")

    ms2 = [0, 1, 2, 3]
    pi3_probs2 = [pi3_fixedpoint_prob(n2, target2, m) for m in ms2]
    pi3_theory2 = [1.0 - eps2 ** (3 ** m) for m in ms2]
    print("pi/3 fixed-point P(m):  (sim vs theory 1 - eps^(3^m))")
    for m, ps, pt in zip(ms2, pi3_probs2, pi3_theory2):
        q = (3 ** (m + 1) - 1) // 2
        print(f"  m={m}  queries={q:3d}   sim P={ps:.10f}   theory P={pt:.10f}   diff={ps-pt:+.2e}")

    results["N64_pi3_fixedpoint"] = {
        "m": ms2,
        "queries": [(3 ** (m + 1) - 1) // 2 for m in ms2],
        "P_sim": pi3_probs2,
        "P_theory": pi3_theory2,
    }

    # ---- Save JSON ----
    with open(os.path.join(HERE, "standard_grover_probs.json"), "w") as f:
        json.dump(results["N16_standard_grover"], f, indent=2)
    with open(os.path.join(HERE, "pi3_fixedpoint_probs.json"), "w") as f:
        json.dump({
            "N16": results["N16_pi3_fixedpoint"],
            "N64": results["N64_pi3_fixedpoint"],
        }, f, indent=2)

    # ---- Save CSV ----
    csv_path = os.path.join(HERE, "convergence_data.csv")
    with open(csv_path, "w") as f:
        f.write("algorithm,N,k_or_m,queries,P_sim,P_theory\n")
        for k, p in zip(ks, grover_probs):
            f.write(f"standard_grover,{N},{k},{k},{p:.10f},\n")
        for m, ps, pt in zip(ms, pi3_probs, pi3_theory):
            q = (3 ** (m + 1) - 1) // 2
            f.write(f"pi3_fixedpoint,{N},{m},{q},{ps:.10f},{pt:.10f}\n")
        for m, ps, pt in zip(ms2, pi3_probs2, pi3_theory2):
            q = (3 ** (m + 1) - 1) // 2
            f.write(f"pi3_fixedpoint,{N2},{m},{q},{ps:.10f},{pt:.10f}\n")

    # ---- Plot ----
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))
    ax = axes[0]
    ax.plot(ks, grover_probs, "o-", label="standard Grover (N=16)")
    ax.axhline(1.0, color="gray", lw=0.5, ls="--")
    ax.set_xlabel("Grover iteration count k")
    ax.set_ylabel("P(mark)")
    ax.set_title("Standard Grover: oscillatory in k")
    ax.set_ylim(-0.02, 1.05)
    ax.legend()

    ax = axes[1]
    ax.plot([q for q in results["N16_pi3_fixedpoint"]["queries"]],
            pi3_probs, "o-", label=r"$\pi/3$ fixed-point sim (N=16)")
    ax.plot([q for q in results["N16_pi3_fixedpoint"]["queries"]],
            pi3_theory, "x--", label=r"theory $1-\epsilon^{3^m}$ (N=16)")
    ax.plot([q for q in results["N64_pi3_fixedpoint"]["queries"]],
            pi3_probs2, "s-", label=r"$\pi/3$ fixed-point sim (N=64)")
    ax.plot([q for q in results["N64_pi3_fixedpoint"]["queries"]],
            pi3_theory2, "+--", label=r"theory $1-\epsilon^{3^m}$ (N=64)")
    ax.set_xscale("log")
    ax.set_xlabel("queries q_m = (3^(m+1)-1)/2  (log scale)")
    ax.set_ylabel("P(mark)")
    ax.set_title(r"$\pi/3$ fixed-point: monotonic convergence to 1")
    ax.set_ylim(-0.02, 1.05)
    ax.legend(loc="lower right")

    fig.suptitle("Grover 2005 (quant-ph/0503205) — replication of pi/3 fixed-point search")
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "convergence.png"), dpi=140)

    # ---- Machine-checkable pass/fail ----
    max_diff_N16 = max(abs(ps - pt) for ps, pt in zip(pi3_probs, pi3_theory))
    max_diff_N64 = max(abs(ps - pt) for ps, pt in zip(pi3_probs2, pi3_theory2))
    monotonic_N16 = all(pi3_probs[i + 1] >= pi3_probs[i] - 1e-12
                        for i in range(len(pi3_probs) - 1))
    monotonic_N64 = all(pi3_probs2[i + 1] >= pi3_probs2[i] - 1e-12
                        for i in range(len(pi3_probs2) - 1))
    grover_oscillates = any(grover_probs[i + 1] < grover_probs[i] - 1e-6
                            for i in range(len(grover_probs) - 1))

    verdict = {
        "N16_max_theory_diff": max_diff_N16,
        "N64_max_theory_diff": max_diff_N64,
        "N16_pi3_monotonic": monotonic_N16,
        "N64_pi3_monotonic": monotonic_N64,
        "standard_grover_oscillates": grover_oscillates,
        "pass_criteria": {
            "theory_match_tol": 1e-10,
            "N16_pi3_matches_theory_to_tol": max_diff_N16 < 1e-10,
            "N64_pi3_matches_theory_to_tol": max_diff_N64 < 1e-10,
            "N16_pi3_monotonic": monotonic_N16,
            "N64_pi3_monotonic": monotonic_N64,
            "standard_grover_oscillates": grover_oscillates,
        },
    }
    verdict["OVERALL_PASS"] = all([
        max_diff_N16 < 1e-10,
        max_diff_N64 < 1e-10,
        monotonic_N16,
        monotonic_N64,
        grover_oscillates,
    ])

    with open(os.path.join(HERE, "verdict.json"), "w") as f:
        json.dump(verdict, f, indent=2)

    print("\n=== VERDICT ===")
    print(json.dumps(verdict, indent=2))


if __name__ == "__main__":
    main()
