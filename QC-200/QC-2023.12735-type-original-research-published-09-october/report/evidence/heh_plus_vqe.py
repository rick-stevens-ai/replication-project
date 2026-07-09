"""Extension replication: HeH+ ground state VQE (also 2-qubit per Meirom&Frankel 2023)."""
import json, os, time
import numpy as np
from scipy.optimize import minimize
from pyscf import gto, scf, fci as pyscf_fci
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import ParityMapper
from qiskit_nature.units import DistanceUnit
from qiskit.circuit.library import EfficientSU2
from qiskit.quantum_info import Statevector


def heh_hamiltonian(d):
    drv = PySCFDriver(atom=f"He 0 0 0; H 0 0 {d}", basis="sto3g",
                       unit=DistanceUnit.ANGSTROM, charge=1, spin=0)
    problem = drv.run()
    h_op = problem.hamiltonian.second_q_op()
    nuc = problem.nuclear_repulsion_energy
    mapper = ParityMapper(num_particles=problem.num_particles)
    qop = mapper.map(h_op)
    mol = gto.M(atom=f"He 0 0 0; H 0 0 {d}", basis="sto-3g", unit="Angstrom", charge=1)
    mf = scf.RHF(mol).run(verbose=0)
    fci_e = pyscf_fci.FCI(mf).kernel()[0]
    return qop, nuc, fci_e


def vqe(qop, seed=42, reps=2):
    n = qop.num_qubits
    ansatz = EfficientSU2(n, reps=reps, entanglement="linear")
    H = qop.to_matrix()
    rng = np.random.default_rng(seed)
    x0 = rng.uniform(-np.pi, np.pi, size=ansatz.num_parameters)
    def c(p):
        bound = ansatz.assign_parameters(p)
        psi = Statevector.from_instruction(bound).data
        return float(np.real(np.conjugate(psi) @ H @ psi))
    t0 = time.time()
    r = minimize(c, x0, method="COBYLA", options={"maxiter": 500, "rhobeg": 0.5})
    return float(r.fun), time.time()-t0


def main():
    ds = [0.6, 0.9, 1.2, 1.5, 2.0]
    res = []
    for d in ds:
        qop, nuc, fci_e = heh_hamiltonian(d)
        e_q, dt = vqe(qop)
        e_tot = e_q + nuc
        err = abs(e_tot - fci_e)
        res.append(dict(d_angstrom=d, fci=float(fci_e), vqe=e_tot,
                        error=err, chem_acc=bool(err<1.6e-3), n_qubits=int(qop.num_qubits),
                        n_terms=len(qop), t_s=dt))
        print(f"HeH+ d={d}A FCI={fci_e:.6f} VQE={e_tot:.6f} err={err:.2e}")
    outdir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(outdir, "heh_plus_vqe_results.json"), "w") as f:
        json.dump(dict(molecule="HeH+ STO-3G", tool="qiskit+pyscf statevector COBYLA",
                       results=res), f, indent=2)
    n_ok = sum(1 for r in res if r["chem_acc"])
    print(f"SUMMARY: {n_ok}/{len(res)} distances chem-accurate")


if __name__ == "__main__":
    main()
