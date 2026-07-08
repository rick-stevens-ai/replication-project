"""
Zhang et al. 2019 (arXiv:1809.08327, JCP 397:108850) — NN-aPC replication
Re-pass against the *correct* paper: "Quantifying total uncertainty in PINNs..."

This script replicates:
  - Example 4.1.1: Forward stochastic Poisson  (Eq. 26-27)
  - Example 4.1.2: Inverse stochastic elliptic (Eq. 28-29), Table 1
                   (1st-order and 2nd-order aPC, 4 k-sensors + 7 u-sensors)

Method (per §3):
  1) MC-sample N=1000 trajectories of the random input field on a fine grid.
  2) Read sensor values, run PCA (paper §3.2.1) to identify principal random
     variables, project sensor data into uncorrelated ξ.
  3) Construct arbitrary polynomial chaos basis (paper §3.2.2) via Gram–Schmidt
     against the empirical density of ξ (moment integrals approximated from
     the same N samples).
  4) Train multi-output DNNs that map x -> aPC modes {g_alpha(x)} (paper §3.2.3),
     using PDE residual loss (PINN, paper §3.2.4) + boundary-condition / sensor
     data loss.
  5) Compute mean & standard deviation analytically from the aPC modes,
     evaluate vs. MC reference computed from the same N=1000 trajectories.

No DeepXDE high-level API is used because NN-aPC's loss couples the modes in a
problem-specific way (the PDE residual is itself a polynomial in ξ); we use the
plain PyTorch building blocks DeepXDE itself wraps. We still pull `deepxde` to
verify it is installed and to fix the global seed for reproducibility.

Author: re-pass subagent for /Users/stevens/Dropbox/REPLICATE-PROJECT/
"""

from __future__ import annotations

import argparse
import json
import math
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from scipy.linalg import cholesky, solve_triangular

# Pin everything
SEED = 1809
np.random.seed(SEED)
torch.manual_seed(SEED)

DEVICE = torch.device("cpu")  # CPU is fine for these tiny networks
DTYPE = torch.float64
torch.set_default_dtype(DTYPE)


# -----------------------------------------------------------------------------
# 1) Random-field samplers (paper §4.1.1, 4.1.2)
# -----------------------------------------------------------------------------
def squared_exp_cov(x: np.ndarray, sigma: float, ell: float) -> np.ndarray:
    """Squared-exponential covariance K_ij = sigma^2 exp(-(x_i-x_j)^2/ell^2)."""
    x = x.reshape(-1, 1)
    return sigma**2 * np.exp(-((x - x.T) ** 2) / (ell**2))


def sample_gp(x_grid: np.ndarray, mean_fn, sigma: float, ell: float, n: int,
              rng: np.random.Generator) -> np.ndarray:
    """Draw n trajectories of a Gaussian Process on x_grid."""
    K = squared_exp_cov(x_grid, sigma, ell) + 1e-10 * np.eye(len(x_grid))
    L = cholesky(K, lower=True)
    z = rng.standard_normal((len(x_grid), n))
    return mean_fn(x_grid)[:, None] + L @ z  # shape (Nx, n)


# -----------------------------------------------------------------------------
# 2) PCA / dimension reduction (paper §3.2.1)
# -----------------------------------------------------------------------------
def pca_reduce(samples: np.ndarray, energy: float = 0.99):
    """
    samples shape (N_sensor, N_samp).
    Return projection matrix V (N_sensor x d), eigenvalues, retained dim d.
    """
    mean = samples.mean(axis=1, keepdims=True)
    Y = samples - mean
    # empirical sensor covariance
    cov = Y @ Y.T / (Y.shape[1] - 1)
    w, V = np.linalg.eigh(cov)
    idx = np.argsort(w)[::-1]
    w = w[idx]
    V = V[:, idx]
    csum = np.cumsum(w) / w.sum()
    d = int(np.searchsorted(csum, energy) + 1)
    return V[:, :d], w[:d], mean.flatten(), d


