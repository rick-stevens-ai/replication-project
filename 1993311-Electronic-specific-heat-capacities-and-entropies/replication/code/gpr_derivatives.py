"""
Gaussian Process Regression for noisy thermodynamic data.

Implements the paper's method:
- Fit E(β) or E(T) with GPR using composite kernel (RBF + Matérn 5/2 + Matérn 3/2)
- Extract C_V(T) via analytic derivative of GP predictive mean
- Extract S(T) via numerical integration of C_V/T

Reference: Malone et al., J. Chem. Phys. (2020)
"""

import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import (
    RBF, Matern, WhiteKernel, ConstantKernel as C
)
from scipy.integrate import cumulative_trapezoid
from typing import Optional, Tuple


def build_paper_kernel(length_scale_init: float = 1.0,
                       constant_init: float = 1.0):
    """
    Build the composite kernel from the paper:
    K = C₁ × RBF + C₂ × Matérn(5/2) + C₃ × Matérn(3/2)

    Each component has its own amplitude (ConstantKernel) and length scale.
    """
    k_rbf = C(constant_init) * RBF(length_scale=length_scale_init)
    k_m52 = C(constant_init) * Matern(length_scale=length_scale_init, nu=2.5)
    k_m32 = C(constant_init) * Matern(length_scale=length_scale_init, nu=1.5)

    return k_rbf + k_m52 + k_m32


def fit_gpr(x: np.ndarray, y: np.ndarray,
            y_err: Optional[np.ndarray] = None,
            kernel=None,
            n_restarts: int = 10,
            alpha: Optional[float] = None) -> GaussianProcessRegressor:
    """
    Fit Gaussian Process Regressor to data.

    Parameters
    ----------
    x : input (β or T), shape (n,)
    y : target (E), shape (n,)
    y_err : standard errors on y (if available, used for alpha)
    kernel : GP kernel (default: paper's composite kernel)
    n_restarts : number of optimizer restarts
    alpha : noise variance (if y_err not given)

    Returns
    -------
    gpr : fitted GaussianProcessRegressor
    """
    if kernel is None:
        kernel = build_paper_kernel()

    X = x.reshape(-1, 1)

    if y_err is not None:
        # Heteroscedastic: alpha = variance at each point
        alpha_arr = y_err**2
    elif alpha is not None:
        alpha_arr = alpha
    else:
        # Add WhiteKernel for noise estimation
        kernel = kernel + WhiteKernel(noise_level=0.01, noise_level_bounds=(1e-10, 1.0))
        alpha_arr = 1e-10  # near-zero jitter

    gpr = GaussianProcessRegressor(
        kernel=kernel,
        alpha=alpha_arr,
        n_restarts_optimizer=n_restarts,
        normalize_y=True
    )
    gpr.fit(X, y)

    return gpr


