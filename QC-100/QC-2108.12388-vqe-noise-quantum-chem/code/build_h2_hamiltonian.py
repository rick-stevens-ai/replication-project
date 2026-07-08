"""Build the exact H2 STO-3G Hamiltonian at R=0.735 A via PySCF + OpenFermion,
then Jordan-Wigner map it to 4 qubits and export as a Qiskit SparsePauliOp.

Reference target ground state: -1.1373 Ha (Sung et al. 2021, arXiv:2108.12388,
section V.A: 'The true ground state energy of hydrogen is -1.1373 hartree.').
"""
import json
import numpy as np
from openfermion.chem import MolecularData
from openfermionpyscf import run_pyscf
from openfermion.transforms import jordan_wigner, get_fermion_operator
from qiskit.quantum_info import SparsePauliOp


def build_h2(bond_length: float = 0.735):
    geom = [('H', (0., 0., 0.)), ('H', (0., 0., bond_length))]
    mol = MolecularData(geom, basis='sto-3g', multiplicity=1, charge=0,
                        description=f'h2_{bond_length}')
    mol = run_pyscf(mol, run_scf=True, run_fci=True)
    hf_energy = mol.hf_energy
    fci_energy = mol.fci_energy

    ham_fop = get_fermion_operator(mol.get_molecular_hamiltonian())
    qubit_ham = jordan_wigner(ham_fop)
    return mol, qubit_ham, hf_energy, fci_energy


def openfermion_to_qiskit_sparsepauliop(qubit_op, n_qubits: int) -> SparsePauliOp:
    """Convert an OpenFermion QubitOperator to a Qiskit SparsePauliOp."""
    pauli_strings = []
    coeffs = []
    for term, coeff in qubit_op.terms.items():
        # term is a tuple of (qubit_index, pauli_letter) pairs
        chars = ['I'] * n_qubits
        for q, p in term:
            chars[q] = p  # 'X', 'Y', 'Z'
        # Qiskit convention: qubit 0 is the RIGHTMOST character in the string.
        pauli_str = ''.join(reversed(chars))
        pauli_strings.append(pauli_str)
        coeffs.append(complex(coeff))
    return SparsePauliOp(pauli_strings, coeffs=coeffs)


if __name__ == "__main__":
    mol, qham, hf, fci = build_h2(0.735)
    n_qubits = mol.n_qubits
    print(f"n_qubits (spin orbitals) = {n_qubits}")
    print(f"HF energy  = {hf:.6f} Ha")
    print(f"FCI energy = {fci:.6f} Ha")
    print(f"Number of Pauli terms (JW): {len(qham.terms)}")

    spo = openfermion_to_qiskit_sparsepauliop(qham, n_qubits)
    # verify by exact diag
    mat = spo.to_matrix()
    eigs = np.linalg.eigvalsh(mat)
    ground = eigs[0].real
    print(f"Ground state via exact diag of qiskit SparsePauliOp: {ground:.6f} Ha")
    print(f"Paper reference (Sung 2021): -1.1373 Ha")
    print(f"Match FCI vs qiskit-diag: |diff|={abs(ground-fci):.2e}")

    # persist
    out = {
        "bond_length_angstrom": 0.735,
        "basis": "sto-3g",
        "mapping": "jordan-wigner",
        "n_qubits": int(n_qubits),
        "hf_energy_ha": float(hf),
        "fci_energy_ha": float(fci),
        "paper_reference_ha": -1.1373,
        "qiskit_exact_diag_ha": float(ground),
        "pauli_terms": [
            {"pauli": p, "coeff_real": float(c.real), "coeff_imag": float(c.imag)}
            for p, c in zip([str(pl) for pl in spo.paulis], spo.coeffs)
        ],
    }
    import os
    os.makedirs("data", exist_ok=True)
    with open("data/h2_hamiltonian.json", "w") as f:
        json.dump(out, f, indent=2)
    print("Wrote data/h2_hamiltonian.json")
