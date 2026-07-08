"""
Independent PyTorch replication of rotationally-invariant VAE (rVAE) for
OSTI 2439897: "Physics and chemistry from parsimonious representations:
image analysis via invariant variational autoencoders".

Reference approach (re-implemented from scratch, no atomai dependency):
    The encoder predicts (mu_z, logvar_z) for a low-dim content code AND an
    SE(2) nuisance (theta, tx, ty) describing the image's rigid transform.
    The decoder generates a canonical image from z, which is then warped by
    the inverse of the encoded transform. This forces z to encode only
    transform-invariant (physical) content.

Dataset: synthetic 2D atomic-lattice patches (hexagonal) with three known
ground-truth factors:
    - lattice constant a (physical)
    - rotation angle theta (nuisance)
    - translation (tx, ty) (nuisance)
We measure how well the learned content latent z tracks 'a', and how well
the predicted nuisance tracks (theta, tx, ty).

Author: Ollie (OpenClaw subagent), 2026-04-23
"""
from __future__ import annotations
import argparse, json, math, os, time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader


# --------------------------------------------------------------------------
# Synthetic hexagonal-lattice dataset
# --------------------------------------------------------------------------
class HexLatticeDataset(Dataset):
    """Synthetic hexagonal atomic-lattice patches.

    Each sample is a 64x64 grayscale image rendered on the fly with:
        a      ~ U(6, 12)   # lattice constant in pixels  (physics)
        theta  ~ U(-pi, pi) # rotation                    (nuisance)
        tx,ty  ~ U(-3, 3)   # sub-pixel translation       (nuisance)
    plus Gaussian noise. Atoms are Gaussian blobs; contrast/width are fixed
    so that the only free 'physics' factor is the lattice constant.
    """

    def __init__(self, n: int, img_size: int = 64, sigma: float = 1.1,
                 a_range=(6.0, 12.0), noise_std: float = 0.05, seed: int = 0):
        self.n = int(n)
        self.img_size = img_size
        self.sigma = sigma
        self.a_range = a_range
        self.noise_std = noise_std
        rng = np.random.default_rng(seed)
        self.a      = rng.uniform(*a_range, size=n).astype(np.float32)
        self.theta  = rng.uniform(-np.pi, np.pi, size=n).astype(np.float32)
        self.tx     = rng.uniform(-3.0, 3.0, size=n).astype(np.float32)
        self.ty     = rng.uniform(-3.0, 3.0, size=n).astype(np.float32)

    def __len__(self):
        return self.n

    def _render(self, a, theta, tx, ty):
        S = self.img_size
        # centred pixel grid
        ys, xs = np.mgrid[0:S, 0:S].astype(np.float32)
        xs -= (S - 1) / 2.0
        ys -= (S - 1) / 2.0
        # rotate *coords* (equivalent to rotating the lattice)
        c, s = math.cos(theta), math.sin(theta)
        xr =  c * xs + s * ys - tx
        yr = -s * xs + c * ys - ty
        # hex basis vectors in the lattice frame, spacing a
        b1 = np.array([a,       0.0])
        b2 = np.array([a * 0.5, a * math.sqrt(3) / 2.0])
        # dual basis to find nearest lattice index (integer)
        B = np.stack([b1, b2], axis=1)             # 2x2
        Binv = np.linalg.inv(B)
        coords = np.stack([xr, yr], axis=-1)       # S,S,2
        # fractional indices
        frac = coords @ Binv.T                     # S,S,2
        # need distance to NEAREST lattice point across several neighbours
        img = np.zeros((S, S), np.float32)
        n_nb = 1
        for di in range(-n_nb, n_nb + 1):
            for dj in range(-n_nb, n_nb + 1):
                i = np.round(frac[..., 0]) + di
                j = np.round(frac[..., 1]) + dj
                nx = i * b1[0] + j * b2[0]
                ny = i * b1[1] + j * b2[1]
                dx = xr - nx
                dy = yr - ny
                img = np.maximum(img, np.exp(-(dx * dx + dy * dy) / (2 * self.sigma ** 2)))
        img += np.random.randn(S, S).astype(np.float32) * self.noise_std
        return img.astype(np.float32)

    def __getitem__(self, idx):
        a, theta, tx, ty = float(self.a[idx]), float(self.theta[idx]), float(self.tx[idx]), float(self.ty[idx])
        img = self._render(a, theta, tx, ty)
        img = np.clip(img, 0.0, 1.0)
        return (
            torch.from_numpy(img).unsqueeze(0),             # 1,H,W
            torch.tensor([a, theta, tx, ty], dtype=torch.float32),
        )


