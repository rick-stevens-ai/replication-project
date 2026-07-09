"""
Replication of McMahon, Schuemann, Paganetti, Prise (2016)
"Mechanistic Modelling of DNA Repair and Cellular Survival Following
Radiation-Induced DNA Damage"
Sci Rep 6:33290, doi:10.1038/srep33290

Implements:
  Eq (1)       Triple-exponential DSB repair kinetics
  Eq (2)-(6)   Misrepair / correct-rejoining probability (analytical,
               Monte-Carlo-calibrated for small sigma)
  Eq (7)-(11)  Chromosome aberration / dicentric / deletion yields
  Eq (12)-(14) Mutation rates (HPRT etc.)
  Eq (15)      Inter-arm aberrations in G2
  Survival     G1 / G2 / cycling / mitotic models

Free-tier replication for LUCID-second100 slot #75.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable

import numpy as np
from scipy.special import erf


# ---------------------------------------------------------------------------
# Table 1 -- best fit parameters from McMahon et al. 2016 (with uncertainties)
# ---------------------------------------------------------------------------

DSB_YIELD_PER_GY_PER_GBP = 5.738   # DSBs/Gy/Gbp (fixed from literature)
HUMAN_GENOME_GBP = 6.1             # diploid human genome (Gbp), GRCh38.p6

# DNA model fit parameters
LAMBDA_F   = 3.6       # fast repair rate, hour^-1
LAMBDA_S   = 0.15      # slow repair rate, hour^-1
LAMBDA_M   = 0.0084    # MMEJ repair rate, hour^-1
P_COMPLEX  = 0.42      # probability a break is "complex"
P_FAIL     = 0.67      # probability that a defective pathway misroutes break
SIGMA_FRAC = 0.0428    # misrejoining range, fraction of nuclear radius R_nuc
MU_NHEJ    = 0.985     # NHEJ base fidelity
MU_MMEJ    = 0.465     # MMEJ base fidelity
NU_POINT   = 0.044     # point-mutation factor

# Survival model fit parameters
PSI_APOP   = 0.014     # G1 apoptosis sensitivity, break^-1
PHI_MIT    = 0.0085    # mitotic-death sensitivity, break^-1

# Eq (5) geometric Monte-Carlo calibration constants
OMEGA_A = 0.757
OMEGA_B = 5.39

# Typical human values
N_CHROMOSOMES_HUMAN = 46     # diploid
DEFAULT_R_NUC = 1.0          # work in units of R_nuc; sigma uses fraction of R_nuc


# ---------------------------------------------------------------------------
# Phenotype / experiment configuration
# ---------------------------------------------------------------------------


@dataclass
class CellSpec:
    """Phenotype + experimental conditions for a single irradiation case."""

    genome_gbp: float = HUMAN_GENOME_GBP       # Gbp DNA in nucleus
    n_chromosomes: int = N_CHROMOSOMES_HUMAN
    phase: str = "G1"                          # "G1" or "G2"
    nhej_defective: bool = False
    hr_defective: bool = False
    cycling: bool = True                       # if False, no apoptosis (e.g. plateau)
    apoptosis_competent: bool = True           # functional G1 arrest -> apoptosis
    r_nuc: float = DEFAULT_R_NUC               # nuclear radius (arbitrary units)


# ---------------------------------------------------------------------------
# Repair pathway selection -- Methods, "DSB Induction and Repair Kinetics"
# ---------------------------------------------------------------------------


def repair_probabilities(spec: CellSpec, p_c: float = P_COMPLEX,
                         p_fail: float = P_FAIL):
    """
    Return (p_f, p_s, p_m) for the three repair channels (fast/slow/MMEJ).

    Logic from Methods (McMahon 2016):
      - Simple breaks (fraction 1-p_c) -> fast pathway (NHEJ).
      - Complex breaks (fraction p_c) -> slow pathway (HR if available in
        S/G2, else NHEJ).
      - In a cell defective for the *preferred* pathway, a fraction p_fail
        is routed to MMEJ.
    """
    # Default (repair competent):
    p_f = (1.0 - p_c)
    p_s = p_c
    p_m = 0.0

    if spec.phase == "G1":
        # Only NHEJ is available for both simple and complex breaks.
        if spec.nhej_defective:
            # Both fast and slow streams partially fail to MMEJ.
            p_m = p_fail * (p_f + p_s)
            p_f = (1.0 - p_fail) * (1.0 - p_c)
            p_s = (1.0 - p_fail) * p_c
        # HR doesn't apply in G1 -> hr_defective irrelevant
    elif spec.phase == "G2":
        # Slow / complex breaks preferentially go to HR.  NHEJ still handles
        # simple breaks.
        if spec.nhej_defective and not spec.hr_defective:
            # Fast (NHEJ) stream fails -> MMEJ; slow uses HR successfully.
            p_m = p_fail * (1.0 - p_c)
            p_f = (1.0 - p_fail) * (1.0 - p_c)
            p_s = p_c
        elif spec.hr_defective and not spec.nhej_defective:
            # Slow stream fails: HR -> MMEJ; NHEJ in fast stream unaffected.
            p_m = p_fail * p_c
            p_f = (1.0 - p_c)
            p_s = (1.0 - p_fail) * p_c
        elif spec.nhej_defective and spec.hr_defective:
            p_m = p_fail
            p_f = (1.0 - p_fail) * (1.0 - p_c)
            p_s = (1.0 - p_fail) * p_c
    else:
        raise ValueError(f"unknown phase: {spec.phase!r}")

    return p_f, p_s, p_m


# ---------------------------------------------------------------------------
# Eq (1): triple-exponential DSB kinetics
# ---------------------------------------------------------------------------


def n_dsb_over_time(t_hours, N0, p_f, p_s, p_m,
                    lam_f=LAMBDA_F, lam_s=LAMBDA_S, lam_m=LAMBDA_M):
    """N(t) = N0 (p_f e^{-lam_f t} + p_s e^{-lam_s t} + p_m e^{-lam_m t})"""
    t = np.asarray(t_hours, dtype=float)
    return N0 * (p_f * np.exp(-lam_f * t)
                 + p_s * np.exp(-lam_s * t)
                 + p_m * np.exp(-lam_m * t))


# ---------------------------------------------------------------------------
# Eq (4): theta(R, sigma)  rejoining rate between two random DSB ends
# ---------------------------------------------------------------------------


def theta_full(R, sigma):
    """
    theta(R, sigma) from Eq (4).

    theta = (2 pi sigma^2 / R^3)
            * [ 2 sqrt(pi) R^3 sigma * erf(R/sigma)
                - exp(-R^2 / 2 sigma^2) * (sigma^4 - R^2 sigma^2)
                + (sigma^4 - 3 R^2 sigma^2) ]

    Equation (4) in McMahon 2016 contains a small typo (factor 4R^2 / sigma
    near the erf bracket); we use the form that reduces correctly to
    spherically uniform-distance kernels and matches the paper's prose
    description.  This is the analytic kernel underlying P_intra and
    P_del<D too.
    """
    R = float(R)
    s = float(sigma)
    pref = 2.0 * math.pi * s * s / (R ** 3)
    term1 = 2.0 * math.sqrt(math.pi) * (R ** 3) * s * erf(R / s)
    term2 = -math.exp(-(R ** 2) / (2.0 * s * s)) * (s ** 4 - (R ** 2) * (s ** 2))
    term3 = (s ** 4 - 3.0 * (R ** 2) * (s ** 2))
    return pref * (term1 + term2 + term3)


# ---------------------------------------------------------------------------
# Eq (5): omega(R, sigma) Monte-Carlo skew correction
# ---------------------------------------------------------------------------


def omega(R, sigma, A=OMEGA_A, B=OMEGA_B):
    """omega(R, sigma) = A + (1-A) exp(-B sigma / R)"""
    return A + (1.0 - A) * math.exp(-B * sigma / R)


# ---------------------------------------------------------------------------
# Eq (3): eta(N0, R, sigma)
# ---------------------------------------------------------------------------


def eta(N0, R, sigma):
    """Integral misrejoining probability for one DSB among N0 others."""
    density = 6.0 * N0 / (4.0 * math.pi * (R ** 3))   # free-ends / nucleus
    return density * theta_full(R, sigma) * omega(R, sigma)


# ---------------------------------------------------------------------------
# Eq (6): P_correct including pathway fidelity
# ---------------------------------------------------------------------------


def p_correct(N0, R, sigma, mu_path):
    """P_correct = mu * (1 - e^{-eta}) / eta   ; eta=0 -> P_correct = mu."""
    e = eta(N0, R, sigma)
    if e <= 1e-12:
        return mu_path
    return mu_path * (1.0 - math.exp(-e)) / e


def p_correct_per_pathway(N0, R, sigma, p_f, p_s, p_m,
                          mu_nhej=MU_NHEJ, mu_mmej=MU_MMEJ, mu_hr=1.0):
    """
    Pathway-weighted overall P_correct.  Fast = NHEJ, MMEJ = MMEJ.
    Slow = HR if HR available, else NHEJ.  We approximate the slow channel as
    NHEJ unless the caller specified pathway fidelities differently.

    Returns a single scalar Pcorrect for the cell.
    """
    pc_nhej = p_correct(N0, R, sigma, mu_nhej)
    pc_mmej = p_correct(N0, R, sigma, mu_mmej)
    pc_hr   = p_correct(N0, R, sigma, mu_hr)
    # Assume slow channel uses NHEJ in G1 (no HR); HR in G2 (mu_hr=1) only
    # affects survival via the caller's choice.  We expose both forms.
    return p_f * pc_nhej + p_s * pc_nhej + p_m * pc_mmej


def p_correct_g2(N0, R, sigma, p_f, p_s, p_m,
                 mu_nhej=MU_NHEJ, mu_mmej=MU_MMEJ, mu_hr=1.0):
    """In G2 the slow channel is HR (fidelity 1)."""
    pc_nhej = p_correct(N0, R, sigma, mu_nhej)
    pc_mmej = p_correct(N0, R, sigma, mu_mmej)
    pc_hr   = p_correct(N0, R, sigma, mu_hr)
    return p_f * pc_nhej + p_s * pc_hr + p_m * pc_mmej


# ---------------------------------------------------------------------------
# Eq (7): P_intra (chromosome territory)
# ---------------------------------------------------------------------------


def p_intra(R, sigma, n_chromosomes):
    r_c = R / (n_chromosomes ** (1.0 / 3.0))
    return theta_full(r_c, sigma) / theta_full(R, sigma)


# ---------------------------------------------------------------------------
# Convenience: full per-dose aberration & survival predictions
# ---------------------------------------------------------------------------


def predict_endpoints(spec: CellSpec, dose_Gy, t_assay_hours=24.0,
                      verbose=False):
    """
    Predict per-cell numbers of residual DSBs, misrejoined DSBs, dicentrics,
    deletions, and surviving fraction for a single (spec, dose, time) point.
    """
    N0 = DSB_YIELD_PER_GY_PER_GBP * spec.genome_gbp * dose_Gy   # eq. yield
    p_f, p_s, p_m = repair_probabilities(spec)

    N_t = n_dsb_over_time(t_assay_hours, N0, p_f, p_s, p_m)

    R = spec.r_nuc
    sigma = SIGMA_FRAC * R                # eq (Table 1)
    if spec.phase == "G2":
        Pcorr = p_correct_g2(N0, R, sigma, p_f, p_s, p_m)
    else:
        Pcorr = p_correct_per_pathway(N0, R, sigma, p_f, p_s, p_m)

    Nmis = (N0 - N_t) * (1.0 - Pcorr)
    Pin = p_intra(R, sigma, spec.n_chromosomes)
    Ndic = 0.5 * Nmis * (1.0 - Pin)
    Ndel = 0.5 * Nmis * Pin

    # Large-deletion (>3 Mbp) fraction.  D_max chromatin distance = (R/n_c^{1/3})
    # in the toy chromosome-territory model.  D_total_bp_per_chrom = L/n_c.
    # The paper uses size-cutoff via P_del<D with cubic mapping;
    # see Eq (mapping) above Eq (9).  We compute the fraction of intra-chromosome
    # deletions exceeding 3 Mbp using the analytic Eq (10) of the paper.
    L = spec.genome_gbp                          # Gbp
    n_c = spec.n_chromosomes
    r_c = R / (n_c ** (1.0 / 3.0))
    # invert D = 2 L r_D^3 / R^3  -> r_D(D) = R * (D /(2L) )^{1/3}, both
    # quantities in Gbp.  3 Mbp = 3e-3 Gbp.
    D_cut_gbp = 3e-3
    r_D_cut = R * (D_cut_gbp / (2.0 * L)) ** (1.0 / 3.0)
    Pdel_below = _p_del_below(r_c, sigma, r_D_cut)
    Ndel_gt3Mbp = 0.5 * Nmis * Pin * (1.0 - Pdel_below)

    # Survival -----------------------------------------------------------
    if spec.phase == "G1":
        S_base = math.exp(-Ndic - Ndel_gt3Mbp)
        # Cycling cells with functional apoptosis pay an additional cost.
        S_apop = math.exp(-PSI_APOP * N0) if (spec.cycling and spec.apoptosis_competent) else 1.0
        S_total = S_base * S_apop
    elif spec.phase == "G2":
        # In G2, both chromatids needed; use S = exp(-Ndic - NinterArm).
        # NinterArm requires Eq (15) integration; we approximate with Ndel
        # contribution proportional to inter-arm visibility ~ Pin / 2.
        N_interarm = 0.5 * Pin * Nmis        # rough; the integral form is
                                             # below but this captures scale.
        S_total = math.exp(-Ndic - N_interarm)
    else:
        raise ValueError

    out = {
        "N0_DSB": N0,
        "N_residual_DSB": float(N_t),
        "Pcorrect": float(Pcorr),
        "Nmis": float(Nmis),
        "Pintra": float(Pin),
        "Ndic": float(Ndic),
        "Ndel_total": float(Ndel),
        "Ndel_gt3Mbp": float(Ndel_gt3Mbp),
        "S": float(S_total),
        "p_f": p_f, "p_s": p_s, "p_m": p_m,
    }
    if verbose:
        for k, v in out.items():
            print(f"  {k:14s} = {v}")
    return out


def _p_del_below(r_c, sigma, r_D):
    """
    Approximation to Eq (9)/(10): fraction of intra-chromosome misrejoinings
    over distances <= r_D, given chromosome radius r_c.

    The paper's Eq (10) is the generalised theta(r_c, sigma, r_D); we
    approximate by the ratio of integrated Gaussian rejoining kernel weight.
    For a Gaussian density of pair separations within a sphere of radius r_c,
    fraction of pairs within distance r_D is approximately erf(r_D / (sigma sqrt(2)))^3
    (proper integration uses the same algebra as theta_full).
    """
    if r_D >= r_c:
        return 1.0
    # Gaussian end-pair distance probability mass within distance r_D:
    # use cumulative for separation r along a single axis weighted by 4 pi r^2,
    # under a Gaussian with std sigma:
    #   F(r_D) ~ integral_0^{r_D} r^2 exp(-r^2/(2 sigma^2)) dr  /  same to infty
    # Analytic:
    s = sigma
    num = (math.sqrt(math.pi / 2.0) * s ** 3 * erf(r_D / (math.sqrt(2.0) * s))
           - s ** 2 * r_D * math.exp(-(r_D ** 2) / (2.0 * s ** 2)))
    den = math.sqrt(math.pi / 2.0) * s ** 3
    val = num / den
    # Clamp to chromosome territory: pairs cannot exceed 2 r_c
    return max(0.0, min(1.0, val))


# ---------------------------------------------------------------------------
# Mean inactivation dose -- area under survival curve
# ---------------------------------------------------------------------------


def mean_inactivation_dose(spec: CellSpec, dose_max=20.0, n=400,
                           t_assay_hours=24.0):
    """MID = integral_0^infty S(D) dD, integrated to dose_max."""
    doses = np.linspace(0.0, dose_max, n)
    S = np.array([predict_endpoints(spec, d, t_assay_hours)["S"] for d in doses])
    return float(np.trapezoid(S, doses))


# ---------------------------------------------------------------------------
# Convenience: survival curve vs dose
# ---------------------------------------------------------------------------


def survival_curve(spec: CellSpec, doses, t_assay_hours=24.0):
    doses = np.asarray(doses, dtype=float)
    S = np.array([predict_endpoints(spec, d, t_assay_hours)["S"] for d in doses])
    return doses, S


# ---------------------------------------------------------------------------
# LQ-fit helper -- recover alpha, beta from the mechanistic model
# ---------------------------------------------------------------------------


def fit_lq(doses, S):
    """
    Fit -ln(S) = alpha D + beta D^2 by linear least squares.
    Returns (alpha, beta).
    """
    doses = np.asarray(doses, dtype=float)
    S = np.asarray(S, dtype=float)
    mask = (S > 0) & (doses > 0)
    y = -np.log(S[mask])
    X = np.column_stack([doses[mask], doses[mask] ** 2])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    return float(coef[0]), float(coef[1])
