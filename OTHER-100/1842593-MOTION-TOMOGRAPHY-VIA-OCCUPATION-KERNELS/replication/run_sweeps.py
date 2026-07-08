#!/usr/bin/env python3
"""
Parameter sweeps: kernel width (mu) and regularization (lambda).

Demonstrates:
- U-shaped error curves for mu and lambda
- Optimal parameter selection
"""

import sys
import os
import time
import numpy as np

sys.path.insert(0, '.')
from src.flow_fields import flow_field_paper
from src.trajectories import generate_random_trajectories
from src.reconstruction import FlowReconstructor, compute_errors
from src.plotting import plot_parameter_sweep
import matplotlib.pyplot as plt

FIGURES_DIR = 'figures'
os.makedirs(FIGURES_DIR, exist_ok=True)

print("=" * 60)
print("Parameter Sweep Study")
print("=" * 60)

N_TRAJS = 20
T = 1.0
SPEED = 1.0
N_STEPS = 50
N_ITER = 5
NX, NY = 15, 15
SEED = 42

# Generate trajectories once
true_trajs, dr_trajs, times_list, displacements, r0s, thetas = \
    generate_random_trajectories(N_TRAJS, flow_field_paper, 
                                 domain=(0.1, 0.9, 0.1, 0.9),
                                 T=T, n_steps=N_STEPS, speed=SPEED, seed=SEED)
true_endpoints = np.array([t[-1] for t in true_trajs])

# === Kernel width sweep ===
print("\n--- Kernel Width (mu) Sweep ---")
mu_values = [0.01, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0]
mu_errors = []

for mu in mu_values:
    t0 = time.time()
    rec = FlowReconstructor(mu=mu, lam=1e-6, n_steps=N_STEPS)
    F_hat, _ = rec.fit_iterative(
        r0s, np.full(N_TRAJS, SPEED), thetas, true_endpoints,
        T=T, n_iterations=N_ITER, verbose=False)
    errs = compute_errors(flow_field_paper, F_hat, nx=NX, ny=NY)
    mu_errors.append(errs['mean_error'])
    print(f"  mu={mu:.3f}: mean_error={errs['mean_error']:.6f} ({time.time()-t0:.1f}s)")

fig, ax = plt.subplots(figsize=(8, 6))
ax.semilogx(mu_values, mu_errors, 'bo-', linewidth=2, markersize=8)
ax.set_xlabel('Kernel Width (μ)', fontsize=12)
ax.set_ylabel('Mean Relative Error', fontsize=12)
ax.set_title('Error vs Kernel Width', fontsize=14)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'{FIGURES_DIR}/sweep_mu.png', dpi=150, bbox_inches='tight')
plt.close()

# === Regularization sweep ===
print("\n--- Regularization (lambda) Sweep ---")
lam_values = [0, 1e-10, 1e-8, 1e-6, 1e-4, 1e-2, 0.1, 1.0, 10.0]
lam_errors = []

for lam in lam_values:
    t0 = time.time()
    rec = FlowReconstructor(mu=1.0, lam=lam, n_steps=N_STEPS)
    F_hat, _ = rec.fit_iterative(
        r0s, np.full(N_TRAJS, SPEED), thetas, true_endpoints,
        T=T, n_iterations=N_ITER, verbose=False)
    errs = compute_errors(flow_field_paper, F_hat, nx=NX, ny=NY)
    lam_errors.append(errs['mean_error'])
    print(f"  lam={lam:.1e}: mean_error={errs['mean_error']:.6f} ({time.time()-t0:.1f}s)")

fig, ax = plt.subplots(figsize=(8, 6))
ax.semilogx([max(v, 1e-12) for v in lam_values], lam_errors, 'ro-', linewidth=2, markersize=8)
ax.set_xlabel('Regularization (λ)', fontsize=12)
ax.set_ylabel('Mean Relative Error', fontsize=12)
ax.set_title('Error vs Regularization', fontsize=14)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'{FIGURES_DIR}/sweep_lambda.png', dpi=150, bbox_inches='tight')
plt.close()

# === Number of trajectories sweep ===
print("\n--- Number of Trajectories Sweep ---")
n_traj_values = [5, 10, 15, 20, 30, 40, 50]
n_traj_errors = []

for nt in n_traj_values:
    t0 = time.time()
    tt, dt, tl, dp, r0, th = generate_random_trajectories(
        nt, flow_field_paper, domain=(0.1, 0.9, 0.1, 0.9),
        T=T, n_steps=N_STEPS, speed=SPEED, seed=SEED)
    te = np.array([t[-1] for t in tt])
    
    rec = FlowReconstructor(mu=1.0, lam=1e-6, n_steps=N_STEPS)
    F_hat, _ = rec.fit_iterative(
        r0, np.full(nt, SPEED), th, te,
        T=T, n_iterations=N_ITER, verbose=False)
    errs = compute_errors(flow_field_paper, F_hat, nx=NX, ny=NY)
    n_traj_errors.append(errs['mean_error'])
    print(f"  N={nt}: mean_error={errs['mean_error']:.6f} ({time.time()-t0:.1f}s)")

fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(n_traj_values, n_traj_errors, 'gs-', linewidth=2, markersize=8)
ax.set_xlabel('Number of Trajectories', fontsize=12)
ax.set_ylabel('Mean Relative Error', fontsize=12)
ax.set_title('Error vs Number of Trajectories', fontsize=14)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'{FIGURES_DIR}/sweep_n_trajs.png', dpi=150, bbox_inches='tight')
plt.close()

print(f"\nFigures saved to {FIGURES_DIR}/")
print("=" * 60)
print("Parameter sweeps COMPLETE")
print("=" * 60)
