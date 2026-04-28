"""ERA5 climate emulation experiment (paper Section 4.4).

Paper uses ERA5 Jan 2000 - Dec 2009 regridded to T30 Gaussian with 4 vars
(t, q, u, v) at specific sigma levels, plus TISR.

We approximate with WeatherBench2 pre-downloaded data at 5.625 deg
(64x32 grid, daily 2m temperature or 500hPa geopotential),
since direct CDS download may be blocked.

Fallback chain:
  1. Try WeatherBench zenodo 5.625deg dataset via HTTPS (no auth).
  2. If blocked -> use synthetic quasi-atmospheric data (documented).
"""
import argparse, json, os, sys, time, urllib.request
import numpy as np
import torch
import torch.nn as nn
from torchdiffeq import odeint

sys.path.insert(0, os.path.dirname(__file__))
from mp_node import DilatedCNNRHS, integrate_segments, mp_loss


# WeatherBench 1.0 - 5.625 deg - publicly downloadable from TU Munich
# Note: paper used ~5.625 deg effective too.
# Mediatum WebDAV direct file URL (discovered via dataserv.ub.tum.de index)
WB_URL_TEMPLATE = (
    "https://dataserv.ub.tum.de/s/m1524895/download?"
    "path=%2F5.625deg%2F{var}&files={var}_{year}_5.625deg.nc"
)
# Alternative: Pangeo ESGF mirror (zarr), or try raw mediatum ID.
MEDIATUM_URL = (
    "https://dataserv.ub.tum.de/public.php/webdav/"
    "5.625deg/{var}/{var}_{year}_5.625deg.nc"
)


def try_download_weatherbench(data_dir, years=(2000, 2001, 2002), var='temperature_850'):
    """Return path to local nc files or None on failure."""
    os.makedirs(data_dir, exist_ok=True)
    paths = []
    for y in years:
        p = os.path.join(data_dir, f"{var}_{y}_5.625deg.nc")
        if os.path.exists(p) and os.path.getsize(p) > 1000:
            paths.append(p); continue
        ok = False
        for tmpl in (MEDIATUM_URL, WB_URL_TEMPLATE):
            url = tmpl.format(var=var, year=y)
            try:
                print(f"[ERA5] trying {url}")
                import subprocess
                ret = subprocess.run(["curl", "-sLf", "-m", "120", "-o", p,
                                      "-u", "m1524895:m1524895", url],
                                     capture_output=True)
                if ret.returncode == 0 and os.path.getsize(p) > 10000:
                    paths.append(p); ok = True; break
            except Exception as e:
                print(f"[ERA5]   failed: {e}")
        if not ok and os.path.exists(p):
            os.remove(p)
    return paths if paths else None


def load_weatherbench(paths):
    import xarray as xr
    ds = xr.open_mfdataset(paths, combine='by_coords')
    # Pick the main variable (first data var)
    var = list(ds.data_vars)[0]
    arr = ds[var].values.astype(np.float32)  # [T, lev?, lat, lon] or [T, lat, lon]
    while arr.ndim > 3:
        arr = arr[:, 0]  # drop level
    print(f"[ERA5] loaded {var} shape={arr.shape}")
    return arr  # [T, H, W]


def synthetic_atmosphere_simple(T=4000, H=32, W=64, seed=0):
    """Very-tame fallback: simple AR(1) + wave drift. Last resort."""
    print("[ERA5] simple fallback in use")
    rng = np.random.default_rng(seed)
    arr = np.zeros((T, H, W), dtype=np.float32)
    lat = np.linspace(-np.pi/2, np.pi/2, H)
    lon = np.linspace(0, 2*np.pi, W, endpoint=False)
    LAT, LON = np.meshgrid(lat, lon, indexing='ij')
    bg = 273.0 + 20 * np.cos(LAT)
    state = rng.standard_normal((H, W)) * 2.0
    for t in range(T):
        wave = 2 * np.sin(3 * LON - 0.1 * t) + np.cos(2 * LAT + 0.07 * t)
        state = 0.95 * state + 0.1 * rng.standard_normal((H, W)) + 0.05 * wave
        arr[t] = (bg + 3 * state).astype(np.float32)
    return arr


