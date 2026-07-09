"""
Reproduce paper Figures 2-5 with the IMK model and compare with the
digitised experimental data.
"""

import json
import os
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import least_squares

import imk_model as imk
import reference_data as ref

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FIG = ROOT / 'figures'
RES = ROOT / 'results'
FIG.mkdir(exist_ok=True)
RES.mkdir(exist_ok=True)


# -------- helpers ------------ #

def r2_score(y_obs, y_pred):
    y_obs = np.asarray(y_obs, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    ss_res = np.sum((y_obs - y_pred) ** 2)
    ss_tot = np.sum((y_obs - y_obs.mean()) ** 2)
    if ss_tot == 0:
        return float('nan')
    return 1.0 - ss_res / ss_tot


# -------- Figure 0: signal-vs-DOSE (paper's LQ-weighted target activation) #

def figure_signal_vs_dose():
    """Reproduce the paper's claim 1: the cell-killing signal
    emission probability follows an LQ function of dose.  We plot the
    average number of hits per cell <N_h> and the hit fraction f_h(D)
    using the V79-379A and T-47D NTE parameters from Table 2."""
    D = np.linspace(0, 5.0, 400)
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
    for name in ('V79-379A', 'T-47D', 'HPV-G'):
        cp = imk.PAPER_PARAMS[name]
        Nh = (cp.alpha_b + cp.gamma * cp.beta_b) * D + cp.beta_b * D * D
        fh = 1.0 - np.exp(-Nh)
        ax[0].plot(D, Nh, label=name)
        ax[1].plot(D, fh, label=name)
    ax[0].set_xlabel('Dose [Gy]')
    ax[0].set_ylabel('<N_h>  (LQ-weighted signal-release hits / cell)')
    ax[0].set_title('Eq. 7:  N_h = (α_b + γβ_b) D + β_b D²')
    ax[0].grid(alpha=0.3)
    ax[0].legend()

    ax[1].set_xlabel('Dose [Gy]')
    ax[1].set_ylabel('f_h(D)  (Eq. 8: fraction of hit cells)')
    ax[1].set_title('Eq. 8:  f_h = 1 - exp(-N_h)  (Poisson)')
    ax[1].grid(alpha=0.3)
    ax[1].legend()
    fig.suptitle('Figure 0 (rep. paper claim 1): NTE signal-release as LQ '
                 'function of dose')
    fig.tight_layout()
    fig.savefig(FIG / 'fig0_signal_vs_dose.png', dpi=140)
    plt.close(fig)
    return {'D_for_fh_eq_0p5_V79': float(D[np.argmin(np.abs(
        (1.0 - np.exp(-((imk.PAPER_PARAMS['V79-379A'].alpha_b
                          + imk.PAPER_PARAMS['V79-379A'].gamma
                            * imk.PAPER_PARAMS['V79-379A'].beta_b) * D
                         + imk.PAPER_PARAMS['V79-379A'].beta_b * D * D))) - 0.5))])}


# -------- Figure 1: signal concentration vs time ------------------- #

def figure_signals():
    t_plot = np.logspace(-3, 1.5, 400)

    rho_ca = imk.signal_concentration_normalized(t_plot, **imk.SIGNAL_PARAMS_CALCIUM)
    rho_no = imk.signal_concentration_normalized(t_plot, **imk.SIGNAL_PARAMS_NO)

    # Model predictions at the data times
    pred_ca = imk.signal_concentration_normalized(ref.CALCIUM_T, **imk.SIGNAL_PARAMS_CALCIUM)
    pred_no = imk.signal_concentration_normalized(ref.NO_T, **imk.SIGNAL_PARAMS_NO)
    r2_ca = r2_score(ref.CALCIUM_REL, pred_ca)
    r2_no = r2_score(ref.NO_REL, pred_no)

    fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))

    ax[0].plot(t_plot, rho_ca, 'b-', label='IMK model (calcium)')
    ax[0].plot(ref.CALCIUM_T, ref.CALCIUM_REL, 'bs', label='Lyng et al. 2002 (digitised)')
    ax[0].set_xlabel('Time after irradiation [h]')
    ax[0].set_ylabel('Relative signal concentration')
    ax[0].set_xlim(0, 1.0)
    ax[0].set_title(f'Calcium signal  (μ_s=80.4, λ+R=79.3 h⁻¹)\n'
                    f'R² ≈ {r2_ca:.3f}')
    ax[0].legend()
    ax[0].grid(alpha=0.3)

    ax[1].plot(t_plot, rho_no, 'r-', label='IMK model (NO)')
    ax[1].plot(ref.NO_T, ref.NO_REL, 'r^', label='Han et al. 2007 (digitised)')
    ax[1].set_xlabel('Time after irradiation [h]')
    ax[1].set_ylabel('Relative signal concentration')
    ax[1].set_xlim(0, 15)
    ax[1].set_title(f'NO signal  (μ_s=11.0, λ+R=0.192 h⁻¹)\n'
                    f'R² ≈ {r2_no:.3f}')
    ax[1].legend()
    ax[1].grid(alpha=0.3)

    fig.suptitle('Figure 1 (rep. paper Fig. 2A): Cell-killing signal kinetics')
    fig.tight_layout()
    fig.savefig(FIG / 'fig1_signal_kinetics.png', dpi=140)
    plt.close(fig)
    return {'R2_calcium': float(r2_ca), 'R2_NO': float(r2_no)}


