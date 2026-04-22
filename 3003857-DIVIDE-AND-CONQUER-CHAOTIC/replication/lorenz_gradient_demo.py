"""
Replication of Section 4.1: Effectiveness of Multistep Penalty Method
- 4.1.1: Exploding Gradients demonstration
- 4.1.2: Non-convexity of Loss Landscape

Paper: "Divide and Conquer: Learning Chaotic Dynamical Systems with 
Multi-Step Penalty Neural ODEs" (OSTI 3003857)
"""

import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import os
import json

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

# ============================================================
# Lorenz-63 System
# ============================================================
def lorenz_rhs(t, state, sigma=10.0, beta=8.0/3.0, rho=28.0):
    x, y, z = state
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return [dx, dy, dz]


def lorenz_rhs_torch(state, sigma=10.0, beta=8.0/3.0, rho=28.0):
    """Torch version for AD-based gradient computation."""
    x, y, z = state[..., 0], state[..., 1], state[..., 2]
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return torch.stack([dx, dy, dz], dim=-1)


def rk4_step(state, dt, rho, sigma=10.0, beta=8.0/3.0):
    """Single RK4 step for Lorenz system."""
    def f(s):
        x, y, z = s[..., 0], s[..., 1], s[..., 2]
        dx = sigma * (y - x)
        dy = x * (rho - z) - y
        dz = x * y - beta * z
        return torch.stack([dx, dy, dz], dim=-1)
    
    k1 = f(state)
    k2 = f(state + 0.5 * dt * k1)
    k3 = f(state + 0.5 * dt * k2)
    k4 = f(state + dt * k3)
    return state + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)


def integrate_lorenz_torch(q0, n_steps, dt, rho):
    """Integrate Lorenz system using RK4 with torch autograd."""
    trajectory = [q0]
    state = q0
    for _ in range(n_steps):
        state = rk4_step(state, dt, rho)
        trajectory.append(state)
    return torch.stack(trajectory, dim=0)


# ============================================================
# Section 4.1.1: Exploding Gradients
# ============================================================
def compute_vanilla_gradient(rho_val, q0, T=20.0, n_steps=2000):
    """Compute gradient of J = (1/T)*integral(|z|)dt w.r.t. rho using vanilla AD."""
    dt = T / n_steps
    rho = torch.tensor(rho_val, dtype=torch.float64, requires_grad=True, device=device)
    state = q0.clone().detach().to(device).double()
    
    J = torch.tensor(0.0, dtype=torch.float64, device=device)
    for i in range(n_steps):
        state = rk4_step(state, dt, rho)
        J = J + torch.abs(state[2]) * dt
    J = J / T
    
    J.backward()
    return rho.grad.item(), J.item()


def compute_mp_gradient(rho_val, q0, T=20.0, n_steps=2000, n_windows=10, mu=1e-5):
    """Compute gradient using multi-step penalty method."""
    dt = T / n_steps
    steps_per_window = n_steps // n_windows
    
    rho = torch.tensor(rho_val, dtype=torch.float64, requires_grad=True, device=device)
    
    # Initialize intermediate initial conditions from a reference trajectory
    with torch.no_grad():
        ref_traj = integrate_lorenz_torch(q0.clone().to(device).double(), n_steps, dt, rho_val)
    
    # Learnable intermediate ICs
    q_plus = []
    for k in range(1, n_windows):
        idx = k * steps_per_window
        qk = ref_traj[idx].clone().detach().requires_grad_(True)
        q_plus.append(qk)
    
    # Compute objective with penalties
    J = torch.tensor(0.0, dtype=torch.float64, device=device)
    P = torch.tensor(0.0, dtype=torch.float64, device=device)
    
    for w in range(n_windows):
        if w == 0:
            state = q0.clone().to(device).double()
        else:
            state = q_plus[w - 1]
        
        for s in range(steps_per_window):
            state = rk4_step(state, dt, rho)
            J = J + torch.abs(state[2]) * dt
        
        # Penalty: discontinuity between end of this window and start of next
        if w < n_windows - 1:
            P = P + torch.sum((q_plus[w] - state) ** 2)
    
    J = J / T
    P = P / (n_windows - 1)
    
    loss = J + (mu / 2.0) * P
    loss.backward()
    
    return rho.grad.item(), J.item()