def synthetic_atmosphere(T=4000, H=32, W=64, seed=0):
    """Fallback: a 2D barotropic beta-plane Kolmogorov turbulence, used when
    real ERA5 data cannot be downloaded. Clearly flagged in the report.

    This is a vorticity-formulation 2D NS on a doubly periodic pseudo-
    sphere grid, with Kolmogorov-style forcing and latitude-dependent
    background temperature superimposed. It produces genuinely chaotic
    trajectories with broadband Fourier energy.
    """
    print("[ERA5] WARNING: using synthetic 2D-turbulence proxy (WB download failed).")
    rng = np.random.default_rng(seed)
    # Wavenumbers matching shape [H, W]
    ky_arr = 2 * np.pi * np.fft.fftfreq(H, d=1.0 / H) / H  # size H (1/radian)
    kx_arr = 2 * np.pi * np.fft.fftfreq(W, d=1.0 / W) / W  # size W
    KY, KX = np.meshgrid(ky_arr, kx_arr, indexing='ij')  # [H, W]
    K2 = KX**2 + KY**2
    K2_safe = K2.copy(); K2_safe[0, 0] = 1.0
    # Dealiasing
    kmax = min(H, W) // 3
    dealias = ((np.abs(KX) < kmax) & (np.abs(KY) < kmax)).astype(float)

    # Initial vorticity: random, low-k
    psi_hat = rng.standard_normal((H, W)) + 1j * rng.standard_normal((H, W))
    psi_hat = psi_hat * (np.sqrt(K2) < 5) * 0.5
    w_hat = -K2 * psi_hat

    # Use low Re for stability of simple 2nd-order solver
    Re = 40.0; nu = 1 / Re; r = 0.1; kf = 4; A = 1.0
    lat_arr = np.linspace(-np.pi/2, np.pi/2, H)
    lon_arr = np.linspace(0, 2*np.pi, W, endpoint=False)
    LAT, LON = np.meshgrid(lat_arr, lon_arr, indexing='ij')
    # Kolmogorov forcing: sin(kf*y) -> in vorticity: -kf*cos(kf*y)
    y_grid = np.linspace(0, 2*np.pi, H, endpoint=False)[:, None]
    f_w = -A * kf * np.cos(kf * y_grid) * np.ones_like(LAT)
    f_w_hat = np.fft.fft2(f_w)

    def N(w_hat):
        psi_hat = w_hat / K2_safe; psi_hat[0, 0] = 0
        u = np.real(np.fft.ifft2(1j * KY * psi_hat))
        v = np.real(np.fft.ifft2(-1j * KX * psi_hat))
        wx = np.real(np.fft.ifft2(1j * KX * w_hat))
        wy = np.real(np.fft.ifft2(1j * KY * w_hat))
        adv = np.fft.fft2(u * wx + v * wy) * dealias
        return -adv - nu * K2 * w_hat - r * w_hat + f_w_hat

    dt = 0.005
    # Burn-in with RK4 for stability
    def rk4_step(w):
        k1 = N(w)
        k2 = N(w + 0.5 * dt * k1)
        k3 = N(w + 0.5 * dt * k2)
        k4 = N(w + dt * k3)
        return w + dt / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)
    for _ in range(int(50.0 / dt)):
        w_hat = rk4_step(w_hat)
        if np.isnan(w_hat).any():
            print("[ERA5] synthetic burn-in diverged, reducing amplitude")
            return synthetic_atmosphere_simple(T=T, H=H, W=W, seed=seed+1)

    # Collect T snapshots every 20 steps (dt_sample = 0.2)
    sample_every = 20
    arr = np.zeros((T, H, W), dtype=np.float32)
    idx = 0
    step = 0
    bg = 273.0 + 20 * np.cos(LAT) + 5 * np.sin(LAT * 2)
    step_count = 0
    while idx < T:
        w_hat = rk4_step(w_hat)
        step_count += 1
        if step_count % sample_every == 0:
            w_re = np.real(np.fft.ifft2(w_hat))
            # Map vorticity to temperature-like scalar field
            arr[idx] = (bg + 10 * np.tanh(w_re / 5.0)).astype(np.float32)
            idx += 1
    print(f"[ERA5] synthetic generated {arr.shape}, mean={arr.mean():.2f}, "
          f"std={arr.std():.2f}, |max|={np.abs(arr).max():.2f}")
    return arr


