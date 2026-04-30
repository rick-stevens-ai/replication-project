#!/usr/bin/env python3
"""
Main replication script for paper 1993311:
"Electronic specific heat capacities and entropies from DMQMC
using Gaussian process regression to find gradients of noisy data"

Replication strategy (synthetic data):
1. Use 2-site Hubbard model (exact eigenvalues known analytically)
2. Generate synthetic noisy E(T) mimicking DMQMC stochastic error
3. Compare three derivative methods:
   (a) Finite difference (numpy gradient)
   (b) Cubic spline + analytic derivative
   (c) GPR + analytic derivative (paper's method)
4. Compute C_V(T) and S(T) from each method
5. Compare against exact analytical results

Also tests multiple noise levels and a second system (4-site chain).

Author: Ollie (OpenClaw AI), replicating Malone et al. (2020)
"""

import numpy as np
import json
import os
import sys
import warnings
warnings.filterwarnings('ignore')

# Add code directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from exact_models import (
    hubbard_2site_eigenvalues, hydrogen_chain_eigenvalues,
    exact_energy, exact_cv, exact_entropy, generate_noisy_energy
)
from gpr_derivatives import (
    fit_gpr, gpr_predict, gpr_cv_from_beta, gpr_cv_from_T,
    compute_entropy_from_cv, TwoRegimeGPR
)
from finite_difference import (
    fd_cv_from_beta, fd_cv_from_T,
    spline_cv_from_beta, spline_cv_from_T,
    compute_entropy_fd
)


def rmse(pred, exact):
    """Root mean square error."""
    return np.sqrt(np.mean((pred - exact)**2))


def mae(pred, exact):
    """Mean absolute error."""
    return np.mean(np.abs(pred - exact))


