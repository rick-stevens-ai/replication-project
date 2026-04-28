"""
MP-NODE for Lorenz-63 System
Implements the Multi-Step Penalty Neural ODE (Algorithm 1) from the paper.

Trains a neural ODE to learn the Lorenz-63 dynamics, comparing:
1. Vanilla NODE (single trajectory backpropagation)
2. MP-NODE (multi-step penalty with windowed training)

Evaluates:
- Short-term trajectory prediction
- Long-term attractor statistics
- Lyapunov exponent estimation
"""

import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import solve_ivp
import json
import os
import time

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

# ============================================================
# True Lorenz-63 System
# ============================================================
SIGMA = 10.0
BETA = 8.0 / 3.0
RHO = 28.0

def lorenz_rhs(t, state):
    x, y, z = state
    return [SIGMA*(y-x), x*(RHO-z)-y, x*y - BETA*z]

def generate_lorenz_data(q0, T, dt, transient=100.0):
    """Generate Lorenz trajectory data."""
    # Integrate through transient
    sol_trans = solve_ivp(lorenz_rhs, [0, transient], q0, method='DOP853',
                          rtol=1e-12, atol=1e-14)
    q0_on_attractor = sol_trans.y[:, -1]
    
    # Generate trajectory on attractor
    t_eval = np.arange(0, T, dt)
    sol = solve_ivp(lorenz_rhs, [0, T], q0_on_attractor, method='DOP853',
                    t_eval=t_eval, rtol=1e-12, atol=1e-14)
    return sol.t, sol.y.T  # (n_steps, 3)

# ============================================================
# Neural ODE Right-Hand Side
# ============================================================
class NeuralODEFunc(nn.Module):
    """Simple feedforward network as ODE RHS: dq/dt = NN(q)"""
    def __init__(self, state_dim=3, hidden_dim=64, n_layers=3):
        super().__init__()
        layers = []
        layers.append(nn.Linear(state_dim, hidden_dim))
        layers.append(nn.Tanh())
        for _ in range(n_layers - 1):
            layers.append(nn.Linear(hidden_dim, hidden_dim))
            layers.append(nn.Tanh())
        layers.append(nn.Linear(hidden_dim, state_dim))
        self.net = nn.Sequential(*layers)
        
        # Initialize weights small
        for m in self.net:
            if isinstance(m, nn.Linear):
                nn.init.xavier_normal_(m.weight, gain=0.1)
                nn.init.zeros_(m.bias)
    
    def forward(self, t, q):
        return self.net(q)

# ============================================================
# ODE Integrator (RK4)
# ============================================================
def rk4_integrate(func, q0, t_span, n_steps):
    """Integrate ODE using RK4, returning trajectory at all steps."""
    dt = (t_span[1] - t_span[0]) / n_steps
    t = t_span[0]
    q = q0
    trajectory = [q]
    times = [t]
    
    for _ in range(n_steps):
        k1 = func(t, q)
        k2 = func(t + 0.5*dt, q + 0.5*dt*k1)
        k3 = func(t + 0.5*dt, q + 0.5*dt*k2)
        k4 = func(t + dt, q + dt*k3)
        q = q + (dt/6.0) * (k1 + 2*k2 + 2*k3 + k4)
        t = t + dt
        trajectory.append(q)
        times.append(t)
    
    return torch.stack(trajectory, dim=0), torch.tensor(times)

# ============================================================
# Training: Vanilla NODE
# ============================================================
def train_vanilla_node(train_data, train_times, dt, n_epochs=2000, lr=1e-3, 
                       rollout_steps=50, batch_size=32, verbose=True):
    """Train vanilla NODE with MSE loss on trajectory."""
    model = NeuralODEFunc(state_dim=3, hidden_dim=64, n_layers=3).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=n_epochs, eta_min=1e-5)
    
    n_data = len(train_data) - rollout_steps
    train_tensor = torch.tensor(train_data, dtype=torch.float32, device=device)
    
    losses = []
    
    for epoch in range(n_epochs):
        # Random batch of starting indices
        idx = np.random.randint(0, n_data, size=batch_size)
        
        batch_loss = 0.0
        for i in idx:
            q0 = train_tensor[i]
            target = train_tensor[i:i+rollout_steps+1]
            
            pred, _ = rk4_integrate(model, q0, [0, rollout_steps*dt], rollout_steps)
            loss = torch.mean((pred - target)**2)
            batch_loss = batch_loss + loss
        
        batch_loss = batch_loss / batch_size
        
        optimizer.zero_grad()
        batch_loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        scheduler.step()
        
        losses.append(batch_loss.item())
        
        if verbose and (epoch+1) % 200 == 0:
            print(f"  Vanilla NODE epoch {epoch+1}/{n_epochs}: loss={batch_loss.item():.6f}")
    
    return model, losses

