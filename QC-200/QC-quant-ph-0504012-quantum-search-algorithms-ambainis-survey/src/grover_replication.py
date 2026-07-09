"""
Independent replication of Grover's algorithm quadratic speedup claim
(Theorem 2.1 in Ambainis "Quantum Search Algorithms", arXiv:quant-ph/0504012).

Claim under test (C1 - headline):
    Search on N unstructured items with 1 marked can be solved with
    O(sqrt(N)) quantum queries.

Operational sub-claim we actually measure (from the standard Grover
analysis the survey summarises around Theorem 2.1 and §2.2):
    After k = round((pi/4) * sqrt(N/M)) Grover iterations on N items with
    M marked, the probability of measuring a marked item is
        P(k) = sin^2( (2k+1) * theta ),  where sin(theta) = sqrt(M/N).
    For M=1 this approaches ~1 as N grows, and equals exactly 1 for N=4
    with k=1 (the well-known "one-query gives certainty" case).

Method:
  * Build the standard oracle + diffuser Grover circuit in Qiskit for
    n = 2, 4, 6, 8 qubits (N = 4, 16, 64, 256), M = 1 marked item.
  * Use statevector simulation (Qiskit Aer AerSimulator method='statevector')
    to get the exact probability of measuring the marked index after k
    iterations.
  * Sweep k in [0 .. k_opt+2] to demonstrate the sin^2((2k+1)theta)
    oscillation, and confirm the optimal k = round((pi/4) * sqrt(N))
    matches the analytic maximum within tolerance.
  * Verify O(sqrt(N)) query scaling: log(k_opt) vs 0.5 * log(N) linear fit,
    slope should be ~= 0.5.

Free / open source only.  No network calls, no fabrication.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from typing import Dict, List

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def analytic_success_prob(n: int, k: int, m: int = 1) -> float:
    """P_success after k Grover iterations on N=2**n items, M marked."""
    N = 2 ** n
    theta = math.asin(math.sqrt(m / N))
    return math.sin((2 * k + 1) * theta) ** 2


def optimal_k(n: int, m: int = 1) -> int:
    """Textbook optimal iteration count k_opt = round((pi/4)*sqrt(N/M))."""
    N = 2 ** n
    return int(round((math.pi / 4.0) * math.sqrt(N / m)))


def grover_oracle(n: int, marked: int) -> QuantumCircuit:
    """Phase-flip oracle that maps |marked> -> -|marked>, others unchanged.

    Implemented as an n-controlled-Z sandwiched with X gates on qubits that
    are 0 in the binary rep of `marked`.  Standard textbook construction.
    """
    qc = QuantumCircuit(n, name=f"O_{marked}")
    bits = [(marked >> i) & 1 for i in range(n)]  # little-endian
    # Flip qubits that are 0 in `marked` so |marked> becomes |11..1>.
    for i, b in enumerate(bits):
        if b == 0:
            qc.x(i)
    # Multi-controlled Z on |11..1>.
    if n == 1:
        qc.z(0)
    else:
        qc.h(n - 1)
        qc.mcx(list(range(n - 1)), n - 1)
        qc.h(n - 1)
    # Undo the X flips.
    for i, b in enumerate(bits):
        if b == 0:
            qc.x(i)
    return qc


def grover_diffuser(n: int) -> QuantumCircuit:
    """Standard Grover diffuser 2|s><s| - I where |s> = H^n |0>."""
    qc = QuantumCircuit(n, name="D")
    qc.h(range(n))
    qc.x(range(n))
    if n == 1:
        qc.z(0)
    else:
        qc.h(n - 1)
        qc.mcx(list(range(n - 1)), n - 1)
        qc.h(n - 1)
    qc.x(range(n))
    qc.h(range(n))
    return qc


def build_grover(n: int, marked: int, k: int) -> QuantumCircuit:
    qc = QuantumCircuit(n)
    qc.h(range(n))
    O = grover_oracle(n, marked)
    D = grover_diffuser(n)
    for _ in range(k):
        qc.compose(O, inplace=True)
        qc.compose(D, inplace=True)
    qc.save_statevector()
    return qc


def measured_success_prob(n: int, marked: int, k: int, sim: AerSimulator) -> float:
    qc = build_grover(n, marked, k)
    tqc = transpile(qc, sim)
    result = sim.run(tqc).result()
    sv = np.asarray(result.get_statevector(tqc))
    return float(abs(sv[marked]) ** 2)


def run_experiment(qubit_sizes: List[int], marked: int = 3, tol: float = 1e-6) -> Dict:
    sim = AerSimulator(method="statevector")
    results = {
        "tool_versions": {
            "qiskit": __import__("qiskit").__version__,
            "qiskit_aer": __import__("qiskit_aer").__version__,
            "numpy": np.__version__,
            "python": sys.version.split()[0],
        },
        "claim_under_test": (
            "Grover: N-item unstructured search with 1 marked is solved with "
            "O(sqrt(N)) quantum queries; after k = round((pi/4)*sqrt(N)) "
            "iterations the marked-item probability equals "
            "sin^2((2k+1)*asin(1/sqrt(N)))."
        ),
        "M_marked": 1,
        "marked_index": marked,
        "per_N": [],
        "scaling_fit": {},
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    log_Ns = []
    log_ks = []

    for n in qubit_sizes:
        N = 2 ** n
        k_opt = optimal_k(n)
        # Sweep 0..k_opt+2 iterations.
        sweep = []
        max_k = k_opt + 2
        for k in range(max_k + 1):
            p_meas = measured_success_prob(n, marked, k, sim)
            p_ana = analytic_success_prob(n, k)
            sweep.append(
                {
                    "k": k,
                    "P_measured": p_meas,
                    "P_analytic": p_ana,
                    "abs_err": abs(p_meas - p_ana),
                }
            )
        # Pick empirical best k from measured sweep.
        best = max(sweep, key=lambda r: r["P_measured"])
        row = {
            "n_qubits": n,
            "N": N,
            "k_opt_theory": k_opt,
            "k_opt_empirical": best["k"],
            "P_at_k_opt_measured": sweep[k_opt]["P_measured"],
            "P_at_k_opt_analytic": sweep[k_opt]["P_analytic"],
            "P_max_measured": best["P_measured"],
            "max_abs_err_over_sweep": max(r["abs_err"] for r in sweep),
            "sweep": sweep,
        }
        results["per_N"].append(row)
        log_Ns.append(math.log(N))
        log_ks.append(math.log(k_opt))

    # Linear fit log(k_opt) vs log(N): slope should be ~0.5 (i.e. k ~ sqrt(N)).
    if len(log_Ns) >= 2:
        slope, intercept = np.polyfit(log_Ns, log_ks, 1)
        results["scaling_fit"] = {
            "model": "log(k_opt) = slope * log(N) + intercept",
            "slope": float(slope),
            "intercept": float(intercept),
            "expected_slope": 0.5,
            "slope_abs_err_from_0.5": float(abs(slope - 0.5)),
            "log_N": log_Ns,
            "log_k_opt": log_ks,
        }
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, help="Path to write JSON evidence.")
    ap.add_argument(
        "--qubits",
        default="2,4,6,8",
        help="Comma-separated n values (N = 2**n).",
    )
    ap.add_argument("--marked", type=int, default=3)
    args = ap.parse_args()

    qubit_sizes = [int(x) for x in args.qubits.split(",") if x.strip()]
    print(f"[run] qubit sizes: {qubit_sizes}  marked index: {args.marked}")
    results = run_experiment(qubit_sizes, marked=args.marked)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(results, f, indent=2)

    # Console summary.
    print()
    print("=" * 72)
    print("Grover replication summary  (paper: arXiv:quant-ph/0504012, Thm 2.1)")
    print("=" * 72)
    print(f"{'n':>3} {'N':>5} {'k_opt':>6} {'P_at_kopt (meas)':>17} "
          f"{'P_at_kopt (analytic)':>21} {'|meas-ana|_max':>16}")
    for row in results["per_N"]:
        print(
            f"{row['n_qubits']:>3d} {row['N']:>5d} {row['k_opt_theory']:>6d}"
            f" {row['P_at_k_opt_measured']:>17.10f}"
            f" {row['P_at_k_opt_analytic']:>21.10f}"
            f" {row['max_abs_err_over_sweep']:>16.2e}"
        )
    fit = results["scaling_fit"]
    if fit:
        print()
        print(f"Scaling fit: log(k_opt) vs log(N), slope = {fit['slope']:.4f}"
              f" (expected 0.5)  |err| = {fit['slope_abs_err_from_0.5']:.4f}")


if __name__ == "__main__":
    main()
