"""
Grover search demo — reproduces the amplitude-amplification claim
Mosca surveys in Section 5 (Algorithms based on Amplitude Amplification).

Setup: N = 8 (n = 3 qubits), 1 marked item |w> = |101> (binary 5).
Optimal iteration count for exactly 1 marked item out of N:
    k_opt = floor((pi/4) * sqrt(N/M)) = floor((pi/4)*sqrt(8)) = 2
After k_opt applications of G = -H^n S_0 H^n O_w, the amplitude on |w>
should be very close to 1 (probability ~= 0.945 for k=2 vs. 0.125 initial).

Uses Qiskit 2.x, statevector simulation only (no shots, no noise).
"""
import json, math, sys
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

n = 3
N = 2 ** n
marked = 5  # |101>
M = 1
k_opt = int(math.floor((math.pi / 4.0) * math.sqrt(N / M)))
print(f"n={n} N={N} marked={marked} (bin {marked:0{n}b}) M={M} k_opt={k_opt}")


def oracle(qc: QuantumCircuit, marked_state: int, n: int) -> None:
    """Phase-flip oracle: |x> -> -|x> iff x == marked_state."""
    # Flip qubits where marked_state has a 0, so |marked> becomes |11..1>
    for q in range(n):
        if not ((marked_state >> q) & 1):
            qc.x(q)
    # Multi-controlled Z on |11..1>
    if n == 1:
        qc.z(0)
    else:
        qc.h(n - 1)
        qc.mcx(list(range(n - 1)), n - 1)
        qc.h(n - 1)
    # Undo the X flips
    for q in range(n):
        if not ((marked_state >> q) & 1):
            qc.x(q)


def diffuser(qc: QuantumCircuit, n: int) -> None:
    """Inversion about the mean: 2|s><s| - I where |s> = H^n|0>."""
    for q in range(n):
        qc.h(q)
        qc.x(q)
    if n == 1:
        qc.z(0)
    else:
        qc.h(n - 1)
        qc.mcx(list(range(n - 1)), n - 1)
        qc.h(n - 1)
    for q in range(n):
        qc.x(q)
        qc.h(q)


qc = QuantumCircuit(n)
# uniform superposition |s>
for q in range(n):
    qc.h(q)

for it in range(k_opt):
    oracle(qc, marked, n)
    diffuser(qc, n)

sv = Statevector.from_instruction(qc)
probs = np.abs(sv.data) ** 2

# Qiskit convention: statevector index i = decimal of bitstring with qubit 0 as LSB
p_marked = probs[marked]
amp_marked = complex(sv.data[marked])
print(f"P(|{marked:0{n}b}>) after k={k_opt} Grover iterations = {p_marked:.6f}")
print(f"amplitude on |{marked:0{n}b}> = {amp_marked}")
print("full probability distribution:")
for i, p in enumerate(probs):
    print(f"  |{i:0{n}b}>  P={p:.6f}")

# Theory: after k applications with theta = arcsin(sqrt(M/N)),
# amplitude on marked = sin((2k+1) theta), on non-marked = cos((2k+1) theta)/sqrt(N-1)
theta = math.asin(math.sqrt(M / N))
amp_theory = math.sin((2 * k_opt + 1) * theta)
p_theory = amp_theory ** 2
print(f"\nTheory: theta = arcsin(sqrt(1/8)) = {theta:.6f}")
print(f"Theory: amplitude on marked = sin({2*k_opt+1}*theta) = {amp_theory:.6f}")
print(f"Theory: P(marked)          = {p_theory:.6f}")

match = math.isclose(p_marked, p_theory, rel_tol=1e-6)
print(f"MATCH (sim vs theory, rel_tol=1e-6): {match}")

out = {
    "algorithm": "Grover",
    "n_qubits": n,
    "N": N,
    "M": M,
    "marked_state_decimal": marked,
    "marked_state_binary": f"{marked:0{n}b}",
    "k_optimal": k_opt,
    "k_formula": "floor((pi/4) * sqrt(N/M))",
    "p_marked_simulation": float(p_marked),
    "amp_marked_simulation": {"real": float(amp_marked.real), "imag": float(amp_marked.imag)},
    "theta_radians": theta,
    "amp_marked_theory": amp_theory,
    "p_marked_theory": p_theory,
    "match_theory": bool(match),
    "initial_prob_uniform": 1.0 / N,
    "gain_factor": float(p_marked) / (1.0 / N),
    "qiskit_version": __import__("qiskit").__version__,
    "circuit_depth": qc.depth(),
    "circuit_num_gates": len(qc.data),
}
with open("grover_N8_result.json", "w") as f:
    json.dump(out, f, indent=2)
print("\nWrote grover_N8_result.json")
sys.exit(0 if match else 1)
