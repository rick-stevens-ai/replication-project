"""UNIVERSE — sparsely ionizing radiation core.

Re-implements the parts of the UNIVERSE model that are explicitly defined in the
text of Liew et al. 2022 (Int. J. Mol. Sci. 23, 6268) Section 5.2:

    S = (1 - K_iDSB)^N_iDSB * (1 - K_cDSB)^N_cDSB         (Eq. 5)
    <N_tDSB>  = alpha_DSB * D,         alpha_DSB = 30 / Gy / cell
    chromatin = N_dom independent "giant-loop" domains (~2 Mbp each)
                -> N_dom = 6e9 bp / 2e6 bp = 3000 domains by default

For sparsely ionizing radiation the dose is treated as homogeneous: each induced
DSB is dropped into a domain uniformly at random.  Domains containing exactly
one DSB are isolated (iDSB); domains containing >= 2 DSB are complex / clustered
(cDSB).

When repair kinetics are switched on the total irradiation time T_irr is split
into N_t = 100 time steps, partial doses D/N_t are deposited at each step, each
DSB receives an exponentially distributed lifetime with the appropriate
half-life, any DSB landing on a domain that already contains a DSB gets the
cDSB lifetime, and a misrepair event (with probability K_iDSB or K_cDSB per
repair) kills the cell.  Surviving cells contribute their end-of-time Eq. 5
survival to the population average.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


ALPHA_DSB_DEFAULT = 30.0           # DSB per Gy per cell (Liang 2017, Stewart 2011)
N_DOMAINS_DEFAULT = 3000           # 6 Gbp / 2 Mbp ~ 3000 giant-loop domains
N_TIME_STEPS_DEFAULT = 100         # paper says N_t = 100
LN2 = float(np.log(2.0))


@dataclass
class CellParams:
    """Endpoint-dependent UNIVERSE parameters (Table 1 of Liew et al. 2022)."""

    name: str
    K_iDSB: float
    K_cDSB: float
    T_iDSB_half_min: float | None    # None -> "no repair" parameter set
    T_cDSB_half_min: float | None
    alpha_DSB: float = ALPHA_DSB_DEFAULT
    n_domains: int = N_DOMAINS_DEFAULT


# ---------------------------------------------------------------------------
# Table 1 reproductions
# ---------------------------------------------------------------------------
PARAMS_DU145 = CellParams(
    name="DU145",
    K_iDSB=5.9e-3,
    K_cDSB=0.17,
    T_iDSB_half_min=4.0,
    T_cDSB_half_min=100.0,
)

PARAMS_RSC_WITH_REPAIR = CellParams(
    # Rat spinal cord, parameters fitted while considering repair
    name="RSC_with_repair",
    K_iDSB=3.5e-5,
    K_cDSB=9.8e-3,
    T_iDSB_half_min=11.4,
    T_cDSB_half_min=129.6,
)

PARAMS_RSC_NO_REPAIR = CellParams(
    # Rat spinal cord, parameters fitted ignoring repair (Table 1 lists K_iDSB
    # = 6.5e-3; text Section 2 paragraph 4 reports K_iDSB = 6.3e-5.  Both
    # values appear in the published article.  We default to the Table 1
    # value because Tables are usually the curated reference.)
    name="RSC_no_repair",
    K_iDSB=6.5e-3,
    K_cDSB=8.5e-3,
    T_iDSB_half_min=None,
    T_cDSB_half_min=None,
)


# ---------------------------------------------------------------------------
# Core photon survival
# ---------------------------------------------------------------------------
def expected_dsb_count(dose_Gy: float, params: CellParams) -> float:
    """alpha_DSB * D (Section 5.2)."""
    return params.alpha_DSB * dose_Gy


def sample_iDSB_cDSB(
    n_dsb: int, n_domains: int, rng: np.random.Generator
) -> tuple[int, int]:
    """Drop n_dsb DSB into n_domains domains uniformly.  Return (N_iDSB, N_cDSB)."""
    if n_dsb <= 0:
        return 0, 0
    occupancies = rng.integers(0, n_domains, size=n_dsb)
    counts = np.bincount(occupancies, minlength=n_domains)
    n_iDSB = int(np.sum(counts == 1))
    n_cDSB = int(np.sum(counts >= 2))
    return n_iDSB, n_cDSB


def survival_no_repair(
    dose_Gy: float,
    params: CellParams,
    n_iter: int = 10_000,
    rng: np.random.Generator | None = None,
) -> float:
    """Eq. 5 with Poisson DSB sampling.  No repair kinetics (T -> infty limit)."""
    rng = rng or np.random.default_rng()
    mean_dsb = expected_dsb_count(dose_Gy, params)
    if mean_dsb <= 0:
        return 1.0
    n_dsb_per_iter = rng.poisson(mean_dsb, size=n_iter)
    surv = np.empty(n_iter, dtype=np.float64)
    for k, n in enumerate(n_dsb_per_iter):
        ni, nc = sample_iDSB_cDSB(int(n), params.n_domains, rng)
        surv[k] = (1.0 - params.K_iDSB) ** ni * (1.0 - params.K_cDSB) ** nc
    return float(surv.mean())


def survival_with_repair(
    dose_Gy: float,
    dose_rate_Gy_per_min: float,
    params: CellParams,
    n_iter: int = 5_000,
    n_time_steps: int = N_TIME_STEPS_DEFAULT,
    rng: np.random.Generator | None = None,
) -> float:
    """Repair-kinetics Monte Carlo for sparsely ionizing radiation.

    Inputs:
        dose_Gy            -- total dose D
        dose_rate_Gy_per_min -- applied dose rate (paper sometimes uses Gy/s;
                                we convert internally to minutes because half-
                                lives are quoted in minutes)
        params             -- CellParams.  Must have T_iDSB_half_min / T_cDSB_half_min.

    Returns the population-averaged surviving fraction.  Iterations in which any
    DSB triggers a misrepair are counted with survival = 0.
    """
    if params.T_iDSB_half_min is None or params.T_cDSB_half_min is None:
        raise ValueError(
            f"survival_with_repair: cell params '{params.name}' have no repair times; "
            "use survival_no_repair instead."
        )
    if dose_rate_Gy_per_min <= 0:
        raise ValueError("dose rate must be positive")
    rng = rng or np.random.default_rng()

    T_irr = dose_Gy / dose_rate_Gy_per_min               # total irradiation time, min
    dt = T_irr / n_time_steps                            # min per step
    partial_dose = dose_Gy / n_time_steps                # Gy per step
    mean_dsb_per_step = expected_dsb_count(partial_dose, params)

    # Convert half-lives to rate constants 1/min for exponential lifetime draws
    lam_i = LN2 / params.T_iDSB_half_min
    lam_c = LN2 / params.T_cDSB_half_min
    K_i = params.K_iDSB
    K_c = params.K_cDSB
    n_dom = params.n_domains

    surv_acc = 0.0
    for _ in range(n_iter):
        # Domain state: count of DSB and lifetime
        # We represent each currently-alive DSB as (domain_idx, death_time, kind)
        # but to stay fast we maintain per-domain counts and a list of (death_time, kind, domain_idx)
        active = []  # list of [death_time, kind('i' or 'c'), domain_idx]
        dom_count = np.zeros(n_dom, dtype=np.int32)
        misrepair = False

        for step in range(n_time_steps):
            t_now = step * dt
            # Step 1: deposit partial_dose worth of DSB at t = t_now (start of step)
            n_new = rng.poisson(mean_dsb_per_step)
            if n_new > 0:
                new_dom = rng.integers(0, n_dom, size=n_new)
                for d in new_dom:
                    d = int(d)
                    prev = dom_count[d]
                    dom_count[d] += 1
                    if prev == 0:
                        # New isolated DSB -- iDSB half-life
                        life = rng.exponential(1.0 / lam_i)
                        active.append([t_now + life, "i", d])
                    else:
                        # Domain already had DSB -- becomes (or remains) cDSB.
                        # The newly added break gets a cDSB lifetime.
                        life = rng.exponential(1.0 / lam_c)
                        active.append([t_now + life, "c", d])
                        # And the previously-isolated DSB needs to be relabelled
                        # to cDSB (its lifetime redrawn from cDSB), per paper text.
                        if prev == 1:
                            # Find that single existing DSB on this domain and
                            # redraw its lifetime as cDSB.
                            for entry in active:
                                if entry[2] == d and entry[1] == "i":
                                    entry[0] = t_now + rng.exponential(1.0 / lam_c)
                                    entry[1] = "c"
                                    break

            # Step 2: process repairs whose death_time <= t_now + dt
            t_end = t_now + dt
            remaining = []
            for entry in active:
                if entry[0] <= t_end:
                    # Repair event.  Misrepair probability = K_i / K_c per kind.
                    k = K_i if entry[1] == "i" else K_c
                    if rng.random() < k:
                        misrepair = True
                        break
                    dom_count[entry[2]] -= 1
                else:
                    remaining.append(entry)
            if misrepair:
                break
            active = remaining

        if misrepair:
            # cell killed by misrepair event
            surv_acc += 0.0
            continue

        # End-of-time: any surviving DSB contribute to Eq. 5 with current iDSB / cDSB classification
        n_iDSB = int(np.sum(dom_count == 1))
        n_cDSB = int(np.sum(dom_count >= 2))
        surv_acc += (1.0 - K_i) ** n_iDSB * (1.0 - K_c) ** n_cDSB

    return surv_acc / n_iter


# ---------------------------------------------------------------------------
# Dose-for-effect / RBE helpers
# ---------------------------------------------------------------------------
def dose_for_survival(
    target_S: float,
    surv_callable,
    d_lo: float = 0.01,
    d_hi: float = 80.0,
    tol: float = 1e-3,
    max_iter: int = 60,
) -> float:
    """Bisection: find dose D such that surv_callable(D) == target_S.

    surv_callable(dose) -> survival fraction (monotone decreasing in dose).
    """
    s_lo = surv_callable(d_lo)
    s_hi = surv_callable(d_hi)
    if s_hi > target_S:
        return float("nan")   # could not reach target
    if s_lo < target_S:
        return d_lo
    for _ in range(max_iter):
        d_mid = 0.5 * (d_lo + d_hi)
        s_mid = surv_callable(d_mid)
        if abs(s_mid - target_S) < tol:
            return d_mid
        if s_mid > target_S:
            d_lo = d_mid
        else:
            d_hi = d_mid
    return 0.5 * (d_lo + d_hi)


if __name__ == "__main__":
    # quick sanity check
    rng = np.random.default_rng(20260529)
    for D in [0.5, 1.0, 2.0, 4.0, 8.0]:
        s = survival_no_repair(D, PARAMS_DU145, n_iter=4000, rng=rng)
        print(f"DU145 photon, D={D:5.2f} Gy : S = {s:.4f}")
