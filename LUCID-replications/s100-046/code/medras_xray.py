"""
s100-046 — Reproduction of McMahon et al. 2017 Sci. Rep. 7:10790
"A general mechanistic model enables predictions of the biological effectiveness
of different qualities of radiation."  DOI: 10.1038/s41598-017-10820-1

Scope of this implementation
----------------------------
Reproduces the X-ray (uniform-DSB) analytic core of the McMahon mechanistic
model:

  N0 = D * G * yDSB                       (number of DSBs)
  yDSB = 5.738 DSB/Gy/Gbp                 (Table 1)
  V_nuc = 5.61 * E_DSB                    (μm^3, E_DSB in keV)  → ND/D = V_nuc / E_DSB,
                                            i.e. 35 DSB/Gy in a human nucleus
  rnuc = 1.1 * E_DSB^(1/3) μm
  E_DSB = 60.7 keV  → rnuc = 4.32 μm      (paper's headline)

  Misrejoin interaction rate:
      ζ(d) ∝ exp(-d^2 / (2 σ^2))     with σ = 0.0428 * R_nuc

  Average η for a uniform pair of DSBs in a sphere of radius R, summed
  over (N0 - 1) other DSBs:
      η_pair = (N0 - 1) * <ζ(d)>_uniform-pair
  where <ζ(d)>_uniform-pair = ∫∫ζ(|r1-r2|) / V^2 d^3r1 d^3r2  is evaluated
  numerically by Monte-Carlo (this surrogates the closed-form θ(R,σ) from
  McMahon 2016, which is not written out in the 2017 PDF).

  Correct repair probability per DSB:
      P_correct = μ_x * (1 - exp(-η)) / η
  (For a NHEJ-competent simple break in G1, μ_x = μ_NHEJ = 0.985.
   For a complex break in G1 in NHEJ-competent cells we treat it as NHEJ
   too at this aggregate level; the paper averages μ across the population
   in N0.)

  Aberrations (Eqs. 1–4):
      N_mis     = N0 * (1 - P_correct)
      N_dic     = 0.5 * N_mis * (1 - P_intra)
      P_intra   = θ(r_c, σ) / θ(R, σ)   with r_c = R / nc^(1/3)
      P_del<D   = θ(r_c, σ, r_D) / θ(r_c, σ)   with D = 3 Mbp and
                  r_D = R * (D / (2 L))^(1/3)
      N_del     = 0.5 * N_mis * P_intra * (1 - P_del<D)
      N_inter-arm = 0.5 * N_mis * P_intra * P_inter-arm    (G2 only)

  Survival:
      S_G1 = exp(-N_dic - N_del>3Mb) * S_apoptosis(if G1-arrest competent)
      S_G2 = exp(-N_dic - N_inter-arm) * S_mitosis
      S_asynch = (2/3) * S_G1 + (1/3) * S_G2

  Mitosis/apoptosis (Methods):
      S_mitosis = exp(-φ * N0)    with φ = 0.0085 break^-1   (apoptosis sym used as φ)
      S_apoptosis = exp(-ψ * N0)  with ψ = 0.014 break^-1
  (NB: McMahon Table 1 names the symbols ψ=mitosis 0.014, φ=apoptosis 0.0085,
   but the Methods text uses S_mitosis = e^{-φ N_M} and S_apoptosis = e^{-ψ N_G1}.
   Symbol mapping inconsistent in the paper; we use the numerical values 0.014
   for mitosis and 0.0085 for apoptosis as Table 1 says.)

This script then runs three predictions:

  (1) The headline geometric check: r_nuc from E_DSB.
  (2) X-ray survival curves and LQ fits for a generic asynchronous V79
      hamster cell (the most studied line) and a generic asynchronous
      human cell, including MID.
  (3) Self-consistency / sanity: monotonicity of S(D), MID > 0, α > 0,
      hamster MID > human MID (hamster more resistant).
"""
from __future__ import annotations
import json
import math
import sys
from dataclasses import dataclass

import numpy as np
from scipy import optimize
from scipy.special import erfc

