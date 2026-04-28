"""
Antisite -> vacancy time-series tracking experiment for OSTI 2439897.

Reproduces (in spirit) the paper's "transformation tracking" demonstration in
which an SE(2)-invariant rVAE encodes per-frame STEM patches around a defect
site and the latent trajectory is post-filtered (Kalman smoother) to recover
the kinetics of the antisite -> vacancy conversion.

We construct a tractable synthetic analogue:
  * 32x32 patches around a central defect site embedded in a hexagonal
    sub-lattice background.
  * The central-site occupancy parameter c in [0, 1] linearly interpolates
    between an "antisite" template (bright dopant atom -- elevated peak
    intensity I_a = 1.0) and a "vacancy" template (no peak, I_v = 0.0).
  * The six nearest neighbours stay put (constant background), so only the
    defect-site occupancy changes; this is the structural "transformation
    coordinate" the rVAE should learn.
  * Each patch has random SE(2) nuisance (theta, t_x, t_y) and Gaussian
    detector noise.

After training a 1D-latent rVAE on i.i.d. patches we synthesise a *time
series* whose ground-truth occupancy follows first-order Arrhenius kinetics
   c(t) = exp(- k * t),     k = k_true (known)
encode every frame, calibrate z(t) -> c_hat(t) via a linear fit on the
training set, and apply a constant-velocity Kalman filter + RTS smoother to
denoise c_hat(t).  Finally we fit log(c_hat) vs t to recover k_est and
compare to k_true.

Outputs (in ../report/):
  * latent_trajectory.png   -- z(t), c_hat raw, Kalman-smoothed, GT
  * kinetics_estimate.png   -- log(c_hat) vs t with linear fit, k_est vs k_true
  * results_timeseries.json -- numerical scores

Author: Ollie (OpenClaw subagent), 2026-04-28
"""
from __future__ import annotations
import argparse, json, math, time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader


# --------------------------------------------------------------------------
# Synthetic antisite/vacancy patch dataset
# --------------------------------------------------------------------------
class DefectPatchDataset(Dataset):
    """32x32 patches around a single defect site.

    Background: 6 fixed neighbour atoms on a hexagonal ring of radius r_nn,
    each rendered as a Gaussian with peak I_bg.

    Centre atom: a Gaussian with peak (I_v + c * (I_a - I_v))*I_a_max where
    c in [0,1] is the antisite occupancy (1 = antisite present, 0 = vacancy).
    This single scalar c is the *physical* content factor.

    Nuisances: rotation theta ~ U(-pi, pi) of the whole patch, sub-pixel
    translation (tx, ty) ~ U(-2, 2) px.  Plus Gaussian detector noise.
    """

    def __init__(self, n: int, img_size: int = 32, sigma: float = 1.4,
                 r_nn: float = 7.0, I_bg: float = 0.6,
                 I_v: float = 0.0, I_a: float = 1.0,
                 noise_std: float = 0.06, seed: int = 0,
                 c_values=None,
                 theta_max: float = math.pi / 12.0,   # ~15deg residual
                 t_max: float = 1.0,                   # +/- 1 px residual
                 fix_pose: bool = False):
        self.n = int(n)
        self.S = img_size
        self.sigma = sigma
        self.r_nn = r_nn
        self.I_bg = I_bg
        self.I_v = I_v
        self.I_a = I_a
        self.noise_std = noise_std
        rng = np.random.default_rng(seed)
        if c_values is None:
            self.c = rng.uniform(0.0, 1.0, size=n).astype(np.float32)
        else:
            self.c = np.asarray(c_values, dtype=np.float32)
            assert self.c.shape[0] == n
        if fix_pose:
            self.theta = np.zeros(n, dtype=np.float32)
            self.tx = np.zeros(n, dtype=np.float32)
            self.ty = np.zeros(n, dtype=np.float32)
        else:
            self.theta = rng.uniform(-theta_max, theta_max, size=n).astype(np.float32)
            self.tx = rng.uniform(-t_max, t_max, size=n).astype(np.float32)
            self.ty = rng.uniform(-t_max, t_max, size=n).astype(np.float32)
        # per-sample noise seed (so encode-after-train is reproducible)
        self._noise_seeds = rng.integers(0, 2**31 - 1, size=n).astype(np.int64)

        # precompute neighbour positions in the canonical (un-rotated) frame
        self._nbrs = np.array([
            [r_nn * math.cos(k * math.pi / 3.0),
             r_nn * math.sin(k * math.pi / 3.0)] for k in range(6)
        ], dtype=np.float32)
        # *fixed* per-neighbour intensities to break the 6-fold rotational
        # symmetry of the ring: this gives the pose head an unambiguous
        # rotation reference and prevents z from encoding mod-60-deg residue.
        self._nbr_I = np.array([1.00, 0.85, 0.70, 0.95, 0.60, 0.80],
                               dtype=np.float32) * I_bg

    def __len__(self):
        return self.n

    def _render(self, c, theta, tx, ty, noise_seed):
        S = self.S
        ys, xs = np.mgrid[0:S, 0:S].astype(np.float32)
        xs -= (S - 1) / 2.0
        ys -= (S - 1) / 2.0
        cs, sn = math.cos(theta), math.sin(theta)
        # rotate coords (rotates the whole patch by theta)
        xr = cs * xs + sn * ys - tx
        yr = -sn * xs + cs * ys - ty
        img = np.zeros((S, S), np.float32)
        # central defect atom (intensity scales with c)
        I_centre = self.I_v + c * (self.I_a - self.I_v)
        img = np.maximum(img, I_centre * np.exp(
            -(xr * xr + yr * yr) / (2 * self.sigma ** 2)))
        # six fixed neighbour background atoms (asymmetric intensities)
        for (nx, ny), I_n in zip(self._nbrs, self._nbr_I):
            dx = xr - nx
            dy = yr - ny
            img = np.maximum(img, float(I_n) * np.exp(
                -(dx * dx + dy * dy) / (2 * self.sigma ** 2)))
        rng = np.random.default_rng(noise_seed)
        img = img + rng.standard_normal(img.shape).astype(np.float32) * self.noise_std
        return np.clip(img, 0.0, 1.0).astype(np.float32)

    def __getitem__(self, idx):
        img = self._render(float(self.c[idx]), float(self.theta[idx]),
                           float(self.tx[idx]), float(self.ty[idx]),
                           int(self._noise_seeds[idx]))
        return (
            torch.from_numpy(img).unsqueeze(0),
            torch.tensor([self.c[idx], self.theta[idx],
                          self.tx[idx], self.ty[idx]], dtype=torch.float32),
        )


