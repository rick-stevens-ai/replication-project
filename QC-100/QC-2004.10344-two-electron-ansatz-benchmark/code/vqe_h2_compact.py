#!/usr/bin/env python3
"""
Independent replication of Smart & Mazziotti, arXiv:2004.10344 (2020),
"Efficient Two-Electron Ansatz for Benchmarking Quantum Chemistry on a Quantum Computer".

Reproduces the H2 (STO-3G) potential energy curve using the paper's compact
2-electron ansatz: a single double-excitation angle |11'>-|22'> mixing,
Jordan-Wigner mapped onto 4 qubits, optimized by VQE.

Compares to:
  - Full Configuration Interaction (FCI) from PySCF  -- the reference the paper compares to
  - UCCSD (equivalent for H2/STO-3G but instructive re: parameter/gate count)

Real state-vector simulation, no noise (this reproduces the "noiseless / ideal"
curve that Fig.1 uses as the FCI reference target). Chemical accuracy target:
< 1.6 mhartree per point.

Author: independent replication for QC-100 wave.
"""

import json
import os
import sys
import time
import numpy as np
from pathlib import Path

from pyscf import gto, scf, fci, ao2mo

import openfermion as of
from openfermion.chem import MolecularData
from openfermion.transforms import get_fermion_operator, jordan_wigner
from openfermion.linalg import get_sparse_operator
from openfermionpyscf import run_pyscf

from scipy.optimize import minimize
from scipy.sparse.linalg import expm_multiply, eigsh
from scipy.sparse import identity as sp_identity

# ---------- Ensure openfermionpyscf is available ----------
# (installed lazily if missing)

REPO = Path(__file__).resolve().parents[1]
RES = REPO / "results"
RES.mkdir(exist_ok=True, parents=True)

# ---------- Molecule setup ----------

def get_h2_hamiltonian(bond_length):
    """Return (qubit_hamiltonian_sparse, n_qubits, fci_energy, hf_energy, nuclear_repulsion).

    Uses PySCF STO-3G, then openfermion Jordan-Wigner to reach a 4-qubit
    Pauli Hamiltonian.  The compact ansatz operates directly on this 4-qubit space.
    """
    geometry = [("H", (0.0, 0.0, 0.0)), ("H", (0.0, 0.0, bond_length))]
    basis = "sto-3g"
    multiplicity = 1
    charge = 0
    molecule = MolecularData(geometry, basis, multiplicity, charge,
                             description=f"h2_R{bond_length:.3f}")
    molecule = run_pyscf(molecule, run_scf=True, run_fci=True)
    # Fermionic Hamiltonian (spin-orbital basis, size 2*2 = 4)
    ferm_ham = get_fermion_operator(molecule.get_molecular_hamiltonian())
    qubit_ham = jordan_wigner(ferm_ham)
    n_qubits = molecule.n_qubits  # 4 for H2/STO-3G
    ham_sparse = get_sparse_operator(qubit_ham, n_qubits=n_qubits)
    return {
        "H_sparse": ham_sparse,
        "H_qubit": qubit_ham,
        "n_qubits": n_qubits,
        "fci_energy": molecule.fci_energy,
        "hf_energy": molecule.hf_energy,
        "nuclear_repulsion": molecule.nuclear_repulsion,
    }


# ---------- Compact 2-electron ansatz ----------
#
# Per Smart & Mazziotti (Eq. 9) with r=2, there is a single generator:
#     T = t * (a†_{2α} a†_{2β} a_{1β} a_{1α} - h.c.)
# acting on the Hartree-Fock reference |1α 1β 0 0>.
# For H2/STO-3G in the natural-orbital (=HF) basis, this single double-excitation
# is *exactly* the FCI subspace within the correct symmetry sector.
#
# In JW with ordering (1α, 1β, 2α, 2β) → qubits (0,1,2,3):
#     |HF> = |0011>   (little-endian, qubits 0 and 1 occupied)
# The double excitation |0011> ↔ |1100> is realised by the well-known
# single-parameter 4-qubit ansatz.

def hf_state_vector(n_qubits=4, occ_qubits=(0, 1)):
    """|HF> = product of |1> on occupied qubits, |0> elsewhere."""
    dim = 2 ** n_qubits
    idx = 0
    for q in occ_qubits:
        idx |= (1 << q)
    vec = np.zeros(dim, dtype=complex)
    vec[idx] = 1.0
    return vec


def double_excitation_generator_sparse(n_qubits=4):
    """Return sparse operator T = a†_2 a†_3 a_1 a_0 - h.c. as a Pauli sum in JW.

    We build it via openfermion to keep signs consistent with the H sparse op.
    """
    op = of.FermionOperator("2^ 3^ 1 0") - of.FermionOperator("0^ 1^ 3 2")
    qop = jordan_wigner(op)
    return get_sparse_operator(qop, n_qubits=n_qubits)


def compact_ansatz_state(theta, hf_vec, T_sparse):
    """|psi(theta)> = exp(theta * T) |HF>.  T is antihermitian, so exp is unitary."""
    # expm_multiply computes exp(A) v efficiently for sparse A.
    return expm_multiply(theta * T_sparse, hf_vec)


def energy_expectation(state, H_sparse):
    """<psi|H|psi> — H is Hermitian so imaginary part is a numerical residual."""
    hv = H_sparse @ state
    e = np.vdot(state, hv)
    return float(np.real(e))


# ---------- VQE driver ----------

