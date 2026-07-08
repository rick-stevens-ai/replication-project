"""Temporal-VAE baseline for ELM forecasting.

Architecture (~50-100k params):
  - ConvVAE encoder: 8x8 frame -> latent z (dim 16)
  - LSTM latent dynamics: rolls latent forward
  - ConvVAE decoder: z -> reconstructed 8x8 frame

Trained autoregressively with the same two-stage scheme as the main models
(direct one-step + H-step rollout) on the SAME synthetic dataset / split.

Loss = MSE(reconstruction) + beta * KL on encoder posterior.

Usage:
    python temporal_vae.py --out results
"""
from __future__ import annotations
import argparse
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader

sys.path.insert(0, os.path.dirname(__file__))
from data import build_datasets
from train import metrics, collect_predictions  # reuse


# --------------------------------------------------------------------------- #
class ConvEncoder(nn.Module):
    def __init__(self, hidden: int = 32, z_dim: int = 16):
        super().__init__()
        # 8x8 -> 8x8 -> 4x4 -> 2x2 -> flatten
        self.net = nn.Sequential(
            nn.Conv2d(1, hidden, 3, padding=1), nn.GELU(),
            nn.Conv2d(hidden, hidden, 4, stride=2, padding=1), nn.GELU(),  # 4x4
            nn.Conv2d(hidden, hidden, 4, stride=2, padding=1), nn.GELU(),  # 2x2
        )
        self.fc_mu = nn.Linear(hidden * 4, z_dim)
        self.fc_lv = nn.Linear(hidden * 4, z_dim)

    def forward(self, x):  # x: (B,1,8,8)
        h = self.net(x).flatten(1)
        return self.fc_mu(h), self.fc_lv(h)


class ConvDecoder(nn.Module):
    def __init__(self, hidden: int = 32, z_dim: int = 16):
        super().__init__()
        self.fc = nn.Linear(z_dim, hidden * 4)
        self.hidden = hidden
        self.net = nn.Sequential(
            nn.ConvTranspose2d(hidden, hidden, 4, stride=2, padding=1), nn.GELU(),  # 4x4
            nn.ConvTranspose2d(hidden, hidden, 4, stride=2, padding=1), nn.GELU(),  # 8x8
            nn.Conv2d(hidden, 1, 3, padding=1),
        )

    def forward(self, z):
        h = self.fc(z).view(-1, self.hidden, 2, 2)
        return self.net(h)  # (B,1,8,8)


class TemporalVAE(nn.Module):
    """Temporal VAE: encode each history frame -> z_t, evolve with LSTM,
    decode each predicted z_{t+i} to a frame."""
    def __init__(self, delta: int, H: int, hidden: int = 32, z_dim: int = 16,
                 lstm_hidden: int = 48, beta: float = 1e-3):
        super().__init__()
        self.delta = delta
        self.H = H
        self.z_dim = z_dim
        self.beta = beta
        self.enc = ConvEncoder(hidden, z_dim)
        self.dec = ConvDecoder(hidden, z_dim)
        self.lstm = nn.LSTM(z_dim, lstm_hidden, batch_first=True)
        self.lstm_out = nn.Linear(lstm_hidden, z_dim)
        # tracked KL diagnostic
        self.last_kl = torch.tensor(0.0)

    def reparam(self, mu, lv):
        if self.training:
            std = (0.5 * lv).exp()
            return mu + std * torch.randn_like(std)
        return mu

    def encode_history(self, hist):
        # hist: (B, T, 8, 8) -> z: (B, T, z_dim)
        B, T, Hs, Ws = hist.shape
        x = hist.reshape(B * T, 1, Hs, Ws)
        mu, lv = self.enc(x)
        z = self.reparam(mu, lv)
        # KL to standard normal
        kl = (-0.5 * (1 + lv - mu.pow(2) - lv.exp())).mean()
        self.last_kl = kl
        z = z.view(B, T, -1)
        return z

    def forward(self, hist, H=None):
        H = H or self.H
        z = self.encode_history(hist)            # (B, delta, z_dim)
        # Run LSTM through history to set state
        out, (h, c) = self.lstm(z)
        z_next = self.lstm_out(out[:, -1:])      # (B,1,z_dim) prediction of next
        outs = []
        cur = z_next
        for _ in range(H):
            frame = self.dec(cur.squeeze(1)).unsqueeze(1)   # (B,1,1,8,8)
            outs.append(frame.squeeze(2))                   # (B,1,8,8)
            # roll
            out, (h, c) = self.lstm(cur, (h, c))
            cur = self.lstm_out(out)
        return torch.cat(outs, dim=1)            # (B, H, 8, 8)


