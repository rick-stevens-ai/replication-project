"""Train simplified Latent SDE on synthetic DRW light curves."""
from __future__ import annotations

import os, pickle, time, math, json
import numpy as np
import torch

from model import LatentSDEModel


def load(split, data_dir):
    with open(os.path.join(data_dir, f"{split}.pkl"), "rb") as f:
        return pickle.load(f)


def make_grid_and_feats(batch, device, T_grid=64):
    """Bin irregular observations onto a fixed uniform grid of size T_grid.

    Features per grid cell:  [y_bin, err_bin, mask, dt_since_last_obs].
    We keep T_grid small so torchsde stays cheap on CPU.
    """
    t = torch.from_numpy(batch["t"]).to(device)        # (B, T)
    y = torch.from_numpy(batch["y"]).to(device)
    err = torch.from_numpy(batch["err"]).to(device)
    mask = torch.from_numpy(batch["mask"]).to(device)
    B = t.shape[0]
    tmax = t.max(dim=1, keepdim=True).values  # per-curve max time
    # Normalise time to [0, 1]
    t_norm = t / tmax.clamp(min=1.0)
    # Build uniform grid 0..1
    grid = torch.linspace(0.0, 1.0, T_grid, device=device)
    bins = torch.bucketize(t_norm, grid) - 1  # (B, T)
    bins = bins.clamp(0, T_grid - 1)

    y_grid = torch.zeros(B, T_grid, device=device)
    err_grid = torch.ones(B, T_grid, device=device)
    mask_grid = torch.zeros(B, T_grid, device=device)
    count = torch.zeros(B, T_grid, device=device)

    # scatter-add means
    for b in range(B):
        m = mask[b].bool()
        idx = bins[b][m]
        y_grid[b].index_add_(0, idx, y[b][m])
        err_grid[b].index_add_(0, idx, err[b][m])
        count[b].index_add_(0, idx, torch.ones_like(idx, dtype=torch.float32))
    has = count > 0
    y_grid = torch.where(has, y_grid / count.clamp(min=1), torch.zeros_like(y_grid))
    err_grid = torch.where(has, err_grid / count.clamp(min=1), torch.ones_like(err_grid))
    mask_grid = has.float()

    # dt-since-last-obs feature
    dt_feat = torch.zeros(B, T_grid, device=device)
    last = torch.full((B,), -1.0, device=device)
    for i in range(T_grid):
        dt_feat[:, i] = (grid[i] - last)
        last = torch.where(mask_grid[:, i] > 0, grid[i].expand(B), last)

    feats = torch.stack([y_grid, err_grid, mask_grid, dt_feat], dim=-1)  # (B, T, 4)
    return feats, mask_grid, grid, y_grid, err_grid


def run(data_dir, out_dir, epochs=40, lr=2e-3, batch_size=32, latent_dim=4,
        T_grid=64, hidden=64, context_dim=32, seed=0, log_every=5):
    torch.manual_seed(seed)
    device = torch.device("cpu")
    os.makedirs(out_dir, exist_ok=True)

    train = load("train", data_dir)
    val   = load("val", data_dir)
    model = LatentSDEModel(input_dim=4, latent_dim=latent_dim,
                           context_dim=context_dim, hidden=hidden).to(device)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"model params: {n_params}")

    opt = torch.optim.Adam(model.parameters(), lr=lr)
    sched = torch.optim.lr_scheduler.ExponentialLR(opt, gamma=0.97)

    N = train["y"].shape[0]
    history = []
    best_val = math.inf
    t0 = time.time()
    for ep in range(epochs):
        # KL annealing: 0 -> 1 over first 10 epochs
        beta = min(1.0, (ep + 1) / 10.0)

        idx = np.random.permutation(N)
        losses, nlls, klps = [], [], []
        model.train()
        for i in range(0, N, batch_size):
            b = {k: v[idx[i : i + batch_size]] for k, v in train.items() if k != "params"}
            feats, mask_g, grid, y_g, err_g = make_grid_and_feats(b, device, T_grid)
            out = model(feats, mask_g, grid, y_g, err_g, beta_kl=beta)
            opt.zero_grad()
            out["loss"].backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 0.5)
            opt.step()
            losses.append(out["loss"].item())
            nlls.append(out["nll"].item())
            klps.append(out["kl_path"].item())
        sched.step()

        # validation
        model.eval()
        with torch.no_grad():
            vb = {k: v for k, v in val.items() if k != "params"}
            feats, mask_g, grid, y_g, err_g = make_grid_and_feats(vb, device, T_grid)
            # chunk to stay under mem
            chunk = 32
            tot = {"nll": 0.0, "n": 0, "se": 0.0, "ae": 0.0, "cnt": 0}
            for j in range(0, feats.shape[0], chunk):
                f_c, m_c, y_c, e_c = feats[j:j+chunk], mask_g[j:j+chunk], y_g[j:j+chunk], err_g[j:j+chunk]
                out_v = model(f_c, m_c, grid, y_c, e_c, beta_kl=1.0)
                tot["nll"] += out_v["nll"].item() * f_c.shape[0]
                tot["n"]   += f_c.shape[0]
                # reconstruction errors on observed cells
                err_diff = (out_v["mean"] - y_c) * m_c
                tot["se"] += (err_diff ** 2).sum().item()
                tot["ae"] += err_diff.abs().sum().item()
                tot["cnt"] += m_c.sum().item()
            val_nll = tot["nll"] / tot["n"]
            val_rmse = math.sqrt(tot["se"] / max(tot["cnt"], 1))
            val_mae  = tot["ae"] / max(tot["cnt"], 1)

        dt = time.time() - t0
        line = dict(epoch=ep, loss=float(np.mean(losses)), nll=float(np.mean(nlls)),
                    kl_path=float(np.mean(klps)), beta=beta, val_nll=val_nll,
                    val_rmse=val_rmse, val_mae=val_mae, elapsed=dt)
        history.append(line)
        if ep % log_every == 0 or ep == epochs - 1:
            print(f"ep {ep:03d}  loss={line['loss']:.4f}  nll={line['nll']:.4f}  "
                  f"kl={line['kl_path']:.3f}  val_nll={val_nll:.4f}  "
                  f"val_rmse={val_rmse:.4f}  val_mae={val_mae:.4f}  t={dt:.1f}s")

        if val_nll < best_val:
            best_val = val_nll
            torch.save({"model": model.state_dict(),
                        "config": dict(latent_dim=latent_dim, context_dim=context_dim,
                                       hidden=hidden, T_grid=T_grid)},
                       os.path.join(out_dir, "best.pt"))

    with open(os.path.join(out_dir, "history.json"), "w") as f:
        json.dump(history, f, indent=2)
    print("best val NLL:", best_val)
    return best_val


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--epochs", type=int, default=40)
    ap.add_argument("--batch_size", type=int, default=32)
    ap.add_argument("--T_grid", type=int, default=64)
    ap.add_argument("--latent_dim", type=int, default=4)
    ap.add_argument("--hidden", type=int, default=64)
    ap.add_argument("--lr", type=float, default=2e-3)
    args = ap.parse_args()
    here = os.path.dirname(__file__)
    run(data_dir=os.path.join(here, "..", "data"),
        out_dir=os.path.join(here, "..", "results"),
        epochs=args.epochs, batch_size=args.batch_size,
        T_grid=args.T_grid, latent_dim=args.latent_dim,
        hidden=args.hidden, lr=args.lr)