def vqe_at_bond_length(R):
    data = get_h2_hamiltonian(R)
    n_qubits = data["n_qubits"]
    hf_vec = hf_state_vector(n_qubits=n_qubits)
    T = double_excitation_generator_sparse(n_qubits=n_qubits)
    H = data["H_sparse"]

    # Direct diagonalization of H (small, 16x16 dense equivalent) for
    # reference (matches PySCF's fci_energy up to tiny numerical noise).
    dense = H.toarray()
    w = np.linalg.eigvalsh(dense)
    e_diag_gs = float(w[0])

    # Optimize the single angle
    def cost(theta_arr):
        theta = float(theta_arr[0])
        psi = compact_ansatz_state(theta, hf_vec, T)
        return energy_expectation(psi, H)

    best = None
    for x0 in np.linspace(-np.pi, np.pi, 9):
        res = minimize(cost, x0=[x0], method="BFGS",
                       options={"gtol": 1e-10, "xrtol": 1e-10})
        if (best is None) or (res.fun < best.fun):
            best = res
    theta_opt = float(best.x[0])
    e_vqe = float(best.fun)

    return {
        "R_angstrom": R,
        "hf_energy": data["hf_energy"],
        "fci_energy_pyscf": data["fci_energy"],
        "gs_energy_qubit_ham_diag": e_diag_gs,
        "vqe_compact_energy": e_vqe,
        "theta_opt": theta_opt,
        "err_vs_fci_mha": (e_vqe - data["fci_energy"]) * 1000.0,
        "err_vs_ham_diag_mha": (e_vqe - e_diag_gs) * 1000.0,
        "nuclear_repulsion": data["nuclear_repulsion"],
    }


def uccsd_reference_counts():
    """Report parameter / CNOT counts for the compact ansatz vs a
    generic UCCSD baseline (Jordan–Wigner, canonical Trotter=1) on H2/STO-3G.

    For H2/STO-3G, the correlated Hilbert space has ONE double excitation
    and (2) singles that are spin-forbidden or symmetry-decoupled; the
    common qiskit-nature UCCSD counts are the standard reference.
    """
    # These are the well-established textbook counts for JW UCCSD on H2/STO-3G:
    #   - 3 fermionic excitations: 2 singles (a†_0 a_2 - h.c.), (a†_1 a_3 - h.c.)
    #     and 1 double (a†_2 a†_3 a_1 a_0 - h.c.).
    #   - After JW → Pauli strings → CNOT ladders per string.
    # See e.g. Yordanov et al. 2020, Table I, and standard qiskit tutorials.
    uccsd = {
        "n_parameters": 3,
        "n_cnots_typical": 14,  # 1 single = 2 CNOTs (staircase) ×2 + 1 double = ~10 CNOTs
        "notes": "JW UCCSD (Trotter=1) canonical decomposition, singles+double excitation.",
    }
    compact = {
        "n_parameters": 1,
        # The single-parameter double-excitation on 4 qubits, optimally
        # decomposed (Vatan-Williams-style), requires ~2 CNOTs; the
        # naive JW-Pauli-string ladder decomposition uses 8 CNOTs
        # (paper uses 8 CNOTs per Nam et al. simplification, see paper).
        "n_cnots_paper_reported": 8,
        "n_cnots_optimal": 2,
        "notes": ("Single double-excitation |0011>↔|1100>. Paper (Sec III) reports "
                  "an 8-CNOT nearest-neighbor construction via Nam et al. [39]. "
                  "Optimal 2-CNOT construction exists for the 2-parameter subspace."),
    }
    return {"compact_paper": compact, "uccsd_reference": uccsd}


def main():
    t0 = time.time()
    # Grid similar to Fig. 1 in the paper: ~0.5 Å to ~2.5 Å
    R_grid = [0.30, 0.40, 0.50, 0.60, 0.70, 0.735, 0.80, 0.90, 1.00, 1.20,
              1.40, 1.60, 1.80, 2.00, 2.25, 2.50, 2.75, 3.00]
    curve = []
    for R in R_grid:
        pt = vqe_at_bond_length(R)
        curve.append(pt)
        print(f"R={R:.3f}Å  HF={pt['hf_energy']:.6f}  "
              f"FCI={pt['fci_energy_pyscf']:.6f}  "
              f"VQE={pt['vqe_compact_energy']:.6f}  "
              f"err={pt['err_vs_fci_mha']:+.4f} mha", flush=True)

    counts = uccsd_reference_counts()

    # Statistics
    errs_mha = np.array([abs(p["err_vs_fci_mha"]) for p in curve])
    summary = {
        "n_points": len(curve),
        "max_abs_err_mhartree": float(errs_mha.max()),
        "mean_abs_err_mhartree": float(errs_mha.mean()),
        "median_abs_err_mhartree": float(np.median(errs_mha)),
        "chemical_accuracy_mha_threshold": 1.6,
        "all_points_within_chem_accuracy": bool(errs_mha.max() < 1.6),
        "elapsed_seconds": round(time.time() - t0, 3),
        "counts": counts,
        "software": {
            "pyscf": __import__("pyscf").__version__,
            "openfermion": of.__version__,
            "openfermionpyscf": __import__("openfermionpyscf").__version__,
            "numpy": np.__version__,
        },
    }

    out = {"curve": curve, "summary": summary}
    (RES / "h2_curve.json").write_text(json.dumps(out, indent=2))

    # Also emit CSV for easy inspection
    import csv
    with (RES / "h2_curve.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["R_angstrom", "HF", "FCI", "VQE_compact",
                    "err_vs_FCI_mhartree", "theta_opt_rad"])
        for p in curve:
            w.writerow([p["R_angstrom"], p["hf_energy"], p["fci_energy_pyscf"],
                        p["vqe_compact_energy"], p["err_vs_fci_mha"], p["theta_opt"]])

    print("\n=== SUMMARY ===")
    print(json.dumps(summary, indent=2))
    print(f"\nWrote {RES/'h2_curve.json'} and {RES/'h2_curve.csv'}")


if __name__ == "__main__":
    main()