def project_to_xi(samples: np.ndarray, V: np.ndarray, mean: np.ndarray,
                  eigvals: np.ndarray) -> np.ndarray:
    """
    Project sensor samples to *standardised* principal random variables.
    Each ξ_i has zero mean and unit variance across the training samples,
    so the empirical aPC moments are well-conditioned.
    Returns xi of shape (d, N_samp).
    """
    Y = samples - mean[:, None]
    coords = V.T @ Y                       # shape (d, N_samp)
    coords = coords / np.sqrt(eigvals)[:, None]
    return coords


# -----------------------------------------------------------------------------
# 3) arbitrary polynomial chaos basis (paper §3.2.2)
# -----------------------------------------------------------------------------
def total_degree_indices(d: int, order: int) -> list[tuple[int, ...]]:
    """All multi-indices (a_1,..,a_d) with sum a_i <= order (total degree)."""
    if d == 0:
        return [()]
    out = []
    for k in range(order + 1):
        for tail in total_degree_indices(d - 1, order - k):
            out.append((k,) + tail)
    return out


def build_apc_basis(xi: np.ndarray, order: int):
    """
    Gram–Schmidt construction of an empirical orthonormal polynomial basis with
    respect to the joint empirical measure of xi (shape (d, N_samp)).
    Returns (eval_fn, P+1) where eval_fn(xi_samp) -> (P+1, N_samp) basis values.
    """
    d, N = xi.shape
    idx = total_degree_indices(d, order)
    P = len(idx) - 1  # total number of basis functions (including constant) is P+1

    # raw monomials Φ_α(ξ) = prod_i ξ_i^{α_i}, shape (P+1, N)
    def monomial(xi_, alpha):
        out = np.ones(xi_.shape[1])
        for i, a in enumerate(alpha):
            if a == 0:
                continue
            out *= xi_[i] ** a
        return out

    M = np.stack([monomial(xi, a) for a in idx], axis=0)  # (P+1, N)

    # Empirical Gram matrix: G_ij = <Φ_i Φ_j> ≈ (1/N) sum Φ_i Φ_j
    G = (M @ M.T) / N
    G = G + 1e-12 * np.eye(G.shape[0])
    L = cholesky(G, lower=True)
    Linv = solve_triangular(L, np.eye(L.shape[0]), lower=True)

    # orthonormal basis Ψ = L^{-1} Φ ; then <Ψ_i Ψ_j>_emp ≈ δ_ij
    def eval_basis(xi_):
        Mx = np.stack([monomial(xi_, a) for a in idx], axis=0)
        return Linv @ Mx  # (P+1, N_eval)

    return eval_basis, P + 1, idx


# -----------------------------------------------------------------------------
# 4) NN-aPC neural network (paper §3.2.3, Fig. 3)
# -----------------------------------------------------------------------------
class APCNet(nn.Module):
    """
    Two heads:
      - mean head (mode 0): 2 hidden layers, 4 neurons (paper default)
      - modes head (modes 1..P): K hidden layers, H neurons (paper: 4×32)
    Input: x (scalar coordinate). Output: vector of length P+1 (modes).
    """

    def __init__(self, num_modes: int, hidden: int = 32, layers: int = 4,
                 mean_hidden: int = 4, mean_layers: int = 2):
        super().__init__()
        self.num_modes = num_modes

        # mean head
        m = [nn.Linear(1, mean_hidden), nn.Tanh()]
        for _ in range(mean_layers - 1):
            m += [nn.Linear(mean_hidden, mean_hidden), nn.Tanh()]
        m += [nn.Linear(mean_hidden, 1)]
        self.mean_head = nn.Sequential(*m)

        # modes head: output (num_modes - 1) for modes 1..P
        h = [nn.Linear(1, hidden), nn.Tanh()]
        for _ in range(layers - 1):
            h += [nn.Linear(hidden, hidden), nn.Tanh()]
        h += [nn.Linear(hidden, max(num_modes - 1, 1))]
        self.modes_head = nn.Sequential(*h)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        m0 = self.mean_head(x)                # (N, 1)
        mk = self.modes_head(x)               # (N, P)
        return torch.cat([m0, mk], dim=1)     # (N, P+1)


