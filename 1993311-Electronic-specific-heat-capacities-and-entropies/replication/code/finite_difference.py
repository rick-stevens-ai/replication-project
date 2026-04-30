"""
Finite-difference and cubic spline baselines for derivative estimation.

These are the "bad" baselines from the paper that GPR improves upon.
Implements:
1. NumPy gradient (central differences) — paper's FD baseline
2. SciPy CubicSpline with analytic derivative — paper's spline baseline

Reference: Malone et al., J. Chem. Phys. (2020), Section II.C
"""

import numpy as np
from scipy.interpolate import CubicSpline
from scipy.integrate import cumulative_trapezoid
from typing import Optional, Tuple


def fd_derivative(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Central finite difference derivative (numpy gradient).
    This is exactly what the paper uses as the FD baseline.

    Uses central differences in the interior, one-sided at boundaries.
    """
    return np.gradient(y, x)


def fd_cv_from_beta(beta: np.ndarray, E: np.ndarray) -> np.ndarray:
    """
    C_V from finite differences on E(β):
    C_V(β) = -β² dE/dβ
    """
    dEdβ = fd_derivative(beta, E)
    return -beta**2 * dEdβ


def fd_cv_from_T(T: np.ndarray, E: np.ndarray) -> np.ndarray:
    """
    C_V from finite differences on E(T):
    C_V(T) = dE/dT
    """
    return fd_derivative(T, E)


def spline_derivative(x: np.ndarray, y: np.ndarray,
                      x_eval: Optional[np.ndarray] = None,
                      resample_factor: int = 10) -> Tuple[np.ndarray, np.ndarray]:
    """
    Cubic spline fit + analytic derivative.

    Paper uses resampling factor of 10 (every 10th point for spline fit,
    evaluated on full grid).

    Parameters
    ----------
    x : input array
    y : data array
    x_eval : evaluation points (default: same as x)
    resample_factor : use every Nth point for fitting

    Returns
    -------
    y_fit : spline values at x_eval
    dydx : spline derivative at x_eval
    """
    if x_eval is None:
        x_eval = x

    # Resample for fitting
    x_fit = x[::resample_factor]
    y_fit = y[::resample_factor]

    cs = CubicSpline(x_fit, y_fit)
    return cs(x_eval), cs(x_eval, 1)  # 0th and 1st derivative


def spline_cv_from_beta(beta: np.ndarray, E: np.ndarray,
                        beta_eval: Optional[np.ndarray] = None,
                        resample_factor: int = 10) -> np.ndarray:
    """
    C_V from cubic spline on E(β):
    C_V(β) = -β² dE/dβ
    """
    if beta_eval is None:
        beta_eval = beta
    _, dEdβ = spline_derivative(beta, E, beta_eval, resample_factor)
    return -beta_eval**2 * dEdβ


def spline_cv_from_T(T: np.ndarray, E: np.ndarray,
                     T_eval: Optional[np.ndarray] = None,
                     resample_factor: int = 10) -> np.ndarray:
    """
    C_V from cubic spline on E(T):
    C_V(T) = dE/dT
    """
    if T_eval is None:
        T_eval = T
    _, dEdT = spline_derivative(T, E, T_eval, resample_factor)
    return dEdT


def compute_entropy_fd(T: np.ndarray, cv: np.ndarray) -> np.ndarray:
    """
    S(T) = ∫₀ᵀ C_V/T dT, using trapezoid rule.
    Same as in GPR module.
    """
    integrand = cv / T
    return cumulative_trapezoid(integrand, T, initial=0.0)


if __name__ == '__main__':
    # Quick validation with known function
    x = np.linspace(0.1, 10, 200)
    y_true = np.sin(x)
    dy_true = np.cos(x)

    # Add noise
    rng = np.random.default_rng(42)
    y_noisy = y_true + 0.05 * rng.normal(size=len(x))

    dy_fd = fd_derivative(x, y_noisy)
    _, dy_spline = spline_derivative(x, y_noisy)

    rmse_fd = np.sqrt(np.mean((dy_fd - dy_true)**2))
    rmse_spline = np.sqrt(np.mean((dy_spline - dy_true)**2))

    print(f"FD derivative RMSE:     {rmse_fd:.4f}")
    print(f"Spline derivative RMSE: {rmse_spline:.4f}")
