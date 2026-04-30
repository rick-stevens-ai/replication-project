#!/usr/bin/env python3
"""
Evaluation script: compares PFGM vs Diffusion baseline on 2D toy data.

Computes:
1. Wasserstein distance between generated samples and true distribution
2. Step-size robustness comparison (varying dt / n_steps)
3. Generates figures: sample_quality.png, step_size_robustness.png
4. Saves JSON metrics
"""

import torch
import numpy as np
import json
import os
import argparse
import sys
from pathlib import Path
from scipy.stats import wasserstein_distance as wd1d
from scipy.spatial.distance import cdist

# Import our models
from pfgm import (PFGMNet, make_mog_data, sample_pfgm, sample_pfgm_euler_raw,
                   train_pfgm, sample_prior)
from diffusion_baseline import (ScoreNet, sample_diffusion, sample_diffusion_euler,
                                 train_diffusion)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


# ── Metrics ──────────────────────────────────────────────────────────────

def sliced_wasserstein_distance(samples_a, samples_b, n_projections=200, seed=0):
    """
    Sliced Wasserstein distance (SWD) between two 2D point clouds.
    Projects onto random 1D directions and averages the 1D Wasserstein distances.
    """
    rng = np.random.RandomState(seed)
    dim = samples_a.shape[1]

    # Random projection directions
    directions = rng.randn(n_projections, dim)
    directions /= np.linalg.norm(directions, axis=1, keepdims=True)

    distances = []
    for d in directions:
        proj_a = samples_a @ d
        proj_b = samples_b @ d
        distances.append(wd1d(proj_a, proj_b))

    return np.mean(distances)


def mode_coverage(samples, centers, radius=0.8):
    """
    Fraction of true modes that have at least one sample nearby.
    """
    covered = 0
    for c in centers:
        dists = np.linalg.norm(samples - c, axis=1)
        if np.any(dists < radius):
            covered += 1
    return covered / len(centers)


def mode_quality_stats(samples, centers, std=0.3):
    """Per-mode statistics: count, mean distance to mode center."""
    stats = []
    for i, c in enumerate(centers):
        dists = np.linalg.norm(samples - c, axis=1)
        assigned = dists < 3 * std  # within 3-sigma
        stats.append({
            'mode': i,
            'center': c.tolist(),
            'n_assigned': int(assigned.sum()),
            'mean_dist': float(dists[assigned].mean()) if assigned.any() else float('inf'),
        })
    return stats


# ── Plotting ─────────────────────────────────────────────────────────────

