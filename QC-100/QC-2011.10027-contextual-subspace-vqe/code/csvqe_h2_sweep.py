#!/usr/bin/env python3
"""
CS-VQE qubit sweep on H2/STO-3G (JW-mapped, 4 qubits).

Reproduces the H2 curve of Fig. 2 of Kirby, Tranter, Love (arXiv:2011.10027):
CS-VQE error vs. number of qubits used for the quantum (contextual) part.

Method (paper Section 3):
  1. Full 4-qubit JW Hamiltonian for H2.
  2. Choose noncontextual set greedily by |coeff| (as in csvqe_h2.py).
  3. The noncontextual set has independent stabilizer generators;
     each generator, when fixed to +/-1, reduces the accessible subspace
     dimension by half. Fixing k generators gives dim 2^(n-k) subspace.
  4. Vary k = n, n-1, ..., 0 to get CS-VQE at q = 0, 1, ..., n contextual qubits.
     (k=n fixes everything => classical noncontextual; k=0 fixes nothing => full VQE.)
  5. At each q, restrict the full Hamiltonian to the subspace stabilized by the
     kept generators at their nc-ground-state eigenvalues, diagonalize.
  6. Chemical accuracy line at 1.6 mHa.

Real computation.
"""

import json
import numpy as np
from itertools import product, combinations

from openfermion import (
    MolecularData, jordan_wigner, get_sparse_operator, FermionOperator
)
from openfermion.transforms import get_fermion_operator
from openfermionpyscf import run_pyscf

CHEMICAL_ACCURACY_HA = 1.6e-3
N_QUBITS = 4


