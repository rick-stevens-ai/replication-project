#!/usr/bin/env python3
"""Generate all figures for the replication of Gori et al. (2025)."""
import sys, os, pickle, warnings
warnings.filterwarnings('ignore')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.lines import Line2D

PROJECT_DIR = os.path.expanduser("~/projects/replicate-darkmatter")
FIG_DIR     = os.path.join(PROJECT_DIR, "figures")
PKL_PATH    = os.path.join(PROJECT_DIR, "data", "all_results.pkl")
DE_DATA     = os.path.join(PROJECT_DIR, "darkelf_repo", "data") + "/"
sys.path.insert(0, os.path.join(PROJECT_DIR, "darkelf_repo"))

os.makedirs(FIG_DIR, exist_ok=True)

# ── colour / style palette ──────────────────────────────────────────────────
TH_COLOR = {'1meV':'#1f77b4','20meV':'#ff7f0e','100meV':'#2ca02c','1eV':'#d62728'}
TH_LABEL = {'1meV':r'$E_{\rm th}=1$ meV','20meV':r'$E_{\rm th}=20$ meV',
            '100meV':r'$E_{\rm th}=100$ meV','1eV':r'$E_{\rm th}=1$ eV'}

def load():
    with open(PKL_PATH,'rb') as f: return pickle.load(f)

def valid(arr, sigma_max=1e-10):
    """Boolean mask: physically sensible cross-section values."""
    return np.isfinite(arr) & (arr > 0) & (arr < sigma_max)

def splot(ax, mx_MeV, arr, **kw):
    m = valid(arr)
    if m.sum() > 1:
        ax.loglog(mx_MeV[m], arr[m], **kw)
        return True
    return False

def leg_handles(include_targets=True):
    h = [Line2D([],[],color=TH_COLOR[t],lw=1.8) for t in ['1meV','20meV','100meV','1eV']]
    l = [TH_LABEL[t] for t in ['1meV','20meV','100meV','1eV']]
    if include_targets:
        h += [Line2D([],[],color='k',lw=1.8,ls='-'),
              Line2D([],[],color='k',lw=1.8,ls='--')]
        l += [r'Al$_2$O$_3$','GaAs']
    return h, l

def fmt_ax(ax, ylabel, title, xlim=(1e-3,1e3)):
    ax.set_xlabel(r'$m_\chi$ [MeV]', fontsize=13)
    ax.set_ylabel(ylabel, fontsize=13)
    ax.set_title(title, fontsize=12)
    ax.set_xlim(*xlim)
    ax.grid(True, alpha=0.25, which='both')
    ax.minorticks_on()


# ── Figure 5 : Phonon partial DOS ────────────────────────────────────────────
def fig5_phonon_dos():
    import darkelf as de
    devnull = open(os.devnull,'w')
    old=sys.stdout; sys.stdout=devnull
    dG = de.darkelf(target='GaAs',   mX=1e6, eps_data_dir=DE_DATA)
    dA = de.darkelf(target='Al2O3',  mX=1e6, eps_data_dir=DE_DATA)
    sys.stdout=old; devnull.close()

    fig, axes = plt.subplots(1,2,figsize=(13,4.5))
    specs = [('GaAs',dG,['#e67e22','#c0392b'],45),
             ('Al2O3',dA,['#27ae60','#8e44ad'],130)]

    for ax,(tname,d,cols,xmax) in zip(axes,specs):
        # Evaluate DOS via interpolant on fine grid
        om_hi = d.dos_omega_range[-1] if hasattr(d.dos_omega_range,'__len__') else d.dos_omega_range[1]
        om_lo = d.dos_omega_range[0]  if hasattr(d.dos_omega_range,'__len__') else d.dos_omega_range[0]
        omegas = np.linspace(om_lo, om_hi, 600)
        for i,atom in enumerate(d.atoms):
            dos = d.DoS_interp[i](omegas)      # 1/eV
            ax.plot(omegas*1000, dos/1000, color=cols[i], lw=1.6, label=atom)
        ax.set_xlabel(r'$\omega$ [meV]', fontsize=13)
        ax.set_ylabel(r'$D_d(\omega)$ [1/meV]', fontsize=13)
        title = r'Al$_2$O$_3$' if tname=='Al2O3' else tname
        ax.set_title(title, fontsize=13)
        ax.set_xlim(0, xmax)
        ax.legend(fontsize=11)
        ax.grid(True,alpha=0.25)

    fig.suptitle('Phonon partial density of states  (cf. Fig. 5 of Gori et al. 2025)',
                 fontsize=13, y=1.01)
    fig.tight_layout()
    fig.savefig(f'{FIG_DIR}/fig5_phonon_dos.png', dpi=150, bbox_inches='tight')
    plt.close(); print('  ✓ fig5_phonon_dos.png')


