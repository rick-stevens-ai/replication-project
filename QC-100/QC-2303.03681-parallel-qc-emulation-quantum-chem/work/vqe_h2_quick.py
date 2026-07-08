#!/usr/bin/env -S python -u
"""Quick smoke test: one R with timing."""
import time
import numpy as np
from scipy.linalg import eigh, expm
from scipy.optimize import minimize
from openfermion.chem import MolecularData
from openfermionpyscf import run_pyscf
from openfermion.transforms import get_fermion_operator, jordan_wigner
from openfermion.linalg import get_sparse_operator
from openfermion.ops import FermionOperator
from openfermion.utils import hermitian_conjugated

HK = 627.5094740631

t0 = time.time()
R = 0.75
geom = [("H",(0,0,0)),("H",(0,0,R))]
mol = MolecularData(geom, "sto-3g", 1, 0, description=f"H2_R{R}")
mol = run_pyscf(mol, run_scf=True, run_fci=True)
print(f"pyscf done: {time.time()-t0:.2f}s")

ham = get_fermion_operator(mol.get_molecular_hamiltonian())
Hq = jordan_wigner(ham)
Hs = get_sparse_operator(Hq, n_qubits=4)
Hd = Hs.toarray()
E_exact = float(eigh(Hd)[0][0].real)
E_fci = mol.fci_energy
print(f"E_exact={E_exact:.10f} E_fci_pyscf={E_fci:.10f} diff={E_exact-E_fci:.3e}")
print(f"ham built + diag: {time.time()-t0:.2f}s")

# Precompute the two generator matrices independent of params.
def op_sparse(fop):
    return get_sparse_operator(jordan_wigner(fop), n_qubits=4).toarray()

# Singles: alpha 0->2 and beta 1->3, both with same amplitude t_s
Gs = op_sparse(FermionOperator("2^ 0", 1.0) + FermionOperator("3^ 1", 1.0))
Gs = Gs - Gs.conj().T
# Doubles: 0,1 -> 2,3, amplitude t_d
Gd = op_sparse(FermionOperator("3^ 2^ 1 0", 1.0))
Gd = Gd - Gd.conj().T

hf = np.zeros(16, dtype=complex); hf[0b0011] = 1.0

def energy(params):
    ts, td = params
    U = expm(ts*Gs + td*Gd)
    psi = U @ hf
    return float(np.real(np.conj(psi) @ (Hd @ psi)))

t1 = time.time()
res = minimize(energy, [0.05, 0.1], method="BFGS",
               options={"gtol":1e-12,"eps":1e-6,"maxiter":500})
print(f"BFGS: fun={res.fun:.10f} nit={res.nit} nfev={res.nfev} t={time.time()-t1:.2f}s")
print(f"err vs pyscf FCI: {(res.fun-E_fci)*HK:.3e} kcal/mol")
print(f"total: {time.time()-t0:.2f}s")
