"""Modified Poisson-Nernst-Planck (mPNP) equilibrium solver in 1D slab geometry.

Independent open-source replication of:
  Ma, Xu, Zhang, "Modified Poisson-Nernst-Planck Model with Coulomb and
  Hard-sphere Correlations", SIAM J. Appl. Math. (2021), arXiv:2002.07489v3.

We solve the *equilibrium* form (modified Poisson-Boltzmann) used in Sec. 4
of the paper:

  -2 epsilon^2  d2 phi / dx2 = sum_i z_i c_i,         |x| < 1 - a       (3.12)
  c_i(x) = c_i^bulk * exp( -z_i phi(x) - mu^co_i(x) - mu^hs_i(x) ),     (eq.)

with Robin BC for phi at x = +/- (1-a):
  phi  +/-  (a/eta_s) * dphi/dx = V_+/-                                 (3.14)

Four model variants are supported, as in the paper:
  - MF :   mean-field PNP  (mu^co = mu^hs = 0)
  - SC :   short-range correlation only (mu^hs from MFMT, mu^co = 0)
  - LC :   long-range Coulomb correlation only (mu^co from WKB-GDH,
           mu^hs = 0)
  - LS :   both (mu^hs + mu^co)

Units: All quantities are dimensionless per Sec. 3.1.
       q     = ell_B / L          (Bjerrum / half-gap)
       eps   = ell_0 / L          (Debye / half-gap), with ell_0 the 1:1
                                  Debye length at bulk c0
       a     = ion radius / L
       eta_b = eps_b / eps_w      (dielectric of electrode region)
       gamma = (1 - eta_b)/(1 + eta_b)

Notation here: we restrict to a binary symmetric electrolyte z1 = +z, z2 = -z,
equal ion size a1 = a2 = a, bulk density c0 in both species. We use
symmetric BC V_- = -V, V_+ = +V (so the system has odd symmetry in phi and
even/odd symmetry in c+/c-).

The MFMT hard-sphere chemical potential is evaluated from the BMCSL /
Rosenfeld-style excess-Helmholtz density (Eq. 2.27) using the 1D weighted
densities (Eqs. 3.3-3.5). The Coulomb-correlation chemical potential is
the WKB form (Eq. 3.22) with x-dependent kappa(x).
"""

from __future__ import annotations

import dataclasses
from typing import Callable, Tuple

import numpy as np
from scipy.integrate import quad


# ---------------------------------------------------------------------------
# Geometry / discretization
# ---------------------------------------------------------------------------


@dataclasses.dataclass
class Geometry:
    """Dimensionless 1D slab geometry as in Sec. 3.

    Domain: x in [-1, 1].
    Ion-accessible region: |x| <= 1 - a.
    Stern layer: 1 - a < |x| < 1 (in the original equations the Stern
    layers are absorbed into the Robin BC; we therefore solve only on the
    ion-accessible region).
    """

    a: float           # dimensionless ion radius
    N: int             # number of integer grid points in [-1+a, 1-a]
    eta_s: float = 1.0 # Stern-layer dielectric (relative); paper uses 1

    def grids(self):
        """Return (x_half, x_int, h) following Sec. 3.3 notation.

        We use N+1 cell-centred ("half") nodes from -(1-a) to (1-a)
        (paper's x_{n+1/2}, n=0..N) and N "integer" nodes between them.
        For Poisson we just solve on uniform N+1 nodes including
        endpoints (Robin BC).
        """
        L = 1.0 - self.a
        N = self.N
        x = np.linspace(-L, L, N + 1)
        h = x[1] - x[0]
        return x, h


# ---------------------------------------------------------------------------
# MFMT hard-sphere chemical potential (1D, equal ion radii a)
# ---------------------------------------------------------------------------


