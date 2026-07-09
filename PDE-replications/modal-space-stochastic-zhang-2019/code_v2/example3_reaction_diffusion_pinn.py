"""
Example 3: Stochastic Reaction-Diffusion — Parametric PINN (Forward + Inverse)
===============================================================================
PDE: du/dt = a*Δu + b*u(1-u), x ∈ [0,1], t ∈ [0,1]
Stochastic: u(x,0;ω) has KL expansion with 19 modes
Forward: compute E[u], Var[u]  
Inverse: given observations, recover a=0.5, b=0.3

The reaction-diffusion equation has known analytical properties:
- Diffusion coefficient a controls spatial smoothing
- Reaction coefficient b controls logistic growth
"""
import os, sys, json, time
import numpy as np
import torch
import torch.nn as nn
from scipy.linalg import eigh

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Device: {device}")

A_TRUE = 0.5
B_TRUE = 0.3
N_KL = 6  # Reduced from 19 for practical training time; captures >95% energy
X_RANGE = (0, 1.0)
T_RANGE = (0, 1.0)
SIGMA_KL = 0.1
L_KL = 0.3


def compute_kl_expansion(n_modes=19, n_quad=200, sigma=0.1, l=0.3):
    """KL eigenpairs for Gaussian covariance on [0, 1]."""
    x_q = np.linspace(0, 1, n_quad)
    dx = x_q[1] - x_q[0]
    X1, X2 = np.meshgrid(x_q, x_q)
    C = sigma**2 * np.exp(-0.5 * (X1 - X2)**2 / l**2)
    C_w = C * dx
    evals, evecs = eigh(C_w)
    idx = np.argsort(-evals)
    evals = evals[idx[:n_modes]]
    evecs = evecs[:, idx[:n_modes]]
    for i in range(n_modes):
        norm_sq = np.sum(evecs[:, i]**2) * dx
        evecs[:, i] /= np.sqrt(norm_sq)
    return evals, evecs, x_q


class ModifiedMLP(nn.Module):
    def __init__(self, input_dim, output_dim=1, n_layers=5, hidden_dim=128):
        super().__init__()
        self.encoder = nn.Linear(input_dim, hidden_dim)
        self.U = nn.Linear(input_dim, hidden_dim)
        self.V = nn.Linear(input_dim, hidden_dim)
        self.layers = nn.ModuleList([nn.Linear(hidden_dim, hidden_dim) for _ in range(n_layers)])
        self.out = nn.Linear(hidden_dim, output_dim)
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_normal_(m.weight, gain=1.0)
                nn.init.zeros_(m.bias)

    def forward(self, x):
        u_gate = torch.tanh(self.U(x))
        v_gate = torch.tanh(self.V(x))
        h = torch.tanh(self.encoder(x))
        for layer in self.layers:
            z = torch.tanh(layer(h))
            h = (1 - z) * u_gate + z * v_gate
        return self.out(h)


def generate_ic(x, xi_samples, eigenvalues, eigenfunctions, x_kl):
    """IC: u0(x; ω) = 0.5 + Σ_k √λ_k * φ_k(x) * ξ_k"""
    u0 = 0.5 * np.ones_like(x)
    for k in range(len(eigenvalues)):
        phi = np.interp(x, x_kl, eigenfunctions[:, k])
        u0 += np.sqrt(eigenvalues[k]) * phi * xi_samples[:, k]
    return u0


def solve_rd_reference(a, b, x_eval, t_eval, u0, nx_fine=201, dt_fine=None):
    """Solve reaction-diffusion with Crank-Nicolson (implicit) for stability."""
    from scipy.linalg import solve_banded
    x_fine = np.linspace(0, 1, nx_fine)
    dx = x_fine[1] - x_fine[0]
    u = np.interp(x_fine, x_eval if len(x_eval) > 1 else [0, 1], 
                  u0 if len(u0) > 1 else [u0[0], u0[0]])
    
    if dt_fine is None:
        dt_fine = 0.5 * dx**2 / (a + 1e-10)  # CFL-safe for explicit part
        dt_fine = min(dt_fine, 0.001)  # cap at 1e-3
    
    nt_steps = max(int(t_eval / dt_fine), 1)
    dt = t_eval / nt_steps
    r = a * dt / (2.0 * dx**2)
    
    # Crank-Nicolson for diffusion, explicit for reaction
    n = nx_fine
    for _ in range(nt_steps):
        # Reaction at current time (explicit)
        react = b * u * (1 - u)
        # RHS: (I + r*A)*u + dt*reaction
        rhs = u.copy()
        rhs[1:-1] += r * (u[2:] - 2*u[1:-1] + u[:-2]) + dt * react[1:-1]
        rhs[0] += dt * react[0]
        rhs[-1] += dt * react[-1]
        
        # Solve (I - r*A)*u_new = rhs using tridiagonal solver
        # Build banded matrix [upper, diag, lower]
        ab = np.zeros((3, n))
        ab[0, 1:] = -r       # upper diagonal
        ab[1, :] = 1 + 2*r   # main diagonal
        ab[2, :-1] = -r      # lower diagonal
        # Neumann BC: du/dx=0 at boundaries
        ab[1, 0] = 1 + r     # modified for Neumann
        ab[1, -1] = 1 + r
        
        u = solve_banded((1, 1), ab, rhs)
        # Clip to prevent extreme values
        u = np.clip(u, -10, 10)
    
    return np.interp(x_eval, x_fine, u)


