"""
Diagnostic: same DMRG data, but fit both formulas
(open BC: c/6 log(chord),  PBC: c/3 log(chord))
and also use the exact free-fermion entropy as a sanity anchor.
"""
import json, math, numpy as np
import quimb as qu, quimb.tensor as qtn
from scipy.linalg import eigvalsh

def build_tfim_mpo(N, h, J=1.0):
    return qtn.MPO_ham_ising(N, j=-4.0 * J, bx=-2.0 * h, S=0.5, cyclic=False)

def block_entropy(psi_mps, l):
    psi = psi_mps.copy()
    psi.canonize(l)
    return float(psi.entropy(l))

def chord(l, N):
    return (2 * N / math.pi) * math.sin(math.pi * l / N)

# Free-fermion block entropy for TFIM at h=1 open BC (Peschel correlation-matrix method).
def ff_entropy(N, h, l):
    # Build correlation matrix G_ij = <c_i^dag c_j> from BdG eigenvectors.
    # For TFIM h=1 open BC, use Bogoliubov transformation.
    A = np.zeros((N, N))
    B = np.zeros((N, N))
    for i in range(N): A[i,i] = -h
    for i in range(N-1):
        A[i,i+1] = A[i+1,i] = -0.5
        B[i,i+1] = -0.5
        B[i+1,i] = +0.5
    # Solve  (A-B)(A+B) phi = eps^2 phi  --> phi_n eigenvectors
    M = (A - B) @ (A + B)
    w, phi = np.linalg.eigh(M)
    w = np.clip(w, 0.0, None)
    eps = np.sqrt(w)
    # psi_n = (A+B) phi_n / eps_n
    psi = np.zeros_like(phi)
    for n in range(N):
        if eps[n] > 1e-14:
            psi[:,n] = (A + B) @ phi[:,n] / eps[n]
        else:
            psi[:,n] = phi[:,n]
    # Standard entanglement matrices for Ising/free fermions in Majorana basis:
    # Compute correlation matrix C of "a" Majoranas (see Peschel 2003)
    #    G_ij = delta_ij - sum_n [phi_n(i) psi_n(j) + psi_n(i) phi_n(j)]  ...
    # Use majorana correlation approach as in Calabrese Cardy 2005 for TFIM.
    # For our purposes just build the C matrix and use standard formula.
    # (Wilm-Kirchner 2009 lecture notes convention.)
    #
    # Following Latorre-Rico-Vidal (2004) for exactly the TFIM at h=1:
    # define G_ij = <psi_i psi_j> - <phi_i phi_j>  (2Nx2N Majorana matrix),
    # take (2l x 2l) block, compute Schmidt entropy = -sum (nu ln nu + (1-nu) ln (1-nu))
    # for eigenvalues nu of the block correlation matrix.
    Phi = phi   # NxN matrix, cols are phi_n
    Psi = psi   # NxN matrix, cols are psi_n
    G = Psi @ Phi.T - Phi @ Psi.T   # NxN antisym
    # Take upper-left l x l block
    G_block = G[:l, :l]
    # eigvals of i*G_block are +/- pairs of real; take positive halves
    # (correlation of Majorana modes)
    # Better: compute singular values of the block that count independent modes.
    # For antisymmetric NxN block, |eigvals of iG| in (0,1) come in +/- pairs;
    # positive halves give nu_k in (0,1), then S = -sum [ (1+nu)/2 log (1+nu)/2 + (1-nu)/2 log (1-nu)/2 ]
    w_block = np.linalg.eigvalsh(1j * G_block)
    nu = np.abs(w_block)
    nu = nu[nu > 1e-14]
    # unique pair values (avoid double counting)
    nu = np.sort(nu)[::-1]
    # Take upper half (positive)
    N_modes = l  # number of independent Majorana pairs = l for l Majorana pairs... this is 2l Majoranas
    # eigvals come in +/-, so take first l values (largest positive halves)
    nu = nu[:l]
    S = 0.0
    for x in nu:
        p_plus = (1 + x) / 2
        p_minus = (1 - x) / 2
        for p in (p_plus, p_minus):
            if p > 1e-14:
                S -= p * math.log(p)
    return S

def main():
    N = 64
    H = build_tfim_mpo(N, 1.0)
    dmrg = qtn.DMRG2(H, bond_dims=[8,16,32,64], cutoffs=1e-12)
    dmrg.solve(tol=1e-10, verbosity=0)
    psi = dmrg.state

    Ss_dmrg = [block_entropy(psi, l) for l in range(1, N)]
    ls = list(range(1, N))
    chords = [chord(l, N) for l in ls]

    print(f"{'l':>4} {'S_DMRG':>10} {'log_chord':>10}   {'S_FF':>10}")
    Ss_ff = []
    for l, S in zip(ls, Ss_dmrg):
        try:
            Sff = ff_entropy(N, 1.0, l)
        except Exception as e:
            Sff = float('nan')
        Ss_ff.append(Sff)
        if l in (2,4,8,16,24,32,48,60):
            print(f"{l:4d} {S:10.5f} {math.log(chord(l,N)):10.5f}   {Sff:10.5f}")

    # Fit slope of S vs log(chord) in the middle region
    mask = np.array([(l >= 8 and l <= N-8) for l in ls])
    x = np.log(np.array(chords)[mask])
    y = np.array(Ss_dmrg)[mask]
    slope, intercept = np.polyfit(x, y, 1)
    print(f"\nDMRG S vs log(chord) middle-region:  slope = {slope:.5f}  ->  c/6 slope, so c = {6*slope:.4f}   (or c=3*slope*2 = {6*slope:.4f})")
    print(f"For c=1/2 open BC formula (c/6 log chord): expected slope = {0.5/6:.5f}")
    y_ff = np.array(Ss_ff)[mask]
    slope_ff, _ = np.polyfit(x, y_ff, 1)
    print(f"FF (Peschel) middle-region slope = {slope_ff:.5f} -> c_from_FF = {6*slope_ff:.4f}")

    # Save
    out = dict(N=N, ls=ls, S_DMRG=Ss_dmrg, chord=chords, S_FF=Ss_ff,
               slope_DMRG=float(slope), c_DMRG_open=float(6*slope),
               slope_FF=float(slope_ff), c_FF_open=float(6*slope_ff),
               expected_c=0.5)
    with open("../report/evidence/exp2b_ent_diag.json", "w") as f:
        json.dump(out, f, indent=2)
    print("Wrote report/evidence/exp2b_ent_diag.json")

if __name__ == "__main__":
    main()
