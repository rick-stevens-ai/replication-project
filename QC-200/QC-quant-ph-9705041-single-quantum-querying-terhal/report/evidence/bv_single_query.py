#!/usr/bin/env python3
"""
Replicate Terhal & Smolin, "Single quantum querying of a database",
arXiv:quant-ph/9705041 (Phys. Rev. A 58, 1822).

Central claim (Sec. II): the Bernstein-Vazirani parity-query protocol
retrieves the entire n-bit database string y in a SINGLE quantum query
with probability 1, whereas the classical information-theoretic bound
requires M >= n / log2(n+1) queries.

We reproduce this for n = 4 using Qiskit Aer statevector simulation:
  * enumerate all 16 possible databases y in {0,1}^4
  * build the parity oracle U_y : |x>|b> -> |x>|b XOR (x.y mod 2)>
  * run the BV circuit: H^n on X, prepare |->=|0>-|1>/sqrt2 on B, oracle, H^n on X
  * measure X register -> must equal y with probability 1.0
Also compare to:
  (a) classical single-query success prob for n=4 = 1/2^n = 1/16
  (b) Grover single-iteration success for N=2^n=16, marked=1: P = sin^2(3*theta),
      theta = arcsin(1/sqrt(N)); for N=16, P = (sin(3*arcsin(1/4)))^2 approx 0.4727.
      (Standard Grover; for N=4 it's exactly 1.0 in 1 iteration, which is a
       degenerate case, so we use N=16 for a fair single-iteration comparison.
       Also record the N=4 Grover=1.0 baseline for the exact database size.)

Outputs JSON to report/evidence/bv_results.json.
"""

import json
import os
from itertools import product

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator


def bv_oracle(qc, x_qubits, b_qubit, y):
    """Apply U_y : |x>|b> -> |x>|b XOR (x.y mod 2)>.
    y is a tuple of bits (y_0, y_1, ..., y_{n-1}) with y_0 the least-significant.
    Implemented as: for each i with y_i=1, CNOT(x_i, b).
    (x.y mod 2 = XOR over i of (x_i AND y_i).)
    """
    for i, bit in enumerate(y):
        if bit == 1:
            qc.cx(x_qubits[i], b_qubit)


def bv_circuit(y):
    """Full BV circuit for database bit-string y, single query."""
    n = len(y)
    x = QuantumRegister(n, "x")
    b = QuantumRegister(1, "b")
    c = ClassicalRegister(n, "c")
    qc = QuantumCircuit(x, b, c)
    # Prepare |->_b = (|0>-|1>)/sqrt(2)
    qc.x(b[0])
    qc.h(b[0])
    # Prepare uniform superposition on X
    for q in x:
        qc.h(q)
    # Single query
    bv_oracle(qc, x, b[0], y)
    # Hadamard on X
    for q in x:
        qc.h(q)
    # Measure X
    qc.measure(x, c)
    return qc


def run_case(y, shots=4096):
    n = len(y)
    qc = bv_circuit(y)
    sim = AerSimulator()
    from qiskit import transpile
    tqc = transpile(qc, sim)
    result = sim.run(tqc, shots=shots).result()
    counts = result.get_counts()
    # Qiskit reports bitstrings with q_{n-1} ... q_0 (leftmost = highest index).
    # Our y is (y_0, y_1, ..., y_{n-1}) with y_0 lowest index.
    # Convert y to the same string convention: bit_{n-1}...bit_0
    target_bitstring = "".join(str(y[i]) for i in reversed(range(n)))
    p_correct = counts.get(target_bitstring, 0) / shots
    return target_bitstring, p_correct, counts


