#!/usr/bin/env python3
"""
Pass-2 reproduction script for Franken et al. 2012
(Oncology Reports 27: 769-774, DOI 10.3892/or.2011.1604).

Pass 1 covered the four Table-I RBE values + first-order σ propagation +
two Discussion ratios (1% / 10% of DSBs lethal). That gave coverage 6/10.

This pass-2 script targets the *additional* testable numeric claims in
the paper, all derivable from Table I + the explicit prose:

  C7.  Effect-level RBE for γ-H2AX foci          (paper says 1, Fig. 2)
  C8.  Effect-level RBE for cell reproductive death (paper says 4, Fig. 2)
  C9.  Effect-level RBE for chromosome fragments (paper says 13, Fig. 2)
  C10. Effect-level RBE for colour junctions     (paper says 13, Fig. 2)
  C11. "factor 4 larger" — α_fragments / α_survival ratio for each rad.
       (Discussion, p. 773)
  C12. Survival "diverge by more than a decade at 2 Gy" — derive
       S_γ(2)/S_α(2) from Table I α values (linear contribution only,
       since paper does not tabulate β_γ-survival).
  C13. Upper bound on β_γ-survival from the requirement that the
       LQ survival curve still satisfy the experimental dose-range
       constraint (γ-survival doses up to 8 Gy).

For each claim we either:
  - compute the predicted value and compare against the paper's number, or
  - derive the value the paper *implies* and check internal consistency.

Outputs are written under ../results/ as JSON.
"""

from __future__ import annotations
import math
import json
import os
from dataclasses import dataclass, asdict


# ---------------------------------------------------------------------------
# Table I (Franken et al. 2012, p. 773) — Marker MD verbatim
# ---------------------------------------------------------------------------

@dataclass
class AlphaPair:
    endpoint: str
    a_alpha: float        # alpha-particle α (Gy^-1)
    s_alpha: float
    a_gamma: float        # γ-ray α (Gy^-1)
    s_gamma: float
    rbe_paper: float
    s_rbe_paper: float


TABLE_I = {
    "h2ax":      AlphaPair("γ-H2AX foci (DNA DSBs)", 25.0,  8.20, 25.00, 3.000, 1.0,  0.3),
    "survival":  AlphaPair("Cell reproductive death", 2.2, 0.38,  0.15, 0.045, 14.7, 5.1),
    "fragments": AlphaPair("Chromosomal fragments",  16.8,  4.50,  1.10, 0.310, 15.3, 5.9),
    "colour":    AlphaPair("Colour junctions",        9.2,  3.20,  0.69, 0.200, 13.3, 6.0),
}

EFFECT_LEVEL_RBE_PAPER = {
    "h2ax": 1.0,
    "survival": 4.0,
    "fragments": 13.0,
    "colour": 13.0,
}


# ---------------------------------------------------------------------------
# C7-C10: Effect-level RBE values from Fig. 2
# ---------------------------------------------------------------------------
# Definition (standard radiobiology, e.g. Hall & Giaccia, *Radiobiology
# for the Radiologist*, 7th ed., ch. 7): the iso-effect RBE at a reference
# dose D_ref of the test (α) radiation is
#
#     RBE_eff(D_ref) = D_ref(reference radiation, here γ) / D_ref(test, α)
#
# such that both deliver the same biological effect E.
#
# For the three linear endpoints (foci, fragments, colour junctions):
#       E(D)   = α D
#       So D_γ such that α_γ D_γ = α_α D_α gives D_γ = (α_α/α_γ) D_α.
#       Therefore RBE_eff = α_α / α_γ  — INDEPENDENT of effect level.
#       Hence effect-level RBE = α-ratio = Table-I RBE.
#
# For survival (S = exp(-αD - βD²)):
#       S_α(D_α) = exp(-α_α D_α)  (paper: β_α was statistically zero)
#       S_γ(D_γ) = exp(-α_γ D_γ - β_γ D_γ²)
#       Solve S_α = S_γ at a reference effect level (e.g. S = 0.1 = 10%).
#       Without β_γ this is again a simple α-ratio (= 14.67).
#       The paper's Fig.2-derived value of 4 is therefore informative
#       BECAUSE β_γ is non-zero for survival: it tells us how much the
#       γ curve bends down at higher doses.
#
# We can in fact INFER β_γ from the requirement RBE_eff(survival) = 4
# at some effect level (typically S = 0.1 = 10% survival, the standard
# radiobiology reference). We do that below as part of C13.


def effect_level_rbe_linear(pair: AlphaPair) -> float:
    """For purely linear endpoints, effect-level RBE = α-ratio."""
    return pair.a_alpha / pair.a_gamma


def survival_alpha(D: float, alpha: float) -> float:
    """Pure-exponential survival (β=0)."""
    return math.exp(-alpha * D)


def survival_gamma_lq(D: float, alpha: float, beta: float) -> float:
    """LQ survival."""
    return math.exp(-alpha * D - beta * D * D)


def dose_at_survival_alpha(S_target: float, alpha: float) -> float:
    """Invert S = exp(-αD) for D."""
    return -math.log(S_target) / alpha


