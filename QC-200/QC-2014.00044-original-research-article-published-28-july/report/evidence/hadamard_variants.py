"""
Try 4 sign-convention variants of the paper's Hadamard Hamiltonian to see which
(if any) reproduces the textbook Hadamard on the data qubit.

Motivation: with the equations exactly as printed in Hen 2014 Eqs. (3)-(5), the
adiabatic gate does drive the aux to |1> at ~99.5% (Trotter-limited) but the
resulting data-register operator is NOT the textbook Hadamard — random-input
fidelities scatter over 0.05..0.52. This is diagnostic of a sign-typo somewhere
in the paper: either in one of the H_x / H_-y Pauli signs, or in the projector
decomposition.
"""
import numpy as np
from scipy.linalg import expm
from adiabatic_qft_gates import (I2, X, Y, Z, Pyp, Pym, kron, H_gate,
                                  adiabatic_evolve, target_state_gate, fidelity,
                                  data_conditioned_on_aux1)

variants = {
    "as_printed (H_x=-cZ-sX, H_-y=-cZ+sY)":
        lambda th: kron(Pyp, -np.cos(th)*Z - np.sin(th)*X) + kron(Pym, -np.cos(th)*Z + np.sin(th)*Y),
    "H_-y sign-flipped (H_x=-cZ-sX, H_-y=-cZ-sY)":
        lambda th: kron(Pyp, -np.cos(th)*Z - np.sin(th)*X) + kron(Pym, -np.cos(th)*Z - np.sin(th)*Y),
    "swap subspaces (H_x with -y, H_-y with +y)":
        lambda th: kron(Pym, -np.cos(th)*Z - np.sin(th)*X) + kron(Pyp, -np.cos(th)*Z + np.sin(th)*Y),
    "H_x uses +sX (H_x=-cZ+sX, H_-y=-cZ-sY)":
        lambda th: kron(Pyp, -np.cos(th)*Z + np.sin(th)*X) + kron(Pym, -np.cos(th)*Z - np.sin(th)*Y),
    "swap + H_-y sign-flipped":
        lambda th: kron(Pym, -np.cos(th)*Z - np.sin(th)*X) + kron(Pyp, -np.cos(th)*Z - np.sin(th)*Y),
}

# fixed representative input: |ψ> = (α|0>+β|1>) with α=0.6+0.2j, β=0.5-0.4j (normalized)
rng = np.random.default_rng(7)
inputs = []
for _ in range(4):
    v = rng.standard_normal(2) + 1j * rng.standard_normal(2)
    v = v / np.linalg.norm(v)
    inputs.append(v)

for name, H_func in variants.items():
    print(f"\n--- {name} ---")
    fids = []
    for v in inputs:
        psi0 = np.kron(v, np.array([1, 0], dtype=complex))
        psi_f = adiabatic_evolve(H_func, psi0, theta_f=np.pi, T=20.0, N=2000)
        data_out, p1 = data_conditioned_on_aux1(psi_f, data_qubits=1)
        target = H_gate @ v
        fid = abs(np.vdot(data_out, target)) ** 2
        fids.append(fid)
        print(f"  in={np.round(v, 3)}  fid_proj(aux=1)={fid:.6f}  P(aux=1)={p1:.6f}")
    print(f"  mean fidelity across {len(inputs)} random inputs = {np.mean(fids):.6f}")
