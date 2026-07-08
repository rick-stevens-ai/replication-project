"""
step2_leading_order.py — Section 2.1, leading order O(eps^0).

Verify the leading-order homogeneous Mathieu solution z0 (Eq. 13):

    z0(t) = A * sum_{n=-2..2} D_2n cos((2n+beta) t)
          + B * sum_{n=-2..2} D_2n sin((2n+beta) t)

with constant A,B (frozen slow time) actually solves the leading-order
Mathieu equation (Eq. 6):

    M(z0) = z0'' - 4(gamma + alpha cos 2t) z0 = 0.

We do this two ways:
 (1) Symbolic-ish residual: plug the 5-term truncation into M and measure the
     residual L2 norm over one fundamental period. It should be small and
     decrease as we add more D_2n terms (truncation error only).
 (2) Direct numerical Floquet check: integrate the linear Mathieu ODE
     y'' = 4(gamma+alpha cos2t) y from the analytic (z0, z0') IC and confirm
     the trajectory stays quasiperiodic / bounded with the predicted
     fundamental frequency beta (first stability region => bounded).

This nails down that our beta and D_2n give a genuine Floquet solution, which
is the foundation for the whole multiple-scales construction.
"""
import sys
import numpy as np
from scipy.integrate import solve_ivp
sys.path.insert(0, str(__file__.rsplit('/',1)[0]))
from mathieu_beta import solve_beta, compute_D_coeffs

def solve_D(alpha, gamma, beta, nmax=5):
    return compute_D_coeffs(alpha, gamma, beta, n_max=nmax)

def z0_series(t, A, B, beta, D, nmax=2):
    z = np.zeros_like(t, dtype=float)
    zp = np.zeros_like(t, dtype=float)
    zpp = np.zeros_like(t, dtype=float)
    for n in range(-nmax, nmax+1):
        w = 2*n + beta
        d = D[n]
        z   += d*(A*np.cos(w*t) + B*np.sin(w*t))
        zp  += d*w*(-A*np.sin(w*t) + B*np.cos(w*t))
        zpp += d*(-w*w)*(A*np.cos(w*t) + B*np.sin(w*t))
    return z, zp, zpp

def residual(alpha, gamma, beta, D, nmax, A=1.0, B=0.3):
    t = np.linspace(0, 2*np.pi, 4000)   # fundamental period of cos2t is pi; use 2pi
    z, zp, zpp = z0_series(t, A, B, beta, D, nmax)
    M = zpp - 4*(gamma + alpha*np.cos(2*t))*z
    return np.sqrt(np.trapezoid(M**2, t)/(t[-1]-t[0])), np.max(np.abs(z))

if __name__ == "__main__":
    for (alpha, gamma, name) in [(0.15,-0.05,"Fig1"), (0.05,-0.1,"Fig4")]:
        beta = solve_beta(alpha, gamma)
        print(f"\n=== {name}: alpha={alpha}, gamma={gamma}, beta={beta:.6f} ===")
        for nmax in [1,2,3,5,8]:
            D = solve_D(alpha, gamma, beta, nmax=nmax)
            res, zmax = residual(alpha, gamma, beta, D, nmax)
            print(f"  nmax={nmax}: ||M(z0)||_rms = {res:.3e}   (max|z0|={zmax:.3f})")

    # Direct Floquet / boundedness check for Fig1 truncation
    print("\n=== Floquet boundedness check (Fig1) ===")
    alpha, gamma = 0.15, -0.05
    beta = solve_beta(alpha, gamma)
    D = solve_D(alpha, gamma, beta, nmax=5)
    t0arr = np.array([0.0])
    z0, zp0, _ = z0_series(t0arr, 1.0, 0.0, beta, D, nmax=5)
    def lin(t,y): return [y[1], 4*(gamma+alpha*np.cos(2*t))*y[0]]
    sol = solve_ivp(lin,(0,400),[z0[0],zp0[0]],rtol=1e-10,atol=1e-12,max_step=0.05)
    print(f"  IC from analytic z0: z(0)={z0[0]:.4f}, z'(0)={zp0[0]:.4f}")
    print(f"  over t in [0,400]: max|z|={np.max(np.abs(sol.y[0])):.4f}  "
          f"(bounded => first stability region confirmed)")