def weighted_densities_1d(c_sum: np.ndarray, c_vec_sum: np.ndarray | None,
                          x: np.ndarray, a: float) -> dict:
    """Compute the four scalar + one (1-component) vector weighted densities
    used in MFMT for a 1D inhomogeneous geometry.

    For a 1D problem with planar symmetry the 3D MFMT weights reduce to:
        n3(x) = int_{x-a}^{x+a} c(x') * pi * (a^2 - (x'-x)^2) dx'
        n2(x) = int_{x-a}^{x+a} c(x') * 2*pi*a dx'   (surface area of disk)
              = 2*pi*a * int_{x-a}^{x+a} c(x') dx'
        n1(x) = n2(x) / (4*pi*a)
        n0(x) = n2(x) / (4*pi*a^2)
        nV2(x) = 2*pi * int_{x-a}^{x+a} c(x') * (x' - x) dx'    (the only
                 surviving vector component; nV1 = nV2/(4*pi*a))

    See Roth (2010), J. Phys.: Condens. Matter 22, 063102 for the planar
    MFMT reduction, equivalent (up to normalization) to Eqs. (3.3)-(3.5)
    of Ma-Xu-Zhang.

    Inputs
    ------
    c_sum : array, shape (Nx,)
        Sum of ionic densities over species (rho_b(x) in MFMT language);
        for equal-size species this is what enters all weighted densities.
    c_vec_sum : ignored (kept for API symmetry; equal-size case identical)
    x : node positions
    a : ion radius

    Returns
    -------
    dict with keys 'n0', 'n1', 'n2', 'n3', 'nV1', 'nV2'.
    """
    Nx = x.size
    n3 = np.zeros(Nx)
    n2_int = np.zeros(Nx)       # int c dx'
    nV2_int = np.zeros(Nx)      # int c*(x'-x) dx'
    h = x[1] - x[0]

    # Pre-extend with zeros for evaluation near boundaries (ions cannot exist
    # outside the ion-accessible region; this gives the correct "wall"
    # behavior where the Stern layer truncates the integral).
    # Build a padded c on a larger grid that extends by ceil(a/h) on each side
    # with zeros.
    pad = int(np.ceil(a / h)) + 2
    x_pad = np.concatenate([x[0] + h * np.arange(-pad, 0),
                            x,
                            x[-1] + h * np.arange(1, pad + 1)])
    c_pad = np.concatenate([np.zeros(pad), c_sum, np.zeros(pad)])

    for i in range(Nx):
        xi = x[i]
        # Window x' in [xi-a, xi+a]
        mask = (x_pad >= xi - a - 1e-14) & (x_pad <= xi + a + 1e-14)
        xw = x_pad[mask]
        cw = c_pad[mask]
        if xw.size < 2:
            continue
        # Composite trapezoid on the windowed nodes
        dx = np.diff(xw)
        # n2_int = int c dx'
        n2_int[i] = np.sum(0.5 * (cw[:-1] + cw[1:]) * dx)
        # n3 = int c * pi*(a^2 - (x'-xi)^2) dx'
        kern3 = np.pi * (a * a - (xw - xi) ** 2)
        kern3 = np.clip(kern3, 0.0, None)
        integrand3 = cw * kern3
        n3[i] = np.sum(0.5 * (integrand3[:-1] + integrand3[1:]) * dx)
        # nV2_int = int c*(x'-xi) dx' (scaled by 2*pi*?, see normalization)
        integrand_v = cw * (xw - xi)
        nV2_int[i] = np.sum(0.5 * (integrand_v[:-1] + integrand_v[1:]) * dx)

    # Apply the geometric prefactors (planar slab MFMT, with the
    # normalization that recovers the bulk hard-sphere mu_HS formula).
    n2 = 2.0 * np.pi * a * n2_int
    n1 = n2 / (4.0 * np.pi * a)
    n0 = n2 / (4.0 * np.pi * a * a)
    nV2 = 2.0 * np.pi * nV2_int
    nV1 = nV2 / (4.0 * np.pi * a)

    return {"n0": n0, "n1": n1, "n2": n2, "n3": n3, "nV1": nV1, "nV2": nV2}


