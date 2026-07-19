"""
sof_model.py — Symmetry-based spin-orbit-field (SOF) model for Fe/GaAs(001)
Replication core of Gmitra, Matos-Abiague, Draxl & Fabian, PRL 111, 036603 (2013)
(arXiv:1303.2510): "Magnetic control of spin-orbit fields."

SCOPE NOTE
----------
The full paper computes the interface electronic structure with relativistic
(SOC) FLAPW DFT (FLEUR) on Fe/GaAs slabs, then extracts the SOF for a generic
Bloch state directly from the ab-initio bands using a symmetry-based formula.
That DFT step is out of scope for an in-process replication (DFT-heavy, needs a
cluster). What IS tractable and is the genuine *analytic core* of the paper is:

  1. The C2v symmetry-allowed SOC Hamiltonian, Eqs. (1)-(3).
  2. The Bychkov-Rashba (alpha) / Dresselhaus (beta) decomposition, and the
     angular (magnetization-orientation) parametrization of Table I, Eqs.(10-11).
  3. Reconstruction of the k-resolved SOF texture w(k) ("butterflies") and its
     magnitude polar plots, Fig. 2.
  4. The qualitative magnetic-control claims: alpha_1 changes sign vs theta,
     alpha_1*beta_1 flips sign between [1-10] and [110]; band n=2 does not.

We take the paper's own extracted numbers (Table I) as the ab-initio "ground
truth" and verify the internal consistency + downstream texture claims that the
paper makes from them. This is a faithful replication of the symmetry model, not
of the DFT numbers themselves.

Conventions (paper):
  x = [1-10], y = [110]  (in-plane diagonal directions of GaAs)
  theta = magnetization angle measured from [1-10]
  SOC parameters alpha_n(theta), beta_n(theta) in meV*Angstrom.
"""

import numpy as np

# ---------------------------------------------------------------------------
# Table I : band-resolved expansion coefficients (meV*Angstrom), E = 0.
#   alpha_n(theta) ~ A+_n + B+_n cos(2 theta)      (Eq. 10)
#   beta_n(theta)  ~ A-_n + B-_n cos(2 theta)      (Eq. 11)
# n=1,2 interface bands ; n=3,4 As-surface bands.
# ---------------------------------------------------------------------------
TABLE_I = {
    # n : (A_plus, B_plus, A_minus, B_minus)
    1: (-0.42,  -6.26, -11.32,   4.32),
    2: (-42.51,  1.82, -57.94,  -1.51),
    3: (-620.24, -88.74, -597.56, -89.62),
    4: (680.09,  95.61,  697.58, 103.15),
}


def alpha_beta(n, theta):
    """Bychkov-Rashba alpha_n and Dresselhaus beta_n (meV*A) vs magnetization
    angle theta (radians), Eqs. (10)-(11) with Table I coefficients."""
    Ap, Bp, Am, Bm = TABLE_I[n]
    alpha = Ap + Bp * np.cos(2.0 * theta)
    beta = Am + Bm * np.cos(2.0 * theta)
    return alpha, beta


def sof_linear(kx, ky, alpha, beta):
    """Linear-in-k spin-orbit field w(k) from the small-k limit of Eqs.(1)-(3).

    Near Gamma:  mu_n^(0) = alpha + beta ,  eta_n^(0) = -alpha + beta   (from
    alpha=(mu0-eta0)/2, beta=(mu0+eta0)/2).  With Eq.(3):
        w_x =  eta_n * ky = (-alpha + beta) ky
        w_y =  mu_n  * kx = ( alpha + beta) kx
        w_z = 0
    alpha,beta in meV*A ; kx,ky in 1/A ; returns (w_x,w_y) in meV.
    """
    mu0 = alpha + beta
    eta0 = -alpha + beta
    wx = eta0 * ky
    wy = mu0 * kx
    return wx, wy