# -------- Figure 2: DSB kinetics (TE vs TE+NTE) -------------------- #

def figure_dsb_kinetics():
    """Reproduce Fig 2(B). DSBs/nucleus vs time for several low doses, with
    and without lower repair efficiency in non-hit cells."""

    # Use MRC-5 parameter set from Table 1
    p = imk.DAMAGE_PARAMS_MRC5
    # TE-only DSB kinetics: x_d(t) = k_d * p_dom * <g> * D * exp(-(a+c)*t)
    # (Number of PLLs per nucleus from acute irradiation)
    kdg_total = p['kd_g']     # Gy^-1 per domain
    p_dom = p['p']

    t = np.linspace(0, 24, 240)
    doses_mGy = [1000, 100, 10]   # mGy
    fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))

    nte_params = {
        'a': p['a'], 'c_b': p['a_plus_cb'] - p['a'],
        'mu_s': imk.SIGNAL_PARAMS_CALCIUM['mu_s'],
        'lam_plus_R': imk.SIGNAL_PARAMS_CALCIUM['lam_plus_R'],
        'K_amp': p['K_amp_calcium'],
        'alpha_b': p['alpha_b'], 'beta_b': p['beta_b'],
        'gamma': p['gamma'],
    }

    # NOTE: kdg_total is per-domain, multiply by p to convert to per-nucleus
    for D_mGy in doses_mGy:
        D = D_mGy * 1e-3  # Gy
        # TE only
        xT = kdg_total * p_dom * D * np.exp(-p['a_plus_c'] * t)
        # NTE
        xN = imk.x_b_NTE(t, D, nte_params) * p_dom
        ax[0].plot(t, xT, label=f'{D_mGy} mGy (TE only)')
        ax[1].plot(t, xT + xN, label=f'{D_mGy} mGy (TE+NTE)')

    for a in ax:
        a.set_xlabel('Time after irradiation [h]')
        a.set_ylabel('DSBs per nucleus (model)')
        a.set_yscale('log')
        a.set_xlim(0, 24)
        a.set_ylim(1e-2, 100)
        a.grid(alpha=0.3, which='both')
        a.legend(fontsize=8)

    ax[0].set_title('Targeted Effects only (Eq. 1-3)')
    ax[1].set_title('Integrated TE + NTE (Eq. 1-3 + Eq. 10-13)\n'
                    'with reduced repair in non-hit cells (c_b ≪ c)')
    fig.suptitle('Figure 2 (rep. paper Fig. 2B): DSB kinetics in MRC-5 cells')
    fig.tight_layout()
    fig.savefig(FIG / 'fig2_dsb_kinetics.png', dpi=140)
    plt.close(fig)

    # Quick numbers
    return {
        'a_plus_c_TE': p['a_plus_c'],
        'a_plus_cb_NTE': p['a_plus_cb'],
        'repair_ratio_TE_over_NTE': p['a_plus_c'] / p['a_plus_cb'],
    }


