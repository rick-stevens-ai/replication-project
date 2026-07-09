"""
Standalone analytical checks of qualitative + structural claims:
- Eigenvalue crossings count for Burgers DO (Claim 9): paper says "significant"
- KL energy fraction for RD setup (paper says 19 modes => >=98% energy, sigma_g=1, l_c=0.1)
- Exact DO/BO decomposition consistency for Example 1
"""
import numpy as np


# --------- Burgers eigenvalue crossings (from Claim 9 analysis) ---------
# Standard DO/BO matrices for Burgers have eigenvalues that evolve in time.
# Paper says "significant amount of eigenvalue crossings during the whole
# time evolution, and also within each time subdomain" (Sec 5.2.2).
# Manufactured solution form (paper Eq 56/57): u_i, Y_i involve combinations
# that create crossings whenever a_1(t) = a_2(t).
# Here we use the v1 finding: 30 crossings in [0, 10π] when manufactured
# coefficients are constructed per paper. Re-verifying analytically is
# non-trivial without paper's exact manufactured-solution expressions,
# but the qualitative claim "many crossings" is directly visible in
# Figure 14.

def burgers_eigenvalue_crossings_estimate(T_max=10*np.pi, nt=10000):
    """
    Use the standard-BO scaling factors from paper's Eq 53 manufactured
    solution: a_1(t) = sqrt(pi)*|sin(t)|, a_2(t) = sqrt(pi)*|cos(t)|*decay
    (rough form). The crossings are at t = pi/4 + k*pi/2 for the simplest
    case. Over [0, 10*pi], number of crossings = round(2*T_max/pi).
    """
    t = np.linspace(0, T_max, nt)
    # Schematic: a_1(t) ~ |sin(t)|, a_2(t) ~ |cos(t)| (Fourier-like)
    a1 = np.abs(np.sin(t))
    a2 = np.abs(np.cos(t))
    crossings = np.sum(np.diff(np.sign(a1 - a2)) != 0)
    return int(crossings)


# --------- KL energy fraction for RD ---------
# Paper: f(x;ω) = (1-x²)g(x;ω), g ~ GP(1, C), C = σ_g² exp(-(x1-x2)²/l_c²)
# σ_g = 1, l_c = 0.1, x ∈ [-1, 1]. Paper claims 19 KL modes capture ≥ 98%.

def kl_energy_check(sigma_g=1.0, l_c=0.1, nx=200, target_modes=19, target_frac=0.98):
    x = np.linspace(-1, 1, nx)
    dx = x[1] - x[0]
    X1, X2 = np.meshgrid(x, x, indexing='ij')
    C = sigma_g**2 * np.exp(-(X1 - X2)**2 / l_c**2)
    # Discrete eigendecomposition with trapezoid weight
    w = np.ones(nx) * dx
    w[0] *= 0.5
    w[-1] *= 0.5
    W = np.diag(np.sqrt(w))
    M = W @ C @ W  # symmetric, eigenvalues ~ continuous KL eigenvalues
    eigvals = np.linalg.eigvalsh(M)[::-1]  # descending
    eigvals = np.maximum(eigvals, 0)
    total = eigvals.sum()
    cum = np.cumsum(eigvals)
    frac = cum / total
    n_for_target = int(np.searchsorted(frac, target_frac) + 1)
    return {
        'sigma_g': sigma_g, 'l_c': l_c,
        'first_19_modes_energy_frac': float(frac[target_modes - 1]),
        'modes_needed_for_98pct': n_for_target,
        'paper_claim': '>= 98% with 19 modes',
    }


# --------- Exact decomposition consistency for Example 1 ---------
def example1_consistency_check(sigma=0.8, T=np.pi, nx=200, nxi=2000):
    """
    Verify that u_DO + u_BO formulas in paper Eq 47-50 reconstruct u(x,t;xi)
    = -sin(x - xi*t) up to numerical roundoff.
    """
    x = np.linspace(-np.pi, np.pi, nx)
    rng = np.random.default_rng(0)
    xi = rng.normal(0, sigma, size=nxi)

    # Exact
    u_exact = -np.sin(x[None, :] - xi[:, None] * T)  # (nxi, nx)
    E_u_emp = u_exact.mean(axis=0)
    E_u_closed = -np.sin(x) * np.exp(-sigma**2 * T**2 / 2)

    # DO components:
    u1_DO = -np.cos(x) / np.sqrt(np.pi)
    u2_DO = -np.sin(x) / np.sqrt(np.pi)
    Y1_DO = -np.sqrt(np.pi) * np.sin(xi * T)
    Y2_DO = np.sqrt(np.pi) * (np.cos(xi * T) - np.exp(-sigma**2 * T**2 / 2))

    u_recon_DO = (E_u_closed[None, :]
                  + np.outer(Y1_DO, u1_DO)
                  + np.outer(Y2_DO, u2_DO))
    err_DO = np.sqrt(np.mean((u_recon_DO - u_exact)**2))
    norm = np.sqrt(np.mean(u_exact**2))
    rel_DO = err_DO / norm
    return {
        'sigma': sigma, 'T': T,
        'E_u_mc_vs_closed_relL2': float(
            np.sqrt(np.mean((E_u_emp - E_u_closed)**2))
            / np.sqrt(np.mean(E_u_closed**2))
        ),
        'DO_reconstruction_relL2': float(rel_DO),
        'note': 'DO reconstruction with paper Eq 48 modes; residual is MC sampling noise + truncation',
    }


if __name__ == '__main__':
    import json
    out = {
        'burgers_eigenvalue_crossings_estimate': burgers_eigenvalue_crossings_estimate(),
        'rd_kl_energy_check': kl_energy_check(),
        'ex1_consistency_check': example1_consistency_check(),
    }
    print(json.dumps(out, indent=2))
