#!/usr/bin/env python
"""Plot outputs from NILC-PS-Model pipeline, analogous to paper Figs 1, 2, 3.

Reads pickles from outputs/ and generates figures in report/figs/.
"""
import os, pickle, sys
import numpy as np
import healpy as hp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = 'outputs'
FIG = 'report/figs'
os.makedirs(FIG, exist_ok=True)

# --- Fig 1 analog: component maps ---
try:
    import yaml
    cfg = yaml.safe_load(open('nilc_ps_config.yaml'))
    freqs = cfg['freqs']
    tsz_amp = cfg['tSZ_amp']
    nside = cfg['nside']
    ellmax = cfg['ellmax']
    noise = cfg['noise']
except Exception as e:
    print('cannot load yaml', e); sys.exit(1)

cmb = hp.read_map(cfg['cmb_map_file'])
cmb = hp.ud_grade(cmb, nside)
tsz = hp.read_map(cfg['tsz_map_file'])
tsz = tsz_amp * hp.ud_grade(tsz, nside)
freq1 = hp.read_map(f'{OUT}/maps/freq1.fits')
freq2 = hp.read_map(f'{OUT}/maps/freq2.fits')

fig = plt.figure(figsize=(12, 8))
hp.mollview(cmb, sub=221, title='CMB [K]', cmap='RdBu_r',
            min=-2.24e-4, max=2.65e-4)
hp.mollview(tsz, sub=222, title=f'Amplified Compton y ($\\times${int(tsz_amp)})',
            min=0, max=4e-3)
hp.mollview(freq1, sub=223, title=f'{freqs[0]:.0f} GHz total sky [K]',
            cmap='RdBu_r', min=-5e-3, max=3e-4)
hp.mollview(freq2, sub=224, title=f'{freqs[1]:.0f} GHz total sky [K]',
            cmap='RdBu_r', min=-5e-3, max=3e-4)
plt.suptitle('Paper Fig. 1 analog: Component + frequency maps')
fig.savefig(f'{FIG}/fig1_maps.png', dpi=130, bbox_inches='tight')
plt.close(fig)
print('Wrote fig1_maps.png')

# --- Fig 2 analog: component power spectra + needlet filters ---
from NILCPSModel_utils import GaussianNeedlets_stub
from math import pi

# Recompute component Cls
ellmax_s = cfg['ell_sum_max']
cmb_cl = hp.anafast(cmb, lmax=ellmax_s)
tsz_cl = hp.anafast(tsz, lmax=ellmax_s)
# tSZ spectral response
h_pl = 6.62607004e-34; kb = 1.38064852e-23; Tc = 2.726
def gtsz(nu):
    x = h_pl * (nu * 1e9) / (kb * Tc)
    return Tc * (x * 1.0 / np.tanh(x / 2) - 4)
g1, g2 = gtsz(freqs[0]), gtsz(freqs[1])
# Noise spectra
theta_fwhm = (1.4/60.) * (np.pi/180.0)
sigma = theta_fwhm / np.sqrt(8*np.log(2))
W = (noise/60.) * (np.pi/180.0)
ells = np.arange(ellmax_s + 1)
noise_cl = W**2 * np.exp(ells*(ells+1)*sigma**2) * 1e-12

# Needlet filters: Gaussian-differences following authors' convention
# h^(0) = gauss(FWHM1), h^(k)_k=1..N-2 = sqrt(gauss(FWHM_k+1)^2 - gauss(FWHM_k)^2),
# h^(N-1) = sqrt(1 - gauss(FWHM_N-1)^2); N=3 here, FWHMs = [1000, 800] arcmin
N_scales = cfg['Nscales']
GN = cfg['GN_FWHM_arcmin']
lmax_cl = ellmax_s
ells_f = np.arange(lmax_cl + 1)
gb = [hp.gauss_beam(np.deg2rad(f/60), lmax=lmax_cl) for f in GN]
h = np.zeros((N_scales, lmax_cl + 1))
h[0] = gb[0]
for k in range(1, N_scales - 1):
    h[k] = np.sqrt(np.maximum(gb[k]**2 - gb[k-1]**2, 0))
