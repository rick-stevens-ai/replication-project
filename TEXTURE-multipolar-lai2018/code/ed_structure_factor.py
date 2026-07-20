"""
Tractable exact-diagonalization (ED) surrogate for the paper's DMRG Fig. 1 claim:
the spin-1 bilinear-biquadratic model on the square lattice, with J1=1, K1=1.2,
J2=0, K2<0, develops a (pi,pi) ANTIFERROQUADRUPOLAR structure-factor peak while
the spin (dipole) structure factor stays weak.

The paper used DMRG on Ly=8 cylinders up to 4000 SU(2) states. That is out of
scope for a laptop. Instead we do a *small-cluster* ED on a 2x2 periodic square
(4 sites, spin-1 -> 3^4 = 81 states) and a 2x4 (8 sites, 3^8 = 6561 states) cluster,
which is the largest exactly-diagonalizable size here, and measure:

    m^2_Q(q) = (1/Ns^2) sum_{ij} <Qi.Qj> e^{i q.(ri-rj)}
    m^2_S(q) = (1/Ns^2) sum_{ij} <Si.Sj> e^{i q.(ri-rj)}

We check the QUALITATIVE, machine-checkable claim: at K2<0 the DOMINANT quadrupolar
structure-factor peak is at q=(pi,pi), and it exceeds the dipole peak. Small clusters
cannot reproduce thermodynamic-limit order parameters, so this is reported as a
finite-size consistency test, NOT a quantitative match to DMRG magnitudes.
"""

import json, os, sys, itertools
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh

sys.path.insert(0, os.path.dirname(__file__))
from model import Sx, Sy, Sz, quad_ops

Qlist = [sp.csr_matrix(Q) for Q in quad_ops()]
Sxs, Sys, Szs = sp.csr_matrix(Sx), sp.csr_matrix(Sy), sp.csr_matrix(Sz)
Sops_sp = [Sxs, Sys, Szs]
d = 3  # spin-1 local dimension
I3s = sp.identity(d, dtype=complex, format='csr')

_cache = {}

def site_op(op, site, N):
    """Embed 3x3 sparse op at `site` into N-site product space (sparse)."""
    out = None
    for k in range(N):
        m = op if k == site else I3s
        out = m if out is None else sp.kron(out, m, format='csr')
    return out


def two_site_scalar(oplistA, oplistB, i, j, N):
    """sum_a A_a(i) B_a(j) for a list of matching operators (dot product), sparse."""
    out = None
    for A, B in zip(oplistA, oplistB):
        term = site_op(A, i, N) @ site_op(B, j, N)
        out = term if out is None else out + term
    return out.tocsr()


def build_lattice(Lx, Ly):
    coords = [(x, y) for x in range(Lx) for y in range(Ly)]
    idx = {c: k for k, c in enumerate(coords)}
    N = Lx * Ly

    def nbrs(x, y):
        # nearest neighbors (periodic)
        return [((x + 1) % Lx, y), (x, (y + 1) % Ly)]

    def nbrs2(x, y):
        # second neighbors (diagonals, periodic)
        return [((x + 1) % Lx, (y + 1) % Ly), ((x + 1) % Lx, (y - 1) % Ly)]

    nn_bonds = []
    for (x, y) in coords:
        for (nx, ny) in nbrs(x, y):
            nn_bonds.append((idx[(x, y)], idx[(nx, ny)]))
    nnn_bonds = []
    for (x, y) in coords:
        for (nx, ny) in nbrs2(x, y):
            nnn_bonds.append((idx[(x, y)], idx[(nx, ny)]))
    return coords, idx, N, nn_bonds, nnn_bonds


def build_H(Lx, Ly, J1, K1, J2, K2):
    coords, idx, N, nn_bonds, nnn_bonds = build_lattice(Lx, Ly)
    dim = d ** N
    H = sp.csr_matrix((dim, dim), dtype=complex)
    for (i, j) in nn_bonds:
        SS = two_site_scalar(Sops_sp, Sops_sp, i, j, N)
        H = H + J1 * SS + K1 * (SS @ SS)
    for (i, j) in nnn_bonds:
        SS = two_site_scalar(Sops_sp, Sops_sp, i, j, N)
        H = H + J2 * SS + K2 * (SS @ SS)
    return H.tocsr(), coords, N


