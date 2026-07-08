"""
Independent replication of arXiv:2203.02012 (Otten et al. 2022)
"Localized Quantum Chemistry on Quantum Computers" — LAS-UCC.

Reproducible core:
  System: (H2)2 dimer, STO-3G basis, CAS(4e,4o).
    - Paper's Fig. 3 uses (H2)2 to show that LAS-UCC recovers CASCI
      energy within chemical accuracy at all H2-H2 separations.
    - With STO-3G and CAS(4,4), CASSCF == FCI, so CASCI energy IS the
      exact reference for this active space.

  Methods compared (real simulation via PySCF + Qiskit Nature):
    1) HF (RHF/STO-3G)                         -- baseline mean field
    2) FCI (== CASCI(4,4)/STO-3G)              -- exact reference
    3) VQE-UCCSD on canonical orbitals         -- "full" quantum VQE
    4) VQE-UCCSD on Boys-localized orbitals    -- localized-orbital VQE
       (both active-space CAS(4,4) mapped to 4 qubits via parity + 2q reduction
        or JW 8-qubit; we use ParityMapper for compactness)

  Headline check:
    LAS-UCC target is chemical accuracy (< 1.6 mHartree) vs CASCI/FCI
    across the dissociation coordinate. We scan R(H2-H2) at 3 geometries
    (short/equilibrium/long) and check:
      |E_VQE_canonical - E_FCI| < 1.6 mHa      ?
      |E_VQE_localized - E_FCI| < 1.6 mHa      ?

Output: JSON to report/evidence/results.json
"""
import json, os, sys, time, traceback
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EVID = ROOT / "report" / "evidence"
EVID.mkdir(parents=True, exist_ok=True)

CHEMACC = 1.6e-3  # Hartree

def build_h4(r_intra=0.74, r_inter=1.5):
    """(H2)2: two H2 monomers, colinear, separated by r_inter (Angstrom)."""
    # H---H  ...  H---H
    z0 = 0.0
    z1 = r_intra
    z2 = r_intra + r_inter
    z3 = r_intra + r_inter + r_intra
    return [("H", (0., 0., z0)),
            ("H", (0., 0., z1)),
            ("H", (0., 0., z2)),
            ("H", (0., 0., z3))]

def run_classical(atoms, basis="sto-3g"):
    from pyscf import gto, scf, fci, lo, mcscf
    mol = gto.M(atom=atoms, basis=basis, unit="Angstrom", verbose=0, symmetry=False)
    mf = scf.RHF(mol).run(verbose=0)
    e_hf = mf.e_tot
    # FCI (= CASCI(4,4) since 4 electrons in 4 STO-3G orbitals)
    cisolver = fci.FCI(mf)
    e_fci, _ = cisolver.kernel()
    return mol, mf, e_hf, e_fci

def boys_localize(mf):
    """Return Boys-localized MO coefficients for the OCCUPIED space,
    then form a full C = [C_occ_loc | C_virt_loc]. Boys is a natural
    proxy for the 'localized active-space' orbitals used in LAS/LASSCF."""
    from pyscf import lo
    mo = mf.mo_coeff
    nocc = mf.mol.nelectron // 2
    # Localize occupied
    loc_occ = lo.Boys(mf.mol, mo[:, :nocc]).kernel()
    # Localize virtual too (still Boys)
    loc_vir = lo.Boys(mf.mol, mo[:, nocc:]).kernel()
    C_loc = np.hstack([loc_occ, loc_vir])
    return C_loc