# --------------------------------------------------------------------------
# Tiny rVAE (32x32, zdim=1)
# --------------------------------------------------------------------------
class TinyConvEncoder(nn.Module):
    def __init__(self, zdim=1, nuisance_dim=3, hidden=32):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(1, hidden, 4, 2, 1), nn.ReLU(True),         # 16
            nn.Conv2d(hidden, hidden*2, 4, 2, 1), nn.ReLU(True),  # 8
            nn.Conv2d(hidden*2, hidden*4, 4, 2, 1), nn.ReLU(True),# 4
            nn.Flatten(),
            nn.Linear(hidden*4*4*4, 128), nn.ReLU(True),
        )
        self.fc_mu = nn.Linear(128, zdim)
        self.fc_lv = nn.Linear(128, zdim)
        self.fc_nu = nn.Linear(128, nuisance_dim)

    def forward(self, x):
        h = self.net(x)
        return self.fc_mu(h), torch.clamp(self.fc_lv(h), -8.0, 8.0), self.fc_nu(h)


class TinyCoordDecoder(nn.Module):
    def __init__(self, zdim=1, hidden=128, n_layers=4, n_fourier=12, sigma=5.0):
        super().__init__()
        B = torch.randn(2, n_fourier) * sigma
        self.register_buffer("B", B)
        in_dim = zdim + 2 * n_fourier
        layers = [nn.Linear(in_dim, hidden), nn.SiLU()]
        for _ in range(n_layers - 1):
            layers += [nn.Linear(hidden, hidden), nn.SiLU()]
        layers += [nn.Linear(hidden, 1), nn.Sigmoid()]
        self.mlp = nn.Sequential(*layers)

    def forward(self, z, grid):
        Bsz, HW, _ = grid.shape
        proj = 2 * math.pi * grid @ self.B
        ff = torch.cat([torch.sin(proj), torch.cos(proj)], dim=-1)
        z_rep = z.unsqueeze(1).expand(-1, HW, -1)
        h = torch.cat([z_rep, ff], dim=-1)
        out = self.mlp(h).squeeze(-1)
        S = int(math.sqrt(HW))
        return out.view(Bsz, 1, S, S)


