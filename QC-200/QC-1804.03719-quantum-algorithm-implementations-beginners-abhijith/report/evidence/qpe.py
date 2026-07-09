"""
Quantum Phase Estimation replication from Abhijith et al. 1804.03719 (phase estimation section).
Target: 1-qubit unitary U with a known eigenphase phi = 1/8 (i.e. eigenvalue exp(2*pi*i*1/8)).
Use t=4 counting qubits + 1 eigenstate qubit.
Because 2^t * phi = 16 * 1/8 = 2, an integer -> QPE yields |0010>_counting with P=1
(read as an integer, MSB-first == 2 -> binary '0010').

Paper text: for phases exactly expressible in t bits, QPE returns the phase with certainty.
"""
import json, math, numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
from qiskit.quantum_info import Statevector

phi = 1.0 / 8.0
t = 4  # counting qubits
# U = diag(1, exp(2*pi*i*phi))  -> its |1> eigenstate has eigenvalue exp(2*pi*i*phi)
theta = 2 * math.pi * phi
U = np.array([[1, 0], [0, np.exp(1j * theta)]], dtype=complex)

qc = QuantumCircuit(t + 1, t)  # last qubit is the eigenstate

# Prepare eigenstate |1>
qc.x(t)

# Hadamards on counting register
for q in range(t):
    qc.h(q)

# Controlled U^{2^j} applied from counting qubit j onto eigenstate qubit
for j in range(t):
    reps = 2 ** j
    U_pow = np.linalg.matrix_power(U, reps)
    gate = UnitaryGate(U_pow, label=f"U^{reps}").control(1)
    qc.append(gate, [j, t])

# Inverse QFT on counting register (Qiskit little-endian; measured as int the standard way)
def iqft(qc, n_qubits):
    # Swap qubits
    for q in range(n_qubits // 2):
        qc.swap(q, n_qubits - 1 - q)
    # Standard inverse QFT
    for j in range(n_qubits):
        for m in range(j):
            qc.cp(-math.pi / (2 ** (j - m)), m, j)
        qc.h(j)

iqft(qc, t)

sv = Statevector.from_instruction(qc)

# Probability of measurement outcomes on the counting register
probs = sv.probabilities(list(range(t)))  # first t qubits

# In qiskit little-endian: index i on counting register interpreted directly as int == measured value
top_idx = int(np.argmax(probs))
top_prob = float(probs[top_idx])
measured_phase = top_idx / (2 ** t)

# Expected integer y such that y / 2^t = phi -> y = 2 for phi=1/8, t=4 -> '0010' MSB-first
expected_int = int(round(phi * (2 ** t)))
expected_bits_msb_first = format(expected_int, f"0{t}b")

result = {
    "algorithm": "Quantum Phase Estimation",
    "counting_qubits": t,
    "true_phase": phi,
    "expected_measured_int": expected_int,
    "expected_bits_msb_first": expected_bits_msb_first,
    "measured_int": top_idx,
    "measured_phase": measured_phase,
    "measured_prob": top_prob,
    "match": (top_idx == expected_int) and (top_prob > 0.9999),
    "all_probs": {
        format(i, f"0{t}b"): float(probs[i]) for i in range(2 ** t)
    },
}
print(json.dumps(result, indent=2))

with open("qpe_result.json", "w") as f:
    json.dump(result, f, indent=2)
