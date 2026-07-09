"""Run only Example 3 (Reaction-Diffusion) with fixed FD solver."""
import os, json, time

SAVE_DIR = 'results'
os.makedirs(SAVE_DIR, exist_ok=True)

t0 = time.time()

print("="*70)
print("EXAMPLE 3: Stochastic Reaction-Diffusion (Forward + Inverse)")
print("="*70)
from example3_reaction_diffusion_pinn import train_all as train_rd
ex3 = train_rd(save_dir=SAVE_DIR)

total = time.time() - t0
print(f"\nTotal wall time: {total:.0f}s ({total/3600:.1f}h)")

with open(f'{SAVE_DIR}/example3_result.json', 'w') as f:
    json.dump(ex3, f, indent=2, default=str)
print(f"Results: {SAVE_DIR}/example3_result.json")
