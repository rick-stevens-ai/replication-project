"""
Temporal convergence study for the exponential Euler scheme.

Fix N (spatial resolution) and vary Δt to check temporal convergence order.
For exponential Euler with additive noise, expect strong order 1/2.
"""

import numpy as np
import json
import time
from galerkin_burgers_fast import GalerkinSolver, compute_pathwise_Linf_error, eigenvalues, initial_condition_coefficients


def solve_temporal_refinement(
    N, n_steps, noise_fine, n_steps_ref, T=0.05, b_noise=1.0/3.0
):
    """
    Solve with n_steps time steps, using subsampled noise from a fine-grid
    realization with n_steps_ref steps.
    
    noise_fine: shape (n_steps_ref, N) standard normal increments for the
                finest grid. Coarser grids sum consecutive increments.
    """
    assert n_steps_ref % n_steps == 0
    ratio = n_steps_ref // n_steps
    dt = T / n_steps
    
    lam = eigenvalues(N)
    exp_neg = np.exp(-lam * dt)
    phi1 = np.where(
        lam * dt > 1e-10,
        (1.0 - exp_neg) / lam,
        dt * (1.0 - lam * dt / 2.0)
    )
    noise_std = b_noise * np.sqrt(
        np.where(
            lam * dt > 1e-10,
            (1.0 - np.exp(-2.0 * lam * dt)) / (2.0 * lam),
            dt * (1.0 - lam * dt)
        )
    )
    
    # Precompute matrices for nonlinear term
    M = max(3 * N, 256)
    x = np.linspace(0, 1, M + 2)[1:-1]
    k = np.arange(1, N + 1)
    sin_matrix = np.sin(np.outer(x, k * np.pi))
    cos_matrix = np.cos(np.outer(x, k * np.pi))
    sqrt2 = np.sqrt(2.0)
    dx_grid = 1.0 / (M + 1)
    proj = sqrt2 * dx_grid * sin_matrix.T
    k_pi = k * np.pi
    
    a = initial_condition_coefficients(N)
    a_history = np.zeros((n_steps + 1, N))
    a_history[0] = a.copy()
    
    # For the noise: the exponential Euler noise term with exact linear integration
    # has variance b² (1 - e^{-2λΔt})/(2λ).
    # But when we sum fine-grid increments, we need to be careful.
    # 
    # Actually, for the exponential Euler, the noise at the coarse step
    # is NOT simply the sum of fine-step noises, because the linear part
    # is integrated exactly. The correct approach is to generate noise
    # directly at the coarse level.
    #
    # For a fair temporal convergence test, we should generate independent
    # noise at each resolution level with matched Brownian paths.
    # 
    # The Brownian increment ΔW over [t_n, t_{n+1}] with Δt_coarse = ratio * Δt_fine
    # is: ΔW_coarse = Σ_{j=0}^{ratio-1} ΔW_fine^{n*ratio + j}
    # 
    # For the exponential Euler scheme, the stochastic integral is:
    # I_i = ∫_{t_n}^{t_{n+1}} e^{-λ_i(t_{n+1}-s)} dβ_i(s)
    # 
    # This is approximated as: √((1-e^{-2λΔt})/(2λ)) · ξ where ξ ~ N(0,1)
    # 
    # The Brownian path consistency requires: for strong convergence,
    # we compare against a reference with the same Brownian motion.
    # 
    # Simplification: use the fine noise directly. At the coarse level,
    # sum consecutive ΔW and use that as the driving noise.
    # The noise in our scheme is: noise_std_i * ξ_i^n
    # The ξ at the coarse level should be chosen so that the Brownian path matches.
    #
    # Actually, for a clean temporal convergence test, let's just use 
    # the noise_std at each level with independent noise and average over
    # many realizations. The convergence is then in the strong (L2) sense.
    
    # For consistency, generate scaled Brownian increments at fine level 
    # and sum for coarse:
    # ΔW_i^n = Σ_{j} (noise_std_fine_i * ξ_fine_i^{n*ratio+j})
    # This represents the total Brownian increment over the coarse interval.
    # Then the coarse-level stochastic integral approximation error is what 
    # we measure.
    
    # Sum noise over blocks of 'ratio' fine steps
    for n in range(n_steps):
        # Nonlinear term
        u = sqrt2 * sin_matrix @ a
        u_x = sqrt2 * cos_matrix @ (a * k_pi)
        f = -60.0 * u * u_x
        F = proj @ f
        
        # Sum noise: ΔB_coarse = Σ fine noise increments (standard normal sum)
        # The variance of the sum is ratio, so divide by sqrt(ratio) to normalize
        xi_sum = noise_fine[n*ratio:(n+1)*ratio, :N].sum(axis=0) / np.sqrt(ratio)
        
        a = exp_neg * a + phi1 * F + noise_std * xi_sum
        a_history[n + 1] = a.copy()
    
    return a_history