# =================== Forward Problem ===================
def train_forward(n_epochs=100000, save_dir='results'):
    """Forward problem: given a, b, compute u(x,t;ω) statistics."""
    os.makedirs(save_dir, exist_ok=True)
    
    eigenvalues, eigenfunctions, x_kl = compute_kl_expansion(N_KL, 200, SIGMA_KL, L_KL)
    print(f"KL eigenvalues (first 5): {eigenvalues[:5]}")
    print(f"Total energy: {np.sum(eigenvalues):.6f}")
    
    # Input: (x, t, xi_1, ..., xi_19) = 21 dims
    input_dim = 2 + N_KL
    net = ModifiedMLP(input_dim=input_dim, output_dim=1, n_layers=6, hidden_dim=160).to(device)
    
    n_params = sum(p.numel() for p in net.parameters())
    print(f"Forward net: {n_params:,} parameters, input_dim={input_dim}")
    
    opt = torch.optim.Adam(net.parameters(), lr=1e-3)
    sched = torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(opt, T_0=20000, eta_min=1e-6)
    
    n_pde = 8000
    n_ic = 2000
    n_bc = 500
    
    def make_points():
        x_p = torch.rand(n_pde, 1, device=device)
        t_p = torch.rand(n_pde, 1, device=device)
        xi_p = torch.randn(n_pde, N_KL, device=device)
        
        x_i = torch.rand(n_ic, 1, device=device)
        xi_i = torch.randn(n_ic, N_KL, device=device)
        
        t_b = torch.rand(n_bc, 1, device=device)
        xi_b = torch.randn(n_bc, N_KL, device=device)
        
        return x_p, t_p, xi_p, x_i, xi_i, t_b, xi_b
    
    def pde_loss(x, t, xi):
        x = x.detach().requires_grad_(True)
        t = t.detach().requires_grad_(True)
        inp = torch.cat([x, t, xi], dim=-1)
        u = net(inp)
        
        du_dt = torch.autograd.grad(u, t, torch.ones_like(u), create_graph=True)[0]
        du_dx = torch.autograd.grad(u, x, torch.ones_like(u), create_graph=True)[0]
        d2u_dx2 = torch.autograd.grad(du_dx, x, torch.ones_like(du_dx), create_graph=True)[0]
        
        res = du_dt - A_TRUE * d2u_dx2 - B_TRUE * u * (1 - u)
        return torch.mean(res**2)
    
    def ic_loss_fn(x, xi):
        t0 = torch.zeros_like(x)
        inp = torch.cat([x, t0, xi], dim=-1)
        u_pred = net(inp)
        
        # Compute IC values
        x_np = x.detach().cpu().numpy().flatten()
        xi_np = xi.detach().cpu().numpy()
        u0 = 0.5 * np.ones(len(x_np))
        for k in range(N_KL):
            phi = np.interp(x_np, x_kl, eigenfunctions[:, k])
            u0 += np.sqrt(eigenvalues[k]) * phi * xi_np[:, k]
        u_target = torch.tensor(u0, dtype=torch.float32, device=device).unsqueeze(1)
        return torch.mean((u_pred - u_target)**2)
    
    def bc_loss_fn(t, xi):
        # Neumann BC: du/dx = 0 at x=0,1
        x_left = torch.zeros_like(t).requires_grad_(True)
        x_right = torch.ones_like(t).requires_grad_(True)
        
        inp_l = torch.cat([x_left, t, xi], dim=-1)
        inp_r = torch.cat([x_right, t, xi], dim=-1)
        u_l = net(inp_l)
        u_r = net(inp_r)
        
        du_dx_l = torch.autograd.grad(u_l, x_left, torch.ones_like(u_l), create_graph=True)[0]
        du_dx_r = torch.autograd.grad(u_r, x_right, torch.ones_like(u_r), create_graph=True)[0]
        
        return torch.mean(du_dx_l**2) + torch.mean(du_dx_r**2)
    
    x_p, t_p, xi_p, x_i, xi_i, t_b, xi_b = make_points()
    
    w_pde, w_ic, w_bc = 1.0, 100.0, 50.0
    best = float('inf')
    history = []
    t_start = time.time()
    
    print(f"\nTraining forward RD ({n_epochs} epochs)...")
    
    for ep in range(1, n_epochs+1):
        net.train()
        
        if ep % 5000 == 0:
            x_p, t_p, xi_p, x_i, xi_i, t_b, xi_b = make_points()
        
        opt.zero_grad()
        L_pde = pde_loss(x_p, t_p, xi_p)
        L_ic = ic_loss_fn(x_i, xi_i)
        L_bc = bc_loss_fn(t_b, xi_b)
        
        loss = w_pde * L_pde + w_ic * L_ic + w_bc * L_bc
        loss.backward()
        torch.nn.utils.clip_grad_norm_(net.parameters(), 1.0)
        opt.step()
        sched.step()
        
        if loss.item() < best:
            best = loss.item()
            torch.save(net.state_dict(), f'{save_dir}/best_rd_forward.pt')
        
        if ep % 2000 == 0:
            if L_ic.item() > 1e-4:
                w_ic = min(w_ic * 1.05, 500)
        
        if ep % 10000 == 0:
            dt_elapsed = time.time() - t_start
            print(f"  Ep{ep:6d} | L={loss.item():.2e} PDE={L_pde.item():.2e} "
                  f"IC={L_ic.item():.2e} BC={L_bc.item():.2e} | {dt_elapsed:.0f}s")
            history.append({
                'ep': ep, 'loss': loss.item(),
                'pde': L_pde.item(), 'ic': L_ic.item(), 'bc': L_bc.item(),
                'time': dt_elapsed
            })
    
    # Load best and evaluate
    net.load_state_dict(torch.load(f'{save_dir}/best_rd_forward.pt', weights_only=True))
    
    print(f"\n{'='*50}")
    print("Forward RD: MC evaluation at t=1.0")
    print(f"{'='*50}")
    
    net.eval()
    x_eval = np.linspace(0, 1, 200)
    n_mc = 5000
    u_mc = np.zeros((len(x_eval), n_mc))
    
    with torch.no_grad():
        x_t = torch.tensor(x_eval, dtype=torch.float32, device=device).unsqueeze(1)
        t_t = torch.ones(len(x_eval), 1, device=device)
        
        for j in range(n_mc):
            xi_j = torch.randn(1, N_KL, device=device).expand(len(x_eval), -1)
            inp = torch.cat([x_t, t_t, xi_j], dim=-1)
            u_mc[:, j] = net(inp).cpu().numpy().flatten()
    
    E_u = np.mean(u_mc, axis=1)
    Var_u = np.var(u_mc, axis=1)
    
    print(f"  E[u] range: [{E_u.min():.4f}, {E_u.max():.4f}]")
    print(f"  Var[u] range: [{Var_u.min():.6f}, {Var_u.max():.6f}]")
    
    # Generate FD reference for comparison
    print("\nGenerating FD reference...")
    n_ref = 2000
    u_ref = np.zeros((len(x_eval), n_ref))
    for j in range(n_ref):
        xi = np.random.randn(1, N_KL)
        u0 = generate_ic(x_eval, np.tile(xi, (len(x_eval), 1)), eigenvalues, eigenfunctions, x_kl)
        u_ref[:, j] = solve_rd_reference(A_TRUE, B_TRUE, x_eval, 1.0, u0)
    
    # Filter out NaN columns (unstable FD samples)
    valid_cols = ~np.any(np.isnan(u_ref), axis=0)
    if valid_cols.sum() < n_ref:
        print(f"  Warning: {n_ref - valid_cols.sum()}/{n_ref} FD reference samples had NaN, filtered out")
    u_ref = u_ref[:, valid_cols]
    E_ref = np.mean(u_ref, axis=1)
    Var_ref = np.var(u_ref, axis=1)
    
    dx = x_eval[1] - x_eval[0]
    rel_E = np.sqrt(np.sum((E_u - E_ref)**2)*dx) / np.sqrt(np.sum(E_ref**2)*dx) * 100
    rel_V = np.sqrt(np.sum((Var_u - Var_ref)**2)*dx) / max(np.sqrt(np.sum(Var_ref**2)*dx), 1e-15) * 100
    
    print(f"  E[u] rel L2 vs FD ref: {rel_E:.4f}%")
    print(f"  Var[u] rel L2 vs FD ref: {rel_V:.4f}%")
    
    forward_results = {
        'E_relL2_vs_FD': float(rel_E),
        'Var_relL2_vs_FD': float(rel_V),
        'wall_time': time.time() - t_start,
    }
    
    return net, eigenvalues, eigenfunctions, x_kl, forward_results, history