def sof_magnitude_linear(k, phi, alpha, beta):
    """|w|/k along a contour of radius k, as function of the k-direction angle
    phi (matches the polar 'w/k' plots of Fig. 2). Returns |w|/k in meV*A."""
    kx = k * np.cos(phi)
    ky = k * np.sin(phi)
    wx, wy = sof_linear(kx, ky, alpha, beta)
    return np.hypot(wx, wy) / k


# ---------------------------------------------------------------------------
# Symmetry-extraction round trip (Eqs. 4-9): given model energy bands E(k,theta)
# built from a chosen (alpha,beta), verify the paper's extraction formulas
# recover alpha,beta.  This tests the *method*, not just the Hamiltonian.
#
# Model dispersion consistent with Hso = w.sigma on top of an exchange-split
# band: the SOC energy shift of the magnetization-aligned branch is
#   dE_so(k,theta) = sigma * [ w(k) . m_hat ]              (1st-order PT, in-plane)
# with m_hat = (cos theta, sin theta). We take sigma=+1 for the extracted band.
# ---------------------------------------------------------------------------
def model_energy(kx, ky, theta, alpha, beta, e0_coeff=1000.0):
    """Toy band energy (meV): parabolic core + linear SOC shift along m_hat.
    E(k,theta) = e0_coeff*(kx^2+ky^2) + w(k).m_hat  (odd-in-k SOC part is what
    the extraction isolates)."""
    wx, wy = sof_linear(kx, ky, alpha, beta)
    mx, my = np.cos(theta), np.sin(theta)
    e_even = e0_coeff * (kx**2 + ky**2)
    e_so = wx * mx + wy * my
    return e_even + e_so


def extract_wxy(kx, ky, theta, alpha, beta, sigma=1.0):
    """Paper Eqs. (4)-(7): extract w_x, w_y from finite-difference of the model
    bands.  dE_so = [E(k)-E(-k)]/2 ; Gamma_so = [E(-kx,ky)-E(kx,-ky)]/2 ;
        w_x = sigma * (dE_so + Gamma_so)/(2 cos theta)
        w_y = sigma * (dE_so - Gamma_so)/(2 sin theta)
    Valid away from theta=0,pi/2 (there L'Hopital needed)."""
    Epp = model_energy(kx, ky, theta, alpha, beta)
    Emm = model_energy(-kx, -ky, theta, alpha, beta)
    Emp = model_energy(-kx, ky, theta, alpha, beta)
    Epm = model_energy(kx, -ky, theta, alpha, beta)
    dE = (Epp - Emm) / 2.0
    Gam = (Emp - Epm) / 2.0
    wx = sigma * (dE + Gam) / (2.0 * np.cos(theta))
    wy = sigma * (dE - Gam) / (2.0 * np.sin(theta))
    return wx, wy


def extract_alpha_beta(theta, alpha_true, beta_true, k=1e-3, sigma=1.0):
    """Paper Eqs. (8)-(9): extract alpha,beta from k-gradients a_n,b_n of bands.
      a_n = dE/dkx|_0 ,  b_n = dE/dky|_0  (odd SOC part)
      alpha = sigma*(a cos th - b sin th)/sin(2 th)
      beta  = sigma*(a cos th + b sin th)/sin(2 th)
    Uses central differences of the model band. Returns (alpha,beta) meV*A."""
    # central difference gradient of the *odd* (SOC) part at Gamma
    def E(kx, ky):
        return model_energy(kx, ky, theta, alpha_true, beta_true)
    a = (E(k, 0) - E(-k, 0)) / (2 * k)      # dE/dkx
    b = (E(0, k) - E(0, -k)) / (2 * k)      # dE/dky
    s2 = np.sin(2 * theta)
    alpha = sigma * (a * np.cos(theta) - b * np.sin(theta)) / s2
    beta = sigma * (a * np.cos(theta) + b * np.sin(theta)) / s2
    return alpha, beta
