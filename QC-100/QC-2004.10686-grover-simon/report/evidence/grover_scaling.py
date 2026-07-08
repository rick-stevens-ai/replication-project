"""Scan Grover success probability vs number of iterations.

For our 6-bit key search with M=2 marked keys (single-pair oracle):
  N = 64, theta = arcsin(sqrt(2/64)) ~ 0.1777 rad
  Optimal k = round( (pi/2 - theta) / (2 theta) ) = 4
  Predicted P_success(k) = sin^2( (2k+1) theta )
"""
import json
import math
from typing import List
from grover_simon import build_grover_circuit, N

from qiskit import transpile
from qiskit_aer import AerSimulator

M_bits = [0, 1, 1, 1, 0, 1]
C_bits = [0, 1, 1, 1, 1, 1]
pairs = [(M_bits, C_bits)]

N_search = 1 << (2 * N)
M_solutions = 2
theta = math.asin(math.sqrt(M_solutions / N_search))
print(f"N_search={N_search}, M={M_solutions}, theta={theta:.4f} rad, "
      f"predicted optimum k=4")

sim = AerSimulator(method='statevector')
rows = []
for k in range(0, 8):
    qc, _, _ = build_grover_circuit(pairs, k)
    tqc = transpile(qc, sim, optimization_level=1)
    counts = sim.run(tqc, shots=4000).result().get_counts()
    total = sum(counts.values())
    # keys sorted with rightmost = bit 0
    marked_bitstrs = ['001110', '111000']
    marked_prob = 0.0
    for bstr, ct in counts.items():
        # Qiskit bit order: rightmost = bit 0, so key list = reverse
        b = bstr[::-1]
        if b in marked_bitstrs:
            marked_prob += ct / total
    predicted = math.sin((2 * k + 1) * theta) ** 2
    row = dict(iterations=k,
               empirical_marked_prob=marked_prob,
               theory_marked_prob=predicted,
               classical_random=M_solutions / N_search,
               classical_random_after_k_queries=(k + 1) * M_solutions / N_search)
    rows.append(row)
    print(f"  k={k}: empirical={marked_prob:.4f}  theory={predicted:.4f}  "
          f"classical_rand~{(k+1)*M_solutions/N_search:.4f}")

with open('report/evidence/grover_scaling.json', 'w') as f:
    json.dump({'N_search': N_search,
               'M_solutions': M_solutions,
               'theta_rad': theta,
               'rows': rows}, f, indent=2)
print("Wrote report/evidence/grover_scaling.json")
