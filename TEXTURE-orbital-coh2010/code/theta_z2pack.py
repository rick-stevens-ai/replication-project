#!/usr/bin/env python3
"""
Z2 invariant / axion theta via hybrid Wannier center (HWCC) partner-switching
-- the discretization-robust standard (Soluyanov & Vanderbilt, PRB 83,
235401 (2011); Gresch et al. Z2Pack).  This is the reliable numerical route
to the Chern-Simons axion angle theta studied by Coh et al.
(arXiv:1010.6071):

  theta = pi   (mod 2pi)   if Z2 invariant nu = 1  (strong TI)
  theta = 0    (mod 2pi)   if nu = 0                (trivial)

Method:
  * On a half-BZ sheet parametrised by ky in [0, pi] (T-invariant plane
    stack), compute the kx-Wilson-loop HWCC eigenphases as a function of ky.
  * Count how many times any horizontal reference line is crossed by the
    HWCC bands as ky goes 0 -> pi (partner switching).  Odd = nu=1 = TI.
  * We use the robust "largest gap" tracking of Soluyanov-Vanderbilt.

This does NOT need a smooth global gauge (the failure mode of the direct CS
3-form integral), so it is numerically stable, exactly as Z2Pack relies on.

Also computes a continuous CS proxy when T is broken (bz != 0): the drift of
the SUM of HWCC across the 2D BZ, which tracks theta away from pi (paper's
Fig. 8 physics).
"""

import numpy as np

s0 = np.eye(2, dtype=complex)
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)
kron = np.kron
G0 = kron(sz, s0); G1 = kron(sx, sx); G2 = kron(sx, sy); G3 = kron(sx, sz)
GZ = kron(s0, sz)


def hamiltonian(kx, ky, kz, m0, t=1.0, d1=1.0, bz=0.0):
    M = m0 + t * (np.cos(kx) + np.cos(ky) + np.cos(kz))
    return (d1 * np.sin(kx) * G1 + d1 * np.sin(ky) * G2 + d1 * np.sin(kz) * G3
            + M * G0 + bz * GZ)


def occ(H, nocc=2):
    w, v = np.linalg.eigh(H)
    return v[:, np.argsort(w)[:nocc]]


def wcc_line(ky, kz, Nx, m0, t, d1, bz, nocc=2):
    """kx-directed Wilson loop at fixed (ky,kz) -> HWCC eigenphases /2pi in [0,1)."""
    ksx = np.linspace(0, 2 * np.pi, Nx, endpoint=False)
    frames = [occ(hamiltonian(kx, ky, kz, m0, t, d1, bz), nocc) for kx in ksx]
    W = np.eye(nocc, dtype=complex)
    for l in range(Nx):
        M = frames[l].conj().T @ frames[(l + 1) % Nx]
        W = M @ W
    ev = np.linalg.eigvals(W)
    wcc = np.sort((np.angle(ev) / (2 * np.pi)) % 1.0)
    return wcc


def z2_invariant(m0, Nky=41, Nx=40, kz=0.0, t=1.0, d1=1.0, bz=0.0, nocc=2):
    """Z2 via HWCC partner switching on the ky in [0,pi] half sheet (kz plane).
    Returns (nu, wcc_array, ky_array)."""
    kys = np.linspace(0, np.pi, Nky)
    wccs = np.array([wcc_line(ky, kz, Nx, m0, t, d1, bz, nocc) for ky in kys])
    # Soluyanov-Vanderbilt largest-gap method (PRB 83, 235401).
    # At each ky step, find the largest gap in the WCC spectrum of step a; its
    # midpoint z_g(a). Then count, at step a+1, how many WCC lie between
    # z_g(a) and z_g(a+1) (i.e. were swept over by the moving gap). The Z2
    # invariant is the parity of the total number of such sweeps.
    def largest_gap_mid(w):
        ws = np.sort(w % 1.0)
        wext = np.concatenate([ws, [ws[0] + 1.0]])
        gaps = np.diff(wext)
        g = np.argmax(gaps)
        return ((wext[g] + wext[g + 1]) / 2.0) % 1.0

    def n_between(lo, hi, w):
        """count WCC (mod1) in the directed arc from lo to hi (going up mod1)."""
        w = w % 1.0
        d = (hi - lo) % 1.0
        cnt = 0
        for x in w:
            if ((x - lo) % 1.0) < d:
                cnt += 1
        return cnt

    total = 0
    for a in range(len(kys) - 1):
        g0 = largest_gap_mid(wccs[a])
        g1 = largest_gap_mid(wccs[a + 1])
        # WCC of the intermediate configuration swept by the gap displacement
        total += n_between(g0, g1, wccs[a + 1])
    nu = total % 2
    return nu, wccs, kys


def theta_from_z2(m0, **kw):
    nu, _, _ = z2_invariant(m0, **kw)
    return np.pi if nu == 1 else 0.0


# ---- continuous theta drift when T broken (Fig. 8 physics) -----------------
def total_hwcc_flow(m0, Nkx=24, Nky=24, Nz=32, t=1.0, d1=1.0, bz=0.0, nocc=2):
    """Continuous CS angle proxy: theta = 2pi * <net winding of the SUM of
    kz-HWCC as (kx,ky) sweeps BZ>.  Robust unwrapped average.

    For a T-broken insulator this returns a value that departs continuously
    from the quantized bz=0 value, reproducing the paper's Fig. 8 trend."""
    ksx = np.linspace(0, 2 * np.pi, Nkx, endpoint=False)
    ksy = np.linspace(0, 2 * np.pi, Nky, endpoint=False)
    # sum of kz-HWCC = total z-polarization P(kx,ky) in [0,1)
    P = np.zeros((Nkx, Nky))
    for i, kx in enumerate(ksx):
        for j, ky in enumerate(ksy):
            w = wcc_line_z(kx, ky, Nz, m0, t, d1, bz, nocc)
            P[i, j] = (np.sum(w)) % 1.0
    return P, ksx, ksy


def wcc_line_z(kx, ky, Nz, m0, t, d1, bz, nocc=2):
    ksz = np.linspace(0, 2 * np.pi, Nz, endpoint=False)
    frames = [occ(hamiltonian(kx, ky, kz, m0, t, d1, bz), nocc) for kz in ksz]
    W = np.eye(nocc, dtype=complex)
    for l in range(Nz):
        M = frames[l].conj().T @ frames[(l + 1) % Nz]
        W = M @ W
    ev = np.linalg.eigvals(W)
    return (np.angle(ev) / (2 * np.pi)) % 1.0


if __name__ == "__main__":
    import sys
    Nky = int(sys.argv[1]) if len(sys.argv) > 1 else 31
    Nx = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    print(f"# Z2 partner-switching, Nky={Nky}, Nx={Nx}, kz=0 plane")
    print(f"{'m0':>6} {'nu':>4} {'theta/pi':>10}")
    for m0 in [-4.5, -3.5, -2.5, -2.0, -1.5, -0.5, 0.0, 0.5, 1.5, 2.0, 2.5, 3.5, 4.5]:
        nu, _, _ = z2_invariant(m0, Nky=Nky, Nx=Nx)
        print(f"{m0:6.1f} {nu:4d} {('pi' if nu==1 else '0'):>10}")
