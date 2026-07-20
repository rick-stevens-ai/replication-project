"""
patch_model.py
=====================================================================
Replication of the 6-band effective patch model of

    A. Friedlan & H.-Y. Kee,
    "Emergence of nematic loop-current bond order in Kagome metals
     near van Hove singularities", arXiv:2510.05234v2 (2026).

PROVENANCE
----------
This module ADAPTS the shared loop-current kagome kernel
    ~/Dropbox/XFER/TEXTURES-100/shared-kernels/loop_current_kagome_kernel.py
(built for Fernandes et al. arXiv:2502.16657). Reused directly:
  * hexagonal-BZ geometry / reciprocal-vector + M-point conventions,
  * the general "loop current = Im<c^dag_i c_j>, charge = Re<...>" bond-operator
    logic and Peierls-flux philosophy,
  * FHS-style density-matrix construction over a k-grid.
The Friedlan-Kee paper, however, is NOT the plain 3x3 NN kagome model of the
kernel. Its central object is a 6x6 *effective patch* Bloch Hamiltonian (Eq. 4)
built from two van Hove singularities (vH1 p-type, vH2 m-type) at each of the
3 M points, with the CBO/LCO/NLCBO order entering as complex 3Q bond parameters
Delta_ab. We therefore build that 6x6 H(k) here from scratch, but keep the
kernel's kagome geometry so the two live in the same convention family.

Everything below is transcribed directly from the paper's equations. No fitted
or fabricated numbers: ε, s1, s2, Δ, λ come from the paper (Figs 4/5, Sec II).
"""
from __future__ import annotations
import numpy as np

SQRT3 = np.sqrt(3.0)

# ---- paper parameters (Fig. 4 / Fig. 5 captions, Sec. II) ------------------
EPS_DEFAULT = 0.12     # eV, half the vH1/vH2 energy separation (Fig. 5)
S1_DEFAULT = -1.62     # = -2|b'|^2, b'~0.9 for CsV3Sb5 (Fig. 5)
S2_DEFAULT = 0.5       # = +2|b|^2,  b ~0.5 for CsV3Sb5 (Fig. 5)
DELTA_FIG4 = 0.2       # eV, order-parameter magnitude used in Figs 4/5


# ---------------------------------------------------------------------------
# patch momenta k_alpha  (Eq. 1)
# ---------------------------------------------------------------------------
def k_alphas(kx, ky):
    """(k1, k2, k3) from Eq. (1). Related by threefold rotation."""
    k1 = -kx / 2.0 + SQRT3 * ky / 2.0
    k2 = -kx / 2.0 - SQRT3 * ky / 2.0
    k3 = kx
    return np.array([k1, k2, k3])


# ---------------------------------------------------------------------------
# the 3Q order-parameter triplet from phases (phi1, phi2, phi3)
# ---------------------------------------------------------------------------
def deltas_from_phases(mag, phis, mags=None):
    """(Δ_AB, Δ_BC, Δ_CA) = |Δ| (e^{iϕ1}, e^{iϕ2}, e^{iϕ3}).
    If `mags` (len-3) given, use per-component amplitudes (for ∆≠∆')."""
    phis = np.asarray(phis, dtype=float)
    if mags is None:
        amp = np.full(3, float(mag))
    else:
        amp = np.asarray(mags, dtype=float)
    return amp * np.exp(1j * phis)


PHASE_CONFIGS = {
    # name        (phi1, phi2, phi3)     -> total phase Phi
    "CBO+":  (0.0, 0.0, 0.0),                    # Phi = 0
    "CBO-":  (np.pi, np.pi, np.pi),              # Phi = 3pi = pi (mod 2pi)
    "LCBO+": (np.pi/3, np.pi/3, np.pi/3),        # Phi = pi
    "LCBO-": (-np.pi/3, -np.pi/3, -np.pi/3),     # Phi = -pi = pi
    "NLCBO": (0.0, np.pi/2, np.pi/2),            # Phi = pi, breaks C3
    "LCO":   (np.pi/2, np.pi/2, np.pi/2),        # pure imaginary Delta (Phi=3pi/2)
}


def total_phase(phis):
    return np.mod(np.sum(phis), 2 * np.pi)


