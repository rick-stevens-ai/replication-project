#!/usr/bin/env python3
"""
Main computation script: Runs all SD rate calculations for paper replication.
Optimized to reuse loaded target objects.
"""
import sys
import os
import numpy as np
import pickle
import time
import warnings
warnings.filterwarnings('ignore')

# Suppress DarkELF loading messages
class SuppressOutput:
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        return self
    def __exit__(self, *args):
        sys.stdout.close()
        sys.stdout = self._stdout

sys.path.insert(0, os.path.expanduser("~/projects/replicate-darkmatter/darkelf_repo"))
import darkelf as de

# ===== Config =====
PROJECT_DIR = os.path.expanduser("~/projects/replicate-darkmatter")
DATA_DIR = os.path.join(PROJECT_DIR, "darkelf_repo", "data") + "/"
C_KMS = 2.99792458e5
V0_KMS = 220.0
VE_KMS = 240.0
VESC_KMS = 500.0
MA_PRIME = 10e9  # 10 GeV A' mediator

THRESHOLDS = {'1meV': 1e-3, '20meV': 20e-3, '100meV': 100e-3, '1eV': 1.0}

def mx_range():
    return np.logspace(np.log10(1e3), np.log10(1e9), 60)

def q0(mX):
    return mX * V0_KMS / C_KMS

def mmed_heavy(mX):
    return 3.0 * q0(mX)

def mmed_light(mX):
    return 0.3 * q0(mX)


def load_target_once(target):
    """Load target with dummy params, then update per mass point."""
    with SuppressOutput():
        d = de.darkelf(target=target, mX=1e6, mMed=1e9,
                       v0kms=V0_KMS, vekms=VE_KMS, vesckms=VESC_KMS,
                       eps_data_dir=DATA_DIR)
    return d


def compute_curve(d, mX_arr, SD_op, regime, threshold_eV, nucleon='p'):
    """Compute sigma for 3 events/kg/yr across mass range."""
    sigmas = np.full(len(mX_arr), np.inf)
    for i, mX in enumerate(mX_arr):
        try:
            if SD_op == "A'":
                mMed = MA_PRIME
            elif regime == 'heavy':
                mMed = mmed_heavy(mX)
            else:
                mMed = mmed_light(mX)
            
            d.update_params(mX=mX, mMed=mMed, SD_op=SD_op,
                           v0kms=V0_KMS, vekms=VE_KMS, vesckms=VESC_KMS)
            
            sig = d.sigma_multiphonons_SD(threshold=threshold_eV, nucleon=nucleon)
            if sig is not None and not np.isnan(sig) and sig != float('inf'):
                sigmas[i] = sig
        except Exception:
            pass
    return sigmas


def compute_curve_SI(d, mX_arr, regime, threshold_eV):
    """Compute sigma for 3 events/kg/yr for SI scattering."""
    sigmas = np.full(len(mX_arr), np.inf)
    for i, mX in enumerate(mX_arr):
        try:
            if regime == 'heavy':
                mMed = mmed_heavy(mX)
            else:
                mMed = mmed_light(mX)
            
            d.update_params(mX=mX, mMed=mMed,
                           v0kms=V0_KMS, vekms=VE_KMS, vesckms=VESC_KMS)
            
            sig = d.sigma_multiphonons_SI(threshold=threshold_eV)
            if sig is not None and not np.isnan(sig) and sig != float('inf'):
                sigmas[i] = sig
        except Exception:
            pass
    return sigmas


def run_full():
    """Run all computations."""
    mx_arr = mx_range()
    results = {'mx_eV': mx_arr}
    
    targets = ['Al2O3', 'GaAs']
    operators = ['phi', 'a', "A'"]
    regimes = ['heavy', 'light']
    
    total_curves = 0
    for target in targets:
        for op in operators:
            if op == "A'":
                total_curves += len(THRESHOLDS)
            else:
                total_curves += 2 * len(THRESHOLDS)
    
    done = 0
    t0 = time.time()
    
    for target in targets:
        print(f"\nLoading {target}...")
        d = load_target_once(target)
        
        for op in operators:
            op_regimes = ['heavy'] if op == "A'" else regimes
            
            for regime in op_regimes:
                key = f"{target}_{op}_{regime}"
                results[key] = {}
                
                for th_label, th_eV in THRESHOLDS.items():
                    t1 = time.time()
                    sigmas = compute_curve(d, mx_arr, op, regime, th_eV, nucleon='p')
                    results[key][th_label] = sigmas
                    done += 1
                    dt = time.time() - t1
                    finite = np.sum(np.isfinite(sigmas) & (sigmas < 1e10))
                    print(f"  [{done}/{total_curves}] {key} {th_label}: "
                          f"{finite}/{len(mx_arr)} finite, {dt:.1f}s")
    
    # Also SI benchmark for Al2O3
    print("\nComputing SI benchmark for Al2O3...")
    d_al = load_target_once('Al2O3')
    results['Al2O3_SI_heavy'] = {}
    for th_label, th_eV in THRESHOLDS.items():
        t1 = time.time()
        sigmas = compute_curve_SI(d_al, mx_arr, 'heavy', th_eV)
        results['Al2O3_SI_heavy'][th_label] = sigmas
        finite = np.sum(np.isfinite(sigmas) & (sigmas < 1e10))
        print(f"  Al2O3 SI heavy {th_label}: {finite}/{len(mx_arr)} finite, {time.time()-t1:.1f}s")
    
    # SI benchmark for GaAs
    print("Computing SI benchmark for GaAs...")
    d_ga = load_target_once('GaAs')
    results['GaAs_SI_heavy'] = {}
    for th_label, th_eV in THRESHOLDS.items():
        t1 = time.time()
        sigmas = compute_curve_SI(d_ga, mx_arr, 'heavy', th_eV)
        results['GaAs_SI_heavy'][th_label] = sigmas
        finite = np.sum(np.isfinite(sigmas) & (sigmas < 1e10))
        print(f"  GaAs SI heavy {th_label}: {finite}/{len(mx_arr)} finite, {time.time()-t1:.1f}s")
    
    elapsed = time.time() - t0
    print(f"\nTotal computation time: {elapsed:.0f}s ({elapsed/60:.1f}min)")
    
    # Save
    outpath = os.path.join(PROJECT_DIR, 'data', 'all_results.pkl')
    with open(outpath, 'wb') as f:
        pickle.dump(results, f)
    print(f"Results saved to {outpath}")
    
    return results


if __name__ == '__main__':
    run_full()
