"""
rpa.py — RPA multipole susceptibilities (paper Fig 2 core claim).

We compute the bare f-electron susceptibility bubble chi0 in the 16x16 operator
basis, then form multipole susceptibilities chi_Q(q) = (Q)^dag chi0(q) Q
(bare) and the RPA-dressed version with a diagonal interaction U0Q.

Because the full 16x16 normalized Coulomb tensor U^0 requires Slater-Condon
machinery from Ref [2] (out of scope), we use the REPORTED diagonal U0Q values
(TABLE II) as a diagonal interaction in the multipole basis:
    chi_Q^RPA(q) = chi0_Q(q) / (1 - u * U0Q * chi0_Q(q))
This is the standard channel-diagonal RPA and lets us test the paper's central
qualitative claims:
  (C2) In RPA the magnetic channel Jz is the largest and peaks at q=0 and q=Q=(pi,pi).
  (C3) Quadrupole (Oxy) stays small in RPA (because U0_Oxy < U0_Jz and chi0 structure).

Bare bubble in operator basis (static, omega=0):
  chi0_Q(q) = -(T/N) sum_k sum_{ab} f-block matrix element traced with G's.
We use the standard Lindhard form built from the f-projected Bloch Green function:
  chi0_{Q}(q,0) = (1/N) sum_k Tr[ Q rho(k+q) Q rho(k) ] * lindhard_weight
Practically we compute the generalized (matrix) bare susceptibility via band sums:
  chi0_{Q}(q) = -(1/N) sum_{k,mn} <m,k+q|Q|n,k><n,k|Q|m,k+q>
                * (f(E_{n,k}) - f(E_{m,k+q}))/(E_{n,k} - E_{m,k+q})
restricted to the f-subspace projection of the Bloch eigenvectors.
"""
import numpy as np
from model import H_full, normalized_multipoles, TEMP, MU, MULTIPOLE_NAMES


def fermi(E, mu, T):
    x = np.clip((E - mu) / T, -50, 50)
    return np.where(x > 0, np.exp(-x) / (1 + np.exp(-x)), 1.0 / (1 + np.exp(x)))


# f-subspace indices in the 6x6 basis: 2..5 = (up,1),(up,2),(dn,1),(dn,2)
# Our 4x4 multipole ordering is index=2*sigma+(l-1): (up,1),(up,2),(dn,1),(dn,2)
# which matches indices 2,3,4,5 -> perfect direct embedding.
FIDX = [2, 3, 4, 5]


def embed(Q4):
    """Embed 4x4 f-operator into 6x6 (c-block zero)."""
    Q6 = np.zeros((6, 6), dtype=complex)
    for a in range(4):
        for b in range(4):
            Q6[FIDX[a], FIDX[b]] = Q4[a, b]
    return Q6


def precompute_bands(nk):
    ks = np.linspace(-np.pi, np.pi, nk, endpoint=False)
    Nk = nk * nk
    Es = np.empty((Nk, 6))
    Vs = np.empty((Nk, 6, 6), dtype=complex)
    idx = 0
    kmap = {}
    for i, kx in enumerate(ks):
        for j, ky in enumerate(ks):
            w, V = np.linalg.eigh(H_full(kx, ky))
            Es[idx] = w
            Vs[idx] = V
            kmap[(i, j)] = idx
            idx += 1
    return ks, Es, Vs, kmap


def chi0_Q(Q6, qi, qj, ks, Es, Vs, kmap, mu=MU, T=TEMP, eta=1e-3):
    """Bare static multipole susceptibility for a single operator Q at wavevector q=(qi,qj) mesh index."""
    nk = len(ks)
    Nk = nk * nk
    total = 0.0 + 0j
    fE = fermi(Es, mu, T)
    for i in range(nk):
        ip = (i + qi) % nk
        for j in range(nk):
            jp = (j + qj) % nk
            a = kmap[(i, j)]        # k
            b = kmap[(ip, jp)]      # k+q
            Va = Vs[a]; Vb = Vs[b]
            Ea = Es[a]; Eb = Es[b]
            fa = fE[a]; fb = fE[b]
            # matrix elements M_{mn} = <m,k+q|Q|n,k> = (Vb^dag Q Va)_{mn}
            M = Vb.conj().T @ Q6 @ Va
            # Standard Lindhard (positive-definite static response):
            #   chi0_Q(q) = sum_{mn} |<m,k+q|Q|n,k>|^2 (f(E_{n,k}) - f(E_{m,k+q}))
            #                        / (E_{m,k+q} - E_{n,k})
            # For m=n (or degenerate) the ratio -> -f'(E) >= 0.
            for m in range(6):
                for n in range(6):
                    num = fa[n] - fb[m]
                    den = Eb[m] - Ea[n]
                    if abs(den) < eta:
                        contrib = abs(M[m, n]) ** 2 * (-_dfermi(Ea[n], mu, T))
                    else:
                        contrib = abs(M[m, n]) ** 2 * num / den
                    total += contrib
    return (total / Nk).real


def _dfermi(E, mu, T):
    x = (E - mu) / T
    # df/dE
    ex = np.exp(-abs(x))
    return -(1.0 / T) * ex / (1 + ex) ** 2


# Reported diagonal normalized Coulomb U0Q (TABLE II)
U0Q = {
    "1": -2.4,
    "O20": 0.50, "O22": 0.50,
    "Oxy": 0.63, "Oyz": 0.63, "Ozx": 0.63,
    "Txyz": 0.81,
    "Jz": 1.03, "Jx": 1.03, "Jy": 1.03,
    "Tza": 0.94, "Txa": 0.94, "Tya": 0.94,   # Tz(x,y)^alpha
    "Tzb": 0.94, "Txb": 0.94, "Tyb": 0.94,   # Tz(x,y)^beta
}


def run(nk=32, u=1.08, channels=None, qlist=None):
    ops = normalized_multipoles()
    if channels is None:
        channels = ["Jz", "Oxy", "Txyz", "Jx", "Txa", "O20"]
    ks, Es, Vs, kmap = precompute_bands(nk)
    # q points of interest: Gamma=(0,0), Q=(pi,pi), (pi,0)
    if qlist is None:
        half = nk // 2
        qlist = {"Gamma": (0, 0), "Q=(pi,pi)": (half, half), "(pi,0)": (half, 0)}
    results = {}
    for name in channels:
        Q6 = embed(ops[name][1])
        row = {}
        for qname, (qi, qj) in qlist.items():
            c0 = chi0_Q(Q6, qi, qj, ks, Es, Vs, kmap)
            denom = 1.0 - u * U0Q[name] * c0
            crpa = c0 / denom if denom > 0 else float("inf")
            row[qname] = (c0, crpa)
        results[name] = row
    return results, qlist


if __name__ == "__main__":
    import sys
    nk = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    u = float(sys.argv[2]) if len(sys.argv) > 2 else 1.08
    res, qlist = run(nk=nk, u=u)
    print(f"# RPA multipole susceptibilities, nk={nk}, u={u}")
    print(f"# {'channel':6s} " + "  ".join(f"{q:>12s}(chi0/chiRPA)" for q in qlist))
    for name, row in res.items():
        cells = []
        for q in qlist:
            c0, cr = row[q]
            cells.append(f"{c0:7.3f}/{cr:8.3f}")
        print(f"{name:8s} " + "  ".join(cells))
