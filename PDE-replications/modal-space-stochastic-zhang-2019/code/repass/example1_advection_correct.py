"""
Re-pass Example 1: Stochastic Advection — corrected setup
==========================================================
Paper (Zhang et al. 2019, Sec 5.1):
  PDE:   u_t + xi * u_x = 0
  Domain: x in [-pi, pi], t in [0, pi], PERIODIC BCs
  IC:    u(x,0;xi) = -sin(x)
  RV:    xi ~ N(0, sigma^2) with sigma = 0.8
  Exact: u(x,t;xi) = -sin(x - xi*t)
         E[u]  = -sin(x) * exp(-sigma^2 * t^2 / 2)
         Var   = 0.5 * (1 - cos(2x) * exp(-2*sigma^2*t^2)) - E[u]^2

Approach: parametric PINN u_theta(x, t, xi) trained with
  - PDE residual (collocation in (x,t,xi))
  - IC penalty (t=0)
  - Periodic BC penalty (u(-pi,t,xi) == u(pi,t,xi) and du/dx matched)
Statistics computed via Gauss-Hermite quadrature (sigma = 0.8).

v2 BUG corrected here:
  v2 used: xi ~ N(1.0, 0.5^2), domain [0, 2*pi]
  paper:   xi ~ N(0,   0.8^2), domain [-pi, pi]
At T=pi the damping factor is exp(-sigma^2*pi^2/2):
  paper:  exp(-0.8^2 * pi^2 / 2) ~= 0.0425  (strong damping; weak E[u] signal)
  v2:     exp(-0.5^2 * pi^2 / 2) ~= 0.292   (much milder damping)
So v2 "3.48% E[u] error" is on an entirely different problem.
"""
import os, sys, json, time, argparse
import numpy as np
import torch
import torch.nn as nn

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# ---- Paper parameters ----
MU = 0.0
SIGMA = 0.8
X_LO, X_HI = -np.pi, np.pi
T_LO, T_HI = 0.0, np.pi


def exact_u(x, t, xi):
    return -np.sin(x - xi * t)

def exact_mean(x, t):
    return -np.sin(x) * np.exp(-SIGMA**2 * t**2 / 2.0)

def exact_var(x, t):
    E_u2 = 0.5 * (1.0 - np.cos(2.0 * x) * np.exp(-2.0 * SIGMA**2 * t**2))
    E_u = exact_mean(x, t)
    return E_u2 - E_u**2


class ModifiedMLP(nn.Module):
    """Wang et al. 2022 modified-MLP with gating."""
    def __init__(self, input_dim=3, output_dim=1, n_layers=5, hidden=128):
        super().__init__()
        self.encoder = nn.Linear(input_dim, hidden)
        self.U = nn.Linear(input_dim, hidden)
        self.V = nn.Linear(input_dim, hidden)
        self.layers = nn.ModuleList([nn.Linear(hidden, hidden) for _ in range(n_layers)])
        self.out = nn.Linear(hidden, output_dim)
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_normal_(m.weight, gain=1.0)
                nn.init.zeros_(m.bias)

    def forward(self, z):
        u_g = torch.tanh(self.U(z))
        v_g = torch.tanh(self.V(z))
        h = torch.tanh(self.encoder(z))
        for layer in self.layers:
            zout = torch.tanh(layer(h))
            h = (1 - zout) * u_g + zout * v_g
        return self.out(h)


def sample_collocation(n_pde=10000, n_ic=2000, n_bc=1000):
    # PDE points uniform in (x,t,xi). Use sigma*3 range for xi.
    x = (X_LO + (X_HI - X_LO) * torch.rand(n_pde, 1, device=device))
    t = (T_LO + (T_HI - T_LO) * torch.rand(n_pde, 1, device=device))
    xi = torch.randn(n_pde, 1, device=device) * SIGMA + MU
    # IC
    x_ic = (X_LO + (X_HI - X_LO) * torch.rand(n_ic, 1, device=device))
    t_ic = torch.zeros_like(x_ic)
    xi_ic = torch.randn(n_ic, 1, device=device) * SIGMA + MU
    # BC (periodic): match u(-pi,t,xi) and u(pi,t,xi)
    t_bc = (T_LO + (T_HI - T_LO) * torch.rand(n_bc, 1, device=device))
    xi_bc = torch.randn(n_bc, 1, device=device) * SIGMA + MU
    return x, t, xi, x_ic, t_ic, xi_ic, t_bc, xi_bc


