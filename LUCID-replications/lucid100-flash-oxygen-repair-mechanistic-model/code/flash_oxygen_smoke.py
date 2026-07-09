"""LUCID-100 #27 — Liew et al. 2021 IJROBP (DOI 10.1016/j.ijrobp.2020.12.048).

Minimal mechanistic smoke replication of the dynamic UNIVERSE extension for
FLASH-dose-rate radiotherapy. This is NOT a bit-exact reproduction: the paper
is closed access and no source code, supplementary parameter table, or run
configurations were released. The implementation here encodes only the
mechanisms that are clearly described in the public abstract, Liew's open
predecessor papers (Liew 2019, IJMS 20:6054; Liew 2020, IJMS 21:3471), and the
companion FLASH-oxygen-depletion literature cited in the paper's reference
list (Pratx 2019, Petersson 2020, Labarbe 2020).

Modules:
    1. Static UNIVERSE giant-loop DSB stochastic survival
       (alpha_DSB, isolated vs complex lesions, K_iDSB / K_cDSB).
    2. Oxygen-modified DSB induction rate via the
       HRF(O2) = (m*K + [O2]) / (K + [O2])
       parametrization (Liew 2019 eq. 6; m = 2.94, K = 0.129%).
       In the "Deciphering..." paper this becomes time-dependent because
       [O2] is now a state variable, not a constant.
    3. Radiolytic oxygen depletion (ROD): linear-with-dose depletion of
       intracellular [O2] during irradiation, with literature-bound
       depletion coefficient g_ROD (mmHg / Gy, ~0.35-0.7 mmHg/Gy depending
       on the cited model).
    4. Reoxygenation: first-order relaxation of [O2] back to the ambient
       value with time constant tau_reox (~ a few seconds, lit. range).
    5. Repair kinetics: first-order exponential repair of iDSB and cDSB
       with half-lives T_iDSB_half, T_cDSB_half (paper text reports
       distinct fast/slow components; we use representative values
       4 min / 100 min consistent with Liew 2022 UNIVERSE Table 1 DU145).
       Damage that fails to repair before "end of biology" contributes to
       lethality through the (1 - K)^N survival expression.

What this smoke can show qualitatively:
    * Conventional (CONV, ~0.07 Gy/s) vs FLASH (~100 Gy/s) survival under
      normoxia (~21%) and physoxia/hypoxia (~5% / <1%).
    * The "FLASH effect": SF(FLASH) > SF(CONV) emerges when the irradiation
      time is short compared to reoxygenation, so transient hypoxia during
      the FLASH pulse reduces DSB induction.
    * Predicted oxygen-tension dependence: the effect vanishes at very low
      starting [O2] (already hypoxic) and at very high [O2] (no transient
      hypoxia possible).

What this smoke CANNOT do:
    * Reproduce Figures 1-5 / Tables 1-2 of the paper bit-exactly because
      the explicit FLASH endpoint parameter values (g_ROD, tau_reox,
      repair half-lives per endpoint) are NOT in the abstract and the
      supplement is paywalled.
    * Match the in-vivo dose-response fits (mouse tail necrosis, brain,
      lung, intestine) reported by the paper.
    * Validate against the underlying experimental data (Montay-Gruel,
      Favaudon, Vozenin) without their digitized survival/endpoint values.

Run:
    python3 flash_oxygen_smoke.py
Output:
    figures/smoke_flash_vs_conv_oxygen.png
    results/smoke_sweep.csv
    logs/smoke_run.log
Wall clock on CherryRd CPU: ~10-30 s.
"""
from __future__ import annotations

import csv
import json
import math
import os
import sys
import time
from dataclasses import dataclass

import numpy as np

# --- Defaults from the open UNIVERSE literature ---------------------------------
ALPHA_DSB = 30.0           # DSB / Gy / cell at 21% O2 (Liang 2017, Stewart 2011)
N_DOMAINS = 3000           # giant-loop domains = 6 Gbp / 2 Mbp (Liew 2019 eq. 2)

# Hypoxia reduction factor parameters (Liew 2019 eq. 6)
HRF_M = 2.94
HRF_K_PERCENT = 0.129      # K in % O2