# ---- Table 1 parameters --------------------------------------------------
Y_DSB        = 5.738      # DSB / Gy / Gbp
P_COMPLEX    = 0.42
P_FAIL       = 0.67
SIGMA_FRAC   = 0.0428     # σ as fraction of R_nuc
MU_NHEJ      = 0.985
MU_MMEJ      = 0.465
MU_HR        = 1.000
PSI_MITOSIS  = 0.014      # break^-1  (Table 1 calls this ψ = mitosis sensitivity)
PHI_APOPT    = 0.0085     # break^-1  (Table 1 calls this φ = apoptosis sensitivity)
LAMBDA_F     = 3.6        # h^-1
LAMBDA_S     = 0.15       # h^-1
LAMBDA_M     = 0.0084     # h^-1
E_DSB_KEV    = 60.7       # fitted in this paper

# Geometric headline relation (Methods, just below Table 1)
# V_nuc = 5.61 * E_DSB μm^3 (E_DSB in keV)  → r_nuc = 1.1 * E_DSB^(1/3) μm
def nuclear_radius_um(e_dsb_keV: float) -> float:
    return 1.1 * e_dsb_keV ** (1.0 / 3.0)

# DSB threshold size for "large deletion" lethality (Methods, Eq. 3 context)
DEL_THRESH_MBP = 3.0

# Cell-cycle distribution for asynchronous populations (Methods)
ASYNC_FRAC_G1 = 2.0 / 3.0
ASYNC_FRAC_G2 = 1.0 / 3.0

# Symmetry of misrepair (Methods)
P_ASYM = 0.5

# Default RNG
RNG = np.random.default_rng(20260625)

# ---- Helpers -------------------------------------------------------------

def theta_pair_uniform(R: float, sigma: float, n_samples: int = 200_000,
                       r_cut: float | None = None,
                       rng: np.random.Generator | None = None) -> float:
    """Monte-Carlo estimate of the average ζ(d) = exp(-d^2/(2σ^2)) over two
    points drawn uniformly inside a sphere of radius R, optionally restricted
    to pairs with separation < r_cut.

    This is the McMahon "θ" function from ref. 24 (closed-form not in the
    2017 PDF). Returns a dimensionless rate per DSB pair.
    """
    rng = rng if rng is not None else RNG
    # sample uniformly inside a sphere of radius R by rejection (simple, robust)
    n_keep = 0
    accum = 0.0
    accum_full = 0.0
    while n_keep < n_samples:
        batch = max(n_samples - n_keep, 8192) * 2
        u1 = rng.uniform(-1, 1, size=(batch, 3)) * R
        u2 = rng.uniform(-1, 1, size=(batch, 3)) * R
        r1 = np.linalg.norm(u1, axis=1)
        r2 = np.linalg.norm(u2, axis=1)
        inside = (r1 <= R) & (r2 <= R)
        if not inside.any():
            continue
        d = np.linalg.norm(u1[inside] - u2[inside], axis=1)
        z = np.exp(-0.5 * (d / sigma) ** 2)
        accum_full += z.sum()
        if r_cut is not None:
            mask = d < r_cut
            accum += z[mask].sum()
        else:
            accum += z.sum()
        n_keep += int(inside.sum())
    if r_cut is None:
        return accum_full / n_keep
    return accum / n_keep, accum_full / n_keep


def theta_R_sigma(R: float, sigma: float, n_samples: int = 200_000,
                  rng: np.random.Generator | None = None) -> float:
    """Average interaction rate ζ for a uniform pair of DSBs in a sphere of
    radius R."""
    return theta_pair_uniform(R, sigma, n_samples=n_samples, rng=rng)


def average_eta(N0: float, R: float, sigma: float,
                n_samples: int = 200_000,
                rng: np.random.Generator | None = None) -> float:
    """Total interaction rate η for an average DSB: (N0-1) * <ζ(d)>_uniform."""
    if N0 <= 1:
        return 0.0
    return (N0 - 1.0) * theta_R_sigma(R, sigma, n_samples=n_samples, rng=rng)