def pauli_str_to_matrix(s):
    I = np.eye(2, dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    d = {"I": I, "X": X, "Y": Y, "Z": Z}
    m = d[s[0]]
    for c in s[1:]:
        m = np.kron(m, d[c])
    return m


def term_to_pauli_string(term, n):
    s = ["I"] * n
    for (idx, p) in term:
        s[idx] = p
    return "".join(s)


def paulis_commute(p1, p2):
    anti = 0
    for a, b in zip(p1, p2):
        if a == "I" or b == "I" or a == b:
            continue
        anti += 1
    return (anti % 2) == 0


def is_noncontextual(term_strings):
    n = len(term_strings)
    if n == 0:
        return True
    adj = [[not paulis_commute(term_strings[i], term_strings[j]) if i != j else False
            for j in range(n)] for i in range(n)]
    comp = [-1] * n
    cid = 0
    for i in range(n):
        if comp[i] != -1:
            continue
        stack = [i]
        while stack:
            v = stack.pop()
            if comp[v] != -1:
                continue
            comp[v] = cid
            for j in range(n):
                if adj[v][j] and comp[j] == -1:
                    stack.append(j)
        cid += 1
    for c in range(cid):
        members = [i for i in range(n) if comp[i] == c]
        if len(members) == 1:
            continue
        for a, b in combinations(members, 2):
            if not adj[a][b]:
                return False
    for c1, c2 in combinations(range(cid), 2):
        for a in [i for i in range(n) if comp[i] == c1]:
            for b in [i for i in range(n) if comp[i] == c2]:
                if adj[a][b]:
                    return False
    return True


def greedy_noncontextual_partition(terms_with_coeff):
    sorted_terms = sorted(terms_with_coeff, key=lambda x: -abs(x[1]))
    nc, c, nc_strings = [], [], []
    for pstr, coeff in sorted_terms:
        if set(pstr) == {"I"}:
            nc.append((pstr, coeff))
            nc_strings.append(pstr)
            continue
        if is_noncontextual(nc_strings + [pstr]):
            nc.append((pstr, coeff))
            nc_strings.append(pstr)
        else:
            c.append((pstr, coeff))
    return nc, c


def build_ham_matrix(terms_with_coeff, n_qubits):
    H = np.zeros((2**n_qubits, 2**n_qubits), dtype=complex)
    for pstr, coeff in terms_with_coeff:
        H += coeff * pauli_str_to_matrix(pstr)
    return H


def find_independent_generators(nc_strings, n_qubits):
    """
    Given a set of mutually-commuting-up-to-cliques nc Pauli strings, extract
    a maximal independent commuting stabilizer group (single generators per
    clique + all universal-commuting ones), representing the noncontextual
    stabilizer group.
    Simpler approach for this small problem: pick nc terms that (a) all mutually
    commute with each other, and (b) are independent (add rank one to symplectic
    representation each). These are the generators we will fix to their nc-ground
    eigenvalue.
    """
    # Filter to pairs-of-commuting subset (drop terms that anticommute with any other kept)
    kept = []
    for p in nc_strings:
        if set(p) == {"I"}:
            continue
        if all(paulis_commute(p, q) for q in kept):
            kept.append(p)
    # Now filter for symplectic independence
    def symplectic_row(p):
        # length 2n binary vector: (x_i, z_i)
        row = np.zeros(2 * len(p), dtype=int)
        for i, ch in enumerate(p):
            if ch == "X":
                row[i] = 1
            elif ch == "Z":
                row[len(p) + i] = 1
            elif ch == "Y":
                row[i] = 1
                row[len(p) + i] = 1
        return row
    indep = []
    mat = []
    for p in kept:
        row = symplectic_row(p)
        # rank check via row-reduction over GF(2)
        test = np.array(mat + [row], dtype=int) % 2
        # gauss elim
        M = test.copy()
        r = 0
        for col in range(M.shape[1]):
            # find pivot
            pivot = None
            for rr in range(r, M.shape[0]):
                if M[rr, col] == 1:
                    pivot = rr
                    break
            if pivot is None:
                continue
            M[[r, pivot]] = M[[pivot, r]]
            for rr in range(M.shape[0]):
                if rr != r and M[rr, col] == 1:
                    M[rr] = (M[rr] + M[r]) % 2
            r += 1
        if r > len(mat):
            mat.append(row)
            indep.append(p)
    return indep


def csvqe_at_q(gens, gen_signs, terms_all, n_qubits, k_fixed):
    """
    Fix the first k_fixed generators of `gens` to their nc-ground signs.
    Project full Hamiltonian into the joint +sign eigenspace of those generators.
    Diagonalize projection -> lowest eigenvalue.
    """
    dim = 2 ** n_qubits
    # Build projector = product of (I + s_i * G_i) / 2 for the fixed generators
    P = np.eye(dim, dtype=complex)
    for i in range(k_fixed):
        G = pauli_str_to_matrix(gens[i])
        s = gen_signs[i]
        P = P @ ((np.eye(dim, dtype=complex) + s * G) / 2)
    # Now find an orthonormal basis of the range of P
    # Use SVD on P (Hermitian projector -> eigen-decomp)
    P_h = 0.5 * (P + P.conj().T)
    evals, evecs = np.linalg.eigh(P_h)
    tol = 1e-8
    mask = evals > 1 - tol
    B = evecs[:, mask]  # basis of the subspace (2^n x d)
    H = build_ham_matrix(terms_all, n_qubits)
    H_proj = B.conj().T @ H @ B
    ev = np.linalg.eigvalsh(H_proj)
    return float(ev[0]), B.shape[1]


def nc_ground_signs(gens, nc_terms, n_qubits):
    """
    Find the joint eigenvalue assignment (±1)^k for the generators that
    minimizes <nc-ground|H_nc|nc-ground>. Brute force over 2^k.
    """
    k = len(gens)
    best_E = None
    best_signs = None
    dim = 2 ** n_qubits
    for signs in product([+1, -1], repeat=k):
        P = np.eye(dim, dtype=complex)
        for i in range(k):
            G = pauli_str_to_matrix(gens[i])
            P = P @ ((np.eye(dim, dtype=complex) + signs[i] * G) / 2)
        P_h = 0.5 * (P + P.conj().T)
        evals, evecs = np.linalg.eigh(P_h)
        tol = 1e-8
        mask = evals > 1 - tol
        B = evecs[:, mask]
        if B.shape[1] == 0:
            continue
        H_nc = build_ham_matrix(nc_terms, n_qubits)
        H_proj = B.conj().T @ H_nc @ B
        ev = float(np.linalg.eigvalsh(H_proj)[0])
        if best_E is None or ev < best_E:
            best_E = ev
            best_signs = signs
    return best_E, best_signs


def main():
    print("Building H2/STO-3G Hamiltonian...")
    geom = [("H", (0, 0, 0)), ("H", (0, 0, 0.7414))]
    mol = MolecularData(geom, "sto-3g", multiplicity=1, charge=0)
    mol = run_pyscf(mol, run_scf=True, run_fci=True)
    fci_energy = float(mol.fci_energy)
    hf_energy = float(mol.hf_energy)
    print(f"  HF: {hf_energy:.8f} Ha    FCI: {fci_energy:.8f} Ha")

    fop = get_fermion_operator(mol.get_molecular_hamiltonian())
    qop = jordan_wigner(fop)
    terms_str = [(term_to_pauli_string(t, N_QUBITS), complex(c))
                 for t, c in qop.terms.items()]

    nc_terms, c_terms = greedy_noncontextual_partition(terms_str)
    nc_strings = [ps for ps, _ in nc_terms]
    print(f"  N terms: {len(terms_str)}  NC: {len(nc_terms)}  C: {len(c_terms)}")

    gens = find_independent_generators(nc_strings, N_QUBITS)
    print(f"  Independent noncontextual stabilizer generators (max {N_QUBITS}): {len(gens)}")
    for g in gens:
        print(f"     {g}")

    # Find nc-ground signs (fix all generators, minimize <H_nc>)
    E_nc_min, best_signs = nc_ground_signs(gens, nc_terms, N_QUBITS)
    print(f"\n  nc-only ground (all {len(gens)} gens fixed): {E_nc_min:.8f} Ha, signs={best_signs}")

    # Sweep: number of stabilizers to fix from all=classical to none=full VQE
    print("\nCS-VQE sweep:")
    print("  q_quantum |   E_CSVQE   |   err vs FCI (Ha)   |  subspace_dim")
    print("  ----------+-------------+---------------------+---------------")
    all_terms = nc_terms + c_terms
    sweep = []
    for k_fixed in range(len(gens), -1, -1):
        # q_quantum = n_qubits - k_fixed (the effective # qubits for VQE)
        E, dim = csvqe_at_q(gens, best_signs, all_terms, N_QUBITS, k_fixed)
        q = int(np.log2(dim))
        err = abs(E - fci_energy)
        print(f"      {q}     |  {E:+.8f}  |    {err:.6f}     |     {dim}")
        sweep.append({
            "n_generators_fixed": k_fixed,
            "q_quantum_qubits": q,
            "subspace_dim": dim,
            "E_csvqe_Ha": E,
            "err_vs_fci_Ha": err,
            "within_chemical_accuracy": bool(err < CHEMICAL_ACCURACY_HA),
        })

    result = {
        "molecule": "H2",
        "basis": "STO-3G",
        "bond_length_A": 0.7414,
        "n_qubits_full": N_QUBITS,
        "n_terms_full": len(terms_str),
        "n_nc_terms": len(nc_terms),
        "n_c_terms": len(c_terms),
        "n_independent_nc_generators": len(gens),
        "nc_generators": gens,
        "nc_ground_signs": [int(s) for s in best_signs] if best_signs else None,
        "hf_energy_Ha": hf_energy,
        "fci_energy_Ha": fci_energy,
        "chemical_accuracy_Ha": CHEMICAL_ACCURACY_HA,
        "sweep": sweep,
    }

    # Interpret: find smallest q where within chemical accuracy
    ca_hits = [s for s in sweep if s["within_chemical_accuracy"]]
    if ca_hits:
        min_q = min(s["q_quantum_qubits"] for s in ca_hits)
        print(f"\nSmallest q with |err| < 1.6 mHa: q = {min_q} qubits")
        result["min_q_for_chemical_accuracy"] = min_q
        result["headline_finding"] = (
            f"H2/STO-3G/JW: full VQE needs {N_QUBITS} qubits; "
            f"CS-VQE reaches chemical accuracy at q = {min_q} qubits."
        )
    else:
        print("\nNo q reaches chemical accuracy in this run.")
        result["min_q_for_chemical_accuracy"] = None

    with open("../report/evidence/h2_sweep_result.json", "w") as f:
        json.dump(result, f, indent=2)
    print("\nWritten: ../report/evidence/h2_sweep_result.json")


if __name__ == "__main__":
    main()
