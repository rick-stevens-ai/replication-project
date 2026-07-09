"""Replication of Tulsi-Grover-Patel (2005), quant-ph/0505007
   "A New Algorithm for Fixed Point Quantum Search"

Headline claim (Eq. 6): iterating the ancilla-controlled search algorithm
q times reduces the error probability from epsilon to epsilon^(2q+1)
for all positive integer q.

We test this exactly via numpy statevector simulation on an n-qubit
register with a single marked state.  The whole system has (n + 2)
qubits: ancilla-1, register (n qubits), ancilla-2.

Everything is real algebra (no external quantum simulator required),
so results are exact up to floating-point rounding.
"""
from __future__ import annotations

import json
import math
import os
import numpy as np

# ---------- basic building blocks ----------

def kron_all(*mats):
    out = mats[0]
    for m in mats[1:]:
        out = np.kron(out, m)
    return out

I2 = np.eye(2, dtype=complex)
X  = np.array([[0, 1], [1, 0]], dtype=complex)
H  = (1 / math.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)

def register_source_state(n: int) -> np.ndarray:
    """|s> = uniform superposition on n qubits."""
    return np.full(2**n, 1.0 / math.sqrt(2**n), dtype=complex)

def U_diffusion_prep_operator(n: int) -> np.ndarray:
    """U such that U|0..0> = |s>.  We take U = H^{\otimes n}."""
    Un = np.array([[1.0]], dtype=complex)
    for _ in range(n):
        Un = np.kron(Un, H)
    return Un

def reflection_about(state: np.ndarray) -> np.ndarray:
    """R = 2|state><state| - I."""
    d = state.shape[0]
    v = state.reshape(-1, 1)
    return 2 * (v @ v.conj().T) - np.eye(d, dtype=complex)

# ---------- algorithm ----------

def run_algorithm(n: int, target_index: int, q: int) -> tuple[float, float]:
    """Run the q-iteration Tulsi/Grover/Patel algorithm.

    Layout of qubits (little / big irrelevant, we just fix an order):
      qubit 0        : ancilla-1
      qubits 1..n    : n-qubit search register
      qubit n+1      : ancilla-2

    Returns (final_error_probability, predicted_error_probability).
    """
    N = 2**n
    assert 0 <= target_index < N
    eps = 1.0 - 1.0 / N            # initial error probability = 1 - f = 1 - |<t|s>|^2 = 1 - 1/N

    # ------------------------------------------------------------------
    # Build state |0>_a1 |s>_reg |0>_a2  (dimensions: 2 * N * 2)
    # ------------------------------------------------------------------
    a1_zero = np.array([1, 0], dtype=complex)
    a2_zero = np.array([1, 0], dtype=complex)
    s = register_source_state(n)
    psi = kron_all(a1_zero, s, a2_zero)              # length 4N
    # apply H to ancilla-1 (initial state preparation)
    H_a1 = kron_all(H, np.eye(N, dtype=complex), I2) # H on ancilla-1
    psi = H_a1 @ psi                                 # now |+>|s>|0>

    # ------------------------------------------------------------------
    # Operators used inside the iteration
    # ------------------------------------------------------------------
    # (1) Controlled oracle: if ancilla-1==1 and register==|t>, flip ancilla-2.
    # This is a CCX with two controls that jointly act on (a1, register==t).
    # We construct it as a diagonal-then-X action for efficiency: pick the
    # subspace ancilla-1=1 AND register=target, then swap ancilla-2 zero <-> one.
    dim = 4 * N
    oracle = np.eye(dim, dtype=complex)
    # index layout: idx = a1*(N*2) + reg*2 + a2  (a1 in {0,1}, reg in {0..N-1}, a2 in {0,1})
    def idx(a1, reg, a2): return a1 * (2 * N) + reg * 2 + a2
    i0 = idx(1, target_index, 0)
    i1 = idx(1, target_index, 1)
    # swap columns i0,i1 (identity except at these positions)
    oracle[i0, i0] = 0
    oracle[i1, i1] = 0
    oracle[i0, i1] = 1
    oracle[i1, i0] = 1

    # (2) Joint diffusion: (H \otimes U) I_{0s} (H \otimes U)^\dagger on (ancilla-1, register).
    # I_{0s} is reflection about |0>|0..0>.  Equivalently, this is reflection
    # about the joint source state |s_j> = (H \otimes U)|0>|0..0>.
    U = U_diffusion_prep_operator(n)                # H^n so |s>=U|0..0>
    HU = np.kron(H, U)                              # (a1, register)
    joint_source_full = HU @ np.eye(2 * N, dtype=complex)[:, 0]  # first column = HU|0..0>
    R_joint = reflection_about(joint_source_full)   # 2N x 2N
    # embed into (a1, register, a2) space (identity on a2)
    diffusion_full = np.kron(R_joint, I2)           # 4N x 4N

    # ------------------------------------------------------------------
    # Iterate q times.  We simulate the deterministic branch that mirrors
    # the paper's analysis exactly: after each measurement of ancilla-2,
    # the outcome-0 branch is post-selected and the outcome-1 branch's
    # probability is accumulated into a running "success" probability.
    # This is faithful to the algorithm because outcome 1 immediately
    # exits with a target-state register (the algorithm has succeeded).
    # ------------------------------------------------------------------
    # Precompute projectors onto ancilla-2 = 0 / = 1
    P0_a2 = np.diag([1.0, 0.0]).astype(complex)
    P1_a2 = np.diag([0.0, 1.0]).astype(complex)
    Proj0 = kron_all(np.eye(2, dtype=complex), np.eye(N, dtype=complex), P0_a2)
    Proj1 = kron_all(np.eye(2, dtype=complex), np.eye(N, dtype=complex), P1_a2)

    # Track probability of NOT having exited yet, and the (normalised)
    # state on the outcome-0 branch.
    prob_still_running = 1.0
    success_prob = 0.0
    current = psi.copy()

    for _ in range(q):
        # Step 1: oracle
        current = oracle @ current
        # Step 2a: measure ancilla-2
        branch1 = Proj1 @ current
        branch0 = Proj0 @ current
        p1 = float(np.vdot(branch1, branch1).real)   # conditional prob of outcome 1
        p0 = float(np.vdot(branch0, branch0).real)
        # Any outcome-1 branch means the register is in |t>: full success.
        success_prob += prob_still_running * p1
        prob_still_running *= p0
        if p0 <= 1e-300:
            current = branch0
            break
        # renormalise the outcome-0 branch so subsequent gates act on a
        # proper unit vector (matches the paper's analytical treatment)
        current = branch0 / math.sqrt(p0)
        # apply joint diffusion on outcome-0 branch
        current = diffusion_full @ current

    # After q iterations we measure the register in the surviving branch.
    # Probability of finding target in the register (given still running):
    prob_target_given_running = 0.0
    for a1 in (0, 1):
        for a2 in (0, 1):
            amp = current[idx(a1, target_index, a2)]
            prob_target_given_running += float((amp.conjugate() * amp).real)
    total_success = success_prob + prob_still_running * prob_target_given_running
    total_error = 1.0 - total_success

    predicted_error = eps ** (2 * q + 1)
    return total_error, predicted_error

