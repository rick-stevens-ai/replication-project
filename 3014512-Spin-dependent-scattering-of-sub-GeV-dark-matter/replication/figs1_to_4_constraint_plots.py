"""
figs1_to_4_constraint_plots.py
------------------------------
Replication of the analytical / phenomenological constraint figures
(Figs. 1-4) of Gori, Knapen, Lin, Munbodh, Suter,
"Spin-Dependent Scattering of Sub-GeV Dark Matter",
Phys. Rev. D 112, 075019 (2025); OSTI 3014512.

These are pure analytical / phenomenological constraint plots --- no
DarkELF rate computation is required. The formulas are taken directly
from the paper's text and the references it cites:

  Fig. 1  -- Spin-0 mediator (phi or a) constraints in the (m_med, g_p) and
             (m_med, g_n) planes:
              * SN1987A cooling+trapping band (Refs. [50,51], paper text)
              * HB star cooling
              * Rare-meson / flavor (B->K+inv, K->pi+inv mapped via c_GG)
              * CHARM and E137 beam-dump envelopes (Refs. [46-48])
              * BBN/Neff red dashed line at 70 MeV decoupling
              * KSVZ-completion bound from Eq. (29)

  Fig. 2  -- SIDM contour for the upper bound on g_chi in the
             (m_chi, m_med) plane for spin-0 mediators, using the
             paper's Eqs. (30)-(37): viscosity cross section in the Born
             limit (small-R limits used analytically).

  Fig. 3  -- SIDM upper bound on g_chi vs m_chi for the two direct-
             detection benchmarks m_med = 0.3 m_chi v_0 (light) and
             m_med = 3 m_chi v_0 (heavy), for both phi and a mediators.

  Fig. 4  -- Axial-vector A' (called A_0 in paper) constraints in the
             (m_A', g_0) plane:
              * LHC anomalon bound  g_0 < m_A'/(sqrt(2) TeV)  [Eq. (43)]
              * BABAR  B -> K + invisible  [Eq. (48)]
              * NA62   K -> pi + invisible  [Eq. (47)]
              * SN1987A axial-vector emission band

Where a constraint comes from external reanalyses (CHARM/E137/HB/SN
fitting formulas in Ref. [50] Eq. (11)), we use the published
parametrizations or piecewise envelopes consistent with the paper's
plotted regions.  The goal is to reproduce the qualitative geometry of
Figs. 1-4 -- not to digitize them pixel-perfect; that requires
WebPlotDigitizer on the PDF and the underlying experimental data files
which are not redistributed by the authors.

Outputs:
  fig1_phi_constraints.png
  fig2_sidm_contour.png
  fig3_sidm_gchi_vs_mchi.png
  fig4_Aprime_constraints.png
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import os

# ----------------------- constants -----------------------
HBAR_C_GEV_CM = 1.973e-14         # GeV * cm
GEV_PER_GRAM  = 5.6096e23         # 1 g = 5.6e23 GeV/c^2
CM2_PER_GEV_M2 = HBAR_C_GEV_CM**2 # cm^2 per 1/GeV^2  (cm^2 * GeV^2)
V0      = 220.0 / 2.998e5         # ~7.34e-4
V_SIDM  = 0.005                   # galaxy-group velocity ~ 0.005 c
SIDM_LIM_CM2_G = 1.1              # sigma/m bound [cm^2/g]

OUTDIR = os.path.dirname(os.path.abspath(__file__))


# =====================================================================
# Helper: SIDM viscosity cross section limits
# =====================================================================
def sigma_phi_V_smallR(g_chi, m_chi_GeV, m_phi_GeV):
    """phi mediator, Born+small-R limit: sigma_V ~ g_chi^4 m_chi^2 / (12 pi m_phi^4).
    Returns sigma in cm^2."""
    sig_GeV2 = g_chi**4 * m_chi_GeV**2 / (12.0 * np.pi * m_phi_GeV**4)
    return sig_GeV2 * CM2_PER_GEV_M2

def sigma_a_V_smallR(g_chi, m_chi_GeV, m_a_GeV, v=V_SIDM):
    """axial (pseudoscalar) mediator a, small-R: sigma_V ~ g_chi^4 m_chi^2 v^4 /(240 pi m_a^4)."""
    sig_GeV2 = g_chi**4 * m_chi_GeV**2 * v**4 / (240.0 * np.pi * m_a_GeV**4)
    return sig_GeV2 * CM2_PER_GEV_M2

def sigma_over_m_phi(g_chi, m_chi_GeV, m_phi_GeV, v=V_SIDM):
    """Returns (sigma_V/m_chi) in cm^2/g for phi mediator (small-R/Born)."""
    sig_cm2 = sigma_phi_V_smallR(g_chi, m_chi_GeV, m_phi_GeV)
    m_g = m_chi_GeV / GEV_PER_GRAM        # m_chi in grams
    return sig_cm2 / m_g

def sigma_over_m_a(g_chi, m_chi_GeV, m_a_GeV, v=V_SIDM):
    sig_cm2 = sigma_a_V_smallR(g_chi, m_chi_GeV, m_a_GeV, v)
    m_g = m_chi_GeV / GEV_PER_GRAM
    return sig_cm2 / m_g

def gchi_max_phi(m_chi_GeV, m_phi_GeV, v=V_SIDM, lim=SIDM_LIM_CM2_G):
    """Solve sigma/m = lim for g_chi^4 = lim * 12 pi m_phi^4 / (m_chi^2 * cm2/GeV^-2 / (m_chi/GeV_per_g))."""
    # sigma/m_chi [cm^2/g] = (g_chi^4 m_chi^2 / (12 pi m_phi^4)) * cm2_per_GeV_m2 * (GeV_per_g / m_chi_GeV)
    coeff = m_chi_GeV * CM2_PER_GEV_M2 * GEV_PER_GRAM / (12.0 * np.pi * m_phi_GeV**4)
    g4 = lim / coeff
    return np.where(g4 > 0, g4**0.25, np.nan)

def gchi_max_a(m_chi_GeV, m_a_GeV, v=V_SIDM, lim=SIDM_LIM_CM2_G):
    coeff = m_chi_GeV * v**4 * CM2_PER_GEV_M2 * GEV_PER_GRAM / (240.0 * np.pi * m_a_GeV**4)
    g4 = lim / coeff
    return np.where(g4 > 0, g4**0.25, np.nan)


# =====================================================================
# Fig 1: Spin-0 mediator constraints in (m_med, g_p) plane
# =====================================================================
def fig1():
    """Reproduce Fig. 1 of the paper (left panel: g_p vs m_phi).

    Constraint shapes (analytical envelopes; numerical levels from paper
    text and cited fitting formulas):
      - HB stars:          excluded for m_med < ~0.5 MeV at g_p > ~1e-9
      - SN1987A:           cooling excludes g_p < ~2e-6 ; trapping
                           re-allows g_p > ~7e-6 .  Window 100keV-100MeV
      - Meson/flavor:      grey band at large m_med from rare meson decays
      - CHARM/E137:        beam-dump exclusions in 100 MeV - 1 GeV
      - BBN red lines:     g_p contour for tau ~ 1 s and ~1e4 s decays
      - KSVZ ceiling:      |g_p| < 2e-2  (Eq. 29)
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # mass range: 1 keV to 10 GeV
    mmed = np.logspace(-6, 1, 600)  # GeV

    # ---------------- LEFT: g_p vs m_med ----------------
    ax = axes[0]

    # SN1987A cooling lower edge (excluded BELOW this for m_med in window)
    sn_low_gp  = 2e-6
    sn_high_gp = 7e-6
    sn_mlow, sn_mhigh = 1e-4, 1e-1   # 100 keV to 100 MeV
    msn = np.logspace(np.log10(sn_mlow), np.log10(sn_mhigh), 100)
    # cooling-excluded band (yellow): below sn_low
    ax.fill_between(msn, sn_low_gp*np.ones_like(msn), sn_high_gp*np.ones_like(msn),
                    color='gold', alpha=0.6, label='SN1987A')

    # HB stars: excludes g_p > ~1e-9 (axion-photon mapped) for m_med < 0.5 MeV
    hb_m = np.logspace(-6, np.log10(5e-4), 100)
    ax.fill_between(hb_m, 1e-9, 1.0, color='steelblue', alpha=0.4, label='HB stars')

    # Meson / flavor (rare meson decays). c_GG <~ 20 -> |g_p| < 2e-2
    # Mapping is mass-dependent; envelope shown for m_med > ~3 MeV
    meson_m = np.logspace(np.log10(3e-3), 1, 200)
    # Below the line (0.5 -- 5 GeV) constraint deepens; above relaxes
    meson_top = 1.0
    meson_bot = np.where(meson_m < 5.0, 2e-4 * (meson_m/0.5)**0.5, 2e-2)
    meson_bot = np.minimum(meson_bot, 2e-2)
    ax.fill_between(meson_m, meson_bot, meson_top, color='gray', alpha=0.35,
                    label='Rare meson decays')

    # CHARM beam dump: 100 MeV < m < 1 GeV ; excludes 1e-6 < g_p < 1e-4 (envelope)
    charm_m = np.logspace(-1, 0, 100)
    charm_lo = 1e-6 * np.ones_like(charm_m)
    charm_hi = 1e-4 * np.ones_like(charm_m)
    ax.fill_between(charm_m, charm_lo, charm_hi, color='seagreen', alpha=0.45,
                    label='CHARM')

    # E137 electron beam dump: similar but slightly weaker, 30 MeV - 500 MeV
    e137_m = np.logspace(np.log10(3e-2), np.log10(0.5), 100)
    e137_lo = 5e-7 * np.ones_like(e137_m)
    e137_hi = 5e-5 * np.ones_like(e137_m)
    ax.fill_between(e137_m, e137_lo, e137_hi, color='purple', alpha=0.35,
                    label='E137')

    # KSVZ ceiling
    ax.axhline(2e-2, color='cyan', ls='--', lw=1.5,
               label=r'KSVZ: $|g_p|<2\times10^{-2}$ (Eq. 29)')

    # BBN: tau ~ 1 s and ~1e4 s lines (decreasing in g_p with m_med^something)
    # Sloped dashed red lines schematic: tau ~ 1/(g_p^2 m_med)
    mbbn = np.logspace(-4, -1, 50)
    ax.plot(mbbn, 1e-4 * (1e-3/mbbn)**0.5, ls='--', color='red', lw=1,
            label=r'$\tau_{a\to\gamma\gamma}\sim 10^4$s')
    ax.plot(mbbn, 5e-3 * (1e-3/mbbn)**0.5, ls='--', color='red', lw=1, alpha=0.7,
            label=r'$\tau_{a\to\gamma\gamma}\sim 1$s')

    # Decoupling/Neff line
    ax.axhline(1.5e-7, color='red', ls=':', lw=1.5,
               label=r'$\Delta N_{eff}>0.36$ (T=70 MeV decoupling)')

    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_xlim(1e-6, 1e1); ax.set_ylim(1e-9, 1e0)
    ax.set_xlabel(r'$m_{\phi,a}$ [GeV]')
    ax.set_ylabel(r'$|g_p|$')
    ax.set_title('Fig. 1 (left): spin-0 mediator, proton coupling')
    ax.grid(True, which='both', alpha=0.2)
    ax.legend(loc='upper left', fontsize=7, ncol=1)

    # ---------------- RIGHT: g_n vs m_med (suppressed by ~3.5e-5/8.11e-4 = 0.043) ----------------
    ax = axes[1]
    suppr = 3.50e-5 / 8.11e-4  # ~0.043

    ax.fill_between(msn, sn_low_gp*suppr, sn_high_gp*suppr,
                    color='gold', alpha=0.6, label='SN1987A')
    ax.fill_between(hb_m, 1e-9*suppr, 1.0*suppr, color='steelblue', alpha=0.4,
                    label='HB stars')
    ax.fill_between(meson_m, meson_bot*suppr, meson_top*suppr, color='gray', alpha=0.35,
                    label='Rare meson decays')
    ax.fill_between(charm_m, charm_lo*suppr, charm_hi*suppr, color='seagreen', alpha=0.45,
                    label='CHARM')
    ax.fill_between(e137_m, e137_lo*suppr, e137_hi*suppr, color='purple', alpha=0.35,
                    label='E137')
    ax.axhline(7e-4, color='cyan', ls='--', lw=1.5,
               label=r'KSVZ: $|g_n|<7\times10^{-4}$ (Eq. 29)')
    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_xlim(1e-6, 1e1); ax.set_ylim(1e-11, 1e-1)
    ax.set_xlabel(r'$m_{\phi,a}$ [GeV]')
    ax.set_ylabel(r'$|g_n|$')
    ax.set_title('Fig. 1 (right): spin-0 mediator, neutron coupling')
    ax.grid(True, which='both', alpha=0.2)
    ax.legend(loc='upper left', fontsize=7)

    fig.suptitle('Fig. 1: Spin-0 mediator constraints (replication)', y=1.01)
    fig.tight_layout()
    out = os.path.join(OUTDIR, 'fig1_phi_constraints.png')
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  wrote {out}')


