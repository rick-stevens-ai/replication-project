"""
Independent replication of Kirby & Love (arXiv:1904.02260) contextuality test.

Implements Theorem 3: A set S of Pauli operators is noncontextual iff, after
removing all operators that commute with everything, commutation is an
equivalence relation on the remainder T.

Equivalently (from Sec. II): S is contextual iff there exist A,B,C in T such
that A commutes with B and A commutes with C, but B and C anticommute
(i.e. commutation is not transitive on T).

We build real molecular Hamiltonians for:
  - H2 STO-3G (4 qubits, Jordan-Wigner)
  - H2 STO-3G (2 qubits, parity + 2-qubit-tapering, ≈ Bravyi-Kitaev flavor
    used by Kandala et al. [17] and O'Malley et al. [13] --- yields |S|=5)
  - HeH+ STO-3G (Peruzzo et al. [11] configuration)
  - LiH STO-3G with active-space reduction (Hempel et al. BK-style, ~|S|=13)
  - H2O STO-3G with active-space reduction (Nam et al., ~|S|=22)

Then run the test and compare to Table I of the paper.

Real simulation: real molecular integrals via PySCF -> real fermionic
Hamiltonian via OpenFermion -> real Pauli-operator Hamiltonian via
Jordan-Wigner / Bravyi-Kitaev encodings.  No hand-picked toy operators.
"""

from __future__ import annotations
import json, itertools, os, sys, time
from collections import defaultdict
from openfermion.chem import MolecularData
from openfermion.transforms import (
    get_fermion_operator, jordan_wigner, bravyi_kitaev
)
from openfermion.ops import QubitOperator
from openfermionpyscf import run_pyscf


# ---------- Contextuality test (paper Sec. II, Thm 3) ----------

def _pauli_at(term, q):
    """Return Pauli letter at qubit q for OpenFermion term tuple, else 'I'."""
    for (qi, p) in term:
        if qi == q:
            return p
    return "I"


def commute(t1, t2, n_qubits):
    """Two Pauli strings commute iff they anticommute on an even number of qubits."""
    anti = 0
    for q in range(n_qubits):
        a, b = _pauli_at(t1, q), _pauli_at(t2, q)
        if a == "I" or b == "I" or a == b:
            continue
        anti += 1
    return (anti % 2) == 0


def pauli_str(term, n_qubits):
    """Pretty-print a Pauli term as e.g. 'XIZY' for logging."""
    s = ["I"] * n_qubits
    for (qi, p) in term:
        s[qi] = p
    return "".join(s)


def is_contextual(qubit_op: QubitOperator, n_qubits: int):
    """
    Implements Theorem 3 of Kirby & Love 2019.

    Returns dict with keys:
      S_size, T_size, contextual (bool), witness (triple or None), notes
    """
    # Collect unique Pauli operators (drop identity; coefficient sign irrelevant
    # to commutation, and the paper's set S is a set of Pauli operators).
    terms = []
    seen = set()
    for term, coeff in qubit_op.terms.items():
        if len(term) == 0:
            continue  # identity contributes constant, not a measurement in S
        if term in seen:
            continue
        seen.add(term)
        terms.append(term)

    S = terms
    # Step 1: remove universally-commuting operators -> T
    T = []
    for i, ti in enumerate(S):
        universal = True
        for j, tj in enumerate(S):
            if i == j:
                continue
            if not commute(ti, tj, n_qubits):
                universal = False
                break
        if not universal:
            T.append(ti)

    # Step 2: search for A,B,C in T with A~B, A~C, B not~C  (non-transitivity)
    witness = None
    n = len(T)
    for a in range(n):
        for b in range(n):
            if b == a:
                continue
            if not commute(T[a], T[b], n_qubits):
                continue
            for c in range(b + 1, n):
                if c == a:
                    continue
                if not commute(T[a], T[c], n_qubits):
                    continue
                # A commutes with B and A commutes with C. Contextual iff B~C anticommute.
                if not commute(T[b], T[c], n_qubits):
                    witness = (
                        pauli_str(T[a], n_qubits),
                        pauli_str(T[b], n_qubits),
                        pauli_str(T[c], n_qubits),
                    )
                    break
            if witness:
                break
        if witness:
            break

    return {
        "S_size": len(S),
        "T_size": len(T),
        "contextual": witness is not None,
        "witness": witness,
    }