# --------------------------------------------------------------------------- #
def count_params(m):
    return sum(p.numel() for p in m.parameters() if p.requires_grad)


def train_vae(model, train_loader, val_loader, device,
              epochs_pre=6, epochs_ft=6, lr=1e-3, tag="VAE"):
    model = model.to(device)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    log = []
    print(f"[{tag}] Stage 1: 1-step pretrain ({epochs_pre} ep)")
    for ep in range(epochs_pre):
        model.train(); tloss = 0.0; n = 0
        for hist, targ in train_loader:
            hist = hist.to(device); targ = targ.to(device)
            pred = model(hist, H=1)
            recon = F.mse_loss(pred, targ[:, :1])
            loss = recon + model.beta * model.last_kl
            opt.zero_grad(); loss.backward(); opt.step()
            tloss += loss.item() * hist.size(0); n += hist.size(0)
        vloss = _eval_mse(model, val_loader, device, H=1)
        msg = f"[{tag}] pre ep{ep+1} train_loss={tloss/n:.5f} val_mse_1step={vloss:.5f}"
        print(msg); log.append(msg)
    print(f"[{tag}] Stage 2: AR rollout ({epochs_ft} ep)")
    for ep in range(epochs_ft):
        model.train(); tloss = 0.0; n = 0
        for hist, targ in train_loader:
            hist = hist.to(device); targ = targ.to(device)
            pred = model(hist)
            recon = F.mse_loss(pred, targ)
            loss = recon + model.beta * model.last_kl
            opt.zero_grad(); loss.backward(); opt.step()
            tloss += loss.item() * hist.size(0); n += hist.size(0)
        vloss = _eval_mse(model, val_loader, device, H=None)
        msg = f"[{tag}] ft  ep{ep+1} train_loss={tloss/n:.5f} val_mse_H={vloss:.5f}"
        print(msg); log.append(msg)
    return log


def _eval_mse(model, loader, device, H=None):
    model.eval(); tot = 0.0; n = 0
    with torch.no_grad():
        for hist, targ in loader:
            hist = hist.to(device); targ = targ.to(device)
            pred = model(hist, H=H) if H is not None else model(hist)
            t = targ[:, :pred.size(1)]
            tot += F.mse_loss(pred, t, reduction="sum").item()
            n += t.numel()
    return tot / max(n, 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results")
    ap.add_argument("--n_train", type=int, default=32)
    ap.add_argument("--n_val", type=int, default=4)
    ap.add_argument("--n_test", type=int, default=4)
    ap.add_argument("--T", type=int, default=80_000)
    ap.add_argument("--delta", type=int, default=30)
    ap.add_argument("--H", type=int, default=30)
    ap.add_argument("--stride", type=int, default=80)
    ap.add_argument("--max_per_shot", type=int, default=200)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--epochs_pre", type=int, default=6)
    ap.add_argument("--epochs_ft", type=int, default=6)
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = ap.parse_args()
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)

    print("[vae] building datasets (same seeds)...")
    train, val, test, norm = build_datasets(
        n_train=args.n_train, n_val=args.n_val, n_test=args.n_test,
        T=args.T, delta=args.delta, H=args.H, stride=args.stride,
        max_per_shot=args.max_per_shot,
    )
    train_loader = DataLoader(train, batch_size=args.batch, shuffle=True, num_workers=2, drop_last=True)
    val_loader   = DataLoader(val,   batch_size=args.batch, shuffle=False, num_workers=1)
    test_loader  = DataLoader(test,  batch_size=args.batch, shuffle=False, num_workers=1)

    model = TemporalVAE(args.delta, args.H, hidden=24, z_dim=16, lstm_hidden=48)
    print(f"[vae] params: {count_params(model):,}")

    log = train_vae(model, train_loader, val_loader, args.device,
                    epochs_pre=args.epochs_pre, epochs_ft=args.epochs_ft)
    p, t, l = collect_predictions(model, test_loader, args.device)
    res = metrics(p, t, l) | {
        "params": count_params(model),
        "train_log": log,
    }
    print(json.dumps({k: v for k, v in res.items() if k not in ("train_log", "mse_per_step")}, indent=2))

    torch.save(model.state_dict(), out / "tvae.pt")
    with open(out / "tvae_metrics.json", "w") as f:
        json.dump(res, f, indent=2)
    print("[vae] saved", out / "tvae_metrics.json")


if __name__ == "__main__":
    main()
