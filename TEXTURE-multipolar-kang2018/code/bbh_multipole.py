#!/usr/bin/env python3
"""
Minimal replication of Kang, Shiozaki, Cho, PRB 100, 245134 (2019)
"Many-Body Order Parameters for Multipoles in Solids" (arXiv:1812.06999).

We implement the non-interacting BBH quadrupole insulator (Eq. 8 / D5) on a
real-space torus and evaluate the MANY-BODY quadrupole order parameter

    Q_xy = (1/2pi) Im ln <U2> ,  U2 = exp( 2pi i sum_r (x y /(Lx Ly)) n_r )   (Eq. 2)

using the Slater-determinant determinant identity (extraction sec. 5):

    <Psi| exp( i sum_r phi(r) n_r ) |Psi> = det( P^dag . diag(e^{i phi(r)}) . P )

with P the (Nsite*orb x Nocc) matrix of occupied single-particle eigenvectors.
Analogously the dipole (Eq. 1) uses phi(r) = 2pi x / Lx.

This is an analytic/tight-binding + linear-algebra reproduction; NO DFT.

Author: replication subagent (2026-07-19).
"""
import numpy as np

# ----------------------------------------------------------------------------
# Gamma matrices (paper convention, line D5):
#   Gamma0 = tau3 (x) tau0
#   Gamma_i = -tau2 (x) tau_i   (i=1,2,3)
#   Gamma4 = tau1 (x) tau0
# Kronecker order: first factor = "cell/sublattice pair", second = orbital pair.
# ----------------------------------------------------------------------------
t0 = np.eye(2, dtype=complex)
t1 = np.array([[0, 1], [1, 0]], dtype=complex)
t2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
t3 = np.array([[1, 0], [0, -1]], dtype=complex)

G0 = np.kron(t3, t0)
G1 = -np.kron(t2, t1)
G2 = -np.kron(t2, t2)
G3 = -np.kron(t2, t3)
G4 = np.kron(t1, t0)


def h_of_k(kx, ky, gx, gy, lx, ly, delta):
    """Bloch Hamiltonian h(k), Eq. (8)/(D5). 4x4 complex."""
    return ((gx + lx * np.cos(kx)) * G4 + lx * np.sin(kx) * G3
            + (gy + ly * np.cos(ky)) * G2 + ly * np.sin(ky) * G1
            + delta * G0)


# ----------------------------------------------------------------------------
# Real-space occupied-subspace projector via Bloch diagonalization.
# Lattice: Lx x Ly unit cells, 4 orbitals each. Half filling => 2 lowest bands.
# We build occupied single-particle states in the real-space basis by inverse
# Fourier transform of the Bloch eigenvectors.
# ----------------------------------------------------------------------------
def occupied_states_realspace(Lx, Ly, gx, gy, lx, ly, delta, nocc_bands=2):
    """
    Return P : (Lx*Ly*4, Lx*Ly*nocc_bands) matrix of occupied single-particle
    eigenstates in the real-space (cell x, cell y, orbital) basis, and the
    per-orbital coordinates (X, Y) arrays aligned with P's row index.
    Also returns the minimum bulk energy gap encountered.
    """
    norb = 4
    Ncell = Lx * Ly
    Nrows = Ncell * norb
    Nocc = Ncell * nocc_bands
    P = np.zeros((Nrows, Nocc), dtype=complex)

    # momentum grid (periodic BC)
    kxs = 2 * np.pi * np.arange(Lx) / Lx
    kys = 2 * np.pi * np.arange(Ly) / Ly

    # row index helper: (cx, cy, orb) -> flat
    def ridx(cx, cy, orb):
        return (cy * Lx + cx) * norb + orb

    cxs = np.arange(Lx)
    cys = np.arange(Ly)

    col = 0
    gap = np.inf
    for ikx, kx in enumerate(kxs):
        for iky, ky in enumerate(kys):
            h = h_of_k(kx, ky, gx, gy, lx, ly, delta)
            w, v = np.linalg.eigh(h)
            order = np.argsort(w.real)
            w = w[order]
            v = v[:, order]
            # track direct gap between occupied and empty
            g = w[nocc_bands] - w[nocc_bands - 1]
            gap = min(gap, g.real)
            # Bloch plane wave over cells, phase e^{i k . R}
            # column (kx,ky, band b) real-space vector:
            phase = np.exp(1j * (kx * cxs[:, None] + ky * cys[None, :])) / np.sqrt(Ncell)
            # phase[cx, cy]
            for b in range(nocc_bands):
                ub = v[:, b]  # 4-component orbital spinor
                psi = np.zeros(Nrows, dtype=complex)
                for cx in cxs:
                    for cy in cys:
                        ph = phase[cx, cy]
                        base = (cy * Lx + cx) * norb
                        psi[base:base + norb] = ph * ub
                P[:, col] = psi
                col += 1
    # orthonormality is guaranteed (distinct k, orthonormal bands); enforce lightly
    return P, gap


