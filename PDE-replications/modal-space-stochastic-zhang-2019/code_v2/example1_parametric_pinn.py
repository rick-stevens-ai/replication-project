"""
Example 1: Stochastic Advection — Parametric PINN
==================================================
Treat xi as an extra input dimension: u_NN(x, t, xi) ≈ u(x, t; xi)
Then compute E[u] and Var[u] by Gauss-Hermite quadrature over xi.

This avoids the modal decomposition entirely (no gauge issues).

PDE: du/dt + xi * du/dx = 0, x ∈ [0, 2π], t ∈ [0, π]
IC: u(x, 0; xi) = -sin(x), xi ~ N(1, 0.5²)
Exact: u(x,t;xi) = -sin(x - xi*t)
"""
import os, sys, json, time
import numpy as np
import torch
import torch.nn as nn
from scipy.stats import norm

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Device: {device}")

MU = 1.0
SIGMA = 0.5
X_RANGE = (0, 2*np.pi)
T_RANGE = (0, np.pi)


def exact_mean(x, t):
    return -np.sin(x - MU*t) * np.exp(-SIGMA**2 * t**2 / 2)

def exact_variance(x, t):
    E_u2 = 0.5 * (1 - np.cos(2*(x - MU*t)) * np.exp(-2*SIGMA**2*t**2))
    E_u = exact_mean(x, t)
    return E_u2 - E_u**2


class ModifiedMLP(nn.Module):
    """Modified MLP with residual connections (Wang et al. 2022 style)."""
    def __init__(self, input_dim=3, output_dim=1, n_layers=5, hidden_dim=128):
        super().__init__()
        self.encoder = nn.Linear(input_dim, hidden_dim)
        self.U = nn.Linear(input_dim, hidden_dim)
        self.V = nn.Linear(input_dim, hidden_dim)
        self.layers = nn.ModuleList([nn.Linear(hidden_dim, hidden_dim) for _ in range(n_layers)])
        self.out = nn.Linear(hidden_dim, output_dim)
        self._init()

    def _init(self):
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


class FourierNet(nn.Module):
    """Network with random Fourier feature encoding."""
    def __init__(self, input_dim=3, output_dim=1, n_layers=5, hidden_dim=128,
                 n_freq=64, sigma_freq=2.0):
        super().__init__()
        B = torch.randn(input_dim, n_freq) * sigma_freq
        self.register_buffer('B', B)
        
        ff_dim = 2 * n_freq
        layers = []
        prev = ff_dim
        for _ in range(n_layers):
            layers.extend([nn.Linear(prev, hidden_dim), nn.Tanh()])
            prev = hidden_dim
        layers.append(nn.Linear(prev, output_dim))
        self.mlp = nn.Sequential(*layers)
        for m in self.mlp:
            if isinstance(m, nn.Linear):
                nn.init.xavier_normal_(m.weight, gain=1.0)
                nn.init.zeros_(m.bias)

    def forward(self, x):
        proj = 2 * np.pi * x @ self.B
        ff = torch.cat([torch.sin(proj), torch.cos(proj)], dim=-1)
        return self.mlp(ff)


def make_points(n_pde=10000, n_ic=2000, n_bc=1000):
    """Generate training points."""
    x_pde = torch.rand(n_pde, 1, device=device) * 2 * np.pi
    t_pde = torch.rand(n_pde, 1, device=device) * np.pi
    # Better xi sampling: stratified inverse CDF
    u_samp = (torch.arange(n_pde, device=device, dtype=torch.float32) + 
              torch.rand(n_pde, device=device)) / n_pde
    u_samp = torch.clamp(u_samp, 0.001, 0.999).unsqueeze(1)
    xi_pde = torch.tensor(norm.ppf(u_samp.cpu().numpy(), loc=MU, scale=SIGMA),
                           dtype=torch.float32, device=device)

    x_ic = torch.rand(n_ic, 1, device=device) * 2 * np.pi
    u_ic = torch.rand(n_ic, 1, device=device) * 0.998 + 0.001
    xi_ic = torch.tensor(norm.ppf(u_ic.cpu().numpy(), loc=MU, scale=SIGMA),
                          dtype=torch.float32, device=device)

    t_bc = torch.rand(n_bc, 1, device=device) * np.pi
    u_bc = torch.rand(n_bc, 1, device=device) * 0.998 + 0.001
    xi_bc = torch.tensor(norm.ppf(u_bc.cpu().numpy(), loc=MU, scale=SIGMA),
                          dtype=torch.float32, device=device)
    
    return x_pde, t_pde, xi_pde, x_ic, xi_ic, t_bc, t_bc, xi_bc


