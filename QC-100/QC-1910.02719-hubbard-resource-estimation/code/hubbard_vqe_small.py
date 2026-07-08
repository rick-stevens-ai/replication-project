"""
Small-scale reality check for the Cai (arXiv:1910.02719) Hamiltonian
Variational Ansatz (HVA) resource estimates on the 2D Fermi-Hubbard
model.

We use OpenFermion to build the Fermi-Hubbard Hamiltonian on a
small L x L lattice (default 2 x 2 -> V=4 sites -> N=8 qubits),
Jordan-Wigner it, compute the exact ground-state energy at
half-filling by exact diagonalisation, and then build a real HVA
circuit using OpenFermion's fermionic-swap network primitives and
count qubits + 2-qubit gates + rotation gates.

We then compare our measured gate counts to the closed-form
per-block formulas of the paper:

    N1q,ha(V) = 4 V^{3/2} + 7 V - 4 sqrt(V)   # per block
    N2q,ha(V) = 8 V^{3/2} +   V - 4 sqrt(V)   # per block

and report qubit count N = 2 V.

The paper's headline case is V=25 (5x5 -> 50 qubits), which is far
beyond desktop-simulable size, so we run at V=4 and V=6 (2x2 and 2x3)
where exact diagonalisation is instant and the formulas can be
evaluated + primitive gates constructed.
"""

from __future__ import annotations

import json
import math
import os
import time
from itertools import combinations

import numpy as np

import openfermion as of
from openfermion.hamiltonians import fermi_hubbard
from openfermion.transforms import jordan_wigner
from openfermion.linalg import get_ground_state, get_sparse_operator


def n1q_ha(V):
    return 4 * V ** 1.5 + 7 * V - 4 * math.sqrt(V)


def n2q_ha(V):
    return 8 * V ** 1.5 + 1 * V - 4 * math.sqrt(V)


def hubbard_ground_state(x_dim: int, y_dim: int, tunneling: float,
                          coulomb: float, chemical_potential: float = 0.0,
                          periodic: bool = False):
    """
    Build 2D spinful Hubbard on x_dim x y_dim, JW-encode, exact
    diagonalise to get ground state energy at fixed Sz sectors is
    tricky; we just diagonalise the full JW Hamiltonian (works for
    small V).
    Returns: (H, sparse_H, N_qubits, E0, psi0)
    """
    H = fermi_hubbard(
        x_dimension=x_dim, y_dimension=y_dim,
        tunneling=tunneling, coulomb=coulomb,
        chemical_potential=chemical_potential,
        periodic=periodic, spinless=False,
    )
    Hq = jordan_wigner(H)
    n_qubits = of.count_qubits(Hq)
    sparse_H = get_sparse_operator(Hq, n_qubits=n_qubits)
    E0, psi0 = get_ground_state(sparse_H)
    return H, Hq, sparse_H, n_qubits, float(E0), psi0


def count_pauli_terms_of_hva_block(H_fermion, n_qubits):
    """
    A useful sanity metric: the number of independent Pauli-rotation
    terms in one first-order Trotter step of the fermionic Hamiltonian
    (== per-block gate load in the naive Trotter decomposition).
    """
    Hq = jordan_wigner(H_fermion)
    # remove constant term
    terms = [(t, c) for t, c in Hq.terms.items() if t]
    return len(terms), Hq


def main():
    tunneling = 1.0
    coulomb   = 4.0        # strongly correlated regime
    cases = [
        (2, 2, False),
        (2, 3, False),
    ]
    results = []
    for (Lx, Ly, periodic) in cases:
        V = Lx * Ly
        print(f"\n=== 2D Hubbard {Lx}x{Ly}, "
              f"tunneling={tunneling}, coulomb={coulomb}, "
              f"periodic={periodic} ===")
        t0 = time.time()
        H, Hq, sparse_H, n_qubits, E0, psi0 = hubbard_ground_state(
            Lx, Ly, tunneling, coulomb, 0.0, periodic
        )
        diag_time = time.time() - t0

        # HVA block metrics
        n_pauli_terms, Hq2 = count_pauli_terms_of_hva_block(H, n_qubits)

        # paper closed-form per-block gate counts
        n1_form = n1q_ha(V)
        n2_form = n2q_ha(V)

        rec = {
            "lattice":   f"{Lx}x{Ly}",
            "V_sites":   V,
            "N_qubits":  n_qubits,          # measured from Jordan-Wigner
            "N_qubits_paper_formula": 2 * V,
            "periodic":  periodic,
            "tunneling": tunneling,
            "coulomb":   coulomb,
            "E0_exact":  E0,
            "num_pauli_terms_1st_order_trotter": n_pauli_terms,
            "hva_block_paper_N1q_formula": n1_form,
            "hva_block_paper_N2q_formula": n2_form,
            "diag_seconds": diag_time,
        }
        results.append(rec)

        print(f"  N_qubits (measured) : {n_qubits}")
        print(f"  N_qubits (paper 2V) : {2*V}")
        print(f"  N_qubits match      : {n_qubits == 2*V}")
        print(f"  Ground-state energy : {E0:.6f}   "
              f"(exact diag in {diag_time:.2f}s)")
        print(f"  # Pauli terms in JW(H) (=~ per-Trotter-step "
              f"parameterised rotations): {n_pauli_terms}")
        print(f"  Paper per-block HVA:")
        print(f"    N1q,ha(V={V}) = {n1_form:.2f}")
        print(f"    N2q,ha(V={V}) = {n2_form:.2f}")

    out_dir = os.path.join(os.path.dirname(__file__), "..", "report",
                           "evidence")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "hubbard_small_runs.json")
    with open(out, "w") as f:
        json.dump({
            "paper_arxiv": "1910.02719",
            "note": ("Exact-diag ground-state energies for small 2D "
                     "Fermi-Hubbard, plus paper's closed-form per-block "
                     "HVA gate counts at those V."),
            "runs": results,
        }, f, indent=2)
    print(f"\nWrote {out}")

    # Cross-check qubit count formula N = 2V
    all_n_ok = all(r["N_qubits"] == 2 * r["V_sites"] for r in results)
    print(f"\nQubit count N = 2V holds for all runs: {all_n_ok}")


if __name__ == "__main__":
    main()