# ============================================================
# Training: MP-NODE (Algorithm 1)
# ============================================================
def train_mp_node(train_data, train_times, dt, n_epochs=2000, lr=1e-3,
                  rollout_steps=50, n_windows=5, batch_size=32,
                  mu_schedule=None, verbose=True):
    """
    Train MP-NODE using Algorithm 1 from the paper.
    
    The trajectory is split into n_windows non-overlapping windows.
    Learnable intermediate initial conditions q_k^+ are optimized along with NN params.
    Loss = L_GT + (mu/2) * L_P
    """
    model = NeuralODEFunc(state_dim=3, hidden_dim=64, n_layers=3).to(device)
    
    if mu_schedule is None:
        # Default: start low, increase by 10x at intervals
        mu_schedule = {0: 1e-6, 400: 1e-4, 800: 1e-2, 1200: 1e0, 1600: 1e2}
    
    n_data = len(train_data) - rollout_steps
    train_tensor = torch.tensor(train_data, dtype=torch.float32, device=device)
    steps_per_window = rollout_steps // n_windows
    
    # All NN parameters
    nn_params = list(model.parameters())
    optimizer_nn = torch.optim.Adam(nn_params, lr=lr)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer_nn, T_max=n_epochs, eta_min=1e-5)
    
    losses = []
    lgt_history = []
    lp_history = []
    mu_current = list(mu_schedule.values())[0]
    
    for epoch in range(n_epochs):
        # Update mu based on schedule
        if epoch in mu_schedule:
            mu_current = mu_schedule[epoch]
            if verbose:
                print(f"  Updated mu to {mu_current:.1e} at epoch {epoch}")
        
        idx = np.random.randint(0, n_data, size=batch_size)
        
        total_lgt = 0.0
        total_lp = 0.0
        
        for i in idx:
            target = train_tensor[i:i+rollout_steps+1]
            
            # Initialize q_plus from ground truth (re-initialized each batch per Algorithm 1)
            q_plus = []
            for k in range(1, n_windows):
                step_idx = k * steps_per_window
                qk = target[step_idx].clone().detach().requires_grad_(True)
                q_plus.append(qk)
            
            # Create optimizer for this batch's q_plus
            all_params = list(model.parameters()) + q_plus
            
            # Forward pass through windows
            pred_all = []
            penalty = torch.tensor(0.0, device=device)
            
            for w in range(n_windows):
                if w == 0:
                    q_start = target[0]  # True initial condition
                else:
                    q_start = q_plus[w - 1]
                
                w_start = w * steps_per_window
                w_end = (w + 1) * steps_per_window
                
                # Integrate this window
                pred_w, _ = rk4_integrate(model, q_start, 
                                         [0, steps_per_window * dt], 
                                         steps_per_window)
                pred_all.append(pred_w)
                
                # Penalty: discontinuity between end of window w and start of window w+1
                if w < n_windows - 1:
                    q_end = pred_w[-1]  # End of this window
                    q_next_start = q_plus[w]  # Start of next window
                    penalty = penalty + torch.sum((q_next_start - q_end)**2)
            
            # Compute L_GT
            pred_full = torch.cat([pw[:-1] for pw in pred_all[:-1]] + [pred_all[-1]], dim=0)
            # Align lengths
            min_len = min(pred_full.shape[0], target.shape[0])
            lgt = torch.mean((pred_full[:min_len] - target[:min_len])**2)
            
            # Compute L_P
            lp = penalty / max(n_windows - 1, 1)
            
            total_lgt = total_lgt + lgt
            total_lp = total_lp + lp
        
        total_lgt = total_lgt / batch_size
        total_lp = total_lp / batch_size
        total_loss = total_lgt + (mu_current / 2.0) * total_lp
        
        optimizer_nn.zero_grad()
        # Zero grad for q_plus manually
        for qp in q_plus:
            if qp.grad is not None:
                qp.grad.zero_()
        
        total_loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer_nn.step()
        
        # Update q_plus with gradient descent
        with torch.no_grad():
            for qp in q_plus:
                if qp.grad is not None:
                    qp -= lr * qp.grad
        
        scheduler.step()
        
        losses.append(total_loss.item())
        lgt_history.append(total_lgt.item())
        lp_history.append(total_lp.item())
        
        if verbose and (epoch+1) % 200 == 0:
            print(f"  MP-NODE epoch {epoch+1}/{n_epochs}: loss={total_loss.item():.6f}, "
                  f"LGT={total_lgt.item():.6f}, LP={total_lp.item():.6f}, mu={mu_current:.1e}")
    
    return model, losses, lgt_history, lp_history