def mu_hs_mfmt(c_total: np.ndarray, x: np.ndarray, a: float) -> np.ndarray:
    """Hard-sphere excess chemical potential per species (equal-size case),
    using the modified FMT (Roth/Yu-Wu) excess Helmholtz density of
    Eq. (2.27) in Ma-Xu-Zhang. Returns mu^hs(x) (dimensionless, in units of
    k_B T) for one species; for the equal-size symmetric case both species
    have the same mu^hs.

    Implementation: compute the six weighted densities, then form the
    derivatives dPhi/dn_alpha, and convolve them with the same weights to
    obtain mu^hs(x) via:
        mu^hs(x) = sum_alpha int dx' (dPhi/dn_alpha)(x') * w_alpha(x-x')
    """
    nd = weighted_densities_1d(c_total, None, x, a)
    n0, n1, n2, n3 = nd["n0"], nd["n1"], nd["n2"], nd["n3"]
    nV1, nV2 = nd["nV1"], nd["nV2"]

    # Avoid singularities
    eps = 1e-12
    one_m = np.clip(1.0 - n3, eps, None)

    # Excess Helmholtz density f^hs (Eq. 2.27) -- not needed explicitly,
    # we only need its partial derivatives w.r.t. each n_alpha. Use the
    # standard Yu-Wu / modified-FMT derivative formulas (Roth 2010, Eqs.
    # 25-29; see also Yu & Wu 2002 JCP).
    #
    # dPhi/dn0 = -ln(1 - n3)
    # dPhi/dn1 = n2 / (1 - n3)
    # dPhi/dn2 = n1/(1-n3) + (n2^2 - nV2^2) * f3p_2(n3)
    # dPhi/dn3 = n0/(1-n3) + (n1*n2 - nV1*nV2)/(1-n3)^2
    #            + (n2^3 - 3 n2 nV2^2) * f3p_3(n3)
    # dPhi/dnV1 = -nV2/(1-n3)
    # dPhi/dnV2 = -nV1/(1-n3) - 6 n2 nV2 * f3p_2(n3) * (something) ...
    #
    # The modified-FMT (BMCSL) third-term derivative coefficients are
    # cleanest as:
    #   Phi3 = f3(n3) * (n2^3 - 3*n2*nV2.nV2),
    # with f3(n3) = [ n3 + (1-n3)^2 ln(1-n3) ] / (36*pi*n3^2*(1-n3)^2).
    # Then dPhi3/dn3 = f3'(n3) * (n2^3 - 3*n2*nV2.nV2), and the n2/nV2
    # derivatives are 3*n2^2*f3 and -6*n2*nV2*f3 respectively.
    #
    # As n3 -> 0, f3 -> 1/(24*pi) (Taylor series). Handle small-n3 limit
    # explicitly to avoid 0/0.

    def f3_of_n3(n3v):
        # Series for small n3: f3 -> 1/(24*pi) + n3/(36*pi) + ...
        out = np.empty_like(n3v)
        small = np.abs(n3v) < 1e-3
        big = ~small
        # Small-n3 expansion (keep 3 terms)
        out[small] = (1.0 / (24.0 * np.pi)
                      + n3v[small] / (36.0 * np.pi)
                      + n3v[small] ** 2 / (48.0 * np.pi))
        n3b = n3v[big]
        n3b_safe = np.clip(n3b, -10.0, 0.95)
        one_m_b = np.clip(1.0 - n3b_safe, 1e-8, None)
        out[big] = (n3b_safe + one_m_b ** 2 * np.log(one_m_b)) \
                   / (36.0 * np.pi * n3b_safe * n3b_safe * one_m_b ** 2)
        return out

    def df3_dn3(n3v):
        # Numerical derivative via central difference is safest, but we
        # can do analytic. Use finite difference for robustness.
        d = 1e-6
        return (f3_of_n3(np.clip(n3v + d, -0.5, 0.95)) -
                f3_of_n3(np.clip(n3v - d, -0.5, 0.95))) / (2 * d)

    f3 = f3_of_n3(n3)
    f3p = df3_dn3(n3)

    # Partial derivatives of total Phi w.r.t. weighted densities
    dPhi_dn0 = -np.log(one_m)
    dPhi_dn1 = n2 / one_m
    dPhi_dn2 = (n1 / one_m
                + (3.0 * n2 * n2 - 3.0 * nV2 * nV2) * f3)
    dPhi_dn3 = (n0 / one_m
                + (n1 * n2 - nV1 * nV2) / one_m ** 2
                + (n2 ** 3 - 3.0 * n2 * nV2 * nV2) * f3p)
    dPhi_dnV1 = -nV2 / one_m
    dPhi_dnV2 = -nV1 / one_m - 6.0 * n2 * nV2 * f3

    # Now convolve with the *same* weights but with sign flips on the
    # vector weights (because mu^hs_i(x) = int dx' dPhi/dn_alpha(x') *
    # w_alpha^i(x - x'); the vector weight is odd, so w_V(x'-x) = -w_V(x-x')).
    # In effect: vector terms get -1 on the convolution from the
    # antisymmetry of the kernel.
    Nx = x.size
    h = x[1] - x[0]
    pad = int(np.ceil(a / h)) + 2
    x_pad = np.concatenate([x[0] + h * np.arange(-pad, 0),
                            x,
                            x[-1] + h * np.arange(1, pad + 1)])

    def pad_field(f):
        return np.concatenate([np.zeros(pad), f, np.zeros(pad)])

    F0p = pad_field(dPhi_dn0)
    F1p = pad_field(dPhi_dn1)
    F2p = pad_field(dPhi_dn2)
    F3p = pad_field(dPhi_dn3)
    FV1p = pad_field(dPhi_dnV1)
    FV2p = pad_field(dPhi_dnV2)

    mu = np.zeros(Nx)
    a2 = a * a
    inv4pia = 1.0 / (4.0 * np.pi * a)
    inv4pia2 = 1.0 / (4.0 * np.pi * a2)
    pref_n2 = 2.0 * np.pi * a
    pref_v2 = 2.0 * np.pi

    for i in range(Nx):
        xi = x[i]
        mask = (x_pad >= xi - a - 1e-14) & (x_pad <= xi + a + 1e-14)
        xw = x_pad[mask]
        if xw.size < 2:
            continue
        dx = np.diff(xw)
        # Scalar weights (even kernels): the convolution of dPhi/dn_alpha
        # with w_alpha integrated over x'.
        # Recall: n_alpha(x) = int dx' c(x') * w_alpha^c(x' - x); but here
        # for mu^hs_i we convolve dPhi(x') with w_alpha^i(x' - x) where
        # the species-i weight equals the species-summed weight when
        # radii are equal.
        # Effective convolution kernels per alpha (radial integrals of 3D
        # weight functions over y, z) in planar geometry:
        #   w_3 (scalar) kernel = pi*(a^2 - (x'-x)^2)
        #   w_2 (scalar) kernel = 2*pi*a    (constant inside |x'-x|<=a)
        #   w_1 (scalar) kernel = 1/2       (= w2/(4*pi*a))
        #   w_0 (scalar) kernel = 1/(2a)    (= w2/(4*pi*a^2))
        #   wV2 (vector) kernel = 2*pi*(x'-x)
        #   wV1 (vector) kernel = (x'-x)/(2a)
        u = xw - xi
        kern3 = np.pi * np.clip(a2 - u * u, 0.0, None)
        kern2 = pref_n2 * np.ones_like(u)
        kern1 = 0.5 * np.ones_like(u)
        kern0 = (1.0 / (2.0 * a)) * np.ones_like(u)
        kernV2 = pref_v2 * u
        kernV1 = u / (2.0 * a)

        def trap_int(integrand):
            return np.sum(0.5 * (integrand[:-1] + integrand[1:]) * dx)

        mu[i] = (trap_int(F0p[mask] * kern0)
                 + trap_int(F1p[mask] * kern1)
                 + trap_int(F2p[mask] * kern2)
                 + trap_int(F3p[mask] * kern3)
                 - trap_int(FV1p[mask] * kernV1)
                 - trap_int(FV2p[mask] * kernV2))
    return mu