# =================== Inverse Problem ===================
def train_inverse(n_epochs=100000, save_dir='results'):
    """Inverse problem: recover a, b from data."""
    os.makedirs(save_dir, exist_ok=True)
    
    eigenvalues, eigenfunctions, x_kl = compute_kl_expansion(N_KL, 200, SIGMA_KL, L_KL)
    
    # Generate "observation" data using FD solver with true a, b
    print("\nGenerating observation data with true a, b...")
    n_obs = 200
    x_obs_pts = np.random.rand(n_obs)
    t_obs_pts = np.random.rand(n_obs)
    xi_obs = np.random.randn(n_obs, N_KL)
    
    u_obs_vals = np.zeros(n_obs)
    for i in range(n_obs):
        x_fine = np.linspace(0, 1, 201)
        u0 = generate_ic(x_fine, xi_obs[i:i+1].repeat(201, axis=0), eigenvalues, eigenfunctions, x_kl)
        u_solved = solve_rd_reference(A_TRUE, B_TRUE, x_fine, t_obs_pts[i], u0)
        u_obs_vals[i] = np.interp(x_obs_pts[i], x_fine, u_solved)
    
    # Filter out NaN observations
    valid = ~np.isnan(u_obs_vals)
    if valid.sum() < n_obs:
        print(f"  Warning: {n_obs - valid.sum()} NaN observations filtered out")
        x_obs_pts = x_obs_pts[valid]
        t_obs_pts = t_obs_pts[valid]
        xi_obs = xi_obs[valid]
        u_obs_vals = u_obs_vals[valid]
        n_obs = len(u_obs_vals)
    print(f"Generated {n_obs} valid observations. u range: [{u_obs_vals.min():.4f}, {u_obs_vals.max():.4f}]")
    
    # Network + learnable parameters
    input_dim = 2 + N_KL
    net = ModifiedMLP(input_dim=input_dim, output_dim=1, n_layers=6, hidden_dim=160).to(device)
    
    # Learnable PDE parameters
    log_a = nn.Parameter(torch.tensor(0.0, device=device))  # init a=1.0
    log_b = nn.Parameter(torch.tensor(0.0, device=device))  # init b=1.0
    
    all_params = list(net.parameters()) + [log_a, log_b]
    opt = torch.optim.Adam(all_params, lr=1e-3)
    sched = torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(opt, T_0=20000, eta_min=1e-6)
    
    # Convert obs to tensors
    x_obs_t = torch.tensor(x_obs_pts, dtype=torch.float32, device=device).unsqueeze(1)
    t_obs_t = torch.tensor(t_obs_pts, dtype=torch.float32, device=device).unsqueeze(1)
    xi_obs_t = torch.tensor(xi_obs, dtype=torch.float32, device=device)
    u_obs_t = torch.tensor(u_obs_vals, dtype=torch.float32, device=device).unsqueeze(1)
    
    n_pde = 5000
    best = float('inf')
    history = []
    t_start = time.time()
    
    print(f"\nTraining inverse RD ({n_epochs} epochs)...")
    
    for ep in range(1, n_epochs+1):
        net.train()
        
        a_val = torch.exp(log_a)
        b_val = torch.exp(log_b)
        
        # PDE collocation
        x_p = torch.rand(n_pde, 1, device=device)
        t_p = torch.rand(n_pde, 1, device=device)
        xi_p = torch.randn(n_pde, N_KL, device=device)
        
        x_p = x_p.detach().requires_grad_(True)
        t_p = t_p.detach().requires_grad_(True)
        inp = torch.cat([x_p, t_p, xi_p], dim=-1)
        u = net(inp)
        
        du_dt = torch.autograd.grad(u, t_p, torch.ones_like(u), create_graph=True)[0]
        du_dx = torch.autograd.grad(u, x_p, torch.ones_like(u), create_graph=True)[0]
        d2u_dx2 = torch.autograd.grad(du_dx, x_p, torch.ones_like(du_dx), create_graph=True)[0]
        
        res = du_dt - a_val * d2u_dx2 - b_val * u * (1 - u)
        L_pde = torch.mean(res**2)
        
        # Data loss
        u_pred_obs = net(torch.cat([x_obs_t, t_obs_t, xi_obs_t], dim=-1))
        L_data = torch.mean((u_pred_obs - u_obs_t)**2)
        
        # IC loss (a few points)
        n_ic_inv = 500
        x_ic = torch.rand(n_ic_inv, 1, device=device)
        xi_ic = torch.randn(n_ic_inv, N_KL, device=device)
        t0 = torch.zeros_like(x_ic)
        u_ic_pred = net(torch.cat([x_ic, t0, xi_ic], dim=-1))
        
        x_ic_np = x_ic.detach().cpu().numpy().flatten()
        xi_ic_np = xi_ic.detach().cpu().numpy()
        u0_vals = 0.5 * np.ones(n_ic_inv)
        for k in range(N_KL):
            phi = np.interp(x_ic_np, x_kl, eigenfunctions[:, k])
            u0_vals += np.sqrt(eigenvalues[k]) * phi * xi_ic_np[:, k]
        u_ic_target = torch.tensor(u0_vals, dtype=torch.float32, device=device).unsqueeze(1)
        L_ic = torch.mean((u_ic_pred - u_ic_target)**2)
        
        loss = L_pde + 100 * L_data + 100 * L_ic
        
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(all_params, 1.0)
        opt.step()
        sched.step()
        
        if loss.item() < best:
            best = loss.item()
            torch.save({
                'net': net.state_dict(),
                'log_a': log_a.item(),
                'log_b': log_b.item()
            }, f'{save_dir}/best_rd_inverse.pt')
        
        if ep % 10000 == 0:
            dt_elapsed = time.time() - t_start
            a_est = torch.exp(log_a).item()
            b_est = torch.exp(log_b).item()
            print(f"  Ep{ep:6d} | L={loss.item():.2e} PDE={L_pde.item():.2e} "
                  f"Data={L_data.item():.2e} IC={L_ic.item():.2e} | "
                  f"a={a_est:.4f} (true={A_TRUE}) b={b_est:.4f} (true={B_TRUE}) | {dt_elapsed:.0f}s")
            history.append({
                'ep': ep, 'loss': loss.item(),
                'a_est': a_est, 'b_est': b_est,
                'a_err': abs(a_est - A_TRUE)/A_TRUE * 100,
                'b_err': abs(b_est - B_TRUE)/B_TRUE * 100,
                'time': dt_elapsed
            })
    
    # Load best
    ckpt = torch.load(f'{save_dir}/best_rd_inverse.pt', weights_only=True)
    a_final = np.exp(ckpt['log_a'])
    b_final = np.exp(ckpt['log_b'])
    
    print(f"\n{'='*50}")
    print("Inverse RD Results")
    print(f"{'='*50}")
    print(f"  a estimated: {a_final:.6f} (true: {A_TRUE}, err: {abs(a_final-A_TRUE)/A_TRUE*100:.2f}%)")
    print(f"  b estimated: {b_final:.6f} (true: {B_TRUE}, err: {abs(b_final-B_TRUE)/B_TRUE*100:.2f}%)")
    
    inverse_results = {
        'a_est': float(a_final),
        'b_est': float(b_final),
        'a_true': A_TRUE,
        'b_true': B_TRUE,
        'a_rel_err': float(abs(a_final - A_TRUE) / A_TRUE * 100),
        'b_rel_err': float(abs(b_final - B_TRUE) / B_TRUE * 100),
        'wall_time': time.time() - t_start,
    }
    
    return inverse_results, history


def train_all(save_dir='results'):
    os.makedirs(save_dir, exist_ok=True)
    
    t0 = time.time()
    
    print("="*60)
    print("EXAMPLE 3: Stochastic Reaction-Diffusion")
    print("="*60)
    
    # Forward problem
    print("\n--- Forward Problem ---")
    net, evals, efns, x_kl, fwd_results, fwd_history = train_forward(
        n_epochs=60000, save_dir=save_dir)
    
    # Inverse problem
    print("\n--- Inverse Problem ---")
    inv_results, inv_history = train_inverse(n_epochs=60000, save_dir=save_dir)
    
    total_time = time.time() - t0
    
    results = {
        'method': 'Parametric_PINN',
        'forward': fwd_results,
        'inverse': inv_results,
        'forward_history': fwd_history,
        'inverse_history': inv_history,
        'wall_time': total_time,
        'paper_claims': {
            'forward': 'Table 5 RMSE values',
            'inverse': 'a→0.5, b→0.3',
        }
    }
    
    with open(f'{save_dir}/example3_result.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nTotal wall time: {total_time:.0f}s")
    print(f"Results saved to {save_dir}/example3_result.json")
    return results


if __name__ == '__main__':
    train_all()