# ── Figure 6 : ϕ mediator ────────────────────────────────────────────────────
def fig6_phi(R):
    mx = R['mx_eV']/1e6
    fig, axes = plt.subplots(1,2,figsize=(15,6))
    for ax, regime, med_str in zip(axes,
                                   ['heavy','light'],
                                   [r'$m_\phi=3\,q_0$',r'$m_\phi=0.3\,q_0$']):
        for tgt,ls in [('Al2O3','-'),('GaAs','--')]:
            key=f'{tgt}_phi_{regime}'
            for th in ['1meV','20meV','100meV','1eV']:
                if key in R and th in R[key]:
                    splot(ax, mx, R[key][th], color=TH_COLOR[th], ls=ls, lw=1.7)
        fmt_ax(ax, r'$\bar\sigma_\phi$ [cm$^2$]',
               rf'$\phi$ mediator ({regime}),  {med_str}')
        h,l = leg_handles()
        ax.legend(h,l, fontsize=8.5, loc='upper left')

    fig.suptitle(r'Fig. 6  —  $\phi$ mediator: $\bar\sigma_\phi$ for 3 events / kg·yr',
                 fontsize=13, y=1.01)
    fig.tight_layout()
    fig.savefig(f'{FIG_DIR}/fig6_phi.png', dpi=150, bbox_inches='tight')
    plt.close(); print('  ✓ fig6_phi.png')


# ── Figure 7 : a mediator ────────────────────────────────────────────────────
def fig7_a(R):
    mx = R['mx_eV']/1e6
    fig, axes = plt.subplots(1,2,figsize=(15,6))
    for ax, regime, med_str in zip(axes,
                                   ['heavy','light'],
                                   [r'$m_a=3\,q_0$',r'$m_a=0.3\,q_0$']):
        for tgt,ls in [('Al2O3','-'),('GaAs','--')]:
            key=f'{tgt}_a_{regime}'
            for th in ['1meV','20meV','100meV','1eV']:
                if key in R and th in R[key]:
                    splot(ax, mx, R[key][th], color=TH_COLOR[th], ls=ls, lw=1.7)
        fmt_ax(ax, r'$\bar\sigma_a$ [cm$^2$]',
               rf'$a$ mediator ({regime}),  {med_str}')
        h,l = leg_handles()
        ax.legend(h,l, fontsize=8.5, loc='upper left')

    fig.suptitle(r'Fig. 7  —  $a$ mediator: $\bar\sigma_a$ for 3 events / kg·yr',
                 fontsize=13, y=1.01)
    fig.tight_layout()
    fig.savefig(f'{FIG_DIR}/fig7_a.png', dpi=150, bbox_inches='tight')
    plt.close(); print('  ✓ fig7_a.png')


# ── Figure 8 : A′ mediator ───────────────────────────────────────────────────
def fig8_Aprime(R):
    mx = R['mx_eV']/1e6
    fig, ax = plt.subplots(figsize=(9,6.5))
    for tgt,ls in [('Al2O3','-'),('GaAs','--')]:
        key=f"{tgt}_A'_heavy"
        for th in ['1meV','20meV','100meV','1eV']:
            if key in R and th in R[key]:
                splot(ax, mx, R[key][th], color=TH_COLOR[th], ls=ls, lw=1.7)
    fmt_ax(ax, r"$\bar\sigma_{A'}$ [cm$^2$]",
           r"$A'$ mediator (heavy),  $m_{A'}=10$ GeV")
    h,l = leg_handles()
    ax.legend(h,l, fontsize=9, loc='upper left')
    fig.tight_layout()
    fig.savefig(f'{FIG_DIR}/fig8_Aprime.png', dpi=150, bbox_inches='tight')
    plt.close(); print('  ✓ fig8_Aprime.png')