# --------------------------------------------------------------------------
# Model
# --------------------------------------------------------------------------
class ConvEncoder(nn.Module):
    def __init__(self, in_ch=1, zdim=2, nuisance_dim=3, hidden=64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(in_ch, hidden, 4, 2, 1), nn.ReLU(True),      # 32
            nn.Conv2d(hidden, hidden*2, 4, 2, 1), nn.ReLU(True),   # 16
            nn.Conv2d(hidden*2, hidden*4, 4, 2, 1), nn.ReLU(True), # 8
            nn.Conv2d(hidden*4, hidden*4, 4, 2, 1), nn.ReLU(True), # 4
            nn.Flatten(),
            nn.Linear(hidden*4*4*4, 256), nn.ReLU(True),
        )
        self.fc_mu      = nn.Linear(256, zdim)
        self.fc_logvar  = nn.Linear(256, zdim)
        self.fc_nuis    = nn.Linear(256, nuisance_dim)   # theta, tx, ty

    def forward(self, x):
        h = self.net(x)
        lv = torch.clamp(self.fc_logvar(h), -8.0, 8.0)
        return self.fc_mu(h), lv, self.fc_nuis(h)


class CoordDecoder(nn.Module):
    """Coordinate-grid MLP decoder with Fourier-feature input encoding.

    Using Fourier features dramatically improves the ability of a coordinate
    MLP to represent high-frequency structure (e.g. sharp lattice peaks).
    """
    def __init__(self, zdim=2, hidden=256, n_layers=5, n_fourier=8, sigma=4.0):
        super().__init__()
        self.n_fourier = n_fourier
        # fixed Gaussian Fourier basis B (2 x m); positional input dim = 2*m
        B = torch.randn(2, n_fourier) * sigma
        self.register_buffer("B", B)
        in_dim = zdim + 2 * n_fourier          # sin + cos of m=n_fourier projections
        layers = [nn.Linear(in_dim, hidden), nn.SiLU()]
        for _ in range(n_layers - 1):
            layers += [nn.Linear(hidden, hidden), nn.SiLU()]
        layers += [nn.Linear(hidden, 1), nn.Sigmoid()]
        self.mlp = nn.Sequential(*layers)

    def forward(self, z, grid):
        # grid: B, HW, 2
        Bsz, HW, _ = grid.shape
        # Fourier features: project (x,y) via fixed random B -> (sin, cos)
        proj = 2 * math.pi * grid @ self.B             # B,HW,m
        ff = torch.cat([torch.sin(proj), torch.cos(proj)], dim=-1)  # B,HW,2m
        z_rep = z.unsqueeze(1).expand(-1, HW, -1)
        h = torch.cat([z_rep, ff], dim=-1)
        out = self.mlp(h).squeeze(-1)                  # B, HW
        S = int(math.sqrt(HW))
        return out.view(Bsz, 1, S, S)


class RVAE(nn.Module):
    def __init__(self, img_size=64, zdim=2, hidden=64, dec_hidden=128):
        super().__init__()
        self.img_size = img_size
        self.zdim = zdim
        self.encoder = ConvEncoder(1, zdim, 3, hidden)
        self.decoder = CoordDecoder(zdim, dec_hidden, n_layers=5, n_fourier=16, sigma=6.0)
        # canonical pixel grid in [-1, 1]
        ys, xs = torch.meshgrid(
            torch.linspace(-1, 1, img_size),
            torch.linspace(-1, 1, img_size),
            indexing="ij",
        )
        self.register_buffer("grid0", torch.stack([xs, ys], dim=-1).view(-1, 2))  # HW,2

    def transform_grid(self, theta, t):
        """Inverse-rigid-transform the canonical grid.

        Input image I(p) is modelled as T(R(-theta)(p - t)) where T is the
        decoder's canonical template.  So to reconstruct I at pixel p we
        must evaluate T at R(-theta)(p - t).
        """
        B = theta.shape[0]
        c, s = torch.cos(theta), torch.sin(theta)
        # R(-theta):  [[cos, sin], [-sin, cos]]
        R = torch.stack([torch.stack([ c,  s], -1),
                          torch.stack([-s,  c], -1)], dim=-2)     # B,2,2
        grid = self.grid0.unsqueeze(0).expand(B, -1, -1)           # B,HW,2
        # translate first (in image frame), then rotate
        grid = grid - t.unsqueeze(1)
        grid = torch.einsum("bij,bnj->bni", R, grid)
        return grid

    def forward(self, x):
        mu, logvar, nuis = self.encoder(x)
        std = torch.exp(0.5 * logvar)
        z = mu + std * torch.randn_like(std)
        theta = nuis[:, 0]
        t     = nuis[:, 1:3] * (2.0 / self.img_size)   # scale px -> [-1,1]
        grid  = self.transform_grid(theta, t)
        x_hat = self.decoder(z, grid)
        return x_hat, mu, logvar, nuis