class TinyRVAE(nn.Module):
    def __init__(self, img_size=32, zdim=1):
        super().__init__()
        self.img_size = img_size
        self.zdim = zdim
        self.encoder = TinyConvEncoder(zdim=zdim)
        self.decoder = TinyCoordDecoder(zdim=zdim)
        ys, xs = torch.meshgrid(
            torch.linspace(-1, 1, img_size),
            torch.linspace(-1, 1, img_size),
            indexing="ij",
        )
        self.register_buffer("grid0", torch.stack([xs, ys], dim=-1).view(-1, 2))

    def transform_grid(self, theta, t):
        B = theta.shape[0]
        c, s = torch.cos(theta), torch.sin(theta)
        R = torch.stack([torch.stack([c, s], -1),
                         torch.stack([-s, c], -1)], dim=-2)
        grid = self.grid0.unsqueeze(0).expand(B, -1, -1) - t.unsqueeze(1)
        grid = torch.einsum("bij,bnj->bni", R, grid)
        return grid

    def forward(self, x):
        mu, lv, nu = self.encoder(x)
        z = mu + torch.exp(0.5 * lv) * torch.randn_like(mu)
        theta = nu[:, 0]
        t = nu[:, 1:3] * (2.0 / self.img_size)
        grid = self.transform_grid(theta, t)
        x_hat = self.decoder(z, grid)
        return x_hat, mu, lv, nu


# --------------------------------------------------------------------------
# Training
# --------------------------------------------------------------------------
def kl_normal(mu, logvar):
    return -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp(), dim=1)


def train_rvae(model, train_loader, val_loader, device, epochs, beta, lr,
               beta_warmup=5, logf=None):
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    hist = []
    for ep in range(1, epochs + 1):
        eff_beta = beta * min(1.0, (ep - 1) / max(1, beta_warmup)) if beta_warmup > 0 else beta
        model.train()
        t0 = time.time()
        tot, tot_rec, tot_kl, n = 0.0, 0.0, 0.0, 0
        for x, _ in train_loader:
            x = x.to(device)
            x_hat, mu, lv, _ = model(x)
            rec = F.mse_loss(x_hat, x, reduction="sum") / x.size(0)
            kl = kl_normal(mu, lv).mean()
            loss = rec + eff_beta * kl
            opt.zero_grad(); loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0)
            opt.step()
            bs = x.size(0); n += bs
            tot += loss.item() * bs; tot_rec += rec.item() * bs; tot_kl += kl.item() * bs
        # val
        model.eval()
        with torch.no_grad():
            v_rec, v_kl, vn = 0.0, 0.0, 0
            for x, _ in val_loader:
                x = x.to(device)
                x_hat, mu, lv, _ = model(x)
                rec = F.mse_loss(x_hat, x, reduction="sum") / x.size(0)
                kl = kl_normal(mu, lv).mean()
                bs = x.size(0); vn += bs
                v_rec += rec.item() * bs; v_kl += kl.item() * bs
        msg = (f"ep {ep:03d}/{epochs}  beta={eff_beta:.3f}  "
               f"tr_loss={tot/n:7.3f} rec={tot_rec/n:7.3f} kl={tot_kl/n:6.3f}  "
               f"val_rec={v_rec/vn:7.3f} val_kl={v_kl/vn:6.3f}  ({time.time()-t0:.1f}s)")
        print(msg, flush=True)
        if logf is not None:
            logf.write(msg + "\n"); logf.flush()
        hist.append(dict(epoch=ep, tr_loss=tot/n, tr_rec=tot_rec/n, tr_kl=tot_kl/n,
                         val_rec=v_rec/vn, val_kl=v_kl/vn))
    return hist


@torch.no_grad()
def encode_dataset(model, loader, device):
    model.eval()
    mus, ys = [], []
    for x, y in loader:
        mu, _, _ = model.encoder(x.to(device))
        mus.append(mu.cpu().numpy()); ys.append(y.numpy())
    return np.concatenate(mus), np.concatenate(ys)


