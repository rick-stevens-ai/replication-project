#!/usr/bin/env python3
"""
Generate a cosmological matter power spectrum dataset using CAMB.

Samples 500 cosmologies via Latin Hypercube in 6 parameters:
  (Omega_m, sigma_8, Omega_b, h, n_s, w)
Computes linear matter P(k) at z=0 on 50 log-spaced k-bins.

Outputs:
  ../data/params.npy   — (500, 6) array of cosmo parameters
  ../data/pks.npy      — (500, 50) array of P(k) values
  ../data/k_bins.npy   — (50,) array of k values [h/Mpc]
"""

import os
import sys
import time
import numpy as np
from scipy.stats.qmc import LatinHypercube

try:
    import camb
except ImportError:
    os.system(f"{sys.executable} -m pip install camb -q")
    import camb

N_COSMO = 500
N_K = 50
K_MIN = 1e-4
K_MAX = 10.0
SEED = 42

PARAM_NAMES = ["Omega_m", "sigma_8", "Omega_b", "h", "n_s", "w"]
PARAM_MINS = np.array([0.1,   0.6,  0.03,  0.55, 0.85, -1.3])
PARAM_MAXS = np.array([0.5,   1.0,  0.07,  0.85, 1.05, -0.7])

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

def generate_lhs_samples(n, dim, seed=42):
    sampler = LatinHypercube(d=dim, seed=seed)
    unit_samples = sampler.random(n=n)
    return PARAM_MINS + unit_samples * (PARAM_MAXS - PARAM_MINS)

def compute_pk(omega_m, sigma_8, omega_b, h, n_s, w, k_bins):
    ombh2 = omega_b * h**2
    omch2 = (omega_m - omega_b) * h**2
    pars = camb.CAMBparams()
    pars.set_cosmology(H0=h * 100, ombh2=ombh2, omch2=omch2)
    pars.set_dark_energy(w=w)
    pars.InitPower.set_params(As=2.1e-9, ns=n_s)
    pars.set_matter_power(redshifts=[0.0], kmax=K_MAX * 1.2)
    pars.NonLinear = camb.model.NonLinear_none
    results = camb.get_results(pars)
    sigma8_camb = results.get_sigma8_0()
    kh, z, pk = results.get_matter_power_spectrum(minkh=K_MIN, maxkh=K_MAX, npoints=200)
    pk_interp = np.interp(k_bins, kh, pk[0])
    rescale = (sigma_8 / sigma8_camb) ** 2
    pk_interp *= rescale
    return pk_interp

def main():
    print(f"Generating {N_COSMO} cosmologies with LHS sampling...")
    params = generate_lhs_samples(N_COSMO, len(PARAM_NAMES), seed=SEED)
    k_bins = np.logspace(np.log10(K_MIN), np.log10(K_MAX), N_K)
    pks = np.zeros((N_COSMO, N_K))
    
    t0 = time.time()
    failed = 0
    for i in range(N_COSMO):
        omega_m, sigma_8, omega_b, h, n_s, w = params[i]
        try:
            pks[i] = compute_pk(omega_m, sigma_8, omega_b, h, n_s, w, k_bins)
        except Exception as e:
            # Clip and retry
            params[i, 0] = np.clip(params[i, 0], 0.12, 0.48)
            params[i, 2] = np.clip(params[i, 2], 0.035, 0.065)
            omega_m, sigma_8, omega_b, h, n_s, w = params[i]
            try:
                pks[i] = compute_pk(omega_m, sigma_8, omega_b, h, n_s, w, k_bins)
            except:
                pks[i] = np.nan
                failed += 1
        if (i + 1) % 50 == 0:
            elapsed = time.time() - t0
            rate = (i + 1) / elapsed
            eta = (N_COSMO - i - 1) / rate
            print(f"  [{i+1}/{N_COSMO}] {elapsed:.1f}s elapsed, ~{eta:.0f}s remaining")
    
    total_time = time.time() - t0
    print(f"\nGenerated {N_COSMO} P(k) spectra in {total_time:.1f}s ({failed} failed)")
    
    # Remove NaN rows
    valid = ~np.any(np.isnan(pks), axis=1)
    params = params[valid]
    pks = pks[valid]
    
    np.save(os.path.join(DATA_DIR, "params.npy"), params)
    np.save(os.path.join(DATA_DIR, "pks.npy"), pks)
    np.save(os.path.join(DATA_DIR, "k_bins.npy"), k_bins)
    
    print(f"Saved: params {params.shape}, pks {pks.shape}, k_bins {k_bins.shape}")

if __name__ == "__main__":
    main()
