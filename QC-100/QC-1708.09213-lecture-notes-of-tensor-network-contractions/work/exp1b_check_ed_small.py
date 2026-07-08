"""
Cross-check: exact diagonalization for small N (N=8,10,12) TFIM open BC,
Pauli convention H = -sum ZZ - h sum X, at h=1.

This nails down conventions before we trust the FF formula.
"""
import numpy as np
from scipy.sparse import kron, identity, csr_matrix
from scipy.sparse.linalg import eigsh
import quimb as qu, quimb.tensor as qtn, math, json

def build_pauli():
    sx = np.array([[0,1],[1,0]], float)
    sy = np.array([[0,-1j],[1j,0]], complex)
    sz = np.array([[1,0],[0,-1]], float)
    return sx, sy, sz

def op_at(N, op, i):
    """Kronecker product op at site i (0-indexed) on N-site chain."""
    I = np.eye(2)
    mats = [I]*N
    mats[i] = op
    out = mats[0]
    for m in mats[1:]:
        out = np.kron(out, m)
    return out

def H_tfim(N, h=1.0):
    sx,_,sz = build_pauli()
    H = np.zeros((2**N, 2**N))
    for i in range(N-1):
        H += -1.0 * op_at(N, sz, i) @ op_at(N, sz, i+1)
    for i in range(N):
        H += -h * op_at(N, sx, i)
    return H

def exact_tfim_open_ff(N, h, J=1.0):
    """
    Correct free-fermion ground-state energy for open TFIM
    H = -J sum sigma^z sigma^z - h sum sigma^x
    Pfeuty/Lieb-Schultz-Mattis convention.

    JW transform (with the standard fermion definition) yields a bilinear
    fermion Hamiltonian; the ground-state energy is
        E_0 = - sum_k Lambda_k
    where Lambda_k are the positive eigenvalues of the BdG matrix.
    """
    # Build the "single-particle" matrix A, B (real).  Pauli convention gives
    # A_{ij} = -h delta_{ij} - (J/... ) etc, but factors depend on the
    # precise JW convention.  Easiest: solve the BdG problem via a Hermitian
    # 2N x 2N matrix, take positive spectrum.
    #
    # Following Lieb-Schultz-Mattis (Ann Phys 1961), one writes
    # H = sum_ij (c_i^dag A_ij c_j + (1/2)(c_i^dag B_ij c_j^dag + h.c.)) + const
    # with A^T = A, B^T = -B.  For H_TFIM (Pauli, open BC, ferro):
    #     A_ii = -h,   A_{i,i+1} = A_{i+1,i} = -J/2,
    #     B_{i,i+1} = -B_{i+1,i} = -J/2.
    # Bogoliubov transformation diagonalizes as
    #     H = sum_k Lambda_k (eta_k^dag eta_k - 1/2) + const
    # with Lambda_k the (positive) singular values of (A + B).
    # But my earlier attempt used the wrong overall factor. Recompute.
    # Actually the *exact* Pfeuty formula for OPEN BC is:
    #     E_0 = - sum_{n=1}^{N} epsilon_n,      epsilon_n = 2|Lambda_n|,
    # where Lambda_n are eigenvalues of the (N x N) matrix
    #     M = (A - B)(A + B) --> take sqrt of eigenvalues.
    A = np.zeros((N, N))
    B = np.zeros((N, N))
    for i in range(N):
        A[i, i] = -h
    for i in range(N - 1):
        A[i, i + 1] = A[i + 1, i] = -J / 2
        B[i, i + 1] = -J / 2
        B[i + 1, i] = +J / 2
    # positive single-particle energies
    Msq = (A - B) @ (A + B)
    # Msq should have non-negative eigenvalues
    w = np.linalg.eigvalsh(Msq)
    w = np.clip(w, 0.0, None)
    eps = np.sqrt(w)             # single-particle energies
    E0 = -np.sum(eps)             # ground state fills all negative-energy modes
    return float(E0)

def main():
    rows = []
    for N in [6, 8, 10, 12]:
        H = H_tfim(N, h=1.0)
        w = np.linalg.eigvalsh(H)
        E_ed = float(w[0])
        E_ff = exact_tfim_open_ff(N, h=1.0)
        # DMRG at bond dim 32 (should be essentially exact for N<=12)
        mpo = qtn.MPO_ham_ising(N, j=-4.0, bx=-2.0, S=0.5, cyclic=False)
        dmrg = qtn.DMRG2(mpo, bond_dims=[8, 16, 32], cutoffs=1e-14)
        dmrg.solve(tol=1e-12, verbosity=0)
        E_dmrg = float(dmrg.energy)
        row = dict(N=N, E_ED=E_ed, E_FF_formula=E_ff, E_DMRG=E_dmrg,
                   diff_ED_DMRG=E_ed - E_dmrg,
                   diff_ED_FF=E_ed - E_ff)
        rows.append(row)
        print(f"N={N:2d}  E_ED={E_ed:.8f}   E_FF={E_ff:.8f}   E_DMRG={E_dmrg:.8f}   "
              f"|ED-DMRG|={abs(E_ed-E_dmrg):.2e}   |ED-FF|={abs(E_ed-E_ff):.2e}")
    print()
    thermo = -4.0/math.pi
    for r in rows:
        r["e_ED_per_site"] = r["E_ED"]/r["N"]
        print(f"N={r['N']:2d}  e_0 = {r['E_ED']/r['N']:.6f}   (thermo limit -4/pi = {thermo:.6f})")
    out = dict(experiment="C1b_ed_ff_check",
               hamiltonian="H = -sum sigma^z sigma^z - h sum sigma^x, open BC, Pauli conv",
               thermo_limit=-4.0/math.pi,
               rows=rows)
    with open("../report/evidence/exp1b_ed_ff_check.json", "w") as f:
        json.dump(out, f, indent=2)
    print("Wrote report/evidence/exp1b_ed_ff_check.json")

if __name__ == "__main__":
    main()