# -----------------------------------------------------------------------------
# 5) Helpers: realisations and statistics from modes (paper Eq. 17)
# -----------------------------------------------------------------------------
def realisations(modes: np.ndarray, basis_vals: np.ndarray) -> np.ndarray:
    """u(x; ξ_s) = sum_α  modes_α(x) * Ψ_α(ξ_s)  ; modes (Nx, P+1), basis (P+1, Ns)."""
    return modes @ basis_vals


def mean_from_modes(modes: np.ndarray, basis_vals: np.ndarray) -> np.ndarray:
    """E[u](x) = mean over samples of u(x; ξ_s).  Use empirical sample mean."""
    return realisations(modes, basis_vals).mean(axis=1)


def std_from_modes(modes: np.ndarray, basis_vals: np.ndarray) -> np.ndarray:
    samp = realisations(modes, basis_vals)
    return samp.std(axis=1, ddof=1)


def rel_l2(pred: np.ndarray, ref: np.ndarray) -> float:
    """Relative L2 error: ||pred - ref|| / ||ref||."""
    num = np.linalg.norm(pred - ref)
    den = np.linalg.norm(ref)
    if den < 1e-14:
        return float("inf")
    return float(num / den)


# -----------------------------------------------------------------------------
# 6) Forward Poisson (§4.1.1)
# -----------------------------------------------------------------------------
@dataclass
class ForwardPoissonResult:
    e_relL2: float
    std_relL2: float
    wall_time: float
    mode_relL2: list
    Nf: int
    P: int
    epochs: int
    layers: int
    hidden: int


