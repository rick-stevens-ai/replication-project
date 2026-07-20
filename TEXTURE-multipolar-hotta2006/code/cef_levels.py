"""
Single f-electron (n=1) CEF + spin-orbit diagonalization for Th symmetry.
Hotta 2006 (cond-mat/0611113), eqs (1)-(9).

We build the 14x14 single-electron Hamiltonian in the |m, sigma> basis
(m = -3..3, sigma = +/-1) with:

  H_so  = lambda * sum zeta_{m,s,m',s'} f^dag f          (eq 2,3)
  H_CEF = sum B_{m,m'} f^dag_{m s} f_{m' s}               (eq 7,8)

with the Hutchings/Th CEF matrix B (eq 8) parameterized by (eq 9):
  B40 = W x / F(4),   B60 = W(1-|x|)/F(6),   B62 = W y / Ft(6)
  F(4)=15, F(6)=180, Ft(6)=24;  W=-6e-4 eV.

For a SINGLE electron there is no Coulomb (H_int) contribution, so this is
the exact one-body problem. Diagonalizing gives the CEF/SO split single-
particle levels. For j=5/2 (lower SO manifold) this is exactly the LS->jj
context the paper discusses, and the ground CEF *character* (Gamma5 doublet
vs Gamma67 quartet) can be read off from degeneracies.

Machine-checkable claims addressed here:
  Claim 1: spin-orbit splits the 14 states into j=5/2 sextet (6) below and
           j=7/2 octet (8) above by exactly (7/2)*lambda in the CEF->0 limit
           (standard result E_5/2 = -2*lambda*(3/2)? we test the 6+8 split &
           gap = (7/2)*lambda*<...>). We verify multiplicities 6 & 8 and the
           j=5/2 / j=7/2 energy separation.
  Claim 2: within the j=5/2 sextet, the CEF splits it into a Gamma5 doublet
           and a Gamma67 quartet; which is the ground state flips with the
           SIGN of x (equivalently sign of B40), reproducing the qualitative
           statement in Sec 2.2 / Fig 1(f): for W<0, x>0 (B40<0) the n=1
           single-electron ground level is Gamma67 quartet.
"""
import numpy as np

# --- basis: index = (m+3)*2 + (0 for up[s=+1], 1 for down[s=-1]) ---
MS = [(m, s) for m in range(-3, 4) for s in (+1, -1)]
IDX = {ms: i for i, ms in enumerate(MS)}
N = len(MS)  # 14

def H_so(lam):
    """Spin-orbit, eq (2)-(3). zeta_{m,s,m,s}=m*s/2 ; zeta_{m+s,-s,m,s}=sqrt(12-m(m+s))/2."""
    H = np.zeros((N, N), dtype=complex)
    for (m, s), i in IDX.items():
        # diagonal
        H[i, i] += lam * (m*s/2.0)
        # spin-flip: from (m,s) to (m+s, -s)
        mp = m + s
        if -3 <= mp <= 3 and (mp, -s) in IDX:
            j = IDX[(mp, -s)]
            val = lam * 0.5*np.sqrt(12 - m*(m+s))
            H[j, i] += val
    return H

def B_matrix(W, x, y):
    """Th CEF matrix B_{m,m'} in the m-space (eq 8,9). Returns 7x7 over m=-3..3."""
    F4, F6, Ft6 = 15.0, 180.0, 24.0
    B40 = W * x / F4
    B60 = W * (1 - abs(x)) / F6
    B62 = W * y / Ft6
    B = np.zeros((7, 7))  # index k = m+3
    def setB(m, mp, val):
        B[m+3, mp+3] += val
    # diagonal (eq 8)
    setB(3, 3, 180*B40 + 180*B60);  setB(-3, -3, 180*B40 + 180*B60)
    setB(2, 2, -420*B40 - 1080*B60); setB(-2, -2, -420*B40 - 1080*B60)
    setB(1, 1, 60*B40 + 2700*B60);  setB(-1, -1, 60*B40 + 2700*B60)
    setB(0, 0, 360*B40 - 3600*B60)
    # off-diagonal (eq 8) -- symmetric B_{m,m'}=B_{m',m}
    v = 60*np.sqrt(15)*(B40 - 21*B60)
    setB(3, -1, v); setB(-1, 3, v); setB(-3, 1, v); setB(1, -3, v)
    v = 300*B40 + 7560*B60
    setB(2, -2, v); setB(-2, 2, v)
    v = 24*np.sqrt(15)*B62
    setB(3, 1, v); setB(1, 3, v); setB(-3, -1, v); setB(-1, -3, v)
    v = -48*np.sqrt(15)*B62
    setB(2, 0, v); setB(0, 2, v); setB(-2, 0, v); setB(0, -2, v)
    # B1,-1 = -B3,-3 = 360 B62
    v = 360*B62
    setB(1, -1, v); setB(-1, 1, v)
    return B

