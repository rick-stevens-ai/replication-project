"""
Cross-check: build a real Qiskit circuit for one (n, t, p) case and compare
the counting-register measurement distribution to our analytic QPE formula.

This validates that the analytic approach used in quantum_counting.py is
faithful to a gate-level implementation of Count(F,P).
"""
import math
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFT, UnitaryGate
from qiskit_aer import AerSimulator
from qiskit import transpile

import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from quantum_counting import grover_operator, quantum_counting_statevector


def build_count_circuit(n, marked, p_counting):
    """Build the Count(F, P) circuit gate-level:
      - p_counting counting qubits
      - n search qubits
      - init: H on counting, H on search
      - controlled-G^{2^k} for k=0..p-1
      - iQFT on counting register
      - measure counting register (analytically here via statevector)
    """
    N = 1 << n
    P = 1 << p_counting

    # Build G as a unitary
    G = grover_operator(n, marked)

    # Precompute G^(2^k) matrices (small n)
    G_powers = [G.copy()]
    for k in range(1, p_counting):
        G_powers.append(G_powers[-1] @ G_powers[-1])

    count_reg = QuantumRegister(p_counting, "c")
    search_reg = QuantumRegister(n, "s")
    qc = QuantumCircuit(count_reg, search_reg)

    # Init
    qc.h(count_reg)
    qc.h(search_reg)

    # Qiskit little-endian: for a gate applied to qubits [q_0, q_1, ..., q_{n-1}]
    # (this exact args list), the gate matrix indexes basis states with q_0 as LSB
    # of the row/col index. To use the convenient block form
    #   full = block_diag(I, U)   ("control off => I;  control on => U")
    # the control qubit must be the MSB of the gate's index, i.e. the LAST entry
    # in the args list. Verified against hand-coded QPE.
    #
    # Convention: count_reg[j] controls U^{2^j}. iQFT (with swaps) on the counting
    # register then produces integer f with little-endian reading: count_reg[0] = LSB.
    for j in range(p_counting):
        U = G_powers[j]
        dim = U.shape[0]
        full = np.zeros((2 * dim, 2 * dim), dtype=complex)
        full[0:dim, 0:dim] = np.eye(dim, dtype=complex)
        full[dim:2 * dim, dim:2 * dim] = U
        cU = UnitaryGate(full, label=f"cG^{2**j}")
        # control LAST => it becomes MSB of the gate matrix indexing.
        qc.append(cU, list(search_reg) + [count_reg[j]])

    # Inverse QFT on counting register (with swaps).
    iqft = QFT(num_qubits=p_counting, do_swaps=True, inverse=True)
    qc.append(iqft.to_gate(label="iQFT"), list(count_reg))

    return qc


def marginal_over_counting(statevec, n_counting, n_search):
    """Compute the marginal probability distribution over the counting register
    from a full statevector.
    Qiskit qubit ordering: statevec is indexed by integer i = sum_j bit_j * 2^j
    where qubit 0 is the least-significant bit. Our circuit put count_reg first,
    so count_reg qubits are 0..p-1 (least significant), search 0..n-1 are next.
    """
    P = 1 << n_counting
    N = 1 << n_search
    probs = np.abs(statevec) ** 2
    dist = np.zeros(P)
    for i in range(len(probs)):
        c_idx = i & (P - 1)         # low p bits
        dist[c_idx] += probs[i]
    return dist


def main():
    from qiskit.quantum_info import Statevector

    # Test case: n=4, t=3 marked items, p=5 counting qubits
    n = 4
    marked = [1, 5, 11]
    p = 5

    qc = build_count_circuit(n, marked, p)
    sv = Statevector.from_instruction(qc)
    dist_gate = marginal_over_counting(np.asarray(sv.data), p, n)

    dist_ana = quantum_counting_statevector(n, marked, p)

    diff = float(np.max(np.abs(dist_gate - dist_ana)))
    print(f"Case n={n}, t={len(marked)}, p={p}")
    print(f"L∞ diff between gate-level and analytic marginals: {diff:.2e}")
    print(f"Top-5 f from gate-level:")
    top_gate = np.argsort(-dist_gate)[:5]
    for f in top_gate:
        print(f"  f={f}: gate={dist_gate[f]:.6f}, ana={dist_ana[f]:.6f}")
    print(f"argmax gate={int(np.argmax(dist_gate))}, argmax analytic={int(np.argmax(dist_ana))}")
    ok = diff < 1e-6
    print(f"AGREE (L∞ < 1e-6): {ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
