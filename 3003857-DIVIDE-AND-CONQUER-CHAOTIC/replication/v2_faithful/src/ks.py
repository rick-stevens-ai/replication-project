"""Kuramoto-Sivashinsky experiment (paper Section 4.2).

Reference solver: ETDRK4 (Kassam & Trefethen 2005).
  q_t = -q*q_x - q_xx - q_xxxx  on [0, L]  periodic
  L = 22 (chaotic inertial-manifold regime, Lyapunov time tau_L ~ 22)

Training: MP-NODE with K segments, penalty mu annealed 1e-5 -> 1e0.
"""
import argparse, json, os, time
import numpy as np
import torch
import torch.nn as nn
from torchdiffeq import odeint

import sys
sys.path.insert(0, os.path.dirname(__file__))
from mp_node import MLPNODE, integrate_segments, mp_loss
from ks_solver import ks_reference


def _unused_ks_etdrk4(N=128, L=22.0, dt_sample=0.25, T=2000.0, ic_seed=0, verbose=True,
              dt_internal=0.01):
    """Return (t, u) where u has shape [T/dt_sample+1, N].

    Uses internal step dt_internal for stability; samples every dt_sample.
    """
    sub = max(1, int(round(dt_sample / dt_internal)))
    dt = dt_internal
    rng = np.random.default_rng(ic_seed)
    x = L * np.arange(N) / N
    u = 0.1 * np.cos(2 * np.pi * x / L) + 0.01 * rng.standard_normal(N)
    u_hat = np.fft.fft(u)

    k = 2 * np.pi * np.fft.fftfreq(N, d=L / N)
    L_op = k**2 - k**4  # linear operator in Fourier space
    # 2/3 dealiasing
    k_max = N // 3
    k_idx = np.abs(k) / (2 * np.pi / L)
    dealias = (k_idx < k_max).astype(float)
    g = -0.5j * k  # for nonlinear -0.5 d/dx(u^2) in Fourier

    def N_hat(uh):
        # nonlinear term in Fourier (pseudospectral with dealiasing)
        u_real = np.real(np.fft.ifft(uh))
        return dealias * g * np.fft.fft(u_real * u_real)

    # Integrating-factor RK4: v_hat = exp(-L*t) u_hat, so dv/dt = exp(-L*t) * N(exp(L*t) v)
    def step_IFRK4(uh, dt):
        # Use integrating factor to absorb stiff linear part.
        E1 = np.exp(L_op * dt / 2)
        E2_ = np.exp(L_op * dt)
        k1 = N_hat(uh)
        k2 = N_hat(E1 * (uh + 0.5 * dt * k1))
        k3 = N_hat(E1 * uh + 0.5 * dt * k2)
        k4 = N_hat(E2_ * uh + dt * E1 * k3)
        return E2_ * uh + (dt / 6.0) * (E2_ * k1 + 2 * E1 * k2 + 2 * E1 * k3 + k4)

    # Burn-in
    burn = int(200.0 / dt)
    for _ in range(burn):
        u_hat = step_IFRK4(u_hat, dt)

    Nsteps_total = int(round(T / dt))
    n_samples = Nsteps_total // sub + 1
    out = np.zeros((n_samples, N), dtype=np.float64)
    out[0] = np.real(np.fft.ifft(u_hat))

    t0 = time.time()
    sidx = 1
    for i in range(Nsteps_total):
        u_hat = step_IFRK4(u_hat, dt)
        if (i + 1) % sub == 0 and sidx < n_samples:
            out[sidx] = np.real(np.fft.ifft(u_hat))
            if verbose and sidx % max(1, n_samples // 10) == 0:
                print(f"  KS sample {sidx}/{n_samples}  t={sidx*dt_sample:.1f}  "
                      f"|u|_max={np.max(np.abs(out[sidx])):.2f}  "
                      f"elapsed={time.time()-t0:.1f}s", flush=True)
            sidx += 1
    t_arr = np.arange(n_samples) * dt_sample
    return t_arr, out[:sidx]


def make_batches(u, seg_len=16, K=4, n_traj=64, stride=4, seed=1):
    """Build training examples: each of shape [K*seg_len+1, N] from the long traj.
    We return:
        y_per_seg : [S+1, B, K, N]   # ground truth per segment
        ic_per_seg : [B, K, N]       # initial condition per segment
    seg_len = S (number of steps per segment)
    K segments -> total length K*seg_len+1 snapshots
    """
    rng = np.random.default_rng(seed)
    total_len = K * seg_len + 1
    available = u.shape[0] - total_len
    assert available > 0
    starts = rng.integers(0, available, size=n_traj)
    batches = np.stack([u[s : s + total_len] for s in starts])  # [B, K*S+1, N]
    B = batches.shape[0]
    N = batches.shape[-1]

    # Build per-segment arrays
    y_per_seg = np.zeros((seg_len + 1, B, K, N))
    ic_per_seg = np.zeros((B, K, N))
    for k in range(K):
        seg = batches[:, k * seg_len : k * seg_len + seg_len + 1]  # [B, S+1, N]
        y_per_seg[:, :, k, :] = seg.transpose(1, 0, 2)
        ic_per_seg[:, k, :] = seg[:, 0, :]
    return y_per_seg, ic_per_seg


def rollout(model, u0, t_eval, device, method='rk4', sub=4):
    """Rollout with finer internal substeps for stability."""
    y0 = torch.tensor(u0, dtype=torch.float32, device=device)
    # Subdivide t_eval for internal stepping
    t_eval = np.asarray(t_eval)
    t_fine = [t_eval[0]]
    for i in range(1, len(t_eval)):
        for s in range(1, sub + 1):
            t_fine.append(t_eval[i - 1] + s * (t_eval[i] - t_eval[i - 1]) / sub)
    t_fine = np.array(t_fine)
    t = torch.tensor(t_fine, dtype=torch.float32, device=device)
    with torch.no_grad():
        sol = odeint(model, y0, t, method=method)
    sol = sol.cpu().numpy()
    # Subsample back to requested times
    step = sub
    out = sol[::step]
    return out[:len(t_eval)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='results/ks')
    ap.add_argument('--data', default='data/ks_traj.npz')
    ap.add_argument('--N', type=int, default=128)
    ap.add_argument('--L', type=float, default=22.0)
    ap.add_argument('--dt', type=float, default=0.25)
    ap.add_argument('--T', type=float, default=2200.0)  # ~100 Lyapunov times
    ap.add_argument('--K', type=int, default=4, help='number of segments per sequence')
    ap.add_argument('--seg-len', type=int, default=16, help='steps per segment')
    ap.add_argument('--n-traj', type=int, default=64)
    ap.add_argument('--epochs', type=int, default=400)
    ap.add_argument('--epochs-per-mu', type=int, default=40)
    ap.add_argument('--lr', type=float, default=1e-3)
    ap.add_argument('--lr-q', type=float, default=1e-2)
    ap.add_argument('--device', default='cuda')
    ap.add_argument('--hidden', type=int, default=256)
    ap.add_argument('--depth', type=int, default=3)
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    os.makedirs(os.path.dirname(args.data) or '.', exist_ok=True)
    device = torch.device(args.device if torch.cuda.is_available() else 'cpu')
    print(f"[KS] device={device}")

    # --- 1. Reference trajectory ---
    if os.path.exists(args.data):
        d = np.load(args.data)
        t_ref, u_ref = d['t'], d['u']
        print(f"[KS] loaded cached ref traj {u_ref.shape}")
    else:
        print(f"[KS] generating ETDRK4 reference: N={args.N} L={args.L} T={args.T}")
        t_ref, u_ref = ks_reference(N=args.N, L=args.L, dt_sample=args.dt, T=args.T, ic_seed=0)
        np.savez_compressed(args.data, t=t_ref, u=u_ref)
        print(f"[KS] saved ref traj {u_ref.shape}")

    # Split train/test chronologically: first 80% train, last 20% test
    split = int(0.8 * u_ref.shape[0])
    u_train = u_ref[:split]
    u_test = u_ref[split:]

    # --- Normalize data so state is O(1) ---
    u_mean = float(u_train.mean())
    u_std = float(u_train.std())
    u_train_n = (u_train - u_mean) / u_std
    u_test_n = (u_test - u_mean) / u_std

    # --- 2. Build minibatches of segmented trajectories ---
    y_per_seg_np, ic_per_seg_np = make_batches(u_train_n, seg_len=args.seg_len,
                                               K=args.K, n_traj=args.n_traj)
    y_true = torch.tensor(y_per_seg_np, dtype=torch.float32, device=device)
    ic_init = torch.tensor(ic_per_seg_np, dtype=torch.float32, device=device)
    print(f"[KS] batches: y={tuple(y_true.shape)}  ic={tuple(ic_init.shape)}")

    # --- 3. Models & optimizers ---
    model = MLPNODE(dim=args.N, hidden=args.hidden, depth=args.depth).to(device)
    q_param = nn.Parameter(ic_init.clone())  # [B, K, N]
    # freeze first-segment IC to data (clamp after step)
    ic_pin = ic_init[:, 0:1, :].clone()

    opt_theta = torch.optim.Adam(model.parameters(), lr=args.lr)
    opt_q = torch.optim.Adam([q_param], lr=args.lr_q)
    t_seg = torch.linspace(0, args.seg_len * args.dt, args.seg_len + 1, device=device)

    # Penalty schedule: start tiny to let model warm up, then crank
    mu_schedule = [1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1.0, 10.0, 100.0]
    epochs_per_mu = args.epochs_per_mu

    history = []
    start = time.time()
    best_loss = float('inf')
    for stage, mu in enumerate(mu_schedule):
        for epoch in range(epochs_per_mu):
            # pin first-segment IC
            with torch.no_grad():
                q_param[:, 0:1, :] = ic_pin

            traj_pred, _ = integrate_segments(model, q_param, t_seg, method='rk4')
            loss, d_loss, p_loss = mp_loss(traj_pred, y_true, q_param, mu)

            opt_theta.zero_grad()
            opt_q.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt_theta.step()
            opt_q.step()

            if epoch % 5 == 0 or epoch == epochs_per_mu - 1:
                print(f"[KS] stage={stage} mu={mu:.1e} epoch={epoch:3d} "
                      f"total={loss.item():.4e} data={d_loss.item():.4e} "
                      f"pen={p_loss.item():.4e} elapsed={time.time()-start:.1f}s",
                      flush=True)
            history.append(dict(stage=stage, mu=mu, epoch=epoch,
                                total=float(loss), data=float(d_loss),
                                pen=float(p_loss)))
            # Track best by DATA loss (not penalty-dominated total)
            if d_loss.item() < best_loss:
                best_loss = d_loss.item()
                torch.save(model.state_dict(), os.path.join(args.out, 'best.pt'))

    torch.save(model.state_dict(), os.path.join(args.out, 'final.pt'))
    with open(os.path.join(args.out, 'history.json'), 'w') as f:
        json.dump(history, f)

    # --- 4. Evaluation: rollout from test IC (in normalized space, then unnormalize) ---
    print("[KS] Evaluating rollout...")
    model.load_state_dict(torch.load(os.path.join(args.out, 'best.pt')))
    u0 = u_test_n[0]
    tau_L = 22.0
    T_eval = 3 * tau_L  # 3 Lyapunov times for short-term, then longer for stats
    n_short = int(T_eval / args.dt) + 1
    t_short = np.arange(n_short) * args.dt
    n_short = min(n_short, u_test.shape[0])
    t_short = np.arange(n_short) * args.dt
    pred_short_n = rollout(model, u0, t_short, device)
    pred_short = pred_short_n * u_std + u_mean
    truth_short = u_test[:n_short]

    rmse_t = np.sqrt(((pred_short - truth_short) ** 2).mean(axis=1))
    u_std = u_train.std()
    normalized = rmse_t / u_std
    # forecast skill horizon: time until NRMSE exceeds 0.5
    horizon_idx = np.argmax(normalized > 0.5) if (normalized > 0.5).any() else len(normalized) - 1
    horizon_t = horizon_idx * args.dt
    horizon_lyap = horizon_t / tau_L
    print(f"[KS] Forecast horizon (NRMSE<0.5): t={horizon_t:.1f} (={horizon_lyap:.2f} Lyapunov times)")

    # Long rollout for attractor stats
    T_long = 750.0  # paper uses t<=750
    n_long = min(int(T_long / args.dt) + 1, u_test.shape[0])
    t_long = np.arange(n_long) * args.dt
    pred_long_n = rollout(model, u0, t_long, device)
    pred_long = pred_long_n * u_std + u_mean
    truth_long = u_test[: min(n_long, len(u_test))]

    # Invariant statistics: histograms of u and of u_x
    dx = args.L / args.N
    ux_truth = np.gradient(truth_long, dx, axis=1)
    ux_pred = np.gradient(pred_long[: len(truth_long)], dx, axis=1)

    metrics = dict(
        forecast_horizon_lyap=float(horizon_lyap),
        forecast_horizon_t=float(horizon_t),
        rmse_normalized_at_1L=float(normalized[min(int(tau_L / args.dt), len(normalized)-1)]),
        rmse_normalized_at_2L=float(normalized[min(int(2*tau_L/args.dt), len(normalized)-1)]),
        u_std_truth=float(truth_long.std()),
        u_std_pred=float(pred_long.std()),
        u_mean_truth=float(truth_long.mean()),
        u_mean_pred=float(pred_long.mean()),
        ux_std_truth=float(ux_truth.std()),
        ux_std_pred=float(ux_pred.std()),
        best_train_loss=float(best_loss),
        wall_time_s=float(time.time() - start),
        hparams=vars(args),
    )
    with open(os.path.join(args.out, 'metrics.json'), 'w') as f:
        json.dump(metrics, f, indent=2)
    np.savez_compressed(os.path.join(args.out, 'rollout.npz'),
                        pred_short=pred_short, truth_short=truth_short,
                        pred_long=pred_long, truth_long=truth_long,
                        t_short=t_short, t_long=t_long, rmse_t=rmse_t)
    print("[KS] DONE.", json.dumps(metrics, indent=2))


if __name__ == '__main__':
    main()
