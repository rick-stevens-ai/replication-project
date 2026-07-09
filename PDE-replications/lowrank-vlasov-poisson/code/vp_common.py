"""Common utilities for 1D1V Vlasov-Poisson solvers.

Periodic in x on [0, L=2π/k], grid v on [-vmax, vmax] (assumed sufficiently large
that f ~ 0 at the boundary; we treat v as periodic for FFT convenience too, but
solve velocity advection in spectral form which is exact for the linear shift
problem here -- and we use a sufficiently wide v-domain).

Vlasov-Poisson (electrons, fixed ion neutralizing background):
   ∂_t f + v ∂_x f - E ∂_v f = 0
   ∂_x E = ∫ f dv - 1 ,    periodic, ⟨E⟩_x = 0.

For low-rank, f(x_i, v_j, t) ≈ Σ_{k,l} X_ik(t) S_kl(t) V_lj(t) with X, V orthonormal
columns (discrete L²) and S an r×r matrix.
"""
from __future__ import annotations
import numpy as np
from dataclasses import dataclass


@dataclass
class Grid:
    Nx: int
    Nv: int
    L: float       # x ∈ [0, L]
    vmax: float    # v ∈ [-vmax, vmax]

    @property
    def dx(self) -> float:
        return self.L / self.Nx

    @property
    def dv(self) -> float:
        return 2.0 * self.vmax / self.Nv

    @property
    def x(self) -> np.ndarray:
        return np.arange(self.Nx) * self.dx

    @property
    def v(self) -> np.ndarray:
        # cell-centered, symmetric grid for nicer ∫v dv conservation
        return -self.vmax + (np.arange(self.Nv) + 0.5) * self.dv

    @property
    def kx(self) -> np.ndarray:
        """Fourier wave numbers for x (periodic)."""
        return 2.0 * np.pi * np.fft.fftfreq(self.Nx, d=self.dx)

    @property
    def kv(self) -> np.ndarray:
        """Fourier wave numbers for v (treated periodic with period 2*vmax)."""
        return 2.0 * np.pi * np.fft.fftfreq(self.Nv, d=self.dv)


def landau_ic(grid: Grid, alpha: float = 0.01, k: float = 0.5) -> np.ndarray:
    """Landau damping initial f(x,v) = (1+α cos(kx)) * exp(-v²/2)/sqrt(2π)."""
    x = grid.x[:, None]
    v = grid.v[None, :]
    return (1.0 + alpha * np.cos(k * x)) * np.exp(-0.5 * v ** 2) / np.sqrt(2.0 * np.pi)


def two_stream_ic(grid: Grid, alpha: float = 0.05, k: float = 0.5, v0: float = 2.4) -> np.ndarray:
    """Two-stream instability:
        f₀(x,v) = (1 + α cos(kx)) * 0.5 * [g(v-v0) + g(v+v0)],   g = e^{-v²/2}/√(2π).
    """
    x = grid.x[:, None]
    v = grid.v[None, :]
    g = lambda u: np.exp(-0.5 * u ** 2) / np.sqrt(2.0 * np.pi)
    return (1.0 + alpha * np.cos(k * x)) * 0.5 * (g(v - v0) + g(v + v0))


def density(f: np.ndarray, grid: Grid) -> np.ndarray:
    """ρ(x) = ∫ f dv."""
    return np.sum(f, axis=1) * grid.dv


def poisson_E(f: np.ndarray, grid: Grid) -> np.ndarray:
    """Solve ∂_x E = 1 - ρ in periodic Fourier space, ⟨E⟩=0.

    Convention (Cheng–Knorr 1976; Einkemmer–Lubich 2018): Vlasov–Poisson written
    as  ∂_t f + v ∂_x f - E ∂_v f = 0,  ∂_x E = 1 - ∫ f dv.
    With this sign, for δρ = α cos(kx) one gets E = -(α/k) sin(kx), and linear
    Landau damping for k=0.5 decays at rate γ ≈ 0.1533.
    """
    rho_minus_bg = 1.0 - density(f, grid)
    rho_hat = np.fft.fft(rho_minus_bg)
    kx = grid.kx
    E_hat = np.zeros_like(rho_hat)
    nz = kx != 0
    E_hat[nz] = rho_hat[nz] / (1j * kx[nz])
    E = np.real(np.fft.ifft(E_hat))
    return E


def electric_energy(E: np.ndarray, grid: Grid) -> float:
    """½ ∫ E² dx."""
    return 0.5 * np.sum(E ** 2) * grid.dx


def total_mass(f: np.ndarray, grid: Grid) -> float:
    return np.sum(f) * grid.dx * grid.dv


def kinetic_energy(f: np.ndarray, grid: Grid) -> float:
    return 0.5 * np.sum(f * grid.v[None, :] ** 2) * grid.dx * grid.dv


def l2_norm(f: np.ndarray, grid: Grid) -> float:
    return np.sqrt(np.sum(f ** 2) * grid.dx * grid.dv)