def run_vqe(mf, mo_coeff, label):
    """Run VQE with UCCSD ansatz using the supplied MO coefficient set.
    Uses ParityMapper + 2-qubit reduction (4-qubit problem for H4/STO-3G, 4 e in 4 o).
    """
    from qiskit_nature.second_q.drivers import PySCFDriver
    from qiskit_nature.second_q.problems import ElectronicStructureProblem
    from qiskit_nature.second_q.mappers import ParityMapper
    from qiskit_nature.second_q.circuit.library import UCCSD, HartreeFock
    from qiskit_nature.second_q.hamiltonians import ElectronicEnergy
    from qiskit_nature.second_q.formats.qcschema_translator import (
        qcschema_to_problem,
    )
    from qiskit_algorithms import VQE
    from qiskit_algorithms.optimizers import SLSQP, L_BFGS_B, COBYLA
    from qiskit.primitives import StatevectorEstimator, Estimator

    # Build ElectronicStructureProblem directly from PySCF using supplied MOs.
    # We swap the mo_coeff on a copy of mf, then let qiskit_nature ingest.
    from pyscf import scf
    mf2 = scf.RHF(mf.mol)
    mf2.mo_coeff = mo_coeff
    mf2.mo_occ = mf.mo_occ.copy()
    mf2.mo_energy = np.zeros(mo_coeff.shape[1])  # placeholder
    mf2.e_tot = mf.e_tot

    from qiskit_nature.second_q.formats.fcidump_translator import fcidump_to_problem
    from qiskit_nature.second_q.formats.fcidump import FCIDump
    # Use PySCF ao2mo to get integrals in the given MO basis, then build problem.
    from pyscf import ao2mo
    mol = mf.mol
    h1e = mo_coeff.T @ mf.get_hcore() @ mo_coeff
    nmo = mo_coeff.shape[1]
    eri = ao2mo.kernel(mol, mo_coeff, compact=False).reshape(nmo, nmo, nmo, nmo)
    e_nuc = mol.energy_nuc()

    # Build ElectronicEnergy from integrals
    from qiskit_nature.second_q.operators import ElectronicIntegrals, PolynomialTensor
    # Chemist-ordering ERI expected? qiskit_nature.ElectronicIntegrals.from_raw_integrals
    # expects physicist-ordering for 2-body? Docs: from_raw_integrals expects
    # (h1_a, h2_aa, h1_b=None, h2_ba=None, h2_bb=None, *, auto_index_order=True)
    # with chemist ordering when auto_index_order=True (default).
    from qiskit_nature.second_q.hamiltonians import ElectronicEnergy as EE
    ee = EE.from_raw_integrals(h1e, eri)  # chemist by default
    ee.nuclear_repulsion_energy = e_nuc

    from qiskit_nature.second_q.problems import ElectronicStructureProblem
    problem = ElectronicStructureProblem(ee)
    problem.num_particles = (mol.nelectron // 2, mol.nelectron // 2)
    problem.num_spatial_orbitals = nmo

    mapper = ParityMapper(num_particles=problem.num_particles)
    ansatz = UCCSD(
        num_spatial_orbitals=problem.num_spatial_orbitals,
        num_particles=problem.num_particles,
        qubit_mapper=mapper,
        initial_state=HartreeFock(
            num_spatial_orbitals=problem.num_spatial_orbitals,
            num_particles=problem.num_particles,
            qubit_mapper=mapper,
        ),
    )
    op = mapper.map(problem.hamiltonian.second_q_op())

    # Statevector Estimator (V1 API expected by qiskit_algorithms 0.4)
    from qiskit.primitives import Estimator as EstimatorV1
    estimator = EstimatorV1()

    from qiskit_algorithms.optimizers import SLSQP
    vqe = VQE(estimator, ansatz, SLSQP(maxiter=200))
    vqe.initial_point = np.zeros(ansatz.num_parameters)

    t0 = time.time()
    result = vqe.compute_minimum_eigenvalue(op)
    dt = time.time() - t0

    e_elec = float(np.real(result.eigenvalue))
    e_tot = e_elec + e_nuc
    return {
        "label": label,
        "e_total": e_tot,
        "e_elec": e_elec,
        "e_nuc": e_nuc,
        "num_parameters": ansatz.num_parameters,
        "num_qubits": op.num_qubits,
        "vqe_seconds": dt,
        "iters": getattr(result, "cost_function_evals", None),
    }

def main():
    results = {"paper": "arXiv:2203.02012", "system": "(H2)2 dimer STO-3G CAS(4,4)"}
    results["geometries"] = []
    geometries = [
        ("short", 0.74, 1.0),      # short H2-H2 separation
        ("equilibrium", 0.74, 1.5),
        ("long", 0.74, 3.0),
    ]
    for label, r_intra, r_inter in geometries:
        print(f"\n=== Geometry: {label} r_intra={r_intra} r_inter={r_inter} ===", flush=True)
        atoms = build_h4(r_intra, r_inter)
        try:
            mol, mf, e_hf, e_fci = run_classical(atoms)
            print(f"  HF  = {e_hf:.8f}", flush=True)
            print(f"  FCI = {e_fci:.8f}", flush=True)
            geom_res = {
                "label": label,
                "r_intra": r_intra,
                "r_inter": r_inter,
                "e_hf": e_hf,
                "e_fci": e_fci,
            }

            # Canonical MO VQE
            try:
                r_can = run_vqe(mf, mf.mo_coeff, "vqe_canonical_uccsd")
                geom_res["vqe_canonical"] = r_can
                dE = r_can["e_total"] - e_fci
                print(f"  VQE canonical UCCSD = {r_can['e_total']:.8f}  ΔE_FCI = {dE*1e3:+.3f} mHa  ({r_can['num_qubits']} qubits, {r_can['num_parameters']} params, {r_can['vqe_seconds']:.1f}s)", flush=True)
            except Exception as e:
                geom_res["vqe_canonical_error"] = f"{type(e).__name__}: {e}"
                traceback.print_exc()

            # Boys-localized MO VQE
            try:
                C_loc = boys_localize(mf)
                r_loc = run_vqe(mf, C_loc, "vqe_boys_localized_uccsd")
                geom_res["vqe_localized"] = r_loc
                dE = r_loc["e_total"] - e_fci
                print(f"  VQE Boys-loc UCCSD  = {r_loc['e_total']:.8f}  ΔE_FCI = {dE*1e3:+.3f} mHa  ({r_loc['num_qubits']} qubits, {r_loc['num_parameters']} params, {r_loc['vqe_seconds']:.1f}s)", flush=True)
            except Exception as e:
                geom_res["vqe_localized_error"] = f"{type(e).__name__}: {e}"
                traceback.print_exc()

            results["geometries"].append(geom_res)
        except Exception as e:
            print(f"  FAILED: {type(e).__name__}: {e}", flush=True)
            traceback.print_exc()
            results["geometries"].append({"label": label, "error": f"{type(e).__name__}: {e}"})

    # Verdict logic
    verdict = "UNKNOWN"
    notes = []
    ok_can = 0; ok_loc = 0; n = 0
    for g in results["geometries"]:
        if "e_fci" in g and "vqe_canonical" in g:
            n += 1
            if abs(g["vqe_canonical"]["e_total"] - g["e_fci"]) < CHEMACC:
                ok_can += 1
            if "vqe_localized" in g and abs(g["vqe_localized"]["e_total"] - g["e_fci"]) < CHEMACC:
                ok_loc += 1
    results["summary"] = {
        "n_geoms": n,
        "canonical_within_chemacc": ok_can,
        "localized_within_chemacc": ok_loc,
        "chemical_accuracy_Ha": CHEMACC,
    }
    print(f"\n=== Summary === geoms={n} canonical_chemacc={ok_can}/{n} localized_chemacc={ok_loc}/{n}", flush=True)

    out = EVID / "results.json"
    out.write_text(json.dumps(results, indent=2))
    print(f"Wrote {out}")
    return results

if __name__ == "__main__":
    main()