def gpr_predict(gpr: GaussianProcessRegressor,
                x_pred: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    GPR prediction with uncertainty.

    Returns
    -------
    mean : predictive mean
    std : predictive standard deviation
    """
    X_pred = x_pred.reshape(-1, 1)
    mean, std = gpr.predict(X_pred, return_std=True)
    return mean, std


def gpr_derivative(gpr: GaussianProcessRegressor,
                   x_pred: np.ndarray,
                   dx: float = 1e-5) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute derivative of GP predictive mean using finite differences
    on the GP itself (not the data). This is effectively analytic since
    the GP is a smooth function.

    For a true analytic derivative, we'd differentiate the kernel.
    Here we use a very fine finite difference on the smooth GP prediction,
    which is numerically equivalent.

    Parameters
    ----------
    gpr : fitted GP
    x_pred : prediction points
    dx : step size for numerical derivative of GP (not the data!)

    Returns
    -------
    dydx : derivative of GP mean
    d2ydx2 : second derivative of GP mean
    """
    X_plus = (x_pred + dx).reshape(-1, 1)
    X_minus = (x_pred - dx).reshape(-1, 1)
    X_plus2 = (x_pred + 2*dx).reshape(-1, 1)
    X_minus2 = (x_pred - 2*dx).reshape(-1, 1)
    X_center = x_pred.reshape(-1, 1)

    y_plus = gpr.predict(X_plus)
    y_minus = gpr.predict(X_minus)
    y_center = gpr.predict(X_center)
    y_plus2 = gpr.predict(X_plus2)
    y_minus2 = gpr.predict(X_minus2)

    # Central difference (4th order)
    dydx = (-y_plus2 + 8*y_plus - 8*y_minus + y_minus2) / (12 * dx)

    # Second derivative (4th order)
    d2ydx2 = (-y_plus2 + 16*y_plus - 30*y_center + 16*y_minus - y_minus2) / (12 * dx**2)

    return dydx, d2ydx2


def gpr_cv_from_beta(gpr_beta: GaussianProcessRegressor,
                     beta: np.ndarray) -> np.ndarray:
    """
    Compute C_V from GP fit of E(β):
    C_V(β) = -β² dE/dβ

    Parameters
    ----------
    gpr_beta : GP fitted to E(β) data
    beta : inverse temperature points

    Returns
    -------
    cv : specific heat capacity (in units of k_B)
    """
    dEdβ, _ = gpr_derivative(gpr_beta, beta)
    return -beta**2 * dEdβ


def gpr_cv_from_T(gpr_T: GaussianProcessRegressor,
                  T: np.ndarray) -> np.ndarray:
    """
    Compute C_V from GP fit of E(T):
    C_V(T) = dE/dT

    Parameters
    ----------
    gpr_T : GP fitted to E(T) data
    T : temperature points

    Returns
    -------
    cv : specific heat capacity (in units of k_B)
    """
    dEdT, _ = gpr_derivative(gpr_T, T)
    return dEdT


def compute_entropy_from_cv(T: np.ndarray, cv: np.ndarray) -> np.ndarray:
    """
    Compute entropy by integrating C_V/T from T=0:
    S(T) = ∫₀ᵀ C_V(T')/T' dT'

    Uses trapezoid rule (as in the paper).
    S(T=0) = 0 boundary condition.

    Parameters
    ----------
    T : temperature array (must be sorted ascending, T[0] > 0)
    cv : specific heat at each T

    Returns
    -------
    S : entropy array
    """
    integrand = cv / T
    S_cumulative = cumulative_trapezoid(integrand, T, initial=0.0)
    return S_cumulative


class TwoRegimeGPR:
    """
    Paper's two-domain strategy:
    - Fit E(β) for low-T regime (high β)
    - Fit E(T) for high-T regime
    - Combine with crossover
    """

    def __init__(self, crossover_T: float = 1.0):
        self.crossover_T = crossover_T
        self.gpr_beta = None  # GP in β-domain
        self.gpr_T = None     # GP in T-domain

    def fit(self, beta: np.ndarray, E: np.ndarray,
            E_err: Optional[np.ndarray] = None,
            E0: Optional[float] = None):
        """
        Fit both domains.

        Parameters
        ----------
        beta : inverse temperatures
        E : energy values
        E_err : error bars
        E0 : ground state energy (added as anchor at β→∞)
        """
        T = 1.0 / beta

        # Low-T (high β) regime: fit E(β) for β > 1/crossover_T
        mask_low_T = T <= self.crossover_T * 1.5  # some overlap
        beta_low = beta[mask_low_T]
        E_low = E[mask_low_T]
        err_low = E_err[mask_low_T] if E_err is not None else None

        # Add ground state anchor
        if E0 is not None:
            beta_anchor = np.array([50.0])  # large β
            beta_low = np.concatenate([beta_low, beta_anchor])
            E_low = np.concatenate([E_low, np.array([E0])])
            if err_low is not None:
                err_low = np.concatenate([err_low, np.array([1e-8])])

        self.gpr_beta = fit_gpr(beta_low, E_low, err_low)

        # High-T (low β) regime: fit E(T) for T > crossover_T
        mask_high_T = T >= self.crossover_T * 0.5  # some overlap
        T_high = T[mask_high_T]
        E_high = E[mask_high_T]
        err_high = E_err[mask_high_T] if E_err is not None else None

        self.gpr_T = fit_gpr(T_high, E_high, err_high)

    def predict_energy(self, T_pred: np.ndarray) -> np.ndarray:
        """Piecewise prediction."""
        E_pred = np.zeros_like(T_pred)
        mask_low = T_pred <= self.crossover_T
        mask_high = T_pred > self.crossover_T

        if np.any(mask_low):
            beta_pred = 1.0 / T_pred[mask_low]
            E_pred[mask_low] = self.gpr_beta.predict(beta_pred.reshape(-1, 1))

        if np.any(mask_high):
            E_pred[mask_high] = self.gpr_T.predict(T_pred[mask_high].reshape(-1, 1))

        return E_pred

    def predict_cv(self, T_pred: np.ndarray) -> np.ndarray:
        """Piecewise C_V prediction."""
        cv = np.zeros_like(T_pred)
        mask_low = T_pred <= self.crossover_T
        mask_high = T_pred > self.crossover_T

        if np.any(mask_low):
            beta_pred = 1.0 / T_pred[mask_low]
            cv[mask_low] = gpr_cv_from_beta(self.gpr_beta, beta_pred)

        if np.any(mask_high):
            cv[mask_high] = gpr_cv_from_T(self.gpr_T, T_pred[mask_high])

        return cv


if __name__ == '__main__':
    from exact_models import hubbard_2site_eigenvalues, exact_energy, generate_noisy_energy

    eigs = hubbard_2site_eigenvalues(t=1.0, U=4.0)
    beta = np.linspace(0.1, 10.0, 100)
    E_noisy, sigma = generate_noisy_energy(eigs, beta, noise_scale=0.02, noise_type='dmqmc_like')

    gpr = fit_gpr(beta, E_noisy, sigma)
    E_pred, E_std = gpr_predict(gpr, beta)

    print(f"GPR fit RMSE: {np.sqrt(np.mean((E_pred - exact_energy(eigs, beta))**2)):.6f}")
    print(f"Kernel: {gpr.kernel_}")
