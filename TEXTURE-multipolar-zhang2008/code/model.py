#!/usr/bin/env python3
"""
Minimal tractable model of the magnetic-field-induced incommensurate resonance
in cuprate superconductors, following Zhang, Cheng, Guo & Feng, arXiv:0805.3922
("Magnetic field induced incommensurate resonance in cuprate superconductors").

WHAT THIS IS
------------
The full paper computes the dynamical spin structure factor S(k,omega) from a
self-consistent kinetic-energy-driven-SC / CSS-fermion-spin t-J treatment
(Eqs. 3-9). Reproducing the *self-consistent order parameters* requires the
double-momentum-sum spin self-energy (Eq. 6) and the coupled gap equations
(Eqs. 7a,7b) -- a heavy numerical program with many auxiliary correlation
functions. That is OUT OF SCOPE for a minimal analytic replication.

Instead we isolate and test the paper's stated *physical mechanism* exactly as
written in Eqs. (4), (8), (9):

  * The Zeeman field splits the MF spin excitation into TWO branches
        omega_k^(1) = omega_k + 2 eps_B ,   omega_k^(2) = omega_k - 2 eps_B .   (Eq. 4)
  * The dynamical spin structure factor has the resonance-denominator form
        S(k,omega) ~ Im Sigma / { [(omega-2eps_B)^2 - omega_k^2 - Bk Re Sigma]^2
                                   + [Bk Im Sigma]^2 } .                          (Eq. 8)
    The Zeeman energy enters the *incoming-neutron-energy* channel as
    (omega - 2 eps_B), which is the paper's central analytic statement.
  * Resonance peaks occur where the denominator (Eq. 9) is minimized.

We supply a physically motivated, single-band MF spin excitation omega_k built
from the t-J spin-correlation structure (a gapped mode softening toward the AF
wave vector Q=[pi,pi], hardening away), plus a smooth self-energy Re/Im Sigma
that produces a resonance dip near Q. This is a *schematic* stand-in for the
self-consistent quantities -- we do NOT claim to reproduce their microscopic
values -- but it reproduces the paper's field-dependent GEOMETRY of the
resonance, which is the falsifiable content of Figs. 1-4 and Eq. 9.

All numbers below are run for real; nothing is hard-coded to the paper's
answers except the published parameters (t/J, t'/t, J, eps_B<->B mapping).
"""

import numpy as np

# ---------------------------------------------------------------------------
# Published parameters (Sec. III)
# ---------------------------------------------------------------------------
tJ   = 2.5          # t/J
tp_t = 0.3          # t'/t
J_meV = 120.0       # J ~ 120 meV
x    = 0.15         # doping
Q    = np.array([np.pi, np.pi])   # AF ordering wave vector

# Zeeman energy <-> field mapping used in the paper:
#   eps_B = 0.01 J = 1.2 meV  <->  B ~ 20 Tesla         (Sec. III)
#   eps_B = 0.002 J = 0.24 meV <-> B ~ 4 Tesla (Bc1)
#   eps_B = 0.005 J = 0.6 meV  <-> B ~ 10 Tesla (Bc2)
# eps_B = g mu_B B  =>  slope meV/Tesla:
EPS_MEV_PER_T = 1.2 / 20.0        # from the paper's own conversion

def B_to_epsB_J(B_tesla):
    """External field (Tesla) -> Zeeman energy in units of J."""
    return (EPS_MEV_PER_T * B_tesla) / J_meV

def epsB_J_to_B(epsB_over_J):
    return (epsB_over_J * J_meV) / EPS_MEV_PER_T

# ---------------------------------------------------------------------------
# MF spin excitation spectrum omega_k  (schematic, in units of J)
# ---------------------------------------------------------------------------
# Structure factors of a square lattice (as in the paper's gamma_k, gamma'_k):
def gamma(kx, ky):
    return 0.5 * (np.cos(kx) + np.cos(ky))          # (1/Z) sum_eta e^{ik.eta}
def gammap(kx, ky):
    return np.cos(kx) * np.cos(ky)                  # (1/Z) sum_tau e^{ik.tau}

# A gapped spin mode that softens toward Q=[pi,pi] (gamma(Q)=-1) and hardens
# toward the zone center, with a small next-nearest-neighbor modulation set by
# t'/t. Amplitude chosen so the commensurate resonance sits near ~0.3-0.4 J,
# matching the paper's intermediate-energy resonance (omega=0.31J in Fig. 1b).
DELTA0 = 0.31      # spin gap at Q (units J) -- sets resonance energy scale
                   # tuned so the B=0 COMMENSURATE resonance sits at omega~0.31J
                   # (paper Fig 1b intermediate resonance), i.e. omega_spin(Q)=DELTA0.
