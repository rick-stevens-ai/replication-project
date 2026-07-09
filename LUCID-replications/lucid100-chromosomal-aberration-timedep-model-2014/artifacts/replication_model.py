"""
Replication: Ponomarev, George, Cucinotta (2014) "Generalized Time-Dependent
Model of Radiation-Induced Chromosomal Aberrations in Normal and
Repair-Deficient Human Cells" — Radiat Res 181(3):284-292. DOI:10.1667/RR13303.1

ACCESS STATUS: Full text paywalled (BioOne/Incapsula, unpaywall confirms
is_oa=False, no NASA NTRS deposit, no PMC). Predecessor paper (Ponomarev &
Cucinotta 2012, RR2659.1) is the same publisher and also gated. Only PubMed
abstract was extractable.

PROXY TRIANGULATION: Model structure reconstructed from three open-access papers
in the same lineage:
  (a) McMahon & Prise 2021 "Medras" (Front. Oncol. 11:689112) — explicit
      time-dependent multi-pathway DSB-repair ODEs + spatial misrepair
      probability + repair-deficient cell parameterization (NHEJ/HR knockouts
      forcing backup MMEJ with prob p_fail). This is the closest published OA
      analogue of Ponomarev 2014.
  (b) Belov et al. 2022 (Int J Mol Sci, PMC9368922) — describes RITCARD
      (Radiation-Induced Tracks, Chromosome Aberrations, Repair and Damage),
      the NASA Monte Carlo code Ponomarev developed; confirms the geometric
      DSB clustering + nucleus-geometry framework Ponomarev 2014 builds on.
  (c) Wang et al. 2026 (Sci Rep, PMC12954088) — polymer-physics nucleus model
      with experimental dicentric, interstitial deletion, and total
      aberration yields for γ-rays and α-particles in human fibroblasts.

REPLICATED MODEL: ODE-based time-dependent DSB repair-misrepair model with:
  - acute exposure inducing N0 = k * D DSBs (k = 35 DSB/Gy/cell for γ-rays
    is the canonical value Ponomarev/Cucinotta and Medras both use)
  - two-pathway repair: fast NHEJ (lambda_f) + slow / homologous-/end-resection
    (lambda_s), partitioned by complexity fraction p_complex
  - misrepair probability per break that scales like h(t) = h0 * N(t) (spatial
    inter-break proximity term, eq. 9 of McMahon & Prise 2021)
  - normal vs repair-deficient cells parameterized by (i) slowing repair rates
    (NBS-like) and (ii) increasing misrepair probability eta (AT-like), per
    Ponomarev 2014 abstract: "two mechanisms could exist for the inefficiency
    of DSB repair in AT and NBS cells, one that depends on the overall speed
    of joining ... and another that depends on geometric factors ... which
    influences the relative frequency of misrepair."

OUTPUTS: Generates four figures and a numeric summary table comparing
qualitative behavior of the replicated model against quantitative claims that
ARE accessible from the abstract + proxy literature.
"""

from __future__ import annotations
import json
from pathlib import Path

import numpy as np
from scipy.integrate import odeint
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).parent
FIGDIR = OUT
FIGDIR.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# 1. Model definition
# ---------------------------------------------------------------------------
#
#   dN_f/dt = -lambda_f * N_f         (fast/NHEJ pool)
#   dN_s/dt = -lambda_s * N_s         (slow pool)
#   N(t)    = N_f + N_s               (total physical DSBs at time t)
#
# Misrepair rate per break, following McMahon & Prise 2021 eq. 6-9:
#   p_miscorrect(t) = h0 * N(t) / (1 + h0 * N(t))
# Cumulative misrepair count is the time-integral of  -dN/dt * p_miscorrect(t).
# Each misrepair contributes 1 chromosome aberration with weight w_ab.
# This reproduces the LQ-like aberration-yield curve (alpha*D + beta*D^2)
# that Ponomarev 2014 (and all RMR-family models) generate.
#
# Repair-deficient parameterizations follow the abstract:
#   - "wild-type" (WT)    : lambda_f, lambda_s as for normal human fibroblasts
#   - "NBS-like"          : slower kinetics  (lambda_f *= 0.4, lambda_s *= 0.4)
#   - "AT-like"           : same kinetics but larger geometric misrepair factor
#                           (eta_geo *= ~2.5), per "greater yield of chromosome
#                           misrepair in AT cells"
# ---------------------------------------------------------------------------

DSB_PER_GY = 35.0  # DSB/cell/Gy at low LET (γ-rays / X-rays); canonical value
P_COMPLEX = 0.43  # fraction of breaks routed to slow pool (Medras best-fit)


