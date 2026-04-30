#!/usr/bin/env python3
"""
Score-based Diffusion Model baseline (VE-SDE variant) for 2D toy data.

Implements a minimal Variance-Exploding score-based diffusion model
(Song et al. 2021, "Score-based generative modeling through SDEs")
for direct comparison with PFGM on the same 2D toy dataset.

Training: denoising score matching at multiple noise levels.
Sampling: reverse-time ODE (probability flow ODE) with Euler method.
"""

import torch
import torch.nn as nn
import numpy as np
import json
import os
import argparse
from pathlib import Path


# ── Data generation (same as pfgm.py) ───────────────────────────────────

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

class ScoreNet(nn.Module):
    """
    Score network s_θ(x, σ) that estimates ∇_x log p_σ(x).
    Input: x ∈ R^N concatenated with log(σ) (scalar) → R^{N+1}
    Output: score ∈ R^N
    """
    def __init__(self, data_dim=2, hidden=256, n_layers=4):
        super().__init__()
        layers = []
        in_dim = data_dim + 1  # x and log(sigma)
        for i in range(n_layers):
            out_dim = hidden
            layers.append(nn.Linear(in_dim, out_dim))
            layers.append(nn.SiLU())
            in_dim = out_dim
        layers.append(nn.Linear(hidden, data_dim))
        self.net = nn.Sequential(*layers)

    def forward(self, x, sigma):
        """
        x: (batch, N)
        sigma: (batch, 1) or (batch,)
        """
        if sigma.dim() == 1:
            sigma = sigma.unsqueeze(1)
        log_sigma = torch.log(sigma.clamp(min=1e-10))
        inp = torch.cat([x, log_sigma], dim=1)
        return self.net(inp)


# ── VE noise schedule ───────────────────────────────────────────────────

def get_sigma_schedule(sigma_min=0.01, sigma_max=10.0, n_levels=100):
    """Geometric sequence of noise levels for VE-SDE."""
    return np.geomspace(sigma_min, sigma_max, n_levels).astype(np.float32)


# ── Denoising score matching loss ────────────────────────────────────────

def dsm_loss(model, x_batch, sigma_min=0.01, sigma_max=10.0, device='cpu'):
    """
    Denoising score matching at random noise levels.

    For VE: x_noisy = x + sigma * eps, eps ~ N(0, I)
    Target score: -eps / sigma = (x - x_noisy) / sigma^2
    Loss: sigma^2 * ||s_θ(x_noisy, sigma) - (-eps/sigma)||^2
          = ||sigma * s_θ(x_noisy, sigma) + eps||^2

    This is equivalent to the standard weighted DSM loss.
    """
    batch = x_batch.shape[0]

    # Sample random sigma (uniform in log-space)
    log_sigma = torch.rand(batch, 1, device=device) * (
        np.log(sigma_max) - np.log(sigma_min)) + np.log(sigma_min)
    sigma = torch.exp(log_sigma)

    # Add noise
    eps = torch.randn_like(x_batch)
    x_noisy = x_batch + sigma * eps

    # Predict score
    score_pred = model(x_noisy, sigma)

    # Target: -eps / sigma
    target = -eps / sigma

    # Weighted loss: sigma^2 * ||score - target||^2
    loss = (sigma ** 2 * (score_pred - target) ** 2).sum(dim=1).mean()

    return loss


# ── Sampling (probability flow ODE) ─────────────────────────────────────

