#!/usr/bin/env python3
"""
Convergence study: Replicate Figure 4 from the paper.

Tests three flow fields:
1. Gaussian bump mixture (Eq 14)
2. Linear: f1=x2, f2=-0.2*x1
3. Constant: f1=0.2, f2=0.1

Shows mean error vs iteration for each.
"""

import sys
import os
import time
import numpy as np

sys.path.insert(0, '.')
from src.flow_fields import flow_field_paper, flow_field_linear, flow_field_constant
from src.trajectories import generate_random_trajectories
from src.reconstruction import FlowReconstructor, compute_errors
from src.plotting import plot_convergence
import matplotlib.pyplot as plt

FIGURES_DIR = 'figures'
os.makedirs(FIGURES_DIR, exist_ok=True)

print("=" * 60)
print("Convergence Study (Figure 4)")
print("=" * 60)

N_TRAJS = 20
MU = 1.0
T = 1.0
SPEED = 1.0
N_STEPS = 50
N_ITER = 10
NX, NY = 15, 15
SEED = 42

flow_fields = {
    'Flow Field 1 (Gaussian mixture)': flow_field_paper,
    'Flow Field 2 (Linear)': flow_field_linear,
    'Flow Field 3 (Constant)': flow_field_constant,
}

all_errors = {}

for name, ff in flow_fields.items():
    print(f"\n--- {name} ---")
    t0 = time.time()
    
    true_trajs, dr_trajs, times_list, displacements, r0s, thetas = \
        generate_random_trajectories(N_TRAJS, ff, domain=(0.1, 0.9, 0.1, 0.9),
                                     T=T, n_steps=N_STEPS, speed=SPEED, seed=SEED)
    true_endpoints = np.array([t[-1] for t in true_trajs])
    
    # Run iterative reconstruction, compute error after each iteration
    mean_errors_per_iter = []
    F_hat = lambda x: np.zeros(2)
    
    reconstructor = FlowReconstructor(mu=MU, lam=1e-6, n_steps=N_STEPS)
    
    for it in range(N_ITER):
        # Single iteration step
        F_hat_new, _ = reconstructor.fit_iterative(
            r0s, np.full(N_TRAJS, SPEED), thetas, true_endpoints,
            T=T, n_iterations=it+1, verbose=False)
        
        # Compute error
        errs = compute_errors(ff, F_hat_new, nx=NX, ny=NY)
        mean_errors_per_iter.append(errs['mean_error'])
        print(f"  Iter {it+1}: mean_error = {errs['mean_error']:.6f}")
    
    all_errors[name] = mean_errors_per_iter
    print(f"  Done in {time.time()-t0:.1f}s")

# Plot convergence (Figure 4)
fig, ax = plt.subplots(1, 1, figsize=(8, 6))
markers = ['o', 'o', 's']
colors = ['blue', 'red', 'red']
fillstyles = ['full', 'none', 'full']

for idx, (label, errors) in enumerate(all_errors.items()):
    ax.plot(range(1, len(errors)+1), errors,
            marker=markers[idx], color=colors[idx],
            fillstyle=fillstyles[idx],
            label=label, linewidth=2, markersize=8)

ax.set_xlabel('Number of Iterations', fontsize=12)
ax.set_ylabel('Mean Error', fontsize=12)
ax.set_title('Figure 4: Convergence of Algorithm 1', fontsize=14)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xlim(0, N_ITER + 1)

plt.tight_layout()
plt.savefig(f'{FIGURES_DIR}/fig4_convergence.png', dpi=150, bbox_inches='tight')
plt.close()

print(f"\nFigure saved to {FIGURES_DIR}/fig4_convergence.png")
print("=" * 60)
print("Convergence study COMPLETE")
print("=" * 60)
