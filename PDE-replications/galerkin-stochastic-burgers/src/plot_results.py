"""
Visualization for the Galerkin stochastic Burgers equation replication.

Generates:
1. Convergence rate plot (replicating Figure 4.1)
2. Sample path visualizations
3. Solution evolution
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json
from galerkin_burgers import (
    solve_galerkin_exponential_euler,
    evaluate_solution,
)


def plot_convergence(results_file, output_file):
    """Plot convergence rates — replication of Figure 4.1."""
    with open(results_file) as f:
        results = json.load(f)
    
    N_values = results['N_values']
    mean_errors = [results[str(N)]['mean'] for N in N_values]
    std_errors = [results[str(N)]['std'] for N in N_values]
    
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    
    # Data points with error bars
    ax.errorbar(N_values, mean_errors, yerr=std_errors, 
                fmt='ko-', capsize=3, markersize=6, linewidth=1.5,
                label='Computed error')
    
    # Reference slopes (orderlines as in the paper)
    N_arr = np.array(N_values, dtype=float)
    
    # Slope -0.5 (paper's predicted rate)
    ref_05 = mean_errors[3] * (N_arr / N_values[3]) ** (-0.5)
    ax.plot(N_arr, ref_05, 'b--', linewidth=1, alpha=0.7, label='Order 0.5')
    
    # Slope -0.25
    ref_025 = mean_errors[3] * (N_arr / N_values[3]) ** (-0.25)
    ax.plot(N_arr, ref_025, 'r--', linewidth=1, alpha=0.7, label='Order 0.25')
    
    # Slope -1.0
    ref_10 = mean_errors[3] * (N_arr / N_values[3]) ** (-1.0)
    ax.plot(N_arr, ref_10, 'g--', linewidth=1, alpha=0.7, label='Order 1.0')
    
    ax.set_xscale('log', base=2)
    ax.set_yscale('log')
    ax.set_xlabel('Number of Galerkin modes N', fontsize=12)
    ax.set_ylabel('Pathwise $L^\\infty$ error', fontsize=12)
    ax.set_title('Spatial Convergence: Galerkin Approximation\n'
                 'Stochastic Burgers Equation (Blömker & Jentzen, 2013)',
                 fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Annotate overall slope
    overall_slope = results['overall_slope']
    ax.text(0.05, 0.05, f'Overall log-log slope: {overall_slope:.3f}\n'
            f'N_ref = {results["N_ref"]}, {results["n_realizations"]} realizations',
            transform=ax.transAxes, fontsize=9,
            verticalalignment='bottom',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Convergence plot saved to {output_file}")


def plot_sample_paths(output_file, N=128, n_samples=5, seed=100):
    """Plot sample solution paths at final time."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    x = np.linspace(0, 1, 500)
    rng = np.random.default_rng(seed)
    
    # Panel 1: Multiple sample paths at T=0.05
    ax = axes[0, 0]
    for i in range(n_samples):
        t, a = solve_galerkin_exponential_euler(N, T=0.05, n_steps=200, rng=rng)
        u_final = evaluate_solution(a[-1], x)
        ax.plot(x, u_final, alpha=0.7, label=f'Sample {i+1}')
    
    # Initial condition
    u0 = (6.0/5.0) * np.sin(np.pi * x)
    ax.plot(x, u0, 'k--', linewidth=2, label='Initial cond.')
    ax.set_xlabel('x')
    ax.set_ylabel('u(x, T)')
    ax.set_title(f'Sample paths at T=0.05 (N={N})')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    
    # Panel 2: Solution evolution for one realization
    ax = axes[0, 1]
    rng2 = np.random.default_rng(42)
    t, a = solve_galerkin_exponential_euler(N, T=0.05, n_steps=200, rng=rng2)
    
    time_indices = [0, 50, 100, 150, 200]
    colors = plt.cm.viridis(np.linspace(0, 1, len(time_indices)))
    for idx, ti in enumerate(time_indices):
        u = evaluate_solution(a[ti], x)
        ax.plot(x, u, color=colors[idx], linewidth=1.5,
                label=f't={t[ti]:.4f}')
    ax.set_xlabel('x')
    ax.set_ylabel('u(x, t)')
    ax.set_title(f'Solution evolution (N={N})')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    
    # Panel 3: Space-time surface plot
    ax = axes[1, 0]
    X_mesh, T_mesh = np.meshgrid(x, t)
    U = evaluate_solution(a, x)  # (n_steps+1, M)
    c = ax.pcolormesh(X_mesh, T_mesh, U, shading='auto', cmap='RdBu_r')
    plt.colorbar(c, ax=ax, label='u(x,t)')
    ax.set_xlabel('x')
    ax.set_ylabel('t')
    ax.set_title('Solution space-time plot')
    
    # Panel 4: Coefficient decay
    ax = axes[1, 1]
    for ti in [0, 100, 200]:
        coeffs = np.abs(a[ti])
        modes = np.arange(1, N + 1)
        ax.semilogy(modes, coeffs + 1e-16, 'o-', markersize=3,
                     label=f't={t[ti]:.4f}')
    ax.set_xlabel('Mode number k')
    ax.set_ylabel('|$a_k$|')
    ax.set_title('Galerkin coefficient magnitudes')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    
    plt.suptitle('Stochastic Burgers Equation — Spectral Galerkin Approximation',
                 fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Sample paths saved to {output_file}")


def plot_comparison_different_N(output_file, seed=42):
    """Show how the solution changes with N (spatial resolution)."""
    fig, ax = plt.subplots(figsize=(8, 5))
    
    x = np.linspace(0, 1, 500)
    N_values = [8, 16, 32, 64, 128, 512]
    
    # Pre-generate noise for largest N
    N_max = max(N_values)
    rng_master = np.random.default_rng(seed)
    noise = rng_master.standard_normal((200, N_max))
    
    from convergence_study import solve_with_precomputed_noise
    
    for N in N_values:
        a_hist = solve_with_precomputed_noise(N, noise, T=0.05, n_steps=200)
        u = evaluate_solution(a_hist[-1], x)
        ax.plot(x, u, linewidth=1.5, label=f'N={N}')
    
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('u(x, T)', fontsize=12)
    ax.set_title('Solution at T=0.05 for different Galerkin truncations\n'
                 '(same Brownian motion)', fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Comparison plot saved to {output_file}")


if __name__ == "__main__":
    import os
    fig_dir = '../figures'
    os.makedirs(fig_dir, exist_ok=True)
    
    results_file = '../report/convergence_results.json'
    
    # Plot convergence if results exist
    if os.path.exists(results_file):
        plot_convergence(results_file, f'{fig_dir}/convergence_rates.png')
    else:
        print("No convergence results yet — run convergence_study.py first")
    
    # Sample paths
    plot_sample_paths(f'{fig_dir}/sample_paths.png')
    
    # Comparison
    plot_comparison_different_N(f'{fig_dir}/N_comparison.png')
