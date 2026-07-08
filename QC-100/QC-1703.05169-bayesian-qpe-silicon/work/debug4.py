"""Try different N particles and see if convergence improves."""
import math, numpy as np
from rfpe_sim import rfpe_run, _wrap_to_pi

Phi_true = 4.8741
for N in [1000, 5000, 20000, 100000]:
    errs = []
    sigs = []
    for seed in range(20):
        r = rfpe_run(Phi_true, 50, math.pi, math.pi, n_particles=N, seed=seed)
        errs.append(abs(_wrap_to_pi(r.final_mu - Phi_true)))
        sigs.append(r.final_sigma)
    print(f"N={N:6d}: median err={np.median(errs):.3e}, median sigma={np.median(sigs):.3e}")

# Test the underlying scaling: does sigma decrease exponentially with N particles?
print("\nOne long run at N=20000:")
r = rfpe_run(Phi_true, 100, math.pi, math.pi, n_particles=20000, seed=7)
print(f"  final err = {abs(_wrap_to_pi(r.final_mu - Phi_true)):.3e}, sigma = {r.final_sigma:.3e}")
print(f"  M history [::10] = {r.M_history[::10]}")
print(f"  sigma history [::10] = {[f'{x:.2e}' for x in r.sigma_history[::10]]}")
