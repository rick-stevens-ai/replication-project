"""
Qiskit cross-check: build the TFIM Trotter circuits in Qiskit natively
(SparsePauliOp + PauliEvolutionGate + LieTrotter/SuzukiTrotter) and verify
they agree with our numpy expm reference, and count actual 2-qubit gates.
"""
import json
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import LieTrotter, SuzukiTrotter
from qiskit.quantum_info import SparsePauliOp, Operator
from scipy.linalg import expm

def tfim_op(n, J=1.0, h=1.0):
    """Build TFIM as SparsePauliOp:  H = -J sum Z Z  -  h sum X."""
    paulis = []
    coeffs = []
    for i in range(n - 1):
        s = ["I"] * n
        s[i] = "Z"; s[i + 1] = "Z"
        paulis.append("".join(reversed(s)))  # qiskit little-endian
        coeffs.append(-J)
    for i in range(n):
        s = ["I"] * n
        s[i] = "X"
        paulis.append("".join(reversed(s)))
        coeffs.append(-h)
    return SparsePauliOp(paulis, coeffs=coeffs)


def compare(n=3, t=1.0):
    H_op = tfim_op(n)
    H_mat = H_op.to_matrix()

    U_exact = expm(-1j * H_mat * t)

    results = []
    for r in [1, 2, 4, 8, 16, 32]:
        # LieTrotter (1st order)
        pe1 = PauliEvolutionGate(H_op, time=t, synthesis=LieTrotter(reps=r))
        qc1 = QuantumCircuit(n); qc1.append(pe1, range(n))
        qc1_t = transpile(qc1, basis_gates=["cx", "rx", "ry", "rz", "h", "s", "sdg"])
        U1 = Operator(qc1_t).data
        err1 = np.linalg.svd(U1 - U_exact, compute_uv=False)[0]
        cx1 = qc1_t.count_ops().get("cx", 0)

        # SuzukiTrotter order=2
        pe2 = PauliEvolutionGate(H_op, time=t, synthesis=SuzukiTrotter(order=2, reps=r))
        qc2 = QuantumCircuit(n); qc2.append(pe2, range(n))
        qc2_t = transpile(qc2, basis_gates=["cx", "rx", "ry", "rz", "h", "s", "sdg"])
        U2 = Operator(qc2_t).data
        err2 = np.linalg.svd(U2 - U_exact, compute_uv=False)[0]
        cx2 = qc2_t.count_ops().get("cx", 0)

        results.append({
            "reps": r,
            "trotter1_err": float(err1), "trotter1_cx": int(cx1),
            "trotter2_err": float(err2), "trotter2_cx": int(cx2),
        })
        print(f"reps={r:3d}: T1 err={err1:.4e} cx={cx1:4d} | T2 err={err2:.4e} cx={cx2:4d}")

    outdir = Path(__file__).resolve().parent.parent / "report" / "evidence"
    (outdir / "qiskit_check.json").write_text(json.dumps(results, indent=2))

    # Save example transpiled circuit
    r = 4
    pe1 = PauliEvolutionGate(H_op, time=t, synthesis=LieTrotter(reps=r))
    qc1 = QuantumCircuit(n); qc1.append(pe1, range(n))
    qc1_t = transpile(qc1, basis_gates=["cx", "rx", "ry", "rz", "h", "s", "sdg"])
    (outdir / "example_trotter1_r4.qasm").write_text(str(qc1_t.draw(output="text")))

    return results


if __name__ == "__main__":
    compare(n=3, t=1.0)
