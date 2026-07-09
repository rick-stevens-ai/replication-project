"""
Independent replication of the H2 STO-3G VQE result from
Meirom & Frankel, "PANSATZ: pulse-based ansatz for variational quantum algorithms",
Front. Quantum Sci. Technol. 2:1273581 (2023), DOI 10.3389/frqst.2023.1273581.

Paper claim being reproduced (headline number):
  Using VQE on the 2-qubit parity-reduced STO-3G H2 Hamiltonian, they reach
  chemical accuracy (|E_VQE - E_FCI| < 0.0016 Ha = 1 mHa in their statement) across
  all H-H atomic distances (Fig. 3A, 3D of the paper).

Our reproduction (gate-based analog of their PANSATZ / GANSATZ,
Qiskit statevector — noise-free upper bound on what any ansatz can achieve):

  1. Build the H2 electronic Hamiltonian in STO-3G at several bond distances.
  2. Do parity mapping + two-qubit reduction (matches their setup exactly).
  3. FCI reference = exact eigendecomposition of the reduced Hamiltonian
     (= numerical FCI in STO-3G, since the full 4-spin-orbital active space
      IS the full space).
  4. VQE with EfficientSU2 (functionally equivalent hardware-efficient
     ansatz; RealAmplitudes has same connectivity but Y-rotations are
     needed for real-valued singlet ground state — matches the paper's
     "Real Amplitudes HEA" (GANSATZ) family).
  5. Report |E_VQE - E_FCI| per distance and check chemical-accuracy claim.
"""
import json
import os
import time
import numpy as np
from scipy.optimize import minimize

# ---- 1. Build H2 STO-3G electronic Hamiltonian via PySCF, map to qubits ----
from pyscf import gto, scf, fci as pyscf_fci

from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import ParityMapper
from qiskit_nature.units import DistanceUnit
from qiskit.circuit.library import EfficientSU2
from qiskit.quantum_info import SparsePauliOp, Statevector


def h2_hamiltonian(bond_len_ang: float):
    """Return (qubit_op, nuclear_rep_energy, hf_energy, fci_energy).

    Uses parity mapping + two_qubit_reduction to match Meirom&Frankel 2023.
    hf/fci are computed classically via PySCF as sanity references.
    """
    driver = PySCFDriver(
        atom=f"H 0 0 0; H 0 0 {bond_len_ang}",
        basis="sto3g",
        unit=DistanceUnit.ANGSTROM,
    )
    problem = driver.run()
    hamiltonian_op = problem.hamiltonian.second_q_op()
    nuclear_rep = problem.nuclear_repulsion_energy
    hf_energy = problem.reference_energy

    # Parity mapper with two-qubit reduction (num_particles required for that)
    mapper = ParityMapper(num_particles=problem.num_particles)
    qubit_op = mapper.map(hamiltonian_op)

    # Independent FCI via PySCF (fully independent path, not through qiskit-nature)
    mol = gto.M(
        atom=f"H 0 0 0; H 0 0 {bond_len_ang}",
        basis="sto-3g",
        unit="Angstrom",
    )
    mf = scf.RHF(mol).run(verbose=0)
    cisolver = pyscf_fci.FCI(mf)
    fci_energy = cisolver.kernel()[0]

    return qubit_op, nuclear_rep, hf_energy, fci_energy


def exact_ground_energy(qubit_op: SparsePauliOp) -> float:
    """Exact eigen-decomposition of the qubit Hamiltonian (2 qubits → 4x4)."""
    H = qubit_op.to_matrix()
    eigvals = np.linalg.eigvalsh(H)
    return float(np.min(eigvals).real)


def vqe_statevector(qubit_op: SparsePauliOp, reps: int = 2, seed: int = 42):
    """Statevector VQE with EfficientSU2 (gate-based HEA, GANSATZ analog).

    Returns (best_energy, n_iters, opt_time_s, best_params).
    """
    n_qubits = qubit_op.num_qubits
    ansatz = EfficientSU2(num_qubits=n_qubits, reps=reps, entanglement="linear")
    n_params = ansatz.num_parameters

    H_mat = qubit_op.to_matrix()

    rng = np.random.default_rng(seed)
    x0 = rng.uniform(-np.pi, np.pi, size=n_params)

    calls = [0]

    def cost(params):
        calls[0] += 1
        bound = ansatz.assign_parameters(params)
        psi = Statevector.from_instruction(bound).data
        return float(np.real(np.conjugate(psi) @ H_mat @ psi))

    t0 = time.time()
    # COBYLA is a common classical optimizer for VQE and doesn't need gradients
    res = minimize(cost, x0, method="COBYLA", options={"maxiter": 500, "rhobeg": 0.5})
    dt = time.time() - t0
    return float(res.fun), calls[0], dt, res.x.tolist()


def main():
    distances = [0.5, 0.7, 0.9, 1.1, 1.5, 2.0, 2.5]
    results = []
    for d in distances:
        qop, nuc, hf, fci_py = h2_hamiltonian(d)
        exact_qubit = exact_ground_energy(qop) + nuc  # add nuclear rep back
        vqe_e_qubit, n_iters, dt, params = vqe_statevector(qop, reps=2)
        vqe_total = vqe_e_qubit + nuc
        err_vs_fci = abs(vqe_total - fci_py)
        err_qubit_vs_fci = abs(exact_qubit - fci_py)
        chem_acc = err_vs_fci < 1.6e-3  # 0.0016 Ha per paper
        results.append(
            dict(
                d_angstrom=d,
                nuclear_rep=nuc,
                hf_energy=float(hf),
                fci_pyscf=float(fci_py),
                exact_qubit_H_gs=exact_qubit,
                qubit_H_vs_fci_error=err_qubit_vs_fci,
                vqe_energy=vqe_total,
                vqe_error_vs_fci=err_vs_fci,
                chemical_accuracy=bool(chem_acc),
                vqe_iterations=n_iters,
                optimizer_wall_s=dt,
                n_qubits=qop.num_qubits,
                n_pauli_terms=len(qop),
                ansatz="EfficientSU2 reps=2 linear",
                n_params=EfficientSU2(qop.num_qubits, reps=2, entanglement="linear").num_parameters,
            )
        )
        print(
            f"d={d:.2f}A  FCI={fci_py:+.6f}  VQE={vqe_total:+.6f}  "
            f"|err|={err_vs_fci:.2e} Ha  chem_acc={chem_acc}  it={n_iters}"
        )
    out = dict(
        paper_doi="10.3389/frqst.2023.1273581",
        paper_title="PANSATZ: pulse-based ansatz for variational quantum algorithms",
        headline_number="H2 STO-3G VQE reaches chemical accuracy (0.0016 Ha) vs FCI",
        tool="qiskit + qiskit_nature + pyscf, statevector, COBYLA",
        results=results,
    )
    outdir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(outdir, "h2_vqe_results.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("wrote", os.path.join(outdir, "h2_vqe_results.json"))

    # Summary line
    n_reach = sum(1 for r in results if r["chemical_accuracy"])
    print(
        f"\nSUMMARY: {n_reach}/{len(results)} distances reached chemical accuracy (<1.6 mHa)."
    )
    return out


if __name__ == "__main__":
    main()