# Repair kinetics (representative DU145 values from Liew 2022 IJMS Table 1)
T_IDSB_HALF_MIN = 4.0
T_CDSB_HALF_MIN = 100.0

# Lethality probabilities (DU145 endpoint, illustrative)
K_IDSB = 5.9e-3
K_CDSB = 0.17

# FLASH oxygen-depletion parameters (literature-bounded; the actual values
# used in Liew 2021 are paywalled. These are conservative central estimates
# from Pratx 2019 / Petersson 2020 / Cao 2021 reviews.)
G_ROD_MMHG_PER_GY = 0.42         # radiolytic O2 depletion coefficient
TAU_REOX_S = 5.0                 # reoxygenation time constant (s)

# Atmospheric saturation conversions
#   21 % O2 (cell-culture incubator atmosphere)  ~ 160 mmHg in gas phase,
#   intracellular cell-line typical 7.5 % (~57 mmHg) under "normoxia",
#   physoxia 4 % (~30 mmHg), hypoxia <1 % (<7.6 mmHg).
def percent_O2_to_mmHg(pct: float) -> float:
    """Convert volume percent O2 (gas-phase or pseudo-cell) to partial pressure mmHg."""
    return pct / 21.0 * 160.0  # naive linear scaling; sufficient for smoke


def mmHg_to_percent_O2(mmHg: float) -> float:
    return mmHg / 160.0 * 21.0


# --- Hypoxia reduction factor --------------------------------------------------
def HRF(o2_percent: float) -> float:
    """Liew 2019 eq. 6:  HRF([O2]) = (m*K + [O2]) / (K + [O2])."""
    return (HRF_M * HRF_K_PERCENT + o2_percent) / (HRF_K_PERCENT + o2_percent)


