#!/usr/bin/env python3
"""
Robust Z2 / axion theta via the Soluyanov-Vanderbilt largest-gap
partner-switching method (PRB 83, 235401 (2011)), the algorithm used by
Z2Pack.  This is the numerically stable route to the Chern-Simons axion
angle theta studied in Coh et al. (arXiv:1010.6071):

    nu = 1  ->  theta = pi (mod 2pi)   [strong TI]
    nu = 0  ->  theta = 0  (mod 2pi)   [trivial]

Algorithm (exact SV prescription):
  * Compute WCC bar-x_n(ky) = kx-Wilson-loop eigenphases at each ky in [0,pi].
  * At each ky, locate the largest gap between adjacent WCC on the circle;
    let z(ky) be its midpoint.
  * Between consecutive ky, count how many WCC lie inside the (directed)
    interval swept by z; the Z2 invariant is the parity of the total count
    of WCC that cross the moving gap midpoint.
  * Equivalent robust scalar: g = number of times the largest-gap midpoint
    line is crossed by a WCC line as ky: 0 -> pi.  nu = g mod 2.

We verify against the exact Fu-Kane parity oracle.
"""

import numpy as np
from itertools import product

s0 = np.eye(2, dtype=complex)
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)
kron = np.kron
G0 = kron(sz, s0); G1 = kron(sx, sx); G2 = kron(sx, sy); G3 = kron(sx, sz)
GZ = kron(s0, sz)
PARITY = kron(sz, s0)


def hamiltonian(kx, ky, kz, m0, t=1.0, d1=1.0, bz=0.0):
    M = m0 + t * (np.cos(kx) + np.cos(ky) + np.cos(kz))
    return (d1 * np.sin(kx) * G1 + d1 * np.sin(ky) * G2 + d1 * np.sin(kz) * G3
            + M * G0 + bz * GZ)


def occ(H, nocc=2):
    w, v = np.linalg.eigh(H)
    return v[:, np.argsort(w)[:nocc]]


def theta_parity(m0, t=1.0, d1=1.0, nocc=2):
    prod = 1.0
    for kx, ky, kz in product([0.0, np.pi], repeat=3):
        w, v = np.linalg.eigh(hamiltonian(kx, ky, kz, m0, t, d1, 0.0))
        u = v[:, np.argsort(w)[:nocc]]
        pe = np.sort(np.linalg.eigvals(u.conj().T @ PARITY @ u).real)
        prod *= np.sign(pe[0])
    return np.pi if prod < 0 else 0.0


def wcc_line(ky, kz, Nx, m0, t, d1, bz, nocc=2):
    ksx = np.linspace(0, 2 * np.pi, Nx, endpoint=False)
    frames = [occ(hamiltonian(kx, ky, kz, m0, t, d1, bz), nocc) for kx in ksx]
    W = np.eye(nocc, dtype=complex)
    for l in range(Nx):
        M = frames[l].conj().T @ frames[(l + 1) % Nx]
        # Loewdin-orthonormalize overlap to keep W unitary (stable)
        Uu, _, Vh = np.linalg.svd(M)
        W = (Uu @ Vh) @ W
    ev = np.linalg.eigvals(W)
    return np.sort((np.angle(ev) / (2 * np.pi)) % 1.0)


def largest_gap_mid(wcc):
    ws = np.sort(wcc % 1.0)
    wext = np.concatenate([ws, [ws[0] + 1.0]])
    gaps = np.diff(wext)
    g = int(np.argmax(gaps))
    return ((wext[g] + wext[g + 1]) / 2.0) % 1.0