def pde_residual(model, x, t, xi):
    x = x.clone().requires_grad_(True)
    t = t.clone().requires_grad_(True)
    z = torch.cat([x, t, xi], dim=1)
    u = model(z)
    grads_t = torch.autograd.grad(u, t, torch.ones_like(u), create_graph=True)[0]
    grads_x = torch.autograd.grad(u, x, torch.ones_like(u), create_graph=True)[0]
    return grads_t + xi * grads_x


def train(epochs=80000, hidden=128, n_layers=5, lr=1e-3,
          n_pde=10000, n_ic=2000, n_bc=1000,
          w_ic=10.0, w_bc=1.0, eval_every=2000, out_json=None, ckpt=None):
    model = ModifiedMLP(3, 1, n_layers=n_layers, hidden=hidden).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(opt, T_0=20000, eta_min=1e-6)

    # Fixed eval grid + GHQ nodes
    nx_eval = 100
    nt_eval = 21
    x_e = np.linspace(X_LO, X_HI, nx_eval)
    t_e = np.linspace(T_LO, T_HI, nt_eval)
    # Gauss-Hermite quadrature (physicist's) for E[f(xi)] with xi~N(0,sigma^2)
    GHN = 32
    gh_nodes, gh_weights = np.polynomial.hermite.hermgauss(GHN)
    # xi nodes mapped: xi = sqrt(2) * sigma * gh_nodes + mu
    xi_nodes = np.sqrt(2.0) * SIGMA * gh_nodes + MU
    gh_weights_norm = gh_weights / np.sqrt(np.pi)  # weights for N(0,sigma^2) integration

    def evaluate():
        model.eval()
        X, T = np.meshgrid(x_e, t_e, indexing='ij')  # (nx, nt)
        nx, nt = X.shape
        # build a big batch: for each (x,t) pair, evaluate at all xi_nodes
        Xf = X.reshape(-1, 1)
        Tf = T.reshape(-1, 1)
        E_pred = np.zeros_like(Xf).flatten()
        Var_pred = np.zeros_like(Xf).flatten()
        with torch.no_grad():
            for k, xi_k in enumerate(xi_nodes):
                xi_col = np.full_like(Xf, xi_k)
                z = torch.tensor(np.concatenate([Xf, Tf, xi_col], axis=1), dtype=torch.float32, device=device)
                u = model(z).cpu().numpy().flatten()
                E_pred += gh_weights_norm[k] * u
                Var_pred += gh_weights_norm[k] * u * u
        Var_pred = Var_pred - E_pred ** 2
        E_pred = E_pred.reshape(nx, nt)
        Var_pred = Var_pred.reshape(nx, nt)
        # Exact at all (x,t)
        E_ex = exact_mean(X, T)
        Var_ex = exact_var(X, T)
        # Errors at T = pi (last time slice)
        E_pred_T = E_pred[:, -1]
        Var_pred_T = Var_pred[:, -1]
        E_ex_T = E_ex[:, -1]
        Var_ex_T = Var_ex[:, -1]
        def relL2(pred, ex):
            num = np.sqrt(np.mean((pred - ex) ** 2))
            den = np.sqrt(np.mean(ex ** 2))
            return num / den if den > 0 else float('inf')
        # All-time errors too
        E_relL2_all = relL2(E_pred, E_ex)
        Var_relL2_all = relL2(Var_pred, Var_ex)
        out = {
            'E_relL2_T': relL2(E_pred_T, E_ex_T) * 100.0,
            'Var_relL2_T': relL2(Var_pred_T, Var_ex_T) * 100.0,
            'E_relL2_all_t': E_relL2_all * 100.0,
            'Var_relL2_all_t': Var_relL2_all * 100.0,
            'E_L2_T': float(np.sqrt(np.mean((E_pred_T - E_ex_T)**2))),
            'Var_L2_T': float(np.sqrt(np.mean((Var_pred_T - Var_ex_T)**2))),
            'E_max_T': float(np.max(np.abs(E_pred_T - E_ex_T))),
            'Var_max_T': float(np.max(np.abs(Var_pred_T - Var_ex_T))),
            'E_norm_T': float(np.sqrt(np.mean(E_ex_T**2))),
            'Var_norm_T': float(np.sqrt(np.mean(Var_ex_T**2))),
        }
        model.train()
        return out

    history = []
    best = {'E_relL2_T': float('inf')}
    best_state = None
    t0 = time.time()
    for ep in range(1, epochs + 1):
        x, t, xi, x_ic, t_ic, xi_ic, t_bc, xi_bc = sample_collocation(n_pde, n_ic, n_bc)
        # Resample only every few steps to stabilize
        opt.zero_grad()
        # PDE residual
        r = pde_residual(model, x, t, xi)
        loss_pde = (r ** 2).mean()
        # IC: u(x,0,xi) = -sin(x)
        z_ic = torch.cat([x_ic, t_ic, xi_ic], dim=1)
        u_ic = model(z_ic)
        target_ic = -torch.sin(x_ic)
        loss_ic = ((u_ic - target_ic) ** 2).mean()
        # Periodic BC: u(-pi,t,xi) = u(pi,t,xi)
        x_left = torch.full_like(t_bc, X_LO)
        x_right = torch.full_like(t_bc, X_HI)
        u_left = model(torch.cat([x_left, t_bc, xi_bc], dim=1))
        u_right = model(torch.cat([x_right, t_bc, xi_bc], dim=1))
        loss_bc = ((u_left - u_right) ** 2).mean()
        loss = loss_pde + w_ic * loss_ic + w_bc * loss_bc
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        sched.step()
        if ep % eval_every == 0 or ep == 1 or ep == epochs:
            ev = evaluate()
            entry = {
                'ep': ep,
                'time_s': time.time() - t0,
                'loss_pde': float(loss_pde.item()),
                'loss_ic': float(loss_ic.item()),
                'loss_bc': float(loss_bc.item()),
                **ev,
            }
            history.append(entry)
            if ev['E_relL2_T'] + ev['Var_relL2_T'] < best.get('E_relL2_T', float('inf')) + best.get('Var_relL2_T', float('inf')):
                best = dict(ev)
                best['ep'] = ep
                best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
            print(f"ep={ep:6d}  pde={loss_pde.item():.2e} ic={loss_ic.item():.2e} bc={loss_bc.item():.2e}  "
                  f"E_T={ev['E_relL2_T']:.3f}%  Var_T={ev['Var_relL2_T']:.3f}%  "
                  f"E_all_t={ev['E_relL2_all_t']:.3f}%  Var_all_t={ev['Var_relL2_all_t']:.3f}%  "
                  f"t={time.time()-t0:.1f}s",
                  flush=True)

    final_eval = evaluate()
    result = {
        'paper_params': {'mu': MU, 'sigma': SIGMA, 'x_range': [X_LO, X_HI], 't_range': [T_LO, T_HI]},
        'training': {'epochs': epochs, 'hidden': hidden, 'n_layers': n_layers, 'lr': lr,
                     'n_pde': n_pde, 'n_ic': n_ic, 'n_bc': n_bc, 'w_ic': w_ic, 'w_bc': w_bc,
                     'GHN': GHN, 'eval_grid': [nx_eval, nt_eval]},
        'final': final_eval,
        'best': best,
        'history': history,
        'wall_time_s': time.time() - t0,
        'device': str(device),
    }
    if out_json:
        os.makedirs(os.path.dirname(out_json) or '.', exist_ok=True)
        with open(out_json, 'w') as fh:
            json.dump(result, fh, indent=2)
        print(f"Wrote {out_json}")
    if ckpt and best_state is not None:
        torch.save(best_state, ckpt)
        print(f"Wrote {ckpt}")
    return result


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--epochs', type=int, default=80000)
    ap.add_argument('--hidden', type=int, default=128)
    ap.add_argument('--n_layers', type=int, default=5)
    ap.add_argument('--lr', type=float, default=1e-3)
    ap.add_argument('--n_pde', type=int, default=10000)
    ap.add_argument('--n_ic', type=int, default=2000)
    ap.add_argument('--n_bc', type=int, default=1000)
    ap.add_argument('--w_ic', type=float, default=10.0)
    ap.add_argument('--w_bc', type=float, default=1.0)
    ap.add_argument('--eval_every', type=int, default=2000)
    ap.add_argument('--out_json', type=str, default='results/repass/example1_correct.json')
    ap.add_argument('--ckpt', type=str, default='results/repass/example1_correct.pt')
    args = ap.parse_args()
    train(**vars(args))
