"""
Spectral Galerkin approximation for the 1D stochastic Burgers equation.

Reference: Blömker & Jentzen, "Galerkin approximations for the stochastic
Burgers equation", SIAM J. Numer. Anal. 51(1), 694–715, 2013.

Equation (4.16):
    dX_t = [ΔX_t - 60 · X_t · X'_t] dt + (1/3) dW_t

on (0,1) with Dirichlet BCs, initial condition X_0(x) = (6/5) sin(πx).

Basis functions: e_i(x) = √2 sin(iπx), i = 1,...,N
Eigenvalues: λ_i = π² i²

The Galerkin ODE system for coefficients a_i(t):
    da_i = [-λ_i a_i + F_i(a)] dt + (1/3) dβ_i

where F_i(a) = <-60 · u_N · u_N', e_i> computed pseudospectrally,
and β_i are independent standard Brownian motions.

Time integration: Accelerated exponential Euler (exact integration of linear part).
"""

import numpy as np
from typing import Optional


def eigenvalues(N: int) -> np.ndarray:
    """Eigenvalues of -Δ with Dirichlet BCs: λ_i = π²i², i=1..N."""
    return (np.pi * np.arange(1, N + 1)) ** 2


def initial_condition_coefficients(N: int) -> np.ndarray:
    """
    Galerkin coefficients for X_0(x) = (6/5) sin(πx).
    
    <X_0, e_i> = (6/5) <sin(πx), √2 sin(iπx)>
               = (6/5) · √2 · (1/2) δ_{i,1}  [orthogonality on (0,1)]
               = (6/(5√2)) · δ_{i,1}
               = (3√2/5) · δ_{i,1}
    """
    a0 = np.zeros(N)
    a0[0] = 6.0 / (5.0 * np.sqrt(2.0))  # = 3√2/5
    return a0


def nonlinear_term_pseudospectral(a: np.ndarray, N: int, M: int) -> np.ndarray:
    """
    Compute F_i = <-60 · u_N · u_N', e_i> using pseudospectral method.
    
    u_N(x) = Σ a_k √2 sin(kπx)
    u_N'(x) = Σ a_k √2 kπ cos(kπx)
    
    Evaluate on M collocation points, multiply pointwise, project back.
    
    Parameters
    ----------
    a : array of Galerkin coefficients, shape (N,)
    N : number of modes
    M : number of collocation points (should be >= 3N/2 for dealiasing)
    
    Returns
    -------
    F : array of shape (N,), the projected nonlinear term coefficients
    """
    # Collocation points: x_j = (j+0.5)/M for j=0,...,M-1 (interior points)
    # Using x_j = j/(M+1) for j=1,...,M is better for Dirichlet
    # Actually, for sine series, use DST-based approach or direct evaluation
    
    x = np.linspace(0, 1, M + 2)[1:-1]  # M interior points
    
    # Mode indices
    k = np.arange(1, N + 1)  # shape (N,)
    
    # Evaluate u_N(x) = Σ a_k √2 sin(kπx)
    # sin_matrix[j, k-1] = sin(k π x_j), shape (M, N)
    sin_matrix = np.sin(np.outer(x, k * np.pi))
    cos_matrix = np.cos(np.outer(x, k * np.pi))
    
    sqrt2 = np.sqrt(2.0)
    
    u = sqrt2 * sin_matrix @ a               # shape (M,)
    u_x = sqrt2 * cos_matrix @ (a * k * np.pi)  # shape (M,)
    
    # Pointwise product: f(x) = -60 · u(x) · u_x(x)
    f = -60.0 * u * u_x  # shape (M,)
    
    # Project back: F_i = <f, e_i> = √2 ∫_0^1 f(x) sin(iπx) dx
    # Approximate by trapezoidal rule on interior points
    dx = 1.0 / (M + 1)
    F = sqrt2 * (sin_matrix.T @ f) * dx  # shape (N,)
    
    return F


