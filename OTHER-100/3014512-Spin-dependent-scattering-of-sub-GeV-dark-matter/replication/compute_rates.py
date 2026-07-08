"""
Compute SD and SI scattering rates using DarkELF.
Reproduces Figures 6, 7, 8 from Gori et al. (2025).
"""
import sys
import os
import numpy as np
import pickle

sys.path.insert(0, os.path.expanduser("~/projects/replicate-darkmatter/darkelf_repo"))
import darkelf as de
from config import *


def load_target(target, mX_eV, SD_op="A'", mMed_eV=None, mediator_regime='heavy'):
    """Load a DarkELF target with given DM parameters."""
    if mMed_eV is None:
        if SD_op == "A'":
            mMed_eV = MA_PRIME
        elif mediator_regime == 'heavy':
            mMed_eV = mediator_mass_heavy(mX_eV)
        else:
            mMed_eV = mediator_mass_light(mX_eV)
    
    d = de.darkelf(
        target=target,
        mX=mX_eV,
        mMed=mMed_eV,
        v0kms=V0_KMS,
        vekms=VE_KMS,
        vesckms=VESC_KMS,
        eps_data_dir=DATA_DIR + '/',
    )
    d.update_params(mX=mX_eV, mMed=mMed_eV, SD_op=SD_op,
                    v0kms=V0_KMS, vekms=VE_KMS, vesckms=VESC_KMS)
    return d


def compute_sigma_sd(target, SD_op, mediator_regime, thresholds_eV, 
                     mx_array=None, nucleon='p'):
    """
    Compute σ̄ corresponding to 3 events/kg/yr for SD scattering.
    
    Returns dict: {threshold_label: array of sigma values}
    """
    if mx_array is None:
        mx_array = mx_range_eV()
    
    results = {}
    for th_label, th_eV in thresholds_eV.items():
        sigmas = np.full(len(mx_array), np.inf)
        for i, mX in enumerate(mx_array):
            try:
                if SD_op == "A'":
                    mMed = MA_PRIME
                elif mediator_regime == 'heavy':
                    mMed = mediator_mass_heavy(mX)
                else:
                    mMed = mediator_mass_light(mX)
                
                d = load_target(target, mX, SD_op=SD_op, mMed_eV=mMed,
                               mediator_regime=mediator_regime)
                
                sig = d.sigma_multiphonons_SD(threshold=th_eV, nucleon=nucleon)
                if sig is not None and not np.isnan(sig) and sig != float('inf'):
                    sigmas[i] = sig
            except Exception as e:
                print(f"  Error at mX={mX:.1e}, {target}, {SD_op}, {th_label}: {e}")
                continue
            
            if (i+1) % 10 == 0:
                print(f"  {target} {SD_op} {mediator_regime} {th_label}: {i+1}/{len(mx_array)}")
        
        results[th_label] = sigmas
    
    return results


def compute_sigma_si(target, mediator_regime, thresholds_eV, mx_array=None):
    """
    Compute σ̄ corresponding to 3 events/kg/yr for SI scattering (benchmark).
    """
    if mx_array is None:
        mx_array = mx_range_eV()
    
    results = {}
    for th_label, th_eV in thresholds_eV.items():
        sigmas = np.full(len(mx_array), np.inf)
        for i, mX in enumerate(mx_array):
            try:
                if mediator_regime == 'heavy':
                    mMed = mediator_mass_heavy(mX)
                else:
                    mMed = mediator_mass_light(mX)
                
                d = load_target(target, mX, mMed_eV=mMed, mediator_regime=mediator_regime)
                
                sig = d.sigma_multiphonons_SI(threshold=th_eV)
                if sig is not None and not np.isnan(sig) and sig != float('inf'):
                    sigmas[i] = sig
            except Exception as e:
                print(f"  SI Error at mX={mX:.1e}, {target}, {th_label}: {e}")
                continue
            
            if (i+1) % 10 == 0:
                print(f"  {target} SI {mediator_regime} {th_label}: {i+1}/{len(mx_array)}")
        
        results[th_label] = sigmas
    
    return results


def run_all_computations(targets=None, operators=None, regimes=None):
    """Run all SD computations for the paper's figures."""
    if targets is None:
        targets = ['Al2O3', 'GaAs']
    if operators is None:
        operators = ['phi', 'a', "A'"]
    if regimes is None:
        regimes = ['heavy', 'light']
    
    mx_array = mx_range_eV()
    all_results = {'mx_eV': mx_array}
    
    for target in targets:
        for op in operators:
            if op == "A'":
                # A' only has heavy mediator
                key = f"{target}_{op}_heavy"
                print(f"\nComputing {key}...")
                nucleon = 'p'
                results = compute_sigma_sd(target, op, 'heavy', THRESHOLDS,
                                          mx_array, nucleon=nucleon)
                all_results[key] = results
            else:
                for regime in regimes:
                    key = f"{target}_{op}_{regime}"
                    print(f"\nComputing {key}...")
                    # For phi/a with gluon coupling, gn/gp is set by UV completion
                    nucleon = 'p'
                    results = compute_sigma_sd(target, op, regime, THRESHOLDS,
                                              mx_array, nucleon=nucleon)
                    all_results[key] = results
    
    return all_results


def save_results(results, filename='sd_results.pkl'):
    """Save results to pickle file."""
    outpath = os.path.join(PROJECT_DIR, 'data', filename)
    with open(outpath, 'wb') as f:
        pickle.dump(results, f)
    print(f"Results saved to {outpath}")


def load_results(filename='sd_results.pkl'):
    """Load results from pickle file."""
    inpath = os.path.join(PROJECT_DIR, 'data', filename)
    with open(inpath, 'rb') as f:
        return pickle.load(f)


if __name__ == '__main__':
    import time
    t0 = time.time()
    
    # Compute for Al2O3 and GaAs (paper's primary targets)
    results = run_all_computations(
        targets=['Al2O3', 'GaAs'],
        operators=['phi', 'a', "A'"],
        regimes=['heavy', 'light']
    )
    
    save_results(results, 'sd_results_al2o3_gaas.pkl')
    
    # Also compute for Si and Ge (for validation)
    results_sige = run_all_computations(
        targets=['Si', 'Ge'],
        operators=["A'"],
        regimes=['heavy']
    )
    save_results(results_sige, 'sd_results_si_ge.pkl')
    
    print(f"\nTotal time: {time.time()-t0:.1f}s")
