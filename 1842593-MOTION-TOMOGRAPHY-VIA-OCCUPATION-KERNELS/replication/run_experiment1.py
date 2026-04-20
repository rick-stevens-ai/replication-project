#!/usr/bin/env python3
"""
Experiment 1: Replicate simulated data experiment from the paper.

Flow field: Gaussian bump mixture (Eq 14)
Method: Iterative Algorithm 1
Kernel: Gaussian RBF with mu=1
Compare: Max error, mean error vs Table 1
"""

import sys
import os
import time
import numpy as np

sys.path.insert(0, '.')
from src.flow_fields import flow_field_paper, evaluate_on_grid
from src.trajectories import generate_random_trajectories
from src.reconstruction import FlowReconstructor, compute_errors
from src.plotting import (plot_comparison, plot_error_field, plot_flow_field)
import matplotlib.pyplot as plt

FIGURES_DIR = 'figures'
os.makedirs(FIGURES_DIR, exist_ok=True)

print("=" * 60)
print("Experiment 1: Simulated Flow Field Reconstruction")
print("=" * 60)

# Parameters matching the paper
N_TRAJS = 25       # Number of trajectories (paper uses ~30)
MU = 1.0            # Kernel width
T = 1.0             # Time horizon
SPEED = 1.0         # Vehicle speed
N_STEPS = 50        # Integration steps (Simpson's rule)
N_ITER = 10         # Algorithm iterations
NX, NY = 20, 20     # Grid resolution for evaluation
SEED = 42

print(f"\nParameters: N={N_TRAJS}, mu={MU}, T={T}, speed={SPEED}, iterations={N_ITER}")
print(f"Grid: {NX}x{NY}")

# Generate trajectories
print("\nGenerating trajectories...")
t0 = time.time()
true_trajs, dr_trajs, times_list, displacements, r0s, thetas = \
    generate_random_trajectories(N_TRAJS, flow_field_paper, 
                                 domain=(0.1, 0.9, 0.1, 0.9),
                                 T=T, n_steps=N_STEPS, speed=SPEED, seed=SEED)
print(f"  Done in {time.time()-t0:.1f}s")
print(f"  Mean displacement: {np.mean(np.linalg.norm(displacements, axis=1)):.4f}")

# True endpoints
true_endpoints = np.array([t[-1] for t in true_trajs])

# Run iterative reconstruction
print("\nRunning iterative motion tomography (Algorithm 1)...")
reconstructor = FlowReconstructor(mu=MU, lam=1e-6, n_steps=N_STEPS)
t0 = time.time()
F_hat, errors_hist = reconstructor.fit_iterative(
    r0s, np.full(N_TRAJS, SPEED), thetas, true_endpoints,
    T=T, n_iterations=N_ITER, verbose=True)
print(f"  Done in {time.time()-t0:.1f}s")

# Evaluate on grid
print("\nEvaluating on grid...")
X_true, Y_true, U_true, V_true = evaluate_on_grid(flow_field_paper, nx=NX, ny=NY)
X_est, Y_est, U_est, V_est = reconstructor.evaluate_on_grid(nx=NX, ny=NY)

# Compute errors
errors = compute_errors(flow_field_paper, F_hat, nx=NX, ny=NY)
print(f"\n--- Error Metrics ---")
print(f"  Max relative error:  {errors['max_error']:.5f}")
print(f"  Mean relative error: {errors['mean_error']:.5f}")
print(f"  RMSE:                {errors['rmse']:.5f}")
print(f"  Relative L2 error:   {errors['rel_l2_error']:.5f}")

print(f"\n--- Paper Table 1 (Algorithm 1) ---")
print(f"  Max Error:  0.25321")
print(f"  Mean Error: 0.025642")

# Figure 1: True vs Estimated flow fields
print("\nGenerating figures...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
plot_flow_field(X_true, Y_true, U_true, V_true, ax=ax1, 
                title='(a) True Flow Field with Trajectories',
                trajectories=true_trajs)
ax1.set_xlim(-0.2, 1.2)
ax1.set_ylim(-0.2, 1.2)

plot_flow_field(X_est, Y_est, U_est, V_est, ax=ax2,
                title='(b) Estimated Flow Field (Algorithm 1, 10 iter)')
ax2.set_xlim(-0.2, 1.2)
ax2.set_ylim(-0.2, 1.2)

plt.suptitle('Figure 1: Flow Field Reconstruction', fontsize=14)
plt.tight_layout()
plt.savefig(f'{FIGURES_DIR}/fig1_flow_comparison.png', dpi=150, bbox_inches='tight')
plt.close()

# Figure 3: Error field
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
U_err = U_true - U_est
V_err = V_true - V_est
err_mag = np.sqrt(U_err**2 + V_err**2)

ax1.quiver(X_true, Y_true, U_err, V_err, color='red')
ax1.set_title('(b) Error: Algorithm 1')
ax1.set_xlim(-0.2, 1.2)
ax1.set_ylim(-0.2, 1.2)
ax1.set_aspect('equal')

c = ax2.pcolormesh(X_true, Y_true, err_mag, cmap='hot', shading='auto')
plt.colorbar(c, ax=ax2)
ax2.set_title('Error Magnitude')
ax2.set_aspect('equal')

plt.suptitle('Figure 3: Error Field', fontsize=14)
plt.tight_layout()
plt.savefig(f'{FIGURES_DIR}/fig3_error_field.png', dpi=150, bbox_inches='tight')
plt.close()

print(f"\nFigures saved to {FIGURES_DIR}/")
print("\n" + "=" * 60)
print("Experiment 1 COMPLETE")
print("=" * 60)
