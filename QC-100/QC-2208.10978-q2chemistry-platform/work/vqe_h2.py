"""
Replication of the Q2Chemistry H2 potential energy curve benchmark
(arXiv:2208.10978, Fig 6): VQE-UCCSD vs FCI.

Paper used ccj-pVDZ (40 qubits, 560 CPU cores, 24h/geom). We use STO-3G
(4 qubits, matches Table 1 of the paper) which is the standard H2 reference
minimal-basis benchmark. Method structure is identical: VQE with UCCSD
ansatz, ground-state energies compared to FCI, potential energy curve.

Stack: OpenFermion + OpenFermion-PySCF for Hamiltonian generation,
Jordan-Wigner encoding, then VQE by scipy.optimize.minimize on the
UCCSD parameters. PySCF FCI for exact ground-state reference.
"""
import json, time
import numpy as np
from scipy.optimize import minimize
from openfermion.chem import MolecularData
from openfermionpyscf import run_pyscf
from openfermion.transforms import jordan_wigner, get_fermion_operator
from openfermion.linalg import get_sparse_operator
from openfermion.circuits import uccsd_singlet_generator, uccsd_singlet_paramsize
import scipy.sparse.linalg as spla

BOHR = 0.5291772109  # not used; distances in Angstrom

def h2_at(distance):
    geometry = [('H', (0.0, 0.0, 0.0)), ('H', (0.0, 0.0, distance))]
    basis = 'sto-3g'
    multiplicity = 1
    charge = 0
    mol = MolecularData(geometry, basis, multiplicity, charge,
                        description=f'H2_{distance:.3f}')
    mol = run_pyscf(mol, run_scf=True, run_fci=True, run_ccsd=True)
    return mol

def vqe_uccsd_energy(mol):
    # Build qubit Hamiltonian
    ferm_op = get_fermion_operator(mol.get_molecular_hamiltonian())
    qubit_op = jordan_wigner(ferm_op)
    n_qubits = mol.n_qubits
    n_electrons = mol.n_electrons
    H_sparse = get_sparse_operator(qubit_op, n_qubits=n_qubits)

    # Hartree-Fock reference state (bitstring: lowest n_electrons spin-orbitals filled)
    # Jordan-Wigner mapping: orbital i occupied -> qubit i = |1>
    hf_index = 0
    for i in range(n_electrons):
        hf_index |= (1 << i)
    hf_state = np.zeros(2**n_qubits, dtype=complex)
    hf_state[hf_index] = 1.0

    # UCCSD singlet generator: T - T^dagger, real amplitude parameters
    n_params = uccsd_singlet_paramsize(n_qubits, n_electrons)

    def energy(params):
        gen = uccsd_singlet_generator(list(params), n_qubits, n_electrons,
                                       anti_hermitian=True)
        gen_qubit = jordan_wigner(gen)
        gen_sparse = get_sparse_operator(gen_qubit, n_qubits=n_qubits)
        # exp(gen) |HF>
        psi = spla.expm_multiply(gen_sparse, hf_state)
        e = np.real(np.vdot(psi, H_sparse.dot(psi)))
        return float(e)

    # Small random start; zero-vector is a saddle point for the anti-hermitian
    # UCCSD generator around the HF reference, which BFGS can't escape.
    rng = np.random.default_rng(42)
    x0 = rng.standard_normal(n_params) * 0.05
    t0 = time.time()
    # COBYLA gradient-free (matches paper's BOBYQA gradient-free choice for VQE)
    res = minimize(energy, x0, method='COBYLA',
                   options={'rhobeg': 0.1, 'maxiter': 2000, 'catol': 1e-8})
    # Polish with BFGS (which uses finite diff)
    res2 = minimize(energy, res.x, method='BFGS',
                    options={'gtol': 1e-7, 'maxiter': 500})
    e_final = min(res.fun, res2.fun)
    n_iter = res.nfev + res2.nit
    vqe_time = time.time() - t0
    return e_final, n_iter, n_params, vqe_time

def main():
    distances = [0.5, 0.735, 1.0, 1.5, 2.0]  # angstrom; 0.735 is near-equilibrium
    results = []
    for d in distances:
        print(f'\n=== H2 at d={d} A ===', flush=True)
        mol = h2_at(d)
        e_fci = float(mol.fci_energy)
        e_hf = float(mol.hf_energy)
        e_ccsd = float(mol.ccsd_energy) if mol.ccsd_energy is not None else None
        print(f'  HF    = {e_hf:.8f}', flush=True)
        print(f'  FCI   = {e_fci:.8f}', flush=True)
        print(f'  CCSD  = {e_ccsd:.8f}' if e_ccsd is not None else '  CCSD  = n/a', flush=True)
        e_vqe, n_iter, n_params, vqe_t = vqe_uccsd_energy(mol)
        err_ha = abs(e_vqe - e_fci)
        err_mha = err_ha * 1000.0
        chem_acc = err_mha < 1.6  # 1 kcal/mol = 1.594 mHa
        print(f'  VQE   = {e_vqe:.8f}  (n_params={n_params}, iters={n_iter}, {vqe_t:.1f}s)', flush=True)
        print(f'  |VQE-FCI| = {err_mha:.4f} mHa  chemical_accuracy={chem_acc}', flush=True)
        results.append({
            'distance_ang': d,
            'n_qubits': mol.n_qubits,
            'n_electrons': mol.n_electrons,
            'n_uccsd_params': n_params,
            'hf_energy_ha': e_hf,
            'ccsd_energy_ha': e_ccsd,
            'fci_energy_ha': e_fci,
            'vqe_energy_ha': e_vqe,
            'vqe_minus_fci_mha': err_mha,
            'chemical_accuracy_1p6mHa': chem_acc,
            'vqe_iterations': int(n_iter),
            'vqe_time_sec': float(vqe_t),
        })
    out = {
        'paper': 'arXiv:2208.10978 (Q2Chemistry)',
        'benchmark': 'H2 potential energy curve, VQE-UCCSD vs FCI',
        'basis': 'sto-3g',
        'encoding': 'Jordan-Wigner',
        'ansatz': 'UCCSD (singlet, anti-hermitian, expm on state vector)',
        'optimizer': 'scipy BFGS',
        'reference': 'FCI via PySCF (same reference method the paper uses)',
        'results': results,
    }
    with open('h2_vqe_results.json', 'w') as f:
        json.dump(out, f, indent=2)
    print('\nWrote h2_vqe_results.json', flush=True)
    # Summary
    max_err = max(r['vqe_minus_fci_mha'] for r in results)
    all_ca = all(r['chemical_accuracy_1p6mHa'] for r in results)
    print(f'\nSummary: max |VQE-FCI| = {max_err:.4f} mHa across {len(results)} geometries. '
          f'All within chemical accuracy? {all_ca}', flush=True)

if __name__ == '__main__':
    main()