def nonlinear_term_analytic(a: np.ndarray, N: int) -> np.ndarray:
    """
    Compute F_i = <-60 · u_N · u_N', e_i> using analytic triple products.
    
    u_N · u_N' = (Σ a_j e_j)(Σ a_k e_k') 
    
    Using: e_j(x) = √2 sin(jπx), e_k'(x) = √2 kπ cos(kπx)
    
    Product: 2 a_j a_k kπ sin(jπx)cos(kπx)
           = a_j a_k kπ [sin((j+k)πx) + sin((j-k)πx)]
    
    Then F_i = √2 ∫ ... √2 sin(iπx) dx
             = 2 ∫ sin(iπx) · Σ a_j a_k kπ [sin((j+k)πx) + sin((j-k)πx)] dx
    
    Using orthogonality: ∫ sin(mπx) sin(nπx) dx = δ_{mn}/2
    
    F_i = Σ_{j,k} a_j a_k kπ [δ_{i,j+k} + δ_{i,|j-k|}·sign(j-k)]
    
    This is O(N²) which is fine for moderate N.
    """
    F = np.zeros(N)
    for j in range(1, N + 1):
        for k in range(1, N + 1):
            coeff = a[j-1] * a[k-1] * k * np.pi
            
            # Term from sin((j+k)πx): contributes to mode i = j+k
            idx = j + k
            if 1 <= idx <= N:
                F[idx - 1] += coeff  # δ_{i,j+k} contributes 1/2, times 2 = 1
            
            # Term from sin((j-k)πx): contributes to mode i = |j-k|
            diff = j - k
            if diff > 0 and diff <= N:
                F[diff - 1] += coeff  # sin((j-k)πx), positive
            elif diff < 0 and -diff <= N:
                F[-diff - 1] -= coeff  # sin((k-j)πx) with sign flip
            # diff == 0: sin(0) = 0, no contribution
    
    # The factor √2/2 accounts for:
    # - √2 from the basis function e_i in the projection <f, e_i>
    # - 1/2 from the orthogonality integral ∫ sin(mπx)sin(nπx)dx = δ_{mn}/2
    F *= -60.0 * np.sqrt(2.0) / 2.0
    return F


def solve_galerkin_exponential_euler(
    N: int,
    T: float = 0.05,
    n_steps: int = 200,
    c: float = -30.0,
    b_noise: float = 1.0 / 3.0,
    seed: Optional[int] = None,
    use_pseudospectral: bool = True,
    M_collocation: Optional[int] = None,
    rng: Optional[np.random.Generator] = None,
) -> tuple:
    """
    Solve the Galerkin-projected stochastic Burgers equation using
    the accelerated exponential Euler method.
    
    The scheme (exact integration of linear part):
        a_i^{n+1} = e^{-λ_i Δt} a_i^n + (1 - e^{-λ_i Δt})/λ_i · F_i(a^n) 
                     + b_noise · √Δt · e^{-λ_i Δt/2} · ξ_i^n / √λ_i  [approximate]
    
    Actually, for the noise term with exact integration:
        noise contribution = b_noise · ∫_0^{Δt} e^{-λ_i(Δt-s)} dβ_i(s)
    
    This integral has variance b_noise² · (1 - e^{-2λ_i Δt}) / (2λ_i).
    
    Parameters
    ----------
    N : int
        Number of Galerkin modes
    T : float
        Final time
    n_steps : int
        Number of time steps
    c : float
        Nonlinearity coefficient (default -30, giving -2c = 60 in front)
    b_noise : float
        Noise coefficient
    seed : int or None
        Random seed
    use_pseudospectral : bool
        Use pseudospectral method for nonlinear term (faster for large N)
    M_collocation : int or None
        Number of collocation points for pseudospectral (default 3*N)
    rng : numpy Generator (overrides seed if provided)
    
    Returns
    -------
    t_values : array of time points, shape (n_steps+1,)
    a_history : array of Galerkin coefficients, shape (n_steps+1, N)
    """
    if rng is None:
        rng = np.random.default_rng(seed)
    
    dt = T / n_steps
    lam = eigenvalues(N)  # shape (N,)
    
    # Precompute exponentials
    exp_neg_lam_dt = np.exp(-lam * dt)  # e^{-λ_i Δt}
    
    # For the nonlinear term: (1 - e^{-λ_i Δt}) / λ_i
    # Use Taylor expansion for small λ_i Δt to avoid numerical issues:
    # (1 - e^{-x})/x ≈ 1 - x/2 + x²/6 for small x
    phi1 = np.where(
        lam * dt > 1e-10,
        (1.0 - exp_neg_lam_dt) / lam,
        dt * (1.0 - lam * dt / 2.0)
    )
    
    # Noise variance: b² · (1 - e^{-2λΔt}) / (2λ)
    noise_std = b_noise * np.sqrt(
        np.where(
            lam * dt > 1e-10,
            (1.0 - np.exp(-2.0 * lam * dt)) / (2.0 * lam),
            dt * (1.0 - lam * dt)
        )
    )
    
    if M_collocation is None:
        M_collocation = max(3 * N, 256)
    
    # Initialize
    a = initial_condition_coefficients(N)
    
    t_values = np.linspace(0, T, n_steps + 1)
    a_history = np.zeros((n_steps + 1, N))
    a_history[0] = a.copy()
    
    for n in range(n_steps):
        # Compute nonlinear term
        if use_pseudospectral:
            F = nonlinear_term_pseudospectral(a, N, M_collocation)
        else:
            F = nonlinear_term_analytic(a, N)
        
        # Generate noise increments
        xi = rng.standard_normal(N)
        
        # Exponential Euler update
        a = exp_neg_lam_dt * a + phi1 * F + noise_std * xi
        
        a_history[n + 1] = a.copy()
    
    return t_values, a_history


