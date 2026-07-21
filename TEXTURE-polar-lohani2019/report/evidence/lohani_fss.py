"""
COVERAGE-FLIP extension of the Lohani et al. 2019 replication.

Goal: finite-size scaling (FSS) of the QUANTUM SKYRMION toward the paper's
31-site flake, testing the paper's central abstract claim (lines 17-18):

  "Their bandwidth is exponentially small and arises from tunneling processes
   between skyrmion and antiskyrmion."

On an open finite flake with 6-fold rotation symmetry, skyrmion and antiskyrmion
are exactly degenerate by symmetry (paper Sec I.A: time-reversal x spin-pi
rotation maps sigma=+1 <-> sigma=-1). Their splitting in a finite cluster is the
finite-size tunneling splitting Delta_tun = E1 - E0 within the skyrmion Nf-sector,
which the paper predicts to be EXPONENTIALLY SMALL and to shrink with system size.

We rerun the exact diagonalization (sparse Lanczos, scipy.sparse.linalg.eigsh)
on progressively LARGER round triangular flakes N = 7, 19, 37 (37 ~ the paper's
31-site cluster), and track:
  - C_perp (transverse AFM correlation, skyrmion signature, paper 0.6-0.8)
  - the low-energy tunneling splitting Delta_tun = E1 - E0 vs N
  - the binding energy E0B (skyrmion stability, paper Eq.5)

Perf-bounded: uses eigsh (k low states) + a VECTORIZED C_perp (searchsorted),
so N=37 (dim up to ~2.3M) fits in the time budget.

Independent reimplementation building on work/lohani_ed.py.
"""
import json, time
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh
import lohani_ed as L


def lowk_eig(H, k=6):
    dim = H.shape[0]
    if dim == 1:
        return np.array([H.toarray()[0, 0].real]), np.ones((1, 1))
    k = min(k, dim - 1)
    try:
        vals, vecs = eigsh(H, k=k, which='SA')
        order = np.argsort(vals)
        return vals[order], vecs[:, order]
    except Exception:
        w, v = np.linalg.eigh(H.toarray())
        return w[:k], v[:, :k]


def cperp_max_fast(psi, states, N):
    """Vectorized max transverse AFM correlation C_perp = max_ij -2<Six Sjx+Siy Sjy>.
    <Six Sjx+Siy Sjy> = (1/2)<Si+Sj- + Si-Sj+> (flip-flop, in-sector).
    Uses numpy bit ops + searchsorted over the sorted basis (no python state loop).
    """
    st = np.asarray(states, dtype=np.int64)
    psi = np.asarray(psi).real
    best = 0.0
    for i in range(N):
        bi = (st >> i) & 1
        for j in range(i + 1, N):
            bj = (st >> j) & 1
            mask = bi != bj                      # one up one down -> flip-flop connects
            if not mask.any():
                continue
            src = st[mask]
            new = src ^ (1 << i) ^ (1 << j)
            pos = np.searchsorted(st, new)       # states sorted -> exact lookup
            val = float(np.dot(psi[mask], psi[pos]))  # <Si+Sj- + Si-Sj+> = 2*val
            corr_xy = 0.5 * (2.0 * val)          # = <SixSjx+SiySjy>
            c = -2.0 * corr_xy
            if c > best:
                best = c
    return float(best)


def gs_sector(N, ndown, nn, nnn, tris, J1, J2, K, k=6):
    H, states, index = L.build_H(N, ndown, nn, nnn, tris, J1, J2, K, 0.0)
    vals, vecs = lowk_eig(H, k=k)
    return vals, vecs, states


