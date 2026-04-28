"""Evaluate trained Latent SDE on test set, reporting RMSE/MAE/NLL at observed
time points and drawing diagnostic plots."""
from __future__ import annotations

import os, pickle, math, json
import numpy as np
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from model import LatentSDEModel
from train import make_grid_and_feats, load


def sample_at_times(model, feats, mask_grid, grid, y_grid, err_grid,
                    t_target, n_samples=16, dt=0.02):
    """Return mean and std of y predicted at t_target (B, K) normalised to [0,1]."""
    device = feats.device
    model.eval()
    B = feats.shape[0]
    with torch.no_grad():
        ctx, mu0, log_var0 = model.encoder(feats, mask_grid)
        std0 = torch.exp(0.5 * log_var0)
        # Build union of grid and targets; we only decode at targets, but
        # SDE needs a monotone time vector.
        all_t = torch.unique(torch.cat([grid, t_target.flatten()])).sort().values
        model.sde.set_context(ctx)

        means, sigmas = [], []
        for _ in range(n_samples):
            eps = torch.randn_like(mu0)
            z0 = mu0 + eps * std0
            zs = __import__("torchsde").sdeint(model.sde, z0, all_t, method="euler", dt=dt)
            mean, log_sigma = model.decoder(zs)  # (L, B)
            means.append(mean.transpose(0, 1))     # (B, L)
            sigmas.append(log_sigma.exp().transpose(0, 1))
        samples = torch.stack(means, dim=0)         # (S, B, L)
        sample_sigmas = torch.stack(sigmas, dim=0)  # (S, B, L) aleatoric

        # index into all_t for each target time
        t_sorted, _ = all_t.sort()
        idx = torch.bucketize(t_target, t_sorted).clamp(max=len(t_sorted) - 1)
        # gather samples at those indices
        S, _, L = samples.shape
        K = t_target.shape[1]
        g_mean = samples.gather(2, idx.unsqueeze(0).expand(S, B, K))        # (S, B, K)
        g_sig  = sample_sigmas.gather(2, idx.unsqueeze(0).expand(S, B, K))
        mean = g_mean.mean(dim=0)                                            # (B, K)
        # total variance = epistemic (across samples) + aleatoric (decoder sigma^2 mean)
        var_ep = g_mean.var(dim=0, unbiased=False)
        var_al = (g_sig ** 2).mean(dim=0)
        std = (var_ep + var_al).clamp(min=1e-6).sqrt()
        return mean, std


