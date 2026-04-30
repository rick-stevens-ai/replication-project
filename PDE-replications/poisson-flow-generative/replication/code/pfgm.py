#!/usr/bin/env python3
"""
PFGM — Poisson Flow Generative Model (2D toy replication)
Based on Xu et al. 2022, NeurIPS (arXiv:2209.11178)

Core idea: data points in R^N are treated as charges on z=0 in R^{N+1}.
The Poisson/electric field they generate defines an ODE whose backward
integration maps uniform samples on a hemisphere to the data distribution.

This file implements the full training loop on 2D toy data (N=2).
"""

import torch
import torch.nn as nn
import numpy as np
import json
import os
import argparse
from pathlib import Path


# ── Data generation ──────────────────────────────────────────────────────

def make_mog_data(n_samples=10000, seed=42):
    """8-mode mixture of Gaussians arranged in a circle."""
    rng = np.random.RandomState(seed)
    n_modes = 8
    radius = 3.0
    std = 0.3
    angles = np.linspace(0, 2 * np.pi, n_modes, endpoint=False)
    centers = np.stack([radius * np.cos(angles), radius * np.sin(angles)], axis=1)
    assignments = rng.randint(0, n_modes, size=n_samples)
    samples = centers[assignments] + rng.randn(n_samples, 2) * std
    return samples.astype(np.float32)


# ── Network ──────────────────────────────────────────────────────────────

class PFGMNet(nn.Module):
    """
    Predicts the negative normalized Poisson field v(x̃) ∈ R^{N+1}.
    Input: (x, z) ∈ R^{N+1}  (here N=2, so input dim = 3).
    Output: v ∈ R^{N+1} (unit-norm direction, scaled by sqrt(N)).
    """

    def __init__(self, data_dim=2, hidden=256, n_layers=4):
        super().__init__()
        layers = []
        in_dim = data_dim + 1  # x and z
        for i in range(n_layers):
            out_dim = hidden
            layers.append(nn.Linear(in_dim, out_dim))
            layers.append(nn.SiLU())
            in_dim = out_dim
        layers.append(nn.Linear(hidden, data_dim + 1))
        self.net = nn.Sequential(*layers)

    def forward(self, x_aug):
        """x_aug: (batch, N+1) — concatenation of [x, z]."""
        return self.net(x_aug)


# ── Perturbation kernel (Algorithm 2 from the paper) ─────────────────────

def perturb(x, data_dim=2, M=120, sigma=0.2, tau=0.03):
    """
    Perturb data point x ∈ R^N to (y, z) ∈ R^{N+1} (Eq. 5 / Algorithm 2).

    For 2D toy data, we adjust hyperparameters so that perturbed points
    reach z values comparable to z_max used during sampling.

    The paper's formula:
      y = x + eps_x + ||x|| * (1+tau)^m * u_{1:N}
      z = |eps_z| * (1+tau)^m

    With M=120, tau=0.03: (1.03)^120 ≈ 34.7, max z ≈ sigma * 34.7 ≈ 7.0
    This matches our z_max = 10.

    x: (batch, N)
    Returns: y_tilde (batch, N+1) = (y, z)
    """
    batch = x.shape[0]
    device = x.device

    # sample power m ~ U[0, M]
    m = torch.rand(batch, 1, device=device) * M

    # sample noise eps = (eps_x, eps_z) ~ N(0, sigma^2 I_{N+1})
    eps = torch.randn(batch, data_dim + 1, device=device) * sigma
    eps_x = eps[:, :data_dim]  # (batch, N)
    eps_z = eps[:, data_dim:]  # (batch, 1)

    # sample u ~ Uniform(S^N(1)) — unit vector in R^{N+1}
    u = torch.randn(batch, data_dim + 1, device=device)
    u = u / (u.norm(dim=1, keepdim=True) + 1e-10)

    # compute perturbation scale
    x_norm = x.norm(dim=1, keepdim=True).clamp(min=1e-6)  # ||x||
    scale = (1.0 + tau) ** m  # (batch, 1)

    # construct perturbed point
    y = x + eps_x + x_norm * scale * u[:, :data_dim]
    z = eps_z.abs() * scale  # (batch, 1) — always positive

    y_tilde = torch.cat([y, z], dim=1)  # (batch, N+1)
    return y_tilde