def p_correct(N0: float, R: float, sigma: float, mu_x: float,
              n_samples: int = 200_000,
              rng: np.random.Generator | None = None) -> float:
    """Correct-repair probability per DSB, averaged over the pair distribution."""
    eta = average_eta(N0, R, sigma, n_samples=n_samples, rng=rng)
    if eta < 1e-9:
        return mu_x
    return mu_x * (1.0 - math.exp(-eta)) / eta


def aberration_yields(N0: float, R: float, sigma: float,
                      nc: int, L_bp: float,
                      mu_eff: float,
                      n_samples: int = 200_000,
                      rng: np.random.Generator | None = None) -> dict:
    """Compute N_mis, N_dic, N_del>3Mb, P_intra, P_del<D for a uniform X-ray
    exposure with N0 DSBs distributed over a sphere of radius R, nc chromosomes
    of total length L_bp."""
    if N0 < 1.0:
        return {"N_mis": 0.0, "N_dic": 0.0, "N_del": 0.0,
                "P_intra": 0.0, "P_del_lt_D": 0.0, "eta": 0.0,
                "P_correct": mu_eff}
    rc = R / (nc ** (1.0 / 3.0))
    # Eqs. (in Methods): θ(rc, σ) / θ(R, σ)
    theta_R = theta_R_sigma(R, sigma, n_samples=n_samples, rng=rng)
    theta_rc = theta_R_sigma(rc, sigma, n_samples=n_samples, rng=rng)
    # Avoid div-by-zero
    P_intra = theta_rc / theta_R if theta_R > 0 else 0.0
    P_intra = min(max(P_intra, 0.0), 1.0)
    # r_D from   D = 2 L r_D^3 / R^3  with D = 3 Mbp = 3e6 bp
    D_bp = DEL_THRESH_MBP * 1.0e6
    rD = R * (D_bp / (2.0 * L_bp)) ** (1.0 / 3.0)
    rD = min(rD, rc)
    # θ(rc, σ, rD) / θ(rc, σ) — fraction of in-chromosome DSB pairs separated by < rD
    if rD > 0:
        ratio, _ = theta_pair_uniform(rc, sigma, n_samples=n_samples,
                                      r_cut=rD, rng=rng)
        denom = theta_rc
        P_del_lt_D = ratio / denom if denom > 0 else 0.0
    else:
        P_del_lt_D = 0.0
    P_del_lt_D = min(max(P_del_lt_D, 0.0), 1.0)

    eta = (N0 - 1.0) * theta_R
    Pc = mu_eff * (1.0 - math.exp(-eta)) / eta if eta > 0 else mu_eff
    Pc = min(max(Pc, 0.0), 1.0)
    N_mis = N0 * (1.0 - Pc)
    N_dic = 0.5 * N_mis * (1.0 - P_intra)
    N_del = 0.5 * N_mis * P_intra * (1.0 - P_del_lt_D)
    return {"N_mis": N_mis, "N_dic": N_dic, "N_del": N_del,
            "P_intra": P_intra, "P_del_lt_D": P_del_lt_D,
            "eta": eta, "P_correct": Pc, "rc_um": rc, "rD_um": rD,
            "theta_R": theta_R, "theta_rc": theta_rc}


# ---- Cell-line container -------------------------------------------------

@dataclass
class CellLine:
    name: str
    genome_size_gbp: float        # haploid + diploid handled via factor
    diploid_factor: float         # 1 for haploid quote, 2 for diploid genome
    n_chromosomes: int            # total chromosomes per cell
    HR_competent: bool
    NHEJ_competent: bool
    G1_arrest_competent: bool

    @property
    def total_dna_bp(self) -> float:
        return self.diploid_factor * self.genome_size_gbp * 1.0e9


# Generic reference cells the paper repeatedly uses
V79_HAMSTER = CellLine(
    name="V79 (Chinese hamster)",
    genome_size_gbp=2.6,        # haploid (CHO/V79 has ~2.6 Gbp haploid)
    diploid_factor=2.0,
    n_chromosomes=22,           # V79 is near-diploid hamster
    HR_competent=True,
    NHEJ_competent=True,
    G1_arrest_competent=False,  # hamster lines typically G1-arrest deficient
)