def fss_point(radius, J1=1.0, J2=0.5, K=0.05, nf_list=None, k=6, verbose=True):
    """Run FSS for one flake size. Returns dict with per-Nf lowest spectra,
    tunneling splitting, C_perp, and binding energies."""
    pts = L.triangular_flake(radius); N = len(pts)
    nn = L.bonds(pts, 1.0); nnn = L.bonds(pts, np.sqrt(3.0))
    tris = L.all_triangles(pts, nn)
    if nf_list is None:
        nf_list = list(range(0, min(N, 7)))

    # references for binding energy (Eq.5)
    v0, _, _ = gs_sector(N, 0, nn, nnn, tris, J1, J2, K, k=1)
    E_fm = float(v0[0])
    v1, _, _ = gs_sector(N, 1, nn, nnn, tris, J1, J2, K, k=1)
    e1 = float(v1[0]) - E_fm

    sectors = []
    for nf in nf_list:
        t = time.time()
        vals, vecs, states = gs_sector(N, nf, nn, nnn, tris, J1, J2, K, k=k)
        E0 = float(vals[0])
        # tunneling splitting = gap to first excited state within the sector
        split = float(vals[1] - vals[0]) if len(vals) > 1 else float('nan')
        eNf = E0 - E_fm
        EB = eNf - nf * e1
        cperp = cperp_max_fast(vecs[:, 0], states, N) if nf >= 2 else 0.0
        low = [float(x) for x in vals[:k]]
        sectors.append(dict(Nf=int(nf), dim=int(len(states)), E0=E0,
                            E_above_FM=float(eNf), binding=float(EB),
                            tunneling_splitting=split, Cperp_max=float(cperp),
                            low_spectrum=low, walltime_s=round(time.time() - t, 2)))
        if verbose:
            print(f"  N={N} Nf={nf:2d} dim={len(states):>8d} E0={E0:9.4f} "
                  f"EB={EB:+8.4f} split={split:.3e} Cperp={cperp:.4f} "
                  f"({time.time()-t:.1f}s)")
    return dict(N=N, radius=radius, J1=J1, J2=J2, K=K, e1_magnon=e1,
                E_fm=E_fm, nn=len(nn), nnn=len(nnn), ntri=len(tris),
                sectors=sectors)


if __name__ == "__main__":
    t0 = time.time()
    print("=== FSS of quantum skyrmion: tunneling splitting vs flake size ===")
    # Choose skyrmion sector per size. Paper: Nf_min ~ 5-9. We probe the
    # low-Nf skyrmion window that fits each flake in the time budget.
    runs = {}
    print("N=7  flake (radius=1):")
    runs['N7'] = fss_point(1, J2=0.5, K=0.05, nf_list=[2, 3, 4], k=6)
    print("N=19 flake (radius=2):")
    runs['N19'] = fss_point(2, J2=0.5, K=0.05, nf_list=[3, 4, 5], k=6)
    print("N=37 flake (radius=3) -- approaches paper's 31-site cluster:")
    # N=37 is heavy; restrict to the skyrmion sector(s) that fit the budget.
    runs['N37'] = fss_point(3, J2=0.5, K=0.05, nf_list=[4, 5], k=4)

    # Assemble the FSS of the tunneling splitting at a fixed skyrmion Nf=4.
    def pick(run, nf):
        for s in run['sectors']:
            if s['Nf'] == nf:
                return s
        return None
    fss_nf4 = []
    for key in ('N7', 'N19', 'N37'):
        s = pick(runs[key], 4)
        if s:
            fss_nf4.append(dict(N=runs[key]['N'], Nf=4,
                                tunneling_splitting=s['tunneling_splitting'],
                                Cperp_max=s['Cperp_max'], binding=s['binding']))

    out = dict(
        description=("Finite-size scaling of the quantum skyrmion toward the "
                     "paper's 31-site flake. Tracks tunneling splitting "
                     "Delta_tun = E1-E0 (skyrmion<->antiskyrmion), C_perp, and "
                     "binding energy vs N in {7,19,37}."),
        runs=runs,
        fss_tunneling_splitting_Nf4=fss_nf4,
        runtime_s=round(time.time() - t0, 1),
    )
    with open("lohani_fss_result.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nFSS tunneling splitting (Nf=4):")
    for r in fss_nf4:
        print(f"  N={r['N']:2d}  Delta_tun={r['tunneling_splitting']:.3e}  "
              f"Cperp={r['Cperp_max']:.4f}  EB={r['binding']:+.4f}")
    print("saved lohani_fss_result.json  (%.1fs)" % out['runtime_s'])
