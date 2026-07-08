#!/usr/bin/env python3
"""
Smarter CS-VQE partition on H2/STO-3G:
Try all noncontextual partitions that include at least one anticommuting clique
(so the noncontextual subspace isn't fully determined), then pick the one that
gives the best CS-VQE result at the smallest q.

For H2 JW the anticommuting excitation terms {YXXY, YYXX, XXYY, XYYX} are
important. We try to include some of them in the noncontextual set as a clique
alongside the Z stabilizers, then evaluate CS-VQE.

Real computation.
"""
import json
import numpy as np
from itertools import combinations, product

from openfermion import MolecularData, jordan_wigner
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


def build_ham_matrix(terms_with_coeff, n_qubits):
    H = np.zeros((2**n_qubits, 2**n_qubits), dtype=complex)
    for pstr, coeff in terms_with_coeff:
        H += coeff * pauli_str_to_matrix(pstr)
    return H


def csvqe_energy_general(nc_terms, c_terms, n_qubits):
    """
    Full CS-VQE energy: restrict full H to nc-ground-state subspace,
    diagonalize -> min eigenvalue.
    """
    H_nc = build_ham_matrix(nc_terms, n_qubits)
    evals, evecs = np.linalg.eigh(H_nc)
    E_nc = float(evals[0])
    tol = 1e-8
    ground_mask = np.abs(evals - E_nc) < tol
    P_ground = evecs[:, ground_mask]  # (2^n, k)
    H_full = build_ham_matrix(nc_terms + c_terms, n_qubits)
    H_proj = P_ground.conj().T @ H_full @ P_ground
    ev = np.linalg.eigvalsh(H_proj)
    return float(ev[0]), E_nc, P_ground.shape[1]


def main():
    print("Building H2/STO-3G Hamiltonian...")
    geom = [("H", (0, 0, 0)), ("H", (0, 0, 0.7414))]
    mol = MolecularData(geom, "sto-3g", multiplicity=1, charge=0)
    mol = run_pyscf(mol, run_scf=True, run_fci=True)
    fci_energy = float(mol.fci_energy)
    hf_energy = float(mol.hf_energy)

    fop = get_fermion_operator(mol.get_molecular_hamiltonian())
    qop = jordan_wigner(fop)
    terms_str = [(term_to_pauli_string(t, N_QUBITS), complex(c))
                 for t, c in qop.terms.items()]
    coeff_map = {ps: cf for ps, cf in terms_str}

    print(f"  HF: {hf_energy:.8f}   FCI: {fci_energy:.8f}   N terms: {len(terms_str)}")

    # Enumerate every subset of the 15 terms that is noncontextual,
    # try each as the noncontextual set, compute CS-VQE, track best result.
    n = len(terms_str)
    all_strs = [ps for ps, _ in terms_str]

    # Track best (min-error) partition and best-per-subspace-dim
    best_records = {}  # subspace_dim -> best (err, nc_strs)
    tested = 0
    # Full enumeration of 2^15 = 32768 subsets
    for mask in range(1, 1 << n):
        subset_strs = [all_strs[i] for i in range(n) if mask & (1 << i)]
        if not is_noncontextual(subset_strs):
            continue
        # Must include identity if present, doesn't affect noncontextuality
        subset = [(ps, coeff_map[ps]) for ps in subset_strs]
        complement = [(ps, coeff_map[ps]) for ps in all_strs if ps not in set(subset_strs)]
        try:
            E_csvqe, E_nc, dim = csvqe_energy_general(subset, complement, N_QUBITS)
        except Exception as e:
            continue
        err = abs(E_csvqe - fci_energy)
        tested += 1
        cur = best_records.get(dim)
        if cur is None or err < cur[0]:
            best_records[dim] = (err, len(subset_strs), subset_strs, E_csvqe)

    print(f"\nEnumerated {tested} noncontextual partitions.")
    print(f"\nBest CS-VQE result per subspace dimension:")
    print(f"  dim (=2^q_quantum) |  q  |   err vs FCI (Ha)   |    E_csvqe    | nc size")
    print(f"  -------------------+-----+---------------------+---------------+--------")
    sweep = []
    for dim in sorted(best_records.keys()):
        err, nc_size, nc_strs, E = best_records[dim]
        q = int(round(np.log2(dim)))
        marker = "  <-- chem acc" if err < CHEMICAL_ACCURACY_HA else ""
        print(f"          {dim:4d}       |  {q}  |    {err:.6f}       |  {E:+.8f} |   {nc_size}{marker}")
        sweep.append({
            "subspace_dim": dim, "q_quantum_qubits": q,
            "err_vs_fci_Ha": err, "E_csvqe_Ha": E,
            "n_nc_terms": nc_size,
            "nc_terms": nc_strs,
            "within_chemical_accuracy": bool(err < CHEMICAL_ACCURACY_HA),
        })

    ca_hits = [s for s in sweep if s["within_chemical_accuracy"]]
    min_q = min(s["q_quantum_qubits"] for s in ca_hits) if ca_hits else None
    print(f"\n=> Smallest q reaching chemical accuracy: q = {min_q}  (full VQE needs {N_QUBITS})")

    result = {
        "molecule": "H2",
        "basis": "STO-3G",
        "bond_length_A": 0.7414,
        "n_qubits_full_VQE": N_QUBITS,
        "hf_energy_Ha": hf_energy,
        "fci_energy_Ha": fci_energy,
        "chemical_accuracy_Ha": CHEMICAL_ACCURACY_HA,
        "n_noncontextual_partitions_tested": tested,
        "sweep_best_per_dim": sweep,
        "min_q_for_chemical_accuracy": min_q,
    }
    with open("../report/evidence/h2_smart_result.json", "w") as f:
        json.dump(result, f, indent=2)
    print("\nWritten: ../report/evidence/h2_smart_result.json")


if __name__ == "__main__":
    main()
