"""
Fig 9 reading uncertainty: the ancilla gate sequence is
   H T H . T† H T . H T H  (dots = CNOTs).
The paper's figure shows "|ψ⟩ - . - . Z". We assumed dots on ancilla row are
CONTROLS and data row is TARGET (CX ancilla->data). Try also the reverse
(CX data->ancilla) and the Z placement before/after the second CNOT.
Also try Fig 1a interpretation with H's on data qubit for phase gadget style.
"""
import itertools, numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

I2 = np.eye(2, dtype=complex)
Z  = np.array([[1,0],[0,-1]], dtype=complex)
V3 = (I2 + 2j*Z)/np.sqrt(5)

def analyse(qc, target=V3):
    W = Operator(qc).data
    # data qubit = 0, ancilla = 1 (little-endian)
    K = np.array([[W[0,0], W[0,1]], [W[1,0], W[1,1]]], dtype=complex)
    p = 0.5 * np.real(np.trace(K.conj().T @ K))
    if p < 1e-12: return None
    Kn = K / np.sqrt(p)
    # match up to global phase
    idx = np.unravel_index(np.argmax(np.abs(target)), target.shape)
    phase = Kn[idx] / target[idx] if abs(target[idx]) > 1e-12 else None
    if phase is None: return None
    phase = phase / abs(phase)
    diff = np.linalg.norm(Kn - target*phase)
    return p, diff

# Try different Fig 9 variants
variants = []

def build(cx_dir, z_pos):
    qc = QuantumCircuit(2)
    a, d = 1, 0
    def CX():
        if cx_dir == 'a2d': qc.cx(a, d)
        else: qc.cx(d, a)
    qc.h(a); qc.t(a); qc.h(a)
    CX()
    qc.tdg(a); qc.h(a); qc.t(a)
    CX()
    qc.h(a); qc.t(a); qc.h(a)
    if z_pos == 'after':
        qc.z(d)
    elif z_pos == 'before2':
        # put Z on data before second CX — impossible now, rebuild
        pass
    return qc

for cx_dir in ['a2d', 'd2a']:
    for z_pos in ['after', 'none']:
        qc = build(cx_dir, z_pos)
        r = analyse(qc)
        if r:
            print(f"cx={cx_dir}, z={z_pos}: p={r[0]:.4f}, diff={r[1]:.4f}")

# Try also swapping which qubit is ancilla vs data
print("\nSwap ancilla/data roles:")
def build_swap(cx_dir, z_pos):
    qc = QuantumCircuit(2)
    a, d = 0, 1   # ancilla = qubit 0 = LSB
    def CX():
        if cx_dir == 'a2d': qc.cx(a, d)
        else: qc.cx(d, a)
    qc.h(a); qc.t(a); qc.h(a)
    CX()
    qc.tdg(a); qc.h(a); qc.t(a)
    CX()
    qc.h(a); qc.t(a); qc.h(a)
    if z_pos == 'after':
        qc.z(d)
    return qc

for cx_dir in ['a2d', 'd2a']:
    for z_pos in ['after', 'none']:
        qc = build_swap(cx_dir, z_pos)
        W = Operator(qc).data
        # Now ancilla=qubit0 (LSB), success = state indices where LSB=0 -> indices 0 and 2
        K = np.array([[W[0,0], W[0,2]], [W[2,0], W[2,2]]], dtype=complex)
        p = 0.5*np.real(np.trace(K.conj().T @ K))
        Kn = K / np.sqrt(p) if p > 0 else K
        idx = np.unravel_index(np.argmax(np.abs(V3)), V3.shape)
        phase = Kn[idx] / V3[idx] if abs(V3[idx]) > 1e-12 else 1
        phase = phase / abs(phase) if abs(phase) > 0 else 1
        diff = np.linalg.norm(Kn - V3*phase)
        print(f"cx={cx_dir}, z={z_pos}: p={p:.4f}, diff-to-V3={diff:.4f}")
