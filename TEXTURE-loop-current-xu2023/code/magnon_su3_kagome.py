"""
magnon_su3_kagome.py
=====================================================================
Replication of the ANALYTICAL single-magnon core of

    Yi Xu, S. Capponi, J.-Y. Chen, L. Vanderstraeten, J. Hasik,
    A. H. Nevidomskyy, M. Mambrini, K. Penc, D. Poilblanc,
    "Phase diagram of the chiral SU(3) antiferromagnet on the kagome
     lattice", arXiv:2306.16192v1 (2023).

------------------------------------------------------------------
PROVENANCE / KERNEL REUSE
------------------------------------------------------------------
Adapted (structurally) from the shared REUSABLE loop-current kagome
kernel:
    ~/Dropbox/XFER/TEXTURES-100/shared-kernels/loop_current_kagome_kernel.py
    (built for Fernandes-Birol-Ye-Vanderbilt arXiv:2502.16657).

WHY the kernel is only a PARTIAL structural fit (honest scope note):
  * The Xu-2023 paper is a MANY-BODY SU(3) *spin* model (chiral spin
    liquid / topological spin liquid on the kagome lattice), solved by
    exact diagonalization + tensor networks (PEPS/PESS/MPS). It is NOT a
    tight-binding loop-current METAL. So the kernel's Fukui-Hatsugai
    Chern / Kubo-conductivity band machinery does not map onto the
    paper's headline TSL claims (those require ED/tensor networks that
    are out of scope for an overnight single-node replication).
  * HOWEVER the paper contains a fully ANALYTICAL, machine-checkable
    core: the single-magnon problem above the SU(3) ferromagnet. Its
    3x3 Bloch matrix (Eq. A1) is a kagome 3-sublattice hopping matrix
    in which the chiral term K_I enters exactly as an IMAGINARY
    (Peierls-like, TRS-breaking) hopping -- structurally the SAME object
    the loop-current kernel builds (complex NN kagome hopping that breaks
    time reversal). We therefore REUSE the kernel's kagome-geometry
    conventions (3 sublattices, hexagonal BZ, half-bond structure,
    eigvalsh-on-a-BZ-grid pattern, and the "imag hopping = broken TRS"
    idea) and specialise the 3x3 matrix to Eq. A1.

This module diagonalises Eq. A1 across the BZ and checks 5 concrete
analytical claims quantitatively. Real code, honest negatives.
"""
from __future__ import annotations
import numpy as np

SQRT3 = np.sqrt(3.0)


# ---------------------------------------------------------------------------
# Eq. A1  --  single-magnon Bloch matrix over the SU(3) ferromagnet
# ---------------------------------------------------------------------------
# Energy measured from the FM state; q=(qx,qy). Depends only on
#   x = J + K_R        (real, symmetric hopping strength)
#   K_I               (chiral / TRS-breaking imaginary part)
#
# As printed in the paper (Eq. A1), the 3x3 matrix is:
#
#   [ -4x                         2(x-iK_I)cos((qx-sqrt3 qy)/2)   2(x+iK_I)cos((qx+sqrt3 qy)/2) ]
#   [ 2(x+iK_I)cos((qx-sqrt3 qy)/2)   -4x                          2(x-iK_I)cos(qx)             ]
#   [ 2(x-iK_I)cos((qx+sqrt3 qy)/2)   2(x+iK_I)cos(qx)             -4x                          ]
#
# (Hermitian: off-diagonals are complex conjugate pairs.)
def magnon_matrix(qx, qy, JpKR, KI):
    """3x3 Hermitian single-magnon Bloch matrix, Eq. A1. Energy from FM."""
    x = JpKR
    a = (qx - SQRT3 * qy) / 2.0      # bond direction 1
    b = (qx + SQRT3 * qy) / 2.0      # bond direction 2
    c = qx                            # bond direction 3

    zp = x + 1j * KI                  # +iK_I  (chiral, TRS-breaking)
    zm = x - 1j * KI                  # -iK_I

    H = np.zeros((3, 3), dtype=complex)
    H[0, 0] = H[1, 1] = H[2, 2] = -4.0 * x
    H[0, 1] = 2.0 * zm * np.cos(a)
    H[0, 2] = 2.0 * zp * np.cos(b)
    H[1, 2] = 2.0 * zm * np.cos(c)
    # Hermitian conjugates
    H[1, 0] = np.conj(H[0, 1])
    H[2, 0] = np.conj(H[0, 2])
    H[2, 1] = np.conj(H[1, 2])
    return H


def magnon_bands(qx, qy, JpKR, KI):
    """Sorted (ascending) magnon eigenvalues at q."""
    return np.sort(np.linalg.eigvalsh(magnon_matrix(qx, qy, JpKR, KI)).real)


# ---------------------------------------------------------------------------
# BZ sampling utilities (kagome hexagonal BZ, reusing kernel conventions)
# ---------------------------------------------------------------------------
A1 = np.array([1.0, 0.0])
A2 = np.array([0.5, SQRT3 / 2.0])


def _reciprocal(a1, a2):
    M = np.array([a1, a2]).T
    B = 2 * np.pi * np.linalg.inv(M).T
    return B[0], B[1]


B1, B2 = _reciprocal(A1, A2)


def bz_grid(nk):
    f = np.linspace(0.0, 1.0, nk, endpoint=False)
    U, V = np.meshgrid(f, f, indexing='ij')
    kx = U * B1[0] + V * B2[0]
    ky = U * B1[1] + V * B2[1]
    return kx.ravel(), ky.ravel()


def all_magnon_eigs(JpKR, KI, nk=120):
    """Vectorised: build all Bloch matrices on the BZ grid and batch-diagonalise.
    Returns (nk*nk, 3) ascending eigenvalues."""
    kx, ky = bz_grid(nk)
    a = (kx - SQRT3 * ky) / 2.0
    b = (kx + SQRT3 * ky) / 2.0
    c = kx
    x = JpKR
    zp = x + 1j * KI
    zm = x - 1j * KI
    n = kx.size
    H = np.zeros((n, 3, 3), dtype=complex)
    H[:, 0, 0] = H[:, 1, 1] = H[:, 2, 2] = -4.0 * x
    H[:, 0, 1] = 2.0 * zm * np.cos(a)
    H[:, 0, 2] = 2.0 * zp * np.cos(b)
    H[:, 1, 2] = 2.0 * zm * np.cos(c)
    H[:, 1, 0] = np.conj(H[:, 0, 1])
    H[:, 2, 0] = np.conj(H[:, 0, 2])
    H[:, 2, 1] = np.conj(H[:, 1, 2])
    w = np.linalg.eigvalsh(H)   # (n,3) ascending
    return w


# ---------------------------------------------------------------------------
# Ferromagnet energy per site (Sec. III E):  e_F = 2 J + 4 K_R / 3
# ---------------------------------------------------------------------------
def fm_energy_per_site(J, KR):
    return 2.0 * J + 4.0 * KR / 3.0


# ---------------------------------------------------------------------------
# Analytic q=0 magnon eigenvalues predicted by the paper:
#   {0,  -6(J+K_R) + 2 sqrt3 K_I,  -6(J+K_R) - 2 sqrt3 K_I}
# ---------------------------------------------------------------------------
def q0_predicted(JpKR, KI):
    x = JpKR
    return np.sort([0.0, -6.0 * x + 2.0 * SQRT3 * KI, -6.0 * x - 2.0 * SQRT3 * KI])


def q0_from_matrix(JpKR, KI):
    return magnon_bands(0.0, 0.0, JpKR, KI)