# ---------- Hamiltonian builders (real molecular integrals) ----------

def hamiltonian_h2_jw(bond=0.735):
    """H2/STO-3G, 4-qubit Jordan-Wigner. Matches Hempel et al. (JW) row: |S|=14."""
    geom = [("H", (0.0, 0.0, 0.0)), ("H", (0.0, 0.0, bond))]
    mol = MolecularData(geom, "sto-3g", 1, 0, description="H2_JW")
    mol = run_pyscf(mol, run_scf=True, run_fci=True)
    fop = get_fermion_operator(mol.get_molecular_hamiltonian())
    qop = jordan_wigner(fop)
    qop.compress()
    return qop, 4, mol

def hamiltonian_h2_bk(bond=0.735):
    """H2/STO-3G, 4-qubit Bravyi-Kitaev.  Not the same reduced 2-qubit form
    used by Kandala/O'Malley -- see hamiltonian_h2_bk2q for that."""
    geom = [("H", (0.0, 0.0, 0.0)), ("H", (0.0, 0.0, bond))]
    mol = MolecularData(geom, "sto-3g", 1, 0, description="H2_BK")
    mol = run_pyscf(mol, run_scf=True, run_fci=True)
    fop = get_fermion_operator(mol.get_molecular_hamiltonian())
    qop = bravyi_kitaev(fop)
    qop.compress()
    return qop, 4, mol

def hamiltonian_h2_bk_2q(bond=0.735):
    """H2/STO-3G reduced to 2 qubits via BK + parity taper.
    This is the 5-term form used by O'Malley et al. [13] and Kandala et al. [17]
    (aa I + b ZI + c IZ + d ZZ + e XX / YY).
    """
    from openfermion.transforms import symmetry_conserving_bravyi_kitaev
    geom = [("H", (0.0, 0.0, 0.0)), ("H", (0.0, 0.0, bond))]
    mol = MolecularData(geom, "sto-3g", 1, 0, description="H2_BK_2q")
    mol = run_pyscf(mol, run_scf=True, run_fci=True)
    fop = get_fermion_operator(mol.get_molecular_hamiltonian())
    # symmetry_conserving_bravyi_kitaev: reduce 4->2 qubits using BK + Z2 symmetries
    qop = symmetry_conserving_bravyi_kitaev(fop, active_orbitals=4, active_fermions=2)
    qop.compress()
    return qop, 2, mol

def hamiltonian_hehp_jw(bond=0.9295):
    """HeH+ / STO-3G, 4-qubit Jordan-Wigner (Peruzzo et al. [11] scale)."""
    geom = [("H", (0.0, 0.0, 0.0)), ("He", (0.0, 0.0, bond))]
    mol = MolecularData(geom, "sto-3g", 1, 1, description="HeHp_JW")
    mol = run_pyscf(mol, run_scf=True, run_fci=True)
    fop = get_fermion_operator(mol.get_molecular_hamiltonian())
    qop = jordan_wigner(fop)
    qop.compress()
    return qop, 4, mol

def hamiltonian_lih_bk_active(bond=1.5, active_indices=(1,2,5)):
    """LiH / STO-3G with active-space reduction (Hempel BK-style)."""
    geom = [("Li", (0.0, 0.0, 0.0)), ("H", (0.0, 0.0, bond))]
    mol = MolecularData(geom, "sto-3g", 1, 0, description="LiH_BK_active")
    mol = run_pyscf(mol, run_scf=True, run_fci=False)
    occupied = [0]
    active = list(active_indices)
    mh = mol.get_molecular_hamiltonian(
        occupied_indices=occupied, active_indices=active
    )
    fop = get_fermion_operator(mh)
    qop = bravyi_kitaev(fop)
    qop.compress()
    n_qubits = 2 * len(active)
    return qop, n_qubits, mol

