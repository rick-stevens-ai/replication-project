"""
Sanity: exact-diagonalization entanglement entropy of critical TFIM
for N=12, 14. Compare against DMRG output.
"""
import numpy as np, math, json
from scipy.linalg import eigh
from scipy.sparse import kron as spkron, identity as spid, csr_matrix
from scipy.sparse.linalg import eigsh

def build_pauli():
    sx = np.array([[0,1],[1,0]], float)
    sz = np.array([[1,0],[0,-1]], float)
    return sx, sz

def op_at_sparse(N, op, i):
    I = spid(2, format='csr')
    op_s = csr_matrix(op)
    mats = [I]*N; mats[i] = op_s
    out = mats[0]
    for m in mats[1:]:
        out = spkron(out, m, format='csr')
    return out

def H_tfim_sparse(N, h=1.0):
    sx, sz = build_pauli()
    dim = 2**N
    H = csr_matrix((dim, dim))
    for i in range(N-1):
        H = H + (-1.0) * op_at_sparse(N,sz,i) @ op_at_sparse(N,sz,i+1)
    for i in range(N):
        H = H + (-h) * op_at_sparse(N,sx,i)
    return H

def ent_entropy(psi_vec, l, N):
    """Bipartite von-Neumann entropy of the state psi (2^N vector)
       across cut between sites l-1 and l."""
    d_L = 2**l
    d_R = 2**(N - l)
    M = psi_vec.reshape(d_L, d_R)
    s = np.linalg.svd(M, compute_uv=False)
    p = s**2
    p = p[p > 1e-14]
    return float(-np.sum(p * np.log(p)))

def main():
    print("ED entanglement entropies for critical TFIM (h=1) open BC:")
    for N in [10, 12, 14, 16]:
        H = H_tfim_sparse(N, 1.0)
        w, v = eigsh(H, k=1, which='SA')
        psi0 = v[:,0]
        ents = [ent_entropy(psi0, l, N) for l in range(1, N)]
        print(f"N={N}: S(l) =", [f"{s:.4f}" for s in ents])
    # Fit c for N=16
    N = 16
    H = H_tfim_sparse(N, 1.0)
    w, v = eigsh(H, k=1, which='SA')
    psi0 = v[:,0]
    ents = [ent_entropy(psi0, l, N) for l in range(1, N)]
    ls = np.arange(1, N)
    chords = np.array([(2*N/math.pi)*math.sin(math.pi*l/N) for l in ls])
    # middle region
    mask = (ls >= 4) & (ls <= N-4)
    slope, intercept = np.polyfit(np.log(chords[mask]), np.array(ents)[mask], 1)
    print(f"\nN=14 middle-region fit: slope = {slope:.5f} -> c(open,c/6) = {6*slope:.4f}")
    print(f"Expected: c=1/2 -> slope = {0.5/6:.5f}")

    with open("../report/evidence/exp2c_ed_entropy.json", "w") as f:
        json.dump(dict(N=N, ls=ls.tolist(), S=ents, slope=float(slope),
                       c_open=float(6*slope), c_ref=0.5), f, indent=2)

if __name__ == "__main__":
    main()
