"""Simplified Latent SDE model following Fagin et al. 2024 (ApJ 2024) /
Li et al. 2020 (Scalable Gradients for SDEs).

Architecture (single-band simplification of the 6-band LSST paper):

  Encoder:  GRU over (y, err, mask, dt)  -> context c
            FC head -> (mu_q, log_var_q) for z0
  Latent SDE: posterior drift f_post(z, t, c), prior drift f_prior(z, t),
              diagonal diffusion g(z, t). Itô, Euler-Maruyama.
  Decoder:  MLP(z_t) -> (y_hat_t, log_sigma_hat_t)  at every grid time.

Training loss = reconstruction NLL (masked)
              + beta * KL between posterior and prior SDE (Girsanov, via
                augmented state in torchsde.sdeint_adjoint with method='logqp').
"""
from __future__ import annotations

import math
import torch
import torch.nn as nn
import torchsde


def _mlp(in_dim, out_dim, hidden=64, layers=2, act=nn.SiLU):
    mods = []
    d = in_dim
    for _ in range(layers):
        mods += [nn.Linear(d, hidden), act()]
        d = hidden
    mods += [nn.Linear(d, out_dim)]
    return nn.Sequential(*mods)


class LatentSDE(nn.Module):
    """Latent SDE with learned prior drift (Li et al. 2020)."""

    noise_type = "diagonal"
    sde_type = "ito"

    def __init__(self, latent_dim: int = 4, context_dim: int = 32, hidden: int = 64):
        super().__init__()
        self.latent_dim = latent_dim
        self.context_dim = context_dim
        # learned prior drift f_prior(z, t)
        self.f_prior = _mlp(latent_dim + 1, latent_dim, hidden=hidden, layers=2)
        # posterior drift f_post(z, t, c)
        self.f_post = _mlp(latent_dim + 1 + context_dim, latent_dim, hidden=hidden, layers=2)
        # diagonal diffusion g(z, t) – keep strictly positive via softplus
        self.g_net = _mlp(latent_dim + 1, latent_dim, hidden=hidden, layers=2)
        # context is set per forward pass
        self._ctx = None  # shape (B, context_dim)

    # ---- torchsde API (stateful context) ----
    def set_context(self, ctx: torch.Tensor):
        self._ctx = ctx

    def f(self, t, y):  # posterior drift
        t_vec = t.expand(y.shape[0], 1) if t.dim() == 0 else t.view(-1, 1).expand(y.shape[0], 1)
        inp = torch.cat([y, t_vec, self._ctx], dim=-1)
        return self.f_post(inp)

    def h(self, t, y):  # prior drift (for KL via logqp)
        t_vec = t.expand(y.shape[0], 1) if t.dim() == 0 else t.view(-1, 1).expand(y.shape[0], 1)
        inp = torch.cat([y, t_vec], dim=-1)
        return self.f_prior(inp)

    def g(self, t, y):
        t_vec = t.expand(y.shape[0], 1) if t.dim() == 0 else t.view(-1, 1).expand(y.shape[0], 1)
        inp = torch.cat([y, t_vec], dim=-1)
        # bound diffusion away from 0 and a big ceiling
        return 0.05 + torch.nn.functional.softplus(self.g_net(inp)) * 0.3


class Encoder(nn.Module):
    def __init__(self, input_dim: int = 4, hidden: int = 64, context_dim: int = 32, latent_dim: int = 4):
        super().__init__()
        self.rnn = nn.GRU(input_dim, hidden, batch_first=True, bidirectional=True)
        self.ctx_head = nn.Linear(2 * hidden, context_dim)
        self.z0_head = nn.Linear(2 * hidden, 2 * latent_dim)
        self.latent_dim = latent_dim

    def forward(self, feats, mask):
        # feats: (B, T, F), mask: (B, T)
        # GRU will process the full sequence; masking is approximated by zeroing
        # missing inputs (features already carry the 'mask' channel).
        out, _ = self.rnn(feats)
        # mean-pool over observed timesteps
        m = mask.unsqueeze(-1)
        pooled = (out * m).sum(dim=1) / m.sum(dim=1).clamp(min=1.0)
        ctx = self.ctx_head(pooled)
        z_params = self.z0_head(pooled)
        mu, log_var = z_params.chunk(2, dim=-1)
        log_var = log_var.clamp(-8.0, 4.0)
        return ctx, mu, log_var


