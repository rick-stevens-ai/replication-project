#!/usr/bin/env python3
"""
Generate publication-quality figures from training results.
Can run locally (no GPU needed) or on uicgpu.
"""

import os
import sys
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Style
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'legend.fontsize': 10,
    'figure.dpi': 150,
    'savefig.dpi': 200,
    'savefig.bbox': 'tight',
})


def plot_shock_comparison(results_dir, fig_dir):
    """
    Figure 1: Side-by-side comparison of MSE vs Godunov predictions
    for each test case, overlaid with FV reference.
    """
    pred_file = os.path.join(results_dir, 'predictions.npz')
    if not os.path.exists(pred_file):
        print(f"  Predictions file not found: {pred_file}")
        return
    
    preds = np.load(pred_file, allow_pickle=True)
    x = preds['x']
    
    test_names = ['strong_step', 'bump_to_shock', 'n_wave']
    titles = ['Strong Shock (Step IC)', 'Bump → Shock', 'N-Wave (Sine IC)']
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    
    for i, (name, title) in enumerate(zip(test_names, titles)):
        ax = axes[i]
        
        u_ref = preds[f'{name}_ref']
        u_mse = preds[f'{name}_mse']
        u_god = preds[f'{name}_god']
        
        ax.plot(x, u_ref, 'k-', linewidth=2.0, label='FV Reference (Godunov)', alpha=0.9)
        ax.plot(x, u_mse, 'b--', linewidth=1.5, label='NN + MSE Loss', alpha=0.8)
        ax.plot(x, u_god, 'r-', linewidth=1.5, label='NN + Godunov Loss', alpha=0.8)
        
        ax.set_xlabel('x')
        ax.set_ylabel('u(x, T)')
        ax.set_title(title)
        ax.legend(loc='best', framealpha=0.9)
        ax.grid(True, alpha=0.3)
    
    fig.suptitle('Comparison of Neural PDE Solvers: MSE vs Godunov Loss\n'
                 '1D Inviscid Burgers Equation', fontsize=14, y=1.02)
    plt.tight_layout()
    
    outpath = os.path.join(fig_dir, 'shock_comparison.png')
    fig.savefig(outpath, dpi=200, bbox_inches='tight')
    print(f"  Saved: {outpath}")
    plt.close(fig)


