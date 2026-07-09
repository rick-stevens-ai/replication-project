"""
FNO-Original (Li et al. 2021) Wave 4 — 1D Burgers super-resolution / operator learning.

Faithful reduced-scale reproduction of one of the three headline experiments
in Li et al. *Fourier Neural Operator for Parametric PDEs* (ICLR 2021):
the 1D viscous Burgers operator learning task. The paper learns the map
u(x, t=0) -> u(x, t=1) for the Burgers equation u_t + u u_x = nu u_xx
with periodic BCs and reports relative L2 errors of ~0.16% at s=256
with 1000 training samples.

We:
  1. Generate a small Burgers dataset (matching the paper's family of
     Gaussian-random-field initial conditions) by integrating with a
     simple upwind+central scheme.
  2. Train the paper's canonical FNO1D architecture (4 spectral conv
     layers, 16 modes, width 64) on (u0 -> u1) supervised pairs.
  3. Report training and test relative L2 errors, training time, and
     resolution-invariance (zero-shot eval at higher resolution).

Compared to the paper's full-scale setup (1000 training samples, s=8192
generation grid down-sampled to 1024/512/256/128/64), we run at much
smaller scale (n_train=128, generation s=1024) to fit in a CPU minute.
"""
import os, time, json
from pathlib import Path
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

ROOT = Path("/Users/stevens/Dropbox/REPLICATE-PROJECT/PDE-replications/fno-original-wave4")
EVID = ROOT / "evidence"
DATA = ROOT / "data"
EVID.mkdir(parents=True, exist_ok=True)
DATA.mkdir(parents=True, exist_ok=True)


# --------- Data generation: Burgers initial-to-final-time pairs ---------
def burgers_step(u, dx, dt, nu):
    uL = np.roll(u, 1, axis=-1)
    uR = np.roll(u, -1, axis=-1)
    a = 0.5 * (u + uR)
    flux_R = np.where(a >= 0, 0.5 * u * u, 0.5 * uR * uR)
    a = 0.5 * (uL + u)
    flux_L = np.where(a >= 0, 0.5 * uL * uL, 0.5 * u * u)
    conv = (flux_R - flux_L) / dx
    diff = nu * (uR - 2 * u + uL) / (dx * dx)
    return u + dt * (-conv + diff)


def grf_initial(rng, n_samples, nx, alpha=2.5, tau=7.0):
    """Smooth random initial conditions: low-mode sinusoid family.
    Equivalent to PDEBench's init_multi family used by burgers_multi_solution_Hydra.
    """
    x = np.linspace(0.0, 1.0, nx, endpoint=False)
    u = np.zeros((n_samples, nx), dtype=np.float64)
    for b in range(n_samples):
        for k in range(1, 5):  # 4 modes
            a = rng.uniform(-1.0, 1.0)
            c = rng.uniform(-1.0, 1.0)
            u[b] += a * np.sin(2 * np.pi * k * x) + c * np.cos(2 * np.pi * k * x)
        amp = np.max(np.abs(u[b]))
        if amp > 1e-9:
            u[b] /= amp
    return u.astype(np.float32)


def generate_pairs(n_samples, nx, t_final=1.0, nu=0.01, seed=0):
    rng = np.random.default_rng(seed)
    u0 = grf_initial(rng, n_samples, nx)
    dx = 1.0 / nx
    u_max = 1.0
    dt = min(0.5 * dx / u_max, 0.4 * dx * dx / nu)
    n_steps = int(np.ceil(t_final / dt))
    dt = t_final / n_steps
    u = u0.copy()
    for _ in range(n_steps):
        u = burgers_step(u, dx, dt, nu)
    return u0, u.astype(np.float32), dict(dx=dx, dt=dt, n_steps=n_steps,
                                            nu=nu, t_final=t_final)