# --------------------------------------------------------------------------
# Kalman filter / RTS smoother (1D constant-level + drift)
# --------------------------------------------------------------------------
def kalman_rts(measurements: np.ndarray, dt: float,
               q_pos: float = 1e-4, q_vel: float = 1e-3,
               r_meas: float = 1e-2):
    """Constant-velocity Kalman filter + RTS smoother on a scalar series.

    State x = [c, c_dot]. Transition:
        c_{k+1}   = c_k + dt * c_dot_k
        c_dot_{k+1} = c_dot_k
    Process noise covariance Q = diag(q_pos, q_vel).
    Measurement: y_k = c_k + v,  v ~ N(0, r_meas).

    Returns: filtered means, smoothed means, smoothed covariance for c.
    """
    F_mat = np.array([[1.0, dt], [0.0, 1.0]])
    H = np.array([[1.0, 0.0]])
    Q = np.diag([q_pos, q_vel])
    R = np.array([[r_meas]])

    n = len(measurements)
    mu_f = np.zeros((n, 2))
    P_f = np.zeros((n, 2, 2))
    mu_p = np.zeros((n, 2))
    P_p = np.zeros((n, 2, 2))

    mu = np.array([measurements[0], 0.0])
    P = np.diag([1.0, 1.0])
    for k in range(n):
        # predict
        mu_pred = F_mat @ mu
        P_pred = F_mat @ P @ F_mat.T + Q
        # update
        y = np.array([measurements[k]])
        S = H @ P_pred @ H.T + R
        K = P_pred @ H.T @ np.linalg.inv(S)
        mu = mu_pred + (K @ (y - H @ mu_pred)).flatten()
        P = (np.eye(2) - K @ H) @ P_pred
        mu_f[k] = mu; P_f[k] = P
        mu_p[k] = mu_pred; P_p[k] = P_pred

    # RTS backward
    mu_s = mu_f.copy(); P_s = P_f.copy()
    for k in range(n - 2, -1, -1):
        C = P_f[k] @ F_mat.T @ np.linalg.inv(P_p[k + 1])
        mu_s[k] = mu_f[k] + C @ (mu_s[k + 1] - mu_p[k + 1])
        P_s[k] = P_f[k] + C @ (P_s[k + 1] - P_p[k + 1]) @ C.T
    return mu_f[:, 0], mu_s[:, 0], P_s[:, 0, 0]


