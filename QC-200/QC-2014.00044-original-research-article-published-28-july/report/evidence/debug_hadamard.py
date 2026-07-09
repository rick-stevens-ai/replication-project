"""Diagnostic: apply the paper's adiabatic Hadamard to |0>_data ⊗ |0>_aux,
inspect the final state, and compare vs H|0>⊗|1> = |+>⊗|1> = (|0>+|1>)/√2 ⊗ |1>."""
import numpy as np
from scipy.linalg import expm
from adiabatic_qft_gates import H_hadamard, adiabatic_evolve, H_gate, fidelity

# input |0>_data ⊗ |0>_aux
psi_data = np.array([1, 0], dtype=complex)
psi0 = np.kron(psi_data, np.array([1, 0], dtype=complex))

for N in [500, 2000, 10000]:
    psi_f = adiabatic_evolve(H_hadamard, psi0, theta_f=np.pi, T=20.0, N=N)
    # Expected (from paper Eq 8 at θf=π): −(H|ψ⟩) ⊗ |1⟩ = −|+⟩⊗|1⟩
    target = -np.kron(H_gate @ psi_data, np.array([0, 1], dtype=complex))
    fid = fidelity(psi_f, target)
    print(f"N={N} fidelity={fid:.6f}")
    print(f"  psi_f = {np.round(psi_f, 4)}")
    print(f"  target= {np.round(target, 4)}")