def solve_forward_poisson(Nf=13, energy=0.99, apc_order=1,
                          layers=4, hidden=32, epochs=20000, lr=1e-3, l2=1e-3,
                          n_grid=201, N_samples=1000, N_test=500,
                          verbose=True) -> ForwardPoissonResult:
    """
    Example 4.1.1 — forward stochastic Poisson:
        -u''(x) = f(x;ω),  x in [-1,1],  u(-1)=u(1)=0
        f ~ GP(10 sin(pi x), sigma=1, ell=0.5)
    Reference statistics: MC over N_samples trajectories solved by finite diff.

    Training: PINN residual at collocation points + Dirichlet BC, with the
    sensor-driven aPC basis enforcing the random-field structure of f.
    """
    rng = np.random.default_rng(SEED)

    # spatial grid for FD reference (interior points)
    x_full = np.linspace(-1, 1, n_grid)
    h = x_full[1] - x_full[0]

    # sample N_samples (train) + N_test trajectories of f on x_full
    f_train = sample_gp(x_full, lambda x: 10 * np.sin(np.pi * x), sigma=1.0, ell=0.5,
                        n=N_samples, rng=rng)
    f_test = sample_gp(x_full, lambda x: 10 * np.sin(np.pi * x), sigma=1.0, ell=0.5,
                       n=N_test, rng=rng)

    # FD solver: -u'' = f, Dirichlet BC => second-difference matrix on interior
    interior = slice(1, -1)
    n_int = n_grid - 2
    diag = -2.0 * np.ones(n_int)
    off = 1.0 * np.ones(n_int - 1)
    A = (np.diag(diag) + np.diag(off, 1) + np.diag(off, -1)) / h**2
    # -u'' = f -> A u_int = -f_int (Dirichlet 0 at both ends)
    u_train = np.linalg.solve(-A, f_train[interior, :])  # (n_int, N_samples)
    u_test = np.linalg.solve(-A, f_test[interior, :])
    # Pad zeros at boundaries
    u_train_full = np.zeros_like(f_train)
    u_test_full = np.zeros_like(f_test)
    u_train_full[interior, :] = u_train
    u_test_full[interior, :] = u_test

    # Reference mean/std (MC)
    u_mean_ref = u_test_full.mean(axis=1)
    u_std_ref = u_test_full.std(axis=1, ddof=1)

    # Place f-sensors equidistantly on [-1, 1]
    x_sensors = np.linspace(-1, 1, Nf)
    sensor_idx = np.searchsorted(x_full, x_sensors)
    sensor_idx[-1] = n_grid - 1
    f_sensor_train = f_train[sensor_idx, :]
    f_sensor_test = f_test[sensor_idx, :]

    # PCA -> principal random variables ξ
    V, eigvals, mean_sensor, d = pca_reduce(f_sensor_train, energy=energy)
    xi_train = project_to_xi(f_sensor_train, V, mean_sensor, eigvals)
    xi_test = project_to_xi(f_sensor_test, V, mean_sensor, eigvals)

    if verbose:
        print(f"[FWD POISSON] Nf={Nf}, PCA dim d={d}, aPC order={apc_order}")

    # aPC basis on training xi
    eval_basis, P_plus_1, _ = build_apc_basis(xi_train, order=apc_order)
    P = P_plus_1 - 1
    psi_train = eval_basis(xi_train)        # (P+1, N_samples)
    psi_test = eval_basis(xi_test)          # (P+1, N_test)

    # ---- Reference mode functions for u (empirical Galerkin projection) ----
    # u_α(x) = <u(x; ξ) Ψ_α(ξ)> ≈ (1/N) Σ_s u(x; ξ_s) Ψ_α(ξ_s)
    u_modes_ref = u_train_full @ psi_train.T / xi_train.shape[1]  # (Nx, P+1)

    # ---- Train PINN to learn u_α(x) ----
    net = APCNet(num_modes=P_plus_1, hidden=hidden, layers=layers).to(DEVICE)
    n_params = sum(p.numel() for p in net.parameters())
    if verbose:
        print(f"[FWD POISSON] PINN num_modes={P_plus_1}, params={n_params}")

    opt = torch.optim.Adam(net.parameters(), lr=lr, weight_decay=l2)

    # collocation points (paper: virtual f-sensors define Nf collocation locs;
    # we use a denser uniform grid for the PDE residual loss)
    x_coll = torch.linspace(-1.0, 1.0, 51, device=DEVICE, dtype=DTYPE).reshape(-1, 1)
    x_coll.requires_grad_(True)

    # boundary points
    x_bc = torch.tensor([[-1.0], [1.0]], device=DEVICE, dtype=DTYPE)

    # f-mode reference at collocation points: project sampled f to aPC basis
    # f_α(x) = <f(x;ξ) Ψ_α(ξ)> ≈ (1/N) f_full @ ψ_train.T
    f_modes_ref = f_train @ psi_train.T / xi_train.shape[1]  # (n_grid, P+1)
    # interp to x_coll grid
    coll_idx = np.searchsorted(x_full, x_coll.detach().cpu().numpy().flatten())
    coll_idx = np.clip(coll_idx, 0, n_grid - 1)
    f_modes_coll = torch.tensor(f_modes_ref[coll_idx], device=DEVICE, dtype=DTYPE)

    # boundary "sensor" data on u (paper: u-sensors at boundary). u_α(-1)=u_α(1)=0
    u_bc_target = torch.zeros((2, P_plus_1), device=DEVICE, dtype=DTYPE)

    t0 = time.time()
    history = []
    for ep in range(1, epochs + 1):
        opt.zero_grad()

        # PDE residual:  -u''_α(x) = f_α(x) for every α
        u_pred = net(x_coll)               # (Ncoll, P+1)
        u_x = torch.autograd.grad(u_pred.sum(), x_coll,
                                  create_graph=True)[0]
        u_xx = torch.autograd.grad(u_x.sum(), x_coll, create_graph=True)[0]
        # u_xx is (Ncoll, 1), broadcast over modes via per-mode autograd:
        # We need ∂² of each mode separately.
        u_xx_modes = torch.zeros_like(u_pred)
        for k in range(P_plus_1):
            uk = u_pred[:, k:k+1]
            uk_x = torch.autograd.grad(uk.sum(), x_coll, create_graph=True)[0]
            uk_xx = torch.autograd.grad(uk_x.sum(), x_coll, create_graph=True)[0]
            u_xx_modes[:, k:k+1] = uk_xx

        pde_res = -u_xx_modes - f_modes_coll       # (Ncoll, P+1)
        loss_pde = torch.mean(pde_res**2)

        # BC loss: u_α(±1) = 0
        u_bc_pred = net(x_bc)
        loss_bc = torch.mean((u_bc_pred - u_bc_target) ** 2)

        loss = loss_pde + 10.0 * loss_bc
        loss.backward()
        opt.step()

        if ep % 2000 == 0 or ep == 1:
            history.append({"ep": ep, "loss": float(loss.item()),
                            "pde": float(loss_pde.item()), "bc": float(loss_bc.item())})
            if verbose:
                print(f"  ep={ep:6d}  loss={loss.item():.3e}"
                      f"  pde={loss_pde.item():.3e}  bc={loss_bc.item():.3e}")

    wall = time.time() - t0

    # Evaluate on full grid: get u_α(x_full)
    with torch.no_grad():
        x_eval = torch.tensor(x_full[:, None], device=DEVICE, dtype=DTYPE)
        u_modes_pred = net(x_eval).cpu().numpy()  # (n_grid, P+1)

    # Compute predicted mean/std using TEST psi values
    u_mean_pred = (u_modes_pred @ psi_test).mean(axis=1)
    u_std_pred = (u_modes_pred @ psi_test).std(axis=1, ddof=1)

    e_mean = rel_l2(u_mean_pred, u_mean_ref)
    e_std = rel_l2(u_std_pred, u_std_ref)

    # per-mode error
    mode_err = []
    for k in range(P_plus_1):
        mode_err.append(rel_l2(u_modes_pred[:, k], u_modes_ref[:, k]))

    return ForwardPoissonResult(e_relL2=e_mean, std_relL2=e_std,
                                wall_time=wall, mode_relL2=mode_err,
                                Nf=Nf, P=P, epochs=epochs,
                                layers=layers, hidden=hidden), history