def compute_loss(net, x_pde, t_pde, xi_pde, x_ic, xi_ic, x_bc, t_bc, xi_bc,
                 w_pde=1.0, w_ic=100.0, w_bc=50.0):
    """PDE + IC + BC loss."""
    # PDE residual
    x = x_pde.detach().requires_grad_(True)
    t = t_pde.detach().requires_grad_(True)
    xi = xi_pde.detach()  # xi is a parameter, not differentiated
    
    inp = torch.cat([x, t, xi], dim=-1)
    u = net(inp)
    du_dt = torch.autograd.grad(u, t, torch.ones_like(u), create_graph=True)[0]
    du_dx = torch.autograd.grad(u, x, torch.ones_like(u), create_graph=True)[0]
    res = du_dt + xi * du_dx
    loss_pde = torch.mean(res**2)

    # IC: u(x, 0, xi) = -sin(x)
    t0 = torch.zeros_like(x_ic)
    u_ic_pred = net(torch.cat([x_ic, t0, xi_ic], dim=-1))
    loss_ic = torch.mean((u_ic_pred - (-torch.sin(x_ic)))**2)

    # BC: periodic
    u_left = net(torch.cat([torch.zeros_like(t_bc), t_bc, xi_bc], dim=-1))
    u_right = net(torch.cat([torch.full_like(t_bc, 2*np.pi), t_bc, xi_bc], dim=-1))
    loss_bc = torch.mean((u_left - u_right)**2)

    total = w_pde * loss_pde + w_ic * loss_ic + w_bc * loss_bc
    return total, {'pde': loss_pde.item(), 'ic': loss_ic.item(), 'bc': loss_bc.item()}


def eval_statistics(net, x_eval, t_val, n_quad=200):
    """Gauss-Hermite quadrature over xi for E[u] and Var[u] — BATCHED."""
    net.eval()
    gh_nodes, gh_weights = np.polynomial.hermite_e.hermegauss(n_quad)
    xi_q = MU + SIGMA * gh_nodes
    w_q = gh_weights / np.sqrt(2 * np.pi)

    nx = len(x_eval)
    
    with torch.no_grad():
        # Batch all (x, t, xi) combinations: shape (nx * n_quad, 3)
        x_rep = torch.tensor(x_eval, dtype=torch.float32, device=device).unsqueeze(1).repeat(n_quad, 1)  # (nx*n_quad, 1)
        t_rep = torch.full((nx * n_quad, 1), t_val, dtype=torch.float32, device=device)
        xi_rep = torch.tensor(np.repeat(xi_q, nx), dtype=torch.float32, device=device).unsqueeze(1)  # (nx*n_quad, 1)
        
        # Process in chunks to avoid OOM
        chunk = 50000
        u_all = []
        for start in range(0, nx * n_quad, chunk):
            end = min(start + chunk, nx * n_quad)
            inp = torch.cat([x_rep[start:end], t_rep[start:end], xi_rep[start:end]], dim=-1)
            u_all.append(net(inp).cpu().numpy().flatten())
        u_all = np.concatenate(u_all)  # (nx * n_quad,)
        
        # Reshape to (n_quad, nx)
        u_grid = u_all.reshape(n_quad, nx)
        w_arr = np.array(w_q).reshape(-1, 1)  # (n_quad, 1)
        
        E_u = np.sum(w_arr * u_grid, axis=0)
        E_u2 = np.sum(w_arr * u_grid**2, axis=0)

    Var_u = E_u2 - E_u**2
    return E_u, Var_u


def compute_errors(net, x_eval, t_val, n_quad=200):
    E_pred, Var_pred = eval_statistics(net, x_eval, t_val, n_quad)
    E_exact = exact_mean(x_eval, t_val)
    Var_exact = exact_variance(x_eval, t_val)
    dx = x_eval[1] - x_eval[0]
    
    norm_E = np.sqrt(np.sum(E_exact**2) * dx)
    norm_V = np.sqrt(np.sum(Var_exact**2) * dx)
    
    rel_E = np.sqrt(np.sum((E_pred - E_exact)**2) * dx) / max(norm_E, 1e-15) * 100
    rel_V = np.sqrt(np.sum((Var_pred - Var_exact)**2) * dx) / max(norm_V, 1e-15) * 100
    
    return {'E_relL2': float(rel_E), 'Var_relL2': float(rel_V),
            'E_max': float(np.max(np.abs(E_pred - E_exact))),
            'Var_max': float(np.max(np.abs(Var_pred - Var_exact)))}


