"""
Generate Falkner-Skan boundary layer reference data.

Falkner-Skan equation: f''' + f*f'' + beta*(1 - f'^2) = 0
where beta = 2*m/(m+1)

For the paper: m = -0.08, beta_FS = -0.1739, Re = 100
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.interpolate import interp1d
import os


def falkner_skan_ode(eta, f, beta):
    """Falkner-Skan ODE system."""
    return [f[1], f[2], -f[0]*f[2] - beta*(1 - f[1]**2)]


def solve_falkner_skan(beta, eta_max=10, n_points=500):
    """Solve via shooting method."""
    eta = np.linspace(0, eta_max, n_points)
    
    def residual(fpp0):
        sol = solve_ivp(
            lambda t, y: falkner_skan_ode(t, y, beta),
            [0, eta_max], [0, 0, fpp0],
            t_eval=[eta_max], rtol=1e-12, atol=1e-14
        )
        return sol.y[1, -1] - 1.0
    
    fpp0_opt = brentq(residual, 0.01, 2.0, xtol=1e-12)
    
    sol = solve_ivp(
        lambda t, y: falkner_skan_ode(t, y, beta),
        [0, eta_max], [0, 0, fpp0_opt],
        t_eval=eta, rtol=1e-12, atol=1e-14
    )
    
    class SolWrapper:
        def __init__(self, x, y):
            self.x = x
            self.y = y
    
    return SolWrapper(sol.t, sol.y)


def generate_2d_field(m, Re, x_range=(1.0, 25.0), y_max=5.0, nx=100, ny=50):
    """
    Generate 2D velocity and pressure fields from Falkner-Skan similarity solution.
    
    Using non-dimensional variables where U_inf = 1, L = 1.
    nu = 1/Re.
    
    U_e(x) = x^m (external velocity)
    
    The key insight: the Falkner-Skan solution gives u, v that EXACTLY satisfy
    the steady 2D NS equations. So we need to compute the consistent pressure
    field from the NS equations themselves.
    """
    beta = 2 * m / (m + 1)
    print(f"m = {m}, beta_FS = {beta:.4f}")
    
    nu = 1.0 / Re
    
    # Solve similarity equation
    sol = solve_falkner_skan(beta, eta_max=12, n_points=1000)
    eta_sol = sol.x
    f_vals = sol.y[0]   # f
    fp_vals = sol.y[1]  # f'
    fpp_vals = sol.y[2] # f''
    
    f_interp = interp1d(eta_sol, f_vals, kind='cubic', fill_value=(0, f_vals[-1]), bounds_error=False)
    fp_interp = interp1d(eta_sol, fp_vals, kind='cubic', fill_value=(0, 1), bounds_error=False)
    fpp_interp = interp1d(eta_sol, fpp_vals, kind='cubic', fill_value=(fpp_vals[0], 0), bounds_error=False)
    
    # Grid
    x = np.linspace(x_range[0], x_range[1], nx)
    y = np.linspace(0, y_max, ny)
    X, Y = np.meshgrid(x, y)
    
    # External velocity
    U_e = X**m
    
    # Similarity variable
    # eta = y * sqrt((m+1) * U_e / (2 * nu * x))
    eta_field = Y * np.sqrt((m + 1) * U_e / (2 * nu * X))
    eta_clipped = np.clip(eta_field, 0, eta_sol[-1])
    
    # Streamwise velocity: u = U_e * f'(eta)
    U = U_e * fp_interp(eta_clipped)
    
    # Wall-normal velocity from stream function
    # psi = sqrt(2*nu*x*U_e/(m+1)) * f(eta)
    # v = -dpsi/dx (with y held constant)
    coeff = np.sqrt(2 * nu / ((m + 1)))
    # v = -sqrt(nu*U_inf/(2*(m+1))) * x^{(m-1)/2} * ((m+1)*f + (m-1)*eta*f')
    V = -coeff * X**((m-1)/2) * (
        (m + 1) * f_interp(eta_clipped) + 
        (m - 1) * eta_clipped * fp_interp(eta_clipped)
    ) / 2
    
    # Pressure: compute from x-momentum equation
    # u*du/dx + v*du/dy = -1/rho * dP/dx + nu*(d2u/dx2 + d2u/dy2)
    # For BL: dP/dy ≈ 0, P(x) = P_e(x) = const - 0.5*U_e^2 (from Bernoulli outside BL)
    # Inside BL, pressure is approximately equal to outer pressure (BL approximation)
    # P = -0.5 * U_e^2 + const
    # Set const so P = 0 at reference
    P = -0.5 * U_e**2
    P = P - P.min()  # Shift so minimum is 0
    
    return X, Y, U, V, P, eta_clipped


def main():
    m = -0.08
    Re = 100
    
    X, Y, U, V, P, eta = generate_2d_field(m, Re, x_range=(1.0, 25.0), y_max=5.0, nx=200, ny=100)
    
    outdir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(outdir, exist_ok=True)
    
    np.savez(os.path.join(outdir, 'falkner_skan_ref.npz'),
             X=X, Y=Y, U=U, V=V, P=P, eta=eta,
             m=m, Re=Re, beta_FS=2*m/(m+1))
    
    print(f"Reference data saved. Grid: {X.shape}")
    print(f"U range: [{U.min():.6f}, {U.max():.6f}]")
    print(f"V range: [{V.min():.6f}, {V.max():.6f}]")
    print(f"P range: [{P.min():.6f}, {P.max():.6f}]")


if __name__ == '__main__':
    main()