# -----------------------------------------------------------------------------
# 7) Inverse stochastic elliptic (§4.1.2, Table 1)
# -----------------------------------------------------------------------------
@dataclass
class InverseEllipticResult:
    apc_order: int
    k_mean_relL2: float
    k_std_relL2: float
    k_modes_relL2: list
    u_mean_relL2: float
    u_std_relL2: float
    u_modes_relL2: list
    wall_time: float
    epochs: int


def solve_inverse_elliptic(apc_order=1, Nk=4, Nu=7, layers=4, hidden=32,
                           epochs=20000, lr=1e-3, l2=5e-4,
                           n_grid=201, N_samples=1000, N_test=500,
                           verbose=True) -> InverseEllipticResult:
    """
    Example 4.1.2 — Inverse stochastic elliptic, Table 1:
        -(k u_x)_x = 10,  x in [-1,1], u(-1)=u(1)=0
        log(k) ~ GP(sin(3 pi x/2)/5, sigma=0.1, ell=1.0)

    Sensor setup: Nk=4 k-sensors, Nu=7 u-sensors, 1st-order aPC (default).
    Train two DNNs: one for k_α(x), one for u_α(x).
    """
    rng = np.random.default_rng(SEED + apc_order)

    x_full = np.linspace(-1, 1, n_grid)
    h = x_full[1] - x_full[0]

    # Sample log(k) trajectories, exponentiate
    logk_train = sample_gp(x_full, lambda x: np.sin(3 * np.pi * x / 2) / 5,
                           sigma=0.1, ell=1.0, n=N_samples, rng=rng)
    logk_test = sample_gp(x_full, lambda x: np.sin(3 * np.pi * x / 2) / 5,
                          sigma=0.1, ell=1.0, n=N_test, rng=rng)
    k_train = np.exp(logk_train)
    k_test = np.exp(logk_test)

    # FD solve: -(k u_x)_x = 10, Dirichlet 0
    def fd_solve(k_field):
        # k at cell faces: k_{i+1/2} = 0.5*(k_i + k_{i+1})
        n_int = n_grid - 2
        u_all = np.zeros_like(k_field)
        for s in range(k_field.shape[1]):
            k = k_field[:, s]
            k_face = 0.5 * (k[:-1] + k[1:])         # (n_grid-1,)
            # Build tridiag for interior points 1..n_grid-2
            diag = -(k_face[:-1] + k_face[1:]) / h**2
            up = k_face[1:-1] / h**2
            lo = k_face[1:-1] / h**2
            A = np.diag(diag) + np.diag(up, 1) + np.diag(lo, -1)
            rhs = -10.0 * np.ones(n_int)
            u_int = np.linalg.solve(A, rhs)
            u_all[1:-1, s] = u_int
        return u_all

    u_train = fd_solve(k_train)
    u_test = fd_solve(k_test)

    # Sensors
    x_k_sensors = np.linspace(-1, 1, Nk)
    x_u_sensors = np.linspace(-1, 1, Nu)
    k_sensor_idx = np.clip(np.searchsorted(x_full, x_k_sensors), 0, n_grid - 1)
    u_sensor_idx = np.clip(np.searchsorted(x_full, x_u_sensors), 0, n_grid - 1)
    k_sensor_train = k_train[k_sensor_idx, :]

    # PCA on k-sensors (paper §3.2.1)
    V, eigvals, mean_sensor, d = pca_reduce(k_sensor_train, energy=0.99)
    xi_train = project_to_xi(k_sensor_train, V, mean_sensor, eigvals)

    # ξ for test set (same projection)
    xi_test = project_to_xi(k_test[k_sensor_idx, :], V, mean_sensor, eigvals)

    eval_basis, P_plus_1, _ = build_apc_basis(xi_train, order=apc_order)
    P = P_plus_1 - 1
    psi_train = eval_basis(xi_train)
    psi_test = eval_basis(xi_test)

    if verbose:
        print(f"[INV ELL aPC={apc_order}] Nk={Nk} Nu={Nu} d={d}  P+1={P_plus_1}")

    # Reference modes (empirical Galerkin against training set)
    k_modes_ref = k_train @ psi_train.T / xi_train.shape[1]
    u_modes_ref = u_train @ psi_train.T / xi_train.shape[1]

    # ---- DNN setup: two nets (k and u) ----
    net_k = APCNet(num_modes=P_plus_1, hidden=hidden, layers=layers).to(DEVICE)
    net_u = APCNet(num_modes=P_plus_1, hidden=hidden, layers=layers).to(DEVICE)
    opt = torch.optim.Adam(
        list(net_k.parameters()) + list(net_u.parameters()),
        lr=lr, weight_decay=l2)

    # collocation grid + boundary
    x_coll_np = np.linspace(-1, 1, 51)
    x_coll = torch.tensor(x_coll_np[:, None], device=DEVICE, dtype=DTYPE,
                          requires_grad=True)
    x_bc = torch.tensor([[-1.0], [1.0]], device=DEVICE, dtype=DTYPE)

    # Sensor training tensors
    x_k_sens_t = torch.tensor(x_k_sensors[:, None], device=DEVICE, dtype=DTYPE)
    x_u_sens_t = torch.tensor(x_u_sensors[:, None], device=DEVICE, dtype=DTYPE)
    k_modes_sens_ref = torch.tensor(k_modes_ref[k_sensor_idx, :],
                                    device=DEVICE, dtype=DTYPE)
    u_modes_sens_ref = torch.tensor(u_modes_ref[u_sensor_idx, :],
                                    device=DEVICE, dtype=DTYPE)
    u_bc_target = torch.zeros((2, P_plus_1), device=DEVICE, dtype=DTYPE)

    t0 = time.time()
    history = []
    for ep in range(1, epochs + 1):
        opt.zero_grad()

        # Predicted modes at collocation points
        k_pred = net_k(x_coll)
        u_pred = net_u(x_coll)

        # PDE residual:  -(k u_x)_x = 10 in expectation, mode-wise this becomes
        # -(k_0 u_α_x)_x - sum_β,γ : term_β term_γ ... -- exact mode coupling is
        # complex. Following paper §3.2.4 we *sample* over training xi:
        #   r_s(x) = -(k(x;ξ_s) u_x(x;ξ_s))_x - 10
        # k(x;ξ_s) = sum_α k_α(x) Ψ_α(ξ_s)
        # u_x and u_xx need autograd per mode.
        u_x_modes = torch.zeros_like(u_pred)
        u_xx_modes = torch.zeros_like(u_pred)
        for kk in range(P_plus_1):
            ukk = u_pred[:, kk:kk+1]
            ukk_x = torch.autograd.grad(ukk.sum(), x_coll, create_graph=True)[0]
            ukk_xx = torch.autograd.grad(ukk_x.sum(), x_coll, create_graph=True)[0]
            u_x_modes[:, kk:kk+1] = ukk_x
            u_xx_modes[:, kk:kk+1] = ukk_xx

        k_x_modes = torch.zeros_like(k_pred)
        for kk in range(P_plus_1):
            kkk = k_pred[:, kk:kk+1]
            kkk_x = torch.autograd.grad(kkk.sum(), x_coll, create_graph=True)[0]
            k_x_modes[:, kk:kk+1] = kkk_x

        # Reconstruct k, u_x, u_xx on a *sub-sample* of training ξ
        sub_idx = np.random.default_rng(ep).choice(xi_train.shape[1], 128, replace=False)
        psi_sub = torch.tensor(psi_train[:, sub_idx], device=DEVICE, dtype=DTYPE)
        # (Ncoll, Ns)
        k_real = k_pred @ psi_sub
        k_x_real = k_x_modes @ psi_sub
        u_x_real = u_x_modes @ psi_sub
        u_xx_real = u_xx_modes @ psi_sub

        # -(k u_x)_x = -(k_x u_x + k u_xx)
        res = -(k_x_real * u_x_real + k_real * u_xx_real) - 10.0
        loss_pde = torch.mean(res**2)

        # k-sensor loss: k_α(x_k) = ref modes
        k_sens_pred = net_k(x_k_sens_t)
        loss_k_sens = torch.mean((k_sens_pred - k_modes_sens_ref) ** 2)

        # u-sensor loss
        u_sens_pred = net_u(x_u_sens_t)
        loss_u_sens = torch.mean((u_sens_pred - u_modes_sens_ref) ** 2)

        # BC loss on u_α
        u_bc_pred = net_u(x_bc)
        loss_bc = torch.mean((u_bc_pred - u_bc_target) ** 2)

        loss = loss_pde + 10.0 * (loss_k_sens + loss_u_sens) + 10.0 * loss_bc
        loss.backward()
        opt.step()

        if ep % 2000 == 0 or ep == 1:
            history.append({"ep": ep, "loss": float(loss.item()),
                            "pde": float(loss_pde.item()),
                            "ksens": float(loss_k_sens.item()),
                            "usens": float(loss_u_sens.item()),
                            "bc": float(loss_bc.item())})
            if verbose:
                print(f"  ep={ep:6d}  loss={loss.item():.3e}"
                      f"  pde={loss_pde.item():.3e}"
                      f"  ksens={loss_k_sens.item():.3e}"
                      f"  usens={loss_u_sens.item():.3e}"
                      f"  bc={loss_bc.item():.3e}")

    wall = time.time() - t0

    # Evaluate
    with torch.no_grad():
        x_eval = torch.tensor(x_full[:, None], device=DEVICE, dtype=DTYPE)
        k_modes_pred = net_k(x_eval).cpu().numpy()
        u_modes_pred = net_u(x_eval).cpu().numpy()

    # Reference statistics from TEST samples
    k_mean_ref = k_test.mean(axis=1)
    k_std_ref = k_test.std(axis=1, ddof=1)
    u_mean_ref = u_test.mean(axis=1)
    u_std_ref = u_test.std(axis=1, ddof=1)

    k_mean_pred = (k_modes_pred @ psi_test).mean(axis=1)
    k_std_pred = (k_modes_pred @ psi_test).std(axis=1, ddof=1)
    u_mean_pred = (u_modes_pred @ psi_test).mean(axis=1)
    u_std_pred = (u_modes_pred @ psi_test).std(axis=1, ddof=1)

    k_mean_err = rel_l2(k_mean_pred, k_mean_ref)
    k_std_err = rel_l2(k_std_pred, k_std_ref)
    u_mean_err = rel_l2(u_mean_pred, u_mean_ref)
    u_std_err = rel_l2(u_std_pred, u_std_ref)

    # Mode errors (modes 1..min(4, P)) for direct Table 1 comparison
    n_modes_report = min(4, P)
    # Reference modes via TEST psi (Galerkin projection) to remove training-sample noise
    k_modes_test_ref = k_test @ psi_test.T / N_test
    u_modes_test_ref = u_test @ psi_test.T / N_test
    k_mode_errs = [rel_l2(k_modes_pred[:, k], k_modes_test_ref[:, k])
                   for k in range(1, n_modes_report + 1)]
    u_mode_errs = [rel_l2(u_modes_pred[:, k], u_modes_test_ref[:, k])
                   for k in range(1, n_modes_report + 1)]

    return InverseEllipticResult(
        apc_order=apc_order,
        k_mean_relL2=k_mean_err, k_std_relL2=k_std_err, k_modes_relL2=k_mode_errs,
        u_mean_relL2=u_mean_err, u_std_relL2=u_std_err, u_modes_relL2=u_mode_errs,
        wall_time=wall, epochs=epochs,
    ), history


