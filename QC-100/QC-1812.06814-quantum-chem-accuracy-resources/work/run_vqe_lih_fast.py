"""
Fast VQE for LiH (STO-3G, 12 qubits) using direct Statevector inner product.
Avoids qiskit primitive overhead. Statevector for 12 qubits = 4096 complex numbers.
"""
from __future__ import annotations
import json, time, sys
from pathlib import Path
import numpy as np
from scipy.optimize import minimize

HARTREE_TO_KJMOL = 2625.499638

from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper
from qiskit_nature.second_q.circuit.library import HartreeFock, UCCSD
from qiskit_nature.units import DistanceUnit
from qiskit.quantum_info import Statevector, SparsePauliOp
from qiskit import transpile
from pyscf import gto, scf, fci


def main():
    print("=== LiH STO-3G fast VQE ===", flush=True)
    t0 = time.time()

    # PySCF reference
    atoms = "Li 0 0 0; H 0 0 1.595"
    mol = gto.M(atom=atoms, basis="sto-3g", spin=0, charge=0, unit="Angstrom", verbose=0)
    mf = scf.RHF(mol)
    e_hf = mf.kernel()
    cisolver = fci.FCI(mf); e_fci = cisolver.kernel()[0]
    print(f"HF={e_hf:.8f} Ha  FCI={e_fci:.8f} Ha  Ecorr(FCI)={(e_fci-e_hf)*HARTREE_TO_KJMOL:.3f} kJ/mol", flush=True)

    # Qiskit Nature problem
    driver = PySCFDriver(atom=atoms, basis="sto-3g", charge=0, spin=0, unit=DistanceUnit.ANGSTROM)
    problem = driver.run()
    nuclear_rep = problem.hamiltonian.nuclear_repulsion_energy
    print(f"nuclear_rep={nuclear_rep:.8f}", flush=True)

    mapper = JordanWignerMapper()
    hamiltonian_op = problem.hamiltonian.second_q_op()
    qubit_op: SparsePauliOp = mapper.map(hamiltonian_op)
    print(f"Hamiltonian: {qubit_op.num_qubits} qubits, {len(qubit_op)} Pauli terms", flush=True)

    initial_state = HartreeFock(problem.num_spatial_orbitals, problem.num_particles, mapper)
    ansatz = UCCSD(problem.num_spatial_orbitals, problem.num_particles, mapper, initial_state=initial_state)
    n_params = ansatz.num_parameters
    print(f"UCCSD params: {n_params}", flush=True)

    # Bind and simulate: build a callable that returns Statevector for given params
    # We use QuantumCircuit.assign_parameters + Statevector.from_instruction.
    ham_matrix = None  # we'll use expectation via SparsePauliOp

    print("Pre-compiling ansatz decomposition once...", flush=True)
    # Decompose ansatz into a fixed circuit shape (parametric) that Statevector can consume fast.
    decomposed = ansatz.decompose(reps=1)

    def energy(params):
        bound = decomposed.assign_parameters(params)
        sv = Statevector.from_instruction(bound)
        e = sv.expectation_value(qubit_op).real
        return float(e)

    x0 = np.zeros(n_params)
    t1 = time.time()
    e0 = energy(x0)
    print(f"Init energy (HF, params=0): E_elec={e0:.8f}  E_tot={e0+nuclear_rep:.8f}  ({(e0+nuclear_rep-e_hf):.2e} vs HF)", flush=True)
    print(f"one energy eval: {time.time()-t1:.2f}s", flush=True)

    iter_ct = [0]; best = [e0, x0.copy()]
    def obj(p):
        iter_ct[0] += 1
        e = energy(p)
        if e < best[0]:
            best[0] = e; best[1] = p.copy()
        if iter_ct[0] % 10 == 0 or iter_ct[0] < 5:
            print(f"  eval {iter_ct[0]}: E_elec={e:.8f} best={best[0]:.8f}  (Ecorr={(best[0]+nuclear_rep-e_hf)*HARTREE_TO_KJMOL:.3f} kJ/mol)", flush=True)
        return e

    print("Starting COBYLA optimization (rhobeg=0.05, maxiter=400)...", flush=True)
    res = minimize(obj, x0, method="COBYLA", options={"maxiter": 400, "rhobeg": 0.05, "catol": 1e-6})
    e_elec = best[0]; e_total = e_elec + nuclear_rep
    dt = time.time() - t0
    print(f"\nVQE E_elec = {e_elec:.8f} Ha", flush=True)
    print(f"VQE E_total= {e_total:.8f} Ha = {e_total*HARTREE_TO_KJMOL:.3f} kJ/mol", flush=True)
    print(f"|E_VQE - E_FCI| = {abs(e_total-e_fci)*1000:.4f} mHa   chem_acc(1.6 mHa)? {abs(e_total-e_fci)<1.6e-3}", flush=True)
    print(f"Ecorr(VQE) = {(e_total-e_hf)*HARTREE_TO_KJMOL:.3f} kJ/mol  (paper VQE={-53.320}, FCI={-53.348})", flush=True)
    print(f"wall: {dt:.1f}s  evals: {iter_ct[0]}", flush=True)

    # Gate count from decomposition-to-cx
    print("\nTranspiling for CNOT count...", flush=True)
    tqc = transpile(ansatz.decompose(reps=3), basis_gates=["cx", "u3"], optimization_level=3)
    ops = dict(tqc.count_ops())
    cx = ops.get("cx", 0)
    print(f"transpiled ops: {ops}", flush=True)
    print(f"# CNOTs (raw, no chem cancels): {cx}", flush=True)

    out = {
        "system": "LiH",
        "basis": "sto-3g",
        "n_qubits": qubit_op.num_qubits,
        "n_uccsd_params": n_params,
        "n_ham_terms": len(qubit_op),
        "nuclear_repulsion": float(nuclear_rep),
        "e_hf_hartree": float(e_hf), "e_fci_hartree": float(e_fci),
        "e_hf_kjmol": float(e_hf*HARTREE_TO_KJMOL), "e_fci_kjmol": float(e_fci*HARTREE_TO_KJMOL),
        "ecorr_fci_kjmol": float((e_fci-e_hf)*HARTREE_TO_KJMOL),
        "vqe_e_elec": float(e_elec), "vqe_e_total": float(e_total),
        "vqe_e_total_kjmol": float(e_total*HARTREE_TO_KJMOL),
        "vqe_ecorr_kjmol": float((e_total-e_hf)*HARTREE_TO_KJMOL),
        "delta_vqe_fci_mHa": float((e_total-e_fci)*1000),
        "chem_accuracy_pass": bool(abs(e_total-e_fci) < 1.6e-3),
        "n_cnots_raw_transpile": int(cx),
        "paper_qubits": 12,
        "paper_two_qubit_gates": 1382,
        "paper_ecorr_vqe_kjmol": -53.320,
        "paper_ecorr_fci_kjmol": -53.348,
        "vqe_seconds": dt, "evals": iter_ct[0], "success": bool(res.success),
    }
    outpath = Path(__file__).resolve().parent / "vqe_results_lih_fast.json"
    with open(outpath, "w") as fh: json.dump(out, fh, indent=2)
    print(f"Wrote {outpath}", flush=True)


if __name__ == "__main__":
    main()