def demo_exploding_gradients():
    """Reproduce Figure 2: gradient comparison between vanilla and MP."""
    print("\n=== Section 4.1.1: Exploding Gradients Demo ===")
    
    q0 = torch.tensor([1.0, 1.0, 1.0], dtype=torch.float64, device=device)
    
    n_opt_steps = 1000
    lr = 0.01
    
    # Vanilla optimization
    print("Running vanilla optimization...")
    rho_vanilla = 28.0
    vanilla_grads = []
    vanilla_objs = []
    
    for i in range(n_opt_steps):
        try:
            grad, obj = compute_vanilla_gradient(rho_vanilla, q0)
            # Clip extreme gradients for stability
            grad_clipped = np.clip(grad, -1e8, 1e8)
            vanilla_grads.append(abs(grad))
            vanilla_objs.append(obj)
            rho_vanilla -= lr * np.sign(grad_clipped) * min(abs(grad_clipped), 1.0)
            rho_vanilla = max(1.0, rho_vanilla)  # Keep rho positive
        except Exception as e:
            print(f"  Vanilla step {i}: error {e}")
            vanilla_grads.append(vanilla_grads[-1] if vanilla_grads else 1e8)
            vanilla_objs.append(vanilla_objs[-1] if vanilla_objs else 100.0)
        
        if (i+1) % 200 == 0:
            print(f"  Step {i+1}: |grad|={vanilla_grads[-1]:.2e}, J={vanilla_objs[-1]:.4f}, rho={rho_vanilla:.4f}")
    
    # MP optimization
    print("\nRunning MP optimization...")
    rho_mp = 28.0
    mp_grads = []
    mp_objs = []
    mu = 1e-5
    mu_schedule = [1e-5]*170 + [1e-4]*170 + [1e-3]*170 + [1e-2]*170 + [1e-1]*170 + [1.0]*150
    
    for i in range(n_opt_steps):
        mu_i = mu_schedule[min(i, len(mu_schedule)-1)]
        try:
            grad, obj = compute_mp_gradient(rho_mp, q0, mu=mu_i)
            grad_clipped = np.clip(grad, -1e4, 1e4)
            mp_grads.append(abs(grad))
            mp_objs.append(obj)
            rho_mp -= lr * np.sign(grad_clipped) * min(abs(grad_clipped), 1.0)
            rho_mp = max(1.0, rho_mp)
        except Exception as e:
            print(f"  MP step {i}: error {e}")
            mp_grads.append(mp_grads[-1] if mp_grads else 1.0)
            mp_objs.append(mp_objs[-1] if mp_objs else 100.0)
        
        if (i+1) % 200 == 0:
            print(f"  Step {i+1}: |grad|={mp_grads[-1]:.2e}, J={mp_objs[-1]:.4f}, rho={rho_mp:.4f}, mu={mu_i:.1e}")
    
    # Plot Figure 2a: Gradient comparison
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    ax = axes[0]
    ax.semilogy(range(len(vanilla_grads)), vanilla_grads, label='Vanilla', alpha=0.7)
    ax.semilogy(range(len(mp_grads)), mp_grads, label='MP', alpha=0.7)
    # Mark mu increase points
    for k in range(1, 6):
        ax.axvline(x=170*k, color='gray', linestyle='--', alpha=0.3)
    ax.set_xlabel('Optimization Steps')
    ax.set_ylabel('|dJ/dρ|')
    ax.set_title('Gradient Magnitude Comparison')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot Figure 2b: Objective comparison
    ax = axes[1]
    ax.plot(range(len(vanilla_objs)), vanilla_objs, label='Vanilla', alpha=0.7)
    ax.plot(range(len(mp_objs)), mp_objs, label='MP', alpha=0.7)
    for k in range(1, 6):
        ax.axvline(x=170*k, color='gray', linestyle='--', alpha=0.3)
    ax.set_xlabel('Optimization Steps')
    ax.set_ylabel('Objective J')
    ax.set_title('Objective Value Comparison')
    ax.axhline(y=0.694, color='k', linestyle=':', label='Theoretical min (~0.694)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('fig2_gradient_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved fig2_gradient_comparison.png")
    
    return {
        'vanilla_final_obj': vanilla_objs[-1],
        'mp_final_obj': mp_objs[-1],
        'vanilla_max_grad': max(vanilla_grads),
        'mp_max_grad': max(mp_grads),
    }


# ============================================================
# Section 4.1.2: Loss Landscape Non-Convexity
# ============================================================
def compute_loss_landscape():
    """Reproduce Figure 3: loss landscape comparison for vanilla vs MP."""
    print("\n=== Section 4.1.2: Loss Landscape Comparison ===")
    
    sigma, beta, rho = 10.0, 8.0/3.0, 28.0
    T = 20.0
    n_steps = 2000
    dt = T / n_steps
    
    # Generate reference trajectory
    q0 = np.array([1.0, 1.0, 1.0])
    sol = solve_ivp(lorenz_rhs, [0, T], q0, method='RK45', 
                    t_eval=np.linspace(0, T, n_steps+1), rtol=1e-10, atol=1e-12)
    ref_traj = sol.y.T  # (n_steps+1, 3)
    
    # Create a time-varying control f(t) with 2000 parameters
    # We pick 2 arbitrary indices to vary for landscape visualization
    n_grid = 50
    f_base = np.zeros(n_steps)
    
    idx1, idx2 = 500, 1000  # Two arbitrary control parameters
    range1 = np.linspace(-5, 5, n_grid)
    range2 = np.linspace(-5, 5, n_grid)
    
    def compute_objective_vanilla(f_vec):
        """Compute objective for controlled Lorenz with f(t) added to dz/dt."""
        state = np.array([1.0, 1.0, 1.0])
        J = 0.0
        for i in range(n_steps):
            x, y, z = state
            dx = sigma * (y - x)
            dy = x * (rho - z) - y
            dz = x * y - beta * z + f_vec[i]
            k1 = np.array([dx, dy, dz])
            
            s2 = state + 0.5*dt*k1
            x, y, z = s2
            dx = sigma * (y - x)
            dy = x * (rho - z) - y
            dz = x * y - beta * z + f_vec[min(i, n_steps-1)]
            k2 = np.array([dx, dy, dz])
            
            s3 = state + 0.5*dt*k2
            x, y, z = s3
            dx = sigma * (y - x)
            dy = x * (rho - z) - y
            dz = x * y - beta * z + f_vec[min(i, n_steps-1)]
            k3 = np.array([dx, dy, dz])
            
            s4 = state + dt*k3
            x, y, z = s4
            dx = sigma * (y - x)
            dy = x * (rho - z) - y
            dz = x * y - beta * z + f_vec[min(i+1, n_steps-1)]
            k4 = np.array([dx, dy, dz])
            
            state = state + (dt/6.0)*(k1 + 2*k2 + 2*k3 + k4)
            
            val = 2*state[0] + state[1]
            if val >= 0:
                J += 0.5 * val**2 * dt
        
        return J / T
    
    def compute_objective_mp(f_vec, n_windows=10, mu=0.1):
        """Compute MP objective for controlled Lorenz."""
        steps_per_window = n_steps // n_windows
        
        # First, get reference trajectory for initialization
        ref_states = []
        state = np.array([1.0, 1.0, 1.0])
        ref_states.append(state.copy())
        for i in range(n_steps):
            x, y, z = state
            dx = sigma * (y - x)
            dy = x * (rho - z) - y
            dz = x * y - beta * z + f_vec[i]
            state = state + dt * np.array([dx, dy, dz])  # Simple Euler for ref
            ref_states.append(state.copy())
        
        # Use RK4 integration with windows
        J = 0.0
        P = 0.0
        
        for w in range(n_windows):
            start_step = w * steps_per_window
            if w == 0:
                state = np.array([1.0, 1.0, 1.0])
            else:
                state = ref_states[start_step].copy()
            
            for s in range(steps_per_window):
                idx = start_step + s
                x, y, z = state
                dx = sigma * (y - x)
                dy = x * (rho - z) - y
                dz = x * y - beta * z + f_vec[idx]
                k1 = np.array([dx, dy, dz])
                
                s2 = state + 0.5*dt*k1
                x, y, z = s2
                dx = sigma * (y - x)
                dy = x * (rho - z) - y
                dz = x * y - beta * z + f_vec[idx]
                k2 = np.array([dx, dy, dz])
                
                s3 = state + 0.5*dt*k2
                x, y, z = s3
                dx = sigma * (y - x)
                dy = x * (rho - z) - y
                dz = x * y - beta * z + f_vec[idx]
                k3 = np.array([dx, dy, dz])
                
                s4 = state + dt*k3
                x, y, z = s4
                dx = sigma * (y - x)
                dy = x * (rho - z) - y
                dz = x * y - beta * z + f_vec[min(idx+1, n_steps-1)]
                k4 = np.array([dx, dy, dz])
                
                state = state + (dt/6.0)*(k1 + 2*k2 + 2*k3 + k4)
                
                val = 2*state[0] + state[1]
                if val >= 0:
                    J += 0.5 * val**2 * dt
            
            # Penalty
            if w < n_windows - 1:
                next_start = ref_states[(w+1)*steps_per_window]
                P += np.sum((next_start - state)**2)
        
        J = J / T
        P = P / (n_windows - 1)
        return J + (mu/2.0) * P
    
    # Compute landscapes
    print("Computing vanilla loss landscape...")
    vanilla_landscape = np.zeros((n_grid, n_grid))
    for i, v1 in enumerate(range1):
        for j, v2 in enumerate(range2):
            f_vec = f_base.copy()
            f_vec[idx1] = v1
            f_vec[idx2] = v2
            vanilla_landscape[i, j] = compute_objective_vanilla(f_vec)
        if (i+1) % 10 == 0:
            print(f"  Vanilla: {i+1}/{n_grid}")
    
    print("Computing MP loss landscape...")
    mp_landscape = np.zeros((n_grid, n_grid))
    for i, v1 in enumerate(range1):
        for j, v2 in enumerate(range2):
            f_vec = f_base.copy()
            f_vec[idx1] = v1
            f_vec[idx2] = v2
            mp_landscape[i, j] = compute_objective_mp(f_vec)
        if (i+1) % 10 == 0:
            print(f"  MP: {i+1}/{n_grid}")
    
    # Plot Figure 3
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    X, Y = np.meshgrid(range1, range2)
    
    ax = axes[0]
    # Clip for visualization
    vl = np.clip(vanilla_landscape, np.percentile(vanilla_landscape, 5), 
                  np.percentile(vanilla_landscape, 95))
    c1 = ax.contourf(X, Y, vl.T, levels=30, cmap='viridis')
    plt.colorbar(c1, ax=ax)
    ax.set_title('Vanilla Loss Landscape')
    ax.set_xlabel(f'f[{idx1}]')
    ax.set_ylabel(f'f[{idx2}]')
    
    ax = axes[1]
    ml = np.clip(mp_landscape, np.percentile(mp_landscape, 5),
                  np.percentile(mp_landscape, 95))
    c2 = ax.contourf(X, Y, ml.T, levels=30, cmap='viridis')
    plt.colorbar(c2, ax=ax)
    ax.set_title('MP Loss Landscape')
    ax.set_xlabel(f'f[{idx1}]')
    ax.set_ylabel(f'f[{idx2}]')
    
    plt.tight_layout()
    plt.savefig('fig3_loss_landscape.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved fig3_loss_landscape.png")
    
    return {
        'vanilla_range': [float(vanilla_landscape.min()), float(vanilla_landscape.max())],
        'mp_range': [float(mp_landscape.min()), float(mp_landscape.max())],
        'vanilla_std': float(vanilla_landscape.std()),
        'mp_std': float(mp_landscape.std()),
    }


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    results = {}
    
    # Demo 1: Exploding gradients
    r1 = demo_exploding_gradients()
    results['exploding_gradients'] = r1
    
    # Demo 2: Loss landscape
    r2 = compute_loss_landscape()
    results['loss_landscape'] = r2
    
    with open('results_section41.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n=== Section 4.1 Results ===")
    print(json.dumps(results, indent=2))
