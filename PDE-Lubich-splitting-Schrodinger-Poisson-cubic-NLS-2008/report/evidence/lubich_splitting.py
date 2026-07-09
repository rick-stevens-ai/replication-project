"""
Numerical replication of Lubich (2008),
"On splitting methods for Schrödinger-Poisson and cubic nonlinear Schrödinger equations",
Math. Comp. 77(264), 2141-2153.  DOI 10.1090/S0025-5718-08-02101-7.

The paper contains no numerical experiments.  This script implements the
Strang split-step Fourier method (eq. (1.4) in the paper) on 1D periodic
domain (paper: "Our arguments would apply similarly to problems with periodic
boundary conditions and in lower space dimension") and verifies the two main
theorems:

  Thm 2.1 (Schrödinger-Poisson):  L2 error = O(tau^2),  H1 error = O(tau)
  Thm 7.1 (cubic NLS):            L2 error = O(tau^2),  H2 error = O(tau)

The reference solution is a highly-refined Strang splitting solve at a much
smaller step size than any of the coarse steps we measure against.

Scheme (from eq. (1.4)):
    psi_{n+1/2}^-  = exp(i tau/2 * Delta) psi_n     (Fourier: multiply by exp(-i tau/2 |k|^2))
    psi_{n+1/2}^+  = exp(-i tau V[psi_{n+1/2}^-]) psi_{n+1/2}^-
    psi_{n+1}      = exp(i tau/2 * Delta) psi_{n+1/2}^+

For cubic NLS (focusing +, defocusing -):     V[psi] = ±|psi|^2
For Schrödinger-Poisson (1D, periodic):       -V'' = ±|psi|^2 with V zero-mean
   -> in Fourier: V_hat[k] = ±rho_hat[k] / k^2 for k != 0,  V_hat[0] = 0.

L2 conservation of the scheme is exact up to floating-point (both sub-flows
are unitary in L2).  This is measured and reported.

Units:  hbar=1, mass = 1/2 so that "-Laplacian" is the Hamiltonian kinetic term.
"""

from __future__ import annotations
import numpy as np
from numpy.fft import fft, ifft, fftfreq


# ----------------------------------------------------------------------------
# grid + spectral helpers
# ----------------------------------------------------------------------------
def make_grid(N: int, L: float):
    """Uniform periodic grid on [0, L)."""
    x  = np.linspace(0.0, L, N, endpoint=False)
    dx = L / N
    # spectral wave numbers (frequencies * 2 pi / L)
    k  = 2.0 * np.pi * fftfreq(N, d=dx)
    k2 = k * k
    return x, dx, k, k2


def norm_L2(u, dx):
    return float(np.sqrt(np.sum(np.abs(u) ** 2) * dx))


def norm_Hm(u, dx, k, m):
    """Weighted Sobolev norm: ||u||_{H^m}^2 = sum_j || d^j u/dx^j ||_{L2}^2 for j=0..m."""
    uh = fft(u)
    Nx = u.size
    s2 = 0.0
    for j in range(0, m + 1):
        # d^j/dx^j <-> (ik)^j in Fourier
        deriv_hat = ((1j * k) ** j) * uh
        deriv     = ifft(deriv_hat)
        s2       += float(np.sum(np.abs(deriv) ** 2) * dx)
    return float(np.sqrt(s2))


# ----------------------------------------------------------------------------
# potential operators
# ----------------------------------------------------------------------------
def V_cubic(psi, sign: float = -1.0):
    """V = sign * |psi|^2   (sign = -1 defocusing, +1 focusing)."""
    return sign * (np.abs(psi) ** 2)


def V_poisson_1d(psi, k2, sign: float = -1.0):
    """
    1D periodic Schrödinger-Poisson: -V'' = sign * |psi|^2, zero-mean.
    In Fourier: V_hat = sign * rho_hat / k^2 for k != 0, V_hat[0] = 0.
    """
    rho     = np.abs(psi) ** 2
    rho_hat = fft(rho)
    V_hat   = np.zeros_like(rho_hat, dtype=complex)
    nz      = k2 > 0
    V_hat[nz] = sign * rho_hat[nz] / k2[nz]
    V = ifft(V_hat).real  # potential is real
    return V


