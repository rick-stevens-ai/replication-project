"""
Run Examples 2 and 3 only (Example 1 already completed).
"""
import os, sys, json, time

SAVE_DIR = 'results'
os.makedirs(SAVE_DIR, exist_ok=True)

t0 = time.time()

print("="*70)
print("Zhang et al. 2019 — Examples 2 & 3 (Parametric PINN)")
print("="*70)

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
print(f"DONE — Total wall time: {total:.0f}s ({total/3600:.1f}h)")
print(f"{'='*70}")

combined = {
    'example2_burgers': ex2,
    'example3_reaction_diffusion': ex3,
    'total_wall_time': total,
}
with open(f'{SAVE_DIR}/remaining_results.json', 'w') as f:
    json.dump(combined, f, indent=2, default=str)
print(f"Results: {SAVE_DIR}/remaining_results.json")
