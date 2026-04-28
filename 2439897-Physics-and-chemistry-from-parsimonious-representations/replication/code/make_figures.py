"""Generate figures for the rVAE replication."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import torch

from rvae import RVAE, VanillaVAE, HexLatticeDataset


def fig_training_curves(outdir: Path):
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.5))
    for nm, col in [("rvae", "C0"), ("vae", "C3")]:
        logp = outdir / f"train_{nm}.log"
        if not logp.exists(): continue
        ep, trec, vrec, vkl = [], [], [], []
        for line in logp.read_text().splitlines():
            # ep 001/030  tr_loss= ... rec=... kl=...  val_loss=... rec=... kl=...
            try:
                toks = line.replace("=", " ").split()
                ep.append(int(toks[1].split("/")[0]))
                trec.append(float(toks[toks.index("rec") + 1]))
                # 2nd "rec" is val
                idx2 = toks.index("rec", toks.index("rec") + 1)
                vrec.append(float(toks[idx2 + 1]))
                idx_vkl = toks.index("kl", toks.index("kl") + 1)
                vkl.append(float(toks[idx_vkl + 1]))
            except Exception:
                continue
        ax[0].plot(ep, trec, col + "-", label=f"{nm} train rec")
        ax[0].plot(ep, vrec, col + "--", label=f"{nm} val rec")
        ax[1].plot(ep, vkl, col, label=f"{nm} val KL")
    ax[0].set_xlabel("epoch"); ax[0].set_ylabel("recon MSE (sum)"); ax[0].legend(); ax[0].set_yscale("log")
    ax[1].set_xlabel("epoch"); ax[1].set_ylabel("KL (val)"); ax[1].legend()
    ax[1].set_yscale("log"); ax[1].set_ylim(1e-2, 100)
    fig.suptitle("Training curves: rVAE vs vanilla VAE")
    fig.tight_layout()
    fig.savefig(outdir / "fig_training.png", dpi=140)
    plt.close(fig)


def fig_latent_vs_gt(outdir: Path):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
    for i, nm in enumerate(["rvae", "vae"]):
        p = outdir / f"encoded_{nm}.npz"
        if not p.exists():
            axes[i].set_visible(False); continue
        d = np.load(p, allow_pickle=True)
        z = d["z"]; y = d["y"]
        # best z dim vs lattice constant a
        best_k = max(range(z.shape[1]),
                     key=lambda k: abs(np.corrcoef(z[:, k], y[:, 0])[0, 1]))
        r = np.corrcoef(z[:, best_k], y[:, 0])[0, 1]
        sc = axes[i].scatter(y[:, 0], z[:, best_k], c=y[:, 1], s=6, cmap="twilight", alpha=0.7)
        axes[i].set_title(f"{nm}: z[{best_k}] vs a  (|r|={abs(r):.3f})")
        axes[i].set_xlabel("ground-truth lattice a (px)")
        axes[i].set_ylabel(f"latent z[{best_k}]")
        plt.colorbar(sc, ax=axes[i], label="theta (GT)")
    fig.suptitle("Content latent captures the physical factor (lattice a)")
    fig.tight_layout()
    fig.savefig(outdir / "fig_latent_vs_a.png", dpi=140)
    plt.close(fig)


def fig_nuisance_recovery(outdir: Path):
    p = outdir / "encoded_rvae.npz"
    if not p.exists(): return
    d = np.load(p, allow_pickle=True)
    nuis = d["nuis"]; y = d["y"]
    if nuis is None or nuis.size == 0: return
    fig, ax = plt.subplots(1, 3, figsize=(13, 4))
    # theta: plot cos(theta) pred vs GT
    ax[0].scatter(np.sin(y[:, 1]), np.sin(nuis[:, 0]), s=6, alpha=0.6)
    ax[0].set_xlabel("sin(theta) GT"); ax[0].set_ylabel("sin(theta) pred")
    r = np.corrcoef(np.sin(y[:, 1]), np.sin(nuis[:, 0]))[0, 1]
    ax[0].set_title(f"theta (r={r:.3f})")
    ax[0].plot([-1, 1], [-1, 1], "k--", lw=0.5)
    for k, nm in [(1, "tx"), (2, "ty")]:
        gt = y[:, k + 1]
        pr = nuis[:, k]
        ax[k].scatter(gt, pr, s=6, alpha=0.6)
        r = np.corrcoef(gt, pr)[0, 1]
        ax[k].set_title(f"{nm}  (r={r:.3f})")
        ax[k].set_xlabel(f"{nm} GT (px)"); ax[k].set_ylabel(f"{nm} pred")
    fig.suptitle("rVAE recovers the nuisance (rotation + translation) factors")
    fig.tight_layout()
    fig.savefig(outdir / "fig_nuisance.png", dpi=140)
    plt.close(fig)


def fig_latent_traversal(outdir: Path, device="cpu"):
    ckpt = outdir / "model_rvae.pt"
    if not ckpt.exists(): return
    model = RVAE(zdim=2)
    model.load_state_dict(torch.load(ckpt, map_location=device))
    model.eval().to(device)
    # sweep each z-dim while keeping the other at 0, zero nuisance
    n_steps = 9
    fig, axes = plt.subplots(2, n_steps, figsize=(n_steps * 1.2, 2.8))
    with torch.no_grad():
        for d in range(2):
            vals = np.linspace(-3, 3, n_steps)
            for j, v in enumerate(vals):
                z = torch.zeros(1, 2, device=device); z[0, d] = float(v)
                theta = torch.zeros(1, device=device); t = torch.zeros(1, 2, device=device)
                grid = model.transform_grid(theta, t)
                img = model.decoder(z, grid).cpu().numpy()[0, 0]
                axes[d, j].imshow(img, cmap="gray", vmin=0, vmax=1)
                axes[d, j].set_xticks([]); axes[d, j].set_yticks([])
                if d == 0: axes[d, j].set_title(f"{v:+.1f}", fontsize=8)
            axes[d, 0].set_ylabel(f"z[{d}]", fontsize=10)
    fig.suptitle("rVAE latent traversal (canonical frame)")
    fig.tight_layout()
    fig.savefig(outdir / "fig_traversal.png", dpi=140)
    plt.close(fig)


def fig_reconstruction(outdir: Path, device="cpu"):
    ckpt = outdir / "model_rvae.pt"
    if not ckpt.exists(): return
    model = RVAE(zdim=2); model.load_state_dict(torch.load(ckpt, map_location=device))
    model.eval().to(device)
    ds = HexLatticeDataset(8, seed=999)
    fig, axes = plt.subplots(2, 8, figsize=(12, 3.2))
    with torch.no_grad():
        for i in range(8):
            x, y = ds[i]
            x_hat, _, _, nu = model(x.unsqueeze(0).to(device))
            axes[0, i].imshow(x.numpy()[0], cmap="gray", vmin=0, vmax=1)
            axes[1, i].imshow(x_hat.cpu().numpy()[0, 0], cmap="gray", vmin=0, vmax=1)
            axes[0, i].set_title(f"a={y[0]:.1f}", fontsize=8)
            for ax in (axes[0, i], axes[1, i]):
                ax.set_xticks([]); ax.set_yticks([])
        axes[0, 0].set_ylabel("input")
        axes[1, 0].set_ylabel("recon")
    fig.suptitle("rVAE reconstructions")
    fig.tight_layout()
    fig.savefig(outdir / "fig_reconstruction.png", dpi=140)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", type=Path, required=True)
    args = ap.parse_args()
    fig_training_curves(args.outdir)
    fig_latent_vs_gt(args.outdir)
    fig_nuisance_recovery(args.outdir)
    fig_latent_traversal(args.outdir)
    fig_reconstruction(args.outdir)
    print("figures ->", args.outdir)


if __name__ == "__main__":
    main()
