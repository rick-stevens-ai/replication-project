#!/usr/bin/env python3
"""
Two supplementary checks:

(A) Toffoli vs paper-Toffoli phase relationship.
    Paper claims their reduced 3-qubit unitary is
        U_paper = exp(-i pi (sig_z1+1)(sig_z2+1) sig_x3 / 8),
    and comments "apart from phase-factors is equivalent to the C^2-NOT or Toffoli
    gate". We verify explicitly that U_paper = D * CCNOT for a diagonal phase D,
    where D applies a global phase only on the |11>_{12} control subspace.

(B) Gate-count comparison.
    The paper's central practical claim (implicit throughout, and quantitative
    in the C^n-NOT discussion) is that their SINGLE-Hamiltonian (or few-Hamiltonian)
    construction beats the Barenco-1995 decomposition of an n-Toffoli into
    O(n) 2-qubit CNOTs + single-qubit rotations.

    For the n=3 (regular Toffoli) case, we count gates in a standard decomposition
    Qiskit ships (6 CNOTs + 9 single-qubit gates = 15 elementary ops), vs the
    paper's construction which uses exactly ONE time-independent Hamiltonian
    turned on for duration tau = K*2*pi/Omega -> "1 pulse".

    For n=4 (Toffoli-4 / C^3-NOT), we do the same: measure the count in a
    Qiskit transpilation, then contrast with the paper's construction which
    uses (n_c + 1) = 4 pulses (one parallelogram side is shared, but each pulse
    in Eq. (6) is a distinct Hamiltonian).
"""
import json, numpy as np
from pathlib import Path
import qutip as qt

from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import MCXGate

OUT = Path(__file__).resolve().parent.parent / "report" / "evidence"
OUT.mkdir(parents=True, exist_ok=True)

# --- (A) phase relationship ---------------------------------------------------
sz = qt.sigmaz(); sx = qt.sigmax(); I2 = qt.qeye(2)
P1 = 0.5 * (I2 + sz)
op = (np.pi/2) * qt.tensor(P1, P1, sx)
U_paper = (-1j*op).expm().full()

CCNOT = np.array([
    [1,0,0,0,0,0,0,0],
    [0,1,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,0],
    [0,0,0,1,0,0,0,0],
    [0,0,0,0,1,0,0,0],
    [0,0,0,0,0,1,0,0],
    [0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,1,0],
], dtype=complex)

D = U_paper @ CCNOT.conj().T   # if U_paper = D CCNOT then D = U_paper CCNOT^dag
# Check diagonal
offdiag_norm = np.linalg.norm(D - np.diag(np.diag(D)))
diag = np.diag(D)
print("Phase relation U_paper = D * CCNOT")
print("  D diagonal? off-diag norm =", offdiag_norm)
print("  D diag entries:")
for i, z in enumerate(diag):
    b = format(i, '03b')
    print(f"    |{b}>: {z.real:+.6f} + {z.imag:+.6f}j   arg/pi = {np.angle(z)/np.pi:+.6f}")

# --- (B) gate counts ----------------------------------------------------------
gate_counts = {}
for n_controls in [2, 3]:
    n_qubits = n_controls + 1
    qc = QuantumCircuit(n_qubits)
    qc.append(MCXGate(n_controls), list(range(n_qubits)))
    # Transpile into a basic gate set {cx, u3} (well-known Barenco-flavor decomposition).
    qc_t = transpile(qc, basis_gates=["cx", "u3", "u2", "u1", "id"], optimization_level=3)
    counts = qc_t.count_ops()
    depth = qc_t.depth()
    n_cx = counts.get("cx", 0)
    n_1q = sum(v for k, v in counts.items() if k != "cx")
    gate_counts[f"C{n_controls}NOT"] = {
        "counts": dict(counts),
        "depth": depth,
        "cx_count": n_cx,
        "single_qubit_count": n_1q,
        "paper_pulse_count": (1 if n_controls == 2 else n_controls + 1),
        "paper_note": ("Single time-independent H (Eq. 5)"
                       if n_controls == 2
                       else f"n_c+1 = {n_controls+1} sequential Hamiltonians via Eq. (6)")
    }
    print(f"\nC^{n_controls}-NOT ({n_qubits} qubits):")
    print(f"  Qiskit transpiled counts: {dict(counts)}")
    print(f"  Depth = {depth}, CNOTs = {n_cx}, single-qubit gates = {n_1q}")
    print(f"  Paper's pulse count = {gate_counts[f'C{n_controls}NOT']['paper_pulse_count']}")

out = {
    "phase_relation_U_paper_vs_CCNOT": {
        "D_offdiag_norm": float(offdiag_norm),
        "D_diagonal_entries_arg_over_pi": [float(np.angle(z)/np.pi) for z in diag],
        "D_diagonal_entries": [{"real": float(z.real), "imag": float(z.imag)} for z in diag],
    },
    "gate_counts": gate_counts,
}
with open(OUT/"toffoli_phase_and_gatecount.json", "w") as f:
    json.dump(out, f, indent=2)
print("\nWrote", OUT/"toffoli_phase_and_gatecount.json")
