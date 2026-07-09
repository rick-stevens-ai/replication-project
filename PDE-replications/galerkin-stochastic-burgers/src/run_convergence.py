"""
Run the full convergence study using the optimized solver.
"""

import numpy as np
import sys
import time
import json
from galerkin_burgers_fast import (
    GalerkinSolver,
    compute_pathwise_Linf_error,
)


def run_study(
    N_ref=4096,
    N_values=None,
    T=0.05,
    n_steps=200,
    n_realizations=10,
    seed=42,
    save_path=None,
):
    if N_values is None:
        N_values = [16, 32, 64, 128, 256, 512, 1024, 2048]
    
    rng = np.random.default_rng(seed)
    
    # Create solvers (precompute matrices once)
    print(f"Precomputing matrices for N_ref={N_ref}...", flush=True)
    t0 = time.time()
    solver_ref = GalerkinSolver(N_ref, T=T, n_steps=n_steps)
    print(f"  Reference solver ready in {time.time()-t0:.1f}s")
    
    solvers = {}
    for N in N_values:
        solvers[N] = GalerkinSolver(N, T=T, n_steps=n_steps)
    print(f"  All test solvers ready.")
    
    errors = {N: [] for N in N_values}
    
    for r in range(n_realizations):
        t0 = time.time()
        
        # Pre-generate noise for N_ref modes
        noise = rng.standard_normal((n_steps, N_ref))
        
        # Reference solution
        a_ref = solver_ref.solve(noise_increments=noise)
        t_ref = time.time() - t0
        
        # Test solutions
        for N in N_values:
            a_test = solvers[N].solve(noise_increments=noise)
            err = compute_pathwise_Linf_error(a_ref, a_test, M_eval=2000)
            errors[N].append(err)
        
        elapsed = time.time() - t0
        print(f"  Realization {r+1}/{n_realizations}: {elapsed:.1f}s "
              f"(ref: {t_ref:.1f}s)", flush=True)
    
    # Results
    results = {}
    print("\n" + "="*60)
    print(f"{'N':>6s} {'Mean Error':>12s} {'Std Error':>12s}")
    print("-"*36)
    for N in N_values:
        errs = np.array(errors[N])
        mean_err = np.mean(errs)
        std_err = np.std(errs)
        results[str(N)] = {
            'mean': float(mean_err), 
            'std': float(std_err),
            'errors': [float(e) for e in errs]
        }
        print(f"{N:6d} {mean_err:12.6e} {std_err:12.6e}")
    
    # Rates
    print("\n" + "="*60)
    print("Convergence rates (log-log slope between successive N):")
    mean_errors = [results[str(N)]['mean'] for N in N_values]
    for i in range(1, len(N_values)):
        rate = -(np.log(mean_errors[i]) - np.log(mean_errors[i-1])) / \
                (np.log(N_values[i]) - np.log(N_values[i-1]))
        print(f"  N={N_values[i-1]:4d} -> {N_values[i]:4d}: rate = {rate:.4f}")
    
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
    args = parser.parse_args()
    
    run_study(
        N_ref=args.N_ref,
        n_realizations=args.n_real,
        save_path='../report/convergence_results.json',
    )