def z2_invariant(m0, Nky=101, Nx=60, kz=0.0, t=1.0, d1=1.0, bz=0.0, nocc=2):
    """Partner-switching Z2 for a 2-WCC (nocc=2) system by continuously
    tracking the WCC across ky in [0, pi] and counting crossings of the
    largest-gap reference line at ky=0.

    Robust prescription for nocc=2 (Kramers pair): the two WCC swap partners
    iff, tracking them continuously (nearest-neighbour on the circle) from
    ky=0 to ky=pi, they interchange positions relative to the ky=0 largest-
    gap midpoint.  Equivalently: unwrap each WCC branch continuously and check
    whether the pair (x1,x2) at ky=pi is the T-image swap of ky=0.  We count
    the parity of crossings of the reference line by the continuously tracked
    lower branch.
    """
    kys = np.linspace(0, np.pi, Nky)
    wccs = [wcc_line(ky, kz, Nx, m0, t, d1, bz, nocc) for ky in kys]

    # continuously track the WCC branches by nearest-neighbour matching on the
    # circle (mod 1), unwrapping so branches are smooth real functions of ky.
    branches = np.zeros((Nky, nocc))
    branches[0] = np.sort(wccs[0] % 1.0)
    for a in range(1, Nky):
        prev = branches[a - 1] % 1.0
        cur = wccs[a] % 1.0
        # greedy nearest-neighbour assignment on the circle
        used = [False] * nocc
        assigned = np.zeros(nocc)
        for n in range(nocc):
            best, bd = -1, 1e9
            for mm in range(nocc):
                if used[mm]:
                    continue
                d = abs(((cur[mm] - prev[n] + 0.5) % 1.0) - 0.5)  # circular dist
                if d < bd:
                    bd, best = d, mm
            used[best] = True
            # unwrap relative to previous branch value
            raw = cur[best]
            delta = ((raw - branches[a - 1][n] + 0.5) % 1.0) - 0.5
            assigned[n] = branches[a - 1][n] + delta
        branches[a] = assigned

    # SV moving-gap: z(ky) = largest-gap midpoint at each ky (continuous).
    # Count how many times a continuously-tracked WCC branch crosses the
    # moving midpoint line z(ky) as ky: 0 -> pi.  nu = parity of that count.
    import math
    z = np.array([largest_gap_mid(wccs[a]) for a in range(Nky)])
    # unwrap z into a continuous curve consistent with the branch unwrap frame
    z_un = np.zeros(Nky)
    z_un[0] = z[0]
    for a in range(1, Nky):
        delta = ((z[a] - z_un[a - 1] + 0.5) % 1.0) - 0.5
        z_un[a] = z_un[a - 1] + delta

    crossings = 0
    for n in range(nocc):
        b = branches[:, n]
        diff = b - z_un                      # branch minus moving gap line
        for a in range(Nky - 1):
            # crossing if diff changes sign by an integer boundary (mod 1),
            # i.e. (b-z) passes through an integer
            lo, hi = diff[a], diff[a + 1]
            if lo == hi:
                continue
            k0 = math.ceil(min(lo, hi))
            k1 = math.floor(max(lo, hi))
            # count integers strictly inside (open interval to avoid endpoints)
            for kk in range(k0, k1 + 1):
                if min(lo, hi) < kk < max(lo, hi):
                    crossings += 1
    nu = crossings % 2
    return nu


if __name__ == "__main__":
    import sys
    Nky = int(sys.argv[1]) if len(sys.argv) > 1 else 101
    Nx = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    print(f"# Robust Z2 (SV largest-gap), Nky={Nky}, Nx={Nx}")
    print(f"{'m0':>6} {'parity/pi':>10} {'nu':>4} {'theta/pi':>9} {'match':>6}")
    ok = True
    for m0 in [-4.5, -3.5, -2.5, -2.0, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5, 4.5]:
        tp = theta_parity(m0)
        nu = z2_invariant(m0, Nky=Nky, Nx=Nx)
        th = 'pi' if nu == 1 else '0'
        match = (nu == 1) == (tp > 0.5)
        ok = ok and match
        print(f"{m0:6.1f} {tp/np.pi:10.0f} {nu:4d} {th:>9} {str(match):>6}")
    print("ALL MATCH PARITY ORACLE:", ok)
