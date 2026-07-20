"""
filling.py — Claim 1: electron fillings nf and ns.
Paper states (main text): T=0.01, mu=-2.45, Ef=-2.0, tsf=0.78 -> nf=0.58, ns=0.69.

We diagonalize the 6x6 Bloch Hamiltonian on a k-mesh, occupy eigenstates by the
Fermi function at (mu, T), and project occupation onto c- vs f-character.
Filling normalized per (Ce site): ns = per-spin sum over conduction weight,
nf = per f-electron over 2 orbitals x 2 pseudospins.

Convention: we report the total conduction occupation (both spins) as ns and
total f occupation (4 f-states) as nf, matching "s(f)-electron number".
"""
import numpy as np
from model import H_full, TEMP, MU


def fermi(E, mu, T):
    x = (E - mu) / T
    # stable
    out = np.empty_like(x)
    pos = x > 0
    out[pos] = np.exp(-x[pos]) / (1.0 + np.exp(-x[pos]))
    out[~pos] = 1.0 / (1.0 + np.exp(x[~pos]))
    return out


def compute_filling(nk=200, mu=MU, T=TEMP):
    ks = np.linspace(-np.pi, np.pi, nk, endpoint=False)
    nf_tot = 0.0
    ns_tot = 0.0
    count = 0
    # projectors: indices 0,1 = conduction (c_up,c_dn); 2..5 = f
    for kx in ks:
        for ky in ks:
            H = H_full(kx, ky)
            w, V = np.linalg.eigh(H)
            occ = fermi(w, mu, T)
            # weight of each eigenstate on c vs f
            wc = np.sum(np.abs(V[0:2, :]) ** 2, axis=0)  # conduction weight per eigvec
            wf = np.sum(np.abs(V[2:6, :]) ** 2, axis=0)  # f weight per eigvec
            ns_tot += np.sum(occ * wc)
            nf_tot += np.sum(occ * wf)
            count += 1
    ns = ns_tot / count
    nf = nf_tot / count
    return nf, ns


if __name__ == "__main__":
    for nk in (120, 200, 300):
        nf, ns = compute_filling(nk=nk)
        print(f"nk={nk:4d}  nf={nf:.4f}  ns={ns:.4f}  (paper: nf=0.58, ns=0.69)")
