"""Build Hn-chain molecular Hamiltonian as a sum of Pauli terms, save to JSON.

Default: H2/STO-3G at bond length 0.735 Å (~15-term Hamiltonian on 4 qubits).
Also supports H4, H6 chains for bigger workloads where per-Pauli evaluation
becomes non-trivial (needed to see parallelism speedup on classical sim).
"""
import argparse
import json
import numpy as np

from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper


def build_hn_chain(n_atoms: int = 2, bond_length: float = 0.735):
    coords = "; ".join(f"H 0 0 {i*bond_length}" for i in range(n_atoms))
    driver = PySCFDriver(
        atom=coords,
        basis="sto3g",
        charge=0,
        spin=0,
        unit=DistanceUnit.ANGSTROM,
    )
    problem = driver.run()
    second_q_op = problem.hamiltonian.second_q_op()
    mapper = JordanWignerMapper()
    qubit_op = mapper.map(second_q_op)

    terms = []
    for pauli, coeff in zip(qubit_op.paulis, qubit_op.coeffs):
        terms.append({"pauli": str(pauli),
                      "coeff_real": float(np.real(coeff)),
                      "coeff_imag": float(np.imag(coeff))})

    nuclear_repulsion = float(problem.nuclear_repulsion_energy)

    H_mat = qubit_op.to_matrix()
    eigvals = np.linalg.eigvalsh(H_mat)
    electronic_ground = float(eigvals[0])
    total_ground = electronic_ground + nuclear_repulsion

    return {
        "molecule": f"H{n_atoms} chain",
        "n_atoms": n_atoms,
        "bond_length_angstrom": bond_length,
        "basis": "sto3g",
        "n_qubits": qubit_op.num_qubits,
        "n_pauli_terms": len(terms),
        "nuclear_repulsion_energy": nuclear_repulsion,
        "electronic_ground_energy_hartree": electronic_ground,
        "total_ground_energy_hartree": total_ground,
        "terms": terms,
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n_atoms", type=int, default=2)
    ap.add_argument("--bond_length", type=float, default=0.735)
    ap.add_argument("--out", default="h2_hamiltonian.json")
    args = ap.parse_args()

    data = build_hn_chain(args.n_atoms, args.bond_length)
    with open(args.out, "w") as f:
        json.dump(data, f, indent=2)
    print(f"molecule={data['molecule']}")
    print(f"n_qubits={data['n_qubits']}  n_pauli_terms={data['n_pauli_terms']}")
    print(f"nuclear_repulsion={data['nuclear_repulsion_energy']:.6f} Ha")
    print(f"electronic_ground={data['electronic_ground_energy_hartree']:.6f} Ha")
    print(f"total_ground={data['total_ground_energy_hartree']:.6f} Ha")
    print(f"wrote {args.out}")