# =====================================================================
# Fig 2: SIDM g_chi contour in (m_chi, m_med) plane
# =====================================================================
def fig2():
    """Reproduce Fig. 2: g_chi upper-bound contours in (m_chi, m_med)."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=False)

    m_chi = np.logspace(-3, 0, 200)        # GeV  (1 MeV - 1 GeV)
    m_med = np.logspace(-7, -1, 200)       # GeV  (1 keV - 100 MeV)

    M, Mm = np.meshgrid(m_chi, m_med, indexing='xy')

    # phi
    G_phi = gchi_max_phi(M, Mm)
    G_phi = np.clip(G_phi, 1e-3, 10.0)

    ax = axes[0]
    levels = [1e-2, 1e-1, 0.3, 1.0, 3.0]
    cf = ax.contourf(M, Mm, np.log10(G_phi), levels=np.log10(levels),
                     cmap='viridis_r', extend='both')
    cb = plt.colorbar(cf, ax=ax)
    cb.set_label(r'$\log_{10} g_\chi^{max}$ (SIDM)')
    cs = ax.contour(M, Mm, G_phi, levels=[0.1, 0.3, 1.0],
                    colors='white', linewidths=1.0)
    ax.clabel(cs, fmt='%.2f', fontsize=8)
    # benchmark lines
    ax.plot(m_chi, 0.3 * m_chi * V0, 'k--', lw=1.5, label=r'$m_{med}=0.3 m_\chi v_0$ (light)')
    ax.plot(m_chi, 3.0 * m_chi * V0, 'k-.', lw=1.5, label=r'$m_{med}=3 m_\chi v_0$ (heavy)')
    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_xlabel(r'$m_\chi$ [GeV]'); ax.set_ylabel(r'$m_\phi$ [GeV]')
    ax.set_title(r'$\phi$ mediator: SIDM bound on $g_\chi$')
    ax.legend(loc='upper left', fontsize=8)

    # a
    G_a = gchi_max_a(M, Mm)
    G_a = np.clip(G_a, 1e-2, 10.0)
    ax = axes[1]
    cf = ax.contourf(M, Mm, np.log10(G_a),
                     levels=np.linspace(-2, 1, 12), cmap='viridis_r', extend='both')
    cb = plt.colorbar(cf, ax=ax)
    cb.set_label(r'$\log_{10} g_\chi^{max}$ (SIDM)')
    cs = ax.contour(M, Mm, G_a, levels=[0.1, 0.3, 1.0, 3.0],
                    colors='white', linewidths=1.0)
    ax.clabel(cs, fmt='%.2f', fontsize=8)
    ax.plot(m_chi, 0.3 * m_chi * V0, 'k--', lw=1.5, label=r'$m_{med}=0.3 m_\chi v_0$ (light)')
    ax.plot(m_chi, 3.0 * m_chi * V0, 'k-.', lw=1.5, label=r'$m_{med}=3 m_\chi v_0$ (heavy)')
    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_xlabel(r'$m_\chi$ [GeV]'); ax.set_ylabel(r'$m_a$ [GeV]')
    ax.set_title(r'$a$ mediator: SIDM bound on $g_\chi$')
    ax.legend(loc='upper left', fontsize=8)

    fig.suptitle('Fig. 2: SIDM upper bound on $g_\\chi$ (Eqs. 30-37, Born small-R)', y=1.01)
    fig.tight_layout()
    out = os.path.join(OUTDIR, 'fig2_sidm_contour.png')
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  wrote {out}')


# =====================================================================
# Fig 3: SIDM g_chi vs m_chi at the two benchmark mediator masses
# =====================================================================
def fig3():
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    m_chi = np.logspace(-3, 0, 300)  # GeV

    # benchmark mediator masses
    m_light = 0.3 * m_chi * V0
    m_heavy = 3.0 * m_chi * V0

    g_phi_light = gchi_max_phi(m_chi, m_light)
    g_phi_heavy = gchi_max_phi(m_chi, m_heavy)
    g_a_light   = gchi_max_a(m_chi, m_light)
    g_a_heavy   = gchi_max_a(m_chi, m_heavy)

    ax.plot(m_chi, g_phi_light, 'b-',  label=r'$\phi$ light ($m_\phi=0.3 m_\chi v_0$)')
    ax.plot(m_chi, g_phi_heavy, 'b--', label=r'$\phi$ heavy ($m_\phi=3 m_\chi v_0$)')
    ax.plot(m_chi, g_a_light,   'r-',  label=r'$a$ light ($m_a=0.3 m_\chi v_0$)')
    ax.plot(m_chi, g_a_heavy,   'r--', label=r'$a$ heavy ($m_a=3 m_\chi v_0$)')

    # perturbativity / unitarity ceiling
    ax.axhline(np.sqrt(4*np.pi), color='k', ls=':', lw=1, label=r'$g_\chi=\sqrt{4\pi}$')
    ax.axhline(1.0, color='gray', ls=':', lw=1, alpha=0.6)

    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_xlim(1e-3, 1e0); ax.set_ylim(1e-3, 10.0)
    ax.set_xlabel(r'$m_\chi$ [GeV]')
    ax.set_ylabel(r'$g_\chi^{max}$ from SIDM')
    ax.set_title('Fig. 3: SIDM upper bound on $g_\\chi$ at direct-detection benchmarks')
    ax.grid(True, which='both', alpha=0.25)
    ax.legend(loc='best', fontsize=9)

    out = os.path.join(OUTDIR, 'fig3_sidm_gchi_vs_mchi.png')
    fig.tight_layout()
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  wrote {out}')


# =====================================================================
# Fig 4: Axial-vector A' constraints in (m_A', g_0)
# =====================================================================
def fig4():
    """Reproduce Fig. 4: axial-vector A' (=A_0) constraints.

    Constraints:
      - LHC anomalons:    g_0 < (1/sqrt(2)) m_A0/TeV   [Eq. 43]
      - BABAR  Br[B->K X]  < 4.1e-5  with Br formula Eq. (48)
      - NA62   Br[K->pi X] < 1.85e-10 with Br formula Eq. (47)
      - SN1987A axial-vector emission window
    """
    fig, ax = plt.subplots(1, 1, figsize=(9, 6))
    m_A = np.logspace(-3, 1.3, 600)  # GeV  (1 MeV - 20 GeV)

    # --- LHC anomalon (Eq. 43): excluded for g_0 > m_A/(sqrt(2) TeV) ---
    g0_lhc = m_A / (np.sqrt(2) * 1000.0)  # TeV = 1000 GeV
    ax.fill_between(m_A, g0_lhc, 1.0, color='lightcoral', alpha=0.5,
                    label=r'LHC anomalons (Eq. 43)')

    # --- NA62 K->pi+inv ---
    # Br[K+ -> pi+ A0] = 8.9e-7 * (g0/1e-8)^2 * (1 MeV/m_X)^2 * sqrt(...)
    # m_X is the additional state mass parameter; use m_X = m_A0 (paper benchmark)
    # Constraint: Br < 1.85e-10  (NA62 K+ -> pi+ nu nu measurement)
    # Solve for g0:  (g0/1e-8)^2 < 1.85e-10/(8.9e-7 * (1e-3/m_A)^2 * KIN)
    m_K, m_pi, m_B = 0.4937, 0.1396, 5.279
    KIN_K = np.where(m_A < (m_K - m_pi),
                     np.sqrt(np.clip((1 - m_pi**2/m_K**2 - m_A**2/m_K**2)**2
                                     - 4*m_pi**2*m_A**2/m_K**4, 0, None)),
                     0.0)
    Br_K_lim = 1.85e-10
    g0_na62_sq = (Br_K_lim / 8.9e-7) * (m_A/1e-3)**2 / np.where(KIN_K>0, KIN_K, np.nan)
    g0_na62 = 1e-8 * np.sqrt(np.clip(g0_na62_sq, 0, None))
    valid = (m_A < (m_K - m_pi)) & np.isfinite(g0_na62)
    ax.fill_between(m_A[valid], g0_na62[valid], 1.0,
                    color='dodgerblue', alpha=0.45,
                    label=r'NA62: $K\to\pi+\mathrm{inv}$ (Eq. 47)')

    # --- BABAR B -> K + invisible ---
    # Br[B+ -> K+ A0] = 2.2e-3 * (g0/1e-8)^2 * (1MeV/m_A0)^2 * F_K^2 * KIN
    # F_K^2(m_A) = 0.33*(1 - m_A^2/22 GeV^2)
    KIN_B = np.where(m_A < (m_B - m_K),
                     np.sqrt(np.clip((1 - m_K**2/m_B**2 - m_A**2/m_B**2)**2
                                     - 4*m_K**2*m_A**2/m_B**4, 0, None)),
                     0.0)
    F_K2 = np.maximum(0.33*(1 - m_A**2/22.0), 1e-3)
    Br_B_lim = 4.1e-5  # BABAR upper limit on Br[B+ -> K+ nu nu]
    g0_babar_sq = (Br_B_lim / 2.2e-3) * (m_A/1e-3)**2 / np.where(
        (KIN_B*F_K2)>0, KIN_B*F_K2, np.nan)
    g0_babar = 1e-8 * np.sqrt(np.clip(g0_babar_sq, 0, None))
    validB = (m_A < (m_B - m_K)) & np.isfinite(g0_babar)
    ax.fill_between(m_A[validB], g0_babar[validB], 1.0,
                    color='mediumseagreen', alpha=0.45,
                    label=r'BABAR: $B\to K+\mathrm{inv}$ (Eq. 48)')

    # --- SN1987A axial-vector cooling/trapping (schematic envelope) ---
    sn_m = np.logspace(-4, np.log10(0.2), 100)
    sn_lo = 1e-9 * np.ones_like(sn_m)
    sn_hi = 1e-7 * np.ones_like(sn_m)
    ax.fill_between(sn_m, sn_lo, sn_hi, color='gold', alpha=0.55,
                    label='SN1987A (axial vector)')

    # Benchmark: m_A0 = 10 GeV, g_0 ~ 7e-3 (max allowed by anomalon bound)
    ax.plot(10.0, 7e-3, '*', color='black', ms=18, label=r'Benchmark ($m_{A_0}=10$ GeV)')

    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_xlim(1e-3, 2e1); ax.set_ylim(1e-10, 1e0)
    ax.set_xlabel(r"$m_{A'}$ [GeV]")
    ax.set_ylabel(r'$g_0$')
    ax.set_title("Fig. 4: Axial-vector $A'$ mediator constraints")
    ax.grid(True, which='both', alpha=0.25)
    ax.legend(loc='lower right', fontsize=9)

    out = os.path.join(OUTDIR, 'fig4_Aprime_constraints.png')
    fig.tight_layout()
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  wrote {out}')


if __name__ == '__main__':
    print('Generating Figs 1-4 (analytical/phenomenological constraint plots)')
    fig1()
    fig2()
    fig3()
    fig4()
    print('Done.')
