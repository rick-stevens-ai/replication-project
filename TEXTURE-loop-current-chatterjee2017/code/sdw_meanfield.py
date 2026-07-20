"""
sdw_meanfield.py
=====================================================================
Square-lattice spin-density-wave (SDW) mean-field kernel for the
replication of

    S. Chatterjee, S. Sachdev, M. S. Scheurer,
    "Intertwining topological order and broken symmetry in a theory of
     fluctuating spin density waves", PRL / arXiv:1705.06289 (2017).

Implements Appendix B (Eqs. B3-B6, free energy) and the Appendix-C
loop-current bond diagnostic (Eq. C14).

PROVENANCE
----------
Reuses the *concept* of the shared kagome loop-current kernel
(~/Dropbox/XFER/TEXTURES-100/shared-kernels/loop_current_kagome_kernel.py):
the real=charge / imag=loop-current decomposition of the bond bilinear
<c_i^dag c_j> read off the filled-band density matrix. The kagome geometry
and Chern/Berry machinery are OUT OF SCOPE for this square-lattice SDW paper
and are not used. See code/PROVENANCE.md.

PHYSICS (Appendix B)
--------------------
* Square lattice, hoppings t_p for p'th neighbor, p = 1,2,3,4.
    Dispersion (Eq. B4):  xi_k = - sum_p t_p * (neighbor structure) - mu.
* SDW order:  <S_i> = N0 [ cos(K.r)cos(th) x + sin(K.r)cos(th) y + sin(th) z ]
    -> canting angle th (th=0 planar/coplanar, th=pi/2 ferromagnet),
       ordering wavevector K, amplitude N0. Field h = 2 U N0.
* Mean-field 2x2 Hamiltonian in the (c_{k,up}, c_{k+K,down}) basis (Eq. B4):
       h_k = [[ xi_k - (h/2) sin th ,   -(h/2) cos th        ],
              [ -(h/2) cos th        ,   xi_{k+K} + (h/2) sin th ]]
* Bands (Eq. B6):
       E_{k,s} = 1/2 [ xi_k + xi_{k+K}
                       + s*sqrt( (xi_k - xi_{k+K} - h sin th)^2 + h^2 cos^2 th ) ]
* Free energy per site (canonical):
       E/Ns = sum_s <E_{k,s} n_F(E_{k,s})>_k + mu*n - U n^2/4 + h^2/(4U)
       with n = sum_s <n_F(E_{k,s})>_k.
  We minimize E/Ns over (h, th, K) at fixed filling n (mu tuned to n).

All routines vectorized numpy; a scan runs in a few seconds.
"""
from __future__ import annotations
import numpy as np

PI = np.pi

# ---------------------------------------------------------------------------
# Square-lattice dispersion with up to 4th-neighbor hopping
# ---------------------------------------------------------------------------
def xi_k(kx, ky, tp, mu):
    """Bare band dispersion xi_k = eps_k - mu on the square lattice.

    tp = (t1, t2, t3, t4) for 1st..4th nearest neighbours.
    eps_k = -[ 2 t1 (cos kx + cos ky)
               + 4 t2 cos kx cos ky
               + 2 t3 (cos 2kx + cos 2ky)
               + 4 t4 (cos 2kx cos ky + cos kx cos 2ky) ]
    (standard square-lattice neighbour shells; the overall sign follows the
     H = - sum t c^dag c convention of Eq. B1.)
    """
    t1, t2, t3, t4 = (list(tp) + [0, 0, 0, 0])[:4]
    eps = (2 * t1 * (np.cos(kx) + np.cos(ky))
           + 4 * t2 * np.cos(kx) * np.cos(ky)
           + 2 * t3 * (np.cos(2 * kx) + np.cos(2 * ky))
           + 4 * t4 * (np.cos(2 * kx) * np.cos(ky)
                       + np.cos(kx) * np.cos(2 * ky)))
    return -eps - mu


def bands(kx, ky, tp, mu, h, theta, K):
    """Lower/upper SDW mean-field bands E_{k,-}, E_{k,+} (Eq. B6).

    Returns (E_minus, E_plus), each same shape as kx.
    """
    Kx, Ky = K
    xk = xi_k(kx, ky, tp, mu)
    xkK = xi_k(kx + Kx, ky + Ky, tp, mu)
    st, ct = np.sin(theta), np.cos(theta)
    disc = np.sqrt((xk - xkK - h * st) ** 2 + (h * ct) ** 2)
    half = 0.5 * (xk + xkK)
    return half - 0.5 * disc, half + 0.5 * disc


# ---------------------------------------------------------------------------
# BZ grid utilities
# ---------------------------------------------------------------------------
def bz_grid(nk):
    """Uniform k-grid over the square-lattice BZ [-pi, pi)^2."""
    k = np.linspace(-PI, PI, nk, endpoint=False)
    kx, ky = np.meshgrid(k, k, indexing="ij")
    return kx, ky