# ---------- experiment sweep ----------

def main():
    outdir = os.path.dirname(os.path.abspath(__file__))
    results = []
    print(f"{'n':>3} {'q':>3} {'eps':>10} {'measured_err':>15} {'predicted eps^(2q+1)':>25} {'abs_diff':>12}")
    for n in (2, 3, 4):                       # N = 4, 8, 16
        for q in (1, 2, 3, 4):
            err, pred = run_algorithm(n, target_index=0, q=q)
            diff = abs(err - pred)
            eps = 1.0 - 1.0 / (2**n)
            print(f"{n:>3d} {q:>3d} {eps:>10.6f} {err:>15.6e} {pred:>25.6e} {diff:>12.2e}")
            results.append({
                "n": n,
                "N": 2**n,
                "q": q,
                "epsilon": eps,
                "measured_error": err,
                "predicted_error": pred,
                "abs_diff": diff,
            })

    # Sanity: monotonic in q for each n?
    monotonic_ok = True
    for n in (2, 3, 4):
        errs = [r["measured_error"] for r in results if r["n"] == n]
        if not all(errs[i+1] <= errs[i] + 1e-12 for i in range(len(errs) - 1)):
            monotonic_ok = False

    # Numerical match test: max abs_diff should be ~ machine precision
    max_diff = max(r["abs_diff"] for r in results)
    tol = 1e-9
    passes = max_diff < tol and monotonic_ok

    with open(os.path.join(outdir, "results.json"), "w") as f:
        json.dump({
            "paper": "quant-ph/0505007 (Tulsi, Grover, Patel 2005)",
            "claim_tested": "After q iterations, net error probability = epsilon^(2q+1) for all positive integer q (Eq. 6).",
            "results": results,
            "max_abs_diff": max_diff,
            "tolerance": tol,
            "monotonic_in_q": monotonic_ok,
            "verdict": "REPLICATED" if passes else "FAILED",
        }, f, indent=2)
    print(f"\nmax abs diff between measured and predicted: {max_diff:.3e} (tol {tol})")
    print(f"monotonic in q for each n: {monotonic_ok}")
    print("VERDICT:", "REPLICATED" if passes else "FAILED")

if __name__ == "__main__":
    main()
