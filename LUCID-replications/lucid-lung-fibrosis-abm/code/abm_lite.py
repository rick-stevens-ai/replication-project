"""
abm_lite.py — ABM-only reproduction of Cogno/Bauer/Durante 2024
"Mechanistic model of radiotherapy-induced lung fibrosis using coupled
3D agent-based and Monte Carlo simulations" (Commun. Med. 4:16).

Reduced-scope replication: skip the BioDynaMo + TOPAS-nBio coupled stack and
instead reproduce the *qualitative* dose-response of the alveolar segment
using the published equations and parameter values pulled from the Zenodo
artifact (10.5281/zenodo.10185637, sim-param.h).

Implements:
  * LQ--critical-volume model for FSU (alveolar) survival, Eq.(4)
  * Sigmoidal ΔECM(D), Eq.(2)
  * RSI(D), Eq.(3)
  * Population-level bystander/macrophage stochastic model per alveolus
    (simplified surrogate for the full 3D ABM, capturing the key
    indirect-damage dynamic)
  * 1-fraction vs 5-fraction comparison

Outputs:
  * results/abm_lite_results.csv  — per-dose, per-replicate measurements
  * figures/fig5_like.png         — FSU survival, ΔECM, RSI vs dose (single fraction)
  * figures/fig6_like.png         — 1fx vs 5fx fractionation comparison
  * figures/fig7_like.png         — sensitivity to bystander threshold & radiosensitivity
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass, asdict
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.special import erf
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------
# Parameters pulled from the released sim-param.h (Zenodo 10.5281/zenodo.10185637)
# ----------------------------------------------------------------------------

# LQ model for AEC2 (epithelial type-II) cell survival
ALPHA_LQ = 0.07427           # Gy^-1   (Cogno et al., sim-param.h line 127)
ALPHA_BETA = 7.0             # Gy      (sim-param.h line 129)
BETA_LQ = ALPHA_LQ / ALPHA_BETA  # Gy^-2 ~ 0.01061

# Alveolar segment geometry / population
ALVEOLI_PER_SEGMENT = 18
AEC2_PER_ALVEOLUS = 60       # paper text and previous-work consistent estimate
                             # (paper says ~"hundreds" per alveolus across all
                             # cell types; AEC2 specifically is the radiosensitive
                             # population on the middle layer — 60 is a tractable
                             # surrogate consistent with the published code's
                             # initial counts).

# Damage handling
DEFAULT_BYSTANDER_THRESHOLD = 2     # paper "assessed best value ... 2"
DEFAULT_PHAG_FRACTION = 0.4         # sim-param.h line 81
DEFAULT_PHAG_INDEX = 1              # sim-param.h line 82
DAMAGED_TO_SEN_RATE = 0.25          # day^-1, sim-param.h line 90
SURV_PROB_AFTER_DAMAGE = 0.6        # paper varies apoptotic/senescent ratio

# Simulation time
DAYS_LATE_ENDPOINT = 1200           # paper: total ABM duration
DAYS_PER_STEP = 1.0                 # 1-day macro steps (paper uses 20s micro
                                    # steps; we coarse-grain since we only need
                                    # the equilibrium late-time endpoint)

# ΔECM model (Eq. 2) parameters — fitted by paper; we use them as priors
# (and re-fit our ABM output against them).
DELTA_ECM_MAX_LATE = 3.5e-3   # g/cm^3, order-of-magnitude from paper Fig. 5
GAMMA_ECM_LATE = 0.10         # steepness (we will fit)
D50_ECM_LATE = 12.0           # Gy (we will fit)

# RSI (Eq. 3)
RSI_A = 1.0                   # saturation (normalised)
RSI_GAMMA = 0.12              # steepness (will fit)
RSI_ED50 = 13.0               # Gy (will fit)

# ECM baseline & saturation
ECM_FLAT = 3.26e-3            # g/cm^3, sim-param.h line 194
ECM_SAT_PER_VOL = 1.0e-2      # sim-param.h line 247

RNG = np.random.default_rng(42)


# ----------------------------------------------------------------------------
# Equations from the paper
# ----------------------------------------------------------------------------

def lq_cell_survival(dose: float | np.ndarray, alpha: float = ALPHA_LQ,
                     beta: float = BETA_LQ) -> float | np.ndarray:
    """AEC2 single-cell survival probability under the LQ model."""
    return np.exp(-alpha * dose - beta * np.asarray(dose) ** 2)


def fsu_survival_lq_cv(dose, n_aec2=AEC2_PER_ALVEOLUS, alpha=ALPHA_LQ,
                       beta=BETA_LQ):
    """Eq. (4): FSU survival = 1 - (1 - LQ)^N_AEC2."""
    p_kill_cell = 1.0 - lq_cell_survival(dose, alpha, beta)
    return 1.0 - p_kill_cell ** n_aec2


def delta_ecm_sigmoid(dose, dmax=DELTA_ECM_MAX_LATE,
                      gamma=GAMMA_ECM_LATE, d50=D50_ECM_LATE):
    """Eq. (2): sigmoidal ΔECM(D)."""
    return dmax / (1.0 + np.exp(-4.0 * gamma * (np.asarray(dose) - d50)))


def rsi_sigmoid(dose, A=RSI_A, gamma=RSI_GAMMA, ed50=RSI_ED50):
    """Eq. (3): RSI(D) = (A/2)·[1 - erf(√π · γ · (1 - D/ED50))]^(1/2)·g  (g=1)."""
    arg = math.sqrt(math.pi) * gamma * (1.0 - np.asarray(dose) / ed50)
    val = 0.5 * A * (1.0 - erf(arg))
    return np.sqrt(np.clip(val, 0.0, None))


# ----------------------------------------------------------------------------
# Lightweight alveolus ABM
# ----------------------------------------------------------------------------

@dataclass
class AbmParams:
    n_alveoli: int = ALVEOLI_PER_SEGMENT
    n_aec2_per_alv: int = AEC2_PER_ALVEOLUS
    alpha: float = ALPHA_LQ
    beta: float = BETA_LQ
    bystander_threshold: int = DEFAULT_BYSTANDER_THRESHOLD
    phag_fraction: float = DEFAULT_PHAG_FRACTION   # fraction of macrophages that clear senescent cells
    phag_index: int = DEFAULT_PHAG_INDEX           # senescent cells removed per active macrophage per day
    n_macrophages: int = 5                          # M1+M2 patrol per alveolus
    damaged_to_sen_rate: float = DAMAGED_TO_SEN_RATE   # day^-1
    apoptosis_prob_after_damage: float = 1.0 - SURV_PROB_AFTER_DAMAGE
    days: int = DAYS_LATE_ENDPOINT
    dose_distribution_cv: float = 0.20              # heterogeneity of dose across cells
                                                     # (paper highlights distribution matters)
    aec2_repop_rate: float = 0.10                   # day^-1 healing of dead -> healthy via proliferation
    bystander_step_prob: float = 0.10               # per-day probability a healthy cell adjacent
                                                     # to >=threshold senescent neighbors becomes damaged


class Alveolus:
    """Stochastic single-alveolus state. Tracks AEC2 cell counts by state.

    ECM accumulates over time (cumulative deposition driven by TGF-β-secreting
    senescent & damaged cells, plus mesenchymal expansion). Once deposited,
    ECM clears slowly via MMP/TIMP dynamics (paper's reaction-diffusion).
    """
    __slots__ = ("healthy", "damaged", "senescent", "apoptotic",
                 "dead", "n0", "params", "ecm_cum", "_secretion_history",
                 "myofibroblasts")

    def __init__(self, params: AbmParams):
        self.params = params
        self.n0 = params.n_aec2_per_alv
        self.healthy = params.n_aec2_per_alv
        self.damaged = 0
        self.senescent = 0
        self.apoptotic = 0
        self.dead = 0  # cumulative removed; "FSU" considered dead if healthy < threshold
        self.ecm_cum = ECM_FLAT   # current local ECM concentration (g/cm^3)
        self._secretion_history = 0.0   # bookkeeping
        self.myofibroblasts = 0.0  # mesenchymal compartment, grows under TGF-β signal

    def irradiate(self, mean_dose: float, rng: np.random.Generator):
        """Apply one fraction at mean dose. Per-cell dose drawn from a
        log-normal with the given CV to mimic MC dose distribution."""
        if self.healthy == 0:
            return
        if self.params.dose_distribution_cv > 0:
            sigma = np.sqrt(np.log(1.0 + self.params.dose_distribution_cv ** 2))
            mu = np.log(max(mean_dose, 1e-9)) - 0.5 * sigma ** 2
            doses = rng.lognormal(mu, sigma, size=self.healthy)
        else:
            doses = np.full(self.healthy, mean_dose)
        # LQ kill probability per cell
        p_kill = 1.0 - np.exp(-self.params.alpha * doses
                               - self.params.beta * doses ** 2)
        killed = rng.random(self.healthy) < p_kill
        n_hit = int(killed.sum())
        if n_hit == 0:
            return
        # fate of hit cells: apoptotic vs damaged (-> senescent over time)
        n_apop = int(rng.binomial(n_hit, self.params.apoptosis_prob_after_damage))
        n_dam = n_hit - n_apop
        self.healthy -= n_hit
        self.apoptotic += n_apop
        self.damaged += n_dam

    def step_day(self, rng: np.random.Generator, n_active_macs: int):
        """One day of ABM dynamics: damaged->senescent, bystander, clearance, repop, ECM deposition."""
        p = self.params
        # damaged -> senescent at rate damaged_to_sen_rate / day
        if self.damaged > 0:
            n_to_sen = int(rng.binomial(self.damaged,
                                         1.0 - math.exp(-p.damaged_to_sen_rate)))
            self.damaged -= n_to_sen
            self.senescent += n_to_sen
        # bystander damage: if senescent count >= threshold, healthy cells
        # have a per-day probability of becoming damaged
        if self.senescent >= p.bystander_threshold and self.healthy > 0:
            excess = self.senescent - p.bystander_threshold + 1
            p_by = 1.0 - math.exp(-p.bystander_step_prob * excess / p.n_aec2_per_alv)
            n_new_dam = int(rng.binomial(self.healthy, min(p_by, 0.5)))
            self.healthy -= n_new_dam
            self.damaged += n_new_dam
        # ECM deposition driven by current cytokine-secreting cells.
        # Net flux = k_dep * (sen + 0.3*dam) * (1 - ECM/ECM_sat) - k_deg * (ECM - ECM_flat)
        # k_dep tuned so that a fully senescent alveolus saturates over ~months.
        # --- Mesenchymal / myofibroblast dynamics --------------------------
        # Senescent AEC2 secrete TGF-β/PDGF -> mesenchymal cells differentiate
        # to myofibroblasts and proliferate. Myofibroblasts persistently
        # deposit ECM. This is the chronic-fibrosis switch.
        sen_frac = self.senescent / max(p.n_aec2_per_alv, 1)
        dam_frac = self.damaged / max(p.n_aec2_per_alv, 1)
        tgfb_signal = sen_frac + 0.3 * dam_frac
        # myofibroblast growth: TGF-β-driven recruitment + logistic cap
        mf_cap = 30.0   # max myofibroblasts per alveolus
        k_mf_grow = 0.05    # day^-1 at full TGF-β signal
        k_mf_decay = 0.02   # day^-1 baseline apoptosis (faster -> need
                            # sustained TGF-β to maintain population)
        # higher activation threshold (~15-20% of cells senescent at peak)
        hill_mf = tgfb_signal ** 4 / (0.15 ** 4 + tgfb_signal ** 4)
        d_mf = (k_mf_grow * hill_mf * (1.0 - self.myofibroblasts / mf_cap)
                - k_mf_decay * self.myofibroblasts)
        self.myofibroblasts = max(0.0, self.myofibroblasts + d_mf)

        # ECM deposition driven by myofibroblasts (sustained source) + acute
        # secretion from senescent AEC2.
        k_dep_mf = 8.0e-5    # g/cm^3 per myofibroblast per day
        k_dep_acute = 1.5e-5 # g/cm^3 per fractional-secretion-unit per day
        k_deg = 3.0e-4       # day^-1 slow MMP-mediated clearance
        gain = (k_dep_mf * self.myofibroblasts + k_dep_acute * tgfb_signal) \
               * max(0.0, 1.0 - self.ecm_cum / ECM_SAT_PER_VOL)
        loss = k_deg * max(0.0, self.ecm_cum - ECM_FLAT)
        self.ecm_cum += gain - loss
        secreting_eff = tgfb_signal
        self.ecm_cum = float(np.clip(self.ecm_cum, ECM_FLAT, ECM_SAT_PER_VOL))
        self._secretion_history += secreting_eff
        # macrophage clearance of senescent cells (paper: phag_fraction=0.4,
        # phag_index=1 -> very limited capacity; matches paper's slow clearance)
        clear_capacity = n_active_macs * p.phag_index
        n_cleared = min(self.senescent, clear_capacity)
        self.senescent -= n_cleared
        self.dead += n_cleared
        # clearance of apoptotic
        n_apop_cleared = min(self.apoptotic, max(1, clear_capacity // 2))
        self.apoptotic -= n_apop_cleared
        self.dead += n_apop_cleared
        # repopulation by AEC2 proliferation, gated by ECM stiffness:
        # the paper shows scarred alveoli do not recover normal AEC2 density.
        deficit = p.n_aec2_per_alv - (self.healthy + self.damaged
                                       + self.senescent + self.apoptotic)
        if deficit > 0 and self.healthy > 0:
            ecm_excess = max(0.0, self.ecm_cum - ECM_FLAT)
            fibrotic_block = math.exp(-ecm_excess / (0.3 * ECM_SAT_PER_VOL))
            p_repop = (1.0 - math.exp(-p.aec2_repop_rate)) * fibrotic_block
            n_new = int(rng.binomial(deficit, max(0.0, min(p_repop, 1.0))))
            self.healthy += n_new

    def fsu_alive(self, frac_threshold: float = 0.3) -> bool:
        """Alveolus is a surviving FSU if at least frac_threshold of its
        AEC2 population is healthy (and there's not overwhelming senescence)."""
        return (self.healthy / self.n0) >= frac_threshold

    def ecm_local(self) -> float:
        """Return current local ECM concentration (g/cm^3)."""
        return float(self.ecm_cum)


class AlveolarSegment:
    def __init__(self, params: AbmParams, rng: np.random.Generator):
        self.params = params
        self.rng = rng
        self.alveoli = [Alveolus(params) for _ in range(params.n_alveoli)]

    def deliver_fraction(self, dose: float):
        for alv in self.alveoli:
            alv.irradiate(dose, self.rng)

    def simulate_days(self, n_days: int):
        p = self.params
        n_active = max(1, int(p.n_macrophages * p.phag_fraction))
        for _ in range(n_days):
            for alv in self.alveoli:
                alv.step_day(self.rng, n_active)

    def fsu_survival(self) -> float:
        return np.mean([a.fsu_alive() for a in self.alveoli])

    def mean_ecm(self) -> float:
        return float(np.mean([a.ecm_local() for a in self.alveoli]))

    def delta_ecm(self) -> float:
        return self.mean_ecm() - ECM_FLAT


# ----------------------------------------------------------------------------
# Experiment drivers
# ----------------------------------------------------------------------------

def run_dose_response(doses, n_fractions=1, n_reps=10,
                       params_override: dict | None = None,
                       seed_base: int = 1000):
    rows = []
    for dose_total in doses:
        dose_per_fx = dose_total / n_fractions
        for rep in range(n_reps):
            seed = seed_base + int(dose_total * 100) + rep * 7
            rng = np.random.default_rng(seed)
            params = AbmParams()
            if params_override:
                for k, v in params_override.items():
                    setattr(params, k, v)
            seg = AlveolarSegment(params, rng)
            # short equilibration
            seg.simulate_days(5)
            for fx in range(n_fractions):
                seg.deliver_fraction(dose_per_fx)
                if fx < n_fractions - 1:
                    seg.simulate_days(1)   # 24 h between fractions
            # long late-time evolution
            seg.simulate_days(params.days - 5 - max(0, n_fractions - 1))
            rows.append({
                "dose_total_Gy": dose_total,
                "dose_per_fx_Gy": dose_per_fx,
                "n_fractions": n_fractions,
                "rep": rep,
                "fsu_survival": seg.fsu_survival(),
                "delta_ecm": seg.delta_ecm(),
            })
    df = pd.DataFrame(rows)
    df["rsi_empirical"] = np.sqrt(
        np.clip(df["delta_ecm"] / DELTA_ECM_MAX_LATE, 0, 1.5)
        * np.clip(1.0 - df["fsu_survival"], 0, 1)
    )
    return df


def fit_ecm(df_grouped: pd.DataFrame):
    def f(D, dmax, g, d50):
        return dmax / (1.0 + np.exp(-4.0 * g * (D - d50)))
    try:
        popt, _ = curve_fit(f, df_grouped["dose_total_Gy"], df_grouped["delta_ecm"],
                            p0=[DELTA_ECM_MAX_LATE, 0.1, 12.0], maxfev=5000)
    except Exception as e:
        print("ecm fit failed:", e)
        popt = [DELTA_ECM_MAX_LATE, 0.1, 12.0]
    return popt


def fit_rsi(df_grouped: pd.DataFrame):
    def f(D, A, g, ed50):
        arg = math.sqrt(math.pi) * g * (1.0 - D / ed50)
        return np.sqrt(np.clip(0.5 * A * (1.0 - erf(arg)), 0, None))
    try:
        popt, _ = curve_fit(f, df_grouped["dose_total_Gy"], df_grouped["rsi_empirical"],
                            p0=[1.0, 0.12, 13.0], maxfev=5000,
                            bounds=([0.1, 0.01, 1.0], [3.0, 5.0, 60.0]))
    except Exception as e:
        print("rsi fit failed:", e)
        popt = [1.0, 0.12, 13.0]
    return popt


# ----------------------------------------------------------------------------
# Plots
# ----------------------------------------------------------------------------

def plot_fig5_like(df1, outpath: Path):
    g = df1.groupby("dose_total_Gy").agg(
        fsu_mean=("fsu_survival", "mean"),
        fsu_sem=("fsu_survival", "sem"),
        ecm_mean=("delta_ecm", "mean"),
        ecm_sem=("delta_ecm", "sem"),
        rsi_mean=("rsi_empirical", "mean"),
        rsi_sem=("rsi_empirical", "sem"),
    ).reset_index()
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    D = g["dose_total_Gy"].values
    Dfine = np.linspace(0, max(D), 200)

    # FSU
    axes[0].errorbar(D, g["fsu_mean"], yerr=g["fsu_sem"], fmt="o", color="k",
                     label="ABM-lite")
    axes[0].plot(Dfine, fsu_survival_lq_cv(Dfine), "r-",
                 label=f"LQ-CV (Eq.4): α={ALPHA_LQ}, β={BETA_LQ:.4f}, N={AEC2_PER_ALVEOLUS}")
    axes[0].set_xlabel("Total dose (Gy)")
    axes[0].set_ylabel("FSU surviving fraction")
    axes[0].set_title("FSU survival vs dose (1 fraction)")
    axes[0].legend(fontsize=8)
    axes[0].grid(alpha=0.3)

    # ECM
    popt_ecm = fit_ecm(g.rename(columns={"ecm_mean": "delta_ecm"})
                        .assign(delta_ecm=g["ecm_mean"]))
    axes[1].errorbar(D, g["ecm_mean"], yerr=g["ecm_sem"], fmt="o", color="k",
                     label="ABM-lite")
    axes[1].plot(Dfine, delta_ecm_sigmoid(Dfine, *popt_ecm), "r-",
                 label=f"Eq.2 fit: ΔECM_max={popt_ecm[0]:.2e}, γ={popt_ecm[1]:.2f}, D50={popt_ecm[2]:.1f}")
    axes[1].set_xlabel("Total dose (Gy)")
    axes[1].set_ylabel("ΔECM (g/cm³)")
    axes[1].set_title("Late ΔECM vs dose (1 fraction)")
    axes[1].legend(fontsize=7)
    axes[1].grid(alpha=0.3)

    # RSI
    popt_rsi = fit_rsi(g.rename(columns={"rsi_mean": "rsi_empirical"})
                        .assign(rsi_empirical=g["rsi_mean"]))
    axes[2].errorbar(D, g["rsi_mean"], yerr=g["rsi_sem"], fmt="o", color="k",
                     label="ABM-lite")
    axes[2].plot(Dfine, rsi_sigmoid(Dfine, *popt_rsi), "r-",
                 label=f"Eq.3 fit: A={popt_rsi[0]:.2f}, γ={popt_rsi[1]:.2f}, ED50={popt_rsi[2]:.1f}")
    axes[2].set_xlabel("Total dose (Gy)")
    axes[2].set_ylabel("RSI (a.u.)")
    axes[2].set_title("RSI vs dose (1 fraction)")
    axes[2].legend(fontsize=7)
    axes[2].grid(alpha=0.3)

    plt.suptitle("Reproduction of paper Fig. 5 (single-fraction dose response)")
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()
    return {"ecm_fit": popt_ecm.tolist() if hasattr(popt_ecm, "tolist") else list(popt_ecm),
            "rsi_fit": popt_rsi.tolist() if hasattr(popt_rsi, "tolist") else list(popt_rsi)}


def plot_fig6_like(df1, df5, outpath: Path):
    g1 = df1.groupby("dose_total_Gy").mean(numeric_only=True).reset_index()
    g5 = df5.groupby("dose_total_Gy").mean(numeric_only=True).reset_index()
    s1 = df1.groupby("dose_total_Gy").sem(numeric_only=True).reset_index()
    s5 = df5.groupby("dose_total_Gy").sem(numeric_only=True).reset_index()

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    axes[0].errorbar(g1["dose_total_Gy"], g1["delta_ecm"], yerr=s1["delta_ecm"],
                     fmt="o-", color="black", label="1 fx")
    axes[0].errorbar(g5["dose_total_Gy"], g5["delta_ecm"], yerr=s5["delta_ecm"],
                     fmt="s-", color="red", label="5 fx")
    axes[0].set_xlabel("Total dose (Gy)")
    axes[0].set_ylabel("ΔECM (g/cm³)")
    axes[0].set_title("Late ΔECM: 1fx vs 5fx")
    axes[0].legend(); axes[0].grid(alpha=0.3)

    axes[1].errorbar(g1["dose_total_Gy"], g1["fsu_survival"], yerr=s1["fsu_survival"],
                     fmt="o-", color="black", label="1 fx")
    axes[1].errorbar(g5["dose_total_Gy"], g5["fsu_survival"], yerr=s5["fsu_survival"],
                     fmt="s-", color="red", label="5 fx")
    axes[1].set_xlabel("Total dose (Gy)")
    axes[1].set_ylabel("FSU surviving fraction")
    axes[1].set_title("FSU survival: 1fx vs 5fx")
    axes[1].legend(); axes[1].grid(alpha=0.3)

    axes[2].errorbar(g1["dose_total_Gy"], g1["rsi_empirical"], yerr=s1["rsi_empirical"],
                     fmt="o-", color="black", label="1 fx")
    axes[2].errorbar(g5["dose_total_Gy"], g5["rsi_empirical"], yerr=s5["rsi_empirical"],
                     fmt="s-", color="red", label="5 fx")
    axes[2].set_xlabel("Total dose (Gy)")
    axes[2].set_ylabel("RSI (a.u.)")
    axes[2].set_title("RSI: 1fx vs 5fx (right-shift expected)")
    axes[2].legend(); axes[2].grid(alpha=0.3)

    plt.suptitle("Reproduction of paper Fig. 6 (fractionation sparing)")
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()


def plot_fig7_like(df_base, df_lowby, df_lowrs, outpath: Path):
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    def summarise(df):
        g = df.groupby("dose_total_Gy").mean(numeric_only=True).reset_index()
        s = df.groupby("dose_total_Gy").sem(numeric_only=True).reset_index()
        return g, s

    for df, name, color, marker in [
        (df_base, "bystander=2 (std)", "black", "o"),
        (df_lowby, "bystander=1", "red", "s"),
        (df_lowrs, "α,β ×0.9", "blue", "^"),
    ]:
        g, s = summarise(df)
        axes[0].errorbar(g["dose_total_Gy"], g["delta_ecm"], yerr=s["delta_ecm"],
                         fmt=f"{marker}-", color=color, label=name)
        axes[1].errorbar(g["dose_total_Gy"], g["fsu_survival"], yerr=s["fsu_survival"],
                         fmt=f"{marker}-", color=color, label=name)
        axes[2].errorbar(g["dose_total_Gy"], g["rsi_empirical"], yerr=s["rsi_empirical"],
                         fmt=f"{marker}-", color=color, label=name)

    axes[0].set_xlabel("Dose (Gy)"); axes[0].set_ylabel("ΔECM (g/cm³)")
    axes[0].set_title("ΔECM"); axes[0].legend(fontsize=8); axes[0].grid(alpha=0.3)
    axes[1].set_xlabel("Dose (Gy)"); axes[1].set_ylabel("FSU survival")
    axes[1].set_title("FSU survival"); axes[1].legend(fontsize=8); axes[1].grid(alpha=0.3)
    axes[2].set_xlabel("Dose (Gy)"); axes[2].set_ylabel("RSI")
    axes[2].set_title("RSI"); axes[2].legend(fontsize=8); axes[2].grid(alpha=0.3)

    plt.suptitle("Reproduction of paper Fig. 7 (parameter sensitivity)")
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()


# ----------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", type=Path,
                    default=Path(__file__).resolve().parents[1])
    ap.add_argument("--reps", type=int, default=10)
    ap.add_argument("--quick", action="store_true",
                    help="Smaller dose grid / fewer reps for fast smoke test.")
    args = ap.parse_args()

    results_dir = args.outdir / "results"
    figures_dir = args.outdir / "figures"
    logs_dir = args.outdir / "logs"
    for d in (results_dir, figures_dir, logs_dir):
        d.mkdir(parents=True, exist_ok=True)

    doses_1fx = [0, 2, 5, 7.5, 10, 12, 15, 17.5, 20, 25, 30, 35, 42.5]
    # Table 1 fractionation totals from paper
    doses_5fx = [0, 2.5, 5.5, 7.5, 10, 20, 25, 30, 35, 42.5]
    if args.quick:
        doses_1fx = [0, 5, 10, 20, 30]
        doses_5fx = [0, 5.5, 10, 20, 30]

    n_reps = args.reps

    print(f"[1/4] Single-fraction dose-response (doses={doses_1fx}, reps={n_reps})")
    df1 = run_dose_response(doses_1fx, n_fractions=1, n_reps=n_reps)
    df1.to_csv(results_dir / "df_1fx.csv", index=False)

    print(f"[2/4] 5-fraction dose-response (totals={doses_5fx}, reps={n_reps})")
    df5 = run_dose_response(doses_5fx, n_fractions=5, n_reps=n_reps)
    df5.to_csv(results_dir / "df_5fx.csv", index=False)

    print("[3/4] Sensitivity: bystander=1, then α,β×0.9")
    df_lowby = run_dose_response(doses_1fx, n_fractions=1, n_reps=n_reps,
                                  params_override={"bystander_threshold": 1})
    df_lowby.to_csv(results_dir / "df_1fx_bystander1.csv", index=False)
    df_lowrs = run_dose_response(doses_1fx, n_fractions=1, n_reps=n_reps,
                                  params_override={"alpha": 0.9 * ALPHA_LQ,
                                                    "beta": 0.9 * BETA_LQ})
    df_lowrs.to_csv(results_dir / "df_1fx_lowRS.csv", index=False)

    print("[4/4] Plots & fits")
    fits = plot_fig5_like(df1, figures_dir / "fig5_like.png")
    plot_fig6_like(df1, df5, figures_dir / "fig6_like.png")
    plot_fig7_like(df1, df_lowby, df_lowrs, figures_dir / "fig7_like.png")

    # Combined results CSV
    df1["condition"] = "1fx_standard"
    df5["condition"] = "5fx_standard"
    df_lowby["condition"] = "1fx_bystander1"
    df_lowrs["condition"] = "1fx_lowRS"
    pd.concat([df1, df5, df_lowby, df_lowrs]).to_csv(
        results_dir / "abm_lite_results.csv", index=False)

    summary = {
        "params_pulled_from_zenodo": {
            "alpha_lq_Gy^-1": ALPHA_LQ,
            "beta_lq_Gy^-2": BETA_LQ,
            "alpha_beta_ratio_Gy": ALPHA_BETA,
            "AEC2_per_alveolus_used": AEC2_PER_ALVEOLUS,
            "alveoli_per_segment": ALVEOLI_PER_SEGMENT,
            "bystander_threshold_default": DEFAULT_BYSTANDER_THRESHOLD,
            "phag_fraction": DEFAULT_PHAG_FRACTION,
            "phag_index": DEFAULT_PHAG_INDEX,
            "damaged_to_sen_rate_per_day": DAMAGED_TO_SEN_RATE,
            "ecm_baseline_g_cm3": ECM_FLAT,
        },
        "fits": fits,
        "n_replicates": n_reps,
        "doses_1fx": doses_1fx,
        "doses_5fx_total": doses_5fx,
        "endpoints_days_late": DAYS_LATE_ENDPOINT,
    }
    with open(logs_dir / "run_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print("DONE. Summary:")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
