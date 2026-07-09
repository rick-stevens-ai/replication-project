"""
Grover replication from Abhijith et al. 1804.03719 Sec. 2.
N=8 (n=3 qubits), single marked item |m> = |101> (5 in decimal).
Optimal iterations k = round( (pi/4) * sqrt(N/M) ) with M=1, N=8 -> k = 2.
Analytic success prob after k iterations: sin^2( (2k+1)*theta ), theta = arcsin(sqrt(M/N)).
For N=8, M=1: theta = arcsin(1/sqrt(8)) ~ 0.3614 rad, (2*2+1)*theta = 5*theta ~ 1.807,
P(marked) = sin^2(1.807) ~ 0.9453.  Paper claims >= 0.945 for this setup.
"""
import json, math, numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

n = 3
N = 2**n
marked = 5  # |101>
M = 1

# Oracle for a single marked state |m>: applies -1 phase to |m> only.
# Implement via X's to flip m -> |111>, then multi-controlled Z, then undo X's.
def oracle(qc, m, n):
    # Flip qubits where m has a 0 so that m maps to all-ones.
    bits = format(m, f"0{n}b")  # msb-first: bits[0] is qubit (n-1)
    for i, b in enumerate(bits):
        if b == '0':
            qc.x(n - 1 - i)
    # multi-controlled Z on n qubits: H on target, mcx, H on target
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    for i, b in enumerate(bits):
        if b == '0':
            qc.x(n - 1 - i)

# Diffuser: 2|s><s| - I where |s> = H^n |0>^n.
def diffuser(qc, n):
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

theta = math.asin(math.sqrt(M / N))
k_opt = int(round((math.pi / 4) * math.sqrt(N / M)))  # = 2 for N=8, M=1
analytic_success = math.sin((2 * k_opt + 1) * theta) ** 2

qc = QuantumCircuit(n)
for q in range(n):
    qc.h(q)
for _ in range(k_opt):
    oracle(qc, marked, n)
    diffuser(qc, n)

sv = Statevector.from_instruction(qc)
probs = sv.probabilities()

# Probability of marked state
p_marked = float(probs[marked])

def idx_to_bits(idx, n):
    return format(idx, f"0{n}b")

result = {
    "algorithm": "Grover",
    "N": N,
    "M": 1,
    "marked_state_decimal": marked,
    "marked_state_msb_first": idx_to_bits(marked, n),
    "iterations_used": k_opt,
    "analytic_success_prob": analytic_success,
    "sim_success_prob": p_marked,
    "threshold_paper": 0.945,
    "match": p_marked >= 0.945,
    "all_probs": {idx_to_bits(i, n): float(probs[i]) for i in range(N)},
}
print(json.dumps(result, indent=2))

with open("grover_result.json", "w") as f:
    json.dump(result, f, indent=2)