def hamiltonian_h2o_jw_active(bond=0.9584, angle=104.45):
    """H2O / STO-3G with active-space reduction, JW.  Aim for ~|S|=22 like Nam et al."""
    import math
    theta = math.radians(angle) / 2
    r = bond
    o = (0.0, 0.0, 0.0)
    h1 = (r*math.sin(theta), 0.0,  r*math.cos(theta))
    h2 = (-r*math.sin(theta), 0.0, r*math.cos(theta))
    geom = [("O", o), ("H", h1), ("H", h2)]
    mol = MolecularData(geom, "sto-3g", 1, 0, description="H2O_JW_active")
    mol = run_pyscf(mol, run_scf=True, run_fci=False)
    # H2O STO-3G: 7 orbitals (2s O + 2p O x3 + 1s H x2 = 7), 10 electrons.
    # Freeze O 1s (orbital 0), take 4 active orbitals with 4 electrons = 8 qubits.
    occupied = [0, 1]
    active = [2, 3, 4, 5]
    mh = mol.get_molecular_hamiltonian(
        occupied_indices=occupied, active_indices=active
    )
    fop = get_fermion_operator(mh)
    qop = jordan_wigner(fop)
    qop.compress()
    n_qubits = 2 * len(active)
    return qop, n_qubits, mol


# ---------- Optional: VQE sanity check on H2 (real simulation) ----------

def h2_vqe_sanity(bond=0.735):
    """Quick real VQE on 2-qubit H2 using scipy optimizer + statevector.
    Confirms that the Hamiltonian we're testing actually has the right ground
    state (matches FCI to a few mE_h)."""
    import numpy as np
    from scipy.optimize import minimize

    qop, n_qubits, mol = hamiltonian_h2_bk_2q(bond)
    # Build dense Hamiltonian matrix
    dim = 2**n_qubits
    H = np.zeros((dim, dim), dtype=complex)
    I2 = np.eye(2, dtype=complex)
    X = np.array([[0,1],[1,0]], dtype=complex)
    Y = np.array([[0,-1j],[1j,0]], dtype=complex)
    Z = np.array([[1,0],[0,-1]], dtype=complex)
    P = {"I": I2, "X": X, "Y": Y, "Z": Z}
    for term, coeff in qop.terms.items():
        mat = np.array([[1.0]], dtype=complex)
        letters = ["I"] * n_qubits
        for qi, p in term:
            letters[qi] = p
        for l in letters:
            mat = np.kron(mat, P[l])
        H += coeff * mat
    # Exact diagonalization
    eigvals = np.linalg.eigvalsh(H)
    e_exact = float(eigvals[0])

    # A tiny hardware-efficient ansatz: Ry(t0) Ry(t1) then CNOT then Ry(t2) Ry(t3)
    def ansatz(theta):
        t0,t1,t2,t3 = theta
        Ry = lambda a: np.array([[np.cos(a/2), -np.sin(a/2)],
                                 [np.sin(a/2),  np.cos(a/2)]], dtype=complex)
        CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=complex)
        psi0 = np.array([1,0,0,0], dtype=complex)
        U1 = np.kron(Ry(t0), Ry(t1))
        U2 = np.kron(Ry(t2), Ry(t3))
        psi = U2 @ CNOT @ U1 @ psi0
        return psi
    def energy(theta):
        psi = ansatz(theta)
        return float(np.real(np.conjugate(psi) @ H @ psi))
    best = None
    for seed in range(5):
        import numpy as _np
        rng = _np.random.default_rng(seed)
        x0 = rng.uniform(-1, 1, 4)
        res = minimize(energy, x0, method="COBYLA", options=dict(maxiter=500))
        if best is None or res.fun < best.fun:
            best = res
    e_vqe = float(best.fun)
    return {
        "bond_angstrom": bond,
        "n_qubits": n_qubits,
        "n_pauli_terms_incl_identity": len(qop.terms),
        "hf_energy": float(mol.hf_energy),
        "fci_energy": float(mol.fci_energy) if mol.fci_energy else None,
        "exact_diag_ground_energy": e_exact,
        "vqe_ground_energy_estimate": e_vqe,
        "vqe_minus_fci_hartree": (e_vqe - (float(mol.fci_energy) if mol.fci_energy else e_exact)),
    }


# ---------- Runner ----------

