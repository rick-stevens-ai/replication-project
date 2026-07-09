#!/usr/bin/env python3
"""
Independent replication of Grover's algorithm claim from Montanaro (2016)
"Quantum algorithms: an overview" arXiv:1511.04206.

Claim under test (from Section 3):
    Grover's algorithm solves unstructured search on N=2^n items with
    O(sqrt(N)) evaluations of the oracle f, versus O(N) classically.

Concrete quantitative predictions from standard Grover analysis
(consistent with Grover 1996 and Boyer-Brassard-Hoyer-Tapp 1998,
both cited in Montanaro 2016):

    - Optimal number of Grover iterations for a unique marked item is
      k* = round( (pi/4) * sqrt(N) ).
    - Success probability at k* satisfies P_success >= 1 - 1/N.
      Specifically, P_success = sin^2( (2k+1) * theta ), where
      sin(theta) = 1/sqrt(N).

We reproduce these using the Qiskit statevector simulator with a
phase-oracle marking a single item w, for N in {16, 64}. We compare
measured success probability against analytic prediction and the
Montanaro survey's claim that Grover requires only O(sqrt(N)) queries.
"""
import json
import math
import os
import sys
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def diffuser(n):
    """Grover diffusion operator on n qubits: 2|s><s| - I."""
    qc = QuantumCircuit(n, name="diffuser")
    qc.h(range(n))
    qc.x(range(n))
    # multi-controlled Z via H-MCX-H on the last qubit
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    qc.x(range(n))
    qc.h(range(n))
    return qc.to_gate()


def phase_oracle(n, marked):
    """Phase oracle that flips the sign of the |marked> basis state."""
    qc = QuantumCircuit(n, name=f"oracle(w={marked})")
    # Convert integer -> bitstring (little-endian to match Qiskit qubit order)
    bits = format(marked, f"0{n}b")[::-1]
    # X on qubits that are 0 in marked, so the all-ones state corresponds to marked
    for i, b in enumerate(bits):
        if b == "0":
            qc.x(i)
    # multi-controlled Z
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    for i, b in enumerate(bits):
        if b == "0":
            qc.x(i)
    return qc.to_gate()


def grover_circuit(n, marked, k):
    N = 2 ** n
    qc = QuantumCircuit(n, n)
    qc.h(range(n))
    orc = phase_oracle(n, marked)
    dif = diffuser(n)
    for _ in range(k):
        qc.append(orc, range(n))
        qc.append(dif, range(n))
    qc.measure(range(n), range(n))
    return qc


def analytic_prob(N, k):
    theta = math.asin(1.0 / math.sqrt(N))
    return math.sin((2 * k + 1) * theta) ** 2


def sweep_iterations(n, marked, shots=8192):
    """Run Grover for k = 0..K_max and record measured probability of marked."""
    N = 2 ** n
    k_opt = int(round((math.pi / 4) * math.sqrt(N)))
    k_max = 2 * k_opt + 2  # sweep past optimum
    sim = AerSimulator()
    rows = []
    for k in range(0, k_max + 1):
        qc = grover_circuit(n, marked, k)
        tqc = transpile(qc, sim)
        counts = sim.run(tqc, shots=shots).result().get_counts()
        # marked bitstring in Qiskit little-endian: reversed
        marked_bits = format(marked, f"0{n}b")
        # Qiskit's classical register is printed MSB-left already; measurement of q_i -> c_i
        # After our measure(range(n), range(n)), classical bit i = qubit i.
        # Qiskit's string is c_{n-1} ... c_0, so bit for qubit i is at position (n-1-i).
        # marked_bits above is standard big-endian: bit[0] is MSB (i.e. qubit n-1).
        # So the qiskit string equals marked_bits itself.
        p = counts.get(marked_bits, 0) / shots
        analytic = analytic_prob(N, k)
        rows.append({
            "k": k,
            "measured_prob": p,
            "analytic_prob": analytic,
        })
    return {
        "n": n,
        "N": N,
        "marked": marked,
        "k_opt_predicted": k_opt,
        "shots": shots,
        "sweep": rows,
    }


def main():
    outdir = Path(__file__).resolve().parent.parent / "report" / "evidence"
    outdir.mkdir(parents=True, exist_ok=True)

    results = {"paper": "arXiv:1511.04206 (Montanaro 2016)",
               "claim": "Grover unstructured search uses O(sqrt(N)) oracle queries; "
                        "optimal iteration count k*=round((pi/4)*sqrt(N)) achieves "
                        "P_success = sin^2((2k+1)*asin(1/sqrt(N))) close to 1.",
               "experiments": []}

    for n, marked in [(4, 11), (6, 42)]:  # N=16, N=64
        print(f"=== Grover n={n} N={2**n} marked={marked} ===", flush=True)
        r = sweep_iterations(n, marked, shots=8192)
        # Find measured optimum
        best = max(r["sweep"], key=lambda row: row["measured_prob"])
        r["measured_argmax_k"] = best["k"]
        r["measured_max_prob"] = best["measured_prob"]
        r["analytic_prob_at_k_opt"] = analytic_prob(r["N"], r["k_opt_predicted"])
        r["measured_prob_at_k_opt"] = next(
            row["measured_prob"] for row in r["sweep"] if row["k"] == r["k_opt_predicted"]
        )
        r["lower_bound_1_minus_1_over_N"] = 1 - 1.0 / r["N"]
        r["match_k_opt"] = (best["k"] == r["k_opt_predicted"])
        # Tolerance: within 2 sigma of shot noise + small circuit noise -> use 0.03
        r["match_prob_within_0.03"] = abs(
            r["measured_prob_at_k_opt"] - r["analytic_prob_at_k_opt"]
        ) < 0.03
        for row in r["sweep"]:
            print(f"  k={row['k']:2d}  measured={row['measured_prob']:.4f}  analytic={row['analytic_prob']:.4f}")
        print(f"  predicted k_opt = {r['k_opt_predicted']}   measured argmax k = {best['k']}")
        print(f"  P(k_opt) measured = {r['measured_prob_at_k_opt']:.4f}   "
              f"analytic = {r['analytic_prob_at_k_opt']:.4f}   "
              f"lower bound 1-1/N = {r['lower_bound_1_minus_1_over_N']:.4f}")
        results["experiments"].append(r)

    outfile = outdir / "grover_results.json"
    with open(outfile, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {outfile}")

    # CSV per experiment
    for r in results["experiments"]:
        csvpath = outdir / f"grover_sweep_N{r['N']}.csv"
        with open(csvpath, "w") as f:
            f.write("k,measured_prob,analytic_prob\n")
            for row in r["sweep"]:
                f.write(f"{row['k']},{row['measured_prob']:.6f},{row['analytic_prob']:.6f}\n")
        print(f"Wrote {csvpath}")


if __name__ == "__main__":
    main()
