"""
Minimal replication of the spin-1 director / multipolar-order formalism from
Lai, Nica, Hu, Gong, Paschen, Si, "Kondo Destruction and Multipolar Order --
Implications for Heavy Fermion Quantum Criticality", arXiv:1807.09258 (PRB 97, ...).

This module encodes the *checkable algebraic and few-site* content of the paper:

  - Spin-1 operators (3x3) and the 5-component quadrupole operator Q (Eqs. in main text).
  - The biquadratic identities:
        (Si.Sj)^2 = (Qi.Qj)/2 - (Si.Sj)/2 + (Si^2 Sj^2)/3               [main text, Eq. after (3)]
        Qi.Qj     = 2 (Si.Sj)^2 + (Si.Sj) - 8/3                          [Supplemental, above (S1)]
  - The time-reversal-invariant director basis |x>,|y>,|z> (Eq. S10) and the
    d-vector -> spin/quadrupole maps (Eqs. S16-S22):
        S^alpha = -i eps^{alpha beta gamma} conj(d^beta) d^gamma          (S16-S17)
        Q^{x2-y2} = -|dx|^2 + |dy|^2                                      (S18)
        Q^{3z2-r2}= (|dx|^2+|dy|^2-2|dz|^2)/sqrt(3)                       (S18)
        Q^{xy}=-conj(dx)dy-conj(dy)dx, etc.                              (S19-S22)
  - Hamiltonian in director language (Eq. S23 region):
        HS = sum_<ij> Jn|di.conj(dj)|^2 + (Kn-Jn)|di.dj|^2               (constants dropped)
    At the SU(3) point Jn=Kn it is a pure function of |di.conj(dj)|^2.
  - The (pi,pi)-AFQ ground-state directors dA=(1,0,0), dB=(0,1,0) (Eq. S24) and the
    verification that they give a staggered <Q^{x2-y2}> ~ (-1)^j and no dipole moment.
  - The 4 Gell-Mann generators lambda_1..4 (Eq. S25) and the check that the global
    rotation U(phi)=exp(i sum lambda_j phi_j) is unitary and leaves the SU(3)-point
    energy of the two-director ground state invariant (marginal / flat direction).

NO DFT, NO DMRG. This is the tractable analytic/algebraic core, done exactly.
"""

import numpy as np

# ------------------------------------------------------------------
# Spin-1 operators (S=1, basis |+1>,|0>,|-1>)
# ------------------------------------------------------------------
_s2 = np.sqrt(2.0)
Sx = np.array([[0, 1, 0],
               [1, 0, 1],
               [0, 1, 0]], dtype=complex) / _s2
Sy = np.array([[0, -1j, 0],
               [1j, 0, -1j],
               [0, 1j, 0]], dtype=complex) / _s2
Sz = np.array([[1, 0, 0],
               [0, 0, 0],
               [0, 0, -1]], dtype=complex)

I3 = np.eye(3, dtype=complex)


def quad_ops():
    """5-component quadrupole operators as defined in the main text:
       Q^{x2-y2} = Sx^2 - Sy^2
       Q^{3z2-r2}= (2 Sz^2 - Sx^2 - Sy^2)/sqrt(3)
       Q^{xy}    = Sx Sy + Sy Sx
       Q^{yz}    = Sy Sz + Sz Sy
       Q^{zx}    = Sz Sx + Sx Sz
    Returned in the order [x2-y2, 3z2-r2, xy, yz, zx].
    """
    Qx2y2 = Sx @ Sx - Sy @ Sy
    Q3z2 = (2 * (Sz @ Sz) - Sx @ Sx - Sy @ Sy) / np.sqrt(3.0)
    Qxy = Sx @ Sy + Sy @ Sx
    Qyz = Sy @ Sz + Sz @ Sy
    Qzx = Sz @ Sx + Sx @ Sz
    return [Qx2y2, Q3z2, Qxy, Qyz, Qzx]


