#!/usr/bin/env -S python -u
"""
Independent replication of Shang et al. 2023 (arXiv:2303.03681)
Table III STO-3g H2 UCCSD-VQE-vs-FCI MAE claim.

Paper's headline claim (Table III):
  For H2, STO-3g, UCCSD-VQE MAE vs FCI = 9.4e-13 kcal/mol,
  MAX = 6.3e-12 kcal/mol.

That row essentially says: at STO-3g, UCCSD IS FCI (2-electron system,
no truncation error). So a competent statevector VQE with a full UCCSD
ansatz should also reach FCI to machine precision on the H2/STO-3g PES.

We reproduce this on an OpenFermion + PySCF stack (statevector, no HPC,
no MPS — the point is *correctness equivalence*, not their PFLOPS).

For each bond length R:
  1. Build the H2 molecular Hamiltonian at STO-3g (2 spatial orbitals,
     4 spin-orbitals, 4 qubits).
  2. Diagonalize the qubit-mapped Hamiltonian (Jordan-Wigner) -> E_FCI
     (this is exact in the 4-qubit Hilbert space for a 2-electron system).
     Cross-check against pyscf's FCI energy.
  3. Build the singlet-restricted UCCSD generator (2 amplitudes:
     one for the paired singles a0->a2 + b1->b3, one for the double
     {0,1}->{2,3}). Precompute the qubit-space generator matrices.
  4. VQE: minimize <HF| exp(-G) H exp(G) |HF> over the 2 amplitudes
     using BFGS with a small finite-diff step. This is a statevector
     UCCSD-VQE.
  5. Record E_VQE, E_FCI, error in Hartree and kcal/mol.

Then compute MAE and MAX across the scan and compare to Table III STO-3g.
"""

import json
import os
import time
import numpy as np
from scipy.linalg import eigh, expm
from scipy.optimize import minimize

from openfermion.chem import MolecularData
from openfermionpyscf import run_pyscf
from openfermion.transforms import get_fermion_operator, jordan_wigner
from openfermion.linalg import get_sparse_operator
from openfermion.ops import FermionOperator

HARTREE_TO_KCAL = 627.5094740631
N_QUBITS = 4
N_ELECTRONS = 2

# Bond lengths (Å) covering the bonding + dissociation region.
# Includes R=2.4 Å which the paper explicitly cites as the MAX-error point
# for aug-cc-pVTZ; at STO-3g their reported MAX is 6.3e-12 kcal/mol.
BOND_LENGTHS = [0.5, 0.6, 0.7, 0.75, 0.8, 0.9, 1.0, 1.1, 1.2, 1.4,
                1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 3.0]


def op_sparse_dense(fop, n_qubits=N_QUBITS):
    return get_sparse_operator(jordan_wigner(fop), n_qubits=n_qubits).toarray()


# Precompute (constant) generator matrices for the 2-parameter singlet UCCSD.
# Spin-orbital ordering in OpenFermion: [0=a0, 1=b0, 2=a1, 3=b1]
# where a=alpha, b=beta, 0=orbital0 (occupied HF), 1=orbital1 (virtual HF).
# Singlet singles: t_s * (a2^ a0  +  b3^ b1)  - h.c.
# Singlet double : t_d * (a2^ b3^ b1 a0)       - h.c.
Gs_op = FermionOperator("2^ 0", 1.0) + FermionOperator("3^ 1", 1.0)
Gs = op_sparse_dense(Gs_op)
Gs = Gs - Gs.conj().T  # anti-hermitian

Gd_op = FermionOperator("3^ 2^ 1 0", 1.0)
Gd = op_sparse_dense(Gd_op)
Gd = Gd - Gd.conj().T


def hf_vec():
    v = np.zeros(1 << N_QUBITS, dtype=complex)
    idx = 0
    for i in range(N_ELECTRONS):
        idx |= (1 << i)
    v[idx] = 1.0
    return v


HF = hf_vec()


def run_R(R):
    geom = [("H", (0.0, 0.0, 0.0)), ("H", (0.0, 0.0, R))]
    mol = MolecularData(geom, basis="sto-3g", multiplicity=1, charge=0,
                        description=f"H2_R{R:.2f}")
    mol = run_pyscf(mol, run_scf=True, run_fci=True)
    assert mol.n_qubits == N_QUBITS and mol.n_electrons == N_ELECTRONS

    ham = get_fermion_operator(mol.get_molecular_hamiltonian())
    Hd = op_sparse_dense(ham)
    evals, _ = eigh(Hd)
    E_diag = float(evals[0].real)
    E_fci = float(mol.fci_energy)

    def energy(params):
        ts, td = params
        U = expm(ts * Gs + td * Gd)
        psi = U @ HF
        return float(np.real(np.conj(psi) @ (Hd @ psi)))

    # Analytic gradient of E(ts, td) = <HF|exp(-G)^T H exp(G)|HF>
    # where G = ts*Gs + td*Gd is anti-hermitian, so exp(G) is unitary
    # and <HF| exp(-G) = <HF| exp(G)^dagger = (exp(G)|HF>)^dagger.
    # dE/dts = 2 Re <psi| H (Gs psi)> where psi = exp(G)|HF>? Not quite — for
    # non-commuting Gs, Gd we would need a proper parameter-shift. For BFGS
    # a tight finite-diff step is more than sufficient here (2D problem).
    res = minimize(energy, np.array([0.05, 0.1]), method="BFGS",
                   options={"gtol": 1e-14, "eps": 1e-8, "maxiter": 2000})
    # Follow with Nelder-Mead polish (small budget, 2D)
    res2 = minimize(energy, res.x, method="Nelder-Mead",
                    options={"xatol": 1e-14, "fatol": 1e-16, "maxiter": 400,
                             "adaptive": True})
    if res2.fun < res.fun:
        res = res2
    E_vqe = float(res.fun)

    return {
        "R": R,
        "E_HF": float(mol.hf_energy),
        "E_FCI_pyscf": E_fci,
        "E_FCI_diag_qubit_H": E_diag,
        "E_VQE_UCCSD": E_vqe,
        "err_vs_diag_hartree": E_vqe - E_diag,
        "err_vs_diag_kcal": (E_vqe - E_diag) * HARTREE_TO_KCAL,
        "err_vs_pyscf_hartree": E_vqe - E_fci,
        "err_vs_pyscf_kcal": (E_vqe - E_fci) * HARTREE_TO_KCAL,
        "params": res.x.tolist(),
        "opt_iters": int(res.nit),
        "opt_nfev": int(res.nfev),
        "opt_success": bool(res.success),
    }