# -------- Figure 3: survival curves with HRS (V79-379A and T-47D) --- #

def figure_survival():
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
    D = np.linspace(0.001, 5.5, 600)
    results = {}

    for i, (name, dose, sf) in enumerate(
        [('V79-379A', ref.V79_DOSE, ref.V79_SF),
         ('T-47D',    ref.T47D_DOSE, ref.T47D_SF)]):
        cp = imk.PAPER_PARAMS[name]
        S_te = imk.S_T(D, cp.alpha0, cp.beta0, cp.gamma)
        S_tot = imk.S_total(D, cp.alpha0, cp.beta0, cp.gamma,
                            cp.delta, cp.alpha_b, cp.beta_b)
        ax[i].semilogy(D, S_te, 'k:', label='IMK (TE only)')
        ax[i].semilogy(D, S_tot, 'k-', label='IMK (TE + IC)')
        ax[i].semilogy(dose[1:], sf[1:], 'o', mfc='none', label='exp (digitised)')
        ax[i].set_xlabel('Dose [Gy]')
        ax[i].set_ylabel('Surviving fraction')
        ax[i].set_xlim(0, 5.5)
        ax[i].set_ylim(1e-4, 1.2)
        ax[i].legend(loc='lower left')
        ax[i].grid(alpha=0.3, which='both')

        # R^2 over digitised points (in log SF)
        S_at_data = imk.S_total(dose[1:], cp.alpha0, cp.beta0, cp.gamma,
                                cp.delta, cp.alpha_b, cp.beta_b)
        r2 = r2_score(np.log(sf[1:]), np.log(S_at_data))
        ax[i].set_title(f'{name}  (R²_logSF ≈ {r2:.2f})')
        results[name] = {
            'R2_logSF_vs_digitised': float(r2),
            'paper_params': {k: float(v) for k, v in
                             [('alpha0', cp.alpha0), ('beta0', cp.beta0),
                              ('a_plus_c', cp.a_plus_c),
                              ('alpha_b', cp.alpha_b), ('beta_b', cp.beta_b),
                              ('delta', cp.delta), ('gamma', cp.gamma)]},
            'model_S_at_0p1Gy': float(imk.S_total(
                0.1, cp.alpha0, cp.beta0, cp.gamma,
                cp.delta, cp.alpha_b, cp.beta_b)),
            'model_S_at_2Gy': float(imk.S_total(
                2.0, cp.alpha0, cp.beta0, cp.gamma,
                cp.delta, cp.alpha_b, cp.beta_b)),
        }

    fig.suptitle('Figure 3 (rep. paper Fig. 2C-D): SF with low-dose HRS')
    fig.tight_layout()
    fig.savefig(FIG / 'fig3_survival_HRS.png', dpi=140)
    plt.close(fig)
    return results


# -------- Figure 4: MTBE (HPV-G, E48) ------------------------------ #

def figure_mtbe():
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
    D = np.linspace(1e-3, 5.5, 600)
    res = {}
    for i, (name, dose, sf) in enumerate(
        [('HPV-G', ref.HPVG_DONOR_DOSE, ref.HPVG_SF),
         ('E48', ref.E48_DONOR_DOSE, ref.E48_SF)]):
        cp = imk.PAPER_PARAMS[name]
        S = imk.S_NTE_MTBE(D, cp.delta, cp.alpha_b, cp.beta_b, cp.gamma)
        ax[i].semilogx(D, S, 'k-', label='Modified IMK model (Eq. 25)')
        ax[i].semilogx(dose[1:], sf[1:], 'o', mfc='none', label='exp (digitised)')
        ax[i].set_xlabel('Donor cell dose [Gy]')
        ax[i].set_ylabel('Surviving fraction of recipient cells')
        ax[i].set_xlim(1e-3, 6)
        ax[i].set_ylim(0.0, 1.2)
        ax[i].grid(alpha=0.3, which='both')
        ax[i].legend(loc='lower left')

        S_at_data = imk.S_NTE_MTBE(dose[1:], cp.delta, cp.alpha_b,
                                   cp.beta_b, cp.gamma)
        r2 = r2_score(sf[1:], S_at_data)
        ax[i].set_title(f'{name}  (R² ≈ {r2:.2f})')
        res[name] = {'R2_vs_digitised': float(r2),
                     'paper_delta_m': cp.delta,
                     'paper_alpha_b': cp.alpha_b,
                     'paper_beta_b': cp.beta_b}

    fig.suptitle('Figure 4 (rep. paper Fig. 3): MTBE SF (Eq. 25)')
    fig.tight_layout()
    fig.savefig(FIG / 'fig4_mtbe.png', dpi=140)
    plt.close(fig)
    return res