# --- Architecture: same as Kolmogorov but no compressive encoder (per paper) ---
class ERA5Model(nn.Module):
    """NODE RHS that operates in full state space (no encoder)."""
    def __init__(self, channels=1, hidden=32):
        super().__init__()
        dilations = (1, 2, 3, 4, 3, 2, 1)
        layers = []
        in_c = channels
        for i, d in enumerate(dilations):
            out_c = hidden if i < len(dilations) - 1 else channels
            layers.append(nn.Conv2d(in_c, out_c, 3, padding=d, dilation=d,
                                    padding_mode='circular'))
            if i < len(dilations) - 1:
                layers.append(nn.GELU())
            in_c = out_c
        self.net = nn.Sequential(*layers)

    def forward(self, t, y):
        return self.net(y)


def make_batches_2d(u_traj, seg_len, K, n_traj, seed=1):
    rng = np.random.default_rng(seed)
    total_len = K * seg_len + 1
    assert u_traj.shape[0] > total_len
    starts = rng.integers(0, u_traj.shape[0] - total_len, size=n_traj)
    batches = np.stack([u_traj[s: s + total_len] for s in starts])  # [B, T, C, H, W]
    B, T, C, H, W = batches.shape
    y_per_seg = np.zeros((seg_len + 1, B, K, C, H, W), dtype=np.float32)
    ic_per_seg = np.zeros((B, K, C, H, W), dtype=np.float32)
    for k in range(K):
        seg = batches[:, k * seg_len: k * seg_len + seg_len + 1]
        y_per_seg[:, :, k] = seg.transpose(1, 0, 2, 3, 4)
        ic_per_seg[:, k] = seg[:, 0]
    return y_per_seg, ic_per_seg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='results/era5')
    ap.add_argument('--data', default='data/era5.npz')
    ap.add_argument('--K', type=int, default=6)
    ap.add_argument('--seg-len', type=int, default=4)  # 4 x 6h = 24h per segment
    ap.add_argument('--n-traj', type=int, default=16)
    ap.add_argument('--epochs-per-mu', type=int, default=30)
    ap.add_argument('--lr', type=float, default=1e-3)
    ap.add_argument('--lr-q', type=float, default=1e-2)
    ap.add_argument('--device', default='cuda')
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    os.makedirs(os.path.dirname(args.data) or '.', exist_ok=True)
    device = torch.device(args.device if torch.cuda.is_available() else 'cpu')

    if os.path.exists(args.data):
        d = np.load(args.data)
        u_raw = d['u']
        is_real = bool(d.get('is_real', np.array(False)).item())
        print(f"[ERA5] loaded cached {u_raw.shape}, real={is_real}")
    else:
        paths = try_download_weatherbench(os.path.dirname(args.data) or '.',
                                           years=(2000, 2001, 2002),
                                           var='temperature_850')
        if paths:
            u_raw = load_weatherbench(paths)
            is_real = True
        else:
            u_raw = synthetic_atmosphere(T=4000, H=32, W=64)
            is_real = False
        np.savez_compressed(args.data, u=u_raw, is_real=is_real)

    # Ensure shape [T, H, W]
    if u_raw.ndim == 3:
        u_raw = u_raw[:, None]  # add channel
    print(f"[ERA5] data={u_raw.shape}  real={is_real}")

    # Normalize per-channel
    mean = u_raw.mean(axis=(0, 2, 3), keepdims=True)
    std = u_raw.std(axis=(0, 2, 3), keepdims=True) + 1e-6
    u_norm = (u_raw - mean) / std

    split = int(0.8 * u_norm.shape[0])
    u_train = u_norm[:split]
    u_test = u_norm[split:]

    y_np, ic_np = make_batches_2d(u_train, seg_len=args.seg_len, K=args.K,
                                  n_traj=args.n_traj)
    y_true = torch.tensor(y_np, device=device)
    ic_init = torch.tensor(ic_np, device=device)
    print(f"[ERA5] y={tuple(y_true.shape)}")

    C = u_raw.shape[1]
    model = ERA5Model(channels=C, hidden=32).to(device)
    q_param = nn.Parameter(ic_init.clone())
    ic_pin = ic_init[:, 0:1].clone()

    opt_theta = torch.optim.Adam(model.parameters(), lr=args.lr)
    opt_q = torch.optim.Adam([q_param], lr=args.lr_q)
    t_seg = torch.linspace(0, float(args.seg_len), args.seg_len + 1, device=device)

    mu_schedule = [1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1.0]
    history = []; start = time.time(); best_loss = float('inf')

    for stage, mu in enumerate(mu_schedule):
        for epoch in range(args.epochs_per_mu):
            with torch.no_grad():
                q_param[:, 0:1] = ic_pin
            traj_pred, _ = integrate_segments(model, q_param, t_seg, method='rk4')
            loss, d_loss, p_loss = mp_loss(traj_pred, y_true, q_param, mu)
            opt_theta.zero_grad(); opt_q.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt_theta.step(); opt_q.step()
            if epoch % 3 == 0 or epoch == args.epochs_per_mu - 1:
                print(f"[ERA5] s={stage} mu={mu:.1e} ep={epoch} "
                      f"tot={loss.item():.4e} data={d_loss.item():.4e} "
                      f"pen={p_loss.item():.4e} t={time.time()-start:.1f}s",
                      flush=True)
            history.append(dict(stage=stage, mu=mu, epoch=epoch,
                                total=float(loss), data=float(d_loss),
                                pen=float(p_loss)))
            if d_loss.item() < best_loss:
                best_loss = d_loss.item()
                torch.save(model.state_dict(), os.path.join(args.out, 'best.pt'))

    torch.save(model.state_dict(), os.path.join(args.out, 'final.pt'))
    with open(os.path.join(args.out, 'history.json'), 'w') as f:
        json.dump(history, f)

    # --- Evaluation: rollout from test IC ---
    model.load_state_dict(torch.load(os.path.join(args.out, 'best.pt')))
    model.eval()

    # Compare to persistence and climatology
    n_ic = min(20, u_test.shape[0] // 30)
    horizon = 14  # steps (14 days if data is daily, or 14 x 6h = 3.5 days if 6h)
    rmse_model = np.zeros((n_ic, horizon + 1))
    rmse_pers = np.zeros((n_ic, horizon + 1))
    rmse_clim = np.zeros((n_ic, horizon + 1))
    climatology = u_train.mean(axis=0)  # [C, H, W] (in normalized space, ~0)

    for i in range(n_ic):
        i0 = i * 30
        if i0 + horizon + 1 > u_test.shape[0]:
            break
        u0 = torch.tensor(u_test[i0:i0+1], dtype=torch.float32, device=device)
        t_eval = torch.arange(horizon + 1, dtype=torch.float32, device=device)
        with torch.no_grad():
            sol = odeint(model, u0, t_eval, method='rk4').cpu().numpy()  # [h+1, 1, C, H, W]
        for h in range(horizon + 1):
            truth = u_test[i0 + h]
            rmse_model[i, h] = np.sqrt(((sol[h, 0] - truth) ** 2).mean())
            rmse_pers[i, h] = np.sqrt(((u_test[i0] - truth) ** 2).mean())
            rmse_clim[i, h] = np.sqrt(((climatology - truth) ** 2).mean())

    mean_model = rmse_model.mean(axis=0).tolist()
    mean_pers = rmse_pers.mean(axis=0).tolist()
    mean_clim = rmse_clim.mean(axis=0).tolist()

    # Skill: 1 - RMSE_model / RMSE_pers  (>0 beats persistence)
    skill_vs_pers = [1 - m / p if p > 0 else 0 for m, p in zip(mean_model, mean_pers)]

    metrics = dict(
        rmse_model_per_step=mean_model,
        rmse_persistence_per_step=mean_pers,
        rmse_climatology_per_step=mean_clim,
        skill_vs_persistence=skill_vs_pers,
        beats_persistence_at_step_1=mean_model[1] < mean_pers[1],
        beats_persistence_at_step_3=mean_model[3] < mean_pers[3] if horizon >= 3 else None,
        beats_persistence_at_step_7=mean_model[7] < mean_pers[7] if horizon >= 7 else None,
        beats_persistence_at_step_14=mean_model[14] < mean_pers[14] if horizon >= 14 else None,
        is_real_data=bool(is_real),
        wall_time_s=float(time.time() - start),
        best_train_loss=float(best_loss),
        hparams=vars(args),
    )
    with open(os.path.join(args.out, 'metrics.json'), 'w') as f:
        json.dump(metrics, f, indent=2)
    np.savez_compressed(os.path.join(args.out, 'rollout.npz'),
                        rmse_model=rmse_model, rmse_pers=rmse_pers,
                        rmse_clim=rmse_clim)
    print("[ERA5] DONE.", json.dumps({k: v for k, v in metrics.items()
                                      if 'per_step' not in k}, indent=2))


if __name__ == '__main__':
    main()
