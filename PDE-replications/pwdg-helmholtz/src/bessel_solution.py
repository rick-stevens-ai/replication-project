"""
Exact solution from Hiptmair-Moiola-Perugia 2011 §4:

    u(x) = J_xi(omega * r) * cos(xi * theta)

with x = (r*cos(theta), r*sin(theta)).

For xi=1: u in C^infty(R^2) (regular, exponential PWDG convergence expected)
For xi=2/3 or 3/2: u has corner singularity at origin (algebraic convergence)

This solves -Delta u - omega^2 u = 0 in R^2 \ {0}, and is smooth on Omega = [0,1]x[-1/2,1/2]
when xi in N (e.g. xi=1). For xi=2/3, 3/2 the origin is on the boundary (mesh vertex).
"""
import numpy as np
from scipy.special import jv, jvp


def make_bessel_solution(xi, omega):
    """Return callable u_exact(pts, deriv=None) -> values or normal derivative.

    pts: (N,2) cartesian coords
    deriv: if None, return u; if 2-vector n, return grad(u) . n
    """
    xi = float(xi)
    omega = float(omega)

    def u(pts, deriv=None):
        pts = np.atleast_2d(pts)
        x, y = pts[:, 0], pts[:, 1]
        r = np.sqrt(x*x + y*y)
        theta = np.arctan2(y, x)
        # guard for r=0 (only one mesh node)
        # For xi integer, J_xi(0)=0 for xi>=1, so u(0)=0
        # For xi not integer, J_xi(omega*r)->0 like r^xi, so u(0)=0
        eps = 1e-300
        r_safe = np.where(r < eps, eps, r)
        if deriv is None:
            val = jv(xi, omega * r_safe) * np.cos(xi * theta)
            # at r=0 exactly:
            val = np.where(r < eps, 0.0, val)
            return val.astype(np.complex128)
        else:
            n = np.asarray(deriv, dtype=float)
            # grad u in polar: u_r * r_hat + (1/r) * u_theta * theta_hat
            # u_r = omega * J'_xi(omega r) * cos(xi theta)
            # u_theta = -xi * J_xi(omega r) * sin(xi theta)
            ur = omega * jvp(xi, omega * r_safe, 1) * np.cos(xi * theta)
            ut = -xi * jv(xi, omega * r_safe) * np.sin(xi * theta)
            cos_t = np.cos(theta)
            sin_t = np.sin(theta)
            ux = ur * cos_t - (ut / r_safe) * sin_t
            uy = ur * sin_t + (ut / r_safe) * cos_t
            # at r=0: gradient is ill-defined for fractional xi; clamp
            ux = np.where(r < 1e-12, 0.0, ux)
            uy = np.where(r < 1e-12, 0.0, uy)
            return (ux * n[0] + uy * n[1]).astype(np.complex128)

    return u


def is_regular(xi):
    """Helmholtz-extendable iff xi is a nonnegative integer."""
    return float(xi).is_integer() and float(xi) >= 0