def statevector_prob(y):
    """Exact success probability via full statevector (no shot noise)."""
    n = len(y)
    x = QuantumRegister(n, "x")
    b = QuantumRegister(1, "b")
    qc = QuantumCircuit(x, b)
    qc.x(b[0]); qc.h(b[0])
    for q in x:
        qc.h(q)
    bv_oracle(qc, x, b[0], y)
    for q in x:
        qc.h(q)
    sv = Statevector.from_instruction(qc)
    # Marginalize over B; sum |amp|^2 over states where X-register bits equal y.
    # qubit ordering in Statevector: qubit 0 = LSB in the tensor index.
    # Here register x has qubits 0..n-1, b has qubit n.
    dim = 2 ** (n + 1)
    p = 0.0
    for idx in range(dim):
        bits = [(idx >> k) & 1 for k in range(n + 1)]
        x_bits = tuple(bits[:n])
        if x_bits == tuple(y):
            p += float(np.abs(sv.data[idx]) ** 2)
    return p


def grover_single_iteration_prob(N, marked=1):
    """Analytic Grover success prob after 1 iteration for N items with `marked` marked.
    theta = arcsin(sqrt(marked/N)); after k iterations P = sin^2((2k+1)*theta).
    """
    theta = np.arcsin(np.sqrt(marked / N))
    return float(np.sin(3 * theta) ** 2)


def main():
    n = 4
    print(f"Bernstein-Vazirani single-query replication, n={n}")
    print(f"Testing all {2**n} databases y in {{0,1}}^{n}")
    results = {}
    all_success = True
    exact_probs = []
    shot_probs = []
    for y_tuple in product([0, 1], repeat=n):
        y = list(y_tuple)
        target, p_shot, counts = run_case(y, shots=4096)
        p_exact = statevector_prob(y)
        exact_probs.append(p_exact)
        shot_probs.append(p_shot)
        y_str = "".join(str(b) for b in reversed(y))
        results[y_str] = {
            "y_lsb_first": y,
            "target_bitstring_msb_first": target,
            "p_success_shots_4096": p_shot,
            "p_success_exact_statevector": p_exact,
        }
        ok = "OK" if p_exact > 0.999 else "FAIL"
        print(f"  y={y_str}  target={target}  P_exact={p_exact:.6f}  P_shots={p_shot:.4f}  {ok}")
        if p_exact < 0.999:
            all_success = False

    classical_single_query_p = 1.0 / (2 ** n)  # picking one of 2^n databases at random after 1 classical query on a Hamming-weight-1 style guess = 1/N; a truly classical strategy needs n queries to be certain
    # Grover for N=2^n=16, one iteration
    grover_p_N16 = grover_single_iteration_prob(16, 1)
    # Note: The task-brief mentioned N=4 Grover (P=(3/4)^2 = 0.5625 is a common textbook claim
    # for 1 iter on N=4 with two-level cost; the exact analytic for N=4, k=1 gives sin^2(3*pi/6)=1.0
    # So we report both for context.
    grover_p_N4_analytic = grover_single_iteration_prob(4, 1)
    grover_p_N4_textbook = 0.75 ** 2

    summary = {
        "paper": "arXiv:quant-ph/9705041 (Terhal & Smolin 1997)",
        "n_bits": n,
        "num_databases_tested": len(results),
        "all_databases_recovered_with_prob_ge_0.999": all_success,
        "min_exact_success_prob": float(min(exact_probs)),
        "max_exact_success_prob": float(max(exact_probs)),
        "mean_shot_success_prob_4096": float(np.mean(shot_probs)),
        "paper_claim_single_query_success": 1.0,
        "comparisons": {
            "classical_uniform_random_guess_after_1_query_(brute)": classical_single_query_p,
            "classical_info_theoretic_min_queries_for_certainty": f"{n}/log2({n}+1) = {n/np.log2(n+1):.3f}",
            "grover_1_iteration_N=16_analytic": grover_p_N16,
            "grover_1_iteration_N=4_analytic": grover_p_N4_analytic,
            "grover_1_iteration_N=4_textbook_(3/4)^2": grover_p_N4_textbook,
        },
        "per_database": results,
    }

    outpath = os.path.join(os.path.dirname(__file__), "bv_results.json")
    with open(outpath, "w") as fh:
        json.dump(summary, fh, indent=2)
    print(f"\nWrote {outpath}")
    print(f"REPLICATED: all {2**n} databases recovered with P=1.0 (exact) — {all_success}")


if __name__ == "__main__":
    main()