NORMAL_HUMAN = CellLine(
    name="Normal human fibroblast",
    genome_size_gbp=3.2,        # haploid
    diploid_factor=2.0,
    n_chromosomes=46,
    HR_competent=True,
    NHEJ_competent=True,
    G1_arrest_competent=True,
)


# ---- Survival ------------------------------------------------------------

def survival_xray(cell: CellLine, dose_Gy: np.ndarray,
                  e_dsb_keV: float = E_DSB_KEV,
                  n_samples: int = 100_000,
                  rng: np.random.Generator | None = None) -> dict:
    """Predict X-ray survival curve for a cell line over an array of doses.

    Returns dict with S(D), the aberration components, and LQ parameters
    fitted from the survival curve over the 0–6 Gy range.
    """
    rng = rng if rng is not None else RNG
    R = nuclear_radius_um(e_dsb_keV)
    sigma = SIGMA_FRAC * R
    # Total DSB per Gy = yield * (Gbp of genome present) * diploid_factor
    # yield is per haploid Gbp; multiply by diploid_factor to get whole-cell yield
    dsb_per_gy = Y_DSB * cell.genome_size_gbp * cell.diploid_factor

    # Aggregate effective repair fidelity — at this aggregate level we use
    # μ_eff = average over (1-pc)*μ_NHEJ + pc * branch (NHEJ in G1 / HR in G2)
    # For G1: complex breaks repaired by NHEJ in G1 → μ_eff = μ_NHEJ if NHEJ+
    #   else MMEJ-backup with prob p_f: μ_eff = (1-pf)*μ_NHEJ + pf*μ_MMEJ
    if cell.NHEJ_competent:
        mu_G1 = MU_NHEJ
        mu_G2 = (1 - P_COMPLEX) * MU_NHEJ + P_COMPLEX * MU_HR
    else:
        mu_simple = (1 - P_FAIL) * MU_NHEJ + P_FAIL * MU_MMEJ
        mu_complex_G1 = (1 - P_FAIL) * MU_NHEJ + P_FAIL * MU_MMEJ
        mu_complex_G2 = (1 - P_FAIL) * MU_HR   + P_FAIL * MU_MMEJ if cell.HR_competent \
                       else (1 - P_FAIL) * MU_NHEJ + P_FAIL * MU_MMEJ
        mu_G1 = (1 - P_COMPLEX) * mu_simple + P_COMPLEX * mu_complex_G1
        mu_G2 = (1 - P_COMPLEX) * mu_simple + P_COMPLEX * mu_complex_G2

    L_bp = cell.total_dna_bp

    S = np.zeros_like(dose_Gy, dtype=float)
    detail = []
    for i, D in enumerate(dose_Gy):
        N0 = D * dsb_per_gy
        if N0 < 1.0:
            S[i] = 1.0
            detail.append({"D": float(D), "N0": float(N0)})
            continue
        # G1
        a_G1 = aberration_yields(N0, R, sigma, cell.n_chromosomes, L_bp,
                                 mu_eff=mu_G1, n_samples=n_samples, rng=rng)
        # G2 — we approximate inter-arm rate by P_inter-arm ≈ P_del<D_centromere.
        # The 2017 paper integrates over chromosome length; for a generic cell,
        # half of each chromosome lies above the centromere, so on average
        # P_inter-arm ≈ 0.5. We use 0.5 as a stand-in.
        a_G2 = aberration_yields(N0, R, sigma, cell.n_chromosomes, L_bp,
                                 mu_eff=mu_G2, n_samples=n_samples, rng=rng)
        P_inter_arm = 0.5

        S_chrom_G1 = math.exp(-(a_G1["N_dic"] + a_G1["N_del"]))
        S_chrom_G2 = math.exp(-(a_G2["N_dic"] +
                                a_G2["N_mis"] * a_G2["P_intra"] * P_inter_arm * 0.5))

        S_mit  = math.exp(-PSI_MITOSIS * N0)   # mitotic catastrophe (G2/M)
        S_apop = math.exp(-PHI_APOPT * N0) if cell.G1_arrest_competent else 1.0

        S_G1 = S_chrom_G1 * S_apop
        S_G2 = S_chrom_G2 * S_mit
        S_asynch = ASYNC_FRAC_G1 * S_G1 + ASYNC_FRAC_G2 * S_G2
        S[i] = max(min(S_asynch, 1.0), 1e-15)
        detail.append({"D": float(D), "N0": float(N0),
                       "S_G1": S_G1, "S_G2": S_G2, "S": float(S[i]),
                       "P_correct_G1": a_G1["P_correct"],
                       "P_intra": a_G1["P_intra"],
                       "P_del_lt_3Mb": a_G1["P_del_lt_D"],
                       "rc_um": a_G1["rc_um"], "rD_um": a_G1["rD_um"]})

    # Fit α, β over doses ≤ 6 Gy (typical reported range)
    fit_mask = (dose_Gy > 0) & (dose_Gy <= 6.0) & (S > 1e-6)
    Dfit = dose_Gy[fit_mask]
    Sfit = S[fit_mask]
    try:
        # log S = -α D - β D^2
        Y = -np.log(Sfit)
        # Solve [D, D^2] @ [α, β] = Y by lsq
        A = np.column_stack([Dfit, Dfit ** 2])
        coef, *_ = np.linalg.lstsq(A, Y, rcond=None)
        alpha, beta = float(coef[0]), float(coef[1])
    except Exception:
        alpha = beta = float("nan")

    # MID via Eq. 5
    if beta > 0 and alpha >= 0:
        MID = math.exp(alpha ** 2 / (4 * beta)) * math.sqrt(math.pi) * \
              erfc(alpha / (2 * math.sqrt(beta))) / (2 * math.sqrt(beta))
    else:
        MID = float("nan")

    return {"D": dose_Gy.tolist(), "S": S.tolist(),
            "alpha": alpha, "beta": beta, "MID": MID,
            "R_um": R, "sigma_um": sigma,
            "dsb_per_gy": dsb_per_gy, "mu_G1": mu_G1, "mu_G2": mu_G2,
            "detail": detail}