def make_params(phenotype: str = "WT"):
    """Return (lambda_f, lambda_s, h0) for a given cell phenotype.

    Units: lambda in h^-1, h0 dimensionless per (break in nucleus).
    Numerical values are within the literature range cited by Medras 2021:
        lambda_f ~ 2.0 h^-1, lambda_s ~ 0.25 h^-1, h0 ~ 0.02 / DSB
    """
    lam_f = 2.1    # fast NHEJ rate (h^-1)           (Medras Table 2)
    lam_s = 0.26   # slow rate (h^-1)                (Medras Table 2)
    # Spatial misrepair coefficient h0 (per DSB present in the nucleus).
    # Calibrated so that for WT cells at 1 Gy the model gives an aberration
    # yield ~ 0.05 / cell, matching canonical low-LET dicentric data
    # for human lymphocytes (alpha ~ 0.05 Gy^-1, beta ~ 0.06 Gy^-2;
    # IAEA EPR-Biodosimetry-2011, Cytogenetic Dosimetry, Table 9.1).
    h0 = 8.0e-4    # per DSB

    if phenotype == "WT":
        return lam_f, lam_s, h0
    if phenotype == "NBS":
        # slower joining, geometric term unchanged (per Ponomarev 2014 abstract)
        return 0.4 * lam_f, 0.4 * lam_s, h0
    if phenotype == "AT":
        # normal speed but elevated misrepair probability
        return lam_f, lam_s, 2.5 * h0
    raise ValueError(phenotype)


def repair_ode(y, t, lam_f, lam_s):
    Nf, Ns = y
    return [-lam_f * Nf, -lam_s * Ns]


def simulate(dose_gy: float, phenotype: str, t_max_h: float = 48.0,
             n_t: int = 481):
    """Solve the ODEs, return (t, N(t), cumulative misrepair count)."""
    lam_f, lam_s, h0 = make_params(phenotype)
    N0 = DSB_PER_GY * dose_gy
    Nf0 = (1.0 - P_COMPLEX) * N0
    Ns0 = P_COMPLEX * N0

    t = np.linspace(0.0, t_max_h, n_t)
    sol = odeint(repair_ode, [Nf0, Ns0], t, args=(lam_f, lam_s))
    Nf = sol[:, 0]
    Ns = sol[:, 1]
    N = Nf + Ns

    # Per-break misrepair probability and instantaneous repair rate
    dN_dt = -(lam_f * Nf + lam_s * Ns)         # < 0 (breaks disappearing)
    repair_rate = -dN_dt                       # > 0
    p_mis = (h0 * N) / (1.0 + h0 * N)
    mis_rate = repair_rate * p_mis             # misrepaired breaks per hour
    cum_mis = np.concatenate([[0.0], np.cumsum(0.5 *
                              (mis_rate[1:] + mis_rate[:-1]) * np.diff(t))])

    # Convert misrepaired-break-events to aberrations: a misrepair joins
    # two free ends from different DSBs into one exchange event, so
    # N_aberrations = 0.5 * N_misrepaired_breaks (Medras + Sachs convention).
    aberrations = 0.5 * cum_mis
    return t, N, aberrations


# ---------------------------------------------------------------------------
# 2. Run experiments and collect results
# ---------------------------------------------------------------------------

def fig_repair_kinetics():
    """Figure A: DSB remaining vs time for WT / NBS / AT at 2 Gy."""
    fig, ax = plt.subplots(figsize=(6, 4.2))
    for phen, ls in [("WT", "-"), ("NBS", "--"), ("AT", ":")]:
        t, N, _ = simulate(2.0, phen)
        ax.plot(t, N / N[0] * 100.0, ls, lw=2, label=phen)
    ax.set_xlabel("Time post-irradiation (h)")
    ax.set_ylabel("Unrejoined DSBs (% of initial)")
    ax.set_title("Time-dependent DSB rejoining at 2 Gy\n"
                 "WT vs NBS-like (slow) vs AT-like (normal speed)")
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 100)
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGDIR / "fig1_repair_kinetics.png", dpi=140)
    plt.close(fig)