# ── Empirical normalized field ───────────────────────────────────────────

def compute_normalized_field(y_tilde, data_aug, data_dim=2, gamma=1e-4):
    """
    Compute the empirical negative normalized Poisson field v_B(y_tilde).

    The paper's field:
      Ê(x̃) = c(x̃) * sum_i (x̃ - x̃_i) / ||x̃ - x̃_i||^{N+1}
      c(x̃) = 1 / sum_i 1/||x̃ - x̃_i||^{N+1}
      v(x̃) = -sqrt(N) * Ê(x̃) / ||Ê(x̃)||

    y_tilde: (batch_perturbed, N+1) — perturbed points
    data_aug: (batch_large, N+1) — augmented data (x, 0)

    Returns: v (batch_perturbed, N+1)
    """
    N = data_dim
    # diff: (B, BL, N+1)
    diff = y_tilde.unsqueeze(1) - data_aug.unsqueeze(0)
    dist = diff.norm(dim=2, keepdim=True).clamp(min=1e-10)  # (B, BL, 1)

    # weight_i = 1 / ||diff_i||^{N+1}
    weight = 1.0 / (dist ** (N + 1))  # (B, BL, 1)

    # c(x̃) = 1 / sum_i weight_i  (normalizer for numerical stability)
    c = 1.0 / (weight.sum(dim=1, keepdim=True) + 1e-10)  # (B, 1, 1)

    # Ê = c * sum_i (diff_i * weight_i)
    E_hat = (c * (diff * weight)).sum(dim=1)  # (B, N+1)

    # v = -sqrt(N) * Ê / ||Ê||
    E_norm = E_hat.norm(dim=1, keepdim=True).clamp(min=gamma)
    v = -np.sqrt(N) * E_hat / E_norm

    return v


# ── Sampling ─────────────────────────────────────────────────────────────

def sample_prior(n_samples, data_dim=2, z_max=10.0, device='cpu', clip_norm=50.0):
    """
    Sample from the prior on the z=z_max hyperplane.

    p_prior(x) = 2*z_max / (S_N(1) * (||x||^2 + z_max^2)^{(N+1)/2})

    This is obtained by radially projecting the uniform distribution
    on the upper hemisphere onto z=z_max.

    The paper clips initial sample norms: "we further clip the norms of
    initial samples into (0, 3000) for CIFAR-10".
    For 2D data, we use clip_norm=50 (5x z_max).
    """
    N = data_dim

    # For N=2: p(r) ∝ r / (r^2 + z_max^2)^{3/2}
    # CDF: F(r) = 1 - z_max / sqrt(r^2 + z_max^2)
    # Inverse CDF: r = z_max * sqrt(1/(1-u)^2 - 1)
    u = torch.rand(n_samples, device=device).clamp(min=1e-6, max=1 - 1e-6)
    radii = z_max * torch.sqrt(1.0 / (1.0 - u) ** 2 - 1.0)

    # Clip radii (analogous to paper's norm clipping)
    radii = radii.clamp(max=clip_norm)

    # Uniform angle on S^{N-1}
    angles = torch.randn(n_samples, N, device=device)
    angles = angles / (angles.norm(dim=1, keepdim=True) + 1e-10)

    x = radii.unsqueeze(1) * angles
    z = torch.full((n_samples, 1), z_max, device=device)

    return torch.cat([x, z], dim=1)