def run_single_system(name, eigenvalues, beta_range, n_points,
                      noise_scale, noise_type, results_dir, seed=42):
    """
    Run full replication pipeline for one system.

    Returns dict of results and metrics.
    """
    print(f"\n{'='*60}")
    print(f"System: {name}")
    print(f"Eigenvalues: {eigenvalues}")
    print(f"Beta range: {beta_range}, N_points: {n_points}")
    print(f"Noise: scale={noise_scale}, type={noise_type}")
    print(f"{'='*60}")

    rng = np.random.default_rng(seed)

    # Generate data
    beta_data = np.linspace(beta_range[0], beta_range[1], n_points)
    T_data = 1.0 / beta_data  # Note: T_data is NOT sorted ascending

    E_exact_data = exact_energy(eigenvalues, beta_data)
    E_noisy, sigma = generate_noisy_energy(
        eigenvalues, beta_data, noise_scale, noise_type, rng
    )

    # Dense evaluation grid (sorted by T for plotting and integration)
    T_eval = np.linspace(1.0/beta_range[1], 1.0/beta_range[0], 500)
    beta_eval = 1.0 / T_eval  # decreasing
    # For beta-domain evaluation, we need sorted ascending beta
    beta_eval_sorted = np.sort(beta_eval)
    T_eval_from_beta = 1.0 / beta_eval_sorted

    # Exact values on evaluation grid
    E_exact_eval = exact_energy(eigenvalues, beta_eval_sorted)
    cv_exact_eval = exact_cv(eigenvalues, beta_eval_sorted)
    S_exact_eval = exact_entropy(eigenvalues, beta_eval_sorted)

    # For T-domain methods, we need data sorted by T
    sort_idx = np.argsort(T_data)
    T_sorted = T_data[sort_idx]
    E_noisy_T_sorted = E_noisy[sort_idx]
    sigma_T_sorted = sigma[sort_idx]

    results = {
        'name': name,
        'eigenvalues': eigenvalues.tolist(),
        'noise_scale': noise_scale,
        'noise_type': noise_type,
        'n_points': n_points,
    }

    # ============================================================
    # Method 1: Finite Difference on E(β) data
    # ============================================================
    print("\n--- Finite Difference (β-domain) ---")

    # Downsample every 10th point (as in paper)
    ds = max(1, n_points // 50)  # aim for ~50 points
    beta_ds = beta_data[::ds]
    E_noisy_ds = E_noisy[::ds]

    cv_fd_beta = fd_cv_from_beta(beta_ds, E_noisy_ds)
    # Map to T for comparison (beta_ds is descending in T)
    T_fd = 1.0 / beta_ds

    # Also do FD in T-domain
    T_ds = T_sorted[::ds]
    E_ds_T = E_noisy_T_sorted[::ds]
    cv_fd_T = fd_cv_from_T(T_ds, E_ds_T)

    # Exact at FD points for RMSE
    cv_exact_fd_beta = exact_cv(eigenvalues, beta_ds)
    cv_exact_fd_T = exact_cv(eigenvalues, 1.0/T_ds)

    rmse_fd_beta = rmse(cv_fd_beta, cv_exact_fd_beta)
    rmse_fd_T = rmse(cv_fd_T, cv_exact_fd_T)
    print(f"  RMSE(C_V, β-domain): {rmse_fd_beta:.6f}")
    print(f"  RMSE(C_V, T-domain): {rmse_fd_T:.6f}")

    results['fd'] = {
        'rmse_cv_beta': float(rmse_fd_beta),
        'rmse_cv_T': float(rmse_fd_T),
        'mae_cv_beta': float(mae(cv_fd_beta, cv_exact_fd_beta)),
        'mae_cv_T': float(mae(cv_fd_T, cv_exact_fd_T)),
    }

    # ============================================================
    # Method 2: Cubic Spline on E(β) data
    # ============================================================
    print("\n--- Cubic Spline ---")
    try:
        cv_spline_T = spline_cv_from_T(T_sorted, E_noisy_T_sorted,
                                         T_eval, resample_factor=max(1, n_points//50))
        cv_exact_spline = exact_cv(eigenvalues, 1.0/T_eval)
        rmse_spline = rmse(cv_spline_T, cv_exact_spline)
        print(f"  RMSE(C_V, T-domain): {rmse_spline:.6f}")
        results['spline'] = {
            'rmse_cv': float(rmse_spline),
            'mae_cv': float(mae(cv_spline_T, cv_exact_spline)),
        }
    except Exception as e:
        print(f"  Spline failed: {e}")
        cv_spline_T = None
        results['spline'] = {'error': str(e)}

    # ============================================================
    # Method 3: GPR (paper's method)
    # ============================================================
    print("\n--- GPR (paper's method) ---")

    # Strategy A: Single GP in β-domain
    print("  Fitting GP to E(β)...")
    try:
        gpr_beta = fit_gpr(beta_data, E_noisy, sigma, n_restarts=5)
        print(f"  Kernel: {gpr_beta.kernel_}")

        E_gpr_beta, E_gpr_std = gpr_predict(gpr_beta, beta_eval_sorted)
        cv_gpr_beta = gpr_cv_from_beta(gpr_beta, beta_eval_sorted)

        rmse_E_gpr = rmse(E_gpr_beta, E_exact_eval)
        rmse_cv_gpr_beta = rmse(cv_gpr_beta, cv_exact_eval)
        print(f"  RMSE(E):  {rmse_E_gpr:.6f}")
        print(f"  RMSE(C_V): {rmse_cv_gpr_beta:.6f}")

        results['gpr_beta'] = {
            'rmse_E': float(rmse_E_gpr),
            'rmse_cv': float(rmse_cv_gpr_beta),
            'mae_cv': float(mae(cv_gpr_beta, cv_exact_eval)),
        }
    except Exception as e:
        print(f"  GPR β-domain failed: {e}")
        cv_gpr_beta = None
        E_gpr_beta = None
        results['gpr_beta'] = {'error': str(e)}

    # Strategy B: Single GP in T-domain
    print("  Fitting GP to E(T)...")
    try:
        gpr_T = fit_gpr(T_sorted, E_noisy_T_sorted, sigma_T_sorted, n_restarts=5)
        print(f"  Kernel: {gpr_T.kernel_}")

        E_gpr_T, E_gpr_T_std = gpr_predict(gpr_T, T_eval)
        cv_gpr_T = gpr_cv_from_T(gpr_T, T_eval)

        cv_exact_T_eval = exact_cv(eigenvalues, 1.0/T_eval)
        E_exact_T_eval = exact_energy(eigenvalues, 1.0/T_eval)

        rmse_E_gpr_T = rmse(E_gpr_T, E_exact_T_eval)
        rmse_cv_gpr_T = rmse(cv_gpr_T, cv_exact_T_eval)
        print(f"  RMSE(E):  {rmse_E_gpr_T:.6f}")
        print(f"  RMSE(C_V): {rmse_cv_gpr_T:.6f}")

        results['gpr_T'] = {
            'rmse_E': float(rmse_E_gpr_T),
            'rmse_cv': float(rmse_cv_gpr_T),
            'mae_cv': float(mae(cv_gpr_T, cv_exact_T_eval)),
        }
    except Exception as e:
        print(f"  GPR T-domain failed: {e}")
        cv_gpr_T = None
        E_gpr_T = None
        results['gpr_T'] = {'error': str(e)}

    # Strategy C: Two-regime GPR (paper's full method)
    print("  Fitting two-regime GP...")
    try:
        crossover = 0.5 * (1.0/beta_range[0] + 1.0/beta_range[1])
        two_gpr = TwoRegimeGPR(crossover_T=crossover)
        E0 = np.min(eigenvalues)
        two_gpr.fit(beta_data, E_noisy, sigma, E0=E0)

        E_two = two_gpr.predict_energy(T_eval)
        cv_two = two_gpr.predict_cv(T_eval)

        rmse_E_two = rmse(E_two, E_exact_T_eval)
        rmse_cv_two = rmse(cv_two, cv_exact_T_eval)
        print(f"  RMSE(E):  {rmse_E_two:.6f}")
        print(f"  RMSE(C_V): {rmse_cv_two:.6f}")

        results['gpr_two_regime'] = {
            'rmse_E': float(rmse_E_two),
            'rmse_cv': float(rmse_cv_two),
            'mae_cv': float(mae(cv_two, cv_exact_T_eval)),
        }
    except Exception as e:
        print(f"  Two-regime GPR failed: {e}")
        cv_two = None
        results['gpr_two_regime'] = {'error': str(e)}

    # ============================================================
    # Entropy comparison
    # ============================================================
    print("\n--- Entropy ---")
    S_exact_T = exact_entropy(eigenvalues, 1.0/T_eval)

    entropy_results = {}

    # GPR entropy (best CV method)
    if cv_gpr_T is not None:
        S_gpr = compute_entropy_from_cv(T_eval, cv_gpr_T)
        rmse_S_gpr = rmse(S_gpr, S_exact_T)
        entropy_results['gpr_T'] = float(rmse_S_gpr)
        print(f"  RMSE(S, GPR-T):  {rmse_S_gpr:.6f}")

    # FD entropy
    S_fd = compute_entropy_fd(T_ds, cv_fd_T)
    cv_exact_at_Tds = exact_cv(eigenvalues, 1.0/T_ds)
    S_exact_at_Tds = exact_entropy(eigenvalues, 1.0/T_ds)
    rmse_S_fd = rmse(S_fd, S_exact_at_Tds)
    entropy_results['fd'] = float(rmse_S_fd)
    print(f"  RMSE(S, FD):     {rmse_S_fd:.6f}")

    # Spline entropy
    if cv_spline_T is not None:
        S_spline = compute_entropy_from_cv(T_eval, cv_spline_T)
        rmse_S_spline = rmse(S_spline, S_exact_T)
        entropy_results['spline'] = float(rmse_S_spline)
        print(f"  RMSE(S, Spline): {rmse_S_spline:.6f}")

    results['entropy_rmse'] = entropy_results

    # ============================================================
    # Save numerical data for plotting
    # ============================================================
    data = {
        'T_eval': T_eval.tolist(),
        'E_exact': E_exact_T_eval.tolist() if 'E_exact_T_eval' in dir() else exact_energy(eigenvalues, 1.0/T_eval).tolist(),
        'cv_exact': cv_exact_T_eval.tolist() if 'cv_exact_T_eval' in dir() else exact_cv(eigenvalues, 1.0/T_eval).tolist(),
        'S_exact': S_exact_T.tolist(),
        'T_data': T_sorted.tolist(),
        'E_noisy': E_noisy_T_sorted.tolist(),
        'sigma': sigma_T_sorted.tolist(),
    }

    if cv_gpr_T is not None:
        data['E_gpr_T'] = E_gpr_T.tolist()
        data['cv_gpr_T'] = cv_gpr_T.tolist()
        data['S_gpr_T'] = S_gpr.tolist() if 'S_gpr' in dir() else None

    if cv_fd_T is not None:
        data['T_fd'] = T_ds.tolist()
        data['cv_fd_T'] = cv_fd_T.tolist()
        data['S_fd'] = S_fd.tolist()

    if cv_spline_T is not None:
        data['cv_spline_T'] = cv_spline_T.tolist()
        data['S_spline'] = S_spline.tolist() if 'S_spline' in dir() else None

    fname = os.path.join(results_dir, f'{name}_data.json')
    with open(fname, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"\n  Data saved to {fname}")

    return results


def run_noise_sweep(eigenvalues, system_name, results_dir, seed=42):
    """Test multiple noise levels to show GPR advantage grows with noise."""
    noise_scales = [0.005, 0.01, 0.02, 0.05, 0.1]
    sweep_results = []

    for ns in noise_scales:
        print(f"\n  Noise scale = {ns}")
        rng = np.random.default_rng(seed)
        beta = np.linspace(0.1, 10.0, 200)
        T = 1.0 / beta
        E_noisy, sigma = generate_noisy_energy(
            eigenvalues, beta, ns, 'dmqmc_like', rng
        )

        sort_idx = np.argsort(T)
        T_sorted = T[sort_idx]
        E_sorted = E_noisy[sort_idx]
        sigma_sorted = sigma[sort_idx]

        T_eval = np.linspace(T_sorted[0], T_sorted[-1], 300)
        cv_exact = exact_cv(eigenvalues, 1.0/T_eval)

        # FD
        ds = 4
        T_ds = T_sorted[::ds]
        E_ds = E_sorted[::ds]
        cv_fd = fd_cv_from_T(T_ds, E_ds)
        cv_exact_ds = exact_cv(eigenvalues, 1.0/T_ds)
        rmse_fd = rmse(cv_fd, cv_exact_ds)

        # GPR
        try:
            gpr = fit_gpr(T_sorted, E_sorted, sigma_sorted, n_restarts=3)
            cv_gpr = gpr_cv_from_T(gpr, T_eval)
            rmse_gpr = rmse(cv_gpr, cv_exact)
        except Exception:
            rmse_gpr = float('nan')

        # Spline
        try:
            cv_sp = spline_cv_from_T(T_sorted, E_sorted, T_eval,
                                      resample_factor=max(1, len(T_sorted)//50))
            rmse_sp = rmse(cv_sp, cv_exact)
        except Exception:
            rmse_sp = float('nan')

        sweep_results.append({
            'noise_scale': ns,
            'rmse_fd': float(rmse_fd),
            'rmse_gpr': float(rmse_gpr),
            'rmse_spline': float(rmse_sp),
        })
        print(f"    FD: {rmse_fd:.4f}  Spline: {rmse_sp:.4f}  GPR: {rmse_gpr:.4f}")

    fname = os.path.join(results_dir, f'{system_name}_noise_sweep.json')
    with open(fname, 'w') as f:
        json.dump(sweep_results, f, indent=2)
    print(f"\n  Noise sweep saved to {fname}")
    return sweep_results


def main():
    results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               '..', 'results')
    os.makedirs(results_dir, exist_ok=True)

    all_results = {}

    # ==========================================================
    # System 1: 2-site Hubbard model (t=1, U=4)
    # ==========================================================
    eigs_hub = hubbard_2site_eigenvalues(t=1.0, U=4.0)
    res_hub = run_single_system(
        name='hubbard_2site_U4',
        eigenvalues=eigs_hub,
        beta_range=(0.1, 15.0),
        n_points=300,
        noise_scale=0.02,
        noise_type='dmqmc_like',
        results_dir=results_dir,
        seed=42
    )
    all_results['hubbard_2site_U4'] = res_hub

    # ==========================================================
    # System 2: 2-site Hubbard model with stronger correlation (U=8)
    # ==========================================================
    eigs_hub8 = hubbard_2site_eigenvalues(t=1.0, U=8.0)
    res_hub8 = run_single_system(
        name='hubbard_2site_U8',
        eigenvalues=eigs_hub8,
        beta_range=(0.1, 15.0),
        n_points=300,
        noise_scale=0.02,
        noise_type='dmqmc_like',
        results_dir=results_dir,
        seed=123
    )
    all_results['hubbard_2site_U8'] = res_hub8

    # ==========================================================
    # System 3: 4-site tight-binding chain
    # ==========================================================
    eigs_chain = hydrogen_chain_eigenvalues(n_sites=4)
    res_chain = run_single_system(
        name='chain_4site',
        eigenvalues=eigs_chain,
        beta_range=(0.1, 10.0),
        n_points=300,
        noise_scale=0.03,
        noise_type='dmqmc_like',
        results_dir=results_dir,
        seed=456
    )
    all_results['chain_4site'] = res_chain

    # ==========================================================
    # System 4: Higher noise to stress-test (Hubbard, noise=0.1)
    # ==========================================================
    res_noisy = run_single_system(
        name='hubbard_2site_U4_noisy',
        eigenvalues=eigs_hub,
        beta_range=(0.1, 15.0),
        n_points=300,
        noise_scale=0.1,
        noise_type='dmqmc_like',
        results_dir=results_dir,
        seed=789
    )
    all_results['hubbard_2site_U4_noisy'] = res_noisy

    # ==========================================================
    # Noise sweep (Fig-like analysis)
    # ==========================================================
    print("\n\n" + "="*60)
    print("NOISE SWEEP: GPR advantage vs noise level")
    print("="*60)
    sweep = run_noise_sweep(eigs_hub, 'hubbard_2site_U4', results_dir)
    all_results['noise_sweep'] = sweep

    # ==========================================================
    # Summary
    # ==========================================================
    print("\n\n" + "="*60)
    print("SUMMARY OF RESULTS")
    print("="*60)

    summary_file = os.path.join(results_dir, 'summary.json')
    with open(summary_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"Full results saved to {summary_file}")

    # Print comparison table
    print(f"\n{'System':<30} {'FD RMSE':>10} {'Spline RMSE':>12} {'GPR RMSE':>10} {'GPR/FD':>8}")
    print("-" * 75)
    for sysname in ['hubbard_2site_U4', 'hubbard_2site_U8', 'chain_4site', 'hubbard_2site_U4_noisy']:
        r = all_results[sysname]
        fd_rmse = r.get('fd', {}).get('rmse_cv_T', float('nan'))
        sp_rmse = r.get('spline', {}).get('rmse_cv', float('nan'))
        gpr_rmse = r.get('gpr_T', {}).get('rmse_cv', float('nan'))
        ratio = gpr_rmse / fd_rmse if fd_rmse > 0 else float('nan')
        print(f"{sysname:<30} {fd_rmse:10.6f} {sp_rmse:12.6f} {gpr_rmse:10.6f} {ratio:8.3f}")

    print("\nNoise sweep (Hubbard U=4):")
    print(f"{'Noise':>8} {'FD':>10} {'Spline':>10} {'GPR':>10} {'GPR/FD':>8}")
    print("-" * 50)
    for s in sweep:
        ratio = s['rmse_gpr'] / s['rmse_fd'] if s['rmse_fd'] > 0 else float('nan')
        print(f"{s['noise_scale']:8.3f} {s['rmse_fd']:10.4f} {s['rmse_spline']:10.4f} {s['rmse_gpr']:10.4f} {ratio:8.3f}")


if __name__ == '__main__':
    main()