def run_temporal_study(
    N=256,
    n_steps_ref=6400,
    n_steps_values=None,
    T=0.05,
    n_realizations=20,
    seed=42,
    save_path=None,
):
    if n_steps_values is None:
        n_steps_values = [25, 50, 100, 200, 400, 800, 1600, 3200]
    
    # Ensure all divide n_steps_ref
    for ns in n_steps_values:
        assert n_steps_ref % ns == 0, f"{n_steps_ref} not divisible by {ns}"
    
    rng = np.random.default_rng(seed)
    errors = {ns: [] for ns in n_steps_values}
    
    print(f"Temporal convergence study: N={N}, T={T}")
    print(f"Reference: {n_steps_ref} steps, test: {n_steps_values}")
    print(f"{n_realizations} realizations\n")
    
    for r in range(n_realizations):
        t0 = time.time()
        
        # Generate fine-grid noise
        noise_fine = rng.standard_normal((n_steps_ref, N))
        
        # Reference solution
        a_ref = solve_temporal_refinement(N, n_steps_ref, noise_fine, n_steps_ref, T=T)
        
        for ns in n_steps_values:
            a_test = solve_temporal_refinement(N, ns, noise_fine, n_steps_ref, T=T)
            
            # Subsample reference to match test time points
            ratio = n_steps_ref // ns
            a_ref_sub = a_ref[::ratio]
            
            err = compute_pathwise_Linf_error(a_ref_sub, a_test, M_eval=1000)
            errors[ns].append(err)
        
        print(f"  Realization {r+1}/{n_realizations}: {time.time()-t0:.1f}s", flush=True)
    
    results = {}
    print("\n" + "="*60)
    print(f"{'n_steps':>8s} {'Δt':>12s} {'Mean Error':>12s} {'Std':>12s}")
    print("-"*50)
    for ns in n_steps_values:
        errs = np.array(errors[ns])
        dt = T / ns
        results[str(ns)] = {
            'mean': float(np.mean(errs)),
            'std': float(np.std(errs)),
            'dt': float(dt),
        }
        print(f"{ns:8d} {dt:12.6e} {np.mean(errs):12.6e} {np.std(errs):12.6e}")
    
    print("\nTemporal convergence rates:")
    mean_errors = [results[str(ns)]['mean'] for ns in n_steps_values]
    dts = [T/ns for ns in n_steps_values]
    for i in range(1, len(n_steps_values)):
        rate = (np.log(mean_errors[i-1]) - np.log(mean_errors[i])) / \
               (np.log(dts[i-1]) - np.log(dts[i]))
        print(f"  Δt={dts[i-1]:.2e} -> {dts[i]:.2e}: rate = {rate:.4f}")
    
    log_dt = np.log(np.array(dts))
    log_err = np.log(np.array(mean_errors))
    slope, _ = np.polyfit(log_dt, log_err, 1)
    print(f"\nOverall temporal slope: {slope:.4f}")
    print(f"Expected (exp Euler, additive noise): ~0.5")
    
    results['temporal_slope'] = float(slope)
    results['N'] = N
    results['n_steps_ref'] = n_steps_ref
    results['n_steps_values'] = n_steps_values
    results['n_realizations'] = n_realizations
    
    if save_path:
        with open(save_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nSaved to {save_path}")
    
    return results


if __name__ == "__main__":
    run_temporal_study(
        N=128,
        n_steps_ref=6400,
        n_steps_values=[50, 100, 200, 400, 800, 1600, 3200],
        n_realizations=20,
        save_path='../report/temporal_results.json',
    )