# ── SD vs SI comparison ───────────────────────────────────────────────────────
def fig_sd_vs_si(R):
    mx = R['mx_eV']/1e6
    fig, axes = plt.subplots(1,2,figsize=(15,6))
    for ax, tgt in zip(axes, ['Al2O3','GaAs']):
        for th, col in [('1meV','#1f77b4'),('1eV','#d62728')]:
            ksd = f"{tgt}_A'_heavy";  ksi = f"{tgt}_SI_heavy"
            if ksd in R and th in R[ksd]:
                splot(ax, mx, R[ksd][th], color=col, ls='-',  lw=2,
                      label=f"SD (A\u2032) {TH_LABEL[th]}")
            if ksi in R and th in R[ksi]:
                splot(ax, mx, R[ksi][th], color=col, ls='--', lw=2,
                      label=f"SI {TH_LABEL[th]}")
        tname = r'Al$_2$O$_3$' if tgt=='Al2O3' else tgt
        fmt_ax(ax, r'$\bar\sigma$ [cm$^2$]',
               f'{tname}: SD vs SI  (heavy mediator)')
        ax.legend(fontsize=9, loc='best')
    fig.suptitle('SD vs SI comparison  (cf. Figs 6 & 8 of Gori et al.)',
                 fontsize=13, y=1.01)
    fig.tight_layout()
    fig.savefig(f'{FIG_DIR}/sd_vs_si.png', dpi=150, bbox_inches='tight')
    plt.close(); print('  ✓ sd_vs_si.png')


# ── All operators summary for Al₂O₃ ─────────────────────────────────────────
def fig_all_ops(R):
    mx = R['mx_eV']/1e6
    fig, ax = plt.subplots(figsize=(10,6.5))
    cfg = [
        ("A'", 'heavy', '#1f77b4', '-',  2.0, r"$A'$  heavy  ($m_{A'}=10$ GeV)"),
        ('phi','heavy', '#ff7f0e', '-',  2.0, r'$\phi$  heavy  ($m_\phi=3\,q_0$)'),
        ('phi','light', '#ff7f0e', '--', 1.5, r'$\phi$  light  ($m_\phi=0.3\,q_0$)'),
        ('a',  'heavy', '#2ca02c', '-',  2.0, r'$a$  heavy  ($m_a=3\,q_0$)'),
        ('a',  'light', '#2ca02c', '--', 1.5, r'$a$  light  ($m_a=0.3\,q_0$)'),
    ]
    for op, regime, col, ls, lw, lbl in cfg:
        key = f'Al2O3_{op}_{regime}'
        if key in R and '1meV' in R[key]:
            splot(ax, mx, R[key]['1meV'], color=col, ls=ls, lw=lw, label=lbl)
    fmt_ax(ax, r'$\bar\sigma$ [cm$^2$]',
           r'Al$_2$O$_3$: all SD operators,  $E_{\rm th}=1$ meV')
    ax.legend(fontsize=10.5, loc='best')
    fig.tight_layout()
    fig.savefig(f'{FIG_DIR}/all_operators_Al2O3.png', dpi=150, bbox_inches='tight')
    plt.close(); print('  ✓ all_operators_Al2O3.png')


# ── Response function C_ld(q,ω) ─────────────────────────────────────────────
def fig_response():
    import darkelf as de
    devnull = open(os.devnull,'w')
    old=sys.stdout; sys.stdout=devnull
    d = de.darkelf(target='Al2O3', mX=1e8, mMed=10e9,
                   v0kms=220, vekms=240, vesckms=500, eps_data_dir=DE_DATA)
    d.update_params(mX=1e8, mMed=10e9, SD_op="A'")
    sys.stdout=old; devnull.close()

    fig, axes = plt.subplots(1,2,figsize=(13,5))
    omegas = np.linspace(1e-3, 0.11, 250)
    q_list = [500, 2000, 5000, 10000]
    cols_q = ['#1f77b4','#ff7f0e','#2ca02c','#d62728']

    for d_idx in range(len(d.atoms)):
        ax = axes[d_idx]
        for qi, q_eV in enumerate(q_list):
            C = np.zeros(len(omegas))
            for j, om in enumerate(omegas):
                try:
                    c = d.C_ld(np.array([float(q_eV)]), om, d_idx)
                    C[j] = float(c[0]) if hasattr(c,'__len__') else float(c)
                except: pass
            ax.plot(omegas*1000, C, color=cols_q[qi], lw=1.3,
                    label=f'q = {q_eV/1000:.1f} keV')
        ax.set_xlabel(r'$\omega$ [meV]', fontsize=13)
        ax.set_ylabel(r'$C_{\ell,d}(q,\omega)$', fontsize=13)
        ax.set_title(f'{d.atoms[d_idx]} in Al₂O₃', fontsize=12)
        ax.legend(fontsize=9); ax.grid(True,alpha=0.25)

    fig.suptitle(r'Phonon correlation function $C_{\ell,d}(q,\omega)$  —  Al$_2$O$_3$',
                 fontsize=13, y=1.01)
    fig.tight_layout()
    fig.savefig(f'{FIG_DIR}/response_functions.png', dpi=150, bbox_inches='tight')
    plt.close(); print('  ✓ response_functions.png')