class VanillaVAE(nn.Module):
    """Standard conv VAE with z-only latent (no explicit invariance)."""
    def __init__(self, img_size=64, zdim=5, hidden=64):
        super().__init__()
        self.img_size = img_size
        self.enc = nn.Sequential(
            nn.Conv2d(1, hidden, 4, 2, 1), nn.ReLU(True),
            nn.Conv2d(hidden, hidden*2, 4, 2, 1), nn.ReLU(True),
            nn.Conv2d(hidden*2, hidden*4, 4, 2, 1), nn.ReLU(True),
            nn.Conv2d(hidden*4, hidden*4, 4, 2, 1), nn.ReLU(True),
            nn.Flatten(), nn.Linear(hidden*4*4*4, 256), nn.ReLU(True),
        )
        self.fc_mu = nn.Linear(256, zdim)
        self.fc_lv = nn.Linear(256, zdim)
        self.dec_fc = nn.Sequential(
            nn.Linear(zdim, 256), nn.ReLU(True),
            nn.Linear(256, hidden*4*4*4), nn.ReLU(True),
        )
        self.dec = nn.Sequential(
            nn.ConvTranspose2d(hidden*4, hidden*4, 4, 2, 1), nn.ReLU(True),
            nn.ConvTranspose2d(hidden*4, hidden*2, 4, 2, 1), nn.ReLU(True),
            nn.ConvTranspose2d(hidden*2, hidden,   4, 2, 1), nn.ReLU(True),
            nn.ConvTranspose2d(hidden, 1, 4, 2, 1), nn.Sigmoid(),
        )
        self.hidden = hidden

    def forward(self, x):
        h = self.enc(x)
        mu, lv = self.fc_mu(h), self.fc_lv(h)
        lv = torch.clamp(lv, -8.0, 8.0)
        z = mu + torch.exp(0.5 * lv) * torch.randn_like(mu)
        d = self.dec_fc(z).view(-1, self.hidden*4, 4, 4)
        return self.dec(d), mu, lv, None


# --------------------------------------------------------------------------
# Training
# --------------------------------------------------------------------------
def kl_normal(mu, logvar):
    return -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp(), dim=1)


def train(model, loader, val_loader, device, epochs, beta, lr, logf,
          beta_warmup_epochs=0):
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    hist = []
    for ep in range(1, epochs + 1):
        # linear beta warmup (free-bits-like anti-collapse)
        if beta_warmup_epochs > 0:
            eff_beta = beta * min(1.0, (ep - 1) / max(1, beta_warmup_epochs))
        else:
            eff_beta = beta
        model.train()
        t0 = time.time()
        total, tot_rec, tot_kl, n = 0.0, 0.0, 0.0, 0
        for x, _y in loader:
            x = x.to(device, non_blocking=True)
            x_hat, mu, lv, _nu = model(x)
            rec = F.mse_loss(x_hat, x, reduction="sum") / x.size(0)
            kl  = kl_normal(mu, lv).mean()
            loss = rec + eff_beta * kl
            opt.zero_grad(); loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0)
            opt.step()
            bs = x.size(0); n += bs
            total   += loss.item() * bs
            tot_rec += rec.item()  * bs
            tot_kl  += kl.item()   * bs
        tr_loss = total / n; tr_rec = tot_rec / n; tr_kl = tot_kl / n

        model.eval()
        with torch.no_grad():
            vtot, vrec, vkl, vn = 0.0, 0.0, 0.0, 0
            for x, _y in val_loader:
                x = x.to(device, non_blocking=True)
                x_hat, mu, lv, _nu = model(x)
                rec = F.mse_loss(x_hat, x, reduction="sum") / x.size(0)
                kl  = kl_normal(mu, lv).mean()
                bs = x.size(0); vn += bs
                vtot += (rec + eff_beta*kl).item() * bs
                vrec += rec.item() * bs
                vkl  += kl.item()  * bs
        msg = (f"ep {ep:03d}/{epochs}  beta={eff_beta:.3f}  tr_loss={tr_loss:8.3f} rec={tr_rec:8.3f} kl={tr_kl:6.3f}"
               f"  val_loss={vtot/vn:8.3f} rec={vrec/vn:8.3f} kl={vkl/vn:6.3f}"
               f"  ({time.time()-t0:.1f}s)")
        print(msg, flush=True); logf.write(msg + "\n"); logf.flush()
        hist.append(dict(epoch=ep, tr_loss=tr_loss, tr_rec=tr_rec, tr_kl=tr_kl,
                         val_loss=vtot/vn, val_rec=vrec/vn, val_kl=vkl/vn))
    return hist


