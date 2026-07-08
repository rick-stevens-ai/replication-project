"""KS re-pass — closer to paper hyperparameters (Table 1 row 7 / MP-NODE 7).

Paper's best configuration in Table 1:
  - mu_min = 1e-4
  - Trajectory length (total) = 75 timesteps
  - Discontinuities K = 25
    => seg_len = floor(75 / 25) = 3 steps between discontinuities

  KL divergence of joint PDF(u_x, u_xx) vs ground truth (best in Table 1)
  is 0.029.

Differences from prior pass:
  - Prior pass used K=8 seg_len=16 (n_steps = 128 total) and 8 stages.
  - Re-pass uses K=25 seg_len=3 (n_steps = 75 total) per paper.
  - Adds KL divergence metric (paper's primary KS quantitative metric).

Other reproducible choices:
  - Reference trajectory: re-use cached KS trajectory from prior pass at
    replication/v2_faithful/data/ks_traj.npz (BDF solver, 8801 samples).
  - Pre-pass paper used ETDRK4 -> we use the same BDF trajectory the v2 pass
    used. The KS attractor statistics are independent of the solver as long
    as it's accurate; we cross-check the KL metric below.
  - Model: 3-layer MLP, 512 hidden (same as v2 pass).
  - Device: CPU/MPS (CherryRd, free compute). Auto-selects MPS if available.
  - Adam lr 5e-4 (theta) / 5e-3 (q), gradient clipping at 1.

Outputs (under results/repass/ks/):
  - history.json
  - metrics.json (forecast_horizon, NRMSE@1L, KL divergence)
  - rollout.npz
  - figures: hovmoller (truth vs pred), joint_pdf (truth vs pred), forecast_nrmse
"""
import argparse, json, os, sys, time
import numpy as np
import torch
import torch.nn as nn
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "replication", "v2_faithful", "src"))
from mp_node import MLPNODE, integrate_segments, mp_loss
from torchdiffeq import odeint


def make_batches(u, seg_len, K, n_traj, seed=1):
    rng = np.random.default_rng(seed)
    total_len = K * seg_len + 1
    available = u.shape[0] - total_len
    assert available > 0, f"need {total_len} consecutive snapshots, have {u.shape[0]}"
    starts = rng.integers(0, available, size=n_traj)
    batches = np.stack([u[s : s + total_len] for s in starts])  # [B, K*S+1, N]
    B, _, N = batches.shape
    y_per_seg = np.zeros((seg_len + 1, B, K, N), dtype=np.float32)
    ic_per_seg = np.zeros((B, K, N), dtype=np.float32)
    for k in range(K):
        seg = batches[:, k * seg_len : k * seg_len + seg_len + 1]
        y_per_seg[:, :, k, :] = seg.transpose(1, 0, 2)
        ic_per_seg[:, k, :] = seg[:, 0, :]
    return y_per_seg, ic_per_seg


def rollout(model, u0, n_steps, dt, device):
    """Rollout starting from u0 for n_steps with substep RK4."""
    y0 = torch.tensor(u0, dtype=torch.float32, device=device)
    t = torch.tensor(np.arange(n_steps + 1) * dt, dtype=torch.float32, device=device)
    with torch.no_grad():
        sol = odeint(model, y0, t, method='rk4')
    return sol.cpu().numpy()


def first_second_derivative(u, dx):
    """Compute u_x and u_xx along the spatial axis using periodic central diffs."""
    ux = (np.roll(u, -1, axis=-1) - np.roll(u, 1, axis=-1)) / (2 * dx)
    uxx = (np.roll(u, -1, axis=-1) - 2 * u + np.roll(u, 1, axis=-1)) / (dx ** 2)
    return ux, uxx


