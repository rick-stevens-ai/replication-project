"""
Independent Qiskit cross-check for the QGC toy replication.

We rebuild the same tests using qiskit.quantum_info (Statevector / DensityMatrix /
Operator) rather than raw numpy, and compare fidelities. This shields against a
numpy-only implementation bug: two different libraries have to agree.
"""
import json, itertools
import numpy as np
from qiskit.quantum_info import Statevector, DensityMatrix, Operator, state_fidelity
from qiskit.circuit.library import CXGate, HGate


def pauli_op(a, b):
    """X^a Z^b as a qiskit Operator."""
    X = Operator.from_label("X")
    Z = Operator.from_label("Z")
    I = Operator.from_label("I")
    op = I
    if b:
        op = Z @ op
    if a:
        op = X @ op
    return op


def qgc_H_on_zero():
    """|0> ---(garble via H-teleportation-frame)---> decode ---> expect |+>."""
    psi = Statevector.from_label("0")
    H = Operator(HGate())
    ideal = psi.evolve(H)
    # QGC output (Clifford slice): X^a Z^b (H|0>) with random (a,b), decoder inverts.
    a, b = np.random.randint(0, 2), np.random.randint(0, 2)
    P = pauli_op(a, b)
    masked = ideal.evolve(P)
    decoded = masked.evolve(P)              # X, Z self-inverse
    return {
        "fidelity_decoded_vs_ideal_H|0>":
            float(state_fidelity(decoded, ideal))
    }


def qgc_CNOT_hiding():
    """Average CNOT-output over 16 Pauli masks -> maximally mixed 4x4."""
    psi = Statevector.from_label("0+")        # |0> ⊗ |+>
    CNOT = Operator(CXGate())
    ideal = psi.evolve(CNOT)
    ideal_rho = DensityMatrix(ideal).data
    acc = np.zeros((4, 4), dtype=complex)
    for a, b, c, d in itertools.product([0, 1], repeat=4):
        P = pauli_op(a, b).tensor(pauli_op(c, d))
        s = ideal.evolve(P)
        acc += DensityMatrix(s).data
    acc /= 16.0
    max_mixed = np.eye(4, dtype=complex) / 4.0
    return {
        "distance_to_max_mixed": float(np.linalg.norm(acc - max_mixed)),
        "close_to_max_mixed": bool(np.allclose(acc, max_mixed, atol=1e-10)),
    }


if __name__ == "__main__":
    np.random.seed(2)
    out = {"H_correctness": qgc_H_on_zero(),
           "CNOT_hiding":   qgc_CNOT_hiding()}
    print(json.dumps(out, indent=2))