def plot_sample_quality(train_data, pfgm_samples, diff_samples,
                        swd_pfgm, swd_diff, save_path):
    """Side-by-side comparison: true data, PFGM samples, diffusion samples."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    common_kwargs = dict(s=2, alpha=0.4)
    lim = 5.5

    # True data
    axes[0].scatter(train_data[:5000, 0], train_data[:5000, 1],
                    c='steelblue', **common_kwargs)
    axes[0].set_title('True Distribution\n(8-mode MoG)', fontsize=13)
    axes[0].set_xlim(-lim, lim); axes[0].set_ylim(-lim, lim)
    axes[0].set_aspect('equal')
    axes[0].grid(True, alpha=0.3)

    # PFGM
    axes[1].scatter(pfgm_samples[:5000, 0], pfgm_samples[:5000, 1],
                    c='darkorange', **common_kwargs)
    axes[1].set_title(f'PFGM Samples\nSWD = {swd_pfgm:.4f}', fontsize=13)
    axes[1].set_xlim(-lim, lim); axes[1].set_ylim(-lim, lim)
    axes[1].set_aspect('equal')
    axes[1].grid(True, alpha=0.3)

    # Diffusion
    axes[2].scatter(diff_samples[:5000, 0], diff_samples[:5000, 1],
                    c='seagreen', **common_kwargs)
    axes[2].set_title(f'Diffusion (VE-SDE) Samples\nSWD = {swd_diff:.4f}', fontsize=13)
    axes[2].set_xlim(-lim, lim); axes[2].set_ylim(-lim, lim)
    axes[2].set_aspect('equal')
    axes[2].grid(True, alpha=0.3)

    plt.suptitle('Sample Quality Comparison: PFGM vs Score-Based Diffusion (2D MoG)',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"    Saved: {save_path}")


def plot_step_size_robustness(results, save_path):
    """Plot SWD vs number of Euler steps for both models."""
    fig, ax = plt.subplots(1, 1, figsize=(9, 6))

    steps = results['n_steps_list']
    pfgm_swds = results['pfgm_swd']
    pfgm_lin_swds = results.get('pfgm_linear_swd', None)
    diff_swds = results['diffusion_swd']

    ax.plot(steps, pfgm_swds, 'o-', color='darkorange', linewidth=2.5,
            markersize=8, label='PFGM (log-z, Eq. 6)', zorder=5)
    if pfgm_lin_swds:
        ax.plot(steps, pfgm_lin_swds, 'D--', color='goldenrod', linewidth=1.5,
                markersize=6, label='PFGM (linear-z Euler)', zorder=4, alpha=0.7)
    ax.plot(steps, diff_swds, 's-', color='seagreen', linewidth=2.5,
            markersize=8, label='Diffusion (VE prob. flow ODE)', zorder=5)

    ax.set_xlabel('Number of Function Evaluations (NFE)', fontsize=12)
    ax.set_ylabel('Sliced Wasserstein Distance ↓', fontsize=12)
    ax.set_title('Step-Size Robustness: PFGM vs Diffusion on 2D MoG\n'
                 '(Paper claim: PFGM more robust to step size)',
                 fontsize=13, fontweight='bold')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.legend(fontsize=11, loc='upper right')
    ax.grid(True, alpha=0.3, which='both')

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"    Saved: {save_path}")


# ── Main evaluation pipeline ────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='PFGM vs Diffusion Evaluation')
    parser.add_argument('--epochs', type=int, default=300)
    parser.add_argument('--n_train', type=int, default=20000)
    parser.add_argument('--n_samples', type=int, default=5000)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--device', type=str, default='auto')
    parser.add_argument('--results_dir', type=str, default='../results')
    parser.add_argument('--figures_dir', type=str, default='../figures')
    parser.add_argument('--skip_train', action='store_true',
                        help='Load existing models instead of retraining')
    args = parser.parse_args()

    if args.device == 'auto':
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
    else:
        device = args.device

    torch.manual_seed(args.seed)
    np.random.seed(args.seed)

    os.makedirs(args.results_dir, exist_ok=True)
    os.makedirs(args.figures_dir, exist_ok=True)

    print("=" * 70)
    print("  PFGM vs Diffusion — Full Evaluation on 2D Mixture of Gaussians")
    print("=" * 70)

    # ── Data ─────────────────────────────────────────────────────────────
    print(f"\n[1/6] Generating training data ({args.n_train} samples)...")
    data = make_mog_data(n_samples=args.n_train, seed=args.seed)

    # True mode centers for coverage analysis
    n_modes = 8
    radius = 3.0
    angles = np.linspace(0, 2 * np.pi, n_modes, endpoint=False)
    centers = np.stack([radius * np.cos(angles), radius * np.sin(angles)], axis=1)

    # Reference samples from the true distribution (for SWD baseline)
    ref_data = make_mog_data(n_samples=args.n_samples, seed=args.seed + 1000)

    # ── Train or Load Models ─────────────────────────────────────────────
    pfgm_path = os.path.join(args.results_dir, 'pfgm_model.pt')
    diff_path = os.path.join(args.results_dir, 'diffusion_model.pt')

    if args.skip_train and os.path.exists(pfgm_path) and os.path.exists(diff_path):
        print("\n[2/6] Loading pre-trained models...")
        pfgm_model = PFGMNet(data_dim=2, hidden=256, n_layers=4).to(device)
        pfgm_ckpt = torch.load(pfgm_path, map_location=device, weights_only=False)
        pfgm_model.load_state_dict(pfgm_ckpt['model_state_dict'])

        diff_model = ScoreNet(data_dim=2, hidden=256, n_layers=4).to(device)
        diff_ckpt = torch.load(diff_path, map_location=device, weights_only=False)
        diff_model.load_state_dict(diff_ckpt['model_state_dict'])
    else:
        print("\n[2/6] Training PFGM...")
        pfgm_model, pfgm_losses = train_pfgm(
            data, epochs=args.epochs, batch_size=512,
            lr=1e-3, device=device
        )
        torch.save({'model_state_dict': pfgm_model.state_dict(),
                     'losses': pfgm_losses}, pfgm_path)

        print("\n[3/6] Training Diffusion baseline...")
        diff_model, diff_losses = train_diffusion(
            data, epochs=args.epochs, batch_size=512,
            lr=1e-3, device=device
        )
        torch.save({'model_state_dict': diff_model.state_dict(),
                     'losses': diff_losses}, diff_path)

    # ── Generate high-quality samples (fine discretization) ──────────────
    print(f"\n[4/6] Generating samples with fine discretization...")

    pfgm_samples = sample_pfgm(pfgm_model, n_samples=args.n_samples,
                                device=device, z_max=10.0, z_min=1e-3, dt=0.005)
    diff_samples = sample_diffusion(diff_model, n_samples=args.n_samples,
                                     n_steps=2000, device=device)

    swd_pfgm = sliced_wasserstein_distance(pfgm_samples, ref_data)
    swd_diff = sliced_wasserstein_distance(diff_samples, ref_data)

    cov_pfgm = mode_coverage(pfgm_samples, centers)
    cov_diff = mode_coverage(diff_samples, centers)

    print(f"    PFGM  — SWD: {swd_pfgm:.4f}, Mode coverage: {cov_pfgm:.2f}")
    print(f"    Diff  — SWD: {swd_diff:.4f}, Mode coverage: {cov_diff:.2f}")

    # ── Sample quality figure ────────────────────────────────────────────
    print(f"\n[5/6] Generating figures...")
    plot_sample_quality(data, pfgm_samples, diff_samples,
                        swd_pfgm, swd_diff,
                        os.path.join(args.figures_dir, 'sample_quality.png'))

    # ── Step-size robustness ─────────────────────────────────────────────
    print(f"\n[6/6] Step-size robustness experiment...")

    # Different numbers of Euler steps (fewer steps → larger dt → harder)
    n_steps_list = [10, 20, 50, 100, 200, 500, 1000]

    pfgm_swd_list = []
    pfgm_linear_swd_list = []
    diff_swd_list = []

    z_max_val = 10.0
    z_min_val = 1e-3

    for ns in n_steps_list:
        print(f"    n_steps = {ns}...")

        # PFGM with log-z parameterization (Eq. 6 — paper's recommended)
        dt_logz = np.log(z_max_val / z_min_val) / ns
        pfgm_s = sample_pfgm(pfgm_model, n_samples=args.n_samples,
                             device=device, z_max=z_max_val, z_min=z_min_val,
                             dt=dt_logz, use_log_z=True)
        swd_p = sliced_wasserstein_distance(pfgm_s, ref_data)
        pfgm_swd_list.append(swd_p)

        # PFGM with linear-z Euler (for comparison)
        pfgm_s_lin = sample_pfgm_euler_raw(pfgm_model, n_samples=args.n_samples,
                                            n_steps=ns, device=device,
                                            z_max=z_max_val, z_min=z_min_val)
        swd_pl = sliced_wasserstein_distance(pfgm_s_lin, ref_data)
        pfgm_linear_swd_list.append(swd_pl)

        # Diffusion: Euler, n_steps
        diff_s = sample_diffusion_euler(diff_model, n_samples=args.n_samples,
                                         n_steps=ns, device=device)
        swd_d = sliced_wasserstein_distance(diff_s, ref_data)
        diff_swd_list.append(swd_d)

        print(f"      PFGM(log-z) SWD={swd_p:.4f}, PFGM(linear) SWD={swd_pl:.4f}, Diff SWD={swd_d:.4f}")

    robustness_results = {
        'n_steps_list': n_steps_list,
        'pfgm_swd': pfgm_swd_list,
        'pfgm_linear_swd': pfgm_linear_swd_list,
        'diffusion_swd': diff_swd_list,
    }

    plot_step_size_robustness(robustness_results,
                              os.path.join(args.figures_dir, 'step_size_robustness.png'))

    # ── Save all metrics ─────────────────────────────────────────────────
    metrics = {
        'sample_quality': {
            'pfgm': {
                'sliced_wasserstein': float(swd_pfgm),
                'mode_coverage': float(cov_pfgm),
                'mode_stats': mode_quality_stats(pfgm_samples, centers),
            },
            'diffusion': {
                'sliced_wasserstein': float(swd_diff),
                'mode_coverage': float(cov_diff),
                'mode_stats': mode_quality_stats(diff_samples, centers),
            },
        },
        'step_size_robustness': {
            'n_steps': n_steps_list,
            'pfgm_logz_swd': [float(x) for x in pfgm_swd_list],
            'pfgm_linear_swd': [float(x) for x in pfgm_linear_swd_list],
            'diffusion_swd': [float(x) for x in diff_swd_list],
            'pfgm_dt_logz': [float(np.log(10.0 / 1e-3) / ns) for ns in n_steps_list],
            'pfgm_dt_linear': [float(10.0 / ns) for ns in n_steps_list],
            'diffusion_dt': [float(1.0 / ns) for ns in n_steps_list],
        },
        'experimental_setup': {
            'data': '8-mode Mixture of Gaussians, radius=3.0, std=0.3',
            'n_train': args.n_train,
            'n_eval_samples': args.n_samples,
            'epochs': args.epochs,
            'seed': args.seed,
            'device': device,
            'metric': 'Sliced Wasserstein Distance (200 projections)',
        },
    }

    metrics_path = os.path.join(args.results_dir, 'metrics.json')
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"\n    Metrics saved to {metrics_path}")

    # Save samples
    np.save(os.path.join(args.results_dir, 'pfgm_samples.npy'), pfgm_samples)
    np.save(os.path.join(args.results_dir, 'diffusion_samples.npy'), diff_samples)
    np.save(os.path.join(args.results_dir, 'train_data.npy'), data)

    # ── Summary ──────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("  RESULTS SUMMARY")
    print("=" * 70)
    print(f"\n  Sample Quality (fine discretization):")
    print(f"    PFGM:      SWD = {swd_pfgm:.4f}, Coverage = {cov_pfgm:.0%}")
    print(f"    Diffusion: SWD = {swd_diff:.4f}, Coverage = {cov_diff:.0%}")
    print(f"\n  Step-Size Robustness (SWD at coarse → fine steps):")
    print(f"    {'Steps':>6s} | {'PFGM(logz)':>10s} | {'PFGM(lin)':>10s} | {'Diffusion':>10s} | {'D/P ratio':>10s}")
    print(f"    {'-'*6}-+-{'-'*10}-+-{'-'*10}-+-{'-'*10}-+-{'-'*10}")
    for i, ns in enumerate(n_steps_list):
        ratio_logz = diff_swd_list[i] / max(pfgm_swd_list[i], 1e-10)
        print(f"    {ns:6d} | {pfgm_swd_list[i]:8.4f} | {pfgm_linear_swd_list[i]:8.4f} | {diff_swd_list[i]:10.4f} | {ratio_logz:10.2f}x")

    print(f"\n  Figures: {args.figures_dir}/")
    print(f"  Metrics: {metrics_path}")
    print("=" * 70)


if __name__ == '__main__':
    main()
