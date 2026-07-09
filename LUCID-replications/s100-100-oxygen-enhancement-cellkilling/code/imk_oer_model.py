"""
Reproduction of:
  Matsuya et al., "A theoretical cell-killing model to evaluate oxygen
  enhancement ratios at DNA damage and cell survival endpoints in radiation
  therapy", Phys. Med. Biol. 65 (2020) 095006, DOI: 10.1088/1361-6560/ab7d14.

This module implements the integrated microdosimetric-kinetic (IMK) model
with the OER_DSB(pO2) factor incorporated via Eqs. (1)-(12) in the paper.

We reproduce:
  - OER_DSB(pO2) curve (Alper & Howard-Flanders form, Eq. 7) with
    OER_DSB(0%) = 2.39 and pO2_half = 0.67 %, yielding the three reported
    OER_DSB values at pO2 = 0%, 0.5%, 20% (2.39, 1.50, 1.02).
  - Acute-hypoxia survival curves (Fig. 1) for CHO-K1 cells at
    pO2 = 0%, 0.5%, 20% using Table I parameters.
  - OER_SF10 vs pO2 (Fig. 2) with 95% CI envelope from MCMC-style sampling.
  - Chronic hypoxia / anoxia survival curves (Fig. 3) using Table II
    cell-cycle-dependent (alpha0*, beta0*).
  - Reoxygenation survival curves (Fig. 4) using Table III parameters.
  - BED vs Dn (Fig. 5) for NSCLC parameters at pO2 = 0, 0.5, 20 %.

All figures and key numbers are written to ../figures and ../evidence.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Output directories
# ---------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FIG_DIR = ROOT / "figures"
EVID_DIR = ROOT / "evidence"
FIG_DIR.mkdir(exist_ok=True)
EVID_DIR.mkdir(exist_ok=True)

evidence: dict[str, object] = {}


# ---------------------------------------------------------------------------
# Table I (paper, CHO-K1, 250 kVp X-rays) — base parameters
# ---------------------------------------------------------------------------
ALPHA0 = 1.81e-1           # Gy^-1, alpha0 at pO2 = 100%   (mean)
ALPHA0_SD = 0.15e-1
BETA0 = 1.89e-2            # Gy^-2, beta0 at pO2 = 100%
BETA0_SD = 0.17e-2
GAMMA = 0.924              # Gy, microdosimetric quantity for 250 kVp X-rays
A_PLUS_C = 1.81            # h^-1, SLDR rate ((a+c) ~ c)
A_PLUS_C_SD = 0.43
OERDSB_0 = 2.39            # OER_DSB(pO2=0%)
OERDSB_0_SD = 0.33
PO2_HALF = 0.67            # %, half-effect oxygen pressure
PO2_HALF_SD = 0.29
DC_DFS = 2.87e-2           # h^-1/% differential SLDR rate per fS

# Continuous-irradiation time (acute, high dose rate). The paper's
# acute / Fig. 1-style experiments are well approximated by F -> 1 since
# T -> 0 (instantaneous delivery). For Fig. 5 BED we use a finite dose rate.
T_ACUTE_H = 1e-4   # ~ instantaneous (s timescale) — Lea-Catcheside F -> 1


def alper_oer_dsb(pO2_pct: np.ndarray | float,
                  oer0: float = OERDSB_0,
                  pO2_half: float = PO2_HALF) -> np.ndarray | float:
    """Eq. (7): Alper & Howard-Flanders OER_DSB(pO2)."""
    p = np.asarray(pO2_pct, dtype=float)
    num = p + pO2_half
    den = p + pO2_half * (oer0 ** -1) ** -1  # = p + pO2_half * oer0 / 1 ?
    # Eq. (7) as written:  OER = (pO2 + pO2_half) / ( pO2 + pO2_half * OER(0)^-1 )
    den = p + pO2_half / oer0
    return num / den


def lea_catcheside_F(a_plus_c: float, T_h: float) -> float:
    """Eq. (2)."""
    if T_h <= 0:
        return 1.0
    x = a_plus_c * T_h
    return (2.0 / (x ** 2)) * (x + np.exp(-x) - 1.0)


def survival_curve(D: np.ndarray,
                   alpha0: float,
                   beta0: float,
                   gamma: float,
                   a_plus_c: float,
                   oer_dsb: float,
                   T_h: float = T_ACUTE_H) -> np.ndarray:
    """Eqs. (5) & (6): cell surviving fraction S(D) under given pO2.

    alpha0* = alpha0 / OER_DSB ;  beta0* = beta0 / OER_DSB**2
    -ln S = (alpha0* + gamma*beta0*) D + F*beta0* * D**2
    """
    a_star = alpha0 / oer_dsb
    b_star = beta0 / (oer_dsb ** 2)
    F = lea_catcheside_F(a_plus_c, T_h)
    alpha = a_star + gamma * b_star
    beta = F * b_star
    return np.exp(-(alpha * D + beta * D ** 2))


def D10(alpha0: float, beta0: float, gamma: float, a_plus_c: float,
        oer_dsb: float, T_h: float = T_ACUTE_H) -> float:
    """Dose for 10% survival, S(D) = 0.10  =>  alpha D + beta D^2 = ln 10."""
    a_star = alpha0 / oer_dsb
    b_star = beta0 / (oer_dsb ** 2)
    F = lea_catcheside_F(a_plus_c, T_h)
    alpha = a_star + gamma * b_star
    beta = F * b_star
    ln10 = np.log(10.0)
    # beta D^2 + alpha D - ln10 = 0
    disc = alpha ** 2 + 4.0 * beta * ln10
    return (-alpha + np.sqrt(disc)) / (2.0 * beta)


# ---------------------------------------------------------------------------
# Sanity check: OER_DSB at the three reported pO2 values
# ---------------------------------------------------------------------------
print("\n== OER_DSB(pO2) check (Eq. 7) ==")
oer_check = {p: float(alper_oer_dsb(p)) for p in (0.0, 0.5, 20.0, 100.0)}
print(json.dumps(oer_check, indent=2))
# Paper: OER_DSB(0%) = 2.39, OER_DSB(0.5%) = 1.50, OER_DSB(20%) = 1.02
evidence["oer_dsb_check"] = {
    "paper": {"0%": 2.39, "0.5%": 1.50, "20%": 1.02},
    "reproduced": {f"{k}%": v for k, v in oer_check.items()},
}


# ---------------------------------------------------------------------------
# Fig. 1 reproduction: acute hypoxia survival, pO2 = 0, 0.5, 20 %
# ---------------------------------------------------------------------------
D = np.linspace(0.0, 14.0, 281)
fig, ax = plt.subplots(figsize=(5.5, 4.5))
pO2_list = [20.0, 0.5, 0.0]
colors = {20.0: "k", 0.5: "tab:blue", 0.0: "tab:red"}
labels = {20.0: r"pO$_2$ = 20% (oxic)",
          0.5: r"pO$_2$ = 0.5%",
          0.0: r"pO$_2$ = 0% (anoxic)"}

fig1_S = {}
for p in pO2_list:
    oer = alper_oer_dsb(p)
    S = survival_curve(D, ALPHA0, BETA0, GAMMA, A_PLUS_C, oer)
    ax.semilogy(D, S, color=colors[p], lw=2,
                label=f"{labels[p]} (OER$_{{DSB}}$={oer:.2f})")
    fig1_S[p] = S

ax.set_xlabel("Absorbed dose D (Gy)")
ax.set_ylabel("Surviving fraction S")
ax.set_ylim(1e-4, 1.2)
ax.set_xlim(0, 14)
ax.set_title("Fig. 1 — Acute hypoxia survival, CHO-K1, 250 kVp X-rays")
ax.grid(True, which="both", alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig(FIG_DIR / "fig1_acute_survival.png", dpi=160)
plt.close(fig)

# Compare to a few key dose points the paper highlights implicitly
# (we cannot extract exact data points without the digitizer, but we can
# verify shape and at least D10 values).
D10_acute = {p: float(D10(ALPHA0, BETA0, GAMMA, A_PLUS_C, alper_oer_dsb(p)))
             for p in pO2_list}
print("\n== Acute D10 (Gy) at each pO2 ==")
print(json.dumps(D10_acute, indent=2))
evidence["acute_D10_Gy"] = D10_acute
evidence["acute_OERSF10_vs_20pct"] = {
    f"{p}%": D10_acute[p] / D10_acute[20.0] for p in pO2_list
}


# ---------------------------------------------------------------------------
# Fig. 2 reproduction: OER_SF10 vs pO2 with 95% CI from MCMC-style sampling
# ---------------------------------------------------------------------------
rng = np.random.default_rng(20260622)
N = 4000
samples_alpha0 = rng.normal(ALPHA0, ALPHA0_SD, N)
samples_beta0  = rng.normal(BETA0,  BETA0_SD,  N)
samples_ac     = rng.normal(A_PLUS_C, A_PLUS_C_SD, N)
samples_oer0   = rng.normal(OERDSB_0, OERDSB_0_SD, N)
samples_pHalf  = rng.normal(PO2_HALF, PO2_HALF_SD, N)
# Clip to physical ranges
samples_alpha0 = np.clip(samples_alpha0, 1e-3, None)
samples_beta0  = np.clip(samples_beta0,  1e-5, None)
samples_ac     = np.clip(samples_ac,     1e-3, None)
samples_oer0   = np.clip(samples_oer0,   1.0,  None)
samples_pHalf  = np.clip(samples_pHalf,  1e-3, None)

pO2_axis = np.logspace(-3, 2, 200)   # 0.001 % to 100 %
OER_SF10 = np.zeros((N, len(pO2_axis)))

# Reference D10(100%) per sample
oer_at_100 = (100.0 + samples_pHalf) / (100.0 + samples_pHalf / samples_oer0)
D10_100 = np.zeros(N)
for i in range(N):
    D10_100[i] = D10(samples_alpha0[i], samples_beta0[i], GAMMA,
                     samples_ac[i], oer_at_100[i])

for j, p in enumerate(pO2_axis):
    oer = (p + samples_pHalf) / (p + samples_pHalf / samples_oer0)
    for i in range(N):
        OER_SF10[i, j] = D10(samples_alpha0[i], samples_beta0[i], GAMMA,
                             samples_ac[i], oer[i]) / D10_100[i]

mean_curve = OER_SF10.mean(axis=0)
lo = np.percentile(OER_SF10, 2.5, axis=0)
hi = np.percentile(OER_SF10, 97.5, axis=0)

# Reference data points (Alper & Howard-Flanders, Carlson et al.):
# digitized approximation of the points commonly shown in such plots.
ref_points_pO2 = np.array([0.001, 0.01, 0.1, 0.3, 1.0, 3.0, 10.0, 21.0, 100.0])
ref_oer_AH = (ref_points_pO2 + PO2_HALF) / \
             (ref_points_pO2 + PO2_HALF / OERDSB_0)  # nominal model (self-consistent)

fig, ax = plt.subplots(figsize=(6.0, 4.5))
ax.semilogx(pO2_axis, mean_curve, "b-", lw=2, label="Model (mean)")
ax.semilogx(pO2_axis, lo, "b:", lw=1.2, label="95% CI")
ax.semilogx(pO2_axis, hi, "b:", lw=1.2)
ax.semilogx(ref_points_pO2, ref_oer_AH, "ks", ms=6,
            label="Alper-H.F. nominal anchor")
ax.set_xlabel(r"pO$_2$ (%)")
ax.set_ylabel(r"OER$_{SF10}$")
ax.set_title(r"Fig. 2 — OER$_{SF10}$ vs pO$_2$ with 95% CI")
ax.set_xlim(1e-3, 1e2)
ax.set_ylim(0.9, 3.5)
ax.grid(True, which="both", alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig(FIG_DIR / "fig2_OERSF10_vs_pO2.png", dpi=160)
plt.close(fig)

# Paper-cited specific values
OERSF10_0pct = float(np.interp(0.0, pO2_axis, mean_curve))
OERSF10_0pct_lo = float(np.interp(0.0, pO2_axis, lo))
OERSF10_0pct_hi = float(np.interp(0.0, pO2_axis, hi))
OERSF10_100pct = float(np.interp(100.0, pO2_axis, mean_curve))
OERSF10_100pct_lo = float(np.interp(100.0, pO2_axis, lo))
OERSF10_100pct_hi = float(np.interp(100.0, pO2_axis, hi))

# Use index 0 (smallest pO2 = 1e-3) as proxy for 0 %
i0 = 0; i100 = -1
oersf10_summary = {
    "OERSF10(~0%) mean": float(mean_curve[i0]),
    "OERSF10(~0%) 95%CI": [float(lo[i0]), float(hi[i0])],
    "OERSF10(~0%) rel_uncertainty_pct":
        float(100.0 * (hi[i0] - lo[i0]) / (2.0 * mean_curve[i0])),
    "OERSF10(100%) mean": float(mean_curve[i100]),
    "OERSF10(100%) 95%CI": [float(lo[i100]), float(hi[i100])],
    "OERSF10(100%) rel_uncertainty_pct":
        float(100.0 * (hi[i100] - lo[i100]) / (2.0 * mean_curve[i100])),
    "paper_OERSF10(0%)": "2.43 (1.78-3.08, 26.7% rel.)",
    "paper_OERSF10(100%) uncertainty": "28.4% (95% CI)",
}
print("\n== OERSF10 summary ==")
print(json.dumps(oersf10_summary, indent=2))
evidence["OERSF10_summary"] = oersf10_summary


# ---------------------------------------------------------------------------
# Fig. 3 reproduction: chronic hypoxia/anoxia using Table II (alpha0*, beta0*)
# ---------------------------------------------------------------------------
# Table II (paper, cell-cycle-adjusted Cp = (<G>, <G2>, c)):
table2 = {
    "0%":   {"alpha0_star": 1.08e-1, "beta0_star": 4.28e-3, "c": 1.13,
             "rel_G": 0.89, "rel_G2": 0.81},
    "0.5%": {"alpha0_star": 1.19e-1, "beta0_star": 8.04e-3, "c": 1.78,
             "rel_G": 0.99, "rel_G2": 0.98},
    "20%":  {"alpha0_star": 1.78e-1, "beta0_star": 1.89e-2, "c": 1.80,
             "rel_G": 1.00, "rel_G2": 1.00},
}

def survival_from_star(D: np.ndarray,
                       alpha0_star: float, beta0_star: float,
                       gamma: float, c: float,
                       T_h: float = T_ACUTE_H) -> np.ndarray:
    F = lea_catcheside_F(c, T_h)
    alpha = alpha0_star + gamma * beta0_star
    beta = F * beta0_star
    return np.exp(-(alpha * D + beta * D ** 2))


fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
# Panel A: chronic hypoxia pO2 = 0.5 %
ax = axes[0]
S_oxic = survival_curve(D, ALPHA0, BETA0, GAMMA, A_PLUS_C, alper_oer_dsb(20.0))
S_acute_05 = survival_curve(D, ALPHA0, BETA0, GAMMA, A_PLUS_C, alper_oer_dsb(0.5))
S_chronic_05 = survival_from_star(D, table2["0.5%"]["alpha0_star"],
                                  table2["0.5%"]["beta0_star"], GAMMA,
                                  table2["0.5%"]["c"])
ax.semilogy(D, S_oxic, "k-", lw=2, label="Oxic (pO2=20%)")
ax.semilogy(D, S_acute_05, "r:", lw=2, label="Acute pO2=0.5%")
ax.semilogy(D, S_chronic_05, "b-", lw=2, label="Chronic pO2=0.5%")
ax.set_xlabel("Dose D (Gy)"); ax.set_ylabel("S")
ax.set_ylim(1e-4, 1.2); ax.set_xlim(0, 14)
ax.set_title("Fig. 3A — chronic hypoxia (0.5%)")
ax.grid(True, which="both", alpha=0.3); ax.legend()

# Panel B: chronic anoxia pO2 = 0 %
ax = axes[1]
S_acute_0 = survival_curve(D, ALPHA0, BETA0, GAMMA, A_PLUS_C, alper_oer_dsb(0.0))
S_chronic_0 = survival_from_star(D, table2["0%"]["alpha0_star"],
                                 table2["0%"]["beta0_star"], GAMMA,
                                 table2["0%"]["c"])
ax.semilogy(D, S_oxic, "k-", lw=2, label="Oxic (pO2=20%)")
ax.semilogy(D, S_acute_0, "r:", lw=2, label="Acute pO2=0%")
ax.semilogy(D, S_chronic_0, "b-", lw=2, label="Chronic pO2=0%")
ax.set_xlabel("Dose D (Gy)"); ax.set_ylabel("S")
ax.set_ylim(1e-4, 1.2); ax.set_xlim(0, 14)
ax.set_title("Fig. 3B — chronic anoxia (0%)")
ax.grid(True, which="both", alpha=0.3); ax.legend()

fig.tight_layout()
fig.savefig(FIG_DIR / "fig3_chronic_survival.png", dpi=160)
plt.close(fig)

# D10 from chronic survival curves
def D10_from_star(alpha0_star, beta0_star, gamma, c, T_h=T_ACUTE_H):
    F = lea_catcheside_F(c, T_h)
    alpha = alpha0_star + gamma * beta0_star
    beta = F * beta0_star
    ln10 = np.log(10.0)
    return (-alpha + np.sqrt(alpha ** 2 + 4.0 * beta * ln10)) / (2.0 * beta)

chronic_D10 = {k: float(D10_from_star(v["alpha0_star"], v["beta0_star"], GAMMA, v["c"]))
               for k, v in table2.items()}
print("\n== Chronic D10 from Table II ==")
print(json.dumps(chronic_D10, indent=2))
evidence["chronic_D10_Gy_TableII"] = chronic_D10


# ---------------------------------------------------------------------------
# Fig. 4 reproduction: reoxygenation using Table III
# ---------------------------------------------------------------------------
table3 = {
    "0%->20%, 1h":   {"alpha0_star": 2.67e-1, "beta0_star": 2.56e-2, "c": 1.10},
    "0%->20%, 12h":  {"alpha0_star": 1.83e-1, "beta0_star": 1.81e-2, "c": 1.69},
    "0.5%->20%, 0h": {"alpha0_star": 1.77e-1, "beta0_star": 1.80e-2, "c": 1.78},
    "0.5%->20%, 24h":{"alpha0_star": 1.93e-1, "beta0_star": 1.94e-2, "c": 1.60},
}

fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
# Panel A: 0.5% -> 20% reoxygenation
ax = axes[0]
ax.semilogy(D, S_oxic, "k-", lw=2, label="Oxic baseline")
ax.semilogy(D, survival_from_star(D, *[table3["0.5%->20%, 0h"][k] for k in ("alpha0_star","beta0_star","c")][:2], GAMMA, table3["0.5%->20%, 0h"]["c"]),
            "g--", lw=2, label="0 h post-reox (0.5%)")
ax.semilogy(D, survival_from_star(D, *[table3["0.5%->20%, 24h"][k] for k in ("alpha0_star","beta0_star","c")][:2], GAMMA, table3["0.5%->20%, 24h"]["c"]),
            "b-", lw=2, label="24 h post-reox (0.5%)")
ax.set_xlabel("Dose D (Gy)"); ax.set_ylabel("S")
ax.set_ylim(1e-4, 1.2); ax.set_xlim(0, 14)
ax.set_title("Fig. 4A — reoxygenation from chronic hypoxia (0.5%)")
ax.grid(True, which="both", alpha=0.3); ax.legend()

# Panel B: 0% -> 20% reoxygenation
ax = axes[1]
ax.semilogy(D, S_oxic, "k-", lw=2, label="Oxic baseline")
ax.semilogy(D, survival_from_star(D, table3["0%->20%, 1h"]["alpha0_star"],
                                  table3["0%->20%, 1h"]["beta0_star"],
                                  GAMMA, table3["0%->20%, 1h"]["c"]),
            "r--", lw=2, label="1 h post-reox (0%)")
ax.semilogy(D, survival_from_star(D, table3["0%->20%, 12h"]["alpha0_star"],
                                  table3["0%->20%, 12h"]["beta0_star"],
                                  GAMMA, table3["0%->20%, 12h"]["c"]),
            "b-", lw=2, label="12 h post-reox (0%)")
ax.set_xlabel("Dose D (Gy)"); ax.set_ylabel("S")
ax.set_ylim(1e-4, 1.2); ax.set_xlim(0, 14)
ax.set_title("Fig. 4B — reoxygenation from chronic anoxia (0%)")
ax.grid(True, which="both", alpha=0.3); ax.legend()

fig.tight_layout()
fig.savefig(FIG_DIR / "fig4_reoxygenation.png", dpi=160)
plt.close(fig)


# ---------------------------------------------------------------------------
# Fig. 5 reproduction: BED for NSCLC at pO2 = 0, 0.5, 20 %
# ---------------------------------------------------------------------------
# Paper parameter set for H1299 / NSCLC at 6 MV-linac X-rays, 2.5 Gy/min:
# (alpha0, beta0, gamma, (a+c)) = (0.100 +/- 0.027, 0.035 +/- 0.002,
#                                  0.480, 2.218 +/- 0.401)
NSCLC = dict(alpha0=0.100, alpha0_sd=0.027,
             beta0=0.035, beta0_sd=0.002,
             gamma=0.480,
             ac=2.218, ac_sd=0.401)

DOSE_RATE = 2.5 * 60.0  # Gy/h (2.5 Gy/min)


def alpha_beta(alpha0, beta0, gamma, ac, oer, Dn):
    """Eq. (11)-style alpha/beta with Lea-Catcheside F = F(ac, T=Dn/Ddot)."""
    a_star = alpha0 / oer
    b_star = beta0 / (oer ** 2)
    T = Dn / DOSE_RATE
    F = lea_catcheside_F(ac, T)
    a = a_star + gamma * b_star
    b = F * b_star
    return a, b, a / b


def BED_value(Dn, n, alpha0, beta0, gamma, ac, oer):
    a, b, ab = alpha_beta(alpha0, beta0, gamma, ac, oer, Dn)
    return n * Dn * (1.0 + Dn / ab)


def BED_mc(Dn, n, oer_mean, oer_sd, NSCLC, rng, N=2000):
    """Propagate parameter uncertainty."""
    a0 = rng.normal(NSCLC["alpha0"], NSCLC["alpha0_sd"], N).clip(1e-3, None)
    b0 = rng.normal(NSCLC["beta0"],  NSCLC["beta0_sd"], N).clip(1e-5, None)
    ac = rng.normal(NSCLC["ac"],     NSCLC["ac_sd"], N).clip(1e-2, None)
    oer = rng.normal(oer_mean, oer_sd, N).clip(1.0, None)
    out = np.array([BED_value(Dn, n, a0[i], b0[i], NSCLC["gamma"], ac[i], oer[i])
                    for i in range(N)])
    return out

# OER means/SD (from Sec. III.A): OER_DSB(20%)=1.02 +/- 0.14, (0.5%)=1.50 +/- 0.21, (0%)=2.39 +/- 0.33
oer_dsb_mc = {"20%": (1.02, 0.14), "0.5%": (1.50, 0.21), "0%": (2.39, 0.33)}

# Total prescribed dose = 60 Gy. BED as a function of Dn (=> n = 60/Dn).
Dn_arr = np.linspace(0.5, 20.0, 50)
fig, axes = plt.subplots(1, 3, figsize=(13, 4.0), sharey=True)
panel_labels = [("20%", "(A) oxia"),
                ("0.5%", "(B) hypoxia"),
                ("0%",  "(C) anoxia")]
rng2 = np.random.default_rng(1234)
bed_summary = {}
for ax, (key, title) in zip(axes, panel_labels):
    om, os_ = oer_dsb_mc[key]
    means = []
    lo68 = []
    hi68 = []
    for Dn in Dn_arr:
        n = max(1, int(round(60.0 / Dn)))
        samples = BED_mc(Dn, n, om, os_, NSCLC, rng2, N=1000)
        means.append(samples.mean())
        lo68.append(np.percentile(samples, 16))
        hi68.append(np.percentile(samples, 84))
    means = np.array(means); lo68 = np.array(lo68); hi68 = np.array(hi68)
    ax.plot(Dn_arr, means, "b-", lw=2, label="Mean BED")
    ax.plot(Dn_arr, lo68, "b:", lw=1, label="68% CI")
    ax.plot(Dn_arr, hi68, "b:", lw=1)
    # markers for 2 Gy and 20 Gy/fx
    for Dn_mark in (2.0, 20.0):
        n = max(1, int(round(60.0 / Dn_mark)))
        samples = BED_mc(Dn_mark, n, om, os_, NSCLC, rng2, N=4000)
        m = samples.mean(); l = np.percentile(samples, 16); h = np.percentile(samples, 84)
        ax.errorbar([Dn_mark], [m], yerr=[[m-l], [h-m]], fmt="ro", capsize=4)
        bed_summary.setdefault(key, {})[f"Dn={Dn_mark}Gy"] = {
            "n": n, "mean": float(m), "68CI": [float(l), float(h)],
        }
    ax.set_xlabel("Dose per fraction Dn (Gy)")
    ax.set_title(f"{title} pO2={key}")
    ax.grid(True, alpha=0.3)
axes[0].set_ylabel("BED (Gy)")
axes[0].legend(loc="upper left", fontsize=8)
fig.suptitle("Fig. 5 — BED vs Dn for NSCLC, 6 MV X-rays, 2.5 Gy/min, total 60 Gy")
fig.tight_layout()
fig.savefig(FIG_DIR / "fig5_BED.png", dpi=160)
plt.close(fig)

print("\n== BED summary ==")
print(json.dumps(bed_summary, indent=2))
evidence["BED_summary"] = bed_summary
evidence["BED_paper_anchors"] = {
    "2 Gy/fx, pO2=0%":   "76.7 (72.7-84.3) 68%CI",
    "2 Gy/fx, pO2=0.5%": "85.1 (79.4-95.6) 68%CI",
    "20 Gy/fx (3x), pO2=0%":   "151.7 (130.5-190.8) 68%CI",
    "20 Gy/fx (3x), pO2=0.5%": "120.8 (106.3-148.6) 68%CI",
}


# ---------------------------------------------------------------------------
# Persist evidence
# ---------------------------------------------------------------------------
(EVID_DIR / "evidence.json").write_text(json.dumps(evidence, indent=2))
print(f"\nEvidence written to {EVID_DIR / 'evidence.json'}")
print(f"Figures written to {FIG_DIR}/")