def mu_hs_bulk(c_bulk: float, a: float) -> float:
    """Bulk HS chemical potential for a single equal-size species at uniform
    density c_bulk (per species), with packing fraction phi = (4/3)*pi*a^3*
    rho_total. We return mu^hs in units of k_B T, for one species.

    For a single-component HS fluid the BMCSL/Carnahan-Starling result is
        mu^hs_CS = (8 phi - 9 phi^2 + 3 phi^3) / (1 - phi)^3
    For a symmetric binary mixture with equal sizes this becomes the same
    as the single-component CS at total packing.
    """
    rho_tot = 2.0 * c_bulk  # cation + anion
    phi = (4.0 / 3.0) * np.pi * (a ** 3) * rho_tot
    return (8.0 * phi - 9.0 * phi ** 2 + 3.0 * phi ** 3) / (1.0 - phi) ** 3


# ---------------------------------------------------------------------------
# Coulomb-correlation chemical potential via WKB (Eq. 3.22 of paper)
# ---------------------------------------------------------------------------


def u_el_wkb(kappa: float, a: float, gamma: float) -> float:
    """Convenience: rescaled electrostatic correlation energy at x=0."""
    return u_el_wkb_at_x(kappa, a, gamma, 0.0)


def _f1_of_omega(omega: float, kappa: float, a: float, gamma: float) -> float:
    """Eq. (3.19)-(3.20) helper f1(omega) with the eta_s=1 simplification.

    Numerically-stable form for large omega*a: factor out exp(2*omega*a).
    For omega*a large:
        (e2wa + gamma)/(e2wa - gamma) -> 1 + 2*gamma*e^{-2wa}/(1 - gamma*e^{-2wa})
    so the ratio is well-defined and tends to 1.
    """
    tau = np.sqrt(omega * omega + kappa * kappa)
    # Stable evaluation of (e2wa + gamma) / (e2wa - gamma)
    if 2.0 * omega * a < 700.0:
        e2wa = np.exp(2.0 * omega * a)
        ratio = (e2wa + gamma) / (e2wa - gamma)
    else:
        # exp(2wa) huge -> ratio ~ 1 + 2*gamma*exp(-2wa)
        ratio = 1.0 + 2.0 * gamma * np.exp(-2.0 * omega * a)
    num = omega - tau * ratio
    den = omega + tau * ratio
    if abs(den) < 1e-300:
        return 0.0
    return num / den