def main():
    t0 = time.time()
    rows = []
    for R in BOND_LENGTHS:
        r = run_R(R)
        rows.append(r)
        print(f"R={r['R']:.2f} Å  E_FCI={r['E_FCI_diag_qubit_H']:.10f}  "
              f"E_VQE={r['E_VQE_UCCSD']:.10f}  err={r['err_vs_diag_kcal']:+.3e} kcal/mol  "
              f"(vs pyscf FCI {r['err_vs_pyscf_kcal']:+.3e} kcal/mol, iters={r['opt_iters']})")

    errs = np.array([r["err_vs_diag_kcal"] for r in rows])
    errs_pyscf = np.array([r["err_vs_pyscf_kcal"] for r in rows])
    mae = float(np.mean(np.abs(errs)))
    mx = float(np.max(np.abs(errs)))
    mae_pyscf = float(np.mean(np.abs(errs_pyscf)))
    mx_pyscf = float(np.max(np.abs(errs_pyscf)))
    dt = time.time() - t0

    import pyscf, openfermion, openfermionpyscf, scipy, numpy as _np
    summary = {
        "paper": "arXiv:2303.03681 (Shang et al. 2023)",
        "target_row": "Table III, STO-3g row",
        "claim_paper": {
            "MAE_kcal_per_mol": 9.4e-13,
            "MAX_kcal_per_mol": 6.3e-12,
            "note": "UCCSD-VQE (MPS-based, bond dim ~256) vs FCI on H2 PES, STO-3g basis",
        },
        "reproduction": {
            "backend": "OpenFermion (statevector, Jordan-Wigner) + PySCF FCI reference, "
                       "singlet-restricted UCCSD (2 params: paired singles + double), "
                       "SciPy BFGS classical optimizer.",
            "n_qubits": N_QUBITS,
            "n_electrons": N_ELECTRONS,
            "n_bond_lengths": len(rows),
            "bond_lengths_A": BOND_LENGTHS,
            "MAE_vs_diag_qubit_H_kcal_per_mol": mae,
            "MAX_vs_diag_qubit_H_kcal_per_mol": mx,
            "MAE_vs_pyscf_FCI_kcal_per_mol": mae_pyscf,
            "MAX_vs_pyscf_FCI_kcal_per_mol": mx_pyscf,
            "wall_seconds": dt,
        },
        "versions": {
            "python": os.popen("python -c 'import sys; print(sys.version.split()[0])'").read().strip(),
            "numpy": _np.__version__,
            "scipy": scipy.__version__,
            "pyscf": pyscf.__version__,
            "openfermion": openfermion.__version__,
            "openfermionpyscf": openfermionpyscf.__version__,
        },
        "rows": rows,
    }

    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "report", "evidence"))
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "h2_sto3g_vqe_vs_fci.json"), "w") as f:
        json.dump(summary, f, indent=2)

    import csv
    with open(os.path.join(out_dir, "h2_sto3g_vqe_vs_fci.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["R_A", "E_HF_Ha", "E_FCI_pyscf_Ha", "E_FCI_diag_qubitH_Ha",
                    "E_VQE_UCCSD_Ha", "err_vs_diag_kcal", "err_vs_pyscf_kcal",
                    "opt_iters", "opt_nfev"])
        for r in rows:
            w.writerow([r["R"], r["E_HF"], r["E_FCI_pyscf"],
                        r["E_FCI_diag_qubit_H"], r["E_VQE_UCCSD"],
                        r["err_vs_diag_kcal"], r["err_vs_pyscf_kcal"],
                        r["opt_iters"], r["opt_nfev"]])

    print()
    print(f"=== SUMMARY ===")
    print(f"Bond lengths scanned: {len(rows)}")
    print(f"MAE (vs diag qubit H) = {mae:.3e} kcal/mol")
    print(f"MAX (vs diag qubit H) = {mx:.3e} kcal/mol")
    print(f"MAE (vs pyscf FCI)    = {mae_pyscf:.3e} kcal/mol")
    print(f"MAX (vs pyscf FCI)    = {mx_pyscf:.3e} kcal/mol")
    print(f"Paper Table III STO-3g: MAE=9.4e-13, MAX=6.3e-12 kcal/mol")
    print(f"Wall time: {dt:.1f} s")


if __name__ == "__main__":
    main()