def _fermi(E, mu_eff=0.0, T=0.0):
    """Occupation. At T=0 (default) this is a step; a tiny T smooths the scan.
    Here E already includes -mu inside xi_k, so the Fermi level is 0."""
    if T <= 0:
        return (E < 0.0).astype(float)
    return 1.0 / (1.0 + np.exp(E / T))


# ---------------------------------------------------------------------------
# Filling and free energy
# ---------------------------------------------------------------------------
def filling(tp, mu, h, theta, K, nk=200, T=0.0):
    """Electron filling n = sum_s <n_F(E_{k,s})>  (per site, spinful: 0..2)."""
    kx, ky = bz_grid(nk)
    Em, Ep = bands(kx, ky, tp, mu, h, theta, K)
    n = _fermi(Em, T=T).mean() + _fermi(Ep, T=T).mean()
    return n


def solve_mu_for_filling(tp, h, theta, K, n_target, nk=160, T=0.01,
                         mu_lo=-12.0, mu_hi=12.0, tol=1e-4, itmax=60):
    """Bisection on mu so that filling(mu) = n_target."""
    for _ in range(itmax):
        mu = 0.5 * (mu_lo + mu_hi)
        n = filling(tp, mu, h, theta, K, nk=nk, T=T)
        if abs(n - n_target) < tol:
            return mu
        # filling increases with mu
        if n < n_target:
            mu_lo = mu
        else:
            mu_hi = mu
    return 0.5 * (mu_lo + mu_hi)


def free_energy(tp, U, h, theta, K, n_target, nk=160, T=0.01):
    """Mean-field free energy per site at fixed filling n_target.

    E/Ns = sum_s <E_{k,s} n_F>_k + mu*n - U n^2/4 + h^2/(4U).
    Returns (E_per_site, mu, n_actual).
    """
    mu = solve_mu_for_filling(tp, h, theta, K, n_target, nk=nk, T=T)
    kx, ky = bz_grid(nk)
    Em, Ep = bands(kx, ky, tp, mu, h, theta, K)
    fm, fp = _fermi(Em, T=T), _fermi(Ep, T=T)
    band_term = (Em * fm).mean() + (Ep * fp).mean()
    n = fm.mean() + fp.mean()
    E = band_term + mu * n - U * n_target ** 2 / 4.0 + h ** 2 / (4.0 * U)
    return E, mu, n


# ---------------------------------------------------------------------------
# Self-consistent gap (order parameter) at fixed (theta, K)
# ---------------------------------------------------------------------------
def sdw_amplitude(tp, mu, h, theta, K, nk=200, T=0.01):
    """Compute N0 = <S> self-consistency residual quantity.

    From Eq. B2, h = 2 U N0 with N0 the SDW amplitude. The mean-field
    self-consistency is N0 = <S_staggered> evaluated in the filled bands.
    For the 2x2 problem the staggered magnetization component conjugate to h
    is  m(h) = -(1/2) d(band energy)/dh summed over filled states, i.e.

        m = (1/2) < [ (h - (xk-xkK) sin th ) / (2 disc) ] (f_- - f_+) ... >

    We instead use the thermodynamically consistent definition m = -dE_band/dh
    per unit h-coupling, evaluated numerically, which is robust. Returns m so
    that the self-consistent condition is h = 2 U m.
    """
    kx, ky = bz_grid(nk)
    Kx, Ky = K
    xk = xi_k(kx, ky, tp, mu)
    xkK = xi_k(kx + Kx, ky + Ky, tp, mu)
    st, ct = np.sin(theta), np.cos(theta)
    disc = np.sqrt((xk - xkK - h * st) ** 2 + (h * ct) ** 2)
    disc = np.where(disc < 1e-12, 1e-12, disc)
    Em = 0.5 * (xk + xkK) - 0.5 * disc
    Ep = 0.5 * (xk + xkK) + 0.5 * disc
    fm, fp = _fermi(Em, T=T), _fermi(Ep, T=T)
    # dE_-/dh = -0.5 * d(disc)/dh ;  dE_+/dh = +0.5 * d(disc)/dh
    ddisc_dh = (-(xk - xkK - h * st) * st + h * ct ** 2) / disc
    dEband_dh = (-0.5 * ddisc_dh * fm + 0.5 * ddisc_dh * fp).mean()
    # m = -dE_band/dh ; self-consistency h = 2 U m
    return -dEband_dh


