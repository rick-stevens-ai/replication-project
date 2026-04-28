"""KS reference solver. Uses scipy.solve_ivp (adaptive RK45) on the Fourier
representation, which is robust and avoids the instability we encountered
with hand-rolled ETDRK4/IF-RK4 at L=22.
"""
import time
import numpy as np


def ks_reference(N=128, L=22.0, dt_sample=0.25, T=2000.0, ic_seed=0, verbose=True):
    from scipy.integrate import solve_ivp
    rng = np.random.default_rng(ic_seed)
    x = L * np.arange(N) / N
    # Smooth IC on attractor scales
    u = np.cos(2 * np.pi * x / L) * (1 + np.sin(2 * np.pi * x / L))
    u = u + 0.05 * rng.standard_normal(N)

    k = 2 * np.pi * np.fft.fftfreq(N, d=L / N)
    L_op = k**2 - k**4
    k_max = N // 3
    k_idx = np.abs(k) / (2 * np.pi / L)
    dealias = (k_idx < k_max).astype(float)

    def rhs(t, u):
        u_hat = np.fft.fft(u) * dealias
        u_x = np.real(np.fft.ifft(1j * k * u_hat))
        lin = np.real(np.fft.ifft(L_op * u_hat))
        nonlin = -u * u_x
        nonlin_hat = dealias * np.fft.fft(nonlin)
        nonlin = np.real(np.fft.ifft(nonlin_hat))
        return nonlin + lin

    t0 = time.time()
    if verbose:
        print(f"  KS burn-in (200 tu), N={N}, L={L}...", flush=True)
    sol = solve_ivp(rhs, (0, 200.0), u, method='BDF',
                    rtol=1e-4, atol=1e-6)
    if not sol.success:
        print("  burn-in failed:", sol.message, flush=True)
        return None, None
    u = sol.y[:, -1]
    if verbose:
        print(f"  burn-in done, |u|_max={np.max(np.abs(u)):.2f}, "
              f"{time.time()-t0:.1f}s", flush=True)

    t_eval = np.arange(0, T + 1e-9, dt_sample)
    sol = solve_ivp(rhs, (0, T), u, method='BDF',
                    rtol=1e-4, atol=1e-6, t_eval=t_eval)
    if not sol.success:
        print("  main solve failed:", sol.message, flush=True)
    out = sol.y.T
    t_arr = sol.t
    if verbose:
        print(f"  KS solved {out.shape}, |u|_max={np.max(np.abs(out)):.2f}, "
              f"{time.time()-t0:.1f}s", flush=True)
    return t_arr, out
