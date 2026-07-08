"""
Exact analytical thermodynamics for benchmark quantum systems.

Systems implemented:
1. Two-site Hubbard model (half-filling, 2 electrons)
2. Simple harmonic oscillator (for validation)
3. Generic: given a set of energy eigenvalues, compute E(T), C_V(T), S(T) exactly.

Reference: Malone et al., J. Chem. Phys. (2020) — Eq. (1)-(5).
"""

import numpy as np
from typing import Optional


def hubbard_2site_eigenvalues(t: float = 1.0, U: float = 4.0) -> np.ndarray:
    """
    Exact eigenvalues of the 2-site Hubbard model at half-filling (2 electrons).

    H = -t sum_{sigma} (c†_{1,sigma} c_{2,sigma} + h.c.) + U sum_i n_{i,up} n_{i,down}

    The 6 two-electron states in (site1, site2) basis split into sectors:
    - S_z = +1: |↑↑⟩ → E = 0 (1 state)
    - S_z = -1: |↓↓⟩ → E = 0 (1 state)
    - S_z = 0: 4 states, Hamiltonian in basis {|↑↓,0⟩, |0,↑↓⟩, |↑,↓⟩, |↓,↑⟩}
      eigenvalues: 0, U, (U ± sqrt(U² + 16t²))/2

    Parameters
    ----------
    t : hopping parameter
    U : on-site repulsion

    Returns
    -------
    eigenvalues : array of all eigenvalues (6 values, with degeneracies)
    """
    discriminant = np.sqrt(U**2 + 16 * t**2)
    E_minus = (U - discriminant) / 2  # ground state (singlet)
    E_plus = (U + discriminant) / 2   # excited singlet
    E_zero = 0.0   # triplet (3-fold degenerate: S_z = -1, 0, +1)
    E_U = U        # another singlet

    # 6 eigenvalues total: E_minus (1), E_zero (3), E_U (1), E_plus (1)
    return np.array([E_minus, E_zero, E_zero, E_zero, E_U, E_plus])


def partition_function(eigenvalues: np.ndarray, beta: np.ndarray) -> np.ndarray:
    """Compute Z(β) = Σ_i exp(-β E_i)."""
    # Shape: (len(beta), len(eigenvalues))
    beta = np.atleast_1d(beta)
    exponents = -np.outer(beta, eigenvalues)
    return np.sum(np.exp(exponents), axis=1)


def exact_energy(eigenvalues: np.ndarray, beta: np.ndarray) -> np.ndarray:
    """Exact thermal energy E(β) = Σ_i E_i exp(-β E_i) / Z(β)."""
    beta = np.atleast_1d(beta)
    exponents = -np.outer(beta, eigenvalues)
    boltzmann = np.exp(exponents)
    Z = np.sum(boltzmann, axis=1)
    return np.sum(eigenvalues[None, :] * boltzmann, axis=1) / Z


def exact_energy_squared(eigenvalues: np.ndarray, beta: np.ndarray) -> np.ndarray:
    """Exact ⟨E²⟩(β) = Σ_i E_i² exp(-β E_i) / Z(β)."""
    beta = np.atleast_1d(beta)
    exponents = -np.outer(beta, eigenvalues)
    boltzmann = np.exp(exponents)
    Z = np.sum(boltzmann, axis=1)
    return np.sum(eigenvalues[None, :]**2 * boltzmann, axis=1) / Z


def exact_cv(eigenvalues: np.ndarray, beta: np.ndarray) -> np.ndarray:
    """
    Exact specific heat C_V(β) = β² (⟨E²⟩ - ⟨E⟩²).
    In units where k_B = 1.
    """
    beta = np.atleast_1d(beta)
    E = exact_energy(eigenvalues, beta)
    E2 = exact_energy_squared(eigenvalues, beta)
    return beta**2 * (E2 - E**2)