def ground_state(H):
    dim = H.shape[0]
    if dim <= 256:
        w, v = np.linalg.eigh(H.toarray())
        return w[0], v[:, 0]
    w, v = eigsh(H, k=1, which='SA')
    return w[0], v[:, 0]


def _expect(psi, Op):
    return np.vdot(psi, Op @ psi)


def structure_factors(psi, coords, N, q, corr_cache):
    mS = 0.0 + 0j
    mQ = 0.0 + 0j
    for i in range(N):
        for j in range(N):
            ri = np.array(coords[i]); rj = np.array(coords[j])
            phase = np.exp(1j * (q[0] * (ri[0] - rj[0]) + q[1] * (ri[1] - rj[1])))
            sij, qij = corr_cache[(i, j)]
            mS += sij * phase
            mQ += qij * phase
    return (mS / N ** 2).real, (mQ / N ** 2).real


def run(Lx, Ly, J1, K1, J2, K2):
    H, coords, N = build_H(Lx, Ly, J1, K1, J2, K2)
    e0, psi = ground_state(H)
    # precompute <Si.Sj> and <Qi.Qj> for all pairs ONCE
    corr_cache = {}
    for i in range(N):
        for j in range(N):
            SS = two_site_scalar(Sops_sp, Sops_sp, i, j, N)
            QQ = two_site_scalar(Qlist, Qlist, i, j, N)
            corr_cache[(i, j)] = (_expect(psi, SS), _expect(psi, QQ))
    qs = {
        "(0,0)": (0.0, 0.0),
        "(pi,0)": (np.pi, 0.0),
        "(0,pi)": (0.0, np.pi),
        "(pi,pi)": (np.pi, np.pi),
    }
    sf = {}
    for name, q in qs.items():
        mS, mQ = structure_factors(psi, coords, N, q, corr_cache)
        sf[name] = {"mS2": mS, "mQ2": mQ}
    e0 = float(np.real(e0))
    return e0, N, sf


def main():
    configs = [
        ("2x2", 2, 2),
        ("2x4", 2, 4),
    ]
    J1, K1, J2 = 1.0, 1.2, 0.0
    K2 = -0.3   # the paper's illustrative point K2/J1 = -0.3
    out = {"params": {"J1": J1, "K1": K1, "J2": J2, "K2": K2}, "clusters": {}}
    print(f"BLBQ ED  J1={J1} K1={K1} J2={J2} K2={K2}")
    for tag, Lx, Ly in configs:
        e0, N, sf = run(Lx, Ly, J1, K1, J2, K2)
        # find dominant quad peak
        qpeak = max(sf.items(), key=lambda kv: kv[1]["mQ2"])[0]
        speak = max(sf.items(), key=lambda kv: kv[1]["mS2"])[0]
        print(f"\ncluster {tag} (N={N}), E0={e0:.6f}")
        for name, v in sf.items():
            print(f"   q={name:8s}  mQ^2={v['mQ2']:+.5f}   mS^2={v['mS2']:+.5f}")
        print(f"   -> dominant quad peak at {qpeak}; dominant spin peak at {speak}")
        out["clusters"][tag] = {"N": N, "E0": e0, "sf": sf,
                                "quad_peak": qpeak, "spin_peak": speak}

    # Machine-checkable assertion: on the largest cluster the dominant quadrupolar
    # peak is at (pi,pi) AND mQ^2(pi,pi) > mS^2(pi,pi).
    big = out["clusters"]["2x4"]
    peak_ok = big["quad_peak"] == "(pi,pi)"
    dom_ok = big["sf"]["(pi,pi)"]["mQ2"] > big["sf"]["(pi,pi)"]["mS2"]
    out["checks"] = {
        "quad_peak_at_pipi": bool(peak_ok),
        "quad_dominates_spin_at_pipi": bool(dom_ok),
        "pass": bool(peak_ok and dom_ok),
    }
    print("\n[CHECK] dominant quad peak at (pi,pi):", peak_ok)
    print("[CHECK] mQ^2(pi,pi) > mS^2(pi,pi):", dom_ok)
    print("[RESULT]", "PASS" if out["checks"]["pass"] else "PARTIAL/FAIL")

    outdir = os.path.join(os.path.dirname(__file__), "..", "work")
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "ed_structure_factor.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("Wrote work/ed_structure_factor.json")


if __name__ == "__main__":
    main()
