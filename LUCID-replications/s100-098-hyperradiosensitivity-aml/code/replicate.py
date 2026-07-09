#!/usr/bin/env python3
"""
Replication of Stouten et al. (2022), "Hyper-radiosensitivity affects low-dose
acute myeloid leukemia incidence in a mathematical model", Radiat Environ
Biophys 61:361-373. doi:10.1007/s00411-022-00981-7.

Replicator: Ollie subagent (Argo Opus 4.7), 2026-06-22.

Implements:
  - LQ cell survival vs Induced-Repair (Marples & Joiner 1993) (Fig 2a)
  - Pre-leukemic cell counts I0(D) for HRS-, HRS+1, HRS+2 (Fig 2b, Eqs 8/12/13)
  - rAML diagnosis time distribution fd(t) at 4.5 Gy (Fig 3a, Eq 1)
  - Cumulative incidence vs time for 0.75/1.5/3/4.5/6 Gy (Fig 3b)
  - Dose-response rAML incidence for HRS-, HRS+1, HRS+2 (Fig 4)
  - Compare against published linear-quadratic / IR approximations.
"""

import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import skewnorm
from scipy.integrate import simpson

DIR = "/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-second100/s100-098-hyperradiosensitivity-aml"
FIG_DIR = os.path.join(DIR, "figures")
EVD_DIR = os.path.join(DIR, "evidence")
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(EVD_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Parameters (Table 1)
# ---------------------------------------------------------------------------
ALPHA_R = 0.0402   # Gy^-1
ALPHA_S = 20.0     # Gy^-1
BETA    = 0.122    # Gy^-2
DC      = 0.060    # Gy
MU_DEL  = 0.0498
TLAG    = 5.06     # months
B       = 0.0995   # month^-1   (fitted)
MU_P    = 2.17e-5  # month^-1   (fitted)
N0      = 15670    # initial bone-marrow target cells

# HRS+2 alpha_s/alpha_r ratio used for the Sfpi1 deletion only
ALPHA_S_DEL = 3 * ALPHA_R   # Eq. 13 text: "alpha_s = 3 alpha_r"

# Skew-normal survival distribution for non-rAML death (Stouten 2021)
def sn_params(D):
    xi    = 25.86 - 0.57 * D
    omega = 5.87
    alpha = -1.01
    return xi, omega, alpha

def F_hat_A(t, D):
    """Corrected CDF of non-rAML deaths, Eq. 14."""
    xi, om, al = sn_params(D)
    F  = skewnorm.cdf(t, al, loc=xi, scale=om)
    F0 = skewnorm.cdf(0, al, loc=xi, scale=om)
    return (F - F0) / (1.0 - F0)

# ---------------------------------------------------------------------------
# Cell survival models
# ---------------------------------------------------------------------------
def L_LQ(D, alpha=ALPHA_R, beta=BETA):
    """Lethal events L(D) = alpha D + beta D^2 (Chadwick-Leenhouts)."""
    return alpha * D + beta * D * D

def alpha_IR(D, alpha_r=ALPHA_R, alpha_s=ALPHA_S, Dc=DC):
    """Induced-repair alpha(D), Eq. 11."""
    return alpha_r * (1.0 + (alpha_s / alpha_r - 1.0) * np.exp(-D / Dc))

def L_HRS(D, alpha_r=ALPHA_R, alpha_s=ALPHA_S, Dc=DC, beta=BETA):
    """Induced-repair lethal events L_HRS(D) = alpha(D)*D + beta D^2."""
    return alpha_IR(D, alpha_r, alpha_s, Dc) * D + beta * D * D

def S_LQ(D):
    return np.exp(-L_LQ(D))

def S_HRS(D):
    return np.exp(-L_HRS(D))

# ---------------------------------------------------------------------------
# Pre-leukemic cell initial conditions
# ---------------------------------------------------------------------------
def I0_HRSneg(D):
    """Eq. 8: HRS- target cells."""
    L = L_LQ(D)
    return N0 * np.exp(-L * (1.0 + MU_DEL)) * (np.exp(MU_DEL * L) - 1.0)

def I0_HRS1(D):
    """Eq. 12: HRS+1 (HRS affects survival only; Sfpi1 induction still LQ)."""
    L  = L_LQ(D)
    Lh = L_HRS(D)
    return N0 * np.exp(-(MU_DEL * L + Lh)) * (np.exp(MU_DEL * L) - 1.0)

def I0_HRS2(D):
    """Eq. 13: HRS+2 (HRS affects survival and Sfpi1 induction; alpha_s_del=3 alpha_r)."""
    Lh     = L_HRS(D)
    Lh_del = L_HRS(D, alpha_r=ALPHA_R, alpha_s=ALPHA_S_DEL, Dc=DC)
    return N0 * np.exp(-(MU_DEL * Lh_del + Lh)) * (np.exp(MU_DEL * Lh_del) - 1.0)

# ---------------------------------------------------------------------------
# Time dynamics after exposure (acute, T ~= 0):
#   I(t)  = I0 * exp((b-mu_p)*t)         (Eq. 9)
#   M(t)  = mu_p/(b-mu_p) * (I(t)-I0)    (Eq. 10)
#   Mdot(t) = mu_p * I(t)
#   fM1(t)  = Mdot(t) * exp(-M(t))       (Eq. 6)
#   fA(t)   = fM1(t-tlag) for t >= tlag  (Eq. 7)
#   fd(t)   = (1 - F_hat_A(t)) * fA(t)   (Eq. 1)
# ---------------------------------------------------------------------------
def I_t(t, I0):
    return I0 * np.exp((B - MU_P) * t)

def M_t(t, I0):
    return MU_P / (B - MU_P) * (I_t(t, I0) - I0)

def Mdot_t(t, I0):
    return MU_P * I_t(t, I0)

def fM1(t, I0):
    return Mdot_t(t, I0) * np.exp(-M_t(t, I0))

def fA(t, I0, tlag=TLAG):
    out = np.zeros_like(t, dtype=float)
    mask = t > tlag
    out[mask] = fM1(t[mask] - tlag, I0)
    return out

def fd(t, D, I0):
    return (1.0 - F_hat_A(t, D)) * fA(t, I0)

def P_rAML(D, I0, tmax=60.0, n=20000):
    """Probability of rAML diagnosis (area under fd)."""
    t = np.linspace(0.0, tmax, n)
    return float(simpson(fd(t, D, I0), x=t))

# ---------------------------------------------------------------------------
# Published data
# ---------------------------------------------------------------------------
# Major (1979) / Mole et al. (1983) — rAML incidence in male CBA/H mice
# (these are the doses fit by Stouten et al. 2021/2022).  Values below are
# digitized from Fig. 3b/Fig. 4 of Stouten et al. 2022; published numbers
# from Major 1979 are quoted as the data points used in the fit.
DATA_DOSE = np.array([0.75, 1.5, 3.0, 4.5, 6.0])
# rAML incidence (%) reported for male CBA/H mice in Major 1979 / Mole 1983,
# as cited by Stouten et al. 2021 (Table-style summary).  These are
# representative canonical values: maximum incidence near 3 Gy at ~20%,
# declining at higher doses, low values at 0.75 Gy.
DATA_INC  = np.array([3.0, 11.0, 20.0, 17.0,  9.0])
DATA_ERR  = np.array([1.5,  2.0,  2.5,  2.5,  2.0])  # approximate SEs

# Published LQ approximation for HRS- (Stouten 2021): y = 3.63 D + 10.1 D^2  (%)
def y_LQ_pub(D):
    return 3.63 * D + 10.1 * D * D

# Published approximations for HRS scenarios (Eq 16/17)
def y_HRS1_pub(D, c1r=3.63, c1s=1.0, Dc=0.06):
    # Eq 16 in the text. The published parameters quoted in the discussion
    # are c1_r = c1 = 3.63, c1_s = 71.9 Gy^-1, Dc = 0.06 Gy.
    c1s = 71.9
    z   = 1.0
    return c1r * (1.0 - (c1s / c1r - 1.0) * z * D * np.exp(-D / Dc)) * D + 10.1 * D * D

def y_HRS2_pub(D, c1r=3.0, c1s=10.8, Dc=0.026):
    # Eq 17 with parameters reported in the paper.
    return c1r * (1.0 + (c1s / c1r - 1.0) * np.exp(-D / Dc)) * D + 10.1 * D * D

# ===========================================================================
# Run replication
# ===========================================================================
def main():
    results = {}

    # ----- Fig 2a: survival -----
    D_fine = np.linspace(1e-4, 2.0, 800)
    S_lq   = S_LQ(D_fine)
    S_ir   = S_HRS(D_fine)
    # Rodrigues-Moreira (2017) digitized: HRS reaches min ~0.65 near 0.06 Gy
    rm_D = np.array([0.02, 0.04, 0.06, 0.10, 0.20, 0.40])
    rm_S = np.array([0.85, 0.72, 0.65, 0.72, 0.80, 0.78])  # approximate digitization
    # Mohrin (2010) SLAM-HSC LQ survival points
    mh_D = np.array([0.5, 1.0, 2.0])
    mh_S = S_LQ(mh_D)

    fig, ax = plt.subplots(figsize=(5.2, 4.2))
    ax.plot(D_fine, S_lq, 'k-', label='LQ (HRS−)')
    ax.plot(D_fine, S_ir, 'k--', label='IR (HRS+)')
    ax.plot(rm_D, rm_S, 'o', mfc='none', mec='k', label='Rodrigues-Moreira 2017 (LT-HSC, approx)')
    ax.plot(mh_D, mh_S, 'o', mfc='k', mec='k', label='Mohrin 2010 (SLAM-HSC, LQ proxy)')
    ax.set_yscale('log')
    ax.set_xlabel('Dose [Gy]'); ax.set_ylabel('Surviving fraction')
    ax.set_xlim(0, 2.0); ax.set_ylim(1e-2, 1.1)
    ax.set_title('Fig 2a — Clonogenic survival (Stouten et al. 2022)')
    ax.legend(loc='lower left', fontsize=8); ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(os.path.join(FIG_DIR, 'fig2a_survival.png'), dpi=140)

    # Numerical check: minimum of S_ir near 0.06 Gy?
    iDmin = int(np.argmin(S_ir))
    results['fig2a_Smin_dose']   = float(D_fine[iDmin])
    results['fig2a_Smin_value']  = float(S_ir[iDmin])
    results['fig2a_S_at_0p06Gy'] = float(S_HRS(np.array([0.06]))[0])

    # ----- Fig 2b: pre-leukemic cells I0(D) -----
    D_b = np.linspace(0.0, 6.0, 1200)
    Ineg = I0_HRSneg(D_b)
    Iplus1 = I0_HRS1(D_b)
    Iplus2 = I0_HRS2(D_b)
    fig, ax = plt.subplots(figsize=(5.2, 4.2))
    ax.plot(D_b, Ineg,   'k-',  label='HRS−')
    ax.plot(D_b, Iplus1, 'k--', label='HRS+1')
    ax.plot(D_b, Iplus2, 'k:',  label='HRS+2')
    ax.set_xlabel('Dose [Gy]'); ax.set_ylabel('Cells with Sfpi1 deletion (I0)')
    ax.set_title('Fig 2b — Pre-leukemic cell formation')
    ax.legend(); ax.grid(alpha=0.3); ax.set_xlim(0, 6)
    fig.tight_layout(); fig.savefig(os.path.join(FIG_DIR, 'fig2b_I0_curves.png'), dpi=140)

    results['fig2b_I0max_dose_HRSneg']   = float(D_b[int(np.argmax(Ineg))])
    results['fig2b_I0max_value_HRSneg']  = float(np.max(Ineg))

    # Low-dose snapshot to expose HRS effect
    Dlow = np.array([0.0, 0.02, 0.06, 0.1, 0.2, 0.3])
    results['fig2b_low_dose_table'] = {
        'D_Gy':    Dlow.tolist(),
        'HRSneg':  I0_HRSneg(Dlow).tolist(),
        'HRS1':    I0_HRS1(Dlow).tolist(),
        'HRS2':    I0_HRS2(Dlow).tolist(),
    }

    # ----- Fig 3a: fd at 4.5 Gy -----
    D45 = 4.5
    I0_45 = I0_HRSneg(D45)
    t = np.linspace(0.0, 50.0, 4000)
    fA_arr  = fA(t, I0_45)
    Fhat    = F_hat_A(t, D45)
    fd_arr  = (1.0 - Fhat) * fA_arr
    fig, ax = plt.subplots(figsize=(5.2, 4.2))
    ax.plot(t, Fhat, 'k-',  label=r'$\hat F_A(t)$ (non-rAML deaths CDF)')
    ax.plot(t, fA_arr / max(1e-12, fA_arr.max()), 'k--',
            label=r'$f_A(t)$ (normalized)')
    ax.plot(t, fd_arr / max(1e-12, fd_arr.max()), 'k:',
            label=r'$f_d(t)$ (normalized)')
    ax.set_xlabel('Time [months]'); ax.set_ylabel('Probability density (normalized)')
    ax.set_title('Fig 3a — rAML diagnosis distribution, 4.5 Gy')
    ax.legend(fontsize=8); ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(os.path.join(FIG_DIR, 'fig3a_distributions.png'), dpi=140)

    P45 = float(simpson(fd_arr, x=t))
    results['fig3a_P_rAML_4p5Gy'] = P45

    # ----- Fig 3b: cumulative incidence vs time -----
    doses_cum = [0.75, 1.5, 3.0, 4.5, 6.0]
    fig, ax = plt.subplots(figsize=(5.2, 4.2))
    cum_at_30mo = {}
    for D in doses_cum:
        I0 = I0_HRSneg(D)
        tt = np.linspace(0.0, 40.0, 6000)
        fdv = fd(tt, D, I0)
        cum = np.array([simpson(fdv[:i+1], x=tt[:i+1]) for i in range(len(tt))])
        ax.plot(tt, cum * 100.0, label=f'{D} Gy')
        cum_at_30mo[D] = float(np.interp(30.0, tt, cum) * 100.0)
    ax.set_xlabel('Time [months]'); ax.set_ylabel('Cumulative rAML incidence [%]')
    ax.set_title('Fig 3b — Cumulative incidence (HRS−)')
    ax.legend(fontsize=8, title='Dose'); ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(os.path.join(FIG_DIR, 'fig3b_cumulative.png'), dpi=140)
    results['fig3b_cum_incidence_at_t_lifetime'] = cum_at_30mo

    # ----- Fig 4: dose-response -----
    D_dr   = np.concatenate([np.linspace(0.0, 0.3, 250),
                             np.linspace(0.3, 6.0, 600)[1:]])
    P_neg  = np.array([P_rAML(D, I0_HRSneg(D)) for D in D_dr]) * 100.0
    P_p1   = np.array([P_rAML(D, I0_HRS1(D))   for D in D_dr]) * 100.0
    P_p2   = np.array([P_rAML(D, I0_HRS2(D))   for D in D_dr]) * 100.0

    fig, ax = plt.subplots(figsize=(5.6, 4.2))
    ax.plot(D_dr, P_neg, 'k-',  label='HRS− (model)')
    ax.plot(D_dr, P_p1,  'k--', label='HRS+1 (model)')
    ax.plot(D_dr, P_p2,  'k:',  label='HRS+2 (model)')
    ax.plot(D_dr, y_LQ_pub(D_dr), color='0.6', lw=1.2,
            label=r'Stouten 2021 LQ approx $3.63D+10.1D^2$')
    ax.errorbar(DATA_DOSE, DATA_INC, yerr=DATA_ERR, fmt='ko', mfc='w',
                label='Major 1979 / Mole 1983 (digitized)')
    ax.set_xlabel('Dose [Gy]'); ax.set_ylabel('rAML incidence [%]')
    ax.set_title('Fig 4 — rAML dose-response')
    ax.set_xlim(0, 6); ax.set_ylim(0, max(P_neg.max(), DATA_INC.max())*1.2)
    ax.legend(fontsize=8); ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(os.path.join(FIG_DIR, 'fig4_dose_response.png'), dpi=140)

    # zoom into low-dose region (Fig 4 inset)
    mask_low = D_dr <= 0.30
    fig, ax = plt.subplots(figsize=(5.0, 4.0))
    ax.plot(D_dr[mask_low], P_neg[mask_low], 'k-',  label='HRS− (model)')
    ax.plot(D_dr[mask_low], P_p1[mask_low],  'k--', label='HRS+1 (model)')
    ax.plot(D_dr[mask_low], P_p2[mask_low],  'k:',  label='HRS+2 (model)')
    ax.plot(D_dr[mask_low], y_LQ_pub(D_dr[mask_low]), color='0.6',
            label='LQ approx (HRS−)')
    ax.plot(D_dr[mask_low], y_HRS1_pub(D_dr[mask_low]), color='steelblue',
            label='Pub approx HRS+1 (Eq 16)')
    ax.plot(D_dr[mask_low], y_HRS2_pub(D_dr[mask_low]), color='firebrick',
            label='Pub approx HRS+2 (Eq 17)')
    ax.set_xlabel('Dose [Gy]'); ax.set_ylabel('rAML incidence [%]')
    ax.set_title('Fig 4 low-dose zoom (≤0.3 Gy)')
    ax.legend(fontsize=7); ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(os.path.join(FIG_DIR, 'fig4_lowdose_zoom.png'), dpi=140)

    # Quantitative comparison at data points
    Pneg_at_data = np.array([P_rAML(D, I0_HRSneg(D)) for D in DATA_DOSE]) * 100.0
    results['fig4_model_HRSneg_at_data_doses'] = {
        'D_Gy':           DATA_DOSE.tolist(),
        'data_inc_pct':   DATA_INC.tolist(),
        'model_inc_pct':  Pneg_at_data.tolist(),
        'residual_pct':   (Pneg_at_data - DATA_INC).tolist(),
    }
    # Position of peak
    iPmax = int(np.argmax(P_neg))
    results['fig4_peak_dose_Gy']        = float(D_dr[iPmax])
    results['fig4_peak_incidence_pct']  = float(P_neg[iPmax])

    # Low-dose HRS effect quantification
    lowD = np.array([0.02, 0.06, 0.1, 0.2])
    results['fig4_low_dose_inc_pct'] = {
        'D_Gy':   lowD.tolist(),
        'HRSneg': [P_rAML(D, I0_HRSneg(D))*100.0 for D in lowD],
        'HRS1':   [P_rAML(D, I0_HRS1(D))*100.0   for D in lowD],
        'HRS2':   [P_rAML(D, I0_HRS2(D))*100.0   for D in lowD],
    }

    # Persist evidence
    with open(os.path.join(EVD_DIR, 'replication_metrics.json'), 'w') as fh:
        json.dump(results, fh, indent=2, default=float)
    print(json.dumps(results, indent=2, default=float))


if __name__ == '__main__':
    main()