# ============================================================
# Evaluation
# ============================================================
def evaluate_trajectory(model, q0, T, dt, true_traj, label=""):
    """Evaluate short-term trajectory prediction."""
    q0_tensor = torch.tensor(q0, dtype=torch.float32, device=device)
    n_steps = int(T / dt)
    
    with torch.no_grad():
        pred, _ = rk4_integrate(model, q0_tensor, [0, T], n_steps)
    pred = pred.cpu().numpy()
    
    # Compute MSE over time
    min_len = min(len(pred), len(true_traj))
    mse = np.mean((pred[:min_len] - true_traj[:min_len])**2, axis=1)
    
    return pred, mse


def compute_attractor_statistics(model, q0, T_total=500.0, dt=0.01, T_transient=50.0):
    """Generate long trajectory and compute attractor statistics."""
    q0_tensor = torch.tensor(q0, dtype=torch.float32, device=device)
    n_total = int(T_total / dt)
    
    with torch.no_grad():
        # Generate in chunks to avoid memory issues
        chunk_size = 10000
        trajectory = []
        q = q0_tensor
        for start in range(0, n_total, chunk_size):
            end = min(start + chunk_size, n_total)
            steps = end - start
            pred, _ = rk4_integrate(model, q, [0, steps*dt], steps)
            trajectory.append(pred[:-1].cpu().numpy())
            q = pred[-1]
        trajectory.append(pred[-1:].cpu().numpy())
        trajectory = np.concatenate(trajectory, axis=0)
    
    # Remove transient
    n_transient = int(T_transient / dt)
    traj = trajectory[n_transient:]
    
    # Statistics
    stats = {
        'mean': traj.mean(axis=0).tolist(),
        'std': traj.std(axis=0).tolist(),
        'x_range': [float(traj[:, 0].min()), float(traj[:, 0].max())],
        'y_range': [float(traj[:, 1].min()), float(traj[:, 1].max())],
        'z_range': [float(traj[:, 2].min()), float(traj[:, 2].max())],
    }
    
    return traj, stats


def estimate_lyapunov_exponent(model, q0, dt=0.01, T=200.0, d0=1e-8):
    """Estimate the maximum Lyapunov exponent of the learned system."""
    q0_tensor = torch.tensor(q0, dtype=torch.float32, device=device)
    n_steps = int(T / dt)
    
    # Perturbed initial condition
    perturbation = np.random.randn(3)
    perturbation = perturbation / np.linalg.norm(perturbation) * d0
    q0_pert = torch.tensor(q0 + perturbation, dtype=torch.float32, device=device)
    
    lyap_sum = 0.0
    n_renorm = 0
    q1 = q0_tensor.clone()
    q2 = q0_pert.clone()
    
    renorm_interval = 100  # steps between renormalization
    
    with torch.no_grad():
        for step in range(0, n_steps, renorm_interval):
            actual_steps = min(renorm_interval, n_steps - step)
            
            traj1, _ = rk4_integrate(model, q1, [0, actual_steps*dt], actual_steps)
            traj2, _ = rk4_integrate(model, q2, [0, actual_steps*dt], actual_steps)
            
            q1 = traj1[-1]
            q2 = traj2[-1]
            
            d = torch.norm(q2 - q1).item()
            if d > 0 and np.isfinite(d):
                lyap_sum += np.log(d / d0)
                n_renorm += 1
                
                # Renormalize
                direction = (q2 - q1) / d * d0
                q2 = q1 + direction
    
    if n_renorm > 0:
        lyap_exp = lyap_sum / (n_renorm * renorm_interval * dt)
    else:
        lyap_exp = float('nan')
    
    return lyap_exp