@torch.no_grad()
def sample_pfgm(model, n_samples=2000, data_dim=2,
                z_max=10.0, z_min=1e-3, dt=0.01,
                device='cpu', use_log_z=True):
    """
    Generate samples via backward ODE (Eq. 6).

    The backward ODE with log-z change of variable:
        d(x, z) = (v_x / v_z * z, z) dt'
        where z = e^{t'}, t' goes from log(z_max) to log(z_min).

    The v_x/v_z ratio gives the direction of x change per unit z change,
    and the factor z comes from the exponential parameterization.
    """
    model.eval()

    x_aug = sample_prior(n_samples, data_dim, z_max, device)

    if use_log_z:
        t_start = np.log(z_max)
        t_end = np.log(z_min)
        n_steps = max(int((t_start - t_end) / dt), 10)
        dt_actual = (t_start - t_end) / n_steps

        for i in range(n_steps):
            v = model(x_aug)
            v_x = v[:, :data_dim]
            v_z = v[:, data_dim:]
            z_current = x_aug[:, data_dim:]

            # v_z should be negative (pointing toward z=0)
            # dx/dt' = v_x / v_z * z
            # dz/dt' = z
            # stepping backward: dt' < 0
            safe_vz = v_z.clone()
            mask = safe_vz.abs() < 1e-6
            safe_vz[mask] = -1e-6 * safe_vz[mask].sign()
            safe_vz[safe_vz == 0] = -1e-6

            dx = v_x / safe_vz * z_current * (-dt_actual)
            dz = z_current * (-dt_actual)

            new_x = x_aug[:, :data_dim] + dx
            new_z = (x_aug[:, data_dim:] + dz).clamp(min=z_min * 0.1)

            x_aug = torch.cat([new_x, new_z], dim=1)
    else:
        # Simple Euler on z directly
        n_steps = max(int((z_max - z_min) / dt), 10)
        dz_step = -(z_max - z_min) / n_steps

        for i in range(n_steps):
            v = model(x_aug)
            v_x = v[:, :data_dim]
            v_z = v[:, data_dim:]

            safe_vz = v_z.clone()
            mask = safe_vz.abs() < 1e-6
            safe_vz[mask] = -1e-6 * safe_vz[mask].sign()
            safe_vz[safe_vz == 0] = -1e-6

            dx = v_x / safe_vz * dz_step
            new_x = x_aug[:, :data_dim] + dx
            new_z = (x_aug[:, data_dim:] + dz_step).clamp(min=z_min * 0.1)

            x_aug = torch.cat([new_x, new_z], dim=1)

    return x_aug[:, :data_dim].cpu().numpy()


@torch.no_grad()
def sample_pfgm_euler_raw(model, n_samples=2000, data_dim=2,
                          z_max=10.0, z_min=1e-3, n_steps=100,
                          device='cpu'):
    """
    Generate samples via simple Euler integration on z (no log transform).
    Used for step-size robustness comparison (directly controls n_steps → dt).
    """
    model.eval()
    x_aug = sample_prior(n_samples, data_dim, z_max, device)

    dz_step = -(z_max - z_min) / n_steps

    for i in range(n_steps):
        v = model(x_aug)
        v_x = v[:, :data_dim]
        v_z = v[:, data_dim:]

        safe_vz = v_z.clone()
        mask = safe_vz.abs() < 1e-6
        safe_vz[mask] = -1e-6 * safe_vz[mask].sign()
        safe_vz[safe_vz == 0] = -1e-6

        dx = v_x / safe_vz * dz_step
        new_x = x_aug[:, :data_dim] + dx
        new_z = (x_aug[:, data_dim:] + dz_step).clamp(min=z_min * 0.1)

        x_aug = torch.cat([new_x, new_z], dim=1)

    return x_aug[:, :data_dim].cpu().numpy()


# ── Training loop ────────────────────────────────────────────────────────

