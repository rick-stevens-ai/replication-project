"""
MP-NODE for Kuramoto-Sivashinsky (KS) Equation
Reproduces Section 4.2 of the paper.

KS equation: dq/dt = -q*dq/dx - d²q/dx² - d⁴q/dx⁴
Domain: L=22 (supports chaotic dynamics)
Lyapunov time: ~22 time units

Key results to reproduce:
- Short-term trajectory prediction (Figure 4)
- Joint PDF of first and second derivatives (Figure 5)
- Return period comparison (Figure 6)
"""

import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.fft import fft, ifft, fftfreq
import json
import os
import time

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

# ============================================================
# KS Equation Solver (Spectral Method)
# ============================================================
class KSSolver:
    """Pseudo-spectral solver for Kuramoto-Sivashinsky equation."""
    
    def __init__(self, L=22.0, N=64, dt=0.25):
        self.L = L
        self.N = N
        self.dt = dt
        self.dx = L / N
        self.x = np.linspace(0, L, N, endpoint=False)
        
        # Wavenumbers
        self.k = 2 * np.pi * fftfreq(N, d=L/N)
        
        # Linear operator: -k^2 - k^4
        self.L_op = -self.k**2 - self.k**4
    
    def rhs_spectral(self, q_hat):
        """Compute RHS in spectral space."""
        q = np.real(ifft(q_hat))
        q_x = np.real(ifft(1j * self.k * q_hat))
        nonlinear = -0.5 * fft(q**2)  # = fft(-q * q_x) via conservation form
        # Actually: -q*q_x = -0.5 * d(q^2)/dx
        nonlinear = -0.5 * 1j * self.k * fft(q**2)
        return self.L_op * q_hat + nonlinear
    
    def integrate(self, q0, T, save_every=1):
        """Integrate KS equation using ETDRK4 (exponential time differencing)."""
        N_steps = int(T / self.dt)
        q_hat = fft(q0)
        
        # ETDRK4 coefficients
        E = np.exp(self.L_op * self.dt)
        E2 = np.exp(self.L_op * self.dt / 2)
        
        # Compute ETDRK4 coefficients using contour integral for stability
        M = 32
        r = np.exp(1j * np.pi * (np.arange(1, M+1) - 0.5) / M)
        
        LR = self.dt * self.L_op[:, None] + r[None, :]
        
        Q = self.dt * np.real(np.mean((np.exp(LR/2) - 1) / LR, axis=1))
        f1 = self.dt * np.real(np.mean((-4 - LR + np.exp(LR) * (4 - 3*LR + LR**2)) / LR**3, axis=1))
        f2 = self.dt * np.real(np.mean((2 + LR + np.exp(LR) * (-2 + LR)) / LR**3, axis=1))
        f3 = self.dt * np.real(np.mean((-4 - 3*LR - LR**2 + np.exp(LR) * (4 - LR)) / LR**3, axis=1))
        
        trajectory = [np.real(ifft(q_hat)).copy()]
        
        for step in range(N_steps):
            Nv = self.rhs_spectral(q_hat) - self.L_op * q_hat  # Nonlinear part only
            a = E2 * q_hat + Q * Nv
            Na = self.rhs_spectral(a) - self.L_op * a
            b = E2 * q_hat + Q * Na
            Nb = self.rhs_spectral(b) - self.L_op * b
            c = E2 * a + Q * (2*Nb - Nv)
            Nc = self.rhs_spectral(c) - self.L_op * c
            
            q_hat = E * q_hat + Nv * f1 + 2*(Na + Nb) * f2 + Nc * f3
            
            if (step + 1) % save_every == 0:
                trajectory.append(np.real(ifft(q_hat)).copy())
        
        return np.array(trajectory)


