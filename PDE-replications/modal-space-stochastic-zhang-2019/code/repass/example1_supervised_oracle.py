"""
Example 1 supervised oracle fit (paper parameters)
===================================================
Train a parametric MLP u_theta(x, t, xi) to match the EXACT advection
solution u(x,t;xi) = -sin(x - xi t) on a dense grid, then compute
E[u], Var[u] via Gauss-Hermite quadrature with sigma = 0.8.

Purpose: sanity-check the eval pipeline and provide a "training-difficulty-free"
upper bound on the accuracy achievable with our network + GHQ.

If this gives sub-1% E[u] and Var[u], then any remaining gap in the PINN run
is due to training/optimization, not setup or eval bugs.
"""
import os, json, time, argparse
import numpy as np
import torch
import torch.nn as nn

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

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


def train(epochs=40000, batch=8192, hidden=128, n_layers=5, lr=1e-3,
          out_json='results/repass/example1_oracle.json'):
    model = ModifiedMLP(3, 1, n_layers=n_layers, hidden=hidden).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(opt, T_0=10000, eta_min=1e-6)

    nx_eval, nt_eval = 100, 21
    x_e = np.linspace(X_LO, X_HI, nx_eval)
    t_e = np.linspace(T_LO, T_HI, nt_eval)
    GHN = 32
    gh_nodes, gh_weights = np.polynomial.hermite.hermgauss(GHN)
    xi_nodes = np.sqrt(2.0) * SIGMA * gh_nodes + MU
    gh_weights_norm = gh_weights / np.sqrt(np.pi)

    def evaluate():
        model.eval()
        X, T = np.meshgrid(x_e, t_e, indexing='ij')
        Xf, Tf = X.reshape(-1, 1), T.reshape(-1, 1)
        E_pred = np.zeros_like(Xf).flatten()
        Var_pred = np.zeros_like(Xf).flatten()
        with torch.no_grad():
            for k, xi_k in enumerate(xi_nodes):
                xi_col = np.full_like(Xf, xi_k)
                z = torch.tensor(np.concatenate([Xf, Tf, xi_col], axis=1),
                                 dtype=torch.float32, device=device)
                u = model(z).cpu().numpy().flatten()
                E_pred += gh_weights_norm[k] * u
                Var_pred += gh_weights_norm[k] * u * u
        Var_pred = Var_pred - E_pred ** 2
        E_pred = E_pred.reshape(*X.shape)
        Var_pred = Var_pred.reshape(*X.shape)
        E_ex, Var_ex = exact_mean(X, T), exact_var(X, T)
        def relL2(p, e):
            return np.sqrt(np.mean((p - e) ** 2)) / np.sqrt(np.mean(e ** 2))
        out = {
            'E_relL2_T': relL2(E_pred[:, -1], E_ex[:, -1]) * 100,
            'Var_relL2_T': relL2(Var_pred[:, -1], Var_ex[:, -1]) * 100,
            'E_relL2_all_t': relL2(E_pred, E_ex) * 100,
            'Var_relL2_all_t': relL2(Var_pred, Var_ex) * 100,
        }
        model.train()
        return out

    history = []
    t0 = time.time()
    for ep in range(1, epochs + 1):
        x = X_LO + (X_HI - X_LO) * torch.rand(batch, 1, device=device)
        t = T_LO + (T_HI - T_LO) * torch.rand(batch, 1, device=device)
        xi = torch.randn(batch, 1, device=device) * SIGMA + MU
        z = torch.cat([x, t, xi], dim=1)
        target = -torch.sin(x - xi * t)
        u = model(z)
        loss = ((u - target) ** 2).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
        if ep % 2000 == 0 or ep == 1:
            ev = evaluate()
            history.append({'ep': ep, 'loss': float(loss.item()), 'time_s': time.time() - t0, **ev})
            print(f"ep={ep:6d}  loss={loss.item():.3e}  E_T={ev['E_relL2_T']:.3f}%  Var_T={ev['Var_relL2_T']:.3f}%  "
                  f"E_all={ev['E_relL2_all_t']:.3f}%  Var_all={ev['Var_relL2_all_t']:.3f}%  t={time.time()-t0:.1f}s",
                  flush=True)
    final = evaluate()
    out = {'paper_params': {'mu': MU, 'sigma': SIGMA},
           'training': {'epochs': epochs, 'batch': batch, 'hidden': hidden, 'n_layers': n_layers},
           'final': final, 'history': history, 'wall_time_s': time.time() - t0}
    os.makedirs(os.path.dirname(out_json) or '.', exist_ok=True)
    with open(out_json, 'w') as fh:
        json.dump(out, fh, indent=2)
    print(f"Wrote {out_json}")
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--epochs', type=int, default=40000)
    ap.add_argument('--batch', type=int, default=8192)
    ap.add_argument('--hidden', type=int, default=128)
    ap.add_argument('--n_layers', type=int, default=5)
    ap.add_argument('--lr', type=float, default=1e-3)
    ap.add_argument('--out_json', type=str, default='results/repass/example1_oracle.json')
    args = ap.parse_args()
    train(**vars(args))
