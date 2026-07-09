"""
TLK (Two-Lesion Kinetics) model replication for Sakata et al., Cancers 13:6046 (2021).
DOI: 10.3390/cancers13236046

Implements Eqs (3)-(7) of the paper:
    dL1/dt = D(t) Y Sigma1 - lam1 L1 - eta L1 (L1+L2)
    dL2/dt = D(t) Y Sigma2 - lam2 L2 - eta L2 (L1+L2)
    dLf/dt = beta1 lam1 L1 + beta2 lam2 L2 + gamma eta (L1+L2)^2
    SF(t)  = exp(-Lf(t))     [paper's Eq 6 has a typographic flaw; standard TLK
                              is SF = exp(-Lf). The paper text says
                              "SF = exp(-Lf)" via Stewart 2001.]
    FAR(t) = Fmax * (1 - (1 + K*(L1+L2)/Y) * (1 - K/M0) * exp(-K*(L1+L2)/Y))

Units:
    L1, L2  : lesions per cell
    t       : hours
    Sigma1, Sigma2 : Gy^-1 Gbp^-1
    Y       : Gbp per cell (DNA content) = 6.4 Gbp for human diploid
    lam1, lam2, eta : h^-1
    beta1, beta2, gamma : dimensionless
    D(t)    : Gy/h, set to 60 Gy/h until target dose is reached, then 0
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp


# ---------------------------------------------------------------------------
# Published constants (Sakata et al. 2021)
# ---------------------------------------------------------------------------

# Total human DNA per cell (the paper uses 6.4 Gbp / 46 chromosomes -> M0 ~139 Mbp)
Y_GBP = 6.4

# Random-breakage FAR constants (paper section 2.2.3)
F_MAX = 1.0
M0_MBP = 139.0   # Mbp average DNA length per chromosome
K_MBP = 1.0      # Mbp detection limit (FAR fiducial marker)

# Dose rate during irradiation
DOSE_RATE = 60.0  # Gy/h

# Default integration end time (= 14 d post-irradiation, used for SF eval)
T_END_SF = 336.0  # hours

# Published Table 1 (optimized) parameters
TABLE1 = dict(
    lam1=3.36,         # h^-1
    lam2=0.99e-2,      # h^-1
    eta=4.58e-6,       # h^-1
    beta1=0.0,         # forced to 0 by paper
    beta2=2.75e-2,
    gamma=0.39,
)

# Simulated initial DSB yields from paper Section 3.2 and Discussion
# complex-DSB total = DSB+ + DSB++ with DSB+/DSB++ ratio ~ 1.44 (0 mm), 1.13 (32 mm)
# Sigma2 = DSB+ + 2*DSB++
def _sigma2_from_complex(complex_total: float, ratio: float) -> float:
    """ratio = DSB+/DSB++; return Sigma2 = DSB+ + 2*DSB++."""
    dsbpp = complex_total / (1.0 + ratio)
    dsbp = ratio * dsbpp
    return dsbp + 2.0 * dsbpp

# Simple DSB yields (Gbp^-1 Gy^-1)
SIGMA1_0MM = 4.11
SIGMA1_32MM = 4.69
SIGMA2_0MM = _sigma2_from_complex(0.74, 1.44)   # ~1.04
SIGMA2_32MM = _sigma2_from_complex(1.04, 1.13)  # ~1.53


# ---------------------------------------------------------------------------
# Core ODE
# ---------------------------------------------------------------------------

def dose_rate(t: float, t_stop: float) -> float:
    """Constant dose rate until t_stop, then 0."""
    return DOSE_RATE if t < t_stop else 0.0


def tlk_rhs(t: float, y: np.ndarray, params: dict, t_stop: float,
            sigma1: float, sigma2: float) -> np.ndarray:
    L1, L2, Lf = y
    L_sum = L1 + L2
    Dt = dose_rate(t, t_stop)
    src1 = Dt * Y_GBP * sigma1
    src2 = Dt * Y_GBP * sigma2

    dL1 = src1 - params["lam1"] * L1 - params["eta"] * L1 * L_sum
    dL2 = src2 - params["lam2"] * L2 - params["eta"] * L2 * L_sum
    dLf = (params["beta1"] * params["lam1"] * L1
           + params["beta2"] * params["lam2"] * L2
           + params["gamma"] * params["eta"] * L_sum * L_sum)
    return np.array([dL1, dL2, dLf])


def simulate(dose_Gy: float, params: dict, sigma1: float, sigma2: float,
             t_end: float = T_END_SF, t_eval: np.ndarray | None = None,
             rtol: float = 1e-8, atol: float = 1e-10):
    """Integrate the TLK ODE for one (dose, sigma) combination.

    Returns the solve_ivp solution object with .t, .y rows = [L1, L2, Lf].
    """
    if dose_Gy <= 0:
        if t_eval is None:
            t_eval = np.array([0.0, t_end])
        # No irradiation: L1=L2=Lf=0 for all time
        y_arr = np.zeros((3, len(t_eval)))
        class _Stub:
            t = t_eval
            y = y_arr
            success = True
        return _Stub()

    t_stop = dose_Gy / DOSE_RATE  # hours to deliver target dose at 60 Gy/h
    y0 = np.zeros(3)

    # Two-phase integration: tight steps during irradiation, then post-irradiation.
    # Phase 1: 0 -> t_stop with small max_step
    phase1_eval = None
    if t_eval is not None:
        phase1_eval = t_eval[t_eval <= t_stop]
        if phase1_eval.size == 0 or phase1_eval[-1] < t_stop:
            phase1_eval = np.concatenate([phase1_eval, [t_stop]])
    sol1 = solve_ivp(
        tlk_rhs, (0.0, t_stop), y0,
        args=(params, t_stop, sigma1, sigma2),
        method="LSODA", rtol=rtol, atol=atol,
        t_eval=phase1_eval, max_step=max(t_stop / 200.0, 1e-4),
    )
    if not sol1.success:
        return sol1
    if t_end <= t_stop:
        return sol1

    # Phase 2: t_stop -> t_end, dose-rate = 0, much smoother; use LSODA stiff-aware
    phase2_eval = None
    if t_eval is not None:
        phase2_eval = t_eval[t_eval > t_stop]
        if phase2_eval.size == 0 or phase2_eval[-1] < t_end:
            phase2_eval = np.concatenate([phase2_eval, [t_end]])
    y0_2 = sol1.y[:, -1]
    sol2 = solve_ivp(
        tlk_rhs, (t_stop, t_end), y0_2,
        args=(params, t_stop, sigma1, sigma2),
        method="LSODA", rtol=rtol, atol=atol,
        t_eval=phase2_eval,
    )
    if not sol2.success:
        return sol2

    # Stitch
    class _Combined:
        success = True
    out = _Combined()
    out.t = np.concatenate([sol1.t, sol2.t])
    out.y = np.concatenate([sol1.y, sol2.y], axis=1)
    return out


def sf_at_dose(dose_Gy: float, params: dict, sigma1: float, sigma2: float,
               t_end: float = T_END_SF) -> float:
    """Return SF = exp(-Lf(t_end)) for a single delivered dose."""
    if dose_Gy <= 0:
        return 1.0
    sol = simulate(dose_Gy, params, sigma1, sigma2, t_end=t_end,
                   t_eval=np.array([0.0, t_end]))
    Lf = sol.y[2, -1]
    return float(np.exp(-Lf))


def far_curve(dose_Gy: float, params: dict, sigma1: float, sigma2: float,
              times_h: np.ndarray) -> np.ndarray:
    """Compute relative FAR(t)/FAR(t0) over given times (post-irradiation hours).

    times_h are measured from the END of irradiation; we shift internally.
    """
    t_stop = dose_Gy / DOSE_RATE
    times_h = np.asarray(times_h, dtype=float)
    # Build absolute time grid from start of irradiation
    t_eval = np.concatenate([[0.0, t_stop], t_stop + times_h])
    t_eval = np.unique(np.sort(t_eval))
    t_end = float(t_eval[-1]) + 1e-6
    sol = simulate(dose_Gy, params, sigma1, sigma2, t_end=t_end,
                   t_eval=t_eval)
    # Use sol.t / sol.y (may include phase boundary duplicate; dedupe)
    sol_t, idx = np.unique(sol.t, return_index=True)
    L1 = sol.y[0][idx]
    L2 = sol.y[1][idx]
    Lsum_per_gbp = (L1 + L2) / Y_GBP  # lesions per Gbp

    # FAR(t) per Eq 7
    K_gbp = K_MBP / 1000.0     # 0.001 Gbp
    M0_gbp = M0_MBP / 1000.0   # 0.139 Gbp
    arg = K_gbp * Lsum_per_gbp
    far_abs = F_MAX * (1.0 - (1.0 + arg) * (1.0 - K_gbp / M0_gbp) * np.exp(-arg))

    # interpolate at requested absolute times (relative to start of irradiation)
    abs_targets = t_stop + times_h
    far_at_t = np.interp(abs_targets, sol_t, far_abs)
    far_t0 = float(np.interp(t_stop, sol_t, far_abs))
    if far_t0 <= 0:
        return np.zeros_like(far_at_t)
    return far_at_t / far_t0


# ---------------------------------------------------------------------------
# Convenience: condition lookup
# ---------------------------------------------------------------------------

def sigmas_for(pmma_mm: int) -> tuple[float, float]:
    if pmma_mm == 0:
        return SIGMA1_0MM, SIGMA2_0MM
    if pmma_mm == 32:
        return SIGMA1_32MM, SIGMA2_32MM
    raise ValueError(f"Unknown PMMA thickness {pmma_mm}; only 0 and 32 mm reported.")
