"""
Example 1 reference check (no training):
- Verify exact formulas via Monte Carlo (1e6 samples, paper sigma=0.8)
- Report L2 norms of E[u] and Var[u] at T=pi
- Establish how close GHQ-32 approximation is to MC truth
- Establish what 'relative L2' a paper-quality result must hit in absolute terms

This anchors the agreement-gap discussion: paper claims 1.96% E[u] rel L2 at T=pi
on a function whose L2 norm at T=pi is exp(-sigma^2 pi^2/2) * ||sin|| ~ 0.0425 * pi
~ 0.0425 * sqrt(pi). So absolute error must be sub-1e-3.
"""
import numpy as np

MU = 0.0
SIGMA = 0.8
X_LO, X_HI = -np.pi, np.pi
T = np.pi

x = np.linspace(X_LO, X_HI, 1000)

# Exact closed-form (paper Eq 46)
E_exact = -np.sin(x) * np.exp(-SIGMA**2 * T**2 / 2.0)
# Exact variance: E[u^2] - E[u]^2 = 0.5*(1 - cos(2x)*exp(-2 sigma^2 t^2)) - E[u]^2
Var_exact = 0.5 * (1.0 - np.cos(2.0 * x) * np.exp(-2.0 * SIGMA**2 * T**2)) - E_exact**2

# MC reference
N = 1_000_000
rng = np.random.default_rng(0)
xi = rng.normal(MU, SIGMA, size=N)
# u(x,t,xi) = -sin(x - xi*t); E[u] = mean over xi for each x
# Compute streaming to avoid (N, len(x)) matrix
E_mc = np.zeros_like(x)
E2_mc = np.zeros_like(x)
chunk = 50000
total = 0
for start in range(0, N, chunk):
    sz = min(chunk, N - start)
    xib = xi[start:start+sz][:, None]  # (sz, 1)
    u = -np.sin(x[None, :] - xib * T)  # (sz, len(x))
    E_mc += u.sum(axis=0)
    E2_mc += (u**2).sum(axis=0)
    total += sz
E_mc /= total
E2_mc /= total
Var_mc = E2_mc - E_mc**2

# GHQ reference
GHN = 32
nodes, weights = np.polynomial.hermite.hermgauss(GHN)
xi_nodes = np.sqrt(2.0) * SIGMA * nodes + MU
w_norm = weights / np.sqrt(np.pi)
E_ghq = np.zeros_like(x)
E2_ghq = np.zeros_like(x)
for k, xk in enumerate(xi_nodes):
    u = -np.sin(x - xk * T)
    E_ghq += w_norm[k] * u
    E2_ghq += w_norm[k] * u * u
Var_ghq = E2_ghq - E_ghq**2

def relL2(p, e):
    return np.sqrt(np.mean((p - e)**2)) / np.sqrt(np.mean(e**2))

print(f"sigma={SIGMA}, T={T}")
print(f"||E_exact|| (L2)   = {np.sqrt(np.mean(E_exact**2)):.6e}")
print(f"||Var_exact|| (L2) = {np.sqrt(np.mean(Var_exact**2)):.6e}")
print(f"E   rel L2: MC vs exact   = {relL2(E_mc, E_exact)*100:.4f}%")
print(f"Var rel L2: MC vs exact   = {relL2(Var_mc, Var_exact)*100:.4f}%")
print(f"E   rel L2: GHQ vs exact  = {relL2(E_ghq, E_exact)*100:.4e}%")
print(f"Var rel L2: GHQ vs exact  = {relL2(Var_ghq, Var_exact)*100:.4e}%")

# What does the paper's 1.96% E[u] relL2 mean in absolute terms?
abs_eps = 0.0196 * np.sqrt(np.mean(E_exact**2))
print(f"\nPaper 1.96% E[u] rel L2 at T=pi => absolute RMS error ~ {abs_eps:.4e}")
abs_eps_v = 0.0011 * np.sqrt(np.mean(Var_exact**2))
print(f"Paper 0.11% Var rel L2 at T=pi => absolute RMS error ~ {abs_eps_v:.4e}")