# ----------------------------------------------------------------------------
# one Strang splitting step (equation (1.4) of the paper)
# ----------------------------------------------------------------------------
def strang_step(psi, tau, k2, potential_fn):
    """
    Apply one Strang step:
      psi_{n+1/2}^-  = exp(i tau/2 * Delta) psi_n            (half kinetic)
      psi_{n+1/2}^+  = exp(-i tau V[psi_{n+1/2}^-]) psi_{n+1/2}^-  (full potential)
      psi_{n+1}      = exp(i tau/2 * Delta) psi_{n+1/2}^+    (half kinetic)

    The paper uses the sign convention i psi_t = -Delta psi + V psi, so:
      free Schrödinger solver: multiply psi_hat by exp(-i tau/2 |k|^2)
      pointwise potential  :   multiply psi   by exp(-i tau V[|psi|^2])
    (Note: |psi| is preserved by the potential step, so V[|psi|^2] evaluated
     at the mid-point value is the same as at the post-step value -> explicit,
     time-reversible; see paper.)
    """
    # half-kinetic (in Fourier)
    psih = fft(psi)
    psih *= np.exp(-0.5j * tau * k2)
    psi  = ifft(psih)

    # full-potential (in physical space)
    V     = potential_fn(psi)
    psi   = psi * np.exp(-1j * tau * V)

    # half-kinetic (in Fourier)
    psih  = fft(psi)
    psih *= np.exp(-0.5j * tau * k2)
    psi   = ifft(psih)
    return psi


def evolve(psi0, T, tau, k2, potential_fn):
    """Time-step from t=0 to t=T with step size tau (T assumed multiple of tau)."""
    n_steps = int(round(T / tau))
    assert abs(n_steps * tau - T) < 1e-12 * max(1.0, T), \
        f"T={T}, tau={tau} -> n_steps={n_steps}, mismatch"
    psi = psi0.astype(complex).copy()
    for _ in range(n_steps):
        psi = strang_step(psi, tau, k2, potential_fn)
    return psi


# ----------------------------------------------------------------------------
# convergence sweep
# ----------------------------------------------------------------------------
def convergence_sweep(problem_name, psi0, T, taus, tau_ref, k, k2, dx, potential_fn, hm_order):
    """
    Compute reference (Strang at tau_ref) and errors at each tau in `taus`.
    Returns dict with per-tau L2 / Hm errors + numerical order estimates.
    """
    print(f"\n=== {problem_name} ===")
    print(f"reference solve: tau_ref = {tau_ref:.3e}, T = {T}, N = {psi0.size}")
    psi_ref = evolve(psi0, T, tau_ref, k2, potential_fn)
    err_L2, err_Hm, mass_drift = [], [], []
    for tau in taus:
        psi_num = evolve(psi0, T, tau, k2, potential_fn)
        e_l2    = norm_L2(psi_num - psi_ref, dx)
        e_hm    = norm_Hm(psi_num - psi_ref, dx, k, hm_order)
        m_final = norm_L2(psi_num, dx)
        m_init  = norm_L2(psi0, dx)
        err_L2.append(e_l2)
        err_Hm.append(e_hm)
        mass_drift.append(abs(m_final - m_init) / m_init)
        print(f"  tau={tau:.4e}  ||e||_L2={e_l2:.4e}  ||e||_H{hm_order}={e_hm:.4e}  "
              f"|dM|/M={mass_drift[-1]:.2e}")
    # numerical orders from consecutive tau ratios
    orders_L2, orders_Hm = [], []
    for i in range(len(taus) - 1):
        r = taus[i] / taus[i + 1]
        orders_L2.append(np.log(err_L2[i] / err_L2[i + 1]) / np.log(r))
        orders_Hm.append(np.log(err_Hm[i] / err_Hm[i + 1]) / np.log(r))
    print(f"  numerical orders (L2)          : {['%.3f'%o for o in orders_L2]}")
    print(f"  numerical orders (H{hm_order}) : {['%.3f'%o for o in orders_Hm]}")
    return dict(problem=problem_name, taus=list(taus), tau_ref=tau_ref,
                err_L2=err_L2, err_Hm=err_Hm, hm_order=hm_order,
                orders_L2=orders_L2, orders_Hm=orders_Hm,
                mass_drift=mass_drift, N=int(psi0.size), T=T)


