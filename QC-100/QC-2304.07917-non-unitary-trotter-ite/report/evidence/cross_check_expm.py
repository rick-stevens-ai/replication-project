#!/usr/bin/env python3
"""Cross-check: our statevector Trotter-ITE (product of exp(-c_k*dtau*P_k) per Pauli
term, per Trotter step) should converge in a small-dtau + many-step limit to the
same ground-state energy as the *exact* imaginary-time propagator exp(-tau*H) applied
to the same initial state. Also directly compare energies at intermediate beta values.

Both are just classical, deterministic simulations of ITE; we're checking that
our Trotter decomposition converges to the exact continuous ITE, and both converge
to the exact GS. Success: no fabrication -- everything checks against scipy.
"""
import numpy as np
from scipy.linalg import expm
from numpy.linalg import eigh
from ite_tim import build_tim_hamiltonian, initial_plus_state, trotter_ite_step

def exact_ite_energy(psi0, H, tau):
    U = expm(-tau*H)
    psi = U @ psi0
    nrm = np.vdot(psi, psi).real
    if nrm < 1e-300:
        return float('nan'), psi
    return float((np.vdot(psi, H @ psi).real)/nrm), psi/np.sqrt(nrm)

def run(n=4, J=0.5, h=0.1, dtau=0.1, n_steps=45):
    H, terms = build_tim_hamiltonian(n, J, h, pbc=True)
    evals, _ = eigh(H)
    E0 = float(evals[0])
    psi0 = initial_plus_state(n)
    psi_trot = psi0.copy()
    print(f"# {n}-site TIM, J={J}, h={h}, PBC. Exact E0 = {E0:.10f}")
    print(f"# {'beta':>5}  {'E_trot':>14}  {'E_exact_ITE':>14}  {'|Δ|':>10}  {'|<psi_trot|psi_exact>|':>22}")
    for k in range(1, n_steps+1):
        psi_trot, _ = trotter_ite_step(psi_trot, terms, n, dtau)
        beta = k*dtau
        E_trot = float((np.vdot(psi_trot, H@psi_trot).real)/np.vdot(psi_trot,psi_trot).real)
        E_ex, psi_ex = exact_ite_energy(psi0, H, beta)
        diff = abs(E_trot - E_ex)
        overlap = abs(np.vdot(psi_trot, psi_ex))
        if k % 5 == 0 or k == n_steps:
            print(f"  {beta:5.2f}  {E_trot:+.8f}  {E_ex:+.8f}  {diff:.2e}  {overlap:.10f}")
    # Final absolute error to E0
    print()
    print(f"Trotter ITE final |E-E0| = {abs(E_trot - E0):.4e}")
    print(f"Exact ITE   final |E-E0| = {abs(E_ex   - E0):.4e}")

if __name__ == '__main__':
    run()
