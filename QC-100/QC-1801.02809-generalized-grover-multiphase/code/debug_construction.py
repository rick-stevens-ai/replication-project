#!/usr/bin/env python3
"""Debug the Eq.12 construction: verify the constructed initial state truly
lives in the 2D span of {|eps_1^+>, |eps_1^->} and produces the predicted
oscillation period ~ pi/(2 c_1) in continuous time, and near it in the
gate iteration."""

import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generalized_grover import (
    random_orthonormal_source_states, build_projector,
    target_basis_projector, unitary_from_projector,
    run_grover_iterations, construct_initial_state_eq12,
)

RNG_SEED = 20260703
rng = np.random.default_rng(RNG_SEED)

n_qubits = 5
D = 2**n_qubits
N = 5
M = 5
target_indices = list(range(M))

psi = random_orthonormal_source_states(D, N, target_indices, rng)
P_S = build_projector(psi)
P_T = target_basis_projector(D, target_indices)
P_Tbar = np.eye(D) - P_T
H_gen = P_S + P_T                     # continuous-time Grover Hamiltonian, Eq. 1
U_G = unitary_from_projector(P_S)
U_O = unitary_from_projector(P_T)

# Diagonalize H_gen directly, look at spectrum
w, V = np.linalg.eigh(H_gen)
print("H_gen eigenvalues (sorted):")
print(np.round(w, 6))
# per Eq. 10, we expect eigenvalues 1 +/- |c_n| in pairs, and eigenvalue 1
# for the |N-M|=0 unpaired states, and 0 for the rest.

# Now build |Psi_1(t=0)>
Psi_init, c1 = construct_initial_state_eq12(psi, D, target_indices)
print(f"c1 = {c1}")
# Expected pair: 1 +/- c1
print(f"Expected paired eigenvalues: {1+c1:.6f}, {1-c1:.6f}")

# Project Psi_init onto energy eigenbasis of H_gen
coeffs = V.conj().T @ Psi_init
print("|coeffs|^2 across eigenmodes (top 10 nonzero):")
support = np.argsort(-np.abs(coeffs)**2)
for i in support[:10]:
    print(f"  E={w[i]:+.6f}  |coeff|^2={abs(coeffs[i])**2:.6f}")

# CONTINUOUS-TIME evolution: does Psi_init give a clean Rabi oscillation?
from scipy.linalg import expm
print("\nContinuous-time evolution P_T(t):")
t_vals = np.linspace(0, np.pi / c1, 25)
for t in t_vals:
    U_t = expm(-1j * H_gen * t)
    st = U_t @ Psi_init
    p = float(np.real(st.conj() @ P_T @ st))
    print(f"  t={t:.4f}  P_T={p:.4f}")

# Gate-based iteration:  G*O per step. What's the effective per-step angle?
# For pure Grover-like 2-state rotation, one iteration ~ evolves by ~2*|c_n|.
# So expected k_peak = pi / (2 * |c_n|).
print(f"\nExpected k_peak (gate): pi/(2*|c1|) = {np.pi/(2*c1):.2f}")
probs = run_grover_iterations(Psi_init, U_G, U_O, P_T, 40)
print("P_T after k gate iterations (every k):")
for k, p in enumerate(probs):
    print(f"  k={k:2d}  P_T={p:.4f}")