# Intra-cell sublattice offsets for the 4 BBH orbitals (unit cell corners).
# Orbital order follows the tau (x) tau Kronecker index 0..3 = (0,0),(0,1),(1,0),(1,1)
# scaled by the intra-cell offset s in [0, 0.5). s -> 0 recovers the pure-cell
# convention; the many-body Q_xy is independent of s for the quantized phases
# (checked via the offset sweep in run_all.py).
SUBOFF = np.array([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]])


def coords(Lx, Ly, s=0.0):
    """Per-row (orbital-resolved) x,y coordinates. s = intra-cell offset
    fraction (0 => all orbitals at cell center; 0.25 => corners at cx +/- 0.25)."""
    norb = 4
    X = np.zeros(Lx * Ly * norb)
    Y = np.zeros(Lx * Ly * norb)
    for cy in range(Ly):
        for cx in range(Lx):
            base = (cy * Lx + cx) * norb
            for orb in range(norb):
                X[base + orb] = cx + s * SUBOFF[orb, 0]
                Y[base + orb] = cy + s * SUBOFF[orb, 1]
    return X, Y


def orderparam(P, phi):
    """<U> = det( P^dag diag(e^{i phi}) P ). Returns complex <U>."""
    D = np.exp(1j * phi)
    M = P.conj().T @ (D[:, None] * P)
    sign, logdet = np.linalg.slogdet(M)
    return sign * np.exp(logdet)


def _raw_qxy_angle(Lx, Ly, gx, gy, lx, ly, delta, s=0.0):
    P, gap = occupied_states_realspace(Lx, Ly, gx, gy, lx, ly, delta)
    X, Y = coords(Lx, Ly, s=s)
    phi = 2 * np.pi * (X * Y) / (Lx * Ly)
    U = orderparam(P, phi)
    return np.angle(U) / (2 * np.pi), abs(U), gap


def atomic_reference_angle(Lx, Ly, s=0.0):
    """Q_xy angle of the deep atomic-trivial insulator (lambda -> 0), used as the
    origin so that the trivial phase reads 0 and the topological phase reads 1/2,
    matching the paper's convention (Q measured relative to the trivial atomic
    insulator; the paper proves invariance under adding a trivial atomic band)."""
    a, _m, _g = _raw_qxy_angle(Lx, Ly, 1.0, 1.0, 1e-3, 1e-3, 0.0, s=s)
    return a


def _fold_half(x):
    """fold a mod-1 phase into (-0.5, 0.5]."""
    return (x + 0.5) % 1.0 - 0.5


def quadrupole(Lx, Ly, gx, gy, lx, ly, delta, referenced=True, s=0.0):
    """Many-body quadrupole Q_xy (Eq. 2). If referenced, subtract the atomic-
    trivial origin so trivial->0, topological->1/2 (paper convention). Returns
    (Q in (-0.5,0.5], |<U2>|, occupied-empty gap)."""
    a, mag, gap = _raw_qxy_angle(Lx, Ly, gx, gy, lx, ly, delta, s=s)
    if referenced:
        a = a - atomic_reference_angle(Lx, Ly, s=s)
    return _fold_half(a), mag, gap


def dipole(Lx, Ly, gx, gy, lx, ly, delta, axis='x'):
    P, gap = occupied_states_realspace(Lx, Ly, gx, gy, lx, ly, delta)
    X, Y = coords(Lx, Ly)
    if axis == 'x':
        phi = 2 * np.pi * X / Lx
    else:
        phi = 2 * np.pi * Y / Ly
    U = orderparam(P, phi)
    return (np.angle(U) / (2 * np.pi)) % 1.0, abs(U)


if __name__ == "__main__":
    L = 8
    print("Self-test: BBH quadrupole order parameter (referenced), L =", L)
    for (gx, gy, tag) in [(1.5, 1.5, "trivial (g>l)"), (0.5, 0.5, "topological (g<l)")]:
        Q, mag, gap = quadrupole(L, L, gx, gy, 1.0, 1.0, 0.0)
        print(f"  g={gx} l=1 delta=0  {tag:20s}  Q_xy={Q:+.4f}  |U2|={mag:.4f}  gap={gap:.3f}")