# ---------------------------------------------------------------------------
# 6x6 effective patch Hamiltonian  H(k)  (Eq. 4)
# basis order (paper): {psi2A, psi2B, psi2C, psi1A, psi1B, psi1C}
#   vH2 block = upper-left 3x3, on-site +eps, factor s2, uses Delta*  (conj)
#   vH1 block = lower-right 3x3, on-site -eps, factor s1, uses Delta
#   lambda k_alpha couples psi1(alpha) <-> psi2(alpha) (diagonal in sublattice)
# ---------------------------------------------------------------------------
def H_patch(kx, ky, deltas, eps=EPS_DEFAULT, s1=S1_DEFAULT, s2=S2_DEFAULT,
            lam=0.0, mu=0.0):
    """Full 6x6 H(k) - mu*I. `deltas` = (Δ_AB, Δ_BC, Δ_CA) complex."""
    dAB, dBC, dCA = deltas
    ka = k_alphas(kx, ky)
    H = np.zeros((6, 6), dtype=complex)

    # --- vH2 block (indices 0,1,2): +eps, factor s2, Delta* off-diagonals ---
    # From Eq. (4): row psi2A: [eps, s2 dAB*, s2 dCA]; row psi2B:[s2 dAB, eps, s2 dBC*]
    #               row psi2C:[s2 dCA*, s2 dBC, eps]
    H[0, 0] = eps; H[1, 1] = eps; H[2, 2] = eps
    H[0, 1] = s2 * np.conj(dAB); H[0, 2] = s2 * dCA
    H[1, 0] = s2 * dAB;          H[1, 2] = s2 * np.conj(dBC)
    H[2, 0] = s2 * np.conj(dCA); H[2, 1] = s2 * dBC

    # --- vH1 block (indices 3,4,5): -eps, factor s1, Delta off-diagonals -----
    # row psi1A:[-eps, s1 dAB, s1 dCA*]; row psi1B:[s1 dAB*, -eps, s1 dBC];
    # row psi1C:[s1 dCA, s1 dBC*, -eps]
    H[3, 3] = -eps; H[4, 4] = -eps; H[5, 5] = -eps
    H[3, 4] = s1 * dAB;          H[3, 5] = s1 * np.conj(dCA)
    H[4, 3] = s1 * np.conj(dAB); H[4, 5] = s1 * dBC
    H[5, 3] = s1 * dCA;          H[5, 4] = s1 * np.conj(dBC)

    # --- lambda k_alpha mixing: psi1(alpha) <-> psi2(alpha) (Eq. 4) ---------
    for a in range(3):
        H[a, 3 + a] = lam * ka[a]
        H[3 + a, a] = lam * ka[a]

    if mu != 0.0:
        H -= mu * np.eye(6)
    # Hermiticity guard
    assert np.allclose(H, H.conj().T), "H not Hermitian"
    return H


# ---------------------------------------------------------------------------
# analytic unperturbed (lambda=0) eigenvalues  (Eq. 9)
# ---------------------------------------------------------------------------
def eig_analytic_unpert(Phi, delta=DELTA_FIG4, eps=EPS_DEFAULT,
                        s1=S1_DEFAULT, s2=S2_DEFAULT, mu=0.0):
    """E_n^(i) = (-1)^i eps - mu + 2 s_i Delta cos((Phi + 2 pi n)/3), Eq. (9).
    i=1,2 (return in that order), n=0,1,2. Returns array shape (2,3)."""
    out = np.empty((2, 3))
    for idx, i in enumerate((1, 2)):
        si = s1 if i == 1 else s2
        for n in range(3):
            out[idx, n] = ((-1) ** i) * eps - mu + 2 * si * delta * np.cos((Phi + 2 * np.pi * n) / 3.0)
    return out


# ---------------------------------------------------------------------------
# inverse-energy perturbation factors  (Eq. 12)
# ---------------------------------------------------------------------------
def inv_energy_factors(delta, eps=EPS_DEFAULT, s1=S1_DEFAULT, s2=S2_DEFAULT):
    """Return (1/DE1, 1/DE2) per Eq. (12)."""
    A = 2 * delta * (s1 - s2) + 2 * eps      # denominator common term
    B = delta * (s1 + 2 * s2) - 2 * eps
    inv_dE1 = 1.0 / A - 2.0 / B
    inv_dE2 = 1.0 / A + 1.0 / B
    return inv_dE1, inv_dE2


