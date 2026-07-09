"""Verify pseudospectral vs analytic nonlinear term computation."""

import numpy as np
from galerkin_burgers import (
    nonlinear_term_pseudospectral,
    nonlinear_term_analytic,
    initial_condition_coefficients,
)

# Test with a known set of coefficients
np.random.seed(42)

for N in [4, 8, 16, 32]:
    a = np.random.randn(N) * 0.5
    
    F_analytic = nonlinear_term_analytic(a, N)
    
    # Test with increasing collocation points
    for M_factor in [3, 5, 10]:
        M = M_factor * N
        F_pseudo = nonlinear_term_pseudospectral(a, N, M)
        rel_err = np.linalg.norm(F_analytic - F_pseudo) / (np.linalg.norm(F_analytic) + 1e-15)
        print(f"N={N:3d}, M={M:5d}: rel error = {rel_err:.2e}")
    print()

# Also verify that the two methods give the same solution trajectory
from galerkin_burgers import solve_galerkin_exponential_euler

N = 16
rng1 = np.random.default_rng(123)
rng2 = np.random.default_rng(123)

t1, a1 = solve_galerkin_exponential_euler(N, T=0.05, n_steps=200, rng=rng1, use_pseudospectral=False)
t2, a2 = solve_galerkin_exponential_euler(N, T=0.05, n_steps=200, rng=rng2, use_pseudospectral=True, M_collocation=10*N)

max_diff = np.max(np.abs(a1 - a2))
print(f"Trajectory max diff (analytic vs pseudo, N={N}): {max_diff:.2e}")
