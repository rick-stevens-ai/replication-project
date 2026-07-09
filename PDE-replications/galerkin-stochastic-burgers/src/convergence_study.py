"""
Convergence study replicating Figure 4.1 from Blömker & Jentzen (2013).

The paper computes:
- Reference solution with N_ref = 16384 modes, 200 time steps
- Test solutions with N = 16, 32, 64, 128, 256, 512, 1024, 2048
- Error metric: sup_t sup_x |u_ref(t,x) - u_N(t,x)|  (Eq. 4.20)
- Expected convergence rate: ~N^{-1/2} in L∞ norm

Key: All solutions share the SAME Brownian motion — the N-mode solution
uses the first N components of the N_ref-dimensional Brownian motion.
"""

import numpy as np
import sys
import time
import json
from galerkin_burgers import (
    eigenvalues,
    initial_condition_coefficients,
    nonlinear_term_pseudospectral,
    evaluate_solution,
)


def solve_with_precomputed_noise(
    N: int,
    noise_increments: np.ndarray,
    T: float = 0.05,
    n_steps: int = 200,
    b_noise: float = 1.0 / 3.0,
    M_collocation: int = None,
) -> np.ndarray:
    """
    Solve the Galerkin system using pre-generated noise increments.
    
    Parameters
    ----------
    N : number of modes to use (uses first N components of noise)
    noise_increments : shape (n_steps, N_max), standard normal increments
    
    Returns
    -------
    a_history : shape (n_steps+1, N)
    """
    dt = T / n_steps
    lam = eigenvalues(N)
    
    exp_neg_lam_dt = np.exp(-lam * dt)
    phi1 = np.where(
        lam * dt > 1e-10,
        (1.0 - exp_neg_lam_dt) / lam,
        dt * (1.0 - lam * dt / 2.0)
    )
    noise_std = b_noise * np.sqrt(
        np.where(
            lam * dt > 1e-10,
            (1.0 - np.exp(-2.0 * lam * dt)) / (2.0 * lam),
            dt * (1.0 - lam * dt)
        )
    )
    
    if M_collocation is None:
        M_collocation = max(3 * N, 256)
    
    a = initial_condition_coefficients(N)
    a_history = np.zeros((n_steps + 1, N))
    a_history[0] = a.copy()
    
    for n in range(n_steps):
        F = nonlinear_term_pseudospectral(a, N, M_collocation)
        xi = noise_increments[n, :N]
        a = exp_neg_lam_dt * a + phi1 * F + noise_std * xi
        a_history[n + 1] = a.copy()
    
    return a_history


def compute_pathwise_Linf_error(a_ref, a_test, M_eval=2000):
    """
    Compute pathwise L∞([0,T]; L∞(0,1)) error.
    """
    x = np.linspace(0, 1, M_eval + 2)[1:-1]
    n_steps = a_ref.shape[0]
    
    N_ref = a_ref.shape[1]
    N_test = a_test.shape[1]
    
    k_ref = np.arange(1, N_ref + 1)
    k_test = np.arange(1, N_test + 1)
    sin_ref = np.sin(np.outer(x, k_ref * np.pi))
    sin_test = np.sin(np.outer(x, k_test * np.pi))
    sqrt2 = np.sqrt(2.0)
    
    max_error = 0.0
    for n in range(n_steps):
        u_ref = sqrt2 * sin_ref @ a_ref[n]
        u_test = sqrt2 * sin_test @ a_test[n]
        err = np.max(np.abs(u_ref - u_test))
        max_error = max(max_error, err)
    
    return max_error


def run_convergence_study(
    N_ref=4096,
    N_values=None,
    T=0.05,
    n_steps=200,
    n_realizations=10,
    seed=42,
    save_path=None,
):
    """
    Run the spatial convergence study with shared Brownian motion.
    """
    if N_values is None:
        N_values = [16, 32, 64, 128, 256, 512, 1024, 2048]
    
    rng = np.random.default_rng(seed)
    
    errors = {N: [] for N in N_values}
    
    for r in range(n_realizations):
        t0 = time.time()
        
        # Pre-generate ALL noise increments for this realization
        # Shape: (n_steps, N_ref) — standard normal
        noise = rng.standard_normal((n_steps, N_ref))
        
        # Compute reference solution
        a_ref = solve_with_precomputed_noise(
            N_ref, noise, T=T, n_steps=n_steps,
            M_collocation=3 * N_ref
        )
        
        # Compute test solutions (each uses first N columns of same noise)
        for N in N_values:
            a_test = solve_with_precomputed_noise(
                N, noise, T=T, n_steps=n_steps,
                M_collocation=max(3 * N, 256)
            )
            err = compute_pathwise_Linf_error(a_ref, a_test, M_eval=2000)
            errors[N].append(err)
        
        elapsed = time.time() - t0
        print(f"  Realization {r+1}/{n_realizations}: {elapsed:.1f}s", flush=True)
    
    # Compute statistics
    results = {}
    print("\n" + "="*60)
    print(f"{'N':>6s} {'Mean Error':>12s} {'Std Error':>12s}")
    print("-"*36)
    for N in N_values:
        errs = np.array(errors[N])
        mean_err = np.mean(errs)
        std_err = np.std(errs)
        results[N] = {'mean': float(mean_err), 'std': float(std_err),
                       'errors': [float(e) for e in errs]}
        print(f"{N:6d} {mean_err:12.6e} {std_err:12.6e}")
    
    # Convergence rates
    print("\n" + "="*60)
    print("Convergence rates (log-log slope between successive N):")
    mean_errors = [results[N]['mean'] for N in N_values]
    for i in range(1, len(N_values)):
        rate = -(np.log(mean_errors[i]) - np.log(mean_errors[i-1])) / \
                (np.log(N_values[i]) - np.log(N_values[i-1]))
        print(f"  N={N_values[i-1]:4d} -> {N_values[i]:4d}: rate = {rate:.4f}")
    
    # Overall rate
    log_N = np.log(np.array(N_values, dtype=float))
    log_err = np.log(np.array(mean_errors))
    slope, intercept = np.polyfit(log_N, log_err, 1)
    print(f"\nOverall log-log slope: {slope:.4f}")
    print(f"Expected (paper): ~-0.5")
    
    results['overall_slope'] = float(slope)
    results['N_ref'] = N_ref
    results['n_realizations'] = n_realizations
    results['N_values'] = N_values
    
    if save_path:
        with open(save_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to {save_path}")
    
    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--N-ref', type=int, default=4096)
    parser.add_argument('--n-real', type=int, default=10)
    parser.add_argument('--quick', action='store_true')
    args = parser.parse_args()
    
    if args.quick:
        N_values = [8, 16, 32, 64, 128, 256]
        N_ref = 1024
        n_real = 3
    else:
        N_values = [16, 32, 64, 128, 256, 512, 1024, 2048]
        N_ref = args.N_ref
        n_real = args.n_real
    
    results = run_convergence_study(
        N_ref=N_ref,
        N_values=N_values,
        n_realizations=n_real,
        save_path='../report/convergence_results.json',
    )