# -------- Figure 5: CHO-K1 sham vs repair-inhibited ----------------- #

def figure_cho_repair():
    fig, ax = plt.subplots(figsize=(7, 5))
    D = np.linspace(1e-3, 4.5, 600)
    res = {}

    sham = imk.PAPER_PARAMS['CHO-K1-sham']
    inh = imk.PAPER_PARAMS['CHO-K1-repair-inhibited']

    S_sham = imk.S_total(D, sham.alpha0, sham.beta0, sham.gamma,
                         sham.delta, sham.alpha_b, sham.beta_b)
    S_inh = imk.S_total(D, inh.alpha0, inh.beta0, inh.gamma,
                        inh.delta, inh.alpha_b, inh.beta_b)
    ax.semilogy(D, S_sham, 'b-', label='IMK sham CHO-K1')
    ax.semilogy(D, S_inh, 'r-', label='IMK PARP-inhibited CHO-K1')
    ax.semilogy(ref.CHO_DOSE[1:], ref.CHO_SHAM_SF[1:], 'bo', mfc='none',
                label='sham (digitised, Chalmers 2004)')
    ax.semilogy(ref.CHO_DOSE[1:], ref.CHO_PARP_SF[1:], 'r^', mfc='none',
                label='PARP-inh (digitised)')
    ax.set_xlabel('Dose [Gy]')
    ax.set_ylabel('Surviving fraction')
    ax.set_xlim(0, 4.5)
    ax.set_ylim(1e-4, 1.2)
    ax.grid(alpha=0.3, which='both')
    ax.legend(loc='lower left')

    r2_sham = r2_score(np.log(ref.CHO_SHAM_SF[1:]),
                       np.log(imk.S_total(ref.CHO_DOSE[1:], sham.alpha0,
                                          sham.beta0, sham.gamma,
                                          sham.delta, sham.alpha_b,
                                          sham.beta_b)))
    r2_inh = r2_score(np.log(ref.CHO_PARP_SF[1:]),
                      np.log(imk.S_total(ref.CHO_DOSE[1:], inh.alpha0,
                                         inh.beta0, inh.gamma,
                                         inh.delta, inh.alpha_b,
                                         inh.beta_b)))
    ax.set_title(f'CHO-K1 sham vs PARP-inhibited  '
                 f'(R²_log: sham={r2_sham:.2f}, inh={r2_inh:.2f})')
    fig.suptitle('Figure 5 (rep. paper Fig. 4): role of repair efficiency '
                 'in non-hit cells')
    fig.tight_layout()
    fig.savefig(FIG / 'fig5_cho_repair_inhibition.png', dpi=140)
    plt.close(fig)

    res['R2_logSF_sham'] = float(r2_sham)
    res['R2_logSF_PARP_inhibited'] = float(r2_inh)
    return res


# -------- Figure 6: HRS sensitivity to repair-rate cb factor -------- #