# ----------------------------------------------------------------------------
# initial data (smooth H^inf on the torus -> automatically H^4)
# ----------------------------------------------------------------------------
def gaussian_bump(x, L, x0=None, sigma=None):
    if x0    is None: x0    = L / 2.0
    if sigma is None: sigma = L / 20.0
    # periodic Gaussian (image method truncated)
    u = np.zeros_like(x, dtype=complex)
    for n in (-1, 0, 1):
        u += np.exp(-((x - x0 - n * L) ** 2) / (2.0 * sigma ** 2))
    # L2-normalize to 1 as in paper
    dx = L / x.size
    u /= np.sqrt(np.sum(np.abs(u) ** 2) * dx)
    return u


def multi_mode(x, L, modes=(1, 2, 3), amps=(1.0, 0.5, 0.3), phases=(0.0, 0.7, 1.3)):
    """Smooth periodic init: sum of low-frequency Fourier modes."""
    u = np.zeros_like(x, dtype=complex)
    for m, a, ph in zip(modes, amps, phases):
        u += a * np.exp(1j * (2.0 * np.pi * m * x / L + ph))
    dx = L / x.size
    u /= np.sqrt(np.sum(np.abs(u) ** 2) * dx)
    return u


# ----------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------
def main():
    import json, os, sys
    L, N   = 2.0 * np.pi, 512
    x, dx, k, k2 = make_grid(N, L)

    # -------- cubic NLS (defocusing, sign=-1) --------
    T_nls      = 1.0
    taus_nls   = [1.0/50, 1.0/100, 1.0/200, 1.0/400, 1.0/800]
    tau_ref_nls = 1.0 / 32000       # ~40x finer than finest coarse tau
    psi0_nls    = multi_mode(x, L)   # smooth, moderate amplitude -> H^inf regular
    res_nls = convergence_sweep(
        "cubic NLS (1D, periodic, defocusing) — Theorem 7.1",
        psi0_nls, T_nls, taus_nls, tau_ref_nls,
        k, k2, dx,
        potential_fn=lambda psi: V_cubic(psi, sign=-1.0),
        hm_order=2,
    )

    # -------- cubic NLS (focusing, sign=+1) --------
    res_nls_foc = convergence_sweep(
        "cubic NLS (1D, periodic, focusing) — Theorem 7.1",
        psi0_nls, T_nls, taus_nls, tau_ref_nls,
        k, k2, dx,
        potential_fn=lambda psi: V_cubic(psi, sign=+1.0),
        hm_order=2,
    )

    # -------- Schrödinger-Poisson (defocusing, sign=-1) --------
    # sign in the paper: -Delta V = +/- |psi|^2 (both signs studied)
    T_sp      = 1.0
    taus_sp   = [1.0/50, 1.0/100, 1.0/200, 1.0/400, 1.0/800]
    tau_ref_sp = 1.0 / 32000
    psi0_sp   = gaussian_bump(x, L)   # bump on torus -> smooth -> H^inf regular
    res_sp = convergence_sweep(
        "Schrödinger-Poisson (1D, periodic, +|psi|^2) — Theorem 2.1",
        psi0_sp, T_sp, taus_sp, tau_ref_sp,
        k, k2, dx,
        potential_fn=lambda psi: V_poisson_1d(psi, k2, sign=+1.0),
        hm_order=1,
    )

    # -------- Schrödinger-Poisson (opposite sign, -|psi|^2) --------
    res_sp_alt = convergence_sweep(
        "Schrödinger-Poisson (1D, periodic, -|psi|^2) — Theorem 2.1",
        psi0_sp, T_sp, taus_sp, tau_ref_sp,
        k, k2, dx,
        potential_fn=lambda psi: V_poisson_1d(psi, k2, sign=-1.0),
        hm_order=1,
    )

    out = dict(cubic_NLS_defocusing=res_nls,
               cubic_NLS_focusing  =res_nls_foc,
               SP_plus =res_sp,
               SP_minus=res_sp_alt,
               grid=dict(L=L, N=int(N), dx=float(dx)))
    outpath = os.path.join(os.path.dirname(__file__), "convergence_results.json")
    with open(outpath, "w") as f:
        json.dump(out, f, indent=2, default=float)
    print(f"\nwrote {outpath}")


if __name__ == "__main__":
    main()