def train(n_epochs=200000, net_type='modified_mlp', lr=1e-3, save_dir='results'):
    os.makedirs(save_dir, exist_ok=True)
    
    if net_type == 'fourier':
        net = FourierNet(input_dim=3, n_layers=5, hidden_dim=128, n_freq=64).to(device)
    else:
        net = ModifiedMLP(input_dim=3, n_layers=5, hidden_dim=128).to(device)

    opt = torch.optim.Adam(net.parameters(), lr=lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(opt, T_0=20000, T_mult=2, eta_min=1e-6)

    n_params = sum(p.numel() for p in net.parameters())
    print(f"\n{'='*70}")
    print(f"Parametric PINN ({net_type}), {n_params:,} params, {n_epochs} epochs")
    print(f"{'='*70}")

    x_pde, t_pde, xi_pde, x_ic, xi_ic, x_bc, t_bc, xi_bc = make_points(10000, 2000, 1000)
    
    history = []
    best = float('inf')
    t0 = time.time()

    # Adaptive loss weighting
    w_pde, w_ic, w_bc = 1.0, 100.0, 50.0

    for ep in range(1, n_epochs+1):
        net.train()
        
        if ep % 5000 == 0:
            x_pde, t_pde, xi_pde, x_ic, xi_ic, x_bc, t_bc, xi_bc = make_points(10000, 2000, 1000)

        opt.zero_grad()
        loss, ld = compute_loss(net, x_pde, t_pde, xi_pde, x_ic, xi_ic,
                                x_bc, t_bc, xi_bc, w_pde, w_ic, w_bc)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(net.parameters(), 1.0)
        opt.step()
        sched.step()

        if loss.item() < best:
            best = loss.item()
            torch.save(net.state_dict(), f'{save_dir}/best_ex1.pt')

        # Simple adaptive: if IC is not converged, boost it
        if ep % 2000 == 0:
            if ld['ic'] > 1e-4:
                w_ic = min(w_ic * 1.05, 500)
            if ld['bc'] > 1e-4:
                w_bc = min(w_bc * 1.05, 200)

        if ep % 5000 == 0:
            x_eval = np.linspace(0, 2*np.pi, 100)
            errs = compute_errors(net, x_eval, np.pi, 30)
            dt = time.time() - t0
            print(f"Ep {ep:6d} | Loss {loss.item():.2e} | PDE {ld['pde']:.2e} IC {ld['ic']:.2e} BC {ld['bc']:.2e} | "
                  f"E[u] {errs['E_relL2']:.3f}% Var[u] {errs['Var_relL2']:.3f}% | {dt:.0f}s")
            history.append({'ep': ep, **ld, **errs, 'time': dt})

    # Final eval
    net.load_state_dict(torch.load(f'{save_dir}/best_ex1.pt', weights_only=True))
    x_eval = np.linspace(0, 2*np.pi, 500)
    
    print(f"\n{'='*50}")
    print("FINAL RESULTS (T=π)")
    print(f"{'='*50}")
    final = compute_errors(net, x_eval, np.pi, 200)
    for k, v in final.items():
        print(f"  {k}: {v:.6f}{'%' if 'rel' in k else ''}")
    
    print("\nPaper targets (Table 1, NN-DO): E[u] 1.96%, Var[u] 0.11%")
    print(f"Paper targets (Table 1, NN-BO): E[u] 1.98%, Var[u] 0.13%")

    # Time evolution
    print("\nTime evolution of errors:")
    for t_val in [0.5, 1.0, 2.0, np.pi]:
        e = compute_errors(net, x_eval, t_val, 200)
        print(f"  t={t_val:.2f}: E[u]={e['E_relL2']:.4f}% Var[u]={e['Var_relL2']:.4f}%")

    results = {
        'method': f'Parametric_PINN_{net_type}',
        'final': final,
        'history': history,
        'wall_time': time.time() - t0,
        'n_epochs': n_epochs,
        'n_params': n_params,
        'paper_DO': {'E_relL2': 1.96, 'Var_relL2': 0.11},
        'paper_BO': {'E_relL2': 1.98, 'Var_relL2': 0.13},
    }
    with open(f'{save_dir}/example1_result.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved to {save_dir}/example1_result.json")
    return results


if __name__ == '__main__':
    nt = sys.argv[1] if len(sys.argv) > 1 else 'modified_mlp'
    ne = int(sys.argv[2]) if len(sys.argv) > 2 else 200000
    train(n_epochs=ne, net_type=nt)