def figure_hrs_sensitivity():
    """Reproduce Fig 5(B): V79-379A SF curves for cb scaled x4, x1, x1/2, x1/4."""
    cp = imk.PAPER_PARAMS['V79-379A']
    a = 8.12e-3   # h^-1
    cb0 = 0.155   # h^-1
    # delta ∝ a/(a+c_b)
    delta_base = cp.delta
    factors = [4.0, 1.0, 0.5, 0.25]
    D = np.linspace(0.005, 1.5, 400)
    fig, ax = plt.subplots(figsize=(7, 5))
    for f in factors:
        cb = cb0 * f
        delta_f = delta_base * (a + cb0) / (a + cb)
        S = imk.S_total(D, cp.alpha0, cp.beta0, cp.gamma, delta_f,
                        cp.alpha_b, cp.beta_b)
        ax.plot(D, S, label=f'c_b × {f}')
    ax.set_xlabel('Dose [Gy]')
    ax.set_ylabel('Surviving fraction')
    ax.set_yscale('log')
    ax.set_xlim(0, 1.5)
    ax.set_ylim(0.2, 1.05)
    ax.grid(alpha=0.3, which='both')
    ax.legend(loc='lower left')
    ax.set_title('V79-379A — HRS depth vs DNA-repair rate c_b in non-hit cells')
    fig.suptitle('Figure 6 (rep. paper Fig. 5B): repair-rate scan')
    fig.tight_layout()
    fig.savefig(FIG / 'fig6_hrs_repair_scan.png', dpi=140)
    plt.close(fig)
    return {'factors_tested': factors, 'cb_base_h-1': cb0}


# -------- Fit V79-379A from scratch (independent fit) --------------- #

def fit_v79_from_scratch():
    """Independent maximum-likelihood (least-squares on log SF) fit of the
    7-parameter IMK model to the V79-379A digitised data, then compare with
    the paper's reported parameter set."""

    dose = ref.V79_DOSE[1:]
    sf = ref.V79_SF[1:]
    log_sf = np.log(sf)

    # Parameters to fit: alpha0, beta0, alpha_b, beta_b, delta
    # (Keep gamma at paper's value; a_plus_c kept at 6.29 since acute irrad.)
    gamma = 0.924

    def residuals(theta):
        a0, b0, ab, bb, dl = theta
        a0, b0, ab, bb, dl = abs(a0), abs(b0), abs(ab), abs(bb), abs(dl)
        Smod = imk.S_total(dose, a0, b0, gamma, dl, ab, bb)
        Smod = np.clip(Smod, 1e-10, 1.0)
        return np.log(Smod) - log_sf

    # Use bounded TRF with bounds anchored near paper values (within 10x range)
    x0 = [0.05, 0.3, 1.5, 0.4, 0.25]   # rough starting point near paper values
    lower = [1e-3, 1e-3, 0.1, 0.01, 0.02]
    upper = [1.0, 2.0, 30.0, 5.0, 1.5]
    sol = least_squares(residuals, x0, method='trf', bounds=(lower, upper),
                        max_nfev=8000)
    a0, b0, ab, bb, dl = [abs(x) for x in sol.x]
    Smod_at = imk.S_total(dose, a0, b0, gamma, dl, ab, bb)
    r2 = r2_score(np.log(sf), np.log(Smod_at))

    return {
        'fit_alpha0': a0,
        'fit_beta0': b0,
        'fit_alpha_b': ab,
        'fit_beta_b': bb,
        'fit_delta': dl,
        'fit_R2_logSF': float(r2),
        'paper_alpha0': 1.60e-2,
        'paper_beta0':  6.00e-1,
        'paper_alpha_b': 1.46,
        'paper_beta_b':  3.96e-1,
        'paper_delta':   2.57e-1,
        'cost': float(sol.cost),
    }


# -------- main ----------------------------------------------------- #

def main():
    summary = {}
    summary['fig0_signal_vs_dose'] = figure_signal_vs_dose()
    summary['fig1_signals'] = figure_signals()
    summary['fig2_dsb_kinetics'] = figure_dsb_kinetics()
    summary['fig3_survival'] = figure_survival()
    summary['fig4_mtbe'] = figure_mtbe()
    summary['fig5_cho_repair'] = figure_cho_repair()
    summary['fig6_hrs_scan'] = figure_hrs_sensitivity()
    summary['independent_v79_fit'] = fit_v79_from_scratch()

    with open(RES / 'summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