def u_el_wkb_at_x(kappa: float, a: float, gamma: float, x: float) -> float:
    """Rescaled electrostatic correlation energy at position x (-1+a <= x <= 1-a)
    for a homogeneous screening kappa. Implements Eq. (3.22) fully, with
    numerically-stable algebra (factor out the dominant growing exponential).
    """
    L = 1.0 - a
    if kappa < 1e-12:
        return 0.0

    def f2_of_t(t):
        if t <= 1.0:
            return _f1_of_omega(0.0, kappa, a, gamma)
        omega = kappa * np.sqrt(t * t - 1.0)
        return _f1_of_omega(omega, kappa, a, gamma)

    def integrand(t):
        f2 = f2_of_t(t)
        kt = kappa * t
        # Multiply numerator and denominator of Eq. (3.22) integrand by
        # f2 * exp(-2*kt*L) to keep exponentials bounded.
        # Original:
        #   num   = 2*f2*e^{-2kt L} - e^{2kt x} - e^{-2kt x}
        #   den   = e^{2kt L}/f2 - f2 e^{-2kt L}
        # Multiply both by f2*e^{-2kt L}:
        #   num'  = 2*f2^2*e^{-4kt L} - f2*(e^{2kt(x-L)} + e^{-2kt(x+L)})
        #   den'  = e^{-2kt(L-L)} - f2^2*e^{-4kt L} = 1 - f2^2*e^{-4kt L}
        # All exponentials have non-positive exponents for x in [-L, L].
        E1 = np.exp(-4.0 * kt * L)               # <= 1
        E2 = np.exp(2.0 * kt * (x - L))          # <= 1
        E3 = np.exp(-2.0 * kt * (x + L))         # <= 1
        f2sq = f2 * f2
        num_p = 2.0 * f2sq * E1 - f2 * (E2 + E3)
        den_p = 1.0 - f2sq * E1
        if abs(den_p) < 1e-300:
            return 0.0
        return num_p / den_p

    try:
        val, _ = quad(integrand, 1.0, np.inf, limit=200, epsabs=1e-10,
                      epsrel=1e-7)
    except Exception:
        val = 0.0
    return -kappa * (1.0 - val)


# ---- Cache for u_el_wkb_at_x tabulation ----
_UEL_CACHE: dict = {}