class Decoder(nn.Module):
    def __init__(self, latent_dim: int = 4, hidden: int = 64):
        super().__init__()
        self.net = _mlp(latent_dim, 2, hidden=hidden, layers=2)

    def forward(self, zs):
        # zs: (T, B, latent_dim) -> (T, B, 2): [y_hat, log_sigma_hat]
        out = self.net(zs)
        mean = out[..., 0]
        log_sigma = out[..., 1].clamp(-5.0, 2.0)
        return mean, log_sigma


class LatentSDEModel(nn.Module):
    def __init__(self, input_dim=4, latent_dim=4, context_dim=32, hidden=64):
        super().__init__()
        self.encoder = Encoder(input_dim=input_dim, hidden=hidden,
                               context_dim=context_dim, latent_dim=latent_dim)
        self.sde = LatentSDE(latent_dim=latent_dim, context_dim=context_dim, hidden=hidden)
        self.decoder = Decoder(latent_dim=latent_dim, hidden=hidden)
        self.latent_dim = latent_dim

    def forward(self, feats, mask, t_grid, y_obs, err_obs, beta_kl=1.0, dt=0.05):
        """Single forward pass on one *shared* time grid (B all share same t_grid).

        feats: (B, T, F) encoder inputs
        mask : (B, T) – 1 where y_obs was observed, 0 otherwise
        t_grid: (T,) – normalised times used for the SDE (monotone)
        y_obs: (B, T), err_obs: (B, T)
        """
        B = feats.shape[0]
        ctx, mu0, log_var0 = self.encoder(feats, mask)
        std0 = torch.exp(0.5 * log_var0)
        eps = torch.randn_like(mu0)
        z0 = mu0 + eps * std0

        # KL(q(z0) || N(0, I))
        kl_z0 = 0.5 * (mu0.pow(2) + std0.pow(2) - 1.0 - log_var0).sum(dim=-1)  # (B,)

        self.sde.set_context(ctx)
        # sdeint with logqp=True returns both path and KL integrand (Girsanov)
        # It evaluates at t_grid points, integrating in between with step dt.
        zs, log_ratio = torchsde.sdeint(
            self.sde, z0, t_grid, method="euler", dt=dt, logqp=True, names={"drift": "f", "diffusion": "g", "prior_drift": "h"},
        )
        # zs: (T, B, latent_dim); log_ratio: (T-1, B)
        kl_path = log_ratio.sum(dim=0)  # (B,)

        mean, log_sigma = self.decoder(zs)  # (T, B)
        mean = mean.transpose(0, 1)  # (B, T)
        log_sigma = log_sigma.transpose(0, 1)

        # Combine model predictive sigma with observational error in quadrature.
        # Observation noise model: y_obs = y_true + N(0, err_obs^2),
        # and y_true ~ N(mean, sigma_hat^2).  =>  y_obs ~ N(mean, sigma_hat^2 + err^2).
        sigma_hat = torch.exp(log_sigma)
        var = sigma_hat.pow(2) + err_obs.pow(2)
        log_var = torch.log(var)

        nll = 0.5 * (log_var + (y_obs - mean).pow(2) / var + math.log(2 * math.pi))
        nll = (nll * mask).sum(dim=1) / mask.sum(dim=1).clamp(min=1.0)  # (B,)

        loss = nll.mean() + beta_kl * (kl_path.mean() + kl_z0.mean()) / mask.sum(dim=1).clamp(min=1.0).mean()

        return dict(
            loss=loss,
            nll=nll.mean(),
            kl_path=kl_path.mean(),
            kl_z0=kl_z0.mean(),
            mean=mean,
            sigma=sigma_hat,
            zs=zs.transpose(0, 1),  # (B, T, latent_dim)
        )
