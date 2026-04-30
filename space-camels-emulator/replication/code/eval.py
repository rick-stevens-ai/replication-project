#!/usr/bin/env python3
"""
Evaluate the trained P(k) emulator:
1. Percent error in P(k) prediction vs CAMB ground truth
2. Speed comparison: CAMB vs emulator
3. Diagnostic plots

Outputs:
  ../figures/pred_vs_true.png
  ../figures/error_vs_k.png
  ../figures/speed_comparison.png
  ../results/eval_results.json
"""

import os
import sys
import json
import time
import numpy as np

import torch
import torch.nn as nn

# Ensure non-interactive backend
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ---- Paths ----
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
FIGURES_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
os.makedirs(FIGURES_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# Import CAMB for speed comparison
try:
    import camb
except ImportError:
    os.system(f"{sys.executable} -m pip install camb -q")
    import camb

# ---- Model definitions (must match training) ----
class PKEmulator(nn.Module):
    def __init__(self, n_input=6, n_output=50, hidden_dim=256, n_hidden=3, activation='gelu'):
        super().__init__()
        act_fn = nn.GELU if activation == 'gelu' else nn.ReLU
        layers = [nn.Linear(n_input, hidden_dim), act_fn()]
        for _ in range(n_hidden - 1):
            layers += [nn.Linear(hidden_dim, hidden_dim), act_fn()]
        layers.append(nn.Linear(hidden_dim, n_output))
        self.net = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.net(x)

class ResBlock(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(dim, dim),
            nn.GELU(),
            nn.Linear(dim, dim),
        )
        self.act = nn.GELU()
    
    def forward(self, x):
        return self.act(x + self.net(x))

class PKEmulatorV2(nn.Module):
    def __init__(self, n_input=6, n_output=50, hidden_dim=512, n_hidden=4):
        super().__init__()
        self.input_proj = nn.Sequential(
            nn.Linear(n_input, hidden_dim),
            nn.GELU(),
        )
        self.blocks = nn.Sequential(*[ResBlock(hidden_dim) for _ in range(n_hidden)])
        self.output_proj = nn.Linear(hidden_dim, n_output)
    
    def forward(self, x):
        x = self.input_proj(x)
        x = self.blocks(x)
        return self.output_proj(x)

def compute_pk_camb(omega_m, sigma_8, omega_b, h, n_s, w, k_bins):
    """Compute P(k) using CAMB (same as gen_dataset.py)."""
    ombh2 = omega_b * h**2
    omch2 = (omega_m - omega_b) * h**2
    
    pars = camb.CAMBparams()
    pars.set_cosmology(H0=h * 100, ombh2=ombh2, omch2=omch2)
    pars.set_dark_energy(w=w)
    pars.InitPower.set_params(As=2.1e-9, ns=n_s)
    pars.set_matter_power(redshifts=[0.0], kmax=k_bins[-1] * 1.2)
    pars.NonLinear = camb.model.NonLinear_none
    
    results = camb.get_results(pars)
    sigma8_camb = results.get_sigma8_0()
    kh, z, pk = results.get_matter_power_spectrum(
        minkh=k_bins[0], maxkh=k_bins[-1], npoints=200
    )
    pk_interp = np.interp(k_bins, kh, pk[0])
    rescale = (sigma_8 / sigma8_camb) ** 2
    pk_interp *= rescale
    return pk_interp

def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # Load data
    params = np.load(os.path.join(DATA_DIR, "params.npy"))
    pks = np.load(os.path.join(DATA_DIR, "pks.npy"))
    k_bins = np.load(os.path.join(DATA_DIR, "k_bins.npy"))
    
    # Load model checkpoint
    ckpt = torch.load(os.path.join(DATA_DIR, "emulator_best.pt"), map_location=device)
    
    param_mean = ckpt['param_mean']
    param_std = ckpt['param_std']
    logpk_mean = ckpt['logpk_mean']
    logpk_std = ckpt['logpk_std']
    test_idx = ckpt['test_idx']
    train_idx = ckpt['train_idx']
    
    # Load model (detect version)
    model_type = ckpt.get('model_type', 'v1')
    hdim = ckpt.get('hidden_dim', 256)
    nhid = ckpt.get('n_hidden', 3)
    if model_type == 'v2':
        model = PKEmulatorV2(n_input=6, n_output=len(k_bins), hidden_dim=hdim, n_hidden=nhid).to(device)
    else:
        model = PKEmulator(n_input=6, n_output=len(k_bins), hidden_dim=hdim, n_hidden=nhid).to(device)
    model.load_state_dict(ckpt['model_state_dict'])
    model.eval()
    
    print(f"Model loaded: {ckpt['n_params']:,} parameters")
    print(f"Test set: {len(test_idx)} cosmologies")
    
    # ---- 1. Accuracy Evaluation ----
    test_params = params[test_idx]
    test_pks = pks[test_idx]
    
    # Predict with emulator
    params_norm = (test_params - param_mean) / param_std
    X = torch.tensor(params_norm, dtype=torch.float32).to(device)
    
    with torch.no_grad():
        logpk_pred_norm = model(X).cpu().numpy()
    
    # Unnormalize
    logpk_pred = logpk_pred_norm * logpk_std + logpk_mean
    pk_pred = 10**logpk_pred
    
    # Percent error
    pct_err = np.abs(pk_pred - test_pks) / test_pks * 100  # (n_test, n_k)
    
    mean_err_per_k = pct_err.mean(axis=0)  # avg over cosmologies for each k
    p95_err_per_k = np.percentile(pct_err, 95, axis=0)
    
    overall_mean = pct_err.mean()
    overall_p95 = np.percentile(pct_err, 95)
    overall_max = pct_err.max()
    
    print(f"\n--- Accuracy (test set) ---")
    print(f"Mean percent error:  {overall_mean:.4f}%")
    print(f"95th percentile:     {overall_p95:.4f}%")
    print(f"Max percent error:   {overall_max:.4f}%")
    
    # ---- 2. Speed Comparison ----
    N_SPEED = min(100, len(test_idx))
    speed_params = test_params[:N_SPEED]
    
    # CAMB timing
    print(f"\nTiming CAMB on {N_SPEED} cosmologies...")
    t0 = time.time()
    for i in range(N_SPEED):
        omega_m, sigma_8, omega_b, h, n_s, w = speed_params[i]
        compute_pk_camb(omega_m, sigma_8, omega_b, h, n_s, w, k_bins)
    camb_total = time.time() - t0
    camb_per = camb_total / N_SPEED
    print(f"  CAMB: {camb_total:.2f}s total, {camb_per*1000:.1f}ms per cosmology")
    
    # Emulator timing
    print(f"Timing emulator on {N_SPEED} cosmologies...")
    speed_norm = (speed_params - param_mean) / param_std
    X_speed = torch.tensor(speed_norm, dtype=torch.float32).to(device)
    
    # Warm up
    with torch.no_grad():
        for _ in range(10):
            model(X_speed)
    
    # Time it (batch mode — realistic usage)
    t0 = time.time()
    n_repeats = 100
    with torch.no_grad():
        for _ in range(n_repeats):
            model(X_speed)
    emu_total = (time.time() - t0) / n_repeats
    emu_per = emu_total / N_SPEED
    print(f"  Emulator: {emu_total*1000:.3f}ms total, {emu_per*1000:.4f}ms per cosmology")
    
    speedup = camb_per / emu_per
    print(f"  Speedup: {speedup:.0f}x")
    
    # ---- 3. Diagnostic Plots ----
    
    # Colors
    colors = plt.cm.tab10(np.arange(5))
    
    # Plot 1: Pred vs True for 5 sample cosmologies
    fig, axes = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1]})
    
    sample_idx = np.linspace(0, len(test_idx)-1, 5, dtype=int)
    for i, si in enumerate(sample_idx):
        label_true = f"CAMB #{test_idx[si]}"
        label_pred = f"Emulator #{test_idx[si]}"
        axes[0].loglog(k_bins, test_pks[si], '-', color=colors[i], alpha=0.7, label=label_true)
        axes[0].loglog(k_bins, pk_pred[si], '--', color=colors[i], alpha=0.9, label=label_pred)
        
        # Residual
        res = (pk_pred[si] - test_pks[si]) / test_pks[si] * 100
        axes[1].semilogx(k_bins, res, '-', color=colors[i], alpha=0.8)
    
    axes[0].set_ylabel(r'$P(k)$ [(Mpc/h)$^3$]', fontsize=12)
    axes[0].set_title('Matter Power Spectrum: Emulator vs CAMB', fontsize=14)
    axes[0].legend(fontsize=7, ncol=2, loc='lower left')
    axes[0].grid(True, alpha=0.3)
    axes[0].set_xlim(k_bins[0], k_bins[-1])
    
    axes[1].axhline(0, color='k', lw=0.5)
    axes[1].axhspan(-1, 1, color='green', alpha=0.1, label='±1%')
    axes[1].set_xlabel(r'$k$ [h/Mpc]', fontsize=12)
    axes[1].set_ylabel('Error [%]', fontsize=12)
    axes[1].set_xlim(k_bins[0], k_bins[-1])
    axes[1].legend(fontsize=9)
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "pred_vs_true.png"), dpi=150)
    plt.close()
    print("\nSaved pred_vs_true.png")
    
    # Plot 2: Error vs k
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.semilogx(k_bins, mean_err_per_k, 'b-', lw=2, label='Mean % error')
    ax.fill_between(k_bins, np.zeros_like(k_bins), p95_err_per_k, 
                     alpha=0.2, color='red', label='95th percentile')
    ax.semilogx(k_bins, p95_err_per_k, 'r--', lw=1.5)
    ax.axhline(1.0, color='gray', ls=':', label='1% threshold')
    ax.set_xlabel(r'$k$ [h/Mpc]', fontsize=12)
    ax.set_ylabel('Percent Error', fontsize=12)
    ax.set_title('Emulator Error vs Wavenumber (Test Set)', fontsize=14)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(k_bins[0], k_bins[-1])
    ax.set_ylim(bottom=0)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "error_vs_k.png"), dpi=150)
    plt.close()
    print("Saved error_vs_k.png")
    
    # Plot 3: Speed comparison
    fig, ax = plt.subplots(figsize=(7, 5))
    methods = ['CAMB\n(Boltzmann solver)', 'Neural Network\nEmulator']
    times_ms = [camb_per * 1000, emu_per * 1000]
    bar_colors = ['#2196F3', '#FF5722']
    
    bars = ax.bar(methods, times_ms, color=bar_colors, width=0.5, edgecolor='black', lw=0.5)
    ax.set_ylabel('Time per cosmology [ms]', fontsize=12)
    ax.set_title(f'Speed Comparison ({speedup:.0f}× speedup)', fontsize=14)
    ax.set_yscale('log')
    
    # Add value labels
    for bar, val in zip(bars, times_ms):
        if val > 1:
            label = f'{val:.0f} ms'
        else:
            label = f'{val*1000:.0f} µs'
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.3,
                label, ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "speed_comparison.png"), dpi=150)
    plt.close()
    print("Saved speed_comparison.png")
    
    # ---- 4. Save results JSON ----
    results = {
        "mean_pct_err": float(overall_mean),
        "p95_pct_err": float(overall_p95),
        "max_pct_err": float(overall_max),
        "speedup_factor": float(speedup),
        "camb_ms_per_cosmology": float(camb_per * 1000),
        "emulator_ms_per_cosmology": float(emu_per * 1000),
        "n_test": int(len(test_idx)),
        "n_train": int(len(train_idx)),
        "n_model_params": int(ckpt['n_params']),
        "n_k_bins": int(len(k_bins)),
        "k_range": [float(k_bins[0]), float(k_bins[-1])],
        "mean_err_per_k": mean_err_per_k.tolist(),
        "p95_err_per_k": p95_err_per_k.tolist(),
    }
    
    with open(os.path.join(RESULTS_DIR, "eval_results.json"), 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nSaved eval_results.json")
    print(f"\n{'='*50}")
    print(f"SUMMARY")
    print(f"{'='*50}")
    print(f"Mean error:     {overall_mean:.4f}%")
    print(f"95th pct error: {overall_p95:.4f}%")
    print(f"Speedup:        {speedup:.0f}×")
    print(f"Model params:   {ckpt['n_params']:,}")

if __name__ == "__main__":
    main()
