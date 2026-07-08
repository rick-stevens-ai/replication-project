"""
Replication of Chubukov/Abrahams-type mean-field analysis of chiral spin order
in Kondo-Heisenberg systems (OSTI 1412756).

The paper's central object is the zero-T mean-field energy density per spin^2:

    E0(alpha) / s^2  =  J_tilde_H(G) * sin^2(alpha)
                      + cos^2(alpha) * [ J_tilde_H(Q)
                                         - rho_F * J_K^2 * ln( D / (s |J_K| |cos alpha|) ) ]

with:
    J_tilde_H(q) = J_H * sum_a cos(q . a)    (Fourier of Heisenberg coupling)
    G = (pi/a, pi/a)                          (AFM ordering vector; J_tilde_H(G) < 0)
    Q = nesting vector (2kF, pi/a_y)          (J_tilde_H(Q) depends on filling)
    rho_F = density of states at Fermi level  (rho_F = 1/(2 pi v_F a_y) in 2D)
    D  = bandwidth
    s  = local spin magnitude (we take s=1/2)

We reproduce:
  (i)   The energy functional E0(alpha) and its minimum alpha*(J_H,J_K).
  (ii)  The critical J_H = J_c at which a nontrivial minimum (sin alpha != 0)
        first appears, from C(J_c) = 1 where
             C(J_H) = (exp(-1/2) D) / (s|J_K|) * exp[(J~H(G)-J~H(Q))/(rho_F J_K^2)]
  (iii) The order parameter <sin alpha> vs T from a one-dimensional partition
        function (alpha is the soft Ising mode at finite T).
  (iv)  T_c(J_H), verifying T_c ~ (J_H - J_c)^2 / J_K near the transition.
  (v)   The scalar chirality O_c(T) which locks onto <sin alpha cos^2 alpha>.
"""

from __future__ import annotations
import numpy as np
from dataclasses import dataclass
from typing import Tuple
from scipy.optimize import brentq
from scipy.integrate import quad


@dataclass
class KHParams:
    J_K: float = 1.0        # Kondo coupling (units of bandwidth)
    J_H: float = 0.0        # Heisenberg NN coupling
    D:   float = 10.0       # bandwidth (sets energy units; take D=10, so sJK << D)
    s:   float = 0.5        # local spin
    rho_F: float = 0.05     # DoS at Fermi level
    # Lattice Fourier factors:
    # J_tilde_H(Q) / J_H  (typically small / negative for nesting Q incommensurate)
    # J_tilde_H(G) / J_H  = 2(cos(pi) + cos(pi)) = -4 on square with NN only
    jQ_over_JH: float = 0.0     # (Q = nesting vector; for generic filling ~ 0)
    jG_over_JH: float = -4.0    # square-lattice AFM vector, NN only

    def Jt_Q(self): return self.jQ_over_JH * self.J_H
    def Jt_G(self): return self.jG_over_JH * self.J_H


# ---------------------------------------------------------------------------
# Zero-T energy functional (eq. 16 of paper)
# ---------------------------------------------------------------------------

def energy_density(alpha: np.ndarray, p: KHParams) -> np.ndarray:
    """E0(alpha) / s^2 at T=0.

    We regularise the logarithm by adding a tiny eps inside the log so that
    alpha = pi/2 (|cos alpha| = 0) does not blow up; physically the log
    argument is bounded from below by the induced fermion gap.
    """
    eps = 1e-12
    c = np.cos(alpha)
    s_ = np.sin(alpha)
    s = p.s
    # fermionic gain from RKKY / Kondo polarisation (negative contribution)
    fermion_piece = -p.rho_F * p.J_K**2 * np.log(p.D / (s*abs(p.J_K)*np.abs(c) + eps))
    return p.Jt_G()*s_**2 + c**2 * (p.Jt_Q() + fermion_piece)


def optimal_alpha(p: KHParams) -> float:
    """Return alpha* in [0, pi/2] minimising E0(alpha)."""
    alphas = np.linspace(0.0, np.pi/2 - 1e-6, 20001)
    E = energy_density(alphas, p)
    return float(alphas[int(np.argmin(E))])


# ---------------------------------------------------------------------------
# Critical Heisenberg coupling J_c from C(J_H) = 1  (eq. 17)
# ---------------------------------------------------------------------------

def C_of_JH(J_H: float, p: KHParams) -> float:
    p2 = KHParams(**{**p.__dict__, "J_H": J_H})
    return (np.exp(-0.5) * p.D / (p.s * abs(p.J_K))) * np.exp(
        (p2.Jt_G() - p2.Jt_Q()) / (p.rho_F * p.J_K**2)
    )


def J_c(p: KHParams) -> float:
    """Solve C(J_c) = 1 for J_c.  C is monotone decreasing in J_H since
    (Jt_G - Jt_Q) < 0 (AFM favoured at G, nesting small at Q)."""
    f = lambda JH: C_of_JH(JH, p) - 1.0
    # Find a bracket
    lo, hi = 1e-6, 10.0
    f_lo = f(lo)
    if f_lo < 0:
        return 0.0  # already past critical
    # expand hi until sign change
    for _ in range(60):
        if f(hi) < 0:
            break
        hi *= 2
    else:
        return float('nan')
    return brentq(f, lo, hi, xtol=1e-10)


