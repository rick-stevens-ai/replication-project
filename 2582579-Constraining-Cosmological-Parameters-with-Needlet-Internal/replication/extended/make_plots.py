#!/usr/bin/env python
"""Diagnostic plots for NILC replication."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import healpy as hp
from src import config as cfg

os.makedirs('figures', exist_ok=True)

sim = np.load('data/sim.npz')
res = np.load('data/nilc_result.npz')

# 1. Needlet bank
fig, ax = plt.subplots(figsize=(7, 4))
bank = res['bank']
ell = np.arange(bank.shape[1])
for k in range(bank.shape[0]):
    ax.plot(ell, bank[k], label=f'scale {k}')
ax.plot(ell, np.sqrt((bank**2).sum(axis=0)), 'k--', lw=1, label=r'$\sqrt{\sum h_k^2}$')
ax.set_xlabel(r'$\ell$')
ax.set_ylabel(r'$h_k(\ell)$')
ax.set_title('Cosine-squared needlet bank')
ax.legend(fontsize=8, ncol=2)
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig('figures/needlet_bank.png', dpi=130)
plt.close(fig)

# 2. Input component maps
fig, axes = plt.subplots(2, 3, figsize=(12, 7))
mm = [sim['cmb_map'], sim['dust_template'], sim['sync_template'],
      sim['maps'][0], sim['maps'][3], sim['maps'][-1]]
titles = ['CMB', 'Dust (353 GHz template)', 'Sync (30 GHz template)',
          f'Freq {cfg.FREQS[0]:.0f} GHz',
          f'Freq {cfg.FREQS[3]:.0f} GHz',
          f'Freq {cfg.FREQS[-1]:.0f} GHz']
for ax, m, t in zip(axes.flat, mm, titles):
    plt.sca(ax)
    hp.mollview(m, title=t, hold=True, cmap='RdBu_r',
                min=np.percentile(m, 1), max=np.percentile(m, 99))
fig.tight_layout()
fig.savefig('figures/input_maps.png', dpi=120)
plt.close(fig)

# 3. NILC recovered CMB vs true
fig, axes = plt.subplots(1, 3, figsize=(14, 4))
for ax, m, t in zip(axes,
                    [sim['cmb_map'], res['cmb_nilc'], res['cmb_nilc'] - sim['cmb_map']],
                    ['True CMB (input)', 'NILC-recovered', 'Residual']):
    plt.sca(ax)
    rng = np.percentile(np.abs(m), 98)
    hp.mollview(m, title=t, hold=True, cmap='RdBu_r', min=-rng, max=rng)
fig.tight_layout()
fig.savefig('figures/cmb_recovery_maps.png', dpi=120)
plt.close(fig)

# 4. Power-spectrum comparison
cl_theory = res['cl_theory']
cl_real = res['cl_cmb_real']
cl_nilc = res['cl_nilc']
L = min(len(cl_theory), len(cl_real), len(cl_nilc))
cl_theory = cl_theory[:L]
cl_real = cl_real[:L]
cl_nilc = cl_nilc[:L]
ell = np.arange(L)
fac = ell * (ell + 1) / (2 * np.pi)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8), sharex=True,
                                gridspec_kw=dict(height_ratios=[3, 1]))
ax1.plot(ell, fac * cl_theory, 'k-', label='CAMB theory (fiducial)')
ax1.plot(ell, fac * cl_real, color='C0', alpha=0.6, label='Input CMB realization')
ax1.plot(ell, fac * cl_nilc, color='C3', label='NILC-recovered')
ax1.set_ylabel(r'$\ell(\ell+1)C_\ell/(2\pi)$  [$\mu K^2$]')
ax1.set_xlim(2, cfg.LMAX)
ax1.set_yscale('log')
ax1.legend()
ax1.grid(alpha=0.3)
ax1.set_title('CMB TT power spectrum recovery')
# Binned fractional bias
bin_edges = np.linspace(2, cfg.LMAX, 25).astype(int)
bin_centers, bias = [], []
for lo, hi in zip(bin_edges[:-1], bin_edges[1:]):
    bc = 0.5 * (lo + hi)
    w = np.arange(lo, hi)
    if len(w) > 0:
        ratio = np.mean((cl_nilc[w] - cl_real[w]) / np.maximum(cl_real[w], 1e-30))
        bin_centers.append(bc)
        bias.append(ratio)
ax2.axhline(0, color='k', lw=0.5)
ax2.plot(bin_centers, bias, 'o-', color='C3')
ax2.set_xlabel(r'$\ell$')
ax2.set_ylabel(r'$(C_\ell^{\rm NILC}-C_\ell^{\rm true})/C_\ell^{\rm true}$')
ax2.set_ylim(-0.5, 0.5)
ax2.grid(alpha=0.3)
fig.tight_layout()
fig.savefig('figures/cl_recovery.png', dpi=130)
plt.close(fig)

# 5. Foreground SEDs
from src import foregrounds as fg
fig, ax = plt.subplots(figsize=(7, 4))
nus = np.linspace(20, 400, 400)
ax.plot(nus, np.abs([fg.dust_sed_cmb(n, 353.0) for n in nus]), label='Dust (norm at 353 GHz)')
ax.plot(nus, np.abs([fg.sync_sed_cmb(n, 30.0) for n in nus]), label='Synchrotron (norm at 30 GHz)')
ax.axhline(1, color='k', lw=0.5, ls='--', label='CMB')
for f in cfg.FREQS:
    ax.axvline(f, color='gray', lw=0.4, alpha=0.5)
ax.set_xlabel('Frequency [GHz]')
ax.set_ylabel('SED amplitude in $\\mu K_{CMB}$ units')
ax.set_yscale('log')
ax.set_xscale('log')
ax.legend()
ax.grid(alpha=0.3, which='both')
ax.set_title('Component SEDs (thermodynamic CMB units)')
fig.tight_layout()
fig.savefig('figures/seds.png', dpi=130)
plt.close(fig)

print('Figures saved to figures/')