def estimate_true_lyapunov():
    """Estimate Lyapunov exponent of the true Lorenz system."""
    q0 = [1.0, 1.0, 1.0]
    d0 = 1e-8
    dt = 0.01
    T = 500.0
    n_steps = int(T / dt)
    renorm_interval = 100
    
    perturbation = np.random.randn(3)
    perturbation = perturbation / np.linalg.norm(perturbation) * d0
    
    q1 = np.array(q0, dtype=np.float64)
    q2 = q1 + perturbation
    
    lyap_sum = 0.0
    n_renorm = 0
    
    for step in range(0, n_steps, renorm_interval):
        t_span = [0, renorm_interval * dt]
        sol1 = solve_ivp(lorenz_rhs, t_span, q1, method='DOP853', rtol=1e-12, atol=1e-14)
        sol2 = solve_ivp(lorenz_rhs, t_span, q2, method='DOP853', rtol=1e-12, atol=1e-14)
        
        q1 = sol1.y[:, -1]
        q2 = sol2.y[:, -1]
        
        d = np.linalg.norm(q2 - q1)
        if d > 0:
            lyap_sum += np.log(d / d0)
            n_renorm += 1
            direction = (q2 - q1) / d * d0
            q2 = q1 + direction
    
    return lyap_sum / (n_renorm * renorm_interval * dt)