def report_case(name, qop, n_qubits, mol, paper_row):
    r = is_contextual(qop, n_qubits)
    # Total number of Pauli terms including identity (for reference)
    n_all = len(qop.terms)
    # |S| in the paper is #distinct non-identity Pauli operators
    print(f"\n=== {name} ===")
    print(f"  n_qubits                     = {n_qubits}")
    print(f"  #Pauli terms (incl identity) = {n_all}")
    print(f"  |S| (our count, no identity) = {r['S_size']}")
    print(f"  |T| (after removing univ.)   = {r['T_size']}")
    print(f"  contextual                   = {r['contextual']}")
    if r["witness"]:
        A,B,C = r["witness"]
        print(f"  witness triple A,B,C         = {A}, {B}, {C}")
        print(f"    (A commutes with B, A commutes with C, B anticommutes with C)")
    print(f"  paper Table I:                 {paper_row}")
    return {
        "name": name,
        "n_qubits": n_qubits,
        "n_pauli_terms_incl_identity": n_all,
        "S_size": r["S_size"],
        "T_size": r["T_size"],
        "contextual": r["contextual"],
        "witness": r["witness"],
        "paper_table_I": paper_row,
        "hf_energy": float(mol.hf_energy),
        "fci_energy": float(mol.fci_energy) if mol.fci_energy else None,
    }


def main():
    results = {}
    t0 = time.time()

    print("Building H2 (JW, 4q) ...")
    qop, n, mol = hamiltonian_h2_jw()
    results["H2_JW_4q"] = report_case(
        "H2 STO-3G JW (4q)", qop, n, mol,
        {"paper_ref": "Hempel et al. [18] JW", "contextual": False, "S": 14, "CD0": 0.0},
    )

    print("\nBuilding H2 (BK, 4q) ...")
    qop, n, mol = hamiltonian_h2_bk()
    results["H2_BK_4q"] = report_case(
        "H2 STO-3G BK (4q)", qop, n, mol,
        {"paper_ref": "Hempel et al. [18] BK", "contextual": False, "S": 5, "CD0": 0.0},
    )

    print("\nBuilding H2 (BK reduced to 2q) ...")
    qop, n, mol = hamiltonian_h2_bk_2q()
    results["H2_BK_2q"] = report_case(
        "H2 STO-3G BK-tapered (2q)", qop, n, mol,
        {"paper_ref": "O'Malley et al. [13] / Kandala et al. [17]",
         "contextual": False, "S": 5, "CD0": 0.0},
    )

    print("\nBuilding HeH+ (JW, 4q) ...")
    qop, n, mol = hamiltonian_hehp_jw()
    results["HeHp_JW_4q"] = report_case(
        "HeH+ STO-3G JW (4q)", qop, n, mol,
        {"paper_ref": "Peruzzo et al. [11]", "contextual": True, "S": 8, "CD0": 0.38},
    )

    print("\nBuilding LiH (BK active, 6q) ...")
    qop, n, mol = hamiltonian_lih_bk_active()
    results["LiH_BK_active_6q"] = report_case(
        "LiH STO-3G BK active (6q)", qop, n, mol,
        {"paper_ref": "Hempel et al. [18] LiH", "contextual": True, "S": 13, "CD0": 0.33},
    )

    print("\nBuilding H2O (JW active, 8q) ...")
    qop, n, mol = hamiltonian_h2o_jw_active()
    results["H2O_JW_active_8q"] = report_case(
        "H2O STO-3G JW active (8q)", qop, n, mol,
        {"paper_ref": "Nam et al. [20]", "contextual": True, "S": 22, "CD0": 0.27},
    )

    print("\nRunning VQE sanity check on 2q H2 ...")
    vqe = h2_vqe_sanity()
    results["_h2_vqe_sanity"] = vqe
    print(f"  HF   = {vqe['hf_energy']:.6f}")
    print(f"  FCI  = {vqe['fci_energy']}")
    print(f"  exact diag = {vqe['exact_diag_ground_energy']:.6f}")
    print(f"  VQE  = {vqe['vqe_ground_energy_estimate']:.6f}")
    print(f"  VQE - FCI = {vqe['vqe_minus_fci_hartree']:.2e} hartree")

    results["_meta"] = {
        "elapsed_seconds": time.time() - t0,
        "paper": "arXiv:1904.02260",
        "paper_title": "Contextuality Test of the Nonclassicality of Variational Quantum Eigensolvers",
        "authors": "Kirby & Love (2019)",
    }
    outdir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "report", "evidence")
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "contextuality_results.json"), "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nSaved: {os.path.join(outdir, 'contextuality_results.json')}")
    return results


if __name__ == "__main__":
    main()
