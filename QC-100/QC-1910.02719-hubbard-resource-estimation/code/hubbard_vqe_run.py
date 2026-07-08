"""
Actually run a small VQE with a Hamiltonian Variational Ansatz (HVA)
on the 2D Fermi-Hubbard model, in the spirit of Cai (arXiv:1910.02719).

We work at V=4 (2x2 open-BC, N=8 qubits) and V=6 (2x3, N=12 qubits)
so exact diagonalisation is cheap and we can compare VQE energy to the
true ground-state energy.

HVA definition (per block, Trotterised first-order):
    U_block(theta) = exp(-i theta_U * H_U) * exp(-i theta_v * H_v)
                     * exp(-i theta_h * H_h)
where
    H_U = sum_i n_{i,up} n_{i,down}        (on-site repulsion)
    H_v = sum_<i,j>_vert (a_i^dag a_j + h.c.)  vertical hopping (both spins)
    H_h = sum_<i,j>_horiz (a_i^dag a_j + h.c.) horizontal hopping (both spins)

Starting state: Slater determinant = ground state of the
non-interacting (U=0) Hubbard Hamiltonian, at half-filling, spin-0.

We simulate exp(-i theta * H_k) exactly (using the sparse matrix
exponent) — this is a resource / expressibility check on the ansatz,
not a NISQ gate-level simulation. The paper's key claim is a
RESOURCE ESTIMATE; the correctness of the HVA as an ansatz for
finding the Hubbard ground state is the well-known Wecker/Kivlichan
result that this reproduces.

We report:
  * E0_exact  (exact ground state)
  * E_HF      (starting Slater determinant expectation of H)
  * E_VQE(p)  for p=1,2,3 HVA blocks
  * rel_error = (E_VQE - E0) / |E0|

and PER-BLOCK gate counts predicted by the paper for these V's.
"""

from __future__ import annotations

import json
import math
import os
import time
from itertools import combinations

import numpy as np
from scipy.optimize import minimize
from scipy.sparse.linalg import expm_multiply

import openfermion as of
from openfermion.hamiltonians import fermi_hubbard
from openfermion.transforms import jordan_wigner
from openfermion.linalg import get_ground_state, get_sparse_operator


def n1q_ha(V): return 4 * V ** 1.5 + 7 * V - 4 * math.sqrt(V)
def n2q_ha(V): return 8 * V ** 1.5 +     V - 4 * math.sqrt(V)


def build_hubbard_pieces(Lx, Ly, tunneling=1.0, coulomb=4.0):
    """Return (H_full, H_U_only, H_hop_horiz, H_hop_vert) as fermion operators."""
    # spinful Hubbard
    H_full = fermi_hubbard(
        x_dimension=Lx, y_dimension=Ly,
        tunneling=tunneling, coulomb=coulomb,
        chemical_potential=0.0, periodic=False, spinless=False,
    )
    H_U = fermi_hubbard(
        x_dimension=Lx, y_dimension=Ly,
        tunneling=0.0, coulomb=coulomb,
        chemical_potential=0.0, periodic=False, spinless=False,
    )
    # Full hopping only
    H_hop = fermi_hubbard(
        x_dimension=Lx, y_dimension=Ly,
        tunneling=tunneling, coulomb=0.0,
        chemical_potential=0.0, periodic=False, spinless=False,
    )
    # Split hopping into horizontal / vertical by hand.
    # OpenFermion index convention (spinful): index = (2*(y*Lx + x) + s),
    # s=0 up, s=1 down.
    H_hop_h = of.FermionOperator()
    H_hop_v = of.FermionOperator()
    for y in range(Ly):
        for x in range(Lx):
            i = 2 * (y * Lx + x)
            # horizontal neighbour +x
            if x + 1 < Lx:
                j = 2 * (y * Lx + (x + 1))
                for s in (0, 1):
                    term = of.FermionOperator(f"{i+s}^ {j+s}", -tunneling)
                    term += of.hermitian_conjugated(term)
                    H_hop_h += term
            # vertical neighbour +y
            if y + 1 < Ly:
                j = 2 * ((y + 1) * Lx + x)
                for s in (0, 1):
                    term = of.FermionOperator(f"{i+s}^ {j+s}", -tunneling)
                    term += of.hermitian_conjugated(term)
                    H_hop_v += term
    # de-dup: each bond should be counted once. The
    # FermionOperator("i^ j", -t) + hc gives -t(i^ j + j^ i).
    # Divide by 2 because we double-counted in the loop above? No —
    # we only visited each bond once (+x, +y).
    return H_full, H_U, H_hop_h, H_hop_v