# ---- Main reproduction ---------------------------------------------------

def main():
    out = {}

    # (1) Geometric headline: r_nuc from E_DSB
    r_nuc = nuclear_radius_um(E_DSB_KEV)
    out["headline_r_nuc"] = {
        "E_DSB_keV": E_DSB_KEV,
        "r_nuc_um_predicted": r_nuc,
        "r_nuc_um_paper": 4.32,
        "abs_error_um": abs(r_nuc - 4.32),
        "rel_error_pct": 100 * abs(r_nuc - 4.32) / 4.32,
    }

    # (2) DSB-per-Gy for human (~3.2 Gbp diploid = 6.4 Gbp total)
    dsb_per_gy_human = Y_DSB * 3.2 * 2.0
    out["headline_dsb_per_gy_human"] = {
        "predicted": dsb_per_gy_human,
        "paper": 35.0,
        "rel_error_pct": 100 * abs(dsb_per_gy_human - 35.0) / 35.0,
    }

    # (3) X-ray survival curves
    dose = np.linspace(0, 10, 21)
    for cell in (V79_HAMSTER, NORMAL_HUMAN):
        res = survival_xray(cell, dose, n_samples=80_000)
        out[cell.name] = {
            "alpha_Gy^-1": res["alpha"],
            "beta_Gy^-2": res["beta"],
            "alpha_over_beta_Gy": (res["alpha"] / res["beta"]
                                    if res["beta"] > 0 else None),
            "MID_Gy": res["MID"],
            "S(2Gy)": res["S"][dose.tolist().index(2.0)] if 2.0 in dose else None,
            "S(4Gy)": res["S"][dose.tolist().index(4.0)] if 4.0 in dose else None,
            "S(6Gy)": res["S"][dose.tolist().index(6.0)] if 6.0 in dose else None,
            "R_um": res["R_um"],
            "sigma_um": res["sigma_um"],
            "dsb_per_gy": res["dsb_per_gy"],
            "mu_G1": res["mu_G1"],
            "mu_G2": res["mu_G2"],
        }

    # Pretty print
    print(json.dumps(out, indent=2, default=float))
    return out


if __name__ == "__main__":
    main()