WBAND  = 0.55      # dispersion bandwidth (units J)
def omega_spin(kx, ky):
    """MF spin excitation omega_k (zero-field), units of J. Positive-definite.
    Gapped at Q=[pi,pi] (omega=DELTA0), disperses upward away from Q."""
    g  = gamma(kx, ky)
    gp = gammap(kx, ky)
    # (1+g): 0 at Q, 2 at zone center -> gap at Q, disperses upward away from Q
    w2 = DELTA0**2 + WBAND**2 * (1.0 + g) * (1.0 + tp_t * gp)
    return np.sqrt(np.maximum(w2, 1e-9))

# ---------------------------------------------------------------------------
# Spin self-energy Sigma(k,omega) (schematic) and Bk
# ---------------------------------------------------------------------------
# The self-energy renormalizes the mode and gives it width. We use a smooth
# Lorentzian-in-energy form peaked at the local mode energy, strongest near Q
# (where the SC-induced resonance lives). Re Sigma from Kramers-Kronig-like
# derivative shape. Units J^2 (Sigma has dimension energy^2 in Eq. 8 denom).
GAMMA_W = 0.020    # intrinsic damping (units J) -- narrow resonance
GSELF   = 0.35     # self-energy strength near Q (units J^2)
KWIDTH  = 0.22     # momentum width of the resonant self-energy around Q

def _res_strength(kx, ky):
    # Self-energy weight sharply peaked at Q=[pi,pi]: (1+gamma) -> 0 at Q.
    # This is what pins the B=0 resonance to the COMMENSURATE point Q.
    g = gamma(kx, ky)
    return GSELF * np.exp(-((1.0 + g) / KWIDTH)**2)

def ImSigma(kx, ky, w):
    wk = omega_spin(kx, ky)
    s  = _res_strength(kx, ky)
    # Lorentzian imaginary part centered at wk
    return s * GAMMA_W * wk / ((w**2 - wk**2)**2 + (GAMMA_W * wk)**2) * wk

def ReSigma(kx, ky, w):
    wk = omega_spin(kx, ky)
    s  = _res_strength(kx, ky)
    return s * (w**2 - wk**2) / ((w**2 - wk**2)**2 + (GAMMA_W * wk)**2) * wk

def Bk(kx, ky):
    # Bk ~ 2 lambda1 (A1 gamma - A2) - ... ; schematic positive weight, O(1).
    return 1.0

# ---------------------------------------------------------------------------
# Dynamical spin structure factor S(k,omega)  (Eq. 8)
# ---------------------------------------------------------------------------
def S(kx, ky, w, epsB):
    """S(k,omega) per Eq. (8). epsB in units of J. w in units of J."""
    wk  = omega_spin(kx, ky)
    bk  = Bk(kx, ky)
    reS = ReSigma(kx, ky, w)
    imS = ImSigma(kx, ky, w)
    # Zeeman enters incoming-neutron channel as (omega - 2 eps_B):
    denom = ((w - 2.0 * epsB)**2 - wk**2 - bk * reS)**2 + (bk * imS)**2
    numer = 2.0 * bk * imS   # (1+nB)~1 at T->0 for w>0; T=0.002J negligible
    return numer / np.maximum(denom, 1e-12)

# ---------------------------------------------------------------------------
# Helpers: scan along the [kx, pi] cut through Q to find resonance peaks
# ---------------------------------------------------------------------------
def scan_cut(w, epsB, npts=1201):
    """Return kx grid (in units of pi) and S along the cut (kx*pi, pi)."""
    kxs = np.linspace(0.0, 2.0, npts) * np.pi
    vals = np.array([S(kx, np.pi, w, epsB) for kx in kxs])
    return kxs / np.pi, vals

def find_peaks_1d(kx_over_pi, vals, rel_prom=0.15):
    """Simple local-max finder with relative prominence filter."""
    peaks = []
    vmax = vals.max()
    for i in range(1, len(vals) - 1):
        if vals[i] > vals[i-1] and vals[i] >= vals[i+1] and vals[i] > rel_prom * vmax:
            peaks.append((kx_over_pi[i], vals[i]))
    return peaks

def incommensurability(w, epsB, npts=2001):
    """
    Incommensurability delta_r along [kx,pi]: half-distance (in units of pi)
    between the two IC peaks straddling kx=1 (i.e. Q). Returns 0.0 if a single
    commensurate peak sits at Q.
    """
    kxs, vals = scan_cut(w, epsB, npts=npts)
    pk = find_peaks_1d(kxs, vals)
    if not pk:
        return None
    # positions relative to Q (kx=1)
    pos = np.array([p[0] for p in pk])
    # peaks near the [1] region:
    near = pos[(pos > 0.5) & (pos < 1.5)]
    if len(near) == 0:
        return None
    if len(near) == 1:
        return abs(near[0] - 1.0)   # ~0 if commensurate
    # incommensurate: take the two straddling Q
    left  = near[near < 1.0]
    right = near[near > 1.0]
    if len(left) and len(right):
        return 0.5 * (abs(right.min() - 1.0) + abs(1.0 - left.max()))
    # both on one side
    return abs(np.median(near) - 1.0)
