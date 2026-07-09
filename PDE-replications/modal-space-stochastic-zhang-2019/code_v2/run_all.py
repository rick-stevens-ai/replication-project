"""
Master runner: Run all 3 examples and collect results.
"""
import os, sys, json, time

SAVE_DIR = 'results'
os.makedirs(SAVE_DIR, exist_ok=True)

t0 = time.time()

print("="*70)
print("Zhang et al. 2019 — Parametric PINN Replication (DeepXDE v2)")
print("="*70)

# Example 1: Stochastic Advection
print("\n" + "="*70)
print("EXAMPLE 1: Stochastic Advection")
print("="*70)
from example1_parametric_pinn import train
ex1 = train(n_epochs=100000, net_type='modified_mlp', save_dir=SAVE_DIR)

# Example 2: Stochastic Burgers
print("\n" + "="*70)  
print("EXAMPLE 2: Stochastic Burgers (Time-Domain Decomposition)")
print("="*70)
from example2_burgers_pinn import train_all as train_burgers
ex2 = train_burgers(n_epochs_per_sub=20000, save_dir=SAVE_DIR)

# Example 3: Stochastic Reaction-Diffusion
print("\n" + "="*70)
print("EXAMPLE 3: Stochastic Reaction-Diffusion (Forward + Inverse)")
print("="*70)
from example3_reaction_diffusion_pinn import train_all as train_rd
ex3 = train_rd(save_dir=SAVE_DIR)

total = time.time() - t0
print(f"\n{'='*70}")
print(f"ALL DONE — Total wall time: {total:.0f}s ({total/3600:.1f}h)")
print(f"{'='*70}")

# Combine results
combined = {
    'example1_advection': ex1,
    'example2_burgers': ex2,
    'example3_reaction_diffusion': ex3,
    'total_wall_time': total,
}
with open(f'{SAVE_DIR}/all_results.json', 'w') as f:
    json.dump(combined, f, indent=2, default=str)
print(f"Combined results: {SAVE_DIR}/all_results.json")