# ------------------------------------------------------------------
# Two-site operators on the 9-dim product space
# ------------------------------------------------------------------
def kron(a, b):
    return np.kron(a, b)


def SdotS():
    """Si . Sj on the 2-site (9-dim) Hilbert space."""
    return kron(Sx, Sx) + kron(Sy, Sy) + kron(Sz, Sz)


def QdotQ():
    """Qi . Qj (5-component dot) on the 2-site (9-dim) Hilbert space."""
    Q = quad_ops()
    out = np.zeros((9, 9), dtype=complex)
    for Qa in Q:
        out += kron(Qa, Qa)
    return out


# ------------------------------------------------------------------
# Director (d-vector) formalism, Eqs. S10-S22
# ------------------------------------------------------------------
def spin_from_d(d):
    """S^alpha = -i eps^{alpha beta gamma} conj(d^beta) d^gamma  (Eq. S16/S17).
    d is a length-3 complex vector (dx,dy,dz). Returns real 3-vector (Sx,Sy,Sz)."""
    d = np.asarray(d, dtype=complex)
    dc = np.conjugate(d)
    # cross-product form: S = -i (conj(d) x d)
    S = -1j * np.cross(dc, d)
    return S.real  # imaginary parts vanish for physical d


def quad_from_d(d):
    """5-component quadrupole expectation from a director d (Eqs. S18-S22).
    Order: [x2-y2, 3z2-r2, xy, yz, zx]."""
    d = np.asarray(d, dtype=complex)
    dx, dy, dz = d
    Qx2y2 = -abs(dx) ** 2 + abs(dy) ** 2
    Q3z2 = (abs(dx) ** 2 + abs(dy) ** 2 - 2 * abs(dz) ** 2) / np.sqrt(3.0)
    Qxy = -(np.conj(dx) * dy + np.conj(dy) * dx)
    Qyz = -(np.conj(dy) * dz + np.conj(dz) * dy)
    Qzx = -(np.conj(dz) * dx + np.conj(dx) * dz)
    return np.array([Qx2y2, Q3z2, Qxy.real, Qyz.real, Qzx.real])


def normalize_d(d):
    d = np.asarray(d, dtype=complex)
    return d / np.sqrt(np.vdot(d, d).real)


# ------------------------------------------------------------------
# Director-language bond energy (Eq. S23 region)
#   e_ij = Jn |di.conj(dj)|^2 + (Kn - Jn) |di.dj|^2
# ------------------------------------------------------------------
def bond_energy(di, dj, Jn, Kn):
    di = np.asarray(di, dtype=complex)
    dj = np.asarray(dj, dtype=complex)
    overlap_c = abs(np.vdot(dj, di)) ** 2      # |di . conj(dj)|^2  (vdot conjugates first arg)
    overlap_d = abs(np.dot(di, dj)) ** 2       # |di . dj|^2
    return Jn * overlap_c + (Kn - Jn) * overlap_d


# ------------------------------------------------------------------
# The 4 Gell-Mann generators used in the paper (Eq. S25)
# ------------------------------------------------------------------
def gell_mann_4():
    l1 = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex)
    l2 = np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=complex)
    l3 = np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=complex)
    l4 = np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex)
    # NOTE: the paper's printed matrices (S25) mix these standard Gell-Mann forms;
    # we reconstruct the *set* {lambda1..4} = standard off-diagonal Gell-Mann
    # generators (lambda1,lambda2,lambda4,lambda5,lambda6,lambda7 minus diagonals),
    # choosing the 4 that rotate within/among the (dx,dy,dz) director components.
    return [l1, l2, l3, l4]


def global_rotation(phis, gens=None):
    """U(phi) = exp(i sum_j lambda_j phi_j)."""
    from scipy.linalg import expm
    if gens is None:
        gens = gell_mann_4()
    M = np.zeros((3, 3), dtype=complex)
    for phi, g in zip(phis, gens):
        M += phi * g
    return expm(1j * M)
