"""
Track-Event Theory (TET) and RAMN core equations.
Reproduces the analytical claims of Ngcezu & Rabus (2021),
Radiat Environ Biophys 60:559-578.

All equations are numbered to match the paper.
"""
from __future__ import annotations
import numpy as np
from dataclasses import dataclass


# ----- Fundamental TET (cellular-level) -----

def survival_tet(D, p, q):
    """Eq. 9: S = (1 + qD) exp(-(p+q)D).
    p, q in Gy^-1; D in Gy."""
    D = np.asarray(D, dtype=float)
    return (1.0 + q * D) * np.exp(-(p + q) * D)


def survival_tet_lq_lowdose(D, p, q):
    """Low-dose limit of Eq. 9 expanded to second order in D:
        S ≈ exp(-α D - β D²), α=p, β=q²/2.
    The paper notes Eq. 9 is equivalent to the LQ model in this limit
    (Besserer & Schneider 2015a)."""
    D = np.asarray(D, dtype=float)
    alpha = p
    beta = 0.5 * q * q
    return np.exp(-alpha * D - beta * D * D)


def survival_tet_repair(D, p, q, R):
    """Eq. 15 (this paper's corrected repair model, derived from Eqs. 14 + 6 + 8).
        S = {1 + qD + R[pD + (qD)^2 / 2]} exp(-(p+q)D)
    R is the repair probability for cells with two sublethal lesions / one
    potentially-lethal lesion."""
    D = np.asarray(D, dtype=float)
    return (1.0 + q * D + R * (p * D + 0.5 * (q * D) ** 2)) * np.exp(-(p + q) * D)


def survival_besserer_schneider_2015b_repair(D, p, q, R):
    """Reconstruction of Eq. 7 of Besserer & Schneider (2015b), which the
    present paper claims is *inconsistent* with the TET assumptions and contains
    extra mixed (p×q) and R^2 D^3 terms.

    Reference reconstructed from the present paper's Discussion of B&S 2015b:
    the prefactor is a polynomial up to cubic in D and quadratic in R; the
    headline difference vs. Eq. 15 is the presence of (i) a p*q*D^2 mixed term
    and (ii) a (qD)^3 R^2 cubic term.

    The full B&S 2015b expression (from their paper) is:
        S_BS = {1 + qD + R[pD + (qD)^2/2 + p q D^2]
                       + R^2 [ (q D)^3 / 6 ]} * exp(-(p+q)D)

    (See present paper, Subsection "Critical observations on the TET model with repair".)
    """
    D = np.asarray(D, dtype=float)
    pref = (1.0
            + q * D
            + R * (p * D + 0.5 * (q * D) ** 2 + p * q * D ** 2)
            + R * R * ((q * D) ** 3 / 6.0))
    return pref * np.exp(-(p + q) * D)


def survival_alt_single_R(D, p, q, R):
    """Eq. 22: S' = R + (1-R)(1+qD) exp(-(p+q)D)."""
    D = np.asarray(D, dtype=float)
    base = (1.0 + q * D) * np.exp(-(p + q) * D)
    return R + (1.0 - R) * base


# ----- N-target (RAMN) form -----

def survival_ramn_Ntargets(D, p_sl_per_gy, p_cl_per_gy, N):
    """Eq. 11: S = (1 + nt pSL)^N · exp(-N nt (pSL + pCL)).

    For numerical convenience we work in `dose` parameterisation directly:
    define u = nt pSL (per Gy) and v = nt pCL (per Gy).  Then S = (1+uD)^N exp(-N(u+v)D).

    Parameters
    ----------
    D : array of doses [Gy]
    p_sl_per_gy : mean SLs per Gy per CV summed over all interacting tracks (= nt pSL / D)
    p_cl_per_gy : mean CLs per Gy per CV
    N           : number of CVs in the cell

    With u·N ≡ q (Gy^-1, sublethal model parameter) and v·N ≡ p (Gy^-1, lethal),
    Eq. 11 should reduce, in the large-N limit (Eq. 12), to Eq. 13 below.
    """
    D = np.asarray(D, dtype=float)
    u = p_sl_per_gy
    v = p_cl_per_gy
    log_prefactor = N * np.log1p(u * D)            # log[(1+uD)^N], stable
    log_exp = -N * (u + v) * D                     # exp(-N(u+v)D)
    return np.exp(log_prefactor + log_exp)


def survival_ramn_largeN_approx(D, p_sl_per_gy, p_cl_per_gy, N):
    """Eq. 13: large-N approximation of Eq. 11.

        S ≈ exp[ -pD - (qD)^2 / (2N) ]
    where p = N v  and  q = N u  (Eq. 8 with the numerators replaced as the
    paper notes).
    """
    D = np.asarray(D, dtype=float)
    u = p_sl_per_gy
    v = p_cl_per_gy
    p = N * v
    q = N * u
    return np.exp(-p * D - (q * D) ** 2 / (2.0 * N))


# ----- Single-track conditional probabilities in a CV (corrected by this paper) -----

def psl_pcl_corrected(F2, n, nt):
    """Eqs. 27, 28: this paper's corrected single-track conditional probabilities.

        PSL ≈ F2 · n
        PCL ≈ nt · n · (n-1) · F2^2
    """
    PSL = F2 * n
    PCL = nt * n * (n - 1) * F2 * F2
    return PSL, PCL


def psl_pcl_schneider_naive(F2, n):
    """Schneider et al. (2019, 2020) naive binomial expressions for comparison:
        PSL_naive = n · F2 · (1 - F2)^(n-1)
        PCL_naive = 1 - (1 - F2)^n - PSL_naive
    These ignore the conditional nature of F2 (no nt factor)."""
    PSL = n * F2 * (1.0 - F2) ** (n - 1)
    PCL = 1.0 - (1.0 - F2) ** n - PSL
    return PSL, PCL


# ----- DSB-from-IC combinatorial probability (Eq. 31) -----

def p_dsb_given_ic(F_k_array):
    """Eq. 31:  P(DSB|IC) = (1/F2) Σ_{k≥2} F_k / 2^(k-1).

    F_k_array : 1D array with F_k for k = 2, 3, 4, ...
    """
    F_k = np.asarray(F_k_array, dtype=float)
    F2 = F_k[0]
    if F2 == 0.0:
        return 0.0
    ks = np.arange(2, 2 + len(F_k))
    weights = 1.0 / (2.0 ** (ks - 1))
    return float(np.sum(weights * F_k) / F2)


# ----- "How big is the quadratic correction?" helper -----

def quadratic_correction_dose_for_unit(q_per_gy: float, N: float) -> float:
    """Returns D* such that (q D*)^2 / (2 N) = 1, i.e. the dose at which
    the quadratic correction in Eq. 13 reaches unity.
    Paper claim: with q = 40 Gy^-1 and N = 5e8 CVs, D* ≈ 500 Gy (order of magnitude).
    """
    return np.sqrt(2.0 * N) / q_per_gy


if __name__ == "__main__":
    # Sanity ping
    D = np.linspace(0, 10, 11)
    print("S_TET(D) at p=0.1, q=0.05:", survival_tet(D, 0.1, 0.05))
    print("D* for (q=40, N=5e8) =", quadratic_correction_dose_for_unit(40.0, 5e8), "Gy")
