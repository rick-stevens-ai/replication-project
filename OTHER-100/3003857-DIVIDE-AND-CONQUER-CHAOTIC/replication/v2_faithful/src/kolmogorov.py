"""2D Kolmogorov flow experiment (paper Section 4.3).

Paper spec:
  Domain: [0, 2pi]^2 periodic, 512x512 DNS filtered to 64x64.
  f = A*sin(k*y)*ex - r*u  with A=1, k=4, r=0.1, Re=1000.
  Sampled every T = 256*dt_DNS.
Architecture: Encoder(3 conv, k=7,5,2, ch=8,16,4) -> NODE (7 dilated CNN) -> Decoder.
Latent: 4 channels + 2 augmented channels.

We use a custom GPU pseudospectral solver in PyTorch (vorticity formulation),
at resolution 128x128 (compromise for budget) and filter to 64x64 for training.
"""
import argparse, json, os, time
import numpy as np
import torch
import torch.nn as nn
from torchdiffeq import odeint

import sys
sys.path.insert(0, os.path.dirname(__file__))
from mp_node import EncoderNODEDecoder, integrate_segments, mp_loss


# ---- Pseudospectral DNS in vorticity formulation ----
def kolmogorov_dns(N_dns=128, N_coarse=64, Re=1000.0, k_f=4, A=1.0, r=0.1,
                   dt=5e-3, T=1500.0, sample_every_dns=256, device='cuda', seed=0,
                   verbose=True):
    """Run 2D Navier-Stokes with Kolmogorov forcing.
    Returns tensor of shape [T_samples, 2, N_coarse, N_coarse] (u,v channels).
    """
    torch.manual_seed(seed)
    device = torch.device(device if torch.cuda.is_available() else 'cpu')
    L = 2 * np.pi
    kx = torch.fft.fftfreq(N_dns, d=L / N_dns).to(device) * 2 * np.pi
    ky = torch.fft.fftfreq(N_dns, d=L / N_dns).to(device) * 2 * np.pi
    KX, KY = torch.meshgrid(kx, ky, indexing='ij')
    K2 = KX**2 + KY**2
    K2_safe = K2.clone()
    K2_safe[0, 0] = 1.0  # avoid div0
    # Dealias filter (2/3 rule)
    k_max = (N_dns // 3)
    dealias = ((torch.abs(KX) < k_max * 2 * np.pi / L) &
               (torch.abs(KY) < k_max * 2 * np.pi / L)).float()

    # Initial condition: random, divergence-free via streamfunction.
    # Restrict to low wavenumbers only to avoid initial aliasing blowup.
    psi_hat = torch.randn(N_dns, N_dns, dtype=torch.cfloat, device=device)
    # Kill all but low wavenumber content (|k|<8)
    k_mag = torch.sqrt(K2)
    ic_mask = (k_mag < 8 * 2 * np.pi / L) & (k_mag > 0)
    psi_hat = psi_hat * ic_mask.to(psi_hat.dtype)
    # Normalize so initial vorticity amplitude is moderate
    psi_hat = psi_hat / (torch.abs(psi_hat).max() + 1e-12) * 0.5
    w_hat = -K2 * psi_hat

    # Forcing in vorticity form: curl(f) = -A*k_f*cos(k_f*y)*ex component ... actually
    # f = A*sin(k_f*y) e_x means vorticity forcing = -d/dy(A*sin(k_f*y)) = -A*k_f*cos(k_f*y)
    x = torch.arange(N_dns, device=device) * (L / N_dns)
    y = torch.arange(N_dns, device=device) * (L / N_dns)
    _, Y = torch.meshgrid(x, y, indexing='ij')
    f_w = -A * k_f * torch.cos(k_f * Y)  # real forcing on vorticity
    f_w_hat = torch.fft.fft2(f_w)

    nu = 1.0 / Re

    def rhs(w_hat):
        # Compute u, v from streamfunction psi: laplacian(psi) = -w  =>  psi_hat = w_hat / K2
        psi_hat = w_hat / K2_safe
        psi_hat[0, 0] = 0
        u_hat = 1j * KY * psi_hat  # u = d psi/dy  (2D)
        v_hat = -1j * KX * psi_hat  # v = -d psi/dx
        wx_hat = 1j * KX * w_hat
        wy_hat = 1j * KY * w_hat
        u = torch.fft.ifft2(u_hat).real
        v = torch.fft.ifft2(v_hat).real
        wx = torch.fft.ifft2(wx_hat).real
        wy = torch.fft.ifft2(wy_hat).real
        advect = torch.fft.fft2(u * wx + v * wy) * dealias
        # dw/dt = -advect - nu*K2*w - r*w + curl(f)
        return -advect - nu * K2 * w_hat - r * w_hat + f_w_hat

    # Integrating-factor RK2 for better stability with viscous + drag linear part.
    L_lin = -nu * K2 - r  # linear operator in vorticity spectral space
    def step_ifrk2(w_hat, dt):
        # Split: w_t = L_lin * w + N(w), with N(w) = -advect + f_w_hat
        # IF-RK2 (Heun in integrating-factor form)
        def N(w):
            psi_hat = w / K2_safe
            psi_hat[0, 0] = 0
            u_hat = 1j * KY * psi_hat
            v_hat = -1j * KX * psi_hat
            wx_hat = 1j * KX * w
            wy_hat = 1j * KY * w
            u = torch.fft.ifft2(u_hat).real
            v = torch.fft.ifft2(v_hat).real
            wx = torch.fft.ifft2(wx_hat).real
            wy = torch.fft.ifft2(wy_hat).real
            advect = torch.fft.fft2(u * wx + v * wy) * dealias
            return -advect + f_w_hat
        E = torch.exp(L_lin * dt)
        k1 = N(w_hat)
        w_pred = E * (w_hat + dt * k1)
        k2 = N(w_pred)
        return E * w_hat + dt * 0.5 * (E * k1 + k2)

    # Burn-in
    n_burn = int(100.0 / dt)
    for i in range(n_burn):
        w_hat = step_ifrk2(w_hat, dt)
        if verbose and i % max(1, n_burn // 5) == 0:
            w_re = torch.fft.ifft2(w_hat).real
            print(f"  Kol burn-in {i}/{n_burn}  |w|max={w_re.abs().max().item():.2f}",
                  flush=True)

    # Sample
    n_steps = int(T / dt)
    n_samples = n_steps // sample_every_dns + 1
    out = torch.zeros(n_samples, 2, N_coarse, N_coarse, dtype=torch.float32)

    def filter_to_coarse(field_hat):
        # field_hat is NxN (full spectrum, fftshift-based crop).
        field_shift = torch.fft.fftshift(field_hat)
        c = N_dns // 2
        half = N_coarse // 2
        cropped = field_shift[c - half:c + half, c - half:c + half]
        cropped_unshift = torch.fft.ifftshift(cropped)
        field_c = torch.fft.ifft2(cropped_unshift).real
        # scale by ratio
        scale = (N_coarse / N_dns) ** 2
        return field_c * scale

    t0 = time.time()
    sidx = 0
    w_hat = w_hat.detach()
    # capture initial
    psi_hat = w_hat / K2_safe; psi_hat[0, 0] = 0
    u_c = filter_to_coarse(1j * KY * psi_hat)
    v_c = filter_to_coarse(-1j * KX * psi_hat)
    out[0, 0] = u_c.cpu(); out[0, 1] = v_c.cpu()
    sidx = 1

    for i in range(n_steps):
        w_hat = step_ifrk2(w_hat, dt)
        if (i + 1) % sample_every_dns == 0 and sidx < n_samples:
            psi_hat = w_hat / K2_safe; psi_hat[0, 0] = 0
            u_c = filter_to_coarse(1j * KY * psi_hat)
            v_c = filter_to_coarse(-1j * KX * psi_hat)
            out[sidx, 0] = u_c.cpu(); out[sidx, 1] = v_c.cpu()
            sidx += 1
            if verbose and sidx % max(1, n_samples // 10) == 0:
                print(f"  Kol sample {sidx}/{n_samples}  elapsed={time.time()-t0:.1f}s",
                      flush=True)
    return out[:sidx].numpy()


def make_batches_2d(u_traj, seg_len=5, K=12, n_traj=16, seed=1):
    """u_traj: [T, 2, H, W]. Return per-segment tensors."""
    rng = np.random.default_rng(seed)
    total_len = K * seg_len + 1
    assert u_traj.shape[0] > total_len
    starts = rng.integers(0, u_traj.shape[0] - total_len, size=n_traj)
    batches = np.stack([u_traj[s: s + total_len] for s in starts])  # [B, K*S+1, 2, H, W]
    B = batches.shape[0]
    _, _, C, H, W = batches.shape
    y_per_seg = np.zeros((seg_len + 1, B, K, C, H, W), dtype=np.float32)
    ic_per_seg = np.zeros((B, K, C, H, W), dtype=np.float32)
    for k in range(K):
        seg = batches[:, k * seg_len: k * seg_len + seg_len + 1]
        y_per_seg[:, :, k, :] = seg.transpose(1, 0, 2, 3, 4)
        ic_per_seg[:, k, :] = seg[:, 0]
    return y_per_seg, ic_per_seg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='results/kolmogorov')
    ap.add_argument('--data', default='data/kolmogorov_traj.npz')
    ap.add_argument('--N-dns', type=int, default=128)
    ap.add_argument('--N-coarse', type=int, default=64)
    ap.add_argument('--Re', type=float, default=1000.0)
    ap.add_argument('--kf', type=int, default=4)
    ap.add_argument('--T', type=float, default=800.0)
    ap.add_argument('--dt', type=float, default=2e-3)
    ap.add_argument('--sample-every', type=int, default=256)
    ap.add_argument('--K', type=int, default=12)
    ap.add_argument('--seg-len', type=int, default=5)
    ap.add_argument('--n-traj', type=int, default=8)
    ap.add_argument('--epochs-per-mu', type=int, default=30)
    ap.add_argument('--lr', type=float, default=1e-3)
    ap.add_argument('--lr-q', type=float, default=1e-2)
    ap.add_argument('--device', default='cuda')
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    os.makedirs(os.path.dirname(args.data) or '.', exist_ok=True)
    device = torch.device(args.device if torch.cuda.is_available() else 'cpu')
    print(f"[KOL] device={device}")

    if os.path.exists(args.data):
        d = np.load(args.data)
        u_traj = d['u']
        print(f"[KOL] loaded {u_traj.shape}")
    else:
        print(f"[KOL] running DNS: N={args.N_dns}, Re={args.Re}, T={args.T}")
        u_traj = kolmogorov_dns(N_dns=args.N_dns, N_coarse=args.N_coarse,
                                Re=args.Re, k_f=args.kf, dt=args.dt, T=args.T,
                                sample_every_dns=args.sample_every,
                                device=args.device)
        np.savez_compressed(args.data, u=u_traj)
        print(f"[KOL] saved {u_traj.shape}")

    # Normalize (per channel)
    u_mean = u_traj.mean(axis=(0, 2, 3), keepdims=True)
    u_std = u_traj.std(axis=(0, 2, 3), keepdims=True) + 1e-6
    u_traj_n = (u_traj - u_mean) / u_std

    # Split train/test
    split = int(0.8 * u_traj_n.shape[0])
    u_train = u_traj_n[:split]
    u_test = u_traj_n[split:]

    y_np, ic_np = make_batches_2d(u_train, seg_len=args.seg_len,
                                  K=args.K, n_traj=args.n_traj)
    y_true = torch.tensor(y_np, device=device)
    ic_init = torch.tensor(ic_np, device=device)
    print(f"[KOL] batches: y={tuple(y_true.shape)}  ic={tuple(ic_init.shape)}")

    H = W = args.N_coarse
    model = EncoderNODEDecoder(in_ch=2, lat_ch=4, augment=2, H=H, W=W).to(device)

    # Learnable segment ICs in physical space.
    # We integrate in latent space, so we encode each segment IC to latent.
    # Strategy: learnable latent starts q_lat (encoded from data initially).
    with torch.no_grad():
        B, K = ic_init.shape[:2]
        ic_flat = ic_init.reshape(B * K, 2, H, W)
        z_flat = model.encode(ic_flat)
        q_lat_init = z_flat.reshape(B, K, *z_flat.shape[1:])
    q_lat = nn.Parameter(q_lat_init.clone())

    # Precompute *latent* ground truth targets via encoder (teacher encoded)
    with torch.no_grad():
        S1, _, _, C, _, _ = y_np.shape
        y_flat = y_true.reshape(-1, 2, H, W)
        z_y_flat = model.encode(y_flat)  # warning: depends on encoder; will update
    # But since encoder is learning, we re-encode each step (targets in physical space).
    y_true_phys = y_true  # [S+1, B, K, 2, H, W]

    opt_theta = torch.optim.Adam(model.parameters(), lr=args.lr)
    opt_q = torch.optim.Adam([q_lat], lr=args.lr_q)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(
        opt_theta, T_max=len(range(args.epochs_per_mu)) * 6, eta_min=1e-5)

    t_seg = torch.linspace(0, float(args.seg_len), args.seg_len + 1, device=device)

    # penalty schedule per paper: 1e-5 .. 1e0
    mu_schedule = [1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1.0]
    history = []
    start = time.time()
    best_loss = float('inf')

    ic_pin_lat = q_lat_init[:, 0:1].detach().clone()

    for stage, mu in enumerate(mu_schedule):
        # re-encode pin to follow encoder updates
        for epoch in range(args.epochs_per_mu):
            # re-pin first segment IC from *current* encoder of data IC
            with torch.no_grad():
                z_pin = model.encode(ic_init[:, 0].reshape(B, 2, H, W))
                q_lat[:, 0] = z_pin

            # Integrate in latent space
            # integrate_segments expects [B,K,*state]
            sol_lat, _ = integrate_segments(model, q_lat, t_seg, method='rk4')
            # sol_lat: [S+1, B, K, C_lat, H, W]
            S1 = sol_lat.shape[0]
            sol_flat = sol_lat.reshape(-1, *sol_lat.shape[3:])  # [(S+1)*B*K, C_lat, H, W]
            pred_phys = model.decode(sol_flat).reshape(*sol_lat.shape[:3], 2, H, W)

            # Data loss (physical space)
            data_loss = ((pred_phys - y_true_phys) ** 2).mean()

            # Penalty loss (latent space)
            q_end_seg = sol_lat[-1]  # [B, K, C_lat, H, W]
            pen_loss = ((q_end_seg[:, :-1] - q_lat[:, 1:]) ** 2).mean()
            loss = data_loss + mu * pen_loss

            opt_theta.zero_grad(); opt_q.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt_theta.step(); opt_q.step()
            try:
                sched.step()
            except Exception:
                pass

            if epoch % 3 == 0 or epoch == args.epochs_per_mu - 1:
                print(f"[KOL] stage={stage} mu={mu:.1e} ep={epoch:3d} "
                      f"tot={loss.item():.4e} data={data_loss.item():.4e} "
                      f"pen={pen_loss.item():.4e} t={time.time()-start:.1f}s",
                      flush=True)
            history.append(dict(stage=stage, mu=mu, epoch=epoch,
                                total=float(loss), data=float(data_loss),
                                pen=float(pen_loss)))
            if data_loss.item() < best_loss:
                best_loss = data_loss.item()
                torch.save(model.state_dict(), os.path.join(args.out, 'best.pt'))

    torch.save(model.state_dict(), os.path.join(args.out, 'final.pt'))
    with open(os.path.join(args.out, 'history.json'), 'w') as f:
        json.dump(history, f)

    # --- Evaluation: rollout from test IC ---
    print("[KOL] Evaluating...")
    model.load_state_dict(torch.load(os.path.join(args.out, 'best.pt')))
    model.eval()
    u0 = torch.tensor(u_test[0:1], device=device)  # [1, 2, H, W]
    n_eval = min(60, u_test.shape[0] - 1)
    t_roll = torch.arange(n_eval + 1, dtype=torch.float32, device=device)
    with torch.no_grad():
        z0 = model.encode(u0)
        z_roll = odeint(model, z0, t_roll, method='rk4')  # [n+1, 1, C_lat, H, W]
        u_pred = model.decode(z_roll.reshape(-1, *z_roll.shape[2:])).reshape(
            n_eval + 1, 2, H, W).cpu().numpy()
    u_true = u_test[: n_eval + 1]

    # Metrics: correlation per step, energy spectrum
    corr = []
    for i in range(n_eval + 1):
        a = u_pred[i].flatten(); b = u_true[i].flatten()
        c = np.corrcoef(a, b)[0, 1]
        corr.append(float(c))

    # Energy spectrum (angle-averaged)
    def energy_spectrum(u):
        # u: [2, H, W]
        uh = np.fft.fft2(u[0]); vh = np.fft.fft2(u[1])
        E = 0.5 * (np.abs(uh) ** 2 + np.abs(vh) ** 2) / (u.shape[-1] * u.shape[-2])**2
        Hs, Ws = u.shape[-2:]
        kx = np.fft.fftfreq(Hs) * Hs
        ky = np.fft.fftfreq(Ws) * Ws
        KX, KY = np.meshgrid(kx, ky, indexing='ij')
        K = np.sqrt(KX**2 + KY**2)
        kbins = np.arange(0.5, min(Hs, Ws) // 2)
        Ek = np.zeros_like(kbins)
        for i, kb in enumerate(kbins):
            mask = (K >= kb - 0.5) & (K < kb + 0.5)
            Ek[i] = E[mask].sum()
        return kbins, Ek

    kbins, Ek_true = energy_spectrum(u_true[min(20, n_eval)])
    _, Ek_pred = energy_spectrum(u_pred[min(20, n_eval)])

    metrics = dict(
        correlation_per_step=corr,
        corr_at_step_5=corr[5] if len(corr) > 5 else None,
        corr_at_step_20=corr[20] if len(corr) > 20 else None,
        corr_at_step_40=corr[40] if len(corr) > 40 else None,
        n_steps_corr_above_0p9=int(sum(1 for c in corr if c > 0.9)),
        n_steps_corr_above_0p5=int(sum(1 for c in corr if c > 0.5)),
        spectrum_rmse=float(np.sqrt(((Ek_pred - Ek_true) ** 2).mean())),
        wall_time_s=float(time.time() - start),
        best_train_loss=float(best_loss),
        hparams=vars(args),
    )
    with open(os.path.join(args.out, 'metrics.json'), 'w') as f:
        json.dump(metrics, f, indent=2)
    np.savez_compressed(os.path.join(args.out, 'rollout.npz'),
                        u_true=u_true, u_pred=u_pred,
                        kbins=kbins, Ek_true=Ek_true, Ek_pred=Ek_pred)
    print("[KOL] DONE.", json.dumps({k: v for k, v in metrics.items()
                                     if k != 'correlation_per_step'}, indent=2))


if __name__ == '__main__':
    main()