def train_pfgm(data, epochs=300, batch_size=512, batch_large_mult=4,
               lr=1e-3, data_dim=2, M=120, sigma=0.2, tau=0.03,
               gamma=1e-4, device='cpu', verbose=True):
    """
    Train the PFGM network (Algorithm 1 from the paper).

    data: (n_samples, N) numpy array
    """
    model = PFGMNet(data_dim=data_dim, hidden=256, n_layers=4).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

    data_tensor = torch.tensor(data, dtype=torch.float32, device=device)
    n = data_tensor.shape[0]

    losses = []

    for epoch in range(epochs):
        perm = torch.randperm(n, device=device)
        epoch_loss = 0.0
        n_batches = 0

        for start in range(0, n, batch_size):
            end = min(start + batch_size, n)
            batch_idx = perm[start:end]
            x_batch = data_tensor[batch_idx]
            B = x_batch.shape[0]

            # Large batch for field estimation
            BL = min(B * batch_large_mult, n)
            large_idx = torch.randperm(n, device=device)[:BL]
            x_large = data_tensor[large_idx]

            # Augment large batch: (x, 0)
            data_aug = torch.cat([x_large, torch.zeros(BL, 1, device=device)], dim=1)

            # Perturb batch data (Algorithm 2)
            y_tilde = perturb(x_batch, data_dim=data_dim, M=M, sigma=sigma, tau=tau)

            # Compute target: normalized field from large batch
            with torch.no_grad():
                v_target = compute_normalized_field(y_tilde, data_aug,
                                                    data_dim=data_dim, gamma=gamma)

            # Forward pass
            v_pred = model(y_tilde)

            # MSE loss
            loss = ((v_pred - v_target) ** 2).sum(dim=1).mean()

            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()

            epoch_loss += loss.item()
            n_batches += 1

        scheduler.step()
        avg_loss = epoch_loss / max(n_batches, 1)
        losses.append(avg_loss)

        if verbose and (epoch + 1) % 50 == 0:
            print(f"  Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.6f}")

    return model, losses


# ── Main ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='PFGM 2D Toy Replication')
    parser.add_argument('--epochs', type=int, default=300)
    parser.add_argument('--batch_size', type=int, default=512)
    parser.add_argument('--n_train', type=int, default=20000)
    parser.add_argument('--n_samples', type=int, default=5000)
    parser.add_argument('--lr', type=float, default=1e-3)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--device', type=str, default='auto')
    parser.add_argument('--save_dir', type=str, default='../results')
    parser.add_argument('--model_path', type=str, default='../results/pfgm_model.pt')
    args = parser.parse_args()

    if args.device == 'auto':
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
    else:
        device = args.device

    torch.manual_seed(args.seed)
    np.random.seed(args.seed)

    print("=" * 60)
    print("PFGM — Poisson Flow Generative Model (2D Toy)")
    print("=" * 60)

    data = make_mog_data(n_samples=args.n_train, seed=args.seed)
    print(f"\n[1] Data: {data.shape}, range: [{data.min():.2f}, {data.max():.2f}]")

    print(f"\n[2] Training PFGM (epochs={args.epochs}, device={device})...")
    model, losses = train_pfgm(
        data, epochs=args.epochs, batch_size=args.batch_size,
        lr=args.lr, device=device
    )

    os.makedirs(os.path.dirname(args.model_path), exist_ok=True)
    torch.save({
        'model_state_dict': model.state_dict(),
        'losses': losses,
        'args': vars(args),
    }, args.model_path)

    print(f"\n[3] Generating {args.n_samples} samples...")
    samples = sample_pfgm(model, n_samples=args.n_samples, device=device,
                          z_max=10.0, z_min=1e-3, dt=0.01)

    os.makedirs(args.save_dir, exist_ok=True)
    np.save(os.path.join(args.save_dir, 'pfgm_samples.npy'), samples)
    np.save(os.path.join(args.save_dir, 'pfgm_train_data.npy'), data)

    with open(os.path.join(args.save_dir, 'pfgm_losses.json'), 'w') as f:
        json.dump({'losses': losses}, f, indent=2)

    print("Done.")


if __name__ == '__main__':
    main()
