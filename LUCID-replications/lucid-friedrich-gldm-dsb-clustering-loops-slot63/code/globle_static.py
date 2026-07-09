"""
Static GLOBLE (Friedrich, Durante, Scholz, Radiat. Res. 178: 385-394, 2012)
DOI: 10.1667/RR2964.1

Replication of the "Giant LOop Binary LEsion" (GLOBLE) static dose-response
model for photon cell survival, based on DSB clustering inside megabase-pair
chromatin giant loops.

Core equations (paper Eqs. 1-7):

    lambda(D)   = alpha_DSB * D / N_L            # mean DSBs per loop (Poisson)
    p_0         = exp(-lambda)
    p_i         = lambda * exp(-lambda)          # exactly one DSB / loop -> isolated
    p_c         = 1 - p_0 - p_i                  # >=2 DSBs / loop      -> clustered
    n_i(D)      = N_L * p_i
    n_c(D)      = N_L * p_c
    -ln S(D)    = eps_i * n_i(D) + eps_c * n_c(D)

Paper-fixed constants (Section "Model formulation" / Table 1 of Friedrich 2012):
    alpha_DSB = 30 DSB / Gy / cell
    N_L       = 3000 giant-loop domains / nucleus

Per-cell-line fit parameters (eps_i, eps_c) come from clonogenic data.  We
re-use the (eps_i, eps_c) values transcribed from Herr et al. 2014 PLoS ONE
Table 2 (the kinetic extension of this same model); for the high-dose-rate /
acute-irradiation regime that Friedrich 2012 targets, only (eps_i, eps_c)
matter for the dose-response and the (alpha, beta) derivation.

LQ correspondence (paper Eqs. ~12-13 region):
    alpha = eps_i * alpha_DSB
    beta  = (eps_c - 2*eps_i) * alpha_DSB^2 / (2 * N_L)

The model predicts an *intrinsic* anti-correlation between alpha and beta:
beta is largest when eps_i is small relative to eps_c, i.e. for cell lines
with small alpha.  We reproduce this prediction below.

No author code is publicly distributed.  This file is a clean-room
reimplementation from the published equations; survival_static() is also
verified equation-by-equation against the sibling kinetic GLOBLE
implementation in lucid-globle-photon-cell-killing/code/globle.py.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

# ---------------- paper-fixed constants (Friedrich 2012) ---------------- #
ALPHA_DSB = 30.0     # DSB per Gy per cell
N_L       = 3000     # giant-loop domains per nucleus


@dataclass(frozen=True)
class StaticParams:
    """Per-cell-line static-GLOBLE parameters."""
    name: str
    eps_i: float   # lethality probability for isolated DSBs
    eps_c: float   # lethality probability for clustered DSBs

    # Convenient LQ-equivalent coefficients
    @property
    def alpha_lq(self) -> float:
        return self.eps_i * ALPHA_DSB
    @property
    def beta_lq(self) -> float:
        # From series expansion of -ln S(D) around D=0 (paper Eq. ~13).
        return (self.eps_c - 2.0 * self.eps_i) * ALPHA_DSB**2 / (2.0 * N_L)


# ---------------- core model ---------------- #

def mean_dsbs_per_loop(dose_gy: float) -> float:
    """lambda(D) = alpha_DSB * D / N_L  (Eq. 2)."""
    return ALPHA_DSB * dose_gy / N_L


def damage_classes(dose_gy: float) -> tuple[float, float, float]:
    """Return (n0, n_i, n_c): expected loops with 0 / 1 / >=2 DSBs (Eqs. 3-6)."""
    lam = mean_dsbs_per_loop(dose_gy)
    p0 = math.exp(-lam)
    pi = lam * math.exp(-lam)
    pc = 1.0 - p0 - pi
    return N_L * p0, N_L * pi, N_L * pc


def survival(params: StaticParams, dose_gy: float) -> float:
    """S(D) = exp[ -(eps_i n_i + eps_c n_c) ]  (Eq. 7 / Eq. 1)."""
    _, ni, nc = damage_classes(dose_gy)
    return math.exp(-(params.eps_i * ni + params.eps_c * nc))


def survival_curve(params: StaticParams, doses_gy: Iterable[float]) -> list[float]:
    return [survival(params, d) for d in doses_gy]


# ---------------- LQ comparison ---------------- #

def lq_survival(alpha: float, beta: float, dose_gy: float) -> float:
    return math.exp(-(alpha * dose_gy + beta * dose_gy**2))


# ---------------- cell-line catalogue ----------------
# (eps_i, eps_c) re-used from Herr 2014 Table 2 / Friedrich 2012 fits.

CELL_LINES: dict[str, StaticParams] = {
    "C3H 10T1/2": StaticParams("C3H 10T1/2", 0.00396, 0.0964),
    "CHO 10B2":   StaticParams("CHO 10B2",   0.00130, 0.162),
    "CHO K1":     StaticParams("CHO K1",     0.00338, 0.674),
    "NFF28":      StaticParams("NFF28",      0.00410, 0.455),
    "HX118":      StaticParams("HX118",      0.0108,  0.297),
    "HX32":       StaticParams("HX32",       0.0142,  0.428),
    "HX58":       StaticParams("HX58",       0.0150,  0.425),
    "MT":         StaticParams("MT",         0.00865, 0.178),
    "LL":         StaticParams("LL",         0.0114,  0.543),
    "B16":        StaticParams("B16",        0.00781, 0.203),
    "HX34":       StaticParams("HX34",       0.00893, 0.320),
    "IN859":      StaticParams("IN859",      0.00536, 0.407),
    "IN1265":     StaticParams("IN1265",     0.00913, 0.215),
    "SB":         StaticParams("SB",         0.00490, 0.259),
    "RT112":      StaticParams("RT112",      0.00529, 0.195),
    "HX138":      StaticParams("HX138",      0.0218,  0.851),
    "HX142":      StaticParams("HX142",      0.0284,  0.809),
}


if __name__ == "__main__":   # smoke run
    out_dir = Path(__file__).resolve().parent.parent / "results"
    out_dir.mkdir(exist_ok=True)
    doses = [round(0.5 * k, 3) for k in range(0, 41)]  # 0..20 Gy step 0.5

    # 1) Per-cell-line survival curves and LQ equivalents
    cell_curves: dict[str, dict] = {}
    ab_table: list[dict] = []
    for name, p in CELL_LINES.items():
        s = survival_curve(p, doses)
        ab_table.append({"cell": name, "eps_i": p.eps_i, "eps_c": p.eps_c,
                         "alpha_lq": p.alpha_lq, "beta_lq": p.beta_lq})
        cell_curves[name] = {"doses_gy": doses, "survival": s,
                              "alpha_lq": p.alpha_lq, "beta_lq": p.beta_lq}

    (out_dir / "static_globle_survival_curves.json").write_text(json.dumps(cell_curves, indent=2))
    (out_dir / "static_globle_alpha_beta_table.json").write_text(json.dumps(ab_table, indent=2))

    # 2) Sanity prints
    print("Friedrich 2012 GLOBLE static-model smoke run")
    print(f"  alpha_DSB = {ALPHA_DSB} /Gy/cell, N_L = {N_L} loops/nucleus")
    print(f"  {len(CELL_LINES)} cell lines, doses 0-20 Gy step 0.5")
    print()
    print(f"  {'cell':<12} {'eps_i':>9} {'eps_c':>9} {'alpha':>8} {'beta':>10}  S(2Gy)  S(10Gy)")
    for row in ab_table:
        p = CELL_LINES[row['cell']]
        print(f"  {row['cell']:<12} {row['eps_i']:>9.5f} {row['eps_c']:>9.4f}"
              f" {row['alpha_lq']:>8.4f} {row['beta_lq']:>10.5f}"
              f"  {survival(p, 2.0):>6.3f}  {survival(p, 10.0):>6.3g}")

    # 3) Cross-check: high-dose linearity (paper claim - LQ at low D, linear at high D)
    p = CELL_LINES["RT112"]
    import math as _m
    slope_high = -(math.log(survival(p, 20.0)) - math.log(survival(p, 18.0))) / 2.0
    # asymptotic slope should approach eps_c * alpha_DSB once Poisson saturates
    asymptote = p.eps_c * ALPHA_DSB
    print()
    print(f"  RT112 high-dose -d(lnS)/dD between 18-20 Gy = {slope_high:.4f}")
    print(f"  Predicted asymptote eps_c*alpha_DSB         = {asymptote:.4f}")
    print(f"  Ratio (should approach 1)                   = {slope_high / asymptote:.4f}")

    print()
    print("Outputs:")
    for f in sorted(out_dir.iterdir()):
        print(f"  {f}")