def self_consistent_h(tp, U, theta, K, n_target, nk=160, T=0.02,
                      h0=1.0, mix=0.5, itmax=200, tol=1e-4):
    """Iterate h <- 2 U m(h) to convergence at fixed (theta, K, n)."""
    h = h0
    for _ in range(itmax):
        mu = solve_mu_for_filling(tp, h, theta, K, n_target, nk=nk, T=T)
        m = sdw_amplitude(tp, mu, h, theta, K, nk=nk, T=T)
        h_new = 2.0 * U * abs(m)
        if abs(h_new - h) < tol:
            h = h_new
            break
        h = (1 - mix) * h + mix * h_new
    return h


# ---------------------------------------------------------------------------
# Loop-current bond diagnostic (Appendix C, Eq. C14)  -- reuses kernel concept
# ---------------------------------------------------------------------------
def sdw_bond_current(tp, mu, h, theta, K, bond=(1, 0), nk=200, T=0.01, Zij=1.0):
    """Bond bilinear T_ij = Z_ij t_ij <psi_i^dag psi_j> on bond delta=`bond`.

    Returns dict(kinetic=K_ij=-2 Re T, current=J_ij=2 Im T, raw=<..>).

    This transplants the shared kagome kernel's real=charge / imag=loop-current
    decomposition (KagomeModel.bond_current_and_charge) to the square-lattice
    2-band SDW problem. The 2x2 eigenvectors give the filled-band density matrix
    rho(k); <psi_i^dag psi_j> = sum_k Tr[rho(k) O_bond(k)] with the appropriate
    Bloch phase. For a purely COLLINEAR order (theta=0 or theta=pi/2 with real
    off-diagonal) the current J_ij vanishes; a NON-COLLINEAR (canted+incomm.)
    configuration is required for finite loop current (paper's key statement).
    """
    kx, ky = bz_grid(nk)
    Kx, Ky = K
    dx, dy = bond
    t1 = (list(tp) + [0])[0]
    st, ct = np.sin(theta), np.cos(theta)
    acc = 0.0 + 0.0j
    # Build the 2x2 h_k, diagonalize, form filled-band projector, evaluate the
    # nearest-neighbour bond operator in the same (k, k+K) two-component basis.
    kxf = kx.ravel(); kyf = ky.ravel()
    n = kxf.size
    xk = xi_k(kxf, kyf, tp, mu)
    xkK = xi_k(kxf + Kx, kyf + Ky, tp, mu)
    H = np.zeros((n, 2, 2), dtype=complex)
    H[:, 0, 0] = xk - 0.5 * h * st
    H[:, 1, 1] = xkK + 0.5 * h * st
    H[:, 0, 1] = -0.5 * h * ct
    H[:, 1, 0] = -0.5 * h * ct
    w, V = np.linalg.eigh(H)   # ascending
    fm = _fermi(w[:, 0], T=T)
    fp = _fermi(w[:, 1], T=T)
    # density matrix rho = f- |v0><v0| + f+ |v1><v1|
    v0 = V[:, :, 0]; v1 = V[:, :, 1]
    rho00 = fm * (v0[:, 0] * np.conj(v0[:, 0])) + fp * (v1[:, 0] * np.conj(v1[:, 0]))
    # The physical c_{k,up} component is channel 0. The NN hopping bond bilinear
    # <c_i^dag c_{i+delta}> for the up-spin electron = <c_{k,up}^dag c_{k,up}>
    # weighted by the Bloch phase e^{i k.delta}, summed over k.
    phase = np.exp(1j * (kxf * dx + kyf * dy))
    acc = np.sum(rho00 * phase) / n
    T_ij = Zij * t1 * acc
    return dict(kinetic=-2.0 * T_ij.real, current=2.0 * T_ij.imag, raw=acc)


# ---------------------------------------------------------------------------
# Phase classification from optimized (h, theta, K)
# ---------------------------------------------------------------------------
def classify_phase(h, theta, K, tol_h=1e-2, tol_ang=0.05, tol_K=0.15):
    """Map optimized order parameters to the paper's phase labels."""
    Kx, Ky = K
    if h < tol_h:
        return "PM (paramagnet, no SDW)"
    commensurate = (abs(Kx - PI) < tol_K) and (abs(Ky - PI) < tol_K)
    ferro = abs(theta - PI / 2) < tol_ang
    canted = (tol_ang < theta < PI / 2 - tol_ang)
    if ferro:
        return "F0 (ferromagnet, theta=pi/2)"
    if commensurate:
        if theta < tol_ang:
            return "D0 (Neel, K=(pi,pi), theta=0)"
        if canted:
            return "A0 (canted AFM, K=(pi,pi), 0<theta<pi/2)"
    else:
        if theta < tol_ang:
            return "B0 (planar spiral, K incommensurate, theta=0)"
        if canted:
            return "C0 (conical spiral, K incommensurate, 0<theta<pi/2)"
    return f"mixed (h={h:.3f}, theta={theta:.3f}, K=({Kx:.2f},{Ky:.2f}))"
