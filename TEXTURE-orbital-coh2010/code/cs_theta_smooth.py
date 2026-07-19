#!/usr/bin/env python3
"""
theta (Chern-Simons axion angle) by building a SMOOTH GAUGE over the 3D BZ
via successive parallel transport, then integrating the Chern-Simons 3-form
Eq. (22) of Coh et al. (arXiv:1010.6071) directly in that gauge.

This is the honest numerical analogue of the paper's own procedure: the raw
grid gauge is scrambled (Sec. III of the paper), so we first FIX a smooth
gauge, then evaluate

  theta = -(1/4pi) \\int_BZ d^3k  eps_ijk tr[ A_i d_j A_k - (2i/3) A_i A_j A_k ]

Smooth-gauge construction (multiband, occupied subspace of dim nocc):
  1. transport along kx at (ky=kz=0) to fix the kx-edge;
  2. from each kx, transport along ky to fill the (kx,ky) face;
  3. from each (kx,ky), transport along kz to fill the cube.
  This "log-cabin" parallel transport gives a gauge that is smooth in the
  interior; residual non-periodicity at the boundary faces is exactly the
  physical content that makes theta well-defined only mod 2pi.  We then
  compute the connection by finite differences and integrate Eq. (22).

The occupied bands here are Kramers-degenerate, so the NON-Abelian trace is
essential (the Abelian/net-Chern piece cancels between the two partners; the
CS 3-form's cubic term carries the axion content).
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


def hamiltonian(kx, ky, kz, m0, t=1.0, d1=1.0, bz=0.0):
    M = m0 + t * (np.cos(kx) + np.cos(ky) + np.cos(kz))
    return (d1 * np.sin(kx) * G1 + d1 * np.sin(ky) * G2 + d1 * np.sin(kz) * G3
            + M * G0 + bz * GZ)


def occ(H, nocc=2):
    w, v = np.linalg.eigh(H)
    idx = np.argsort(w)[:nocc]
    return v[:, idx]


def _align(u_prev, u_next):
    """Rotate u_next to the smooth gauge closest to u_prev (SVD/Loewdin)."""
    M = u_prev.conj().T @ u_next
    U, _, Vh = np.linalg.svd(M)
    R = Vh.conj().T @ U.conj().T
    return u_next @ R


def build_smooth_gauge(m0, N, t=1.0, d1=1.0, bz=0.0, nocc=2):
    ks = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
    U = np.empty((N, N, N), dtype=object)

    # (1) seed at origin
    U[0, 0, 0] = occ(hamiltonian(ks[0], ks[0], ks[0], m0, t, d1, bz), nocc)
    # (1a) transport along kx at ky=kz=0
    for i in range(1, N):
        u = occ(hamiltonian(ks[i], ks[0], ks[0], m0, t, d1, bz), nocc)
        U[i, 0, 0] = _align(U[i - 1, 0, 0], u)
    # (2) transport along ky for each kx (kz=0)
    for i in range(N):
        for j in range(1, N):
            u = occ(hamiltonian(ks[i], ks[j], ks[0], m0, t, d1, bz), nocc)
            U[i, j, 0] = _align(U[i, j - 1, 0], u)
    # (3) transport along kz for each (kx,ky)
    for i in range(N):
        for j in range(N):
            for l in range(1, N):
                u = occ(hamiltonian(ks[i], ks[j], ks[l], m0, t, d1, bz), nocc)
                U[i, j, l] = _align(U[i, j, l - 1], u)
    return U, ks


def connection(U, i, j, l, mu, N, dk):
    """Non-Abelian Berry connection A_mu = i <u| d_mu u> (Hermitian, nocc x nocc)
    via central-difference in the smooth gauge (periodic index wrap)."""
    u = U[i, j, l]
    if mu == 0:
        up = U[(i + 1) % N, j, l]; um = U[(i - 1) % N, j, l]
    elif mu == 1:
        up = U[i, (j + 1) % N, l]; um = U[i, (j - 1) % N, l]
    else:
        up = U[i, j, (l + 1) % N]; um = U[i, j, (l - 1) % N]
    # smooth-gauge derivative of the frame
    dU = (up - um) / (2 * dk)
    A = 1j * (u.conj().T @ dU)
    return 0.5 * (A + A.conj().T)


def theta_smooth(m0, N=14, t=1.0, d1=1.0, bz=0.0, nocc=2):
    U, ks = build_smooth_gauge(m0, N, t, d1, bz, nocc)
    dk = 2 * np.pi / N

    # Precompute connections A[mu][i,j,l]
    A = [np.empty((N, N, N), dtype=object) for _ in range(3)]
    for i in range(N):
        for j in range(N):
            for l in range(N):
                for mu in range(3):
                    A[mu][i, j, l] = connection(U, i, j, l, mu, N, dk)

    def dA(mu, nu, i, j, l):
        """d_nu A_mu central difference."""
        if nu == 0:
            p = A[mu][(i + 1) % N, j, l]; m = A[mu][(i - 1) % N, j, l]
        elif nu == 1:
            p = A[mu][i, (j + 1) % N, l]; m = A[mu][i, (j - 1) % N, l]
        else:
            p = A[mu][i, j, (l + 1) % N]; m = A[mu][i, j, (l - 1) % N]
        return (p - m) / (2 * dk)

    total = 0.0
    for i in range(N):
        for j in range(N):
            for l in range(N):
                Ax = A[0][i, j, l]; Ay = A[1][i, j, l]; Az = A[2][i, j, l]
                # eps_ijk tr[A_i d_j A_k]  (6 terms)
                lin = (np.trace(Ax @ (dA(2, 1, i, j, l) - dA(1, 2, i, j, l)))
                       + np.trace(Ay @ (dA(0, 2, i, j, l) - dA(2, 0, i, j, l)))
                       + np.trace(Az @ (dA(1, 0, i, j, l) - dA(0, 1, i, j, l))))
                # -(2i/3) eps_ijk tr[A_i A_j A_k] = -(2i/3)*(tr[AxAyAz]-tr[AxAzAy])*... 
                # eps sum over 6 perms -> 2*(tr[AxAyAz]-tr[AxAzAy]) grouping:
                cub = (np.trace(Ax @ Ay @ Az) - np.trace(Ax @ Az @ Ay)
                       + np.trace(Ay @ Az @ Ax) - np.trace(Ay @ Ax @ Az)
                       + np.trace(Az @ Ax @ Ay) - np.trace(Az @ Ay @ Ax))
                integrand = lin - (2j / 3.0) * cub
                total += integrand.real * dk**3

    theta = -total / (4 * np.pi)
    return theta


if __name__ == "__main__":
    import sys
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    print(f"# smooth-gauge CS theta, N={N}")
    print(f"{'m0':>6} {'theta/pi':>10}")
    for m0 in [-4.0, -2.0, 0.0, 2.0, 4.0]:
        th = theta_smooth(m0, N=N)
        print(f"{m0:6.1f} {th/np.pi:10.4f}")