def plot_shock_detail(results_dir, fig_dir):
    """
    Figure 1b: Zoom into shock region for the strong_step case.
    """
    pred_file = os.path.join(results_dir, 'predictions.npz')
    if not os.path.exists(pred_file):
        return
    
    preds = np.load(pred_file, allow_pickle=True)
    x = preds['x']
    
    u_ref = preds['strong_step_ref']
    u_mse = preds['strong_step_mse']
    u_god = preds['strong_step_god']
    
    # Find shock location (where reference has steepest gradient)
    grad = np.abs(np.diff(u_ref))
    shock_idx = np.argmax(grad)
    x_shock = x[shock_idx]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))
    
    # Full view
    ax1.plot(x, u_ref, 'k-', linewidth=2.0, label='FV Reference')
    ax1.plot(x, u_mse, 'b--', linewidth=1.5, label='NN + MSE')
    ax1.plot(x, u_god, 'r-', linewidth=1.5, label='NN + Godunov')
    ax1.axvspan(x_shock - 0.05, x_shock + 0.05, alpha=0.15, color='gray')
    ax1.set_xlabel('x')
    ax1.set_ylabel('u')
    ax1.set_title('Full Domain')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Zoomed shock region
    mask = (x > x_shock - 0.05) & (x < x_shock + 0.05)
    ax2.plot(x[mask], u_ref[mask], 'k-', linewidth=2.5, label='FV Reference')
    ax2.plot(x[mask], u_mse[mask], 'b--', linewidth=2.0, label='NN + MSE', marker='o', 
             markersize=3, alpha=0.8)
    ax2.plot(x[mask], u_god[mask], 'r-', linewidth=2.0, label='NN + Godunov', marker='s', 
             markersize=3, alpha=0.8)
    ax2.set_xlabel('x')
    ax2.set_ylabel('u')
    ax2.set_title('Shock Region (Zoomed)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    fig.suptitle('Shock Resolution: Strong Step Case', fontsize=13)
    plt.tight_layout()
    
    outpath = os.path.join(fig_dir, 'shock_detail.png')
    fig.savefig(outpath, dpi=200, bbox_inches='tight')
    print(f"  Saved: {outpath}")
    plt.close(fig)


def plot_loss_curves(results_dir, fig_dir):
    """
    Figure 2: Training and validation loss curves.
    """
    mse_file = os.path.join(results_dir, 'losses_mse.npz')
    god_file = os.path.join(results_dir, 'losses_godunov.npz')
    
    if not os.path.exists(mse_file) or not os.path.exists(god_file):
        print("  Loss files not found")
        return
    
    mse_data = np.load(mse_file)
    god_data = np.load(god_file)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    
    # Training losses
    ax = axes[0]
    epochs = np.arange(1, len(mse_data['train']) + 1)
    ax.semilogy(epochs, mse_data['train'], 'b-', alpha=0.8, label='MSE Loss (train)')
    ax.semilogy(epochs, god_data['train'], 'r-', alpha=0.8, label='Godunov Loss (train)')
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Loss')
    ax.set_title('Training Loss')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Validation losses (MSE metric for fair comparison)
    ax = axes[1]
    ax.semilogy(epochs, mse_data['val'], 'b-', alpha=0.8, label='MSE model (val MSE)')
    ax.semilogy(epochs, god_data['val'], 'r-', alpha=0.8, label='Godunov model (val MSE)')
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Validation MSE')
    ax.set_title('Validation Loss (MSE metric)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    fig.suptitle('Training Convergence', fontsize=13)
    plt.tight_layout()
    
    outpath = os.path.join(fig_dir, 'loss_curves.png')
    fig.savefig(outpath, dpi=200, bbox_inches='tight')
    print(f"  Saved: {outpath}")
    plt.close(fig)


def plot_error_bars(results_dir, fig_dir):
    """
    Figure 3: Bar chart of L1, TV error for each test case.
    """
    mse_file = os.path.join(results_dir, 'results_mse.json')
    god_file = os.path.join(results_dir, 'results_godunov.json')
    
    if not os.path.exists(mse_file) or not os.path.exists(god_file):
        print("  Result JSON files not found")
        return
    
    with open(mse_file) as f:
        mse_res = json.load(f)
    with open(god_file) as f:
        god_res = json.load(f)
    
    test_names = list(mse_res['test_results'].keys())
    
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
    
    for i, metric in enumerate(['L1', 'Linf', 'TV_relative_error']):
        ax = axes[i]
        mse_vals = [mse_res['test_results'][name][metric] for name in test_names]
        god_vals = [god_res['test_results'][name][metric] for name in test_names]
        
        x_pos = np.arange(len(test_names))
        width = 0.35
        
        bars1 = ax.bar(x_pos - width/2, mse_vals, width, label='MSE Loss', color='steelblue', alpha=0.8)
        bars2 = ax.bar(x_pos + width/2, god_vals, width, label='Godunov Loss', color='indianred', alpha=0.8)
        
        ax.set_xlabel('Test Case')
        ax.set_ylabel(metric.replace('_', ' '))
        ax.set_title(metric.replace('_', ' ').title())
        ax.set_xticks(x_pos)
        ax.set_xticklabels([n.replace('_', '\n') for n in test_names], fontsize=9)
        ax.legend()
        ax.grid(True, axis='y', alpha=0.3)
    
    fig.suptitle('Error Metrics: MSE vs Godunov Loss', fontsize=13)
    plt.tight_layout()
    
    outpath = os.path.join(fig_dir, 'error_bars.png')
    fig.savefig(outpath, dpi=200, bbox_inches='tight')
    print(f"  Saved: {outpath}")
    plt.close(fig)


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results_dir = os.path.join(base_dir, 'results')
    fig_dir = os.path.join(base_dir, 'figures')
    os.makedirs(fig_dir, exist_ok=True)
    
    print("Generating figures...")
    print("\n1. Shock comparison plots")
    plot_shock_comparison(results_dir, fig_dir)
    
    print("\n2. Shock detail (zoomed)")
    plot_shock_detail(results_dir, fig_dir)
    
    print("\n3. Loss curves")
    plot_loss_curves(results_dir, fig_dir)
    
    print("\n4. Error bar charts")
    plot_error_bars(results_dir, fig_dir)
    
    print(f"\nAll figures saved to {fig_dir}/")


if __name__ == '__main__':
    main()