# ── Differential rate dR/dω ──────────────────────────────────────────────────
def fig_dR_domega():
    import darkelf as de
    devnull = open(os.devnull,'w')
    old=sys.stdout; sys.stdout=devnull
    d = de.darkelf(target='Al2O3', mX=1e8, mMed=10e9,
                   v0kms=220, vekms=240, vesckms=500, eps_data_dir=DE_DATA)
    sys.stdout=old; devnull.close()

    fig, ax = plt.subplots(figsize=(9,6))
    omegas = np.logspace(-3, np.log10(0.12), 120)
    sigman = 1e-38
    C_KMS = 2.99792458e5
    q0_val = 1e8 * 220 / C_KMS

    for op, col, lbl in [("A'", '#1f77b4', r"$A'$ heavy"),
                          ('phi','#ff7f0e', r'$\phi$ heavy'),
                          ('a',  '#2ca02c', r'$a$ heavy')]:
        mMed = 10e9 if op=="A'" else 3*q0_val
        d.update_params(mX=1e8, mMed=mMed, SD_op=op)
        dR = np.array([d._dR_domega_multiphonons_SD(om, sigman=sigman)
                       for om in omegas])
        m = dR > 0
        if m.sum() > 1:
            ax.loglog(omegas[m]*1000, dR[m], color=col, lw=2, label=lbl)

    ax.set_xlabel(r'$\omega$ [meV]', fontsize=13)
    ax.set_ylabel(r'$dR/d\omega$  [kg$^{-1}$yr$^{-1}$eV$^{-1}$]', fontsize=13)
    ax.set_title(r'Al$_2$O$_3$,  $m_\chi=100$ MeV,  $\bar\sigma=10^{-38}$ cm$^2$',
                 fontsize=12)
    ax.legend(fontsize=11); ax.grid(True,alpha=0.25,which='both')
    fig.tight_layout()
    fig.savefig(f'{FIG_DIR}/dR_domega.png', dpi=150, bbox_inches='tight')
    plt.close(); print('  ✓ dR_domega.png')


# ── Summary: σ vs mχ for "best-reach" thresholds, both targets side-by-side ──
def fig_summary(R):
    mx = R['mx_eV']/1e6
    fig, axes = plt.subplots(1,2,figsize=(15,6))
    ops_cfg = [
        ("A'", 'heavy', '#1f77b4', '-',  2.0, r"$A'$ heavy"),
        ('phi','heavy', '#ff7f0e', '-',  2.0, r'$\phi$ heavy'),
        ('phi','light', '#ff7f0e', '--', 1.5, r'$\phi$ light'),
        ('a',  'heavy', '#2ca02c', '-',  2.0, r'$a$ heavy'),
        ('a',  'light', '#2ca02c', '--', 1.5, r'$a$ light'),
    ]
    for ax, tgt in zip(axes, ['Al2O3','GaAs']):
        for op, regime, col, ls, lw, lbl in ops_cfg:
            key = f'{tgt}_{op}_{regime}'
            if key in R and '1meV' in R[key]:
                splot(ax, mx, R[key]['1meV'], color=col, ls=ls, lw=lw, label=lbl)
        tname = r'Al$_2$O$_3$' if tgt=='Al2O3' else tgt
        fmt_ax(ax, r'$\bar\sigma$ [cm$^2$]', f'{tname}  (best threshold = 1 meV)')
        ax.legend(fontsize=9.5, loc='best')
    fig.suptitle('Summary: detection reach for all SD operators  (3 events/kg·yr)',
                 fontsize=13, y=1.01)
    fig.tight_layout()
    fig.savefig(f'{FIG_DIR}/summary_all_operators.png', dpi=150, bbox_inches='tight')
    plt.close(); print('  ✓ summary_all_operators.png')


# ── main ─────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print('Loading results...')
    R = load()
    print('Generating figures...')
    fig5_phonon_dos()
    fig6_phi(R)
    fig7_a(R)
    fig8_Aprime(R)
    fig_sd_vs_si(R)
    fig_all_ops(R)
    fig_response()
    fig_dR_domega()
    fig_summary(R)
    print(f'\nAll figures written to {FIG_DIR}/')