def evaluate_solution(a: np.ndarray, x: np.ndarray) -> np.ndarray:
    """
    Evaluate the Galerkin solution u_N(x) = Σ a_k √2 sin(kπx).
    
    Parameters
    ----------
    a : array of coefficients, shape (N,) or (n_times, N)
    x : evaluation points, shape (M,)
    
    Returns
    -------
    u : solution values, shape (M,) or (n_times, M)
    """
    if a.ndim == 1:
        N = len(a)
        k = np.arange(1, N + 1)
        sin_matrix = np.sin(np.outer(x, k * np.pi))  # (M, N)
        return np.sqrt(2.0) * sin_matrix @ a
    else:
        n_times, N = a.shape
        k = np.arange(1, N + 1)
        sin_matrix = np.sin(np.outer(x, k * np.pi))  # (M, N)
        return np.sqrt(2.0) * (a @ sin_matrix.T)  # (n_times, M)


def compute_pathwise_error(a_ref: np.ndarray, a_test: np.ndarray, M_eval: int = 1000) -> float:
    """
    Compute pathwise L∞ error: max_t max_x |u_ref(t,x) - u_test(t,x)|.
    
    Following Eq. (4.20) in the paper.
    
    Parameters
    ----------
    a_ref : reference coefficients, shape (n_steps+1, N_ref)
    a_test : test coefficients, shape (n_steps+1, N_test)
    M_eval : number of spatial evaluation points
    
    Returns
    -------
    error : L∞ error
    """
    x = np.linspace(0, 1, M_eval + 2)[1:-1]
    
    n_steps = a_ref.shape[0]
    max_error = 0.0
    
    for n in range(n_steps):
        u_ref = evaluate_solution(a_ref[n], x)
        u_test = evaluate_solution(a_test[n], x)
        err = np.max(np.abs(u_ref - u_test))
        max_error = max(max_error, err)
    
    return max_error


if __name__ == "__main__":
    # Quick test
    N = 32
    t, a = solve_galerkin_exponential_euler(N, T=0.05, n_steps=200, seed=42)
    print(f"N={N}: final coefficients (first 5): {a[-1,:5]}")
    
    x = np.linspace(0, 1, 100)
    u_final = evaluate_solution(a[-1], x)
    print(f"Solution range at T=0.05: [{u_final.min():.4f}, {u_final.max():.4f}]")