# ============================================================
# Neural ODE for KS
# ============================================================
class KSNeuralODE(nn.Module):
    """1D CNN-based Neural ODE for KS dynamics."""
    
    def __init__(self, n_spatial=64, hidden_channels=32, n_layers=4):
        super().__init__()
        
        layers = []
        # Input: (batch, 1, n_spatial)
        layers.append(nn.Conv1d(1, hidden_channels, kernel_size=5, padding=2, padding_mode='circular'))
        layers.append(nn.GELU())
        
        for _ in range(n_layers - 2):
            layers.append(nn.Conv1d(hidden_channels, hidden_channels, kernel_size=5, padding=2, padding_mode='circular'))
            layers.append(nn.GELU())
        
        layers.append(nn.Conv1d(hidden_channels, 1, kernel_size=5, padding=2, padding_mode='circular'))
        
        self.net = nn.Sequential(*layers)
        
        # Initialize small
        for m in self.net:
            if isinstance(m, nn.Conv1d):
                nn.init.xavier_normal_(m.weight, gain=0.1)
                if m.bias is not None:
                    nn.init.zeros_(m.bias)
    
    def forward(self, t, q):
        """q shape: (batch, n_spatial) or (n_spatial,)"""
        if q.dim() == 1:
            q = q.unsqueeze(0).unsqueeze(0)  # (1, 1, N)
        elif q.dim() == 2:
            q = q.unsqueeze(1)  # (batch, 1, N)
        
        out = self.net(q)
        
        if out.shape[0] == 1 and out.dim() == 3:
            return out.squeeze(0).squeeze(0)
        return out.squeeze(1)


def rk4_step_ks(func, t, q, dt):
    """Single RK4 step."""
    k1 = func(t, q)
    k2 = func(t + 0.5*dt, q + 0.5*dt*k1)
    k3 = func(t + 0.5*dt, q + 0.5*dt*k2)
    k4 = func(t + dt, q + dt*k3)
    return q + (dt/6.0) * (k1 + 2*k2 + 2*k3 + k4)


def rk4_integrate_ks(func, q0, n_steps, dt):
    """Integrate KS Neural ODE."""
    trajectory = [q0]
    q = q0
    t = 0.0
    for _ in range(n_steps):
        q = rk4_step_ks(func, t, q, dt)
        t += dt
        trajectory.append(q)
    return torch.stack(trajectory, dim=0)


# ============================================================
# Training
# ============================================================
def train_vanilla_ks(model, train_data, dt, n_epochs=3000, lr=1e-3,
                     rollout_steps=10, batch_size=16, verbose=True):
    """Train vanilla NODE on KS data."""
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=n_epochs, eta_min=1e-5)
    
    n_data = len(train_data) - rollout_steps
    train_tensor = torch.tensor(train_data, dtype=torch.float32, device=device)
    
    losses = []
    
    for epoch in range(n_epochs):
        idx = np.random.randint(0, n_data, size=batch_size)
        
        batch_loss = 0.0
        for i in idx:
            q0 = train_tensor[i]
            target = train_tensor[i:i+rollout_steps+1]
            
            pred = rk4_integrate_ks(model, q0, rollout_steps, dt)
            loss = torch.mean((pred - target)**2)
            batch_loss = batch_loss + loss
        
        batch_loss = batch_loss / batch_size
        
        optimizer.zero_grad()
        batch_loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        scheduler.step()
        
        losses.append(batch_loss.item())
        
        if verbose and (epoch+1) % 500 == 0:
            print(f"  Vanilla KS epoch {epoch+1}/{n_epochs}: loss={batch_loss.item():.6f}")
    
    return losses


