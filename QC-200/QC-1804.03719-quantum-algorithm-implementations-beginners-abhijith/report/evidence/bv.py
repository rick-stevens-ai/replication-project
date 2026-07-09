"""
Bernstein-Vazirani (BV) replication from Abhijith et al. 1804.03719 Sec. 3.
n=4, hidden string s = '1011' (little-endian: s0=1,s1=1,s2=0,s3=1).
Expected: single query recovers s with P=1 on statevector.
"""
import json, numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

s = "1011"           # as written (msb-first, matches paper's textual convention)
n = len(s)

# BV oracle: |x>|y> -> |x>|y XOR (s.x)>
# Implement with CX from each x_i (where s_i=1) into the ancilla.
qc = QuantumCircuit(n + 1, n)

# Ancilla in |->
qc.x(n)
qc.h(n)

# H on all input qubits
for i in range(n):
    qc.h(i)

# Oracle: CX(x_i -> ancilla) for each s_i == 1.
# Qiskit indexing: qubit 0 is rightmost in |q_{n-1}...q_0>.
# We map string s (msb-first) so that s[0] -> qubit (n-1), s[1] -> qubit (n-2), ...
for i, bit in enumerate(s):
    if bit == '1':
        qc.cx(n - 1 - i, n)

# H on all input qubits again
for i in range(n):
    qc.h(i)

# Statevector (no measurement collapse)
sv = Statevector.from_instruction(qc)

# Probability of each computational basis state on the first n qubits
# Ancilla ends up in |-> regardless -> factor it out by tracing / summing over ancilla.
probs = sv.probabilities(list(range(n)))  # first n qubits
# Convert index -> bitstring (qiskit little-endian: bit 0 = LSB)
def idx_to_bits(idx, n):
    b = format(idx, f"0{n}b")  # msb-first
    return b

# Find top state
top_idx = int(np.argmax(probs))
top_bits = idx_to_bits(top_idx, n)
top_prob = float(probs[top_idx])

# Expected string is s (msb-first)
expected = s
match = (top_bits == expected)

result = {
    "algorithm": "Bernstein-Vazirani",
    "n": n,
    "hidden_string_s_msb_first": s,
    "recovered_bits_msb_first": top_bits,
    "recovered_probability": top_prob,
    "expected_bits": expected,
    "match": match,
    "num_qiskit_queries": 1,
    "note": "1 oracle query recovers s with P=1 on statevector (paper Sec. 3).",
}
print(json.dumps(result, indent=2))

# All probs for the reader
all_probs = {idx_to_bits(i, n): float(probs[i]) for i in range(2**n)}
result["all_probs"] = all_probs

with open("bv_result.json", "w") as f:
    json.dump(result, f, indent=2)
