"""
IMK (Integrated Microdosimetric-Kinetic) forward model
Re-implementation of Matsuya et al., Sci Rep 9:9483 (2019) — DOI 10.1038/s41598-019-45960-z

Equations follow the main paper numbering:
- Eq (1): cell surviving fraction under N fractions / arbitrary dose-time profile, DNA-TEs only.
- Eq (2): continuous-irradiation closed form with Lea-Catcheside time factor.
- Eq (3): Lea-Catcheside time factor F.
- Eq (5): non-targeted (intercellular communication) contribution.
- Eq (6): combined survival = exp(-(w_T + w_NT)).

This module is forward-only: it consumes the published parameter set from
Table 1 of the paper and emits predicted survival curves. No new fits.

Author: Ollie (subagent) for Rick Stevens, LUCID100 Wave 1 replication.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


# Physical constants
RHO_WATER_G_PER_CM3 = 1.0  # g/cm^3
DOMAIN_RADIUS_UM = 0.5  # µm (Matsuya 2019, set as 0.5 µm)


def gamma_from_yD(yD_keV_per_um: float, rd_um: float = DOMAIN_RADIUS_UM,
                  rho_g_per_cm3: float = RHO_WATER_G_PER_CM3) -> float:
    """
    γ = yD / (ρ π rd^2)  in Gy.

    Units: yD in keV/µm, rd in µm, ρ in g/cm³ → γ in Gy.

    Use the standard MK conversion: 1 keV/µm deposited in a sphere of radius rd (µm)
    in water of density ρ (g/cm³) gives a specific energy z (Gy) of
        z[Gy] = (yD[keV/µm] / (ρ[g/cm³] · π · rd²[µm²])) · (1.602e-7)
    so γ = z / 1 event.

    Numerical constant: keV → J: 1 keV = 1.602176634e-16 J.
    Mass of sphere = ρ · (4/3)π rd³  with ρ in g/cm³ converted to kg/µm³:
        ρ[kg/µm³] = ρ[g/cm³] · 1e-15
    z (Gy = J/kg) = E[J] / m[kg].
    For a track-length 2 rd (chord average) carrying yD keV/µm of LET,
        E = yD · 2 rd · 1.602176634e-16  J
        m = ρ · (4/3) π rd^3 · 1e-15  kg
        z = E/m = (yD · 2 rd · 1.602e-16) / (ρ · (4/3) π rd^3 · 1e-15)
          = 3 yD · 1.602e-16 / (2 π ρ rd² · 1e-15)
          = (3/2π) · yD / (ρ rd²) · (1.602e-16 / 1e-15)
          = (3/2π) · yD / (ρ rd²) · 0.1602    [Gy]
    Matsuya uses the simplified form  γ = yD / (ρ π rd²)  *with implicit units*,
    matching the original Hawkins MK formulation; concrete numeric scaling is
    absorbed into β0 by construction (β0 here is what's fit, not "intrinsic" β).
    """
    # The paper uses the symbolic formula γ = yD/(ρ π rd²); the term γβ0 multiplies dose
    # in Eq (2). Since (α0, β0, αb, βb, δ) in Table 1 are *measured* fit parameters,
    # they have absorbed any unit conventions of the original code, and γ should be
    # computed with the same convention. Numerically:
    return yD_keV_per_um / (rho_g_per_cm3 * math.pi * rd_um ** 2)


@dataclass
class IMKParams:
    """Per-cell, per-field IMK parameter set (Table 1 of Matsuya 2019)."""
    name: str  # e.g. "AGO1522 / MF"
    alpha0: float  # Gy^-1, DNA-TE linear term
    beta0: float   # Gy^-2, DNA-TE quadratic term
    apc: float     # h^-1, (a+c) = SLDR transition rate
    yD: float      # keV/µm, dose-mean lineal energy (used to build γ)
    alpha_b: float  # Gy^-1, IC linear coefficient
    beta_b: float   # Gy^-2, IC quadratic coefficient
    delta: float    # dimensionless, IC efficiency for non-hit cells

    @property
    def gamma(self) -> float:
        return gamma_from_yD(self.yD)


# ---------- Table 1 parameter sets ------------------------------------------

# yD values (main text, §Monte Carlo simulation to calculate yD value)
YD_INFIELD_KEV_PER_UM = 4.393
YD_OUTOFFIELD_KEV_PER_UM = 4.769

# AGO1522 — Table 1
AGO_MF = IMKParams(
    name="AGO1522 / Modulated Field (half-field, in-field)",
    alpha0=0.363, beta0=0.011, apc=0.034,
    yD=YD_INFIELD_KEV_PER_UM,
    alpha_b=0.388, beta_b=0.031, delta=0.617,
)
AGO_UF = IMKParams(
    name="AGO1522 / Uniform Field",
    alpha0=0.388, beta0=0.081, apc=1.684,
    yD=YD_INFIELD_KEV_PER_UM,
    alpha_b=0.388, beta_b=0.031, delta=0.617,
)
# DU145 — Table 1
DU145_MF = IMKParams(
    name="DU145 / Modulated Field (half-field, in-field)",
    alpha0=0.032, beta0=0.039, apc=2.509,
    yD=YD_INFIELD_KEV_PER_UM,
    alpha_b=0.041, beta_b=0.023, delta=0.470,
)
DU145_UF = IMKParams(
    name="DU145 / Uniform Field",
    alpha0=0.022, beta0=0.041, apc=1.506,
    yD=YD_INFIELD_KEV_PER_UM,
    alpha_b=0.041, beta_b=0.023, delta=0.470,
)


# ---------- Time factor & DNA-TE survival ------------------------------------

def lea_catcheside_F(apc: float, T_h: float) -> float:
    """
    Eq (3a): F = (2 / ((a+c)² T²)) · [(a+c) T + exp(-(a+c) T) - 1].

    Limits: F → 1 when (a+c)T → 0 (instantaneous), F → 0 when (a+c)T → ∞ (full repair).
    Robust to small (a+c)T via series expansion.
    """
    x = apc * T_h
    if x < 1e-6:
        # Taylor: F ≈ 1 - x/3 + x²/12 - x³/60 + ...
        return 1.0 - x / 3.0 + x ** 2 / 12.0 - x ** 3 / 60.0
    return 2.0 * (x + math.exp(-x) - 1.0) / (x ** 2)


def survival_TE_continuous(D: float, T_h: float, p: IMKParams) -> float:
    """
    Eq (2): continuous irradiation, dose D delivered in time T (hours), DNA-TEs only.
        -ln S_T = (α0 + γ β0) D + F β0 D²
    """
    F = lea_catcheside_F(p.apc, T_h)
    minus_lnS = (p.alpha0 + p.gamma * p.beta0) * D + F * p.beta0 * D ** 2
    return math.exp(-minus_lnS)


def survival_TE_fractions(doses_per_subinterval, dt_h: float, p: IMKParams) -> float:
    """
    Eq (1): N sub-intervals of length ΔT each delivering dose Dn.
        -ln S_T = Σ_n [(α0 + γβ0) Dn ΔT + β0 (Dn ΔT)²]
                + 2 Σ_{n<m} β0 exp(-(m-n)(a+c)ΔT) Dn Dm ΔT²

    Note: in the paper, Dn is *dose-rate* (Gy/h) within sub-interval ΔT, so the dose
    in interval n is (Dn · ΔT). For convenience here we let `doses_per_subinterval[n]`
    be the *absorbed dose in interval n* (Gy), i.e. (Dn · ΔT) already. The kernel
    becomes:
        -ln S_T = Σ (α0 + γβ0) δD_n + β0 (δD_n)²
                + 2 Σ_{n<m} β0 exp(-(m-n)(a+c)ΔT) δD_n δD_m
    which is equivalent to the paper since δD_n = Dn · ΔT.
    """
    dD = np.asarray(doses_per_subinterval, dtype=float)
    N = dD.size
    if N == 0:
        return 1.0
    apc = p.apc
    # diagonal
    lin = (p.alpha0 + p.gamma * p.beta0) * dD.sum()
    quad_diag = p.beta0 * (dD ** 2).sum()
    # cross terms (n<m)
    cross = 0.0
    for n in range(N - 1):
        # vectorize the inner sum
        m = np.arange(n + 1, N)
        weights = np.exp(-(m - n) * apc * dt_h)
        cross += float(np.sum(weights * dD[n] * dD[m]))
    quad_cross = 2.0 * p.beta0 * cross
    minus_lnS = lin + quad_diag + quad_cross
    return math.exp(-minus_lnS)


# ---------- NTE / IC contribution -------------------------------------------

def f_h_IF(D_IF: float, p: IMKParams) -> float:
    """Eq (NTE): hit probability of an in-field cell, fh(D)_IF = 1 - exp(-(αb + γIF βb)D - βb D²)."""
    arg = (p.alpha_b + p.gamma * p.beta_b) * D_IF + p.beta_b * D_IF ** 2
    return 1.0 - math.exp(-arg)


def f_b_star(D_star: float, gamma_star: float, p: IMKParams) -> float:
    """Eq (NTE): non-hit fraction at site *, fb(D)_* = exp(-(αb + γ* βb)D - βb D²)."""
    arg = (p.alpha_b + gamma_star * p.beta_b) * D_star + p.beta_b * D_star ** 2
    return math.exp(-arg)


def survival_NT(D_IF: float, D_star: float, gamma_star: float, p: IMKParams) -> float:
    """
    Eq (5):
        -ln S_NT = δ · [1 - exp(-(αb + γIF βb) D_IF - βb D_IF²)]
                   · exp(-(αb + γ* βb) D_* - βb D_*²)
    """
    hit_IF = f_h_IF(D_IF, p)
    nonhit_star = f_b_star(D_star, gamma_star, p)
    minus_lnS = p.delta * hit_IF * nonhit_star
    return math.exp(-minus_lnS)


# ---------- Combined cell survival ------------------------------------------

def survival_total_continuous(D: float, T_h: float, p_TE: IMKParams,
                              p_IC: IMKParams,
                              field: str = "in") -> float:
    """
    Eq (6): combined survival = S_T · S_NT.

    `field` ∈ {"in", "out"}:
      - "in":  in-field cells. D_IF = D_* = D, γ_* = γ_IF (= γ(yD_in)).
      - "out": out-of-field cells. D_* = 0 OR the OOF received dose; γ_* = γ_OOF.
              For pure-shielded OOF cells under half-field, D_OOF ≈ 0 and the
              only killing is via IC from in-field hits.
    """
    if field == "in":
        S_T = survival_TE_continuous(D, T_h, p_TE)
        S_NT = survival_NT(D_IF=D, D_star=D, gamma_star=p_TE.gamma, p=p_IC)
    elif field == "out":
        S_T = 1.0  # negligible direct TE for shielded cells
        gamma_oof = gamma_from_yD(YD_OUTOFFIELD_KEV_PER_UM)
        S_NT = survival_NT(D_IF=D, D_star=0.0, gamma_star=gamma_oof, p=p_IC)
    else:
        raise ValueError("field must be 'in' or 'out'")
    return S_T * S_NT


def survival_total_fractions(dD_per_sub, dt_h: float, p_TE: IMKParams,
                             p_IC: IMKParams, field: str = "in") -> float:
    """Multi-fraction / arbitrary dose-time pattern (Eq (1) + Eq (5))."""
    dD = np.asarray(dD_per_sub, dtype=float)
    D_total = float(dD.sum())
    if field == "in":
        S_T = survival_TE_fractions(dD, dt_h, p_TE)
        S_NT = survival_NT(D_IF=D_total, D_star=D_total, gamma_star=p_TE.gamma, p=p_IC)
    elif field == "out":
        S_T = 1.0
        gamma_oof = gamma_from_yD(YD_OUTOFFIELD_KEV_PER_UM)
        S_NT = survival_NT(D_IF=D_total, D_star=0.0, gamma_star=gamma_oof, p=p_IC)
    else:
        raise ValueError("field must be 'in' or 'out'")
    return S_T * S_NT


# ---------- Convenience curves -----------------------------------------------

def dose_response_curve(p_TE: IMKParams, p_IC: IMKParams,
                        doses: np.ndarray, dose_rate_Gy_per_min: float = 0.59,
                        field: str = "in") -> np.ndarray:
    """Compute survival across a dose array at a constant single-dose dose-rate."""
    dr_Gy_per_h = dose_rate_Gy_per_min * 60.0
    out = np.zeros_like(doses, dtype=float)
    for i, D in enumerate(doses):
        T_h = float(D) / dr_Gy_per_h if D > 0 else 0.0
        out[i] = survival_total_continuous(float(D), T_h, p_TE, p_IC, field=field)
    return out


def split_dose_recovery(p_TE: IMKParams, p_IC: IMKParams,
                        tau_h_array: np.ndarray, D_each: float = 2.0,
                        dose_rate_Gy_per_min: float = 0.59,
                        field: str = "in") -> np.ndarray:
    """
    Two fractions of `D_each` Gy separated by `τ` h, each delivered at the stated
    dose-rate. We discretize each fraction into a single sub-interval at its own
    dose-rate, and put a τ-hour gap in between.
    """
    dr_h = dose_rate_Gy_per_min * 60.0
    T_each = D_each / dr_h
    out = np.zeros_like(tau_h_array, dtype=float)
    for i, tau in enumerate(tau_h_array):
        # Discretize at fine ΔT for the Eq (1) cross-term to register.
        # Use 50 sub-intervals across each fraction + 1 long gap step.
        n_sub = 50
        dt_in = T_each / n_sub
        dD_in = np.full(n_sub, D_each / n_sub)
        # gap: many zero-dose sub-intervals to advance time by τ
        if tau > 0:
            # represent as variable-length sub-intervals -- use same dt by
            # padding zeros, but exponent in Eq (1) depends on (m-n) * dt.
            # To keep dt uniform, set dt = min(dt_in, τ / nzero) and rescale.
            dt = dt_in
            n_zero = max(1, int(round(tau / dt)))
            # First fraction
            dD = np.concatenate([dD_in, np.zeros(n_zero), dD_in])
        else:
            dt = dt_in
            dD = np.concatenate([dD_in, dD_in])
        out[i] = survival_total_fractions(dD, dt, p_TE, p_IC, field=field)
    return out


def fractionated_constant_rate(p_TE: IMKParams, p_IC: IMKParams,
                               total_dose: float, dose_rate_Gy_per_min: float,
                               n_intervals: int = 200,
                               field: str = "in") -> float:
    """Single continuous exposure delivering `total_dose` Gy at the given dose-rate."""
    dr_h = dose_rate_Gy_per_min * 60.0
    T_total = total_dose / dr_h
    dt = T_total / n_intervals
    dD = np.full(n_intervals, total_dose / n_intervals)
    return survival_total_fractions(dD, dt, p_TE, p_IC, field=field)


# ---------- Self-test / smoke check ------------------------------------------

def _smoke_test():
    print("=== IMK forward-model smoke test ===")
    print(f"γ(in-field)  = {gamma_from_yD(YD_INFIELD_KEV_PER_UM):.4f} Gy (symbolic units)")
    print(f"γ(out-field) = {gamma_from_yD(YD_OUTOFFIELD_KEV_PER_UM):.4f} Gy (symbolic units)")
    print()

    # F-limits
    for x in [1e-9, 0.01, 0.1, 1.0, 10.0, 1000.0]:
        F = lea_catcheside_F(x, 1.0)  # apc * T = x
        print(f"  F(apc*T = {x:>6g}) = {F:.6f}")
    print()

    # Single-dose survival landmark: 2 Gy in-field, dose-rate 0.59 Gy/min
    for p_TE, p_IC, label in [
        (AGO_MF, AGO_MF, "AGO MF in-field"),
        (AGO_UF, AGO_UF, "AGO UF in-field"),
        (DU145_MF, DU145_MF, "DU145 MF in-field"),
        (DU145_UF, DU145_UF, "DU145 UF in-field"),
    ]:
        S2 = survival_total_continuous(2.0, 2.0 / 35.4, p_TE, p_IC, field="in")
        S4 = survival_total_continuous(4.0, 4.0 / 35.4, p_TE, p_IC, field="in")
        S10 = survival_total_continuous(10.0, 10.0 / 35.4, p_TE, p_IC, field="in")
        print(f"  {label:25s}  S(2) = {S2:.3f}  S(4) = {S4:.3e}  S(10) = {S10:.3e}")

    # Reduced SLDR check: continuous 4 Gy at 0.05 Gy/min vs 0.59 Gy/min for AGO
    print()
    for rate in [0.59, 0.20, 0.10, 0.05]:
        S_MF = fractionated_constant_rate(AGO_MF, AGO_MF, 4.0, rate, n_intervals=200)
        S_UF = fractionated_constant_rate(AGO_UF, AGO_UF, 4.0, rate, n_intervals=200)
        print(f"  AGO 4 Gy @ {rate:>4} Gy/min   S_MF(in) = {S_MF:.3f}   S_UF(in) = {S_UF:.3f}   "
              f"ratio MF/UF = {S_MF/S_UF:.2f}")

    print()
    print("Qualitative claim 1 (in-field MF survival > UF survival, same dose, same rate)")
    for D in [2, 4, 6, 8, 10]:
        S_MF = survival_total_continuous(D, D / 35.4, AGO_MF, AGO_MF, field="in")
        S_UF = survival_total_continuous(D, D / 35.4, AGO_UF, AGO_UF, field="in")
        verdict = "OK" if S_MF >= S_UF else "FAIL"
        print(f"  AGO D={D:>2} Gy:  S_MF = {S_MF:.3e},  S_UF = {S_UF:.3e},  MF≥UF? {verdict}")


if __name__ == "__main__":
    _smoke_test()