h[N_scales - 1] = np.sqrt(np.maximum(1 - gb[-1]**2, 0))

fig, axes = plt.subplots(2, 1, figsize=(7, 8))
ax = axes[0]
fac = ells * (ells + 1) / (2 * np.pi)
ax.plot(ells, fac * cmb_cl, label='CMB')
ax.plot(ells, fac * (g1**2) * tsz_cl, label=f'{freqs[0]:.0f} GHz: $g^2 C_\\ell^{{ftSZ}}$')
ax.plot(ells, fac * (g2**2) * tsz_cl, label=f'{freqs[1]:.0f} GHz: $g^2 C_\\ell^{{ftSZ}}$')
ax.plot(ells, fac * noise_cl, label=f'Noise ({noise:.0f} $\\mu$K·arcmin)')
ax.set_yscale('log')
ax.set_xlabel('$\\ell$'); ax.set_ylabel('$\\ell(\\ell+1) C_\\ell / 2\\pi$ [K$^2$]')
ax.set_title('Component power spectra (at nside=%d, $\\ell_{\\max}$=%d)' % (nside, ellmax_s))
ax.legend(fontsize=9); ax.grid(alpha=0.3)

ax = axes[1]
for k in range(N_scales):
    ax.plot(ells_f, h[k], label=f'scale {k}')
ax.plot(ells_f, np.sqrt((h**2).sum(0)), 'k--', lw=0.8, label=r'$\sqrt{\sum h_k^2}$')
ax.set_xlabel('$\\ell$'); ax.set_ylabel('$h^{(n)}(\\ell)$')
ax.set_title('Needlet filters (Gaussian differences, FWHM=%s arcmin)' % GN)
ax.legend(fontsize=9); ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(f'{FIG}/fig2_cls_needlets.png', dpi=130)
plt.close(fig)
print('Wrote fig2_cls_needlets.png')

# --- Fig 3 analog: analytic vs directly computed NILC power spectra ---
try:
    Clpq = pickle.load(open(f'{OUT}/data_vecs/Clpq.p', 'rb'))          # [p,q,z,term,ell]
    Clpq_direct = pickle.load(open(f'{OUT}/data_vecs/Clpq_direct.p', 'rb'))  # [p,q,ell]
    direct_prop = pickle.load(open(f'{OUT}/data_vecs/directly_computed_prop_to_NILC_PS.p', 'rb'))
except FileNotFoundError as e:
    print('Data vectors not found yet:', e)
    sys.exit(0)

