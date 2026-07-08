"""
Multi-case Qiskit gate-level vs analytic QPE cross-check for Quantum Counting.
Prints max L∞ deviation across a small grid.
"""
import math
import numpy as np
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from quantum_counting import quantum_counting_statevector
from verify_qiskit import build_count_circuit, marginal_over_counting
from qiskit.quantum_info import Statevector

cases = [
    (2, [0], 3),
    (3, [1, 4], 4),
    (4, [0], 4),
    (4, [3, 7, 12], 5),
    (5, [1, 5, 10, 20, 25], 5),
    (5, [2, 4, 6, 8, 10, 12, 14, 16, 18, 20], 6),
    (6, [1, 10, 25, 40, 55, 63], 6),
]

rows = []
worst = 0.0
for n, marked, p in cases:
    qc = build_count_circuit(n, marked, p)
    sv = Statevector.from_instruction(qc)
    dist_gate = marginal_over_counting(np.asarray(sv.data), p, n)
    dist_ana = quantum_counting_statevector(n, marked, p)
    diff = float(np.max(np.abs(dist_gate - dist_ana)))
    worst = max(worst, diff)
    argmax_gate = int(np.argmax(dist_gate))
    argmax_ana = int(np.argmax(dist_ana))
    # both mirrors are valid; compute both t_hat
    N = 1 << n
    P = 1 << p
    t_hat_gate = N * math.sin(math.pi * argmax_gate / P) ** 2
    t_hat_ana = N * math.sin(math.pi * argmax_ana / P) ** 2
    row = {
        "n": n, "t": len(marked), "p": p, "N": N, "P": P,
        "L_inf_diff": diff,
        "argmax_gate": argmax_gate, "t_hat_gate": round(t_hat_gate, 4),
        "argmax_ana": argmax_ana, "t_hat_ana": round(t_hat_ana, 4),
        "ok": diff < 1e-6,
    }
    rows.append(row)
    print(row)

print()
print(f"Worst L∞ deviation across {len(cases)} cases: {worst:.2e}")
print(f"All pass (< 1e-6): {all(r['ok'] for r in rows)}")