# --- Oxygen dynamics during irradiation ----------------------------------------
def integrate_o2(
    total_dose_Gy: float,
    dose_rate_Gy_per_s: float,
    o2_initial_percent: float,
    g_ROD_mmHg_per_Gy: float = G_ROD_MMHG_PER_GY,
    tau_reox_s: float = TAU_REOX_S,
    n_steps: int = 400,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Integrate
        d[O2]/dt = -g_ROD * dD/dt + ([O2]_amb - [O2]) / tau_reox
    over the irradiation time T_irr = D / R + 5 * tau_reox.

    Returns (t_seconds, dose_Gy(t), o2_percent(t)).
    """
    T_irr_s = total_dose_Gy / dose_rate_Gy_per_s
    T_total_s = T_irr_s + 5.0 * tau_reox_s
    t = np.linspace(0.0, T_total_s, n_steps + 1)
    dt = t[1] - t[0]

    dose_t = np.minimum(dose_rate_Gy_per_s * t, total_dose_Gy)
    dDdt = np.where(t < T_irr_s, dose_rate_Gy_per_s, 0.0)

    o2_amb_mmHg = percent_O2_to_mmHg(o2_initial_percent)
    o2_mmHg = np.empty_like(t)
    o2_mmHg[0] = o2_amb_mmHg
    for i in range(n_steps):
        dO2 = (-g_ROD_mmHg_per_Gy * dDdt[i]
               + (o2_amb_mmHg - o2_mmHg[i]) / tau_reox_s)
        o2_mmHg[i + 1] = max(0.0, o2_mmHg[i] + dt * dO2)
    o2_pct = np.array([mmHg_to_percent_O2(x) for x in o2_mmHg])
    return t, dose_t, o2_pct


# --- UNIVERSE giant-loop survival ---------------------------------------------
def sample_iDSB_cDSB(n_dsb: int, n_dom: int, rng: np.random.Generator) -> tuple[int, int]:
    if n_dsb <= 0:
        return 0, 0
    occ = rng.integers(0, n_dom, size=n_dsb)
    counts = np.bincount(occ, minlength=n_dom)
    return int(np.sum(counts == 1)), int(np.sum(counts >= 2))


def survival_dynamic(
    total_dose_Gy: float,
    dose_rate_Gy_per_s: float,
    o2_initial_percent: float,
    n_iter: int = 4_000,
    n_steps: int = 100,
    rng: np.random.Generator | None = None,
    repair_on: bool = True,
    g_ROD: float = G_ROD_MMHG_PER_GY,
    tau_reox: float = TAU_REOX_S,
) -> dict:
    """Dynamic UNIVERSE: split the irradiation into n_steps, compute the
    *instantaneous* O2 in each step from the ROD/reoxygenation ODE,
    convert it to a step-local HRF, accumulate DSBs into giant-loop domains
    while repairing them with first-order exponential kinetics.

    Returns dict with surviving fraction, mean DSB induced, etc.
    """
    rng = rng or np.random.default_rng(20210104)

    T_irr_s = total_dose_Gy / dose_rate_Gy_per_s
    dt_s = T_irr_s / n_steps                       # irradiation step
    dose_step = total_dose_Gy / n_steps
    lam_i = math.log(2.0) / (T_IDSB_HALF_MIN * 60.0)   # per second
    lam_c = math.log(2.0) / (T_CDSB_HALF_MIN * 60.0)

    # Pre-compute O2 trajectory on a fine grid and pick step centers
    t_fine, _, o2_fine = integrate_o2(
        total_dose_Gy, dose_rate_Gy_per_s, o2_initial_percent,
        g_ROD_mmHg_per_Gy=g_ROD, tau_reox_s=tau_reox, n_steps=400,
    )
    step_times = (np.arange(n_steps) + 0.5) * dt_s
    o2_step = np.interp(step_times, t_fine, o2_fine)
    hrf_step = np.array([HRF(o) for o in o2_step])
    alpha_eff_step = ALPHA_DSB / hrf_step                # DSB / Gy at this step
    mean_dsb_step = alpha_eff_step * dose_step           # expected DSB / step

    sf = np.empty(n_iter)
    total_dsb_iter = np.empty(n_iter)
    for k in range(n_iter):
        # Track per-domain DSB count (decaying with time) plus lethality strikes
        dom_count = np.zeros(N_DOMAINS, dtype=np.int32)
        # List of active breaks: (death_time_s, domain_idx, kind: 0=i, 1=c)
        active: list[list] = []
        n_dsb_total = 0
        misrepair = False
        for s in range(n_steps):
            t_now = s * dt_s
            # Decay step: drop breaks whose lifetime expired before t_now
            kept = []
            for entry in active:
                death, di, kind = entry
                if death <= t_now:
                    # Repair complete; with probability K_? -> lethal misrepair
                    p_misrep = K_IDSB if kind == 0 else K_CDSB
                    if rng.random() < p_misrep:
                        misrepair = True
                    dom_count[di] -= 1
                else:
                    kept.append(entry)
            active = kept
            if misrepair and repair_on:
                # Optimization: dead cell, skip the rest of the deposition.
                # We still need to add the remaining dose contribution to mean
                # DSB count for diagnostics but lethality is already 1.
                pass
            # Deposit Poisson(mean_dsb_step[s]) DSB at t_now into domains
            n_new = int(rng.poisson(mean_dsb_step[s]))
            n_dsb_total += n_new
            if n_new > 0:
                new_dom = rng.integers(0, N_DOMAINS, size=n_new)
                for d in new_dom:
                    d = int(d)
                    prev = dom_count[d]
                    dom_count[d] += 1
                    if repair_on:
                        if prev == 0:
                            life = rng.exponential(1.0 / lam_i)
                            active.append([t_now + life, d, 0])
                        else:
                            life = rng.exponential(1.0 / lam_c)
                            active.append([t_now + life, d, 1])
        # End-of-irradiation snapshot for the Eq. 3/5 survival expression.
        n_iDSB = int(np.sum(dom_count == 1))
        n_cDSB = int(np.sum(dom_count >= 2))
        sf_k = (1.0 - K_IDSB) ** n_iDSB * (1.0 - K_CDSB) ** n_cDSB
        if misrepair and repair_on:
            sf_k = 0.0
        sf[k] = sf_k
        total_dsb_iter[k] = n_dsb_total
    return {
        "SF_mean": float(sf.mean()),
        "SF_std": float(sf.std()),
        "mean_total_DSB": float(total_dsb_iter.mean()),
        "T_irr_s": T_irr_s,
        "o2_min_pct": float(o2_step.min()),
        "o2_init_pct": o2_initial_percent,
    }


# --- Driver --------------------------------------------------------------------
def run_smoke(outdir: str) -> dict:
    os.makedirs(os.path.join(outdir, "figures"), exist_ok=True)
    os.makedirs(os.path.join(outdir, "results"), exist_ok=True)
    os.makedirs(os.path.join(outdir, "logs"), exist_ok=True)

    log_path = os.path.join(outdir, "logs", "smoke_run.log")
    csv_path = os.path.join(outdir, "results", "smoke_sweep.csv")
    fig_path = os.path.join(outdir, "figures", "smoke_flash_vs_conv_oxygen.png")

    t0 = time.time()

    o2_levels = [0.5, 2.0, 5.0, 7.5, 21.0]    # % O2
    doses = [10.0, 20.0]
    dose_rates = {"CONV_0.07Gys": 0.07, "FLASH_100Gys": 100.0}

    rows = []
    rng = np.random.default_rng(20210104)  # paper online publication date
    for d in doses:
        for o in o2_levels:
            for label, R in dose_rates.items():
                res = survival_dynamic(
                    total_dose_Gy=d,
                    dose_rate_Gy_per_s=R,
                    o2_initial_percent=o,
                    n_iter=1500,
                    n_steps=80,
                    rng=np.random.default_rng(rng.integers(1, 2**32 - 1)),
                )
                rows.append({
                    "dose_Gy": d,
                    "o2_initial_pct": o,
                    "regime": label,
                    "dose_rate_Gy_per_s": R,
                    "SF_mean": res["SF_mean"],
                    "SF_std": res["SF_std"],
                    "mean_total_DSB": res["mean_total_DSB"],
                    "T_irr_s": res["T_irr_s"],
                    "o2_min_pct_during_irrad": res["o2_min_pct"],
                })

    with open(csv_path, "w") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    # Plot SF vs initial O2 for the two regimes at D=20 Gy
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 2, figsize=(10, 4.2), constrained_layout=True)
        for d_target, panel in zip(doses, ax):
            for label in dose_rates:
                sub = [r for r in rows if r["dose_Gy"] == d_target and r["regime"] == label]
                xs = [r["o2_initial_pct"] for r in sub]
                ys = [max(r["SF_mean"], 1e-6) for r in sub]
                panel.semilogy(xs, ys, "o-", label=label.replace("_", " "))
            panel.set_xlabel("Initial [O2] (%)")
            panel.set_ylabel("Surviving fraction")
            panel.set_title(f"D = {d_target} Gy")
            panel.set_ylim(1e-5, 1.5)
            panel.grid(True, which="both", alpha=0.3)
            panel.legend()
        fig.suptitle("Smoke: dynamic UNIVERSE - FLASH vs CONV vs initial [O2]")
        fig.savefig(fig_path, dpi=130)
        plt.close(fig)
    except Exception as e:
        with open(log_path, "a") as f:
            f.write(f"matplotlib failed: {e!r}\n")

    elapsed = time.time() - t0
    summary = {
        "elapsed_s": elapsed,
        "n_conditions": len(rows),
        "outputs": {"csv": csv_path, "figure": fig_path},
        "headline_flash_vs_conv_at_D20_O2_2pct": {
            label: next(
                r["SF_mean"] for r in rows
                if r["dose_Gy"] == 20.0 and r["o2_initial_pct"] == 2.0 and r["regime"] == label
            )
            for label in dose_rates
        },
        "parameters_used": {
            "ALPHA_DSB": ALPHA_DSB,
            "N_DOMAINS": N_DOMAINS,
            "HRF_M": HRF_M,
            "HRF_K_PERCENT": HRF_K_PERCENT,
            "K_IDSB": K_IDSB,
            "K_CDSB": K_CDSB,
            "T_IDSB_HALF_MIN": T_IDSB_HALF_MIN,
            "T_CDSB_HALF_MIN": T_CDSB_HALF_MIN,
            "G_ROD_MMHG_PER_GY": G_ROD_MMHG_PER_GY,
            "TAU_REOX_S": TAU_REOX_S,
        },
    }
    with open(log_path, "a") as f:
        f.write(json.dumps(summary, indent=2) + "\n")
    return summary


if __name__ == "__main__":
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    s = run_smoke(here)
    print(json.dumps(s, indent=2))
