#!/usr/bin/env python
"""MCMC on NILC-recovered CMB power spectrum.

Fit 3 LCDM parameters: As, ns, H0. Fix others to fiducial (ombh2, omch2, tau).
Gaussian likelihood on binned Cl with cosmic variance + diagonal noise term.
"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import camb
import emcee
import corner
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src import config as cfg

# Load NILC spectra
res = np.load('data/nilc_result.npz')
sim = np.load('data/sim.npz')
cl_nilc = res['cl_nilc']
cl_real = res['cl_cmb_real']
LMAX_FIT = min(cfg.LMAX, 350)  # fit up to 350 to avoid deconvolution tail

# Define bins
bin_edges = np.unique(np.concatenate([[2], np.linspace(10, LMAX_FIT, 18).astype(int)]))
nbin = len(bin_edges) - 1
bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])


def bin_cl(cl):
    out = np.zeros(nbin)
    for b, (lo, hi) in enumerate(zip(bin_edges[:-1], bin_edges[1:])):
        sel = np.arange(lo, hi)
        out[b] = np.mean(cl[sel])
    return out


# Data: binned NILC Cl
cl_data = bin_cl(cl_nilc[:LMAX_FIT + 1])

# Effective noise Cl: residual foreground + instrument noise contribution.
# Estimate empirically: difference between NILC Cl and true-CMB-realization Cl,
# smoothed. If negative, set to small floor. This accounts for ILC bias too.
ell = np.arange(len(cl_nilc))
# Simple white-ish noise floor from dispersion of (cl_nilc - cl_real)
diff = cl_nilc[:LMAX_FIT + 1] - cl_real[:LMAX_FIT + 1]
# Binned variance from data
var_cl = np.zeros(nbin)
for b, (lo, hi) in enumerate(zip(bin_edges[:-1], bin_edges[1:])):
    ellb = np.arange(lo, hi)
    nmodes = np.sum(2 * ellb + 1)
    # Cosmic variance + noise-like term using magnitude of NILC spectrum as a guess
    cv = 2.0 * cl_data[b]**2 / max(nmodes, 1)
    # Add 10% modelling-error floor (residual foregrounds / ILC bias)
    mod_err = (0.10 * cl_data[b])**2
    var_cl[b] = cv + mod_err


def theory_cl(As, ns, H0, lmax=LMAX_FIT):
    p = camb.CAMBparams()
    p.set_cosmology(H0=H0, ombh2=cfg.FID['ombh2'], omch2=cfg.FID['omch2'],
                    tau=cfg.FID['tau'])
    p.InitPower.set_params(As=As, ns=ns)
    p.set_for_lmax(lmax + 50, lens_potential_accuracy=0)
    r = camb.get_results(p)
    totCL = r.get_cmb_power_spectra(p, CMB_unit='muK', raw_cl=True)['total']
    return totCL[:lmax + 1, 0]


def log_prior(theta):
    As, ns, H0 = theta
    if not (1.0e-9 < As < 4.0e-9):
        return -np.inf
    if not (0.85 < ns < 1.05):
        return -np.inf
    if not (55.0 < H0 < 80.0):
        return -np.inf
    return 0.0


def log_prob(theta):
    lp = log_prior(theta)
    if not np.isfinite(lp):
        return -np.inf
    As, ns, H0 = theta
    try:
        cl = theory_cl(As, ns, H0)
    except Exception:
        return -np.inf
    cl_bin = bin_cl(cl)
    resid = cl_data - cl_bin
    chi2 = np.sum(resid**2 / var_cl)
    return -0.5 * chi2 + lp


if __name__ == '__main__':
    ndim = 3
    nwalkers = 16
    nsteps = 250
    # Initialize near fiducial
    p0 = np.array([cfg.FID['As'], cfg.FID['ns'], cfg.FID['H0']])
    scale = np.array([0.1e-9, 0.02, 2.0])
    pos = p0 + scale * np.random.default_rng(1).normal(size=(nwalkers, ndim))

    # Serial execution (multiprocessing+spawn on macOS had heavy startup cost)
    os.environ.setdefault('OMP_NUM_THREADS', '2')
    t0 = time.time()
    sampler = emcee.EnsembleSampler(nwalkers, ndim, log_prob)
    # Print periodic progress manually
    for i, _ in enumerate(sampler.sample(pos, iterations=nsteps)):
        if (i + 1) % 10 == 0:
            elapsed = time.time() - t0
            frac = (i + 1) / nsteps
            eta = elapsed * (1 - frac) / frac
            print(f'  step {i+1}/{nsteps}  elapsed={elapsed:.0f}s  ETA={eta:.0f}s', flush=True)
    elapsed = time.time() - t0
    print(f'MCMC took {elapsed:.0f} s')

    # Burn-in
    burn = 80
    samples = sampler.get_chain(discard=burn, flat=True)
    np.savez('data/mcmc.npz', samples=samples,
             chain=sampler.get_chain(), log_prob=sampler.get_log_prob(),
             param_names=np.array(['As', 'ns', 'H0']),
             fiducial=np.array([cfg.FID['As'], cfg.FID['ns'], cfg.FID['H0']]))

    # Summary
    labels = ['$A_s$ [$10^{-9}$]', '$n_s$', '$H_0$']
    disp = samples.copy()
    disp[:, 0] *= 1e9
    means = disp.mean(axis=0)
    stds = disp.std(axis=0)
    truths = np.array([cfg.FID['As'] * 1e9, cfg.FID['ns'], cfg.FID['H0']])
    print('\nParameter estimates (mean ± 1σ, fiducial):')
    for l, m, s, t in zip(labels, means, stds, truths):
        print(f'  {l}: {m:.4f} ± {s:.4f}  (fid {t:.4f})  bias={((m - t) / s):+.2f}σ')

    # Corner plot
    fig = corner.corner(disp, labels=labels, truths=truths,
                        show_titles=True, title_fmt='.3f')
    fig.savefig('figures/corner.png', dpi=130)
    plt.close(fig)

    # Chain plot
    fig, axes = plt.subplots(ndim, 1, figsize=(8, 6), sharex=True)
    chain = sampler.get_chain()
    for i, (ax, l) in enumerate(zip(axes, labels)):
        factor = 1e9 if i == 0 else 1.0
        ax.plot(chain[:, :, i] * factor, alpha=0.4, lw=0.5)
        ax.axhline(truths[i], color='k', lw=1)
        ax.set_ylabel(l)
    axes[-1].set_xlabel('step')
    fig.tight_layout()
    fig.savefig('figures/chain.png', dpi=130)
    plt.close(fig)

    # Save binning info too
    np.savez('data/binning.npz', bin_edges=bin_edges, bin_centers=bin_centers,
             cl_data=cl_data, var_cl=var_cl)
    print('Done.')
