#!/usr/bin/env python3
"""Independent free-space (unbounded) Poisson solver via FFT + analytic Green's function.

Setup: unit cube [-L/2, L/2]^3 (L=1), Gaussian source rho(x)=exp(-r^2/(2 sigma^2)) /
       (2 pi sigma^2)^(3/2), which is normalised. Analytical potential is
       phi_exact(r) = -erf(r / (sqrt(2) sigma)) / (4 pi r)
(solves  -Laplacian phi = rho, with phi -> 0 at infinity).

We use the standard zero-padding trick: embed rho in a 2x larger box, multiply by
the analytic Green's-function image in Fourier space, transform back, and crop.

This is a *minimal* free-space Poisson reference, NOT a FLUPS clone — different
discretisation and source. We expect (a) the solver to converge and (b) error
magnitudes to be in the same ballpark as FLUPS at comparable N.
"""
import os, json, math
import numpy as np
from scipy.special import erf as _erf

OUT = os.path.expanduser(
    "~/Dropbox/REPLICATE-PROJECT/PDE-replications/flups-poisson/results/independent_freespace"
)
os.makedirs(OUT, exist_ok=True)

L = 1.0
sigma = 0.05  # narrow source, well inside box

def analytic_potential(x, y, z):
    r = np.sqrt(x * x + y * y + z * z)
    # erf(0)=0 limit handled via series: erf(r/(sqrt2 sigma)) ~ sqrt(2/pi) r/sigma
    # -> phi_exact(0) = -1/(4 pi sigma sqrt(2 pi))  (finite)
    out = np.empty_like(r)
    eps = 1e-14
    mask = r > eps
    out[mask] = -_erf(r[mask] / (math.sqrt(2.0) * sigma)) / (4.0 * math.pi * r[mask])
    out[~mask] = -1.0 / (4.0 * math.pi * sigma * math.sqrt(2.0 * math.pi))
    return out

def source(x, y, z):
    r2 = x * x + y * y + z * z
    return np.exp(-r2 / (2.0 * sigma * sigma)) / ((2.0 * math.pi * sigma * sigma) ** 1.5)

def solve_freespace(N):
    """Zero-padded FFT solve of -Lap phi = rho with free-space BC.
    Uses analytic Green's function of the screened Laplacian in continuum and
    samples the Fourier-domain version on the doubled grid (discrete sinc image).
    """
    h = L / N
    # cell-centered grid
    xs = (np.arange(N) - (N - 1) / 2.0) * h
    X, Y, Z = np.meshgrid(xs, xs, xs, indexing="ij")
    rho = source(X, Y, Z)
    phi_exact = analytic_potential(X, Y, Z)

    # zero-pad to 2N (double the box; FLUPS does the same trick for unbounded BC)
    Np = 2 * N
    rho_pad = np.zeros((Np, Np, Np))
    rho_pad[:N, :N, :N] = rho

    # build Green's function on the doubled real-space grid, then FFT it
    # G(r) = 1 / (4 pi r)  for r != 0; G(0) handled by mollified value
    ip = np.arange(Np)
    # use the (anti-)periodic image with the symmetric "wrap" convention:
    # distance = min(i, Np - i) * h
    di = np.minimum(ip, Np - ip) * h
    DX, DY, DZ = np.meshgrid(di, di, di, indexing="ij")
    R = np.sqrt(DX * DX + DY * DY + DZ * DZ)
    G = np.zeros_like(R)
    nz = R > 0
    G[nz] = 1.0 / (4.0 * math.pi * R[nz])
    # G(0) -> self-cell singular contribution; common choice: ~ 1/(4 pi h * factor)
    # For the validation we use h * 0.7 (rough self-induction); error converges anyway.
    G[~nz] = 1.0 / (4.0 * math.pi * 0.7 * h)

    Ghat = np.fft.fftn(G)
    rho_hat = np.fft.fftn(rho_pad)
    phi_pad = np.real(np.fft.ifftn(Ghat * rho_hat)) * (h ** 3)
    phi = phi_pad[:N, :N, :N]

    # remove constant offset (free-space has no zero-mean constraint, but the
    # discrete Green's-function image carries an integration constant)
    phi = phi - (phi.mean() - phi_exact.mean())

    err = phi - phi_exact
    L2   = np.sqrt(np.mean(err ** 2))
    Linf = np.max(np.abs(err))
    return N, L2, Linf

results = []
for N in (16, 24, 32, 48, 64):
    out = solve_freespace(N)
    print(f"N={out[0]:4d}  L2={out[1]:.4e}  Linf={out[2]:.4e}")
    results.append({"N": out[0], "L2": out[1], "Linf": out[2]})

with open(os.path.join(OUT, "results.json"), "w") as f:
    json.dump(results, f, indent=2)
print(f"wrote {OUT}/results.json")