def joint_pdf_kl(u_truth, u_pred, dx, bins=64, eps=1e-12):
    """KL divergence between joint PDFs of (u_x, u_xx) for truth and pred.

    Returns D_KL(P_pred || P_truth) on the union range with `bins` per axis.
    """
    ux_t, uxx_t = first_second_derivative(u_truth, dx)
    ux_p, uxx_p = first_second_derivative(u_pred, dx)

    # Use truth ranges as canonical (so out-of-attractor pred mass shows up)
    rng_x = (np.percentile(ux_t, 0.5),  np.percentile(ux_t, 99.5))
    rng_y = (np.percentile(uxx_t, 0.5), np.percentile(uxx_t, 99.5))
    # Clamp pred values into the truth grid (so we count out-of-range as edge bins)
    ux_p_c  = np.clip(ux_p,  rng_x[0], rng_x[1] - 1e-9)
    uxx_p_c = np.clip(uxx_p, rng_y[0], rng_y[1] - 1e-9)

    H_t, xedges, yedges = np.histogram2d(ux_t.ravel(),  uxx_t.ravel(),
                                          bins=bins, range=[rng_x, rng_y])
    H_p, _, _           = np.histogram2d(ux_p_c.ravel(), uxx_p_c.ravel(),
                                          bins=[xedges, yedges])

    P = H_p / max(H_p.sum(), 1)
    Q = H_t / max(H_t.sum(), 1)
    # Smooth zeros
    P = P + eps; P /= P.sum()
    Q = Q + eps; Q /= Q.sum()
    KL_PQ = np.sum(P * np.log(P / Q))
    return float(KL_PQ), float(P.sum()), float(Q.sum())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--data', default=os.path.join(REPO_ROOT, 'replication', 'v2_faithful', 'data', 'ks_traj.npz'))
    ap.add_argument('--out',  default=os.path.join(REPO_ROOT, 'results', 'repass', 'ks'))
    ap.add_argument('--N', type=int, default=128)
    ap.add_argument('--L', type=float, default=22.0)
    ap.add_argument('--dt', type=float, default=0.25)
    ap.add_argument('--K', type=int, default=25, help='paper Table-1 row 7')
    ap.add_argument('--seg-len', type=int, default=3, help='75 total steps / K=25 = 3 per seg')
    ap.add_argument('--n-traj', type=int, default=128)
    ap.add_argument('--epochs-per-mu', type=int, default=120)
    ap.add_argument('--lr', type=float, default=5e-4)
    ap.add_argument('--lr-q', type=float, default=5e-3)
    ap.add_argument('--hidden', type=int, default=512)
    ap.add_argument('--depth', type=int, default=3)
    ap.add_argument('--rollout-steps', type=int, default=400, help='~100 tu rollout')
    ap.add_argument('--device', default='auto')
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)

    # Device selection
    if args.device == 'auto':
        if torch.cuda.is_available():
            device = torch.device('cuda')
        elif getattr(torch.backends, 'mps', None) and torch.backends.mps.is_available():
            device = torch.device('mps')
        else:
            device = torch.device('cpu')
    else:
        device = torch.device(args.device)
    print(f"[KS-repass] device={device}", flush=True)

    # --- 1. Load reference trajectory (cached from v2 pass) ---
    d = np.load(args.data)
    t_ref, u_ref = d['t'], d['u']
    print(f"[KS-repass] ref traj shape {u_ref.shape}, dt={t_ref[1]-t_ref[0]:.3f}", flush=True)

    split = int(0.8 * u_ref.shape[0])
    u_train = u_ref[:split]
    u_test  = u_ref[split:]
    u_mean = float(u_train.mean()); u_std = float(u_train.std())
    u_train_n = ((u_train - u_mean) / u_std).astype(np.float32)
    u_test_n  = ((u_test  - u_mean) / u_std).astype(np.float32)
    print(f"[KS-repass] u_mean={u_mean:.4f} u_std={u_std:.4f}", flush=True)

    # --- 2. Batches per paper config (K=25, S=3) ---
    y_per_seg_np, ic_per_seg_np = make_batches(u_train_n, args.seg_len, args.K, args.n_traj)
    y_true = torch.tensor(y_per_seg_np, dtype=torch.float32, device=device)
    ic_init = torch.tensor(ic_per_seg_np, dtype=torch.float32, device=device)
    print(f"[KS-repass] batches y={tuple(y_true.shape)} ic={tuple(ic_init.shape)}", flush=True)

    # --- 3. Model & optimizers ---
    model = MLPNODE(dim=args.N, hidden=args.hidden, depth=args.depth).to(device)
    q_param = nn.Parameter(ic_init.clone())
    ic_pin = ic_init[:, 0:1, :].clone()

    opt_theta = torch.optim.Adam(model.parameters(), lr=args.lr)
    opt_q     = torch.optim.Adam([q_param], lr=args.lr_q)
    t_seg = torch.linspace(0, args.seg_len * args.dt, args.seg_len + 1, device=device)

    # Paper Table 1 row 7 (best): mu_min=1e-4. Schedule per the paper: ×10 per stage.
    mu_schedule = [1e-4, 1e-3, 1e-2, 1e-1, 1.0, 10.0]

    history = []
    start = time.time()
    best_data_loss = float('inf')
    best_state = None
    for stage, mu in enumerate(mu_schedule):
        for epoch in range(args.epochs_per_mu):
            with torch.no_grad():
                q_param[:, 0:1, :] = ic_pin
            traj_pred, _ = integrate_segments(model, q_param, t_seg, method='rk4')
            loss, d_loss, p_loss = mp_loss(traj_pred, y_true, q_param, mu)
            opt_theta.zero_grad(); opt_q.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt_theta.step(); opt_q.step()
            if float(d_loss) < best_data_loss:
                best_data_loss = float(d_loss)
                best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
            if epoch % 20 == 0 or epoch == args.epochs_per_mu - 1:
                rec = dict(stage=stage, mu=mu, epoch=epoch,
                           loss=float(loss), data=float(d_loss), pen=float(p_loss),
                           elapsed=time.time() - start)
                history.append(rec)
                print(f"[KS-repass] stage={stage} mu={mu:.1e} epoch={epoch:3d} "
                      f"total={loss.item():.4e} data={d_loss.item():.4e} "
                      f"pen={p_loss.item():.4e} elapsed={rec['elapsed']:.1f}s", flush=True)
    wall = time.time() - start
    print(f"[KS-repass] training done in {wall:.1f}s, best_data_loss={best_data_loss:.4e}", flush=True)

    # Reload best
    model.load_state_dict(best_state)
    model.eval()

    # --- 4. Rollout from test IC ---
    u0_n = u_test_n[0]
    pred_n = rollout(model, u0_n, args.rollout_steps, args.dt, device)  # [n+1, N]
    truth_n = u_test_n[: args.rollout_steps + 1]

    # Un-normalize for KL on real units
    pred = pred_n * u_std + u_mean
    truth = truth_n * u_std + u_mean

    # --- 5. Metrics ---
    # Forecast horizon (normalized RMSE < 0.5)
    err = pred_n - truth_n
    nrmse = np.sqrt(np.mean(err ** 2, axis=1)) / np.sqrt(np.mean(truth_n ** 2))
    tau_L = 22.0  # Lyapunov time per paper Section 4.2
    t = np.arange(args.rollout_steps + 1) * args.dt
    horizon_idx = int(np.argmax(nrmse > 0.5)) if np.any(nrmse > 0.5) else len(nrmse)
    horizon_t = t[horizon_idx]
    horizon_L = horizon_t / tau_L
    idx_1L = int(round(tau_L / args.dt))
    nrmse_at_1L = float(nrmse[idx_1L]) if idx_1L < len(nrmse) else float('nan')
    nrmse_at_2L = float(nrmse[2 * idx_1L]) if 2 * idx_1L < len(nrmse) else float('nan')

    # KL divergence of joint PDF u_x, u_xx (paper's KS quantitative metric)
    dx = args.L / args.N
    # Use the model rollout after dropping initial transient
    burn = idx_1L  # drop first tau_L
    if pred.shape[0] > burn + 50:
        kl_div, _, _ = joint_pdf_kl(truth[burn:], pred[burn:], dx)
    else:
        kl_div = float('nan')

    # Stability: std of long rollout vs truth
    u_std_truth = float(np.std(truth_n))
    u_std_pred  = float(np.std(pred_n))

    metrics = dict(
        forecast_horizon_t=float(horizon_t),
        forecast_horizon_lyap=float(horizon_L),
        nrmse_at_1_tau_L=nrmse_at_1L,
        nrmse_at_2_tau_L=nrmse_at_2L,
        kl_divergence_pdf_ux_uxx=float(kl_div),
        u_std_truth=u_std_truth,
        u_std_pred=u_std_pred,
        wall_time_s=float(wall),
        best_data_loss=float(best_data_loss),
        rollout_steps=args.rollout_steps,
        rollout_t_max=float(t[-1]),
        rollout_t_max_lyap=float(t[-1] / tau_L),
        paper_table1_best_kl=0.02915,
        paper_table1_row_used=7,
        hparams=dict(K=args.K, seg_len=args.seg_len, n_traj=args.n_traj,
                     epochs_per_mu=args.epochs_per_mu, lr=args.lr, lr_q=args.lr_q,
                     hidden=args.hidden, depth=args.depth, dt=args.dt, N=args.N, L=args.L,
                     mu_schedule=mu_schedule),
    )
    with open(os.path.join(args.out, "metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)
    with open(os.path.join(args.out, "history.json"), "w") as f:
        json.dump(history, f, indent=2)
    np.savez_compressed(os.path.join(args.out, "rollout.npz"),
                        t=t, pred=pred, truth=truth, nrmse=nrmse,
                        pred_norm=pred_n, truth_norm=truth_n)
    torch.save(best_state, os.path.join(args.out, "best.pt"))

    # --- 6. Figures ---
    # Hovmoller (truth vs pred)
    fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    x_grid = np.arange(args.N) * (args.L / args.N)
    extent = [t[0], t[-1], x_grid[0], x_grid[-1]]
    vmax = float(np.max(np.abs(truth)))
    axes[0].imshow(truth.T, aspect='auto', origin='lower', extent=extent, cmap='RdBu_r', vmin=-vmax, vmax=vmax)
    axes[0].set_title("KS truth (test trajectory)")
    axes[0].set_ylabel("x")
    im = axes[1].imshow(pred.T, aspect='auto', origin='lower', extent=extent, cmap='RdBu_r', vmin=-vmax, vmax=vmax)
    axes[1].set_title(f"MP-NODE prediction (re-pass: K={args.K}, S={args.seg_len}, mu_min={mu_schedule[0]:.0e})")
    axes[1].set_ylabel("x"); axes[1].set_xlabel("t")
    fig.colorbar(im, ax=axes.ravel().tolist(), shrink=0.7)
    fig.savefig(os.path.join(args.out, "hovmoller.png"), dpi=130, bbox_inches='tight')
    plt.close(fig)

    # Forecast NRMSE
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(t / tau_L, nrmse, lw=1.5)
    ax.axhline(0.5, color='k', ls='--', alpha=0.5)
    ax.axvline(horizon_L, color='C3', ls=':', alpha=0.7, label=f"NRMSE>0.5 at {horizon_L:.2f} tau_L")
    ax.set_xlabel("time / Lyapunov time tau_L")
    ax.set_ylabel("normalized RMSE")
    ax.set_title(f"KS forecast skill (re-pass)  NRMSE@1tau_L = {nrmse_at_1L:.3f}")
    ax.set_yscale('log'); ax.set_ylim(1e-3, 10)
    ax.grid(True, alpha=0.3); ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(args.out, "forecast_nrmse.png"), dpi=130)
    plt.close(fig)

    # Joint PDF (truth vs pred)
    ux_t, uxx_t = first_second_derivative(truth[burn:], dx)
    ux_p, uxx_p = first_second_derivative(pred[burn:], dx)
    rng_x = (np.percentile(ux_t, 0.5), np.percentile(ux_t, 99.5))
    rng_y = (np.percentile(uxx_t, 0.5), np.percentile(uxx_t, 99.5))
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5), sharey=True)
    axes[0].hist2d(ux_t.ravel(), uxx_t.ravel(), bins=80, range=[rng_x, rng_y], cmap='magma')
    axes[0].set_title("Ground truth: P(u_x, u_xx)")
    axes[0].set_xlabel("u_x"); axes[0].set_ylabel("u_xx")
    axes[1].hist2d(ux_p.ravel(), uxx_p.ravel(), bins=80, range=[rng_x, rng_y], cmap='magma')
    axes[1].set_title(f"MP-NODE pred: P(u_x, u_xx)   KL = {kl_div:.4f}\n(paper Table 1 best = 0.029)")
    axes[1].set_xlabel("u_x")
    fig.tight_layout()
    fig.savefig(os.path.join(args.out, "joint_pdf.png"), dpi=130)
    plt.close(fig)

    print("\n=== KS re-pass metrics ===")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