def train_mp_ks(model, train_data, dt, n_epochs=3000, lr=1e-3,
                rollout_steps=60, n_windows=5, batch_size=16,
                mu_schedule=None, verbose=True):
    """Train MP-NODE on KS data (Algorithm 1)."""
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=n_epochs, eta_min=1e-5)
    
    if mu_schedule is None:
        mu_schedule = {0: 1e-4, 750: 1e-2, 1500: 1e0, 2250: 1e2}
    
    n_data = len(train_data) - rollout_steps
    train_tensor = torch.tensor(train_data, dtype=torch.float32, device=device)
    steps_per_window = rollout_steps // n_windows
    
    losses = []
    lgt_list = []
    lp_list = []
    mu_current = list(mu_schedule.values())[0]
    
    for epoch in range(n_epochs):
        if epoch in mu_schedule:
            mu_current = mu_schedule[epoch]
            if verbose:
                print(f"  Updated mu to {mu_current:.1e} at epoch {epoch}")
        
        idx = np.random.randint(0, n_data, size=batch_size)
        
        total_lgt = 0.0
        total_lp = 0.0
        
        for i in idx:
            target = train_tensor[i:i+rollout_steps+1]
            
            # Initialize q_plus from ground truth
            q_plus = []
            for k in range(1, n_windows):
                step_idx = k * steps_per_window
                qk = target[step_idx].clone().detach().requires_grad_(True)
                q_plus.append(qk)
            
            pred_all = []
            penalty = torch.tensor(0.0, device=device)
            
            for w in range(n_windows):
                if w == 0:
                    q_start = target[0]
                else:
                    q_start = q_plus[w - 1]
                
                pred_w = rk4_integrate_ks(model, q_start, steps_per_window, dt)
                pred_all.append(pred_w)
                
                if w < n_windows - 1:
                    q_end = pred_w[-1]
                    q_next = q_plus[w]
                    penalty = penalty + torch.mean((q_next - q_end)**2)
            
            pred_full = torch.cat([pw[:-1] for pw in pred_all[:-1]] + [pred_all[-1]], dim=0)
            min_len = min(pred_full.shape[0], target.shape[0])
            lgt = torch.mean((pred_full[:min_len] - target[:min_len])**2)
            lp = penalty / max(n_windows - 1, 1)
            
            total_lgt = total_lgt + lgt
            total_lp = total_lp + lp
        
        total_lgt = total_lgt / batch_size
        total_lp = total_lp / batch_size
        total_loss = total_lgt + (mu_current / 2.0) * total_lp
        
        optimizer.zero_grad()
        total_loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        scheduler.step()
        
        losses.append(total_loss.item())
        lgt_list.append(total_lgt.item())
        lp_list.append(total_lp.item())
        
        if verbose and (epoch+1) % 500 == 0:
            print(f"  MP-KS epoch {epoch+1}/{n_epochs}: loss={total_loss.item():.6f}, "
                  f"LGT={total_lgt.item():.6f}, LP={total_lp.item():.6f}")
    
    return losses, lgt_list, lp_list


# ============================================================
# Evaluation
# ============================================================
def compute_derivatives(trajectory, dx):
    """Compute first and second spatial derivatives using finite differences."""
    qx = np.gradient(trajectory, dx, axis=-1)
    qxx = np.gradient(qx, dx, axis=-1)
    return qx, qxx


def compute_joint_pdf(qx, qxx, n_bins=100):
    """Compute joint PDF of qx and qxx."""
    qx_flat = qx.flatten()
    qxx_flat = qxx.flatten()
    
    H, xedges, yedges = np.histogram2d(qx_flat, qxx_flat, bins=n_bins, density=True)
    return H, xedges, yedges


def compute_kl_divergence(P, Q, eps=1e-12):
    """Compute KL divergence D_KL(P || Q)."""
    P = P + eps
    Q = Q + eps
    P = P / P.sum()
    Q = Q / Q.sum()
    return np.sum(P * np.log(P / Q))


def compute_return_period(trajectory, dt_save):
    """Compute return period: average time between exceedances of magnitude thresholds."""
    max_vals = np.max(trajectory, axis=-1)  # Max over spatial dimension at each time
    
    thresholds = np.linspace(np.percentile(max_vals, 10), np.percentile(max_vals, 99), 50)
    return_periods = []
    
    for thresh in thresholds:
        exceedance_times = np.where(max_vals > thresh)[0] * dt_save
        if len(exceedance_times) > 1:
            intervals = np.diff(exceedance_times)
            intervals = intervals[intervals > 0]
            if len(intervals) > 0:
                return_periods.append(np.mean(intervals))
            else:
                return_periods.append(np.nan)
        else:
            return_periods.append(np.nan)
    
    return thresholds, np.array(return_periods)


