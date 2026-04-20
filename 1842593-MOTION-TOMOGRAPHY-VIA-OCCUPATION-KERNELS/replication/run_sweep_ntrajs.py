#!/usr/bin/env python3
"""Number of trajectories sweep only."""
import sys, os, time
import numpy as np
sys.path.insert(0, '.')
from src.flow_fields import flow_field_paper
from src.trajectories import generate_random_trajectories
from src.reconstruction import FlowReconstructor, compute_errors
import matplotlib.pyplot as plt

FIGURES_DIR = 'figures'
os.makedirs(FIGURES_DIR, exist_ok=True)

N_STEPS = 50
T = 1.0
SPEED = 1.0
N_ITER = 5
NX, NY = 15, 15
SEED = 42

print("--- Number of Trajectories Sweep ---")
n_traj_values = [5, 10, 15, 20, 25, 30, 40]
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
print("Done!")