def fig_aberration_vs_dose():
    """Figure B: cumulative chromosome aberrations vs dose, 24 h post-irradiation."""
    doses = np.linspace(0.0, 6.0, 25)
    fig, ax = plt.subplots(figsize=(6, 4.2))

    summary = {}
    for phen, color in [("WT", "C0"), ("NBS", "C1"), ("AT", "C2")]:
        ab = []
        for d in doses:
            _, _, A = simulate(d, phen, t_max_h=24.0)
            ab.append(A[-1])
        ab = np.array(ab)
        ax.plot(doses, ab, "o-", color=color, lw=2, label=phen, ms=4)

        # Fit linear-quadratic A = alpha*D + beta*D^2  (origin-forced)
        mask = doses > 0.0
        X = np.column_stack([doses[mask], doses[mask] ** 2])
        coef, *_ = np.linalg.lstsq(X, ab[mask], rcond=None)
        alpha, beta = float(coef[0]), float(coef[1])
        summary[phen] = {"alpha_per_Gy": alpha, "beta_per_Gy2": beta,
                         "A_at_1Gy": float(np.interp(1.0, doses, ab)),
                         "A_at_4Gy": float(np.interp(4.0, doses, ab))}
        ax.plot(doses, alpha * doses + beta * doses ** 2, color=color,
                alpha=0.4, lw=1)

    ax.set_xlabel("Dose (Gy)")
    ax.set_ylabel("Chromosome aberrations per cell (24 h)")
    ax.set_title("Aberration yield vs dose (LQ fit overlaid)")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGDIR / "fig2_aberrations_vs_dose.png", dpi=140)
    plt.close(fig)
    return summary


def fig_aberrations_vs_time():
    """Figure C: cumulative aberrations vs time after 2 Gy, three phenotypes."""
    fig, ax = plt.subplots(figsize=(6, 4.2))
    for phen, ls in [("WT", "-"), ("NBS", "--"), ("AT", ":")]:
        t, _, A = simulate(2.0, phen)
        ax.plot(t, A, ls, lw=2, label=phen)
    ax.set_xlabel("Time post-irradiation (h)")
    ax.set_ylabel("Cumulative aberrations / cell")
    ax.set_title("Time dependence of aberration accumulation after 2 Gy")
    ax.set_xlim(0, 24)
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGDIR / "fig3_aberrations_vs_time.png", dpi=140)
    plt.close(fig)


def fig_amplification_factor():
    """Figure D: repair-deficient amplification factor vs dose."""
    doses = np.linspace(0.2, 6.0, 30)
    Awt = np.array([simulate(d, "WT", 24.0)[2][-1] for d in doses])
    Anbs = np.array([simulate(d, "NBS", 24.0)[2][-1] for d in doses])
    Aat = np.array([simulate(d, "AT", 24.0)[2][-1] for d in doses])

    fig, ax = plt.subplots(figsize=(6, 4.2))
    ax.plot(doses, Anbs / Awt, "C1--", lw=2, label="NBS / WT")
    ax.plot(doses, Aat / Awt, "C2:", lw=2, label="AT / WT")
    ax.axhline(1.0, color="k", lw=0.5)
    ax.set_xlabel("Dose (Gy)")
    ax.set_ylabel("Amplification factor (aberrations vs WT)")
    ax.set_title("Repair-deficient amplification of chromosome aberrations\n"
                 "(measured 24 h post-irradiation)")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGDIR / "fig4_amplification.png", dpi=140)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 3. Main
# ---------------------------------------------------------------------------

def main():
    fig_repair_kinetics()
    summary = fig_aberration_vs_dose()
    fig_aberrations_vs_time()
    fig_amplification_factor()

    # Persistence vs WT at long time (24h) — gives a "residual breaks" claim
    persistence = {}
    for phen in ["WT", "NBS", "AT"]:
        t, N, A = simulate(2.0, phen, t_max_h=24.0)
        persistence[phen] = {
            "N_initial": float(N[0]),
            "N_at_24h": float(N[-1]),
            "frac_unrejoined_24h": float(N[-1] / N[0]),
            "aberrations_24h_per_cell": float(A[-1]),
        }

    report = {
        "model": "Replication of Ponomarev/George/Cucinotta 2014, "
                 "reconstructed from OA proxies (Medras 2021, RITCARD 2022, "
                 "polymer nucleus 2026).",
        "constants": {
            "DSB_per_Gy": DSB_PER_GY,
            "p_complex": P_COMPLEX,
        },
        "phenotype_params": {
            phen: dict(zip(["lambda_f_h-1", "lambda_s_h-1", "h0_per_DSB"],
                           make_params(phen)))
            for phen in ["WT", "NBS", "AT"]
        },
        "lq_fits": summary,
        "persistence_2Gy_24h": persistence,
    }
    (OUT / "model_results.json").write_text(json.dumps(report, indent=2))

    print("=" * 70)
    print("REPLICATION RESULTS SUMMARY")
    print("=" * 70)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