def _build_uel_table(a: float, gamma: float, x_grid: np.ndarray,
                     kappa_max: float = 30.0, n_kappa: int = 80) -> tuple:
    """Build a tabulation of u_el_wkb_at_x(kappa, a, gamma, x) on a
    (kappa, x)-grid for fast bilinear interpolation. Cached by (a, gamma,
    x_grid.tobytes()).
    """
    key = (a, gamma, kappa_max, n_kappa, x_grid.tobytes())
    if key in _UEL_CACHE:
        return _UEL_CACHE[key]
    kappa_grid = np.concatenate([[0.0],
                                 np.geomspace(1e-3, kappa_max, n_kappa - 1)])
    table = np.zeros((kappa_grid.size, x_grid.size))
    for i, kap in enumerate(kappa_grid):
        for j, xj in enumerate(x_grid):
            table[i, j] = u_el_wkb_at_x(kap, a, gamma, xj)
    out = (kappa_grid, table)
    _UEL_CACHE[key] = out
    return out


def _uel_lookup(kappa_arr: np.ndarray, x_grid: np.ndarray,
                a: float, gamma: float) -> np.ndarray:
    """Interpolate u_el(kappa(x), x) from the cached table; returns array
    of length len(x_grid) = len(kappa_arr).
    """
    kappa_grid, table = _build_uel_table(a, gamma, x_grid)
    # For each x-index j we interpolate over kappa.
    out = np.empty_like(kappa_arr)
    for j in range(kappa_arr.size):
        out[j] = np.interp(np.clip(kappa_arr[j], kappa_grid[0],
                                    kappa_grid[-1]),
                            kappa_grid, table[:, j])
    return out


def _uel_bulk_value(a: float, gamma: float, eps_param: float) -> float:
    """Reference bulk u_el (kappa = 1/eps, x = 0)."""
    return u_el_wkb_at_x(1.0 / eps_param, a, gamma, 0.0)


def mu_co_wkb(c_total: np.ndarray, x: np.ndarray, a: float, q: float,
              eps_param: float, gamma: float, z: float = 1.0) -> np.ndarray:
    """Coulomb-correlation chemical potential mu^co_i(x) via WKB.

    From paper Eq. (3.9):
        mu^co_i = (1/2) z_i^2 * q * [ ... ]
    where the bracket is the WKB self-correlation u_el (Eq. 3.22), and
    q = l_B / L is the dimensionless Bjerrum length.

    We use local kappa(x):
        kappa(x) = sqrt(I(x)) / eps      (Eq. 3.11 / 3.10)
    where I(x) = (c_+ + c_-)/2 (1:1 symmetric electrolyte). Then
        mu^co_i(x) = 0.5 * z_i^2 * q * (u_el(kappa(x), a, gamma; x) - u_bulk).
    Normalization sets mu^co = 0 in the bulk so the Boltzmann form
    c_i = exp(-z_i phi - mu^co - mu^hs) is consistent with bulk c = 1.
    """
    Ix = 0.5 * c_total
    kappa_x = np.sqrt(np.maximum(Ix, 0.0)) / eps_param
    u_loc = _uel_lookup(kappa_x, x, a, gamma)
    u_bulk = _uel_bulk_value(a, gamma, eps_param)
    return 0.5 * z * z * q * (u_loc - u_bulk)


# ---------------------------------------------------------------------------
# Poisson solve with Robin BC
# ---------------------------------------------------------------------------


def solve_poisson_robin(x: np.ndarray, rho: np.ndarray, eps_param: float,
                        a: float, V: float, eta_s: float = 1.0) -> np.ndarray:
    """Solve  -2*eps^2 * phi'' = rho(x)  on x in [-(1-a), 1-a] with Robin BC
        phi(-L)  -  (a/eta_s) * phi'(-L) = -V
        phi(+L)  +  (a/eta_s) * phi'(+L) = +V
    where L = 1 - a.

    Standard second-order finite-difference with one-sided derivatives at
    boundaries.
    """
    N = x.size - 1  # so we have N+1 unknowns phi_0..phi_N
    h = x[1] - x[0]
    A = np.zeros((N + 1, N + 1))
    b = np.zeros(N + 1)
    # Interior: -2*eps^2 * (phi_{i+1} - 2 phi_i + phi_{i-1})/h^2 = rho_i
    coef = -2.0 * eps_param ** 2 / (h * h)
    for i in range(1, N):
        A[i, i - 1] = coef
        A[i, i] = -2.0 * coef
        A[i, i + 1] = coef
        b[i] = rho[i]
    # Robin BC at i=0:  phi_0 - (a/eta_s) * (phi_1 - phi_0)/h = -V
    A[0, 0] = 1.0 + (a / eta_s) / h
    A[0, 1] = -(a / eta_s) / h
    b[0] = -V
    # Robin BC at i=N:  phi_N + (a/eta_s) * (phi_N - phi_{N-1})/h = +V
    A[N, N] = 1.0 + (a / eta_s) / h
    A[N, N - 1] = -(a / eta_s) / h
    b[N] = +V

    phi = np.linalg.solve(A, b)
    return phi


