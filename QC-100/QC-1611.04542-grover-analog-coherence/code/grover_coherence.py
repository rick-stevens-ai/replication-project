"""
Independent replication of arXiv:1611.04542
"Coherence and Entanglement Monogamy in the Discrete Analogue of Analog Grover Search"
Anand & Pati, 2016.

We reproduce the paper's central quantitative signature:
  Coherence (l1-norm and relative-entropy) is non-zero throughout the search
  and drops to zero at (and only at) the point where the success probability
  peaks to 1 (the optimal Grover iteration ~ (pi/4) sqrt(N)).

We implement STANDARD discrete Grover search on n qubits using Qiskit's
statevector simulation, for n = 3, 4, 5 qubits.  For each iteration k we
record:
  - P_success(k)  = |<w|psi_k>|^2
  - C_l1(rho_k)   = sum_{i!=j} |rho_ij|   (l1-norm of coherence, computational basis)
  - C_r(rho_k)    = S(rho_diag) - S(rho)  (relative entropy of coherence)

Because psi_k is a pure state, rho_k = |psi_k><psi_k|, so
   C_l1(rho) = (sum_i |c_i|)^2 - 1   where c_i are the amplitudes
   S(rho)    = 0
   S(rho_diag) = H( { |c_i|^2 } )

We also compute the theoretical Grover success probability
   P_theory(k) = sin^2( (2k+1) * theta ),   sin(theta) = 1/sqrt(N)
and the optimal iteration count k_opt = round( (pi/4) sqrt(N) - 1/2 ).

Outputs: JSON evidence per n, saved to report/evidence/.
"""

import json
import math
import os
import sys
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, Operator

EVIDENCE_DIR = Path(__file__).resolve().parents[1] / "report" / "evidence"
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)


def grover_oracle(n: int, marked_index: int) -> QuantumCircuit:
    """Phase-flip oracle marking basis state |marked_index>."""
    qc = QuantumCircuit(n, name="oracle")
    # Flip bits so that marked_index -> |11..1>, apply multi-controlled Z, flip back.
    bits = [(marked_index >> i) & 1 for i in range(n)]
    for q, b in enumerate(bits):
        if b == 0:
            qc.x(q)
    # multi-controlled Z on the last qubit using H + MCX + H
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    for q, b in enumerate(bits):
        if b == 0:
            qc.x(q)
    return qc


def grover_diffuser(n: int) -> QuantumCircuit:
    """Standard Grover diffuser (reflection about |s>)."""
    qc = QuantumCircuit(n, name="diffuser")
    for q in range(n):
        qc.h(q)
    for q in range(n):
        qc.x(q)
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    for q in range(n):
        qc.x(q)
    for q in range(n):
        qc.h(q)
    return qc


def l1_coherence_pure(amps: np.ndarray) -> float:
    """C_l1 = sum_{i!=j} |rho_ij| = (sum_i |c_i|)^2 - sum_i |c_i|^2."""
    abs_amps = np.abs(amps)
    return float((abs_amps.sum()) ** 2 - (abs_amps ** 2).sum())


def rel_entropy_coherence_pure(amps: np.ndarray) -> float:
    """C_r = S(rho_diag) - S(rho) = H({|c_i|^2}), since S(rho_pure) = 0."""
    p = np.abs(amps) ** 2
    p = p[p > 0]
    return float(-(p * np.log2(p)).sum())


def run_for_n(n: int, marked_index: int, max_extra_iters: int = 3):
    N = 2 ** n
    theta = math.asin(1.0 / math.sqrt(N))
    k_opt_float = (math.pi / (4 * theta)) - 0.5
    k_opt = int(round(k_opt_float))
    max_k = k_opt + max_extra_iters

    # Initial state |s> = uniform superposition (n Hadamards)
    init = QuantumCircuit(n)
    for q in range(n):
        init.h(q)

    oracle = grover_oracle(n, marked_index)
    diffuser = grover_diffuser(n)

    state = Statevector.from_instruction(init)
    records = []

    # k = 0 (initial state, no Grover iteration applied)
    amps = state.data
    p_success = float(abs(amps[marked_index]) ** 2)
    p_theory = math.sin((2 * 0 + 1) * theta) ** 2
    records.append({
        "k": 0,
        "p_success": p_success,
        "p_theory_grover": p_theory,
        "c_l1": l1_coherence_pure(amps),
        "c_relative_entropy": rel_entropy_coherence_pure(amps),
    })

    # Apply k Grover iterations, record after each
    for k in range(1, max_k + 1):
        state = state.evolve(oracle).evolve(diffuser)
        amps = state.data
        p_success = float(abs(amps[marked_index]) ** 2)
        p_theory = math.sin((2 * k + 1) * theta) ** 2
        records.append({
            "k": k,
            "p_success": p_success,
            "p_theory_grover": p_theory,
            "c_l1": l1_coherence_pure(amps),
            "c_relative_entropy": rel_entropy_coherence_pure(amps),
        })

    # Find where success actually peaks in our sim
    ks = [r["k"] for r in records]
    ps = [r["p_success"] for r in records]
    cls = [r["c_l1"] for r in records]
    crs = [r["c_relative_entropy"] for r in records]
    k_peak = ks[int(np.argmax(ps))]
    p_peak = max(ps)
    c_l1_at_peak = cls[int(np.argmax(ps))]
    c_r_at_peak = crs[int(np.argmax(ps))]

    summary = {
        "n_qubits": n,
        "N": N,
        "marked_index": marked_index,
        "theta_rad": theta,
        "k_opt_theory_float": k_opt_float,
        "k_opt_theory_rounded": k_opt,
        "k_peak_simulated": k_peak,
        "p_success_peak": p_peak,
        "c_l1_at_peak": c_l1_at_peak,
        "c_relative_entropy_at_peak": c_r_at_peak,
        "c_l1_initial": records[0]["c_l1"],
        "c_relative_entropy_initial": records[0]["c_relative_entropy"],
        "records": records,
    }
    return summary


def main():
    results = {}
    for n in [3, 4, 5]:
        # Mark index 0 for concreteness; result independent of choice.
        summary = run_for_n(n, marked_index=0)
        results[f"n{n}"] = summary
        out = EVIDENCE_DIR / f"grover_coherence_n{n}.json"
        out.write_text(json.dumps(summary, indent=2))
        print(f"[n={n}] k_opt_theory={summary['k_opt_theory_rounded']}  "
              f"k_peak_sim={summary['k_peak_simulated']}  "
              f"P_peak={summary['p_success_peak']:.6f}  "
              f"C_l1(initial)={summary['c_l1_initial']:.6f}  "
              f"C_l1(at peak)={summary['c_l1_at_peak']:.6f}  "
              f"C_r(at peak)={summary['c_relative_entropy_at_peak']:.6f}")

    # Aggregate top-line file
    top = {
        "paper": "arXiv:1611.04542",
        "tool": "Qiskit statevector",
        "cases": {k: {kk: v for kk, v in s.items() if kk != "records"}
                  for k, s in results.items()},
    }
    (EVIDENCE_DIR / "summary.json").write_text(json.dumps(top, indent=2))
    print("\nSaved evidence to", EVIDENCE_DIR)


if __name__ == "__main__":
    main()