# ============================================================
# Main
# ============================================================
def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("=== MP-NODE Replication: Lorenz-63 ===")
    
    # Generate training data
    print("\nGenerating Lorenz-63 training data...")
    dt = 0.01
    T_train = 200.0  # Total training time
    q0_train = [1.0, 1.0, 1.0]
    t_train, data_train = generate_lorenz_data(q0_train, T_train, dt, transient=100.0)
    print(f"Training data shape: {data_train.shape}")
    
    # Generate test data (different IC on attractor)
    q0_test = data_train[-1]  # Start from end of training
    t_test, data_test = generate_lorenz_data(q0_test.tolist(), 50.0, dt, transient=50.0)
    print(f"Test data shape: {data_test.shape}")
    
    # Lyapunov time for Lorenz-63: ~1/0.9 ≈ 1.1 time units
    # Window size should be ~1 Lyapunov time
    rollout_steps = 100  # 100 * 0.01 = 1.0 time unit (~ 1 Lyapunov time)
    n_windows = 5  # Each window ~ 0.2 time units (sub-Lyapunov)
    
    # ========== Train Vanilla NODE ==========
    print("\n--- Training Vanilla NODE ---")
    t0 = time.time()
    vanilla_model, vanilla_losses = train_vanilla_node(
        data_train, t_train, dt,
        n_epochs=3000, lr=1e-3, rollout_steps=rollout_steps,
        batch_size=16, verbose=True
    )
    vanilla_time = time.time() - t0
    print(f"Vanilla NODE training time: {vanilla_time:.1f}s")
    
    # ========== Train MP-NODE ==========
    print("\n--- Training MP-NODE ---")
    mu_schedule = {0: 1e-6, 600: 1e-4, 1200: 1e-2, 1800: 1e0, 2400: 1e2}
    t0 = time.time()
    mp_model, mp_losses, mp_lgt, mp_lp = train_mp_node(
        data_train, t_train, dt,
        n_epochs=3000, lr=1e-3, rollout_steps=rollout_steps,
        n_windows=n_windows, batch_size=16,
        mu_schedule=mu_schedule, verbose=True
    )
    mp_time = time.time() - t0
    print(f"MP-NODE training time: {mp_time:.1f}s")
    
    # ========== Evaluate ==========
    print("\n--- Evaluating Models ---")
    
    # Short-term prediction
    T_eval_short = 5.0  # ~5 Lyapunov times
    q0_eval = data_test[0]
    
    vanilla_pred, vanilla_mse = evaluate_trajectory(
        vanilla_model, q0_eval, T_eval_short, dt, data_test, "Vanilla")
    mp_pred, mp_mse = evaluate_trajectory(
        mp_model, q0_eval, T_eval_short, dt, data_test, "MP-NODE")
    
    # Lyapunov exponent estimation
    print("\nEstimating Lyapunov exponents...")
    true_lyap = estimate_true_lyapunov()
    print(f"  True Lorenz LE: {true_lyap:.4f} (expected ~0.906)")
    
    vanilla_lyap = estimate_lyapunov_exponent(vanilla_model, q0_eval.tolist())
    print(f"  Vanilla NODE LE: {vanilla_lyap:.4f}")
    
    mp_lyap = estimate_lyapunov_exponent(mp_model, q0_eval.tolist())
    print(f"  MP-NODE LE: {mp_lyap:.4f}")
    
    # Long-term attractor statistics
    print("\nComputing attractor statistics...")
    true_traj_long, true_stats = None, None
    # True attractor
    t_long, true_long = generate_lorenz_data([1.0, 1.0, 1.0], 500.0, dt, transient=200.0)
    true_stats = {
        'mean': true_long.mean(axis=0).tolist(),
        'std': true_long.std(axis=0).tolist(),
    }
    
    vanilla_traj, vanilla_stats = compute_attractor_statistics(
        vanilla_model, q0_eval.tolist(), T_total=500.0)
    mp_traj, mp_stats = compute_attractor_statistics(
        mp_model, q0_eval.tolist(), T_total=500.0)
    
    print(f"\nAttractor Statistics Comparison:")
    print(f"  True    mean: [{true_stats['mean'][0]:.2f}, {true_stats['mean'][1]:.2f}, {true_stats['mean'][2]:.2f}]")
    print(f"  Vanilla mean: [{vanilla_stats['mean'][0]:.2f}, {vanilla_stats['mean'][1]:.2f}, {vanilla_stats['mean'][2]:.2f}]")
    print(f"  MP-NODE mean: [{mp_stats['mean'][0]:.2f}, {mp_stats['mean'][1]:.2f}, {mp_stats['mean'][2]:.2f}]")
    print(f"  True    std:  [{true_stats['std'][0]:.2f}, {true_stats['std'][1]:.2f}, {true_stats['std'][2]:.2f}]")
    print(f"  Vanilla std:  [{vanilla_stats['std'][0]:.2f}, {vanilla_stats['std'][1]:.2f}, {vanilla_stats['std'][2]:.2f}]")
    print(f"  MP-NODE std:  [{mp_stats['std'][0]:.2f}, {mp_stats['std'][1]:.2f}, {mp_stats['std'][2]:.2f}]")
    
    # ========== Plotting ==========
    print("\nGenerating plots...")
    
    # Fig 1: Training loss comparison
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    ax = axes[0]
    ax.semilogy(vanilla_losses, alpha=0.5, label='Vanilla NODE')
    ax.semilogy(mp_losses, alpha=0.5, label='MP-NODE (total)')
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Loss')
    ax.set_title('Training Loss')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    ax = axes[1]
    ax.semilogy(mp_lgt, alpha=0.5, label='L_GT (ground truth)')
    ax.semilogy(mp_lp, alpha=0.5, label='L_P (penalty)')
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Loss')
    ax.set_title('MP-NODE Loss Components')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('fig_lorenz_training.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # Fig 2: Short-term trajectory comparison
    t_eval = np.arange(0, T_eval_short, dt)
    n_plot = min(len(t_eval), len(vanilla_pred)-1, len(mp_pred)-1, len(data_test)-1)
    
    fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)
    labels = ['x', 'y', 'z']
    for dim in range(3):
        ax = axes[dim]
        ax.plot(t_eval[:n_plot], data_test[:n_plot, dim], 'k-', label='True', linewidth=1.5)
        ax.plot(t_eval[:n_plot], vanilla_pred[:n_plot, dim], 'b--', label='Vanilla NODE', alpha=0.7)
        ax.plot(t_eval[:n_plot], mp_pred[:n_plot, dim], 'r--', label='MP-NODE', alpha=0.7)
        ax.set_ylabel(labels[dim])
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)
    axes[2].set_xlabel('Time')
    axes[0].set_title('Short-term Trajectory Prediction (Lorenz-63)')
    plt.tight_layout()
    plt.savefig('fig_lorenz_trajectory.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # Fig 3: MSE over time
    fig, ax = plt.subplots(figsize=(10, 5))
    t_mse_v = np.arange(len(vanilla_mse)) * dt
    t_mse_m = np.arange(len(mp_mse)) * dt
    ax.semilogy(t_mse_v, vanilla_mse, label='Vanilla NODE', alpha=0.7)
    ax.semilogy(t_mse_m, mp_mse, label='MP-NODE', alpha=0.7)
    ax.axvline(x=1.1, color='gray', linestyle='--', label='1 Lyapunov time', alpha=0.5)
    ax.set_xlabel('Time')
    ax.set_ylabel('MSE')
    ax.set_title('Prediction Error vs Time')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('fig_lorenz_mse.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # Fig 4: Attractor comparison (3D)
    fig = plt.figure(figsize=(18, 6))
    
    ax1 = fig.add_subplot(131, projection='3d')
    ax1.plot(true_long[::10, 0], true_long[::10, 1], true_long[::10, 2], 
             'k-', alpha=0.3, linewidth=0.3)
    ax1.set_title('True Lorenz Attractor')
    ax1.set_xlabel('x'); ax1.set_ylabel('y'); ax1.set_zlabel('z')
    
    if len(vanilla_traj) > 100:
        ax2 = fig.add_subplot(132, projection='3d')
        ax2.plot(vanilla_traj[::10, 0], vanilla_traj[::10, 1], vanilla_traj[::10, 2],
                 'b-', alpha=0.3, linewidth=0.3)
        ax2.set_title('Vanilla NODE Attractor')
        ax2.set_xlabel('x'); ax2.set_ylabel('y'); ax2.set_zlabel('z')
    
    if len(mp_traj) > 100:
        ax3 = fig.add_subplot(133, projection='3d')
        ax3.plot(mp_traj[::10, 0], mp_traj[::10, 1], mp_traj[::10, 2],
                 'r-', alpha=0.3, linewidth=0.3)
        ax3.set_title('MP-NODE Attractor')
        ax3.set_xlabel('x'); ax3.set_ylabel('y'); ax3.set_zlabel('z')
    
    plt.tight_layout()
    plt.savefig('fig_lorenz_attractor.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # Fig 5: Distribution comparison (histograms)
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    labels = ['x', 'y', 'z']
    for dim in range(3):
        ax = axes[dim]
        ax.hist(true_long[:, dim], bins=80, density=True, alpha=0.5, label='True', color='k')
        if len(vanilla_traj) > 100:
            ax.hist(vanilla_traj[:, dim], bins=80, density=True, alpha=0.4, label='Vanilla', color='blue')
        if len(mp_traj) > 100:
            ax.hist(mp_traj[:, dim], bins=80, density=True, alpha=0.4, label='MP-NODE', color='red')
        ax.set_xlabel(labels[dim])
        ax.set_ylabel('Density')
        ax.legend()
        ax.set_title(f'Distribution of {labels[dim]}')
    plt.tight_layout()
    plt.savefig('fig_lorenz_distributions.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("All plots saved.")
    
    # ========== Save Results ==========
    results = {
        'training': {
            'vanilla_final_loss': float(vanilla_losses[-1]),
            'mp_final_loss': float(mp_losses[-1]),
            'vanilla_time_s': vanilla_time,
            'mp_time_s': mp_time,
            'n_epochs': 3000,
            'rollout_steps': rollout_steps,
            'n_windows': n_windows,
            'dt': dt,
        },
        'lyapunov_exponents': {
            'true': float(true_lyap),
            'vanilla_node': float(vanilla_lyap),
            'mp_node': float(mp_lyap),
            'reference_value': 0.906,
        },
        'attractor_stats': {
            'true': true_stats,
            'vanilla': vanilla_stats,
            'mp_node': mp_stats,
        },
        'short_term': {
            'vanilla_mean_mse_1LT': float(np.mean(vanilla_mse[:110])),  # ~1 Lyapunov time
            'mp_mean_mse_1LT': float(np.mean(mp_mse[:110])),
            'vanilla_mean_mse_3LT': float(np.mean(vanilla_mse[:330])),
            'mp_mean_mse_3LT': float(np.mean(mp_mse[:330])),
        }
    }
    
    with open('results_lorenz.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n=== Final Results ===")
    print(json.dumps(results, indent=2))
    
    return results


if __name__ == '__main__':
    results = main()