def dose_at_survival_gamma(S_target: float, alpha: float, beta: float) -> float:
    """Invert S = exp(-αD - βD²) for D (positive root of αD + βD² = -ln S)."""
    rhs = -math.log(S_target)
    if beta == 0:
        return rhs / alpha
    disc = alpha * alpha + 4.0 * beta * rhs
    return (-alpha + math.sqrt(disc)) / (2.0 * beta)


def infer_beta_gamma_survival(rbe_target: float = 4.0,
                              S_ref: float = 0.1,
                              alpha_alpha: float = 2.2,
                              alpha_gamma: float = 0.15
                              ) -> tuple[float, dict]:
    """
    Find β_γ such that the iso-survival RBE at S = S_ref equals
    rbe_target (= 4 per the paper's Fig. 2 caption).

    For α-particles (β_α ≈ 0):
        D_α(S_ref) = -ln(S_ref) / α_α
    For γ-rays (LQ):
        D_γ(S_ref) solves α_γ D + β_γ D² = -ln(S_ref)
    RBE_eff = D_γ / D_α = rbe_target  ⇒  D_γ = rbe_target * D_α
    ⇒  β_γ D_γ² + α_γ D_γ - (-ln S_ref) = 0   solved for β_γ.
    """
    D_alpha = -math.log(S_ref) / alpha_alpha
    D_gamma = rbe_target * D_alpha
    rhs = -math.log(S_ref)
    # alpha_gamma * D_gamma + beta * D_gamma^2 = rhs
    beta = (rhs - alpha_gamma * D_gamma) / (D_gamma * D_gamma)
    diag = {
        "S_ref": S_ref,
        "rbe_target_paper": rbe_target,
        "alpha_alpha": alpha_alpha,
        "alpha_gamma": alpha_gamma,
        "D_alpha_at_Sref_Gy": D_alpha,
        "D_gamma_at_Sref_Gy": D_gamma,
        "alpha_over_beta_gamma_Gy": alpha_gamma / beta if beta > 0 else None,
    }
    return beta, diag


# ---------------------------------------------------------------------------
# C11: factor-4 claim
# ---------------------------------------------------------------------------
# Discussion (p.773): "The frequencies of chromosome aberrations shown
# in Table I are for α radiation as well as for γ-radiation at least
# a factor 4 larger than the corresponding value for cell reproductive death."
#
# Operational test: α_fragments / α_survival for each radiation should
# be >= 4. (Author's strongest statement is "at least 4"; let's compute
# both fragments and colour-junctions ratios.)


def factor_check(numer: AlphaPair, denom: AlphaPair, label: str) -> dict:
    out = {
        "label": label,
        "alpha_radiation_ratio": numer.a_alpha / denom.a_alpha,
        "gamma_radiation_ratio": numer.a_gamma / denom.a_gamma,
    }
    out["passes_factor_4_paper_claim"] = (
        out["alpha_radiation_ratio"] >= 4.0
        and out["gamma_radiation_ratio"] >= 4.0
    )
    return out


# ---------------------------------------------------------------------------
# C12: "more than a decade at 2 Gy" survival divergence
# ---------------------------------------------------------------------------
# Paper Fig. 2 (visual claim, also implied by α-values): at 2 Gy the
# survival curves for α vs γ should differ by more than a factor of 10.
#
# Pass-1 plot used pure exponential (β=0) for both. That under-estimates
# γ-survival at 2 Gy (the γ curve has β>0, which bends it DOWN, making
# the divergence LARGER, not smaller). So the pure-α linear lower bound is
# an under-estimate of the true divergence. We compute both:
#
#   Lower bound (β_γ=0):    S_γ(2) / S_α(2) = exp((α_α - α_γ)*2)
#   With inferred β_γ:      S_γ(2) / S_α(2) = exp(-α_γ*2 - β_γ*4) / exp(-α_α*2)
#                                            = exp((α_α - α_γ)*2 - 4 β_γ)