def exact_entropy(eigenvalues: np.ndarray, beta: np.ndarray) -> np.ndarray:
    """
    Exact entropy S(β) = -Σ_i p_i ln(p_i) where p_i = exp(-β E_i)/Z.
    In units where k_B = 1.
    """
    beta = np.atleast_1d(beta)
    exponents = -np.outer(beta, eigenvalues)
    boltzmann = np.exp(exponents)
    Z = np.sum(boltzmann, axis=1, keepdims=True)
    p = boltzmann / Z
    # Avoid log(0) by masking
    log_p = np.where(p > 1e-300, np.log(p), 0.0)
    return -np.sum(p * log_p, axis=1)


def generate_noisy_energy(eigenvalues: np.ndarray, beta: np.ndarray,
                          noise_scale: float = 0.01,
                          noise_type: str = 'proportional',
                          rng: Optional[np.random.Generator] = None) -> tuple:
    """
    Generate synthetic noisy E(β) data mimicking DMQMC stochastic error.

    Parameters
    ----------
    eigenvalues : energy eigenvalues of the system
    beta : inverse temperatures
    noise_scale : base noise magnitude
    noise_type : 'proportional' — σ ∝ noise_scale × |E_range|
                 'constant' — σ = noise_scale
                 'dmqmc_like' — noise that increases with β (mimics real DMQMC)
    rng : numpy random generator

    Returns
    -------
    E_noisy : noisy energy values
    sigma : noise standard deviations at each point
    """
    if rng is None:
        rng = np.random.default_rng(42)

    E_exact = exact_energy(eigenvalues, beta)
    E_range = np.max(E_exact) - np.min(E_exact)

    if noise_type == 'proportional':
        sigma = noise_scale * np.abs(E_range) * np.ones_like(beta)
    elif noise_type == 'constant':
        sigma = noise_scale * np.ones_like(beta)
    elif noise_type == 'dmqmc_like':
        # DMQMC noise grows with β because signal (dE/dβ) shrinks
        # while stochastic error stays roughly constant in absolute terms.
        # At low β (high T), good signal. At high β (low T), noise dominates.
        beta_ref = np.median(beta)
        sigma = noise_scale * np.abs(E_range) * (1.0 + 0.5 * (beta / beta_ref))
    else:
        raise ValueError(f"Unknown noise_type: {noise_type}")

    noise = rng.normal(0, sigma)
    E_noisy = E_exact + noise

    return E_noisy, sigma


def hydrogen_chain_eigenvalues(n_sites: int = 4) -> np.ndarray:
    """
    Simple tight-binding chain (non-interacting) as another benchmark.
    E_k = -2t cos(k π / (N+1)) for k = 1,...,N
    Fill with n_sites/2 electrons (each level doubly occupied).

    For thermodynamics, we enumerate all many-body states.
    But for n_sites > 6 this gets expensive. For small chains, use brute force.
    """
    if n_sites > 8:
        raise ValueError("Too many sites for brute-force enumeration")

    t = 1.0  # hopping
    # Single-particle energies
    sp_energies = np.array([-2*t * np.cos(k * np.pi / (n_sites + 1))
                            for k in range(1, n_sites + 1)])

    # For 2 electrons (1 up, 1 down), many-body energies:
    n_electrons = 2
    from itertools import combinations
    # Each electron picks one spatial orbital; for 2 electrons (different spin),
    # all pairs of spatial orbitals are allowed
    mb_energies = []
    for i in range(n_sites):
        for j in range(n_sites):
            mb_energies.append(sp_energies[i] + sp_energies[j])

    return np.array(mb_energies)


if __name__ == '__main__':
    # Quick test
    eigs = hubbard_2site_eigenvalues(t=1.0, U=4.0)
    print(f"Hubbard 2-site eigenvalues (t=1, U=4): {eigs}")
    print(f"Ground state: {np.min(eigs):.6f}")

    beta_test = np.array([0.1, 1.0, 5.0, 10.0])
    T_test = 1.0 / beta_test
    print(f"\nβ = {beta_test}")
    print(f"T = {T_test}")
    print(f"E(β) = {exact_energy(eigs, beta_test)}")
    print(f"C_V(β) = {exact_cv(eigs, beta_test)}")
    print(f"S(β) = {exact_entropy(eigs, beta_test)}")
