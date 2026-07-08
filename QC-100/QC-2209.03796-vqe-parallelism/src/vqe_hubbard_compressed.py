#!/usr/bin/env python3
"""
Faithful reproduction of the physics target in arXiv:2209.03796
"Accelerating the variational quantum eigensolver using parallelism"
(Mineh & Montanaro, Phasecraft).

The paper's VQE problem is the COMPRESSED 2-site half-filled Hubbard model,
mapped to TWO qubits (their Eq. 1):

    H_C = -t (X⊗I + I⊗X) + (U/2)(I + Z⊗Z)

with t = 1, U = 2 (paper's chosen instance).

We:
  1. Build H_C exactly as a 4x4 matrix and as a Pauli operator.
  2. Compute the exact ground-state energy by diagonalization.
  3. Run a REAL VQE using the Hamiltonian-Variational (HV) ansatz described
     in the paper (Eq. 2): |psi> = exp(i theta H_hop) exp(i phi H_os) |psi0>,
     where |psi0> is the ground state of H_C at U=0, prepared as a state-vector.
     We optimize (theta, phi) classically on a statevector simulator.
  4. Compare exact vs VQE ground-state energy.

Everything runs on CPU with Qiskit statevector simulation. No hardware, no paid APIs.
"""
import json, time, sys
import numpy as np
from numpy.linalg import eigh

# ---- Pauli matrices ----
I2 = np.array([[1,0],[0,1]], dtype=complex)
X  = np.array([[0,1],[1,0]], dtype=complex)
Y  = np.array([[0,-1j],[1j,0]], dtype=complex)
Z  = np.array([[1,0],[0,-1]], dtype=complex)

def kron(a,b): return np.kron(a,b)

def build_HC(t=1.0, U=2.0):
    XI = kron(X, I2)
    IX = kron(I2, X)
    ZZ = kron(Z, Z)
    II = kron(I2, I2)
    H = -t*(XI + IX) + (U/2.0)*(II + ZZ)
    return H

def build_Hhop(t=1.0):
    return -t*(kron(X,I2) + kron(I2,X))

def build_Hos(U=2.0):
    return (U/2.0)*(kron(I2,I2) + kron(Z,Z))

def exact_ground(H):
    w, v = eigh(H)
    idx = int(np.argmin(w))
    return float(w[idx]), v[:, idx], w

def matexp(H, coeff):
    """exp(coeff * H) via eigendecomposition (H Hermitian)."""
    w, v = eigh(H)
    return v @ np.diag(np.exp(coeff * w)) @ v.conj().T

def hv_ansatz_state(theta, phi, psi0, Hhop, Hos):
    """|psi> = exp(i theta Hhop) exp(i phi Hos) |psi0>  (paper Eq. 2)."""
    U_os  = matexp(Hos,  1j*phi)
    U_hop = matexp(Hhop, 1j*theta)
    return U_hop @ (U_os @ psi0)

def energy(state, H):
    return float(np.real(state.conj().T @ (H @ state)))

def main():
    t, U = 1.0, 2.0
    H  = build_HC(t, U)
    Hhop = build_Hhop(t)
    Hos  = build_Hos(U)

    # Exact ground state of full H_C
    e0_exact, gs, spectrum = exact_ground(H)

    # |psi0> = ground state of H_C at U=0  (i.e. only hopping term -t(X⊗I+I⊗X))
    H_U0 = build_HC(t, 0.0)
    e0_U0, psi0, _ = exact_ground(H_U0)

    # ---- Real VQE over the HV ansatz (theta, phi) ----
    try:
        from scipy.optimize import minimize
        have_scipy = True
    except Exception:
        have_scipy = False

    def cost(params):
        theta, phi = params
        st = hv_ansatz_state(theta, phi, psi0, Hhop, Hos)
        return energy(st, H)

    best = None
    n_starts = 40
    rng = np.random.default_rng(2209)
    t_start = time.time()
    evals = 0
    if have_scipy:
        for _ in range(n_starts):
            x0 = rng.uniform(-np.pi, np.pi, size=2)
            res = minimize(cost, x0, method="COBYLA",
                           options={"maxiter": 500, "tol": 1e-9})
            evals += int(res.nfev) if hasattr(res, "nfev") else 0
            if best is None or res.fun < best["fun"]:
                best = {"fun": float(res.fun), "x": [float(v) for v in res.x]}
    else:
        # crude grid + refine fallback
        grid = np.linspace(-np.pi, np.pi, 200)
        for th in grid:
            for ph in grid:
                f = cost([th, ph]); evals += 1
                if best is None or f < best["fun"]:
                    best = {"fun": float(f), "x": [float(th), float(ph)]}
    wall = time.time() - t_start

    vqe_energy = best["fun"]
    abs_err = abs(vqe_energy - e0_exact)

    # ---- Also verify with a genuine Qiskit statevector circuit for the HV ansatz ----
    qiskit_check = None
    try:
        from qiskit import QuantumCircuit
        from qiskit.quantum_info import Statevector, SparsePauliOp, Operator
        # Build H_C as SparsePauliOp
        HC_op = SparsePauliOp.from_list([
            ("XI", -t), ("IX", -t), ("II", U/2.0), ("ZZ", U/2.0),
        ])
        # Confirm operator matches our matrix (endianness aside)
        # Build |psi0> circuit: since psi0 is a fixed statevector, initialize it.
        theta_opt, phi_opt = best["x"]
        # Reproduce the ansatz as unitaries applied to psi0 via Operator
        Uos  = Operator(matexp(Hos,  1j*phi_opt))
        Uhop = Operator(matexp(Hhop, 1j*theta_opt))
        qc = QuantumCircuit(2)
        qc.initialize(psi0, [0,1])
        qc.append(Uos.to_instruction(), [0,1])
        qc.append(Uhop.to_instruction(), [0,1])
        sv = Statevector(qc)
        e_qiskit = float(np.real(sv.expectation_value(HC_op)))
        # Also exact ground from qiskit operator
        mat = HC_op.to_matrix()
        wq, _ = np.linalg.eigh(mat)
        qiskit_check = {
            "vqe_energy_qiskit_statevector": e_qiskit,
            "exact_ground_from_qiskit_op": float(np.min(wq)),
            "operator_matches_numpy": bool(np.allclose(mat, H)),
        }
    except Exception as e:
        qiskit_check = {"error": repr(e)}

    out = {
        "paper": "arXiv:2209.03796",
        "model": "compressed 2-site half-filled Hubbard, mapped to 2 qubits (paper Eq.1)",
        "parameters": {"t": t, "U": U},
        "hamiltonian_HC_pauli": "-t(XI+IX) + (U/2)(II+ZZ)",
        "exact": {
            "ground_energy": e0_exact,
            "spectrum": [float(w) for w in spectrum],
            "ground_state_U0_energy": e0_U0,
        },
        "vqe": {
            "ansatz": "Hamiltonian-Variational (Eq.2): exp(i*theta*Hhop) exp(i*phi*Hos)|psi0>",
            "optimizer": "COBYLA" if have_scipy else "grid",
            "n_starts": n_starts if have_scipy else None,
            "n_cost_evals": evals,
            "wall_seconds": wall,
            "best_params_theta_phi": best["x"],
            "vqe_ground_energy": vqe_energy,
            "abs_error_vs_exact": abs_err,
            "chem_accuracy_1p6mHa_met": bool(abs_err < 1.6e-3),
        },
        "qiskit_statevector_check": qiskit_check,
    }
    print(json.dumps(out, indent=2))
    return out

if __name__ == "__main__":
    main()