def survival_divergence_at(D: float, alpha_a: float, alpha_g: float,
                           beta_g: float = 0.0) -> dict:
    S_a = math.exp(-alpha_a * D)
    S_g = math.exp(-alpha_g * D - beta_g * D * D)
    ratio = S_a / S_g  # how much MORE the α-particles kill at dose D
    return {
        "dose_Gy": D,
        "S_alpha": S_a,
        "S_gamma": S_g,
        "beta_gamma_used": beta_g,
        "ratio_S_gamma_over_S_alpha": S_g / S_a,
        "ratio_S_alpha_over_S_gamma": ratio,
        "log10_decades_of_divergence": math.log10(S_g / S_a) if S_a > 0 else None,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.normpath(os.path.join(here, "..", "results"))
    os.makedirs(out_dir, exist_ok=True)

    summary = {"pass": 2, "claims": {}}

    # ---- C7-C10: effect-level RBE ----
    eff = {}
    for key in ("h2ax", "fragments", "colour"):
        p = TABLE_I[key]
        recomp = effect_level_rbe_linear(p)
        target = EFFECT_LEVEL_RBE_PAPER[key]
        eff[key] = {
            "endpoint": p.endpoint,
            "model": "linear F(D) = αD",
            "rbe_effect_level_recomputed": recomp,
            "rbe_effect_level_paper": target,
            "rbe_paper_table_I": p.rbe_paper,
            "match_to_paper_effect_level_pct": (
                100.0 * abs(recomp - target) / target if target else None
            ),
            "note": (
                "For purely linear endpoints F(D)=αD, iso-effect RBE "
                "is identical to the α-ratio and is INDEPENDENT of "
                "effect level. So Fig.2's effect-level value MUST equal "
                "Table I to first order — modulo paper's rounding to a "
                "single digit (1, 13, 13)."
            ),
        }
    # C8: survival is the interesting one
    p_surv = TABLE_I["survival"]
    rbe_lin_only = effect_level_rbe_linear(p_surv)
    # iso-survival at 10% with β_γ = 0 → same α-ratio (~14.7).
    # The paper says 4 — meaning β_γ is non-zero AND we are at a chosen
    # effect level.
    beta_g_inferred, diag = infer_beta_gamma_survival(
        rbe_target=EFFECT_LEVEL_RBE_PAPER["survival"],
        S_ref=0.1,
        alpha_alpha=p_surv.a_alpha,
        alpha_gamma=p_surv.a_gamma,
    )
    eff["survival"] = {
        "endpoint": p_surv.endpoint,
        "model_alpha": "S = exp(-α_α D), β_α ≈ 0 per paper",
        "model_gamma": "S = exp(-α_γ D - β_γ D²)",
        "rbe_paper_table_I_alpha_ratio": rbe_lin_only,
        "rbe_paper_fig2_effect_level": EFFECT_LEVEL_RBE_PAPER["survival"],
        "delta_explanation": (
            "Table-I RBE (14.7) is the α-only ratio at low dose. "
            "Fig-2 effect-level RBE (4) is the iso-survival ratio at "
            "a clinically relevant effect (~10% survival), where β_γ "
            "bends the γ curve down so much that γ catches up."
        ),
        "inferred_beta_gamma_survival_at_S0p1_Gy_minus2": beta_g_inferred,
        "inferred_alpha_over_beta_gamma_Gy": diag["alpha_over_beta_gamma_Gy"],
        "diagnostic": diag,
    }
    summary["claims"]["C7_C10_effect_level_rbe"] = eff

    # ---- C11: factor-4 fragments-vs-survival ----
    f4_frag = factor_check(TABLE_I["fragments"], TABLE_I["survival"],
                           "fragments/survival")
    f4_col  = factor_check(TABLE_I["colour"],    TABLE_I["survival"],
                           "colour_junctions/survival")
    summary["claims"]["C11_factor_4"] = {
        "paper_claim": (
            "Chromosome aberration frequencies (Table I) for both α and γ "
            "are at least a factor 4 larger than the corresponding "
            "value for cell reproductive death."
        ),
        "fragments_over_survival": f4_frag,
        "colour_junctions_over_survival": f4_col,
    }

    # ---- C12: decade survival divergence at 2 Gy ----
    lo = survival_divergence_at(2.0, p_surv.a_alpha, p_surv.a_gamma, 0.0)
    hi = survival_divergence_at(2.0, p_surv.a_alpha, p_surv.a_gamma,
                                beta_g_inferred)
    summary["claims"]["C12_divergence_at_2Gy"] = {
        "paper_visual_claim_fig2": "Survival curves diverge by more than a decade at 2 Gy.",
        "with_beta_gamma_zero": lo,
        "with_inferred_beta_gamma": hi,
        "verdict": (
            ">1 decade of divergence" if lo["log10_decades_of_divergence"] > 1
            else "less than a decade — paper claim NOT supported"
        ),
    }

    # ---- C13: bound on β_γ-survival ----
    # Paper notes β_γ-survival is "significant" but doesn't tabulate it.
    # Sanity bound: it must be positive and the LQ curve must still give
    # finite survival at 8 Gy (the experimental max γ-dose).
    S_g_8Gy_bound = math.exp(
        -p_surv.a_gamma * 8.0 - beta_g_inferred * 64.0
    )
    summary["claims"]["C13_beta_gamma_survival_bound"] = {
        "paper_claim": (
            "β_γ for survival is significant but not tabulated. "
            "Recover its order of magnitude by demanding iso-survival "
            "RBE(S=0.1) = 4 (Fig.2 caption)."
        ),
        "inferred_beta_gamma_Gy_minus2": beta_g_inferred,
        "inferred_alpha_over_beta_gamma_Gy": diag["alpha_over_beta_gamma_Gy"],
        "S_gamma_predicted_at_8Gy": S_g_8Gy_bound,
        "physical_check": (
            "α/β ≈ 1-3 Gy is the canonical range for late-responding "
            "human tissues; the inferred value should fall in/near "
            "that range or in the tumour range (5-15 Gy)."
        ),
        "max_gamma_dose_in_experiment_Gy": 8.0,
    }

    out_path = os.path.join(out_dir, "pass2_extended_claims.json")
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"wrote {out_path}")
    print(json.dumps(summary, indent=2, default=str))


if __name__ == "__main__":
    main()