# ---------------------------------------------------------------------------
# Equilibrium mPB solver
# ---------------------------------------------------------------------------


@dataclasses.dataclass
class mPBParams:
    eps: float          # dimensionless Debye/half-gap
    q: float            # dimensionless Bjerrum/half-gap (only needed for LC scaling)
    a: float            # dimensionless ion radius
    V: float            # +- boundary potential
    eta_s: float = 1.0
    gamma: float = 0.0   # dielectric mismatch (LC, LS)
    model: str = "MF"    # one of MF, SC, LC, LS
    N: int = 200
    tol: float = 1e-8
    max_iter: int = 500
    damping: float = 0.1 # Picard damping factor (densities)
    phi_damping: float = 0.3  # Picard damping for potential
    enforce_neutrality: bool = True
    voltage_steps: int = 1    # voltage continuation steps for hard problems
    canonical: bool = True    # if True, rescale c+,c- to preserve mass
                              # (canonical ensemble; no chemical-potential offset)


def solve_mpb(p: mPBParams, c_init: Tuple[np.ndarray, np.ndarray] | None = None,
              verbose: bool = False):
    """Solve equilibrium mPB system iteratively.

    Uses damped Picard iteration with separate damping for densities and
    potential. When `canonical=True` (default), at each step the densities
    are normalized so that the integral over the ion-accessible region equals
    `2*(1-a)`, i.e. enforcing mass conservation (no-flux BC at equilibrium
    implies total ionic content is conserved). When `voltage_steps > 1`, we
    ramp V from 0 to p.V over multiple sub-problems using continuation.

    Returns: dict with keys
        'x', 'c_plus', 'c_minus', 'phi', 'mu_hs', 'mu_co', 'residuals',
        'iter', 'converged', 'params'.
    """
    geom = Geometry(a=p.a, N=p.N, eta_s=p.eta_s)
    x, h = geom.grids()
    L_acc = 2.0 * (1.0 - p.a)  # length of ion-accessible region

    if c_init is None:
        c_plus = np.ones_like(x)
        c_minus = np.ones_like(x)
    else:
        c_plus, c_minus = c_init[0].copy(), c_init[1].copy()

    phi = np.zeros_like(x)
    residuals = []
    converged = False
    it_total = 0

    # Continuation in V
    V_targets = np.linspace(p.V / p.voltage_steps, p.V, p.voltage_steps)

    for V_cur in V_targets:
        if verbose and p.voltage_steps > 1:
            print(f"  [continuation] V = {V_cur:.3f}")
        for it in range(p.max_iter):
            # ------ Excess chemical potentials ------
            c_tot = c_plus + c_minus
            if p.model in ("SC", "LS"):
                mu_hs_full = mu_hs_mfmt(c_tot, x, p.a)
                mu_hs_bulk_val = mu_hs_bulk(1.0, p.a)
                mu_hs = mu_hs_full - mu_hs_bulk_val
            else:
                mu_hs = np.zeros_like(x)

            if p.model in ("LC", "LS"):
                mu_co = mu_co_wkb(c_tot, x, p.a, p.q, p.eps, p.gamma, z=1.0)
            else:
                mu_co = np.zeros_like(x)

            # ------ Poisson ------
            rho = (+1.0) * c_plus + (-1.0) * c_minus
            phi_solve = solve_poisson_robin(x, rho, p.eps, p.a, V_cur,
                                            eta_s=p.eta_s)
            phi_new = (1.0 - p.phi_damping) * phi + p.phi_damping * phi_solve

            # ------ Boltzmann update ------
            U_plus = (+1.0) * phi_new + mu_co + mu_hs
            U_minus = (-1.0) * phi_new + mu_co + mu_hs
            U_plus = np.clip(U_plus, -50.0, 50.0)
            U_minus = np.clip(U_minus, -50.0, 50.0)
            # Log-space damping is far more stable than linear damping when
            # c spans many orders of magnitude. We update log(c) by a damped
            # step of (-U) toward log(c_new) = -U, then clip log(c) to avoid
            # overshoots that send the iteration into a non-physical basin.
            log_c_plus = np.log(np.clip(c_plus, 1e-50, None))
            log_c_minus = np.log(np.clip(c_minus, 1e-50, None))
            log_c_plus_new = -U_plus
            log_c_minus_new = -U_minus
            log_cp_upd = (1.0 - p.damping) * log_c_plus + p.damping * log_c_plus_new
            log_cm_upd = (1.0 - p.damping) * log_c_minus + p.damping * log_c_minus_new
            # Hard ceiling on local density growth per step (factor 1.3 max
            # in linear scale per Picard sweep). This trades convergence speed
            # for robustness against MFMT-driven spikes.
            step_cap = np.log(1.3)
            log_cp_upd = np.minimum(log_cp_upd, log_c_plus + step_cap)
            log_cm_upd = np.minimum(log_cm_upd, log_c_minus + step_cap)
            log_cp_upd = np.maximum(log_cp_upd, log_c_plus - step_cap)
            log_cm_upd = np.maximum(log_cm_upd, log_c_minus - step_cap)
            # Cap absolute log(c) at [-25, log(10)] (densities at most 10x bulk).
            log_cp_upd = np.clip(log_cp_upd, -25.0, np.log(10.0))
            log_cm_upd = np.clip(log_cm_upd, -25.0, np.log(10.0))
            c_plus_upd = np.exp(log_cp_upd)
            c_minus_upd = np.exp(log_cm_upd)

            # Canonical normalization: rescale so that ion content equals
            # the bulk value (closed system, no-flux BC).
            if p.canonical:
                int_p = np.trapezoid(c_plus_upd, dx=h)
                int_m = np.trapezoid(c_minus_upd, dx=h)
                if int_p > 0:
                    c_plus_upd *= L_acc / int_p
                if int_m > 0:
                    c_minus_upd *= L_acc / int_m

            res = max(np.max(np.abs(c_plus_upd - c_plus)),
                      np.max(np.abs(c_minus_upd - c_minus)),
                      np.max(np.abs(phi_new - phi)))
            residuals.append(float(res))
            c_plus, c_minus, phi = c_plus_upd, c_minus_upd, phi_new
            it_total += 1

            if verbose and (it < 5 or it % 50 == 0):
                print(f"    iter {it:4d}  res = {res:.3e}")

            if res < p.tol:
                converged = True
                break
        if not converged and V_cur < V_targets[-1] - 1e-12:
            # Soft-fail this continuation step but keep going
            pass

    # Final chemical potentials for reporting
    c_tot = c_plus + c_minus
    if p.model in ("SC", "LS"):
        mu_hs = mu_hs_mfmt(c_tot, x, p.a) - mu_hs_bulk(1.0, p.a)
    else:
        mu_hs = np.zeros_like(x)
    if p.model in ("LC", "LS"):
        mu_co = mu_co_wkb(c_tot, x, p.a, p.q, p.eps, p.gamma, z=1.0)
    else:
        mu_co = np.zeros_like(x)

    return {
        "x": x,
        "c_plus": c_plus,
        "c_minus": c_minus,
        "phi": phi,
        "mu_hs": mu_hs,
        "mu_co": mu_co,
        "residuals": np.array(residuals),
        "iter": it_total,
        "converged": converged,
        "params": dataclasses.asdict(p),
    }


# ---------------------------------------------------------------------------
# Diagnostics
# ---------------------------------------------------------------------------


def diffuse_charge(x: np.ndarray, c_plus: np.ndarray,
                   c_minus: np.ndarray) -> float:
    """Total diffuse charge in the left half (Eq. 3.16)."""
    h = x[1] - x[0]
    mask = x < 0
    rho = c_plus - c_minus
    # Trapezoid on the masked region
    rho_l = rho[mask]
    return float(np.trapezoid(rho_l, dx=h))


def mass_conservation(x: np.ndarray, c: np.ndarray, target: float = 2.0) -> float:
    """Total integral of c over [-(1-a), 1-a]; target = 2*(1-a) for uniform c=1."""
    h = x[1] - x[0]
    return float(np.trapezoid(c, dx=h))
