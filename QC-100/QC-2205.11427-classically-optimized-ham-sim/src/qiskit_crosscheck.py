"""Qiskit cross-check.

Independently rebuild the same L=2 optimized brickwall circuit for t=0.2 using
Qiskit's rx / rz / rzz primitives and confirm the resulting unitary matches
our pure-numpy ansatz to numerical precision. Also confirm the Trotter II
circuit at n_reps=2 matches. This proves the numpy 'unitary' is a
faithful representation of a real Qiskit-executable circuit.

We regenerate optimized params here (cheap n=3 L=2 problem).
"""

from __future__ import annotations

import numpy as np
from scipy.linalg import expm
from scipy.optimize import minimize

from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

import replicate as rep


def qiskit_brickwall(n, thetas, n_layers):
    """Build the same brickwall ansatz with Qiskit rx/rz/rzz gates.

    Qiskit convention:
        rx(theta) = exp(-i theta X / 2)   -- same as paper Rx
        rz(theta) = exp(-i theta Z / 2)   -- same as paper Rz
        rzz(theta) = exp(-i theta Z tensor Z / 2)  -- same as paper Uzz

    Our numpy code uses qubit-0-on-the-LEFT (most significant) kron order.
    Qiskit uses qubit-0-on-the-RIGHT (little-endian). After bit-reversing
    the Qiskit unitary rows/cols, paper qubit k maps DIRECTLY to Qiskit
    qubit k (verified empirically). So we use the same index in both.
    """
    def q(k):
        return k

    # Numpy applies Rz(a) @ Rx(b) @ Rz(c) as MATRIX product; on a state, that
    # means the *rightmost* factor Rz(c) is applied FIRST. Qiskit .rz/.rx are
    # applied in temporal ORDER (first appended = first applied). So to match
    # numpy semantics we must reverse: Rz(c), Rx(b), Rz(a).
    qc = QuantumCircuit(n)
    idx = 0
    for _ in range(n_layers):
        for k in range(n):
            a = thetas[idx + 3 * k]
            b = thetas[idx + 3 * k + 1]
            c = thetas[idx + 3 * k + 2]
            qc.rz(c, q(k))
            qc.rx(b, q(k))
            qc.rz(a, q(k))
        idx += 3 * n
        for k in range(n - 1):
            qc.rzz(thetas[idx + k], q(k), q(k + 1))
        idx += (n - 1)
    for k in range(n):
        a = thetas[idx + 3 * k]
        b = thetas[idx + 3 * k + 1]
        c = thetas[idx + 3 * k + 2]
        qc.rz(c, q(k))
        qc.rx(b, q(k))
        qc.rz(a, q(k))
    return qc


def qiskit_trotter_II(n, t, J=2.0, g=1.0, h=1.0, n_reps=1):
    qc = QuantumCircuit(n)
    tau = t / n_reps
    for _ in range(n_reps):
        # exp(-i tau H_X/2) = product rx(tau*g)  (angle = 2*(tau/2)*g)
        for k in range(n):
            qc.rx(tau * g, k)
        # exp(-i tau H_Z)
        for k in range(n):
            qc.rz(2 * tau * h, k)
        for k in range(n - 1):
            qc.rzz(2 * tau * J, k, k + 1)
        # exp(-i tau H_X/2)
        for k in range(n):
            qc.rx(tau * g, k)
    return qc


def _qiskit_unitary_paper_order(qc):
    """Qiskit's Operator uses little-endian qubit-0-on-the-right convention.

    Our numpy code uses qubit-0-on-the-left (kron order). To compare, we
    reverse the Qiskit unitary's qubit order.
    """
    n = qc.num_qubits
    U_le = Operator(qc).data  # little-endian
    # reverse bit order of both rows and columns
    dim = 2 ** n
    perm = np.array([int(bin(i)[2:].zfill(n)[::-1], 2) for i in range(dim)])
    return U_le[np.ix_(perm, perm)]


def main():
    n = 3
    t = 0.2

    H = rep.build_H(n)
    U_target = expm(-1j * t * H)

    # 1) Trotter II cross-check
    U_trot_np = rep.trotter_II(n, t, n_reps=2)
    U_trot_qk = _qiskit_unitary_paper_order(qiskit_trotter_II(n, t, n_reps=2))
    diff_trot = np.linalg.norm(U_trot_np - U_trot_qk)
    print(f"Trotter II n_reps=2  ||numpy - qiskit||_F = {diff_trot:.3e}")
    e_np = rep.eps_approx(U_trot_np, U_target, n)
    e_qk = rep.eps_approx(U_trot_qk, U_target, n)
    print(f"  eps_approx  numpy={e_np:.6e}   qiskit={e_qk:.6e}")

    # 2) Optimize L=2 brickwall and cross-check
    print("\nOptimizing L=2 brickwall (n=3, t=0.2) for cross-check...")
    theta, err, _ = rep.optimize_brickwall(n, t, 2, H, n_restarts=4, seed=42)
    print(f"  optimized eps = {err:.6e}, nparam = {len(theta)}")
    U_ans_np = rep.brickwall_ansatz(n, theta, 2)
    qc = qiskit_brickwall(n, theta, 2)
    U_ans_qk = _qiskit_unitary_paper_order(qc)
    diff_ans = np.linalg.norm(U_ans_np - U_ans_qk)
    print(f"Brickwall L=2  ||numpy - qiskit||_F = {diff_ans:.3e}")
    e_np = rep.eps_approx(U_ans_np, U_target, n)
    e_qk = rep.eps_approx(U_ans_qk, U_target, n)
    print(f"  eps_approx  numpy={e_np:.6e}   qiskit={e_qk:.6e}")

    print(f"\nQiskit brickwall QASM-ish gate count:")
    print(f"  depth = {qc.depth()}, size = {qc.size()}, ops = {dict(qc.count_ops())}")
    print(f"\nCircuit (first 30 lines of QASM):")
    from qiskit.qasm3 import dumps
    q3 = dumps(qc)
    print("\n".join(q3.splitlines()[:30]))

    # Save cross-check summary
    import json
    from pathlib import Path
    Path("report/evidence").mkdir(parents=True, exist_ok=True)
    with open("report/evidence/qiskit_crosscheck.json", "w") as f:
        json.dump({
            "n": n, "t": t,
            "trotterII_reps2_diff_np_vs_qiskit": diff_trot,
            "trotterII_eps_numpy": e_np, "trotterII_eps_qiskit": e_qk,
            "opt_L2_diff_np_vs_qiskit": diff_ans,
            "opt_L2_eps": err,
            "opt_L2_qiskit_gate_counts": {str(k): int(v) for k, v in qc.count_ops().items()},
            "opt_L2_qiskit_depth": qc.depth(),
        }, f, indent=2)
    with open("report/evidence/opt_L2_qiskit_circuit.qasm", "w") as f:
        f.write(q3)


if __name__ == "__main__":
    main()
