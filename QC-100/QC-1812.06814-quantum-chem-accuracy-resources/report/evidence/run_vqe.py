"""
Independent replication of Kühn et al. arXiv:1812.06814
UCCSD-VQE ground-state energy + two-qubit gate count for H2 and LiH in STO-3G.

Targets from paper (Table SI I, STO-3G, kJ/mol):
  H2:   Etotal(HF)=-2931.8, Ecorr(FCI)=-54.085, Ecorr(UCCSD-VQE)=-54.085,
        # qubits=4,  # two-qubit gates=56
  LiH:  Etotal(HF)=-20642.0, Ecorr(FCI)=-53.348, Ecorr(UCCSD-VQE)=-53.320,
        # qubits=12, # two-qubit gates=1382 (with gate cancellation + MP2 pre-screening)

Approach:
  * Build second-quantized Hamiltonian via PySCF driver in Qiskit Nature.
  * Reference: PySCF HF + FCI for exact ground-state energy.
  * VQE: UCCSD ansatz + Jordan-Wigner mapper, statevector Estimator (V2),
    optimized with scipy.optimize.minimize (L-BFGS-B), starting from HF (params=0).
  * Two-qubit gate count: transpile ansatz to {cx,u3} at opt_level=3 and count CNOTs.
    Paper's counts include chemistry-specific optimizations (gate cancellations, MP2
    pre-screening); our raw count is expected to be higher.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

HARTREE_TO_KJMOL = 2625.499638

from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper
from qiskit_nature.second_q.circuit.library import HartreeFock, UCCSD
from qiskit_nature.units import DistanceUnit
from qiskit.primitives import StatevectorEstimator
from qiskit import transpile
from pyscf import gto, scf, fci


def flush():
    sys.stdout.flush()


def pyscf_reference(atoms, basis="sto-3g", spin=0, charge=0):
    mol = gto.M(atom=atoms, basis=basis, spin=spin, charge=charge, unit="Angstrom", verbose=0)
    mf = scf.RHF(mol) if spin == 0 else scf.ROHF(mol)
    e_hf = mf.kernel()
    cisolver = fci.FCI(mf)
    e_fci = cisolver.kernel()[0]
    ecorr_fci = e_fci - e_hf
    return {
        "e_hf_hartree": float(e_hf),
        "e_fci_hartree": float(e_fci),
        "ecorr_fci_hartree": float(ecorr_fci),
        "e_hf_kjmol": float(e_hf * HARTREE_TO_KJMOL),
        "e_fci_kjmol": float(e_fci * HARTREE_TO_KJMOL),
        "ecorr_fci_kjmol": float(ecorr_fci * HARTREE_TO_KJMOL),
    }


def build_problem(atom_str, basis, charge, spin):
    driver = PySCFDriver(
        atom=atom_str, basis=basis, charge=charge, spin=spin,
        unit=DistanceUnit.ANGSTROM,
    )
    problem = driver.run()
    return problem


def run_vqe_uccsd(atom_str, basis="sto-3g", charge=0, spin=0, vqe_maxiter=200):
    print(f"\n=== VQE UCCSD for {atom_str}  basis={basis}  spin={spin} ===", flush=True)
    t0 = time.time()
    problem = build_problem(atom_str, basis, charge, spin)
    print(f"  # spatial orbitals: {problem.num_spatial_orbitals}", flush=True)
    print(f"  # particles: {problem.num_particles}", flush=True)
    n_spin_orb = 2 * problem.num_spatial_orbitals
    print(f"  # spin orbitals (= paper qubit count): {n_spin_orb}", flush=True)

    hamiltonian_op = problem.hamiltonian.second_q_op()
    mapper = JordanWignerMapper()
    qubit_op = mapper.map(hamiltonian_op)
    n_qubits = qubit_op.num_qubits
    nuclear_rep = problem.hamiltonian.nuclear_repulsion_energy
    print(f"  # qubits (JW): {n_qubits}", flush=True)
    print(f"  nuclear repulsion: {nuclear_rep:.8f} Ha", flush=True)

    initial_state = HartreeFock(problem.num_spatial_orbitals, problem.num_particles, mapper)
    ansatz = UCCSD(
        problem.num_spatial_orbitals, problem.num_particles, mapper,
        initial_state=initial_state,
    )
    n_params = ansatz.num_parameters
    print(f"  UCCSD parameters: {n_params}", flush=True)
    flush()

    # Transpile for gate counting
    print("  transpiling ansatz for gate count...", flush=True)
    t_transp = time.time()
    tqc = transpile(ansatz.decompose(reps=3), basis_gates=["cx", "u3"], optimization_level=3)
    ops = dict(tqc.count_ops())
    cx_count = ops.get("cx", 0)
    print(f"  transpile time: {time.time()-t_transp:.1f}s", flush=True)
    print(f"  transpiled ops: {ops}", flush=True)
    print(f"  # CNOTs (raw, no chem-specific cancellations): {cx_count}", flush=True)

    # Set up VQE energy evaluator using V2 estimator
    estimator = StatevectorEstimator()

    def energy(params):
        pub = (ansatz, [qubit_op], [params.tolist()])
        job = estimator.run([pub])
        res = job.result()
        val = float(res[0].data.evs[0])
        return val

    # Initial energy at params=0 (HF state)
    x0 = np.zeros(n_params)
    e0 = energy(x0)
    print(f"  E at HF init (params=0): {e0:.8f} Ha (Etotal={e0+nuclear_rep:.8f})", flush=True)

    # Optimize with L-BFGS-B
    print("  running L-BFGS-B optimization...", flush=True)
    iter_count = [0]
    best = [e0, x0.copy()]

    def obj(params):
        iter_count[0] += 1
        e = energy(params)
        if e < best[0]:
            best[0] = e
            best[1] = params.copy()
        if iter_count[0] % 20 == 0:
            print(f"    eval {iter_count[0]}: E_elec={e:.8f} best={best[0]:.8f}", flush=True)
        return e

    res = minimize(obj, x0, method="L-BFGS-B",
                   options={"maxiter": vqe_maxiter, "ftol": 1e-10, "gtol": 1e-8})
    e_elec = float(best[0])
    e_total = e_elec + nuclear_rep
    dt = time.time() - t0
    print(f"  VQE optimized E_elec = {e_elec:.8f} Ha", flush=True)
    print(f"  VQE E_total          = {e_total:.8f} Ha  ({e_total*HARTREE_TO_KJMOL:.3f} kJ/mol)", flush=True)
    print(f"  wall: {dt:.1f}s, evals: {iter_count[0]}", flush=True)

    return {
        "atom": atom_str,
        "basis": basis,
        "n_spin_orbitals_qubits": n_spin_orb,
        "n_qubits_jw": n_qubits,
        "n_uccsd_params": n_params,
        "nuclear_repulsion_hartree": float(nuclear_rep),
        "transpiled_ops": ops,
        "n_cnots_raw_transpile": int(cx_count),
        "vqe_e_electronic_hartree": e_elec,
        "vqe_total_energy_hartree": e_total,
        "vqe_total_energy_kjmol": e_total * HARTREE_TO_KJMOL,
        "vqe_seconds": dt,
        "optimizer_evals": iter_count[0],
        "optimizer_success": bool(res.success),
        "optimizer_message": str(res.message),
    }


def compare(system, paper, ref, vqe):
    ecorr_vqe_hartree = vqe["vqe_total_energy_hartree"] - ref["e_hf_hartree"]
    ecorr_vqe_kjmol = ecorr_vqe_hartree * HARTREE_TO_KJMOL
    delta_fci_hartree = vqe["vqe_total_energy_hartree"] - ref["e_fci_hartree"]
    delta_fci_kjmol = delta_fci_hartree * HARTREE_TO_KJMOL
    chem_accuracy_hartree = 1.6e-3
    return {
        "system": system,
        "paper": paper,
        "our_e_hf_kjmol": ref["e_hf_kjmol"],
        "our_e_fci_kjmol": ref["e_fci_kjmol"],
        "our_ecorr_fci_kjmol": ref["ecorr_fci_kjmol"],
        "our_vqe_total_kjmol": vqe["vqe_total_energy_kjmol"],
        "our_ecorr_vqe_kjmol": ecorr_vqe_kjmol,
        "delta_vqe_vs_fci_hartree": float(delta_fci_hartree),
        "delta_vqe_vs_fci_mHa": float(delta_fci_hartree * 1000),
        "delta_vqe_vs_fci_kjmol": float(delta_fci_kjmol),
        "chem_accuracy_pass": bool(abs(delta_fci_hartree) < chem_accuracy_hartree),
        "our_qubits": vqe["n_qubits_jw"],
        "paper_qubits": paper["qubits"],
        "qubits_match": vqe["n_qubits_jw"] == paper["qubits"],
        "our_cnots_raw_transpile": vqe["n_cnots_raw_transpile"],
        "paper_two_qubit_gates_optimized": paper["two_qubit_gates"],
    }


def main():
    outdir = Path(__file__).resolve().parent
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    results = {}

    if which in ("h2", "both"):
        print("\n############ H2 (STO-3G) ############", flush=True)
        h2_atoms = "H 0 0 0; H 0 0 0.735"
        h2_ref = pyscf_reference(h2_atoms, basis="sto-3g", spin=0, charge=0)
        print(f"  HF   = {h2_ref['e_hf_hartree']:.8f} Ha = {h2_ref['e_hf_kjmol']:.3f} kJ/mol", flush=True)
        print(f"  FCI  = {h2_ref['e_fci_hartree']:.8f} Ha = {h2_ref['e_fci_kjmol']:.3f} kJ/mol", flush=True)
        print(f"  Ecorr(FCI) = {h2_ref['ecorr_fci_hartree']:.6f} Ha = {h2_ref['ecorr_fci_kjmol']:.3f} kJ/mol", flush=True)
        h2_vqe = run_vqe_uccsd(h2_atoms, basis="sto-3g", charge=0, spin=0, vqe_maxiter=200)
        h2_cmp = compare(
            "H2",
            paper={
                "etotal_hf_kjmol": -2931.8, "ecorr_fci_kjmol": -54.085,
                "ecorr_uccsd_vqe_kjmol": -54.085, "delta_fci_uccsd_vqe_kjmol": 0.0,
                "qubits": 4, "two_qubit_gates": 56,
            },
            ref=h2_ref, vqe=h2_vqe,
        )
        results["H2"] = {"ref": h2_ref, "vqe": h2_vqe, "compare": h2_cmp}

    if which in ("lih", "both"):
        print("\n############ LiH (STO-3G) ############", flush=True)
        lih_atoms = "Li 0 0 0; H 0 0 1.595"
        lih_ref = pyscf_reference(lih_atoms, basis="sto-3g", spin=0, charge=0)
        print(f"  HF   = {lih_ref['e_hf_hartree']:.8f} Ha = {lih_ref['e_hf_kjmol']:.3f} kJ/mol", flush=True)
        print(f"  FCI  = {lih_ref['e_fci_hartree']:.8f} Ha = {lih_ref['e_fci_kjmol']:.3f} kJ/mol", flush=True)
        print(f"  Ecorr(FCI) = {lih_ref['ecorr_fci_hartree']:.6f} Ha = {lih_ref['ecorr_fci_kjmol']:.3f} kJ/mol", flush=True)
        lih_vqe = run_vqe_uccsd(lih_atoms, basis="sto-3g", charge=0, spin=0, vqe_maxiter=150)
        lih_cmp = compare(
            "LiH",
            paper={
                "etotal_hf_kjmol": -20642.0, "ecorr_fci_kjmol": -53.348,
                "ecorr_uccsd_vqe_kjmol": -53.320, "delta_fci_uccsd_vqe_kjmol": 0.028,
                "qubits": 12, "two_qubit_gates": 1382,
            },
            ref=lih_ref, vqe=lih_vqe,
        )
        results["LiH"] = {"ref": lih_ref, "vqe": lih_vqe, "compare": lih_cmp}

    print("\n============ SUMMARY ============", flush=True)
    for name, r in results.items():
        c = r["compare"]
        print(f"\n[{name}]", flush=True)
        print(f"  Etotal HF        our={c['our_e_hf_kjmol']:.2f}  paper={c['paper']['etotal_hf_kjmol']}   kJ/mol", flush=True)
        print(f"  Ecorr FCI        our={c['our_ecorr_fci_kjmol']:.3f}  paper={c['paper']['ecorr_fci_kjmol']}  kJ/mol", flush=True)
        print(f"  Ecorr VQE-UCCSD  our={c['our_ecorr_vqe_kjmol']:.3f}  paper={c['paper']['ecorr_uccsd_vqe_kjmol']}  kJ/mol", flush=True)
        print(f"  |E_VQE - E_FCI|  = {abs(c['delta_vqe_vs_fci_mHa']):.4f} mHa  (chem accuracy 1.6 mHa: {'PASS' if c['chem_accuracy_pass'] else 'FAIL'})", flush=True)
        print(f"  qubits           our={c['our_qubits']}  paper={c['paper_qubits']}  match={c['qubits_match']}", flush=True)
        print(f"  CNOT count       our(raw,opt3)={c['our_cnots_raw_transpile']}  paper(opt.w/MP2+cancel)={c['paper_two_qubit_gates_optimized']}", flush=True)

    outpath = outdir / f"vqe_results_{which}.json"
    with open(outpath, "w") as fh:
        json.dump(results, fh, indent=2, default=str)
    print(f"\nWrote {outpath}", flush=True)


if __name__ == "__main__":
    main()
