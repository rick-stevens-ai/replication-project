#!/usr/bin/env python3
"""
Standard Grover amplitude amplification on N=16 with a single marked item.

Reproduces the well-known bound: for a Grover search with success probability
p, standard amplitude amplification uses ~ (pi/4)/sqrt(p) queries to the oracle
to reach probability >= 1/2 (and O(1/sqrt(p)) to hit any high probability).

Ambainis (1010.4458) states standard AA runs in time O(T_max / sqrt(p_succ)).
Here T_max = 1 query, p_succ = 1/16, so query count grows as 1/sqrt(p_succ)
~ 4. We verify by running the full Qiskit statevector circuit.

Outputs a JSON summary to standard_aa_result.json.
"""
import json
import math
import time
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

N_QUBITS = 4  # search space of N = 16
N = 2 ** N_QUBITS
MARKED = 5  # one marked item

OUTDIR = Path(__file__).resolve().parent
OUTFILE = OUTDIR / "standard_aa_result.json"


def marked_bits(x, n):
    """Return list of bit values [b_0..b_{n-1}] for integer x (LSB first)."""
    return [(x >> i) & 1 for i in range(n)]


def build_oracle(n, marked):
    """Marks |marked> with a phase flip: |x> -> -|x> if x==marked else |x>."""
    qc = QuantumCircuit(n, name="Oracle")
    bits = marked_bits(marked, n)
    # X where bit is 0 so that a multi-controlled Z fires on |marked>.
    for q, b in enumerate(bits):
        if b == 0:
            qc.x(q)
    # multi-controlled Z on all qubits (via H + MCX + H on the last)
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    for q, b in enumerate(bits):
        if b == 0:
            qc.x(q)
    return qc


def build_diffuser(n):
    """Grover diffuser 2|s><s| - I where |s> = H^n |0>."""
    qc = QuantumCircuit(n, name="Diffuser")
    qc.h(range(n))
    qc.x(range(n))
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    qc.x(range(n))
    qc.h(range(n))
    return qc


def grover_circuit(n, marked, iterations):
    qc = QuantumCircuit(n)
    qc.h(range(n))
    oracle = build_oracle(n, marked)
    diffuser = build_diffuser(n)
    for _ in range(iterations):
        qc.compose(oracle, inplace=True)
        qc.compose(diffuser, inplace=True)
    return qc


def prob_marked(sv, marked, n):
    # amplitude of |marked>
    idx = marked  # Qiskit uses little-endian integer index directly
    amp = sv.data[idx]
    return abs(amp) ** 2


def run():
    t0 = time.time()
    p0 = 1 / N  # initial success probability after H^n
    # Theoretical Grover: optimal iterations = round((pi/4)*sqrt(N/M))
    opt_theory = (math.pi / 4) * math.sqrt(N)
    theta = math.asin(math.sqrt(p0))
    # After k iterations, prob = sin^2((2k+1)*theta)

    curve = []
    first_hit_prob09 = None
    for k in range(0, 15):
        qc = grover_circuit(N_QUBITS, MARKED, k)
        sv = Statevector.from_instruction(qc)
        p = prob_marked(sv, MARKED, N_QUBITS)
        p_analytic = math.sin((2 * k + 1) * theta) ** 2
        # Each Grover iteration uses 1 oracle query.
        # Building the state uses 0 oracle queries (just H^n).
        oracle_queries = k
        curve.append(
            dict(
                iterations=k,
                oracle_queries=oracle_queries,
                p_marked_qiskit=p,
                p_marked_analytic=p_analytic,
            )
        )
        if first_hit_prob09 is None and p >= 0.9:
            first_hit_prob09 = k

    # Best iteration (max prob) and theoretical optimum
    best = max(curve, key=lambda r: r["p_marked_qiskit"])

    result = dict(
        N=N,
        marked_item=MARKED,
        initial_success_prob=p0,
        theta_radians=theta,
        optimal_iterations_theory=opt_theory,
        first_iterations_reaching_p_ge_0_9=first_hit_prob09,
        best_iteration=best["iterations"],
        best_prob=best["p_marked_qiskit"],
        curve=curve,
        ambainis_standard_AA_scaling="O(T_max / sqrt(p_succ))",
        T_max_queries=1,
        p_succ=p0,
        expected_query_count_scaling=1.0 / math.sqrt(p0),
        wall_time_seconds=time.time() - t0,
    )
    OUTFILE.write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    run()