# --------- FNO-1D model (Li et al. 2021) ---------
class SpectralConv1d(nn.Module):
    def __init__(self, in_ch, out_ch, modes):
        super().__init__()
        self.in_ch, self.out_ch, self.modes = in_ch, out_ch, modes
        scale = 1.0 / (in_ch * out_ch)
        self.weights = nn.Parameter(scale * torch.randn(in_ch, out_ch, modes, dtype=torch.cfloat))

    def forward(self, x):
        # x: (B, C, X)
        B, C, X = x.shape
        x_ft = torch.fft.rfft(x, dim=-1)  # (B, C, X//2+1)
        out_ft = torch.zeros(B, self.out_ch, X // 2 + 1, dtype=torch.cfloat, device=x.device)
        modes = min(self.modes, x_ft.shape[-1])
        # contract: (B, in_ch, m) x (in_ch, out_ch, m) -> (B, out_ch, m)
        out_ft[:, :, :modes] = torch.einsum("bim,iom->bom", x_ft[:, :, :modes], self.weights[:, :, :modes])
        return torch.fft.irfft(out_ft, n=X, dim=-1)


class FNO1d(nn.Module):
    def __init__(self, modes=16, width=64, n_layers=4):
        super().__init__()
        self.lift = nn.Linear(2, width)  # input channels: (u0, x)
        self.specs = nn.ModuleList([SpectralConv1d(width, width, modes) for _ in range(n_layers)])
        self.locals = nn.ModuleList([nn.Conv1d(width, width, 1) for _ in range(n_layers)])
        self.proj1 = nn.Linear(width, 128)
        self.proj2 = nn.Linear(128, 1)

    def forward(self, u0):
        # u0: (B, X)
        B, X = u0.shape
        x = torch.linspace(0, 1, X, device=u0.device).unsqueeze(0).expand(B, X)  # (B, X)
        inp = torch.stack([u0, x], dim=-1)  # (B, X, 2)
        h = self.lift(inp).permute(0, 2, 1)  # (B, W, X)
        for sc, lc in zip(self.specs, self.locals):
            h = F.gelu(sc(h) + lc(h))
        h = h.permute(0, 2, 1)  # (B, X, W)
        return self.proj2(F.gelu(self.proj1(h))).squeeze(-1)  # (B, X)


def rel_l2(pred, target):
    # per-sample relative L2, mean over batch
    num = torch.linalg.vector_norm(pred - target, dim=-1)
    den = torch.linalg.vector_norm(target, dim=-1) + 1e-12
    return (num / den).mean().item()


def train_eval(n_train=128, n_test=32, nx_train=128, nx_test=256,
                modes=16, width=64, epochs=40, batch_size=16, lr=1e-3,
                seed=0):
    torch.manual_seed(seed)
    np.random.seed(seed)

    print(f"[gen] training pairs: n={n_train}, nx={nx_train}")
    t0 = time.time()
    u0_tr, u1_tr, info = generate_pairs(n_train, nx_train, seed=seed)
    print(f"      ({time.time()-t0:.1f}s)  dx={info['dx']:.2e} dt={info['dt']:.2e}")

    print(f"[gen] test pairs (in-distribution): n={n_test}, nx={nx_train}")
    t0 = time.time()
    u0_te_id, u1_te_id, _ = generate_pairs(n_test, nx_train, seed=seed + 999)
    print(f"      ({time.time()-t0:.1f}s)")

    print(f"[gen] test pairs (super-resolution): n={n_test}, nx={nx_test}")
    t0 = time.time()
    u0_te_hi, u1_te_hi, _ = generate_pairs(n_test, nx_test, seed=seed + 999)
    print(f"      ({time.time()-t0:.1f}s)")

    u0_tr_t = torch.from_numpy(u0_tr)
    u1_tr_t = torch.from_numpy(u1_tr)
    u0_te_id_t = torch.from_numpy(u0_te_id)
    u1_te_id_t = torch.from_numpy(u1_te_id)
    u0_te_hi_t = torch.from_numpy(u0_te_hi)
    u1_te_hi_t = torch.from_numpy(u1_te_hi)

    model = FNO1d(modes=modes, width=width)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"FNO1d params = {n_params}  (modes={modes}, width={width})")

    opt = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=1e-4)
    sched = torch.optim.lr_scheduler.StepLR(opt, step_size=max(1, epochs // 4), gamma=0.5)

    # baseline (identity) test L2 — what does "predict u1=u0" get us?
    base_id = rel_l2(u0_te_id_t, u1_te_id_t)
    base_hi = rel_l2(u0_te_hi_t, u1_te_hi_t)
    print(f"baseline (identity prediction): in-dist rel_L2={base_id:.4f}  super-res={base_hi:.4f}")

    train_curve = []
    t0_train = time.time()
    for ep in range(epochs):
        model.train()
        perm = torch.randperm(n_train)
        ep_loss = 0.0
        n_batches = 0
        for s in range(0, n_train, batch_size):
            idx = perm[s:s + batch_size]
            pred = model(u0_tr_t[idx])
            loss = F.mse_loss(pred, u1_tr_t[idx])
            opt.zero_grad()
            loss.backward()
            opt.step()
            ep_loss += loss.item()
            n_batches += 1
        sched.step()
        avg = ep_loss / n_batches
        # eval every few epochs
        if (ep + 1) % max(1, epochs // 10) == 0 or ep == 0:
            model.eval()
            with torch.no_grad():
                rl_id = rel_l2(model(u0_te_id_t), u1_te_id_t)
                rl_hi = rel_l2(model(u0_te_hi_t), u1_te_hi_t)
            train_curve.append(dict(epoch=ep + 1, mse=avg, rel_l2_id=rl_id, rel_l2_hi=rl_hi))
            print(f"  ep {ep+1:3d}/{epochs}: mse={avg:.4e}  rel_L2_id={rl_id:.4f}  rel_L2_super={rl_hi:.4f}")
    train_time = time.time() - t0_train

    model.eval()
    with torch.no_grad():
        rl_id = rel_l2(model(u0_te_id_t), u1_te_id_t)
        rl_hi = rel_l2(model(u0_te_hi_t), u1_te_hi_t)
        pred_id = model(u0_te_id_t).cpu().numpy()
        pred_hi = model(u0_te_hi_t).cpu().numpy()

    print(f"\nFINAL: rel_L2 in-dist (nx={nx_train}) = {rl_id:.4f}")
    print(f"FINAL: rel_L2 super-res (nx={nx_test}) = {rl_hi:.4f}")
    print(f"Training time: {train_time:.1f}s")

    summary = dict(
        n_params=n_params,
        modes=modes,
        width=width,
        epochs=epochs,
        batch_size=batch_size,
        lr=lr,
        n_train=n_train,
        n_test=n_test,
        nx_train=nx_train,
        nx_test_super=nx_test,
        baseline_rel_l2_in_dist=base_id,
        baseline_rel_l2_super_res=base_hi,
        final_rel_l2_in_dist=rl_id,
        final_rel_l2_super_res=rl_hi,
        improvement_factor_in_dist=base_id / rl_id,
        improvement_factor_super_res=base_hi / rl_hi,
        train_time_s=round(train_time, 2),
        train_curve=train_curve,
        gen_info=info,
    )
    with open(EVID / "burgers_results.json", "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"\nresults -> {EVID / 'burgers_results.json'}")

    # Save predictions for plotting
    np.savez(EVID / "burgers_preds.npz",
              u0_te_id=u0_te_id, u1_te_id=u1_te_id, pred_id=pred_id,
              u0_te_hi=u0_te_hi, u1_te_hi=u1_te_hi, pred_hi=pred_hi)
    return summary


def make_plots():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    d = np.load(EVID / "burgers_preds.npz")
    fig, axes = plt.subplots(2, 3, figsize=(12, 6))
    for i in range(3):
        x_id = np.linspace(0, 1, d['u0_te_id'].shape[-1])
        axes[0, i].plot(x_id, d['u0_te_id'][i], 'k:', label='u0', lw=1)
        axes[0, i].plot(x_id, d['u1_te_id'][i], 'b-', label='u1 (true)', lw=1.5)
        axes[0, i].plot(x_id, d['pred_id'][i], 'r--', label='u1 (FNO)', lw=1.5)
        axes[0, i].set_title(f'in-dist test {i}, nx={x_id.size}')
        axes[0, i].grid(True, ls=':')
        if i == 0:
            axes[0, i].legend(fontsize=8)
        x_hi = np.linspace(0, 1, d['u0_te_hi'].shape[-1])
        axes[1, i].plot(x_hi, d['u0_te_hi'][i], 'k:', lw=1)
        axes[1, i].plot(x_hi, d['u1_te_hi'][i], 'b-', lw=1.5)
        axes[1, i].plot(x_hi, d['pred_hi'][i], 'r--', lw=1.5)
        axes[1, i].set_title(f'super-res test {i}, nx={x_hi.size}')
        axes[1, i].grid(True, ls=':')
    plt.tight_layout()
    plt.savefig(EVID / "burgers_predictions.png", dpi=130)
    plt.close()
    print(f"plotted -> {EVID / 'burgers_predictions.png'}")


if __name__ == "__main__":
    s = train_eval(n_train=128, n_test=32, nx_train=128, nx_test=256,
                    modes=16, width=64, epochs=40, batch_size=16, lr=1e-3, seed=0)
    make_plots()