# --------------------------------------------------------------------------
# Time-series experiment
# --------------------------------------------------------------------------
def run_experiment(args):
    if args.device == "cuda" and not torch.cuda.is_available():
        device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    else:
        device = torch.device(args.device)
    print(f"device={device}")
    torch.manual_seed(args.seed); np.random.seed(args.seed)

    args.outdir.mkdir(parents=True, exist_ok=True)
    args.figdir.mkdir(parents=True, exist_ok=True)

    # ---------------- 1. Train rVAE on i.i.d. defect patches ----------------
    print(f"[1/5] building i.i.d. patch dataset (fix_pose={args.fix_pose})")
    train_ds = DefectPatchDataset(args.n_train, seed=args.seed,
                                  fix_pose=args.fix_pose)
    val_ds = DefectPatchDataset(args.n_val, seed=args.seed + 1,
                                fix_pose=args.fix_pose)
    tl = DataLoader(train_ds, batch_size=args.batch, shuffle=True,
                    num_workers=args.workers, pin_memory=True, drop_last=True)
    vl = DataLoader(val_ds, batch_size=args.batch, shuffle=False,
                    num_workers=args.workers, pin_memory=True)

    print(f"[2/5] training rVAE (zdim={args.zdim})")
    model = TinyRVAE(img_size=32, zdim=args.zdim).to(device)
    n_par = sum(p.numel() for p in model.parameters())
    print(f"  params: {n_par/1e6:.2f} M")
    log = open(args.outdir / "train_timeseries.log", "w")
    hist = train_rvae(model, tl, vl, device, args.epochs, args.beta, args.lr,
                      beta_warmup=args.beta_warmup, logf=log)
    log.close()
    torch.save(model.state_dict(), args.outdir / "model_timeseries.pt")

    # ---------------- 3. Calibrate z -> c on training set ------------------
    print("[3/5] encoding training set for z->c calibration")
    cal_loader = DataLoader(train_ds, batch_size=args.batch, shuffle=False,
                            num_workers=args.workers)
    z_train, y_train = encode_dataset(model, cal_loader, device)
    c_train = y_train[:, 0]
    # pick the best z-dim (highest |Pearson r| with c) -- the rVAE is
    # 'parsimonious': only one latent should track the physical factor
    z_train_dims = z_train if z_train.ndim > 1 else z_train.reshape(-1, 1)
    rs = [float(np.corrcoef(z_train_dims[:, k], c_train)[0, 1])
          for k in range(z_train_dims.shape[1])]
    best_dim = int(np.argmax(np.abs(rs)))
    r_zc = rs[best_dim]
    print(f"  per-dim Pearson(z_k, c): {[f'{r:+.4f}' for r in rs]}")
    print(f"  selected best dim = z{best_dim}  (|r|={abs(r_zc):.4f})")
    z_train_best = z_train_dims[:, best_dim]
    a_lin, b_lin = np.polyfit(z_train_best, c_train, 1)
    print(f"  linear calibration:  c_hat = {a_lin:+.4f} * z{best_dim}  +  {b_lin:+.4f}")

    # ---------------- 4. Synthesise time series with first-order kinetics --
    print("[4/5] synthesising time series with Arrhenius first-order kinetics")
    T = args.n_frames
    dt = args.dt
    k_true = args.k_true
    t_grid = np.arange(T, dtype=np.float32) * dt
    c_true = np.exp(-k_true * t_grid).astype(np.float32)   # antisite -> vacancy

    ts_ds = DefectPatchDataset(T, seed=args.seed + 100, c_values=c_true,
                               noise_std=args.noise_std_ts,
                               fix_pose=args.fix_pose)
    ts_loader = DataLoader(ts_ds, batch_size=args.batch, shuffle=False, num_workers=0)
    z_ts_all, y_ts = encode_dataset(model, ts_loader, device)
    z_ts_all = z_ts_all if z_ts_all.ndim > 1 else z_ts_all.reshape(-1, 1)
    z_ts = z_ts_all[:, best_dim]
    c_hat_raw = a_lin * z_ts + b_lin
    # clip to physically valid range so log() is well defined
    c_hat_raw_clipped = np.clip(c_hat_raw, 1e-3, 1.5)

    # ---------------- 5. Kalman / RTS smoother and kinetics fit ------------
    print("[5/5] Kalman / RTS smoothing and Arrhenius fit")
    # robust measurement noise estimate from high-frequency residual
    diff = np.diff(c_hat_raw)
    r_meas = float(0.5 * np.var(diff))
    if r_meas <= 0: r_meas = 1e-3
    c_filt, c_smooth, c_smooth_var = kalman_rts(
        c_hat_raw, dt=dt, q_pos=1e-5, q_vel=5e-4, r_meas=r_meas
    )
    c_smooth_clipped = np.clip(c_smooth, 1e-3, 1.5)

    # fit log(c) vs t -> -k
    # raw fit
    p_raw = np.polyfit(t_grid, np.log(c_hat_raw_clipped), 1)
    k_raw = -p_raw[0]
    # smoothed fit
    p_sm = np.polyfit(t_grid, np.log(c_smooth_clipped), 1)
    k_smooth = -p_sm[0]

    # diagnostic correlations / agreement
    pearson_z_c = float(np.corrcoef(z_ts, c_true)[0, 1])
    pearson_chat_c = float(np.corrcoef(c_hat_raw, c_true)[0, 1])
    pearson_smooth_c = float(np.corrcoef(c_smooth, c_true)[0, 1])
    rmse_raw = float(np.sqrt(np.mean((c_hat_raw - c_true) ** 2)))
    rmse_smooth = float(np.sqrt(np.mean((c_smooth - c_true) ** 2)))

    # paper-style "coverage / agreement" scores for this experiment
    # coverage = |corr(z, c_true)| (latent recovers transformation coordinate)
    # agreement = 1 - |k_smooth - k_true| / k_true   (kinetics rate accuracy)
    cov_score = abs(pearson_z_c)
    agr_score = max(0.0, 1.0 - abs(k_smooth - k_true) / max(k_true, 1e-9))

    results = dict(
        n_train=args.n_train, n_val=args.n_val, n_frames=T,
        k_true=float(k_true), k_raw=float(k_raw), k_smooth=float(k_smooth),
        rate_error_raw_pct=float(100.0 * abs(k_raw - k_true) / k_true),
        rate_error_smooth_pct=float(100.0 * abs(k_smooth - k_true) / k_true),
        pearson_train_z_vs_c=r_zc,
        pearson_z_vs_c_true=pearson_z_c,
        pearson_chat_vs_c_true=pearson_chat_c,
        pearson_smooth_vs_c_true=pearson_smooth_c,
        rmse_chat_raw=rmse_raw,
        rmse_chat_smoothed=rmse_smooth,
        coverage_score=float(cov_score),
        agreement_score=float(agr_score),
        calibration_a=float(a_lin), calibration_b=float(b_lin),
        kalman_q_pos=1e-5, kalman_q_vel=5e-4, kalman_r_meas=r_meas,
        zdim=int(args.zdim), best_z_dim=int(best_dim),
        per_dim_train_pearson=[float(r) for r in rs],
        params_millions=float(n_par / 1e6),
        final_train=hist[-1],
    )
    with open(args.outdir / "results_timeseries.json", "w") as f:
        json.dump(results, f, indent=2)
    print(json.dumps(results, indent=2))

    # ---------------- 6. Plots ---------------------------------------------
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax1 = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
    ax1[0].plot(t_grid, z_ts, "o", ms=3, alpha=0.5, label="raw rVAE latent z(t)")
    ax1[0].set_ylabel("rVAE latent z (a.u.)")
    ax1[0].set_title("Per-frame rVAE latent on antisite→vacancy time series")
    ax1[0].legend(loc="best"); ax1[0].grid(alpha=0.3)

    ax1[1].plot(t_grid, c_true,     "k-",  lw=2, label=f"ground truth $c(t)=e^{{-k t}}$, $k={k_true:.3f}$")
    ax1[1].plot(t_grid, c_hat_raw,  "o",   ms=3, alpha=0.4, color="tab:orange",
                label=f"$\\hat c(t)$ raw  (RMSE={rmse_raw:.3f})")
    ax1[1].plot(t_grid, c_smooth,   "-",   lw=2, color="tab:blue",
                label=f"$\\hat c(t)$ Kalman/RTS  (RMSE={rmse_smooth:.3f})")
    ax1[1].fill_between(t_grid, c_smooth - 2*np.sqrt(c_smooth_var),
                                 c_smooth + 2*np.sqrt(c_smooth_var),
                        alpha=0.18, color="tab:blue", label="$\\pm 2\\sigma$ smoother")
    ax1[1].set_xlabel("time (a.u.)")
    ax1[1].set_ylabel("antisite occupancy $c$")
    ax1[1].set_title(f"Calibrated occupancy estimate vs ground truth "
                     f"($|r|_{{z\\leftrightarrow c}}={pearson_z_c:+.3f}$)")
    ax1[1].legend(loc="best"); ax1[1].grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(args.figdir / "latent_trajectory.png", dpi=150)
    plt.close(fig)

    # kinetics figure
    fig, ax = plt.subplots(1, 1, figsize=(7, 5))
    ax.plot(t_grid, np.log(c_hat_raw_clipped), "o", ms=3, alpha=0.5,
            color="tab:orange", label="$\\log\\hat c$ raw (per-frame)")
    ax.plot(t_grid, np.log(c_smooth_clipped), "-", lw=2, color="tab:blue",
            label=f"$\\log\\hat c$ Kalman-smoothed (slope $\\Rightarrow k_{{est}}={k_smooth:.4f}$)")
    ax.plot(t_grid, np.log(np.clip(c_true, 1e-6, None)),
            "k--", lw=2, label=f"ground truth ($k_{{true}}={k_true:.4f}$)")
    ax.set_xlabel("time (a.u.)")
    ax.set_ylabel(r"$\log c(t)$")
    ax.set_title(
        f"Arrhenius kinetics fit: "
        f"$|k_{{est}}-k_{{true}}|/k_{{true}} = {100*abs(k_smooth-k_true)/k_true:.1f}$%  "
        f"(raw: {100*abs(k_raw-k_true)/k_true:.1f}%)"
    )
    ax.legend(loc="best"); ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(args.figdir / "kinetics_estimate.png", dpi=150)
    plt.close(fig)

    print(f"\nSaved figures to {args.figdir}")
    print(f"Saved results / model / log to {args.outdir}")
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", type=Path,
                    default=Path(__file__).resolve().parent.parent / "results")
    ap.add_argument("--figdir", type=Path,
                    default=Path(__file__).resolve().parent.parent / "report")
    ap.add_argument("--epochs", type=int, default=25)
    ap.add_argument("--batch", type=int, default=128)
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--beta", type=float, default=0.5)
    ap.add_argument("--beta_warmup", type=int, default=5)
    ap.add_argument("--n_train", type=int, default=6000)
    ap.add_argument("--n_val", type=int, default=600)
    ap.add_argument("--n_frames", type=int, default=200)
    ap.add_argument("--dt", type=float, default=0.05)
    ap.add_argument("--k_true", type=float, default=0.20)   # exp half-life ~ 3.5
    ap.add_argument("--noise_std_ts", type=float, default=0.04)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--zdim", type=int, default=2)
    ap.add_argument("--fix_pose", action="store_true",
                    help="Disable pose variation in synthesised patches (matches"
                         " the paper's defect-tracking workflow where patches are"
                         " already registered upstream).")
    args = ap.parse_args()
    run_experiment(args)


if __name__ == "__main__":
    main()