@torch.no_grad()
def sample_diffusion(model, n_samples=2000, data_dim=2,
                     sigma_min=0.01, sigma_max=10.0,
                     n_steps=1000, device='cpu'):
    """
    Sample via the VE probability flow ODE:
        dx = -σ̇(t) σ(t) ∇_x log p_{σ(t)}(x) dt

    With σ(t) = σ_min * (σ_max/σ_min)^t for t ∈ [0, 1],
    we integrate backward from t=1 to t=0.

    Using Euler discretization with n_steps.
    """
    model.eval()

    # Initialize from N(0, sigma_max^2 * I)
    x = torch.randn(n_samples, data_dim, device=device) * sigma_max

    dt = 1.0 / n_steps  # stepping in t from 1 to 0

    for i in range(n_steps):
        t = 1.0 - i * dt  # current time
        t_next = t - dt

        # sigma(t) = sigma_min * (sigma_max / sigma_min)^t
        sigma_t = sigma_min * (sigma_max / sigma_min) ** t
        sigma_t_tensor = torch.full((n_samples, 1), sigma_t, device=device)

        # d(sigma)/dt = sigma * log(sigma_max / sigma_min)
        dsigma_dt = sigma_t * np.log(sigma_max / sigma_min)

        # Score prediction
        score = model(x, sigma_t_tensor)

        # dx = -dsigma_dt * sigma_t * score * (-dt)
        #     = dsigma_dt * sigma_t * score * dt  (backward)
        x = x + dsigma_dt * sigma_t * score * dt

    return x.cpu().numpy()


@torch.no_grad()
def sample_diffusion_euler(model, n_samples=2000, data_dim=2,
                           sigma_min=0.01, sigma_max=10.0,
                           n_steps=1000, device='cpu'):
    """
    Same as sample_diffusion but with explicit n_steps control
    for step-size robustness testing.
    """
    return sample_diffusion(model, n_samples, data_dim,
                            sigma_min, sigma_max, n_steps, device)


# ── Training ─────────────────────────────────────────────────────────────

def train_diffusion(data, epochs=300, batch_size=512, lr=1e-3,
                    sigma_min=0.01, sigma_max=10.0,
                    device='cpu', verbose=True):
    """Train the score-based diffusion model."""
    model = ScoreNet(data_dim=2, hidden=256, n_layers=4).to(device)
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

            loss = dsm_loss(model, x_batch, sigma_min, sigma_max, device)

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
    parser = argparse.ArgumentParser(description='Diffusion Baseline (VE-SDE) 2D')
    parser.add_argument('--epochs', type=int, default=300)
    parser.add_argument('--batch_size', type=int, default=512)
    parser.add_argument('--n_train', type=int, default=20000)
    parser.add_argument('--n_samples', type=int, default=5000)
    parser.add_argument('--lr', type=float, default=1e-3)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--device', type=str, default='auto')
    parser.add_argument('--save_dir', type=str, default='../results')
    parser.add_argument('--model_path', type=str, default='../results/diffusion_model.pt')
    args = parser.parse_args()

    if args.device == 'auto':
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
    else:
        device = args.device

    torch.manual_seed(args.seed)
    np.random.seed(args.seed)

    print("=" * 60)
    print("Score-Based Diffusion Model (VE-SDE) — 2D Toy Baseline")
    print("=" * 60)

    # Generate data
    print(f"\n[1] Generating 8-mode MoG data ({args.n_train} samples)...")
    data = make_mog_data(n_samples=args.n_train, seed=args.seed)
    print(f"    Data shape: {data.shape}")

    # Train
    print(f"\n[2] Training diffusion model (epochs={args.epochs}, device={device})...")
    model, losses = train_diffusion(
        data, epochs=args.epochs, batch_size=args.batch_size,
        lr=args.lr, device=device
    )

    # Save model
    os.makedirs(os.path.dirname(args.model_path), exist_ok=True)
    torch.save({
        'model_state_dict': model.state_dict(),
        'losses': losses,
        'args': vars(args),
    }, args.model_path)
    print(f"    Model saved to {args.model_path}")

    # Generate samples with default (fine) settings
    print(f"\n[3] Generating {args.n_samples} samples (n_steps=1000)...")
    samples = sample_diffusion(model, n_samples=args.n_samples, n_steps=1000, device=device)
    print(f"    Samples shape: {samples.shape}")

    # Save
    os.makedirs(args.save_dir, exist_ok=True)
    np.save(os.path.join(args.save_dir, 'diffusion_samples.npy'), samples)

    loss_data = {'losses': losses}
    with open(os.path.join(args.save_dir, 'diffusion_losses.json'), 'w') as f:
        json.dump(loss_data, f, indent=2)

    print(f"\n    Results saved to {args.save_dir}/")
    print("Done.")


if __name__ == '__main__':
    main()