def H_cef(W, x, y):
    """Embed 7x7 m-space CEF into 14x14 (spin-diagonal), eq (7)."""
    B = B_matrix(W, x, y)
    H = np.zeros((N, N), dtype=complex)
    for (m, s), i in IDX.items():
        for mp in range(-3, 4):
            if (mp, s) in IDX:
                j = IDX[(mp, s)]
                H[j, i] += B[mp+3, m+3]
    return H

def diag(lam, W, x, y):
    H = H_so(lam) + H_cef(W, x, y)
    H = 0.5*(H + H.conj().T)
    w, v = np.linalg.eigh(H)
    return w, v

def group_levels(w, tol=1e-8):
    """Cluster near-degenerate eigenvalues; return list of (energy, multiplicity)."""
    groups = []
    for e in w:
        placed = False
        for g in groups:
            if abs(e - g[0]) < tol*max(1, abs(e)) + 1e-12:
                g[1] += 1
                placed = True
                break
        if not placed:
            groups.append([e, 1])
    return [(g[0], g[1]) for g in groups]

if __name__ == '__main__':
    lam, W, y = 0.1, -6e-4, 0.3
    print("=== n=1 single f-electron CEF+SO diagonalization (Hotta 2006) ===")
    print(f"lambda={lam}, W={W}, y={y}\n")

    # --- Claim 1: SO splitting into 6 (j=5/2) + 8 (j=7/2) with CEF -> 0 ---
    w0, _ = diag(lam, W=0.0, x=0.0, y=0.0)  # pure SO
    g0 = group_levels(w0, tol=1e-6)
    print("[Claim 1] Pure spin-orbit (CEF off), lambda=0.1:")
    for e, mult in sorted(g0):
        jval = 2.5 if mult == 6 else (3.5 if mult == 8 else None)
        print(f"    E={e:+.6f}  multiplicity={mult}  -> j={jval}")
    mults = sorted([m for _, m in g0])
    E56 = sorted(g0)[0][0]; E78 = sorted(g0)[1][0]
    gap = E78 - E56
    print(f"    j=5/2 -> j=7/2 gap = {gap:.6f} eV   (theory (7/2)*lambda = {3.5*lam:.6f})")
    print(f"    multiplicities = {mults}  (expect [6, 8])")

    # --- Claim 2: within j=5/2, CEF -> Gamma5 doublet + Gamma67 quartet; sign of x flips GS ---
    print("\n[Claim 2] CEF splitting of j=5/2 sextet; ground character vs sign(x):")
    for x in (+0.4, -0.4):
        w, _ = diag(lam, W, x, y)
        # lowest 6 states = j=5/2 manifold
        w6 = np.sort(w)[:6]
        g = group_levels(w6 - w6[0], tol=5e-3)  # relative, meV-scale CEF
        # classify ground multiplicity
        gsort = sorted(g)
        gmult = gsort[0][1]
        gs_label = 'Gamma5 doublet' if gmult == 2 else ('Gamma67 quartet' if gmult == 4 else f'mult={gmult}')
        exc = (gsort[1][0]-gsort[0][0]) if len(gsort) > 1 else 0.0
        print(f"    x={x:+.2f}:  sextet splits into {[(round(e*1e3,3),m) for e,m in gsort]} (meV, mult)")
        print(f"             ground = {gs_label}, CEF excitation = {exc*1e3:.3f} meV")

    # --- Extra: full 14-level structure at x=0.4 for the record ---
    print("\n[Record] full 14-level structure at x=+0.4:")
    w, _ = diag(lam, W, 0.4, y)
    for e, mult in group_levels(w, tol=5e-3):
        print(f"    E={e:+.6f} eV  mult={mult}")