# --------------------------------------------------------------------------
# Evaluation
# --------------------------------------------------------------------------
@torch.no_grad()
def encode_all(model, loader, device):
    mus, nuis, ys = [], [], []
    model.eval()
    for x, y in loader:
        x = x.to(device)
        out = model.encoder(x) if hasattr(model, "encoder") else (
            model.fc_mu(model.enc(x)), None, None)
        if isinstance(out, tuple) and len(out) == 3:
            mu, _lv, nu = out
        else:
            mu = out[0]; nu = None
        mus.append(mu.cpu().numpy())
        ys.append(y.numpy())
        if nu is not None:
            nuis.append(nu.cpu().numpy())
    mus = np.concatenate(mus); ys = np.concatenate(ys)
    nuis = np.concatenate(nuis) if nuis else None
    return mus, nuis, ys


def pearson_abs(x, y):
    x = x - x.mean(); y = y - y.mean()
    denom = (np.linalg.norm(x) * np.linalg.norm(y))
    return abs((x * y).sum() / denom) if denom > 0 else 0.0


def correlation_table(z, nuis, y):
    """y columns: a, theta, tx, ty  (ground truth)"""
    names_phys = ["a", "theta", "tx", "ty"]
    out = {"z_vs_gt": {}, "nuis_vs_gt": {}}
    for i, nm in enumerate(names_phys):
        for k in range(z.shape[1]):
            out["z_vs_gt"][f"z{k}_vs_{nm}"] = float(pearson_abs(z[:, k], y[:, i]))
        if nuis is not None:
            # special: theta requires circular handling; use cos/sin
            gt = y[:, i]
            if nm == "theta":
                gt_sin, gt_cos = np.sin(gt), np.cos(gt)
                pred = nuis[:, 0]
                pr_sin, pr_cos = np.sin(pred), np.cos(pred)
                val = max(pearson_abs(pr_sin, gt_sin), pearson_abs(pr_cos, gt_cos))
                out["nuis_vs_gt"][f"pred_theta_vs_theta(circ)"] = float(val)
            elif nm == "tx":
                out["nuis_vs_gt"][f"pred_tx_vs_tx"] = float(pearson_abs(nuis[:, 1], gt))
            elif nm == "ty":
                out["nuis_vs_gt"][f"pred_ty_vs_ty"] = float(pearson_abs(nuis[:, 2], gt))
    return out


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", type=Path, required=True)
    ap.add_argument("--model", choices=["rvae", "vae"], default="rvae")
    ap.add_argument("--epochs", type=int, default=30)
    ap.add_argument("--batch", type=int, default=128)
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--beta", type=float, default=1.0)
    ap.add_argument("--beta_warmup", type=int, default=0)
    ap.add_argument("--zdim", type=int, default=2)
    ap.add_argument("--n_train", type=int, default=20000)
    ap.add_argument("--n_val", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--device", default="cuda")
    args = ap.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)
    torch.manual_seed(args.seed); np.random.seed(args.seed)
    device = torch.device(args.device if torch.cuda.is_available() else "cpu")
    print(f"device={device}, model={args.model}")

    train_ds = HexLatticeDataset(args.n_train, seed=args.seed)
    val_ds   = HexLatticeDataset(args.n_val,   seed=args.seed + 1)
    train_loader = DataLoader(train_ds, batch_size=args.batch, shuffle=True,
                              num_workers=4, pin_memory=True, drop_last=True)
    val_loader   = DataLoader(val_ds,   batch_size=args.batch, shuffle=False,
                              num_workers=2, pin_memory=True)

    if args.model == "rvae":
        model = RVAE(zdim=args.zdim).to(device)
    else:
        model = VanillaVAE(zdim=max(args.zdim, 5)).to(device)
    n_par = sum(p.numel() for p in model.parameters())
    print(f"params: {n_par/1e6:.2f} M")

    logf = open(args.outdir / f"train_{args.model}.log", "w")
    hist = train(model, train_loader, val_loader, device,
                 args.epochs, args.beta, args.lr, logf,
                 beta_warmup_epochs=args.beta_warmup)
    logf.close()

    # encode val set
    val_loader_eval = DataLoader(val_ds, batch_size=args.batch, shuffle=False, num_workers=2)
    z, nuis, y = encode_all(model, val_loader_eval, device)
    corrs = correlation_table(z, nuis, y)
    print("correlations:", json.dumps(corrs, indent=2))

    np.savez(args.outdir / f"encoded_{args.model}.npz", z=z, nuis=nuis if nuis is not None else np.zeros(0), y=y)
    with open(args.outdir / f"results_{args.model}.json", "w") as f:
        json.dump({
            "model": args.model, "args": {k: str(v) for k, v in vars(args).items()},
            "final_val": hist[-1], "correlations": corrs,
            "best_val_rec": min(h["val_rec"] for h in hist),
            "params_millions": n_par / 1e6,
        }, f, indent=2)
    torch.save(model.state_dict(), args.outdir / f"model_{args.model}.pt")
    print("done ->", args.outdir)


if __name__ == "__main__":
    main()