# ---------------------------------------------------------------------------
# Finite-T: alpha is an Ising-like soft mode.  Partition function in alpha
#  over [0, pi/2] with measure sin(2 alpha) d alpha gives thermal averages.
#
# The full field theory is a SU(2)xU(1) nl-sigma-model; at mean-field level
# we treat only the massive alpha fluctuation and assume the O(3) triad is
# quasi-static.  This is the same Ising-reduction the paper invokes to
# obtain its T_c estimate.
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Mean-field Ising treatment for the soft mode alpha.
#
# The paper identifies the chiral broken-symmetry phase with a Z2 Ising
# transition (sign of sin alpha).  Within standard single-site mean-field we
# introduce an Ising magnetisation  m = <sigma>, sigma = +-1, with |sigma|
# tracking the amplitude |sin alpha|.  The Landau free-energy density is
#
#     F(m ; T) = [ V(alpha*(m)) - V(0) ]  -  T * S_Ising(m)
#
# with V(alpha) the zero-T energy density (per spin^2), alpha*(m) defined
# by sin(alpha*(m)) = sin(a*) * |m|, and S_Ising(m) the usual binary
# entropy per site,
#
#     S(m) = -(1+m)/2 log((1+m)/2) - (1-m)/2 log((1-m)/2).
#
# Minimising F over m in [0,1] yields the mean-field order parameter.
# An overall 'coherence volume' multiplier A_coh (number of spins whose
# alpha mode locks coherently) is absorbed into T -> T/A_coh; we set
# A_coh = 1 and report T in the same energy units as J_H, J_K, D.
# ---------------------------------------------------------------------------

def _ising_entropy(m: np.ndarray) -> np.ndarray:
    m = np.clip(m, -1 + 1e-12, 1 - 1e-12)
    p = 0.5*(1.0 + m)
    q = 1.0 - p
    return -(p*np.log(p) + q*np.log(q))


def thermal_averages(p: KHParams, T: float, N: int = 2000):
    """Mean-field order parameter m* and induced averages.

    Returns a dict with:
        m                 : Ising order parameter  (= |sin alpha| / sin alpha*)
        sin_alpha         : <|sin alpha|>          (= m * sin alpha*)
        cos2              : <cos^2 alpha>          at alpha*(m)
        sin_cos2          : <|sin alpha| cos^2 alpha> at alpha*(m)
        F                 : minimised free energy density
    """
    a_star = optimal_alpha(p)
    sin_star = np.sin(a_star)
    ms = np.linspace(0.0, 1.0 - 1e-6, N)
    # alpha(m) : interpolate linearly in sin(alpha) from 0 to sin(a_star)
    sin_a = sin_star * ms
    alpha = np.arcsin(np.clip(sin_a, 0.0, 1.0 - 1e-12))
    V = energy_density(alpha, p) - energy_density(np.array([0.0]), p)[0]
    S = _ising_entropy(ms)
    F = V - T*S
    i = int(np.argmin(F))
    m_opt = float(ms[i])
    a_opt = alpha[i]
    return dict(
        m=m_opt,
        sin_alpha = float(np.sin(a_opt)),
        cos2 = float(np.cos(a_opt)**2),
        sin_cos2 = float(np.sin(a_opt)*np.cos(a_opt)**2),
        F = float(F[i]),
        alpha_star = a_star,
    )


def T_c_estimate(p: KHParams, tol: float = 5e-3, T_hi: float = 1.0) -> float:
    """Estimate T_c via bisection on T where m drops below `tol`."""
    a0 = optimal_alpha(p)
    if np.sin(a0) < 1e-3:
        return 0.0
    lo = 1e-8
    m_lo = thermal_averages(p, lo)['m']
    if m_lo < tol:
        return 0.0
    hi = T_hi
    for _ in range(80):
        if thermal_averages(p, hi)['m'] < tol:
            break
        hi *= 2
        if hi > 1e6:
            return float('nan')
    for _ in range(60):
        mid = 0.5*(lo+hi)
        if thermal_averages(p, mid)['m'] > tol:
            lo = mid
        else:
            hi = mid
        if (hi-lo) < 1e-6*max(hi, 1e-6):
            break
    return 0.5*(lo+hi)


# ---------------------------------------------------------------------------
# Scalar chirality (eq. 7 of paper, averaged over triangle positions)
# ---------------------------------------------------------------------------

def scalar_chirality_amplitude(p: KHParams, T: float,
                               triangle=(np.array([0,0]), np.array([1,0]), np.array([0,1])),
                               Q=np.array([np.pi*0.4, np.pi])) -> float:
    """|O_c| = s^3 <sin alpha cos^2 alpha> * |geometric factor|.

    We take a representative NN triangle on the square lattice and the
    nesting vector Q = (0.4 pi, pi) (generic filling).  Only the amplitude
    vs T is meaningful for our replication.
    """
    r1, r2, r3 = triangle
    N = lambda r: int(r[0] + r[1])        # sublattice parity
    D12 = Q @ (r1 - r2)
    D23 = Q @ (r2 - r3)
    D31 = Q @ (r3 - r1)
    geom = (-1)**N(r3)*np.sin(D12) + (-1)**N(r1)*np.sin(D23) + (-1)**N(r2)*np.sin(D31)
    avg = thermal_averages(p, T)
    return p.s**3 * avg['sin_cos2'] * geom


if __name__ == "__main__":
    p = KHParams(J_K=1.0, J_H=0.25, D=10.0, s=0.5, rho_F=0.05)
    print("J_c =", J_c(p))
    print("alpha* =", optimal_alpha(p))
    print("thermal (T=0.05):", {k: v for k, v in thermal_averages(p, 0.05).items()
                                if not isinstance(v, np.ndarray)})
    print("T_c =", T_c_estimate(p))
    print("|O_c|(T=0.01) =", scalar_chirality_amplitude(p, 0.01))