def main():
    here = os.path.dirname(__file__)
    data_dir = os.path.join(here, "..", "data")
    res_dir = os.path.join(here, "..", "results")
    fig_dir = os.path.join(here, "..", "figures")
    os.makedirs(fig_dir, exist_ok=True)

    ckpt = torch.load(os.path.join(res_dir, "best.pt"), map_location="cpu")
    cfg = ckpt["config"]
    model = LatentSDEModel(input_dim=4, latent_dim=cfg["latent_dim"],
                           context_dim=cfg.get("context_dim", 32), hidden=cfg["hidden"])
    model.load_state_dict(ckpt["model"])

    test = load("test", data_dir)
    feats, mask_g, grid, y_g, err_g = make_grid_and_feats(test, torch.device("cpu"), cfg["T_grid"])
    tmax_np = test["t"].max(axis=1)
    tmax_np = np.where(tmax_np < 1.0, 1.0, tmax_np)
    # normalised target times at ORIGINAL observation times
    t_norm = torch.from_numpy(test["t"] / tmax_np[:, None]).float()
    y_obs = torch.from_numpy(test["y"])
    err_obs = torch.from_numpy(test["err"])
    mask_obs = torch.from_numpy(test["mask"])

    # chunked sampling
    mean_all = torch.zeros_like(y_obs)
    std_all = torch.ones_like(y_obs)
    chunk = 16
    for i in range(0, feats.shape[0], chunk):
        sl = slice(i, i + chunk)
        m_b, s_b = sample_at_times(model, feats[sl], mask_g[sl], grid,
                                   y_g[sl], err_g[sl], t_norm[sl], n_samples=16, dt=0.02)
        mean_all[sl] = m_b
        std_all[sl] = s_b

    # Metrics on observed points only
    m = mask_obs.bool()
    err_diff = (mean_all - y_obs)[m]
    se = (err_diff ** 2).sum().item()
    ae = err_diff.abs().sum().item()
    cnt = int(m.sum().item())
    # Predictive variance combines model std and observation noise
    var = std_all[m] ** 2 + err_obs[m] ** 2
    nll = 0.5 * (torch.log(var) + err_diff ** 2 / var + math.log(2 * math.pi))
    nll_mean = nll.mean().item()

    rmse = math.sqrt(se / cnt)
    mae = ae / cnt
    results = dict(rmse=float(rmse), mae=float(mae), nll=float(nll_mean),
                   n_curves=int(y_obs.shape[0]), n_points=cnt)
    with open(os.path.join(res_dir, "latentsde_test.json"), "w") as f:
        json.dump(results, f, indent=2)
    print("LatentSDE test:", results)

    # Plot a few example reconstructions
    fig, axes = plt.subplots(3, 2, figsize=(12, 9), sharex=False)
    axes = axes.ravel()
    for k, ax in enumerate(axes):
        i = k * 5 % y_obs.shape[0]
        m_i = mask_obs[i].bool()
        t_i = torch.from_numpy(test["t"][i]).float()[m_i]
        y_i = y_obs[i][m_i]
        mu_i = mean_all[i][m_i]
        sd_i = std_all[i][m_i]
        ax.errorbar(t_i, y_i, yerr=err_obs[i][m_i], fmt=".", ms=3, color="k",
                    lw=0.5, capsize=0, label="observations")
        ord_ = torch.argsort(t_i)
        ax.plot(t_i[ord_], mu_i[ord_], "-", color="C0", lw=1.5, label="latent-SDE mean")
        ax.fill_between(t_i[ord_].numpy(), (mu_i - sd_i)[ord_].numpy(),
                        (mu_i + sd_i)[ord_].numpy(), color="C0", alpha=0.25)
        p = test["params"][i]
        ax.set_title(f"log10(tau)={p[0]:.2f}, SF_inf={p[1]:.2f}")
        if k == 0:
            ax.legend(fontsize=8, loc="upper right")
    fig.supxlabel("time (days)"); fig.supylabel("magnitude (mean-subtracted)")
    fig.tight_layout()
    fig.savefig(os.path.join(fig_dir, "reconstructions.png"), dpi=140)
    plt.close(fig)
    print("saved reconstructions.png")

    # training curve
    with open(os.path.join(res_dir, "history.json")) as f:
        hist = json.load(f)
    epochs = [h["epoch"] for h in hist]
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.5))
    ax[0].plot(epochs, [h["loss"] for h in hist], label="train loss")
    ax[0].plot(epochs, [h["val_nll"] for h in hist], label="val NLL")
    ax[0].set_xlabel("epoch"); ax[0].legend(); ax[0].set_title("Loss curves")
    ax[1].plot(epochs, [h["val_rmse"] for h in hist], label="val RMSE (grid)")
    ax[1].plot(epochs, [h["val_mae"]  for h in hist], label="val MAE  (grid)")
    ax[1].set_xlabel("epoch"); ax[1].legend(); ax[1].set_title("Validation metrics")
    fig.tight_layout()
    fig.savefig(os.path.join(fig_dir, "training_curves.png"), dpi=140)
    plt.close(fig)
    print("saved training_curves.png")

    # Latent trajectories
    with torch.no_grad():
        # encode a small batch, sample SDE on fine grid, plot latent paths
        small = {k: v[:8] for k, v in test.items() if k != "params"}
        feats_s, mask_s, grid_s, y_s, err_s = make_grid_and_feats(small, torch.device("cpu"), cfg["T_grid"])
        ctx, mu0, log_var0 = model.encoder(feats_s, mask_s)
        std0 = torch.exp(0.5 * log_var0)
        model.sde.set_context(ctx)
        fine = torch.linspace(0.0, 1.0, 128)
        z0 = mu0 + std0 * torch.randn_like(mu0)
        import torchsde
        zs = torchsde.sdeint(model.sde, z0, fine, method="euler", dt=0.01)  # (T, B, D)
    fig, axes = plt.subplots(1, cfg["latent_dim"], figsize=(3 * cfg["latent_dim"], 3), sharex=True)
    if cfg["latent_dim"] == 1: axes = [axes]
    for d, ax in enumerate(axes):
        for b in range(zs.shape[1]):
            ax.plot(fine.numpy(), zs[:, b, d].numpy(), alpha=0.6)
        ax.set_title(f"latent dim {d}")
    fig.supxlabel("normalised time"); fig.tight_layout()
    fig.savefig(os.path.join(fig_dir, "latent_paths.png"), dpi=140)
    plt.close(fig)
    print("saved latent_paths.png")

    return results


if __name__ == "__main__":
    main()
