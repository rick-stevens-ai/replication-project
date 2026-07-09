"""Full-grid baseline: Fourier semi-Lagrangian Strang splitting for 1D1V Vlasov-Poisson.

Step: A_{Δt/2} ∘ B_{Δt} ∘ A_{Δt/2}, where
   A: ∂_t f + v ∂_x f = 0     (free streaming in x; shift in x by v Δt, exact via FFT)
   B: ∂_t f - E(x) ∂_v f = 0  (force in v;          shift in v by -E Δt, exact via FFT)

Both half-/full-step shifts are exact for a single Fourier mode -> use spectral
shift operator  f(x) -> IFFT( exp(-i k Δ) FFT(f) ). This is the classical
Cheng-Knorr (1976) semi-Lagrangian Fourier method.
"""
from __future__ import annotations
import numpy as np
from vp_common import Grid, poisson_E, density, electric_energy, total_mass, kinetic_energy, l2_norm


def _shift_x(f: np.ndarray, grid: Grid, dt: float) -> np.ndarray:
    """Solve ∂_t f + v ∂_x f = 0 for time dt exactly. For each v_j, shift by v_j*dt."""
    fhat = np.fft.fft(f, axis=0)              # (Nx, Nv)
    kx = grid.kx[:, None]                     # (Nx, 1)
    v = grid.v[None, :]                       # (1, Nv)
    fhat *= np.exp(-1j * kx * v * dt)
    return np.real(np.fft.ifft(fhat, axis=0))


def _shift_v(f: np.ndarray, E: np.ndarray, grid: Grid, dt: float) -> np.ndarray:
    """Solve ∂_t f - E(x) ∂_v f = 0 for time dt. For each x_i, shift in v by -E_i*dt."""
    fhat = np.fft.fft(f, axis=1)              # (Nx, Nv)
    kv = grid.kv[None, :]                     # (1, Nv)
    Ec = E[:, None]                           # (Nx, 1)
    fhat *= np.exp(1j * kv * Ec * dt)         # ∂_t f - E ∂_v f = 0  ->  shift by -E*dt
    return np.real(np.fft.ifft(fhat, axis=1))


def step(f: np.ndarray, grid: Grid, dt: float) -> np.ndarray:
    """One Strang step: x-half, then v-full with E mid, then x-half."""
    f = _shift_x(f, grid, 0.5 * dt)
    E = poisson_E(f, grid)
    f = _shift_v(f, E, grid, dt)
    f = _shift_x(f, grid, 0.5 * dt)
    return f


def run(f0: np.ndarray, grid: Grid, T: float, dt: float, diag_every: int = 1):
    """Run full-grid simulation. Returns dict with time series of diagnostics and final f."""
    Nt = int(round(T / dt))
    t = np.zeros(Nt + 1)
    Ee = np.zeros(Nt + 1)
    mass = np.zeros(Nt + 1)
    KE = np.zeros(Nt + 1)
    L2 = np.zeros(Nt + 1)

    f = f0.copy()
    E = poisson_E(f, grid)
    Ee[0] = electric_energy(E, grid)
    mass[0] = total_mass(f, grid)
    KE[0] = kinetic_energy(f, grid)
    L2[0] = l2_norm(f, grid)

    snapshots = {0.0: f.copy()}

    for n in range(Nt):
        f = step(f, grid, dt)
        t[n + 1] = (n + 1) * dt
        if (n + 1) % diag_every == 0 or n == Nt - 1:
            E = poisson_E(f, grid)
            Ee[n + 1] = electric_energy(E, grid)
            mass[n + 1] = total_mass(f, grid)
            KE[n + 1] = kinetic_energy(f, grid)
            L2[n + 1] = l2_norm(f, grid)

    return {
        "t": t,
        "E_energy": Ee,
        "mass": mass,
        "kinetic_energy": KE,
        "l2": L2,
        "f_final": f,
    }
