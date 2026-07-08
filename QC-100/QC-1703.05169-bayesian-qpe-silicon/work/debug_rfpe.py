"""Quick diagnosis: does RFPE converge for an easier phi and prior?"""
import math, numpy as np
from rfpe_sim import rfpe_run

# Case 1: easy phi = 0.3, prior N(0.5, 0.2)  (well within [0,1))
r = rfpe_run(phi_true=0.3, n_steps=50, mu0=0.5, sigma0=0.2, n_particles=1000, seed=42)
print(f"Case 1 (phi=0.3, prior mu=0.5 sd=0.2): mu={r.final_mu:.6f}, sigma={r.final_sigma:.3e}, err={r.final_error:.3e}")
print(f"  Ms: {r.M_history[:20]}")
print(f"  outs: {r.outcome_history[:20]}")

# Case 2: paper's phi_true_norm ~0.7757, prior N(0.5, 0.5)
phi_true = 4.8741/(2*math.pi)
r = rfpe_run(phi_true=phi_true, n_steps=50, mu0=0.5, sigma0=0.5, n_particles=1000, seed=42)
print(f"Case 2 (phi={phi_true:.4f}, prior mu=0.5 sd=0.5): mu={r.final_mu:.6f}, sigma={r.final_sigma:.3e}, err={r.final_error:.3e}")
print(f"  Ms: {r.M_history[:20]}")
print(f"  outs: {r.outcome_history[:20]}")
print(f"  mus[:10]: {[f'{x:.3f}' for x in r.mu_history[:10]]}")
print(f"  sigmas[:10]: {[f'{x:.3f}' for x in r.sigma_history[:10]]}")

# Case 3: paper's phi_true_norm ~0.7757, prior N(0.5, 0.5), but cap M so first step is M=1
r = rfpe_run(phi_true=phi_true, n_steps=50, mu0=0.5, sigma0=0.5, n_particles=2000, seed=42, M_cap=None)
print(f"Case 3 (n_particles=2000): mu={r.final_mu:.6f}, sigma={r.final_sigma:.3e}, err={r.final_error:.3e}")

# Case 4: same but prior std=0.25 (tighter, less aliasing pressure)
r = rfpe_run(phi_true=phi_true, n_steps=50, mu0=0.75, sigma0=0.25, n_particles=1000, seed=42)
print(f"Case 4 (prior mu=0.75 sd=0.25): mu={r.final_mu:.6f}, sigma={r.final_sigma:.3e}, err={r.final_error:.3e}")

# Case 5: same as case 2 but seed variation
for seed in [1,2,3,4,5]:
    r = rfpe_run(phi_true=phi_true, n_steps=50, mu0=0.5, sigma0=0.5, n_particles=1000, seed=seed)
    print(f"Case 5 seed={seed}: mu={r.final_mu:.6f}, err={r.final_error:.3e}, sigma={r.final_sigma:.3e}")