# ============================================================
# Main
# ============================================================
def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("=== MP-NODE Replication: Kuramoto-Sivashinsky ===")
    
    # KS parameters
    L = 22.0
    N = 64
    dt_ks = 0.25  # Time step for saving (paper uses 0.25)
    
    # Generate training data
    print("\nGenerating KS training data...")
    solver = KSSolver(L=L, N=N, dt=0.05)  # Internal dt for solver
    
    # Random initial condition
    np.random.seed(42)
    q0 = np.random.randn(N) * 0.1
    
    # First integrate for transient
    print("  Running transient (t=0 to 1000)...")
    transient_data = solver.integrate(q0, T=1000.0, save_every=5)
    q0_on_manifold = transient_data[-1]
    
    # Generate training trajectory (t=0 to 25000, save every 0.25)
    print("  Generating training data (t=0 to 25000)...")
    # save_every=5 because internal dt=0.05, so 5 steps = 0.25
    train_data = solver.integrate(q0_on_manifold, T=25000.0, save_every=5)
    print(f"  Training data shape: {train_data.shape}")  # Should be ~100001 x 64
    
    # Subsample for manageable training
    train_data = train_data[::1]  # Keep all
    # But limit to first 10000 snapshots for speed
    train_data = train_data[:10000]
    print(f"  Using {len(train_data)} training snapshots")
    
    # Generate test data
    print("  Generating test data...")
    q0_test = train_data[-1]
    test_data = solver.integrate(q0_test, T=2000.0, save_every=5)
    print(f"  Test data shape: {test_data.shape}")
    
    # Normalize data
    data_mean = train_data.mean()
    data_std = train_data.std()
    train_norm = (train_data - data_mean) / data_std
    test_norm = (test_data - data_mean) / data_std
    
    dt = dt_ks  # dt between saved snapshots
    
    # ========== Train Vanilla NODE ==========
    print("\n--- Training Vanilla KS NODE ---")
    vanilla_model = KSNeuralODE(n_spatial=N, hidden_channels=32, n_layers=4).to(device)
    print(f"  Model params: {sum(p.numel() for p in vanilla_model.parameters())}")
    
    t0 = time.time()
    vanilla_losses = train_vanilla_ks(
        vanilla_model, train_norm, dt,
        n_epochs=3000, lr=1e-3, rollout_steps=10, batch_size=8
    )
    vanilla_time = time.time() - t0
    print(f"  Training time: {vanilla_time:.1f}s")
    
    # ========== Train MP-NODE ==========
    print("\n--- Training MP KS NODE ---")
    mp_model = KSNeuralODE(n_spatial=N, hidden_channels=32, n_layers=4).to(device)
    
    # Paper: trajectory length=75, discontinuities=25 (Table 1 best)
    # We use rollout_steps=60 (60*0.25=15 time units, sub-Lyapunov since tau_L~22)
    # n_windows=5 (12 steps per window = 3 time units each)
    mu_schedule = {0: 1e-4, 750: 1e-2, 1500: 1e0, 2250: 1e2}
    
    t0 = time.time()
    mp_losses, mp_lgt, mp_lp = train_mp_ks(
        mp_model, train_norm, dt,
        n_epochs=3000, lr=1e-3, rollout_steps=60, n_windows=5,
        batch_size=8, mu_schedule=mu_schedule
    )
    mp_time = time.time() - t0
    print(f"  Training time: {mp_time:.1f}s")
    
    # ========== Evaluate ==========
    print("\n--- Evaluating Models ---")
    
    # Short-term prediction
    q0_eval = torch.tensor(test_norm[0], dtype=torch.float32, device=device)
    n_pred_short = 200  # 200 * 0.25 = 50 time units (~2.3 Lyapunov times)
    n_pred_long = 3000  # 3000 * 0.25 = 750 time units (~34 Lyapunov times)
    
    with torch.no_grad():
        vanilla_short = rk4_integrate_ks(vanilla_model, q0_eval, n_pred_short, dt)
        vanilla_short = vanilla_short.cpu().numpy() * data_std + data_mean
        
        mp_short = rk4_integrate_ks(mp_model, q0_eval, n_pred_short, dt)
        mp_short = mp_short.cpu().numpy() * data_std + data_mean
    
    test_denorm = test_data[:n_pred_short+1]
    
    # Long-term prediction for statistics
    print("  Generating long rollouts for statistics...")
    with torch.no_grad():
        vanilla_long = rk4_integrate_ks(vanilla_model, q0_eval, n_pred_long, dt)
        vanilla_long = vanilla_long.cpu().numpy() * data_std + data_mean
        
        mp_long = rk4_integrate_ks(mp_model, q0_eval, n_pred_long, dt)
        mp_long = mp_long.cpu().numpy() * data_std + data_mean
    
    test_long = test_data[:n_pred_long+1]
    
    # ========== Plots ==========
    print("\nGenerating plots...")
    dx = L / N
    
    # Fig 4: Hovmöller diagrams (space-time plots)
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    x = np.linspace(0, L, N, endpoint=False)
    
    # Short-term
    n_show_short = min(200, len(test_denorm), len(vanilla_short), len(mp_short))
    t_show = np.arange(n_show_short) * dt
    
    vmin, vmax = test_denorm[:n_show_short].min(), test_denorm[:n_show_short].max()
    
    ax = axes[0, 0]
    ax.pcolormesh(x, t_show, test_denorm[:n_show_short], cmap='RdBu_r', vmin=vmin, vmax=vmax)
    ax.set_title('True KS (Short)')
    ax.set_xlabel('x'); ax.set_ylabel('t')
    
    ax = axes[0, 1]
    ax.pcolormesh(x, t_show, vanilla_short[:n_show_short], cmap='RdBu_r', vmin=vmin, vmax=vmax)
    ax.set_title('Vanilla NODE (Short)')
    ax.set_xlabel('x'); ax.set_ylabel('t')
    
    ax = axes[0, 2]
    ax.pcolormesh(x, t_show, mp_short[:n_show_short], cmap='RdBu_r', vmin=vmin, vmax=vmax)
    ax.set_title('MP-NODE (Short)')
    ax.set_xlabel('x'); ax.set_ylabel('t')
    
    # Long-term
    n_show_long = min(2000, len(test_long), len(vanilla_long), len(mp_long))
    t_show_long = np.arange(n_show_long) * dt
    
    ax = axes[1, 0]
    ax.pcolormesh(x, t_show_long, test_long[:n_show_long], cmap='RdBu_r')
    ax.set_title('True KS (Long)')
    ax.set_xlabel('x'); ax.set_ylabel('t')
    
    ax = axes[1, 1]
    vl = vanilla_long[:n_show_long]
    if np.isfinite(vl).all():
        ax.pcolormesh(x, t_show_long, vl, cmap='RdBu_r')
    ax.set_title('Vanilla NODE (Long)')
    ax.set_xlabel('x'); ax.set_ylabel('t')
    
    ax = axes[1, 2]
    ml = mp_long[:n_show_long]
    if np.isfinite(ml).all():
        ax.pcolormesh(x, t_show_long, ml, cmap='RdBu_r')
    ax.set_title('MP-NODE (Long)')
    ax.set_xlabel('x'); ax.set_ylabel('t')
    
    plt.tight_layout()
    plt.savefig('fig_ks_hovmoller.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # Fig 5: Joint PDF of derivatives
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # Use long-term data for PDF
    n_pdf = min(3000, len(test_long), len(mp_long))
    
    qx_true, qxx_true = compute_derivatives(test_long[:n_pdf], dx)
    pdf_true, xe_t, ye_t = compute_joint_pdf(qx_true, qxx_true, n_bins=80)
    
    ax = axes[0]
    ax.pcolormesh(xe_t[:-1], ye_t[:-1], pdf_true.T, cmap='hot_r')
    ax.set_title('True KS')
    ax.set_xlabel('q_x'); ax.set_ylabel('q_xx')
    
    if np.isfinite(vanilla_long[:n_pdf]).all():
        qx_v, qxx_v = compute_derivatives(vanilla_long[:n_pdf], dx)
        pdf_v, _, _ = compute_joint_pdf(qx_v, qxx_v, n_bins=80)
        ax = axes[1]
        ax.pcolormesh(xe_t[:-1], ye_t[:-1], pdf_v.T, cmap='hot_r')
        ax.set_title('Vanilla NODE')
        ax.set_xlabel('q_x'); ax.set_ylabel('q_xx')
        kl_vanilla = compute_kl_divergence(pdf_v, pdf_true)
    else:
        kl_vanilla = float('nan')
        axes[1].set_title('Vanilla NODE (diverged)')
    
    if np.isfinite(mp_long[:n_pdf]).all():
        qx_m, qxx_m = compute_derivatives(mp_long[:n_pdf], dx)
        pdf_m, _, _ = compute_joint_pdf(qx_m, qxx_m, n_bins=80)
        ax = axes[2]
        ax.pcolormesh(xe_t[:-1], ye_t[:-1], pdf_m.T, cmap='hot_r')
        ax.set_title('MP-NODE')
        ax.set_xlabel('q_x'); ax.set_ylabel('q_xx')
        kl_mp = compute_kl_divergence(pdf_m, pdf_true)
    else:
        kl_mp = float('nan')
        axes[2].set_title('MP-NODE (diverged)')
    
    plt.tight_layout()
    plt.savefig('fig_ks_joint_pdf.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"  KL divergence - Vanilla: {kl_vanilla:.4f}, MP-NODE: {kl_mp:.4f}")
    
    # Fig 6: Return period
    fig, ax = plt.subplots(figsize=(8, 6))
    
    thresh_t, rp_t = compute_return_period(test_long[:n_pdf], dt)
    ax.plot(thresh_t, rp_t, 'k-', linewidth=2, label='True')
    
    if np.isfinite(vanilla_long[:n_pdf]).all():
        thresh_v, rp_v = compute_return_period(vanilla_long[:n_pdf], dt)
        ax.plot(thresh_v, rp_v, 'b--', label='Vanilla NODE')
    
    if np.isfinite(mp_long[:n_pdf]).all():
        thresh_m, rp_m = compute_return_period(mp_long[:n_pdf], dt)
        ax.plot(thresh_m, rp_m, 'r--', label='MP-NODE')
    
    ax.set_xlabel('Maximum State Magnitude')
    ax.set_ylabel('Return Period (time units)')
    ax.set_title('Return Period Comparison')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('fig_ks_return_period.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # Training loss comparison
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.semilogy(vanilla_losses, alpha=0.5, label='Vanilla NODE')
    ax.semilogy(mp_losses, alpha=0.5, label='MP-NODE')
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Loss')
    ax.set_title('KS Training Loss')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('fig_ks_training.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("All KS plots saved.")
    
    # ========== Save Results ==========
    results = {
        'ks_params': {
            'L': L, 'N': N, 'dt': dt,
            'lyapunov_time': 22.0,
        },
        'training': {
            'vanilla_final_loss': float(vanilla_losses[-1]),
            'mp_final_loss': float(mp_losses[-1]),
            'vanilla_time_s': vanilla_time,
            'mp_time_s': mp_time,
            'n_epochs': 3000,
        },
        'kl_divergence': {
            'vanilla': float(kl_vanilla),
            'mp_node': float(kl_mp),
            'note': 'Paper Table 1: best MP-NODE KL=0.029, vanilla NODE KL=0.773'
        },
    }
    
    with open('results_ks.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n=== KS Results ===")
    print(json.dumps(results, indent=2))
    
    return results


if __name__ == '__main__':
    main()
