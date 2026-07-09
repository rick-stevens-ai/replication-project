"""
Plot convergence results for PWDG Helmholtz replication.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json
import os


def plot_p_convergence(results_file, output_dir):
    """Plot p-convergence for plane wave solution."""
    with open(results_file) as f:
        results = json.load(f)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    markers = ['o', 's', '^', 'D']
    
    for idx, (key, data) in enumerate(results.items()):
        p_vals = np.array(data['p_values'])
        L2_errs = np.array(data['errors_L2'])
        DG_errs = np.array(data['errors_DG'])
        k = data['k']
        
        # Filter out NaN
        valid_L2 = ~np.isnan(L2_errs)
        valid_DG = ~np.isnan(DG_errs)
        
        if np.any(valid_L2):
            axes[0].semilogy(p_vals[valid_L2], L2_errs[valid_L2], 
                           f'-{markers[idx]}', color=colors[idx],
                           label=f'k = {k}', markersize=6, linewidth=1.5)
        
        if np.any(valid_DG):
            axes[1].semilogy(p_vals[valid_DG], DG_errs[valid_DG],
                           f'-{markers[idx]}', color=colors[idx],
                           label=f'k = {k}', markersize=6, linewidth=1.5)
    
    # Add reference exponential convergence line
    for ax_idx, ax in enumerate(axes):
        if len(results) > 0:
            first_key = list(results.keys())[0]
            p_ref = np.array(results[first_key]['p_values'])
            # Exponential reference: C * exp(-sigma * p)
            if ax_idx == 0:
                errs = np.array(results[first_key]['errors_L2'])
            else:
                errs = np.array(results[first_key]['errors_DG'])
            valid = ~np.isnan(errs) & (errs > 0)
            if np.sum(valid) >= 3:
                # Fit exponential
                log_errs = np.log(errs[valid])
                p_fit = p_ref[valid]
                coeffs_fit = np.polyfit(p_fit, log_errs, 1)
                rate = -coeffs_fit[0]
                ref_line = np.exp(coeffs_fit[1]) * np.exp(-rate * p_ref)
                ax.semilogy(p_ref, ref_line, '--', color='gray', alpha=0.5,
                          label=f'exp(-{rate:.2f}p) reference')
    
    axes[0].set_xlabel('Number of plane wave directions p', fontsize=12)
    axes[0].set_ylabel('L² error', fontsize=12)
    axes[0].set_title('L² Error vs p (plane wave solution)', fontsize=13)
    axes[0].legend(fontsize=10)
    axes[0].grid(True, alpha=0.3)
    
    axes[1].set_xlabel('Number of plane wave directions p', fontsize=12)
    axes[1].set_ylabel('DG error', fontsize=12)
    axes[1].set_title('DG Error vs p (plane wave solution)', fontsize=13)
    axes[1].legend(fontsize=10)
    axes[1].grid(True, alpha=0.3)
    
    plt.suptitle('PWDG p-Convergence — Helmholtz Equation\n'
                 '(Hiptmair, Moiola, Perugia, SIAM J. Numer. Anal., 2011)',
                 fontsize=14, y=1.02)
    plt.tight_layout()
    
    out_path = os.path.join(output_dir, 'p_convergence_plane_wave.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved {out_path}")
    return out_path


def plot_p_convergence_circular(results_file, output_dir):
    """Plot p-convergence for circular wave solution."""
    with open(results_file) as f:
        data = json.load(f)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    p_vals = np.array(data['p_values'])
    L2_errs = np.array(data['errors_L2'])
    DG_errs = np.array(data['errors_DG'])
    k = data['k']
    
    valid_L2 = ~np.isnan(L2_errs) & (L2_errs > 0)
    valid_DG = ~np.isnan(DG_errs) & (DG_errs > 0)
    
    if np.any(valid_L2):
        ax.semilogy(p_vals[valid_L2], L2_errs[valid_L2], '-o', 
                   label='L² error', markersize=6, linewidth=1.5)
    if np.any(valid_DG):
        ax.semilogy(p_vals[valid_DG], DG_errs[valid_DG], '-s',
                   label='DG error', markersize=6, linewidth=1.5)
    
    # Fit exponential rate
    if np.sum(valid_L2) >= 3:
        log_errs = np.log(L2_errs[valid_L2])
        p_fit = p_vals[valid_L2]
        c = np.polyfit(p_fit, log_errs, 1)
        rate = -c[0]
        ref = np.exp(c[1]) * np.exp(-rate * p_vals)
        ax.semilogy(p_vals, ref, '--', color='gray', alpha=0.5,
                   label=f'exp(-{rate:.2f}p) fit')
    
    ax.set_xlabel('Number of plane wave directions p', fontsize=12)
    ax.set_ylabel('Error', fontsize=12)
    ax.set_title(f'PWDG p-Convergence — Circular Wave, k={k}', fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    out_path = os.path.join(output_dir, 'p_convergence_circular_wave.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved {out_path}")
    return out_path


def plot_h_convergence(results_file, output_dir):
    """Plot h-convergence results."""
    with open(results_file) as f:
        data = json.load(f)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    h_vals = np.array(data['h_values'])
    L2_errs = np.array(data['errors_L2'])
    DG_errs = np.array(data['errors_DG'])
    p = data['p']
    k = data['k']
    
    valid_L2 = ~np.isnan(L2_errs) & (L2_errs > 0)
    valid_DG = ~np.isnan(DG_errs) & (DG_errs > 0)
    
    if np.any(valid_L2):
        ax.loglog(h_vals[valid_L2], L2_errs[valid_L2], '-o',
                 label='L² error', markersize=6, linewidth=1.5)
    if np.any(valid_DG):
        ax.loglog(h_vals[valid_DG], DG_errs[valid_DG], '-s',
                 label='DG error', markersize=6, linewidth=1.5)
    
    # Reference slopes
    if np.sum(valid_L2) >= 3:
        log_h = np.log(h_vals[valid_L2])
        log_e = np.log(L2_errs[valid_L2])
        slope = np.polyfit(log_h, log_e, 1)[0]
        ref = L2_errs[valid_L2][0] * (h_vals / h_vals[valid_L2][0])**slope
        ax.loglog(h_vals, ref, '--', color='gray', alpha=0.5,
                 label=f'O(h^{slope:.1f}) reference')
    
    ax.set_xlabel('Mesh size h', fontsize=12)
    ax.set_ylabel('Error', fontsize=12)
    ax.set_title(f'PWDG h-Convergence — k={k}, p={p}', fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    out_path = os.path.join(output_dir, 'h_convergence.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved {out_path}")
    return out_path


def plot_convergence_rates(results_file, output_dir):
    """Compute and plot estimated exponential convergence rates."""
    with open(results_file) as f:
        results = json.load(f)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    for key, data in results.items():
        k = data['k']
        p_vals = np.array(data['p_values'])
        L2_errs = np.array(data['errors_L2'])
        
        valid = ~np.isnan(L2_errs) & (L2_errs > 0)
        if np.sum(valid) < 3:
            continue
        
        # Sliding window rate estimation
        p_v = p_vals[valid]
        e_v = L2_errs[valid]
        rates = []
        p_mid = []
        for i in range(len(p_v) - 1):
            if e_v[i] > 0 and e_v[i+1] > 0:
                r = -(np.log(e_v[i+1]) - np.log(e_v[i])) / (p_v[i+1] - p_v[i])
                rates.append(r)
                p_mid.append(0.5 * (p_v[i] + p_v[i+1]))
        
        if rates:
            ax.plot(p_mid, rates, '-o', label=f'k = {k}', markersize=5)
    
    ax.set_xlabel('p (midpoint)', fontsize=12)
    ax.set_ylabel('Estimated convergence rate σ', fontsize=12)
    ax.set_title('Estimated Exponential Rate: error ~ exp(-σp)', fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='black', linewidth=0.5)
    
    plt.tight_layout()
    out_path = os.path.join(output_dir, 'convergence_rates.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved {out_path}")
    return out_path


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(__file__))
    results_dir = os.path.join(base_dir, 'results')
    figures_dir = os.path.join(base_dir, 'figures')
    os.makedirs(figures_dir, exist_ok=True)
    
    # Plot all available results
    pw_file = os.path.join(results_dir, 'p_convergence_plane_wave.json')
    cw_file = os.path.join(results_dir, 'p_convergence_circular_wave.json')
    h_file = os.path.join(results_dir, 'h_convergence.json')
    
    if os.path.exists(pw_file):
        plot_p_convergence(pw_file, figures_dir)
        plot_convergence_rates(pw_file, figures_dir)
    
    if os.path.exists(cw_file):
        plot_p_convergence_circular(cw_file, figures_dir)
    
    if os.path.exists(h_file):
        plot_h_convergence(h_file, figures_dir)
    
    print("\nAll plots generated!")