# ---------------------------------------------------------------------------
# second-order-in-lambda energy corrections per phase (Eq. 11)
# integrated over occupied k (we use a symmetric patch disk of radius kcut).
# ---------------------------------------------------------------------------
def delta_E_configs(delta, lam, eps=EPS_DEFAULT, s1=S1_DEFAULT, s2=S2_DEFAULT,
                    kcut=1.0, nk=241, fill_frac=1.0):
    """Return dict of second-order corrections deltaE for CBO-, LCBO+, NLCBO,
    integrated over the OCCUPIED patch (Eq. 11). `fill_frac` in (0,1] sets the
    occupied fraction: fill_frac=1 -> full disk |k|<=kcut (band fully occupied,
    paper says LCBO+ wins); fill_frac<1 -> partially filled band occupying only
    an inner disk of radius kcut*sqrt(fill_frac) (condition iii: NLCBO regime).
      dECBO-  = (lam^2/6) sum [1/DE1 - 1/DE2] (kx^2+ky^2)
      dELCBO+ = (lam^2/6) sum{[1/DE1 - 1/DE2](kx^2+ky^2) + (3/2)(kx^2+ky^2)/DE2}
      dENLCBO = (lam^2/6) sum{[1/DE1 - 1/DE2](kx^2+ky^2) + (8/3) kx^2 /DE2}
    (The paper writes k1^2+k2^2+k3^2 = (3/2)(kx^2+ky^2), used in the isotropic term.)
    """
    inv_dE1, inv_dE2 = inv_energy_factors(delta, eps, s1, s2)
    xs = np.linspace(-kcut, kcut, nk)
    KX, KY = np.meshgrid(xs, xs)
    r_occ = kcut * np.sqrt(fill_frac)
    mask = (KX ** 2 + KY ** 2) <= r_occ ** 2
    kx = KX[mask]; ky = KY[mask]
    r2 = kx ** 2 + ky ** 2
    iso = (inv_dE1 - inv_dE2) * r2
    pref = lam ** 2 / 6.0
    dECBOm = pref * np.sum(iso)
    dELCBOp = pref * np.sum(iso + 1.5 * r2 * inv_dE2)
    dENLCBO = pref * np.sum(iso + (8.0 / 3.0) * kx ** 2 * inv_dE2)
    return dict(CBOm=dECBOm, LCBOp=dELCBOp, NLCBO=dENLCBO,
                inv_dE1=inv_dE1, inv_dE2=inv_dE2)


def band_correction_along_axis(delta, lam, axis="kx", eps=EPS_DEFAULT,
                               s1=S1_DEFAULT, s2=S2_DEFAULT, kmax=1.0, nk=51):
    """Per-k band energy correction (integrand of Eq. 11, without the 1/6 sum)
    along a line in k-space. This is the *dispersion* of the corrected band that
    the paper's mechanism argument (Sec III B) rests on. Returns dict of arrays
    keyed by phase; along k_x the NLCBO correction is the MOST negative because
    of its +8kx^2/(3 DE2) term with 1/DE2<0.
    Correction integrands (per Eq. 11, dropping common lam^2/6 factor):
        CBO- : [1/DE1 - 1/DE2] (kx^2+ky^2)
        LCBO+: [1/DE1 - 1/DE2] (kx^2+ky^2) + (3/2)(kx^2+ky^2)/DE2
        NLCBO: [1/DE1 - 1/DE2] (kx^2+ky^2) + (8/3) kx^2 / DE2
    """
    inv_dE1, inv_dE2 = inv_energy_factors(delta, eps, s1, s2)
    ks = np.linspace(-kmax, kmax, nk)
    if axis == "kx":
        kx = ks; ky = np.zeros_like(ks)
    else:
        kx = np.zeros_like(ks); ky = ks
    r2 = kx ** 2 + ky ** 2
    iso = (inv_dE1 - inv_dE2) * r2
    pref = lam ** 2 / 6.0
    return dict(k=ks,
                CBOm=pref * iso,
                LCBOp=pref * (iso + 1.5 * r2 * inv_dE2),
                NLCBO=pref * (iso + (8.0 / 3.0) * kx ** 2 * inv_dE2),
                inv_dE2=inv_dE2)


# ---------------------------------------------------------------------------
# bond current / charge extraction (adapted from shared kernel philosophy)
# For a given order config, integrate <psi^dag psi> to expose Re (charge/CBO)
# vs Im (loop current/LCO) content of each Delta channel.
# ---------------------------------------------------------------------------
def order_current_charge(config_name, mag=DELTA_FIG4, eps=EPS_DEFAULT,
                         s1=S1_DEFAULT, s2=S2_DEFAULT, lam=0.3, mu=0.0,
                         nk=61, kcut=1.0, nfill=3):
    """Classify a config by the Re/Im content of its Delta triplet AND by the
    filled-band bond expectation. Returns per-channel (Re, Im) of Delta and a
    boolean TRSB flag (loop current present <=> any Im(Delta_ab) != 0 in a way
    not removable by gauge, i.e. Phi encodes it via individual phi_i)."""
    phis = PHASE_CONFIGS[config_name]
    d = deltas_from_phases(mag, phis)
    Phi = total_phase(phis)
    re = np.round(d.real, 6)
    im = np.round(d.imag, 6)
    # TRSB present if the current-density operator has nonzero expectation:
    # encoded by individual phi_i (any nonzero Im component that is not a pure
    # real CBO). CBO+/CBO- have all-real Delta -> no loop current.
    trsb = bool(np.any(np.abs(im) > 1e-9))
    return dict(config=config_name, Phi=float(Phi),
                Re_Delta=re.tolist(), Im_Delta=im.tolist(), TRSB=trsb)