def sparse(op, n): return get_sparse_operator(jordan_wigner(op), n_qubits=n)


def half_filling_slater_state(Lx, Ly, tunneling, n_qubits):
    """
    Ground state of the U=0, half-filled Hubbard model (i.e. the
    Slater determinant that Cai / Kivlichan use as the HVA starting
    state).
    """
    H_ni = fermi_hubbard(
        x_dimension=Lx, y_dimension=Ly,
        tunneling=tunneling, coulomb=0.0,
        chemical_potential=0.0, periodic=False, spinless=False,
    )
    Hni_sparse = sparse(H_ni, n_qubits)
    _, psi = get_ground_state(Hni_sparse)
    return psi


def run_vqe(Lx, Ly, p_blocks, tunneling=1.0, coulomb=4.0, seed=0):
    V = Lx * Ly
    n_qubits = 2 * V

    H_full, H_U, H_hop_h, H_hop_v = build_hubbard_pieces(
        Lx, Ly, tunneling=tunneling, coulomb=coulomb,
    )
    H_sp   = sparse(H_full,  n_qubits)
    HU_sp  = sparse(H_U,     n_qubits)
    Hh_sp  = sparse(H_hop_h, n_qubits)
    Hv_sp  = sparse(H_hop_v, n_qubits)

    # Exact ground state
    E0_exact, psi0_exact = get_ground_state(H_sp)

    # HVA starting state (Slater determinant, U=0)
    psi_start = half_filling_slater_state(Lx, Ly, tunneling, n_qubits)

    # Expectation of H in starting state
    E_start = float(np.real(np.vdot(psi_start, H_sp @ psi_start)))

    # Ansatz: apply p blocks of  exp(-i theta * H_v) exp(-i theta * H_h) exp(-i theta * H_U)
    def apply_ansatz(theta_flat, psi):
        # theta_flat has 3 * p_blocks entries
        state = psi
        for b in range(p_blocks):
            tU = theta_flat[3 * b + 0]
            th = theta_flat[3 * b + 1]
            tv = theta_flat[3 * b + 2]
            # exp(-i t H) applied to state
            state = expm_multiply(-1j * tU * HU_sp, state)
            state = expm_multiply(-1j * th * Hh_sp, state)
            state = expm_multiply(-1j * tv * Hv_sp, state)
        return state

    def energy(theta_flat):
        psi = apply_ansatz(theta_flat, psi_start)
        e = float(np.real(np.vdot(psi, H_sp @ psi)))
        return e

    rng = np.random.default_rng(seed)
    theta0 = 0.05 * rng.standard_normal(3 * p_blocks)

    t0 = time.time()
    res = minimize(energy, theta0, method="L-BFGS-B",
                   options={"maxiter": 200, "ftol": 1e-10, "gtol": 1e-8})
    dt = time.time() - t0
    return {
        "V":            V,
        "N_qubits":     n_qubits,
        "p_blocks":     p_blocks,
        "E0_exact":     float(E0_exact),
        "E_start_slater": E_start,
        "E_vqe":        float(res.fun),
        "rel_error":    float(abs(res.fun - E0_exact) /
                              max(abs(E0_exact), 1e-12)),
        "vqe_iterations": int(res.nit),
        "optimise_seconds": dt,
        "hva_block_N1q_paper_formula": n1q_ha(V),
        "hva_block_N2q_paper_formula": n2q_ha(V),
        "hva_total_N1q_p_blocks":      p_blocks * n1q_ha(V),
        "hva_total_N2q_p_blocks":      p_blocks * n2q_ha(V),
    }


def main():
    all_results = []
    for (Lx, Ly) in [(2, 2), (2, 3)]:
        print(f"\n=== 2D Hubbard {Lx}x{Ly}, U/t=4 ===")
        exact_ref = None
        for p in [1, 2, 3]:
            r = run_vqe(Lx, Ly, p_blocks=p, tunneling=1.0, coulomb=4.0, seed=0)
            all_results.append(r)
            if exact_ref is None:
                exact_ref = r["E0_exact"]
            print(f"  p={p}: E_start = {r['E_start_slater']:.6f}, "
                  f"E_VQE = {r['E_vqe']:.6f}, "
                  f"E0_exact = {r['E0_exact']:.6f}, "
                  f"rel_err = {r['rel_error']:.3e}   "
                  f"({r['optimise_seconds']:.1f}s, {r['vqe_iterations']} iters)")

    out_dir = os.path.join(os.path.dirname(__file__), "..", "report", "evidence")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "hubbard_vqe_runs.json")
    with open(out, "w") as f:
        json.dump({
            "paper": "1910.02719",
            "runs": all_results,
        }, f, indent=2)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