ell_plot = np.arange(ellmax + 1)
fac = ell_plot * (ell_plot + 1) / (2 * np.pi)
# Four panels: z=CMB->p=CMB, z=CMB->p=tSZ, z=ftSZ->p=CMB, z=ftSZ->p=tSZ
# analytic: sum over 4 reMASTERed terms of Clpq[p,q,z,:,:]
labels_pq = [('CMB', 'CMB'), ('CMB', 'tSZ'), ('tSZ', 'CMB'), ('tSZ', 'tSZ')]
panel_map = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1)]
# indexes: Clpq[p,q,z,term,l], p/q in {0:CMB,1:tSZ}, z in {0:CMB,1:tSZ}
fig, axes = plt.subplots(2, 2, figsize=(12, 9))
pairs = [  # (z, p, q, title)
    (0, 0, 0, 'CMB $\\to$ CMB-NILC'),
    (1, 0, 0, 'ftSZ $\\to$ CMB-NILC'),
    (0, 1, 1, 'CMB $\\to$ tSZ-NILC'),
    (1, 1, 1, 'ftSZ $\\to$ tSZ-NILC'),
]
for ax, (z, p, q, ttl) in zip(axes.flat, pairs):
    analytic_tot = np.sum(Clpq[p, q, z], axis=0)  # sum over terms
    direct = direct_prop[z, p] if p == q else np.zeros(ellmax + 1)
    ax.plot(ell_plot, fac * analytic_tot, 'o-', label='Analytic (Eq. 26 sum)')
    ax.plot(ell_plot, fac * direct, 's--', alpha=0.7, label='Directly computed')
    # Individual terms
    term_names = [r'$\langle zz\rangle\langle ww\rangle$',
                  r'$\langle zw\rangle\langle zw\rangle$ etc',
                  r'$\langle w\rangle\langle zzw\rangle_c$',
                  r'$\langle z\rangle\langle wzw\rangle_c$',
                  r'$\langle zzww\rangle_c$']
    # Clpq has 4 terms but paper lists 5; adjust
    n_terms = Clpq.shape[3]
    cmap = plt.get_cmap('tab10')
    for t in range(n_terms):
        ax.plot(ell_plot, fac * Clpq[p, q, z, t], ':', color=cmap(2+t), alpha=0.6,
                label=f'term {t}', lw=1)
    ax.set_xlabel('$\\ell$'); ax.set_ylabel('$\\ell(\\ell+1) C_\\ell/2\\pi$ [K$^2$]')
    ax.set_title(ttl)
    ax.legend(fontsize=7)
    ax.grid(alpha=0.3)
plt.suptitle('Paper Fig. 3 analog: Analytic NILC $C_\\ell$ (Eq. 26) vs simulation')
fig.tight_layout()
fig.savefig(f'{FIG}/fig3_analytic_vs_direct.png', dpi=130)
plt.close(fig)
print('Wrote fig3_analytic_vs_direct.png')

# NILC total power spectra from pyilc direct
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(ell_plot, fac * Clpq_direct[0, 0], 'o-', label='Direct: $C_\\ell^{CMB,CMB}$ NILC')
ax.plot(ell_plot, fac * Clpq_direct[1, 1], 's-', label='Direct: $C_\\ell^{tSZ,tSZ}$ NILC')
ax.plot(ell_plot, fac * Clpq_direct[0, 1], '^-', label='Direct: $C_\\ell^{CMB,tSZ}$ NILC cross')
ax.set_xlabel('$\\ell$'); ax.set_ylabel('$\\ell(\\ell+1) C_\\ell/2\\pi$ [K$^2$]')
ax.set_yscale('symlog', linthresh=1e-15)
ax.legend(); ax.grid(alpha=0.3)
ax.set_title('Directly computed NILC auto/cross Cls')
fig.tight_layout()
fig.savefig(f'{FIG}/fig3_nilc_total.png', dpi=130)
plt.close(fig)
print('Wrote fig3_nilc_total.png')

# Residual fractional difference
fig, axes = plt.subplots(1, 4, figsize=(16, 4), sharey=True)
for ax, (z, p, q, ttl) in zip(axes, pairs):
    analytic_tot = np.sum(Clpq[p, q, z], axis=0)
    direct = direct_prop[z, p]
    # Skip ell=0 and 1 (mean-subtracted monopole/dipole: near-zero power, 
    # fractional residual cosmetically huge but absolute diff is ~1e-30)
    mask = ell_plot >= 2
    denom = np.where(np.abs(direct) > 1e-30, direct, np.nan)
    resid = (analytic_tot - direct) / denom
    ax.plot(ell_plot[mask], resid[mask], 'o-')
    ax.axhline(0, color='k', lw=0.5)
    ax.set_ylim(-0.01, 0.03)
    ax.set_xlabel('$\\ell$'); ax.set_title(ttl); ax.grid(alpha=0.3)
axes[0].set_ylabel('(analytic $-$ direct) / direct')
fig.suptitle('Analytic vs direct fractional residual (ell>=2; paper target: <1%)')
fig.tight_layout()
fig.savefig(f'{FIG}/fig3_residual.png', dpi=130)
plt.close(fig)
print('Wrote fig3_residual.png')
print('Done.')