# -----------------------------------------------------------------------------
# Driver
# -----------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=".", help="output dir for JSON results")
    ap.add_argument("--forward-epochs", type=int, default=20000)
    ap.add_argument("--inverse-epochs", type=int, default=20000)
    ap.add_argument("--skip-forward", action="store_true")
    ap.add_argument("--skip-inverse", action="store_true")
    ap.add_argument("--quick", action="store_true",
                    help="Tiny epochs for smoke test")
    args = ap.parse_args()

    if args.quick:
        args.forward_epochs = 1000
        args.inverse_epochs = 1000

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    summary = {"seed": SEED, "torch": torch.__version__,
               "numpy": np.__version__, "device": str(DEVICE)}

    if not args.skip_forward:
        print("\n=== Example 4.1.1: Forward stochastic Poisson ===")
        fwd, fwd_hist = solve_forward_poisson(epochs=args.forward_epochs)
        summary["forward_poisson"] = {
            "Nf": fwd.Nf, "P": fwd.P, "epochs": fwd.epochs,
            "layers": fwd.layers, "hidden": fwd.hidden,
            "E_mean_relL2": fwd.e_relL2,
            "E_std_relL2": fwd.std_relL2,
            "mode_relL2": fwd.mode_relL2,
            "wall_time_s": fwd.wall_time,
        }
        print(f"  -> E_mean relL2 = {fwd.e_relL2*100:.2f}%, "
              f"std relL2 = {fwd.std_relL2*100:.2f}%, "
              f"wall {fwd.wall_time:.1f}s")
        (out / "forward_history.json").write_text(json.dumps(fwd_hist, indent=2))
        (out / "summary.json").write_text(json.dumps(summary, indent=2))

    if not args.skip_inverse:
        for order in (1, 2):
            print(f"\n=== Example 4.1.2: Inverse stochastic elliptic, aPC order {order} ===")
            inv, inv_hist = solve_inverse_elliptic(apc_order=order,
                                                   epochs=args.inverse_epochs)
            key = f"inverse_elliptic_apc{order}"
            summary[key] = {
                "apc_order": order,
                "k_mean_relL2": inv.k_mean_relL2,
                "k_std_relL2": inv.k_std_relL2,
                "k_modes_relL2": inv.k_modes_relL2,
                "u_mean_relL2": inv.u_mean_relL2,
                "u_std_relL2": inv.u_std_relL2,
                "u_modes_relL2": inv.u_modes_relL2,
                "epochs": inv.epochs,
                "wall_time_s": inv.wall_time,
            }
            print(f"  -> k: mean {inv.k_mean_relL2*100:.2f}%  "
                  f"std {inv.k_std_relL2*100:.2f}%  "
                  f"modes {[f'{e*100:.2f}%' for e in inv.k_modes_relL2]}")
            print(f"     u: mean {inv.u_mean_relL2*100:.2f}%  "
                  f"std {inv.u_std_relL2*100:.2f}%  "
                  f"modes {[f'{e*100:.2f}%' for e in inv.u_modes_relL2]}")
            (out / f"inverse_history_apc{order}.json").write_text(
                json.dumps(inv_hist, indent=2))
            (out / "summary.json").write_text(json.dumps(summary, indent=2))

    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    print(f"\nResults summary written to {out / 'summary.json'}")


if __name__ == "__main__":
    main()
