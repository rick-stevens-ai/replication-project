"""
Example 2: Stochastic Burgers Equation - NN-DO and NN-BO methods.
Zhang et al. 2019, Section 5.2.

PDE: du/dt + u*du/dx = nu * d2u/dx2 + f(x,t;w)
Domain: x in [-pi, pi], t in [0, 10*pi] (10 subdomains of length pi)
nu = 0.1
xi_1, xi_2 ~ U[0,1]

Exact solution (manufactured):
u(x,t;xi1,xi2) = -sin(x-t)
    - sqrt(3)*(1.5+sin(t))*cos(x-t)*(2*xi1-1)
    + sqrt(3)*(1.5+cos(3t))*cos(2x-3t)*(2*xi2-1)
"""
import torch
import torch.nn as nn
import numpy as np
import json
import os
import time
from networks import FeedForwardNet, gauss_legendre_points

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

NU = 0.1
N_MODES = 2
T_FINAL = 10 * np.pi
N_SUBDOMAINS = 10
SUBDOMAIN_LEN = np.pi


def exact_solution(x, t, xi1, xi2):
    return (-np.sin(x - t)
            - np.sqrt(3) * (1.5 + np.sin(t)) * np.cos(x - t) * (2*xi1 - 1)
            + np.sqrt(3) * (1.5 + np.cos(3*t)) * np.cos(2*x - 3*t) * (2*xi2 - 1))


def exact_mean(x, t):
    return -np.sin(x - t)


def exact_variance(x, t):
    """Var[u] = E[u^2] - (E[u])^2 computed analytically."""
    # The stochastic parts: s1 = sqrt(3)*(1.5+sin(t))*cos(x-t)*(2xi1-1)
    #                        s2 = sqrt(3)*(1.5+cos(3t))*cos(2x-3t)*(2xi2-1)
    # E[(2xi-1)^2] = 1/3 for U[0,1]
    # E[s1^2] = 3*(1.5+sin(t))^2 * cos^2(x-t) * 1/3 = (1.5+sin(t))^2*cos^2(x-t)
    # E[s2^2] = (1.5+cos(3t))^2*cos^2(2x-3t)
    # Cross term = 0 since xi1, xi2 independent and E[2xi-1]=0
    var = ((1.5 + np.sin(t))**2 * np.cos(x - t)**2 +
           (1.5 + np.cos(3*t))**2 * np.cos(2*x - 3*t)**2)
    return var


def exact_u1(x, t):
    return -1.0/np.sqrt(np.pi) * np.cos(x - t)

def exact_u2(x, t):
    return 1.0/np.sqrt(np.pi) * np.cos(2*x - 3*t)

def exact_a1(t):
    return np.sqrt(np.pi) * (1.5 + np.sin(t))

def exact_a2(t):
    return np.sqrt(np.pi) * (1.5 + np.cos(3*t))

def exact_Y1(xi1):
    return 2*xi1 - 1

def exact_Y2(xi2):
    return 2*xi2 - 1


def compute_forcing(x, t, xi1, xi2):
    """Compute f(x,t;xi) from the manufactured solution."""
    # f = du/dt + u*du/dx - nu*d2u/dx2
    # This is derived from the exact solution
    s3 = np.sqrt(3)
    c1 = 2*xi1 - 1
    c2 = 2*xi2 - 1

    # Mean part
    u_mean = -np.sin(x - t)
    # Stochastic parts
    s1_coeff = s3 * (1.5 + np.sin(t))
    s2_coeff = s3 * (1.5 + np.cos(3*t))

    u = u_mean - s1_coeff * np.cos(x - t) * c1 + s2_coeff * np.cos(2*x - 3*t) * c2

    # du/dt
    du_dt = (-np.cos(x - t)
             - s3 * np.cos(t) * np.cos(x - t) * c1
             - s3 * (1.5 + np.sin(t)) * np.sin(x - t) * c1
             + s3 * (-3*np.sin(3*t)) * np.cos(2*x - 3*t) * c2
             + s3 * (1.5 + np.cos(3*t)) * 3*np.sin(2*x - 3*t) * c2)

    # du/dx
    du_dx = (-np.cos(x - t)
             + s1_coeff * np.sin(x - t) * c1
             - s2_coeff * 2*np.sin(2*x - 3*t) * c2)

    # d2u/dx2
    d2u_dx2 = (np.sin(x - t)
               + s1_coeff * np.cos(x - t) * c1
               - s2_coeff * 4*np.cos(2*x - 3*t) * c2)

    f = du_dt + u * du_dx - NU * d2u_dx2
    return f


class BurgersNNDOBO:
    """Combined NN-DO/BO for stochastic Burgers on one subdomain."""

    def __init__(self, n_modes=2, method='DO'):
        self.n_modes = n_modes
        self.method = method

        self.u_nn = FeedForwardNet(2, 1, 3, 32).to(device)
        self.U_nn = FeedForwardNet(2, n_modes, 3, 64).to(device)
        self.A_nn = FeedForwardNet(1, n_modes, 3, 32).to(device)
        self.Y_nn = FeedForwardNet(2, n_modes, 3, 32).to(device)  # input: (xi1, xi2, t) but paper uses 2D xi

        # Actually Y depends on (xi, t) where xi is 2D, so input dim = 3
        self.Y_nn = FeedForwardNet(3, n_modes, 3, 32).to(device)

        self.params = (list(self.u_nn.parameters()) +
                      list(self.U_nn.parameters()) +
                      list(self.A_nn.parameters()) +
                      list(self.Y_nn.parameters()))

    def reconstruct(self, x, t, xi1, xi2):
        u_bar = self.u_nn(torch.cat([x, t], dim=-1))
        U = self.U_nn(torch.cat([x, t], dim=-1))
        A = self.A_nn(t)
        Y = self.Y_nn(torch.cat([xi1, xi2, t], dim=-1))
        u_full = u_bar.clone()
        for i in range(self.n_modes):
            u_full = u_full + A[:, i:i+1] * U[:, i:i+1] * Y[:, i:i+1]
        return u_full

    def compute_loss(self, x_c, t_c, xi1_c, xi2_c, f_c,
                     x_ic, t_ic0, a_ic, u_ic, Y_ic_vals, u_bar_ic,
                     t0_val):
        """Compute loss for one subdomain."""
        x_c = x_c.requires_grad_(True)
        t_c = t_c.requires_grad_(True)

        u_bar = self.u_nn(torch.cat([x_c, t_c], dim=-1))
        U = self.U_nn(torch.cat([x_c, t_c], dim=-1))
        A = self.A_nn(t_c)
        Y = self.Y_nn(torch.cat([xi1_c, xi2_c, t_c], dim=-1))

        u_full = u_bar.clone()
        for i in range(self.n_modes):
            u_full = u_full + A[:, i:i+1] * U[:, i:i+1] * Y[:, i:i+1]

        # PDE: du/dt + u*du/dx - nu*d2u/dx2 = f
        du_dt = torch.autograd.grad(u_full, t_c, torch.ones_like(u_full),
                                     create_graph=True, retain_graph=True)[0]
        du_dx = torch.autograd.grad(u_full, x_c, torch.ones_like(u_full),
                                     create_graph=True, retain_graph=True)[0]
        d2u_dx2 = torch.autograd.grad(du_dx, x_c, torch.ones_like(du_dx),
                                       create_graph=True, retain_graph=True)[0]

        residual = du_dt + u_full * du_dx - NU * d2u_dx2 - f_c
        MSE_0 = torch.mean(residual**2)

        # IC loss at subdomain start
        t_zero = torch.full_like(x_ic, t0_val)
        u_bar_pred_ic = self.u_nn(torch.cat([x_ic, t_zero], dim=-1))
        U_pred_ic = self.U_nn(torch.cat([x_ic, t_zero], dim=-1))
        A_pred_ic = self.A_nn(t_zero[:1])

        loss_ubar_ic = torch.mean((u_bar_pred_ic - u_bar_ic)**2)
        loss_U_ic = torch.mean((U_pred_ic - u_ic)**2)
        loss_A_ic = torch.mean((A_pred_ic - a_ic)**2)

        MSE_IC = loss_ubar_ic + loss_U_ic + loss_A_ic

        # BC: periodic
        u_left = self.u_nn(torch.cat([torch.full_like(t_c, -np.pi), t_c], dim=-1))
        u_right = self.u_nn(torch.cat([torch.full_like(t_c, np.pi), t_c], dim=-1))
        MSE_BC = torch.mean((u_left - u_right)**2)

        # DO/BO constraint - compute per-mode gradients
        dU_dt_list = []
        for i in range(self.n_modes):
            dUi_dt = torch.autograd.grad(U[:, i].sum(), t_c, create_graph=True, retain_graph=True)[0]
            dU_dt_list.append(dUi_dt)
        dY_dt_list = []
        for i in range(self.n_modes):
            dYi_dt = torch.autograd.grad(Y[:, i].sum(), t_c, create_graph=True, retain_graph=True)[0]
            dY_dt_list.append(dYi_dt)

        if self.method == 'DO':
            loss_EY = sum(torch.mean(Y[:, i:i+1])**2 for i in range(self.n_modes))
            loss_orth = 0.0
            for i in range(self.n_modes):
                for j in range(self.n_modes):
                    loss_orth += torch.mean(dU_dt_list[i].squeeze() * U[:, j])**2
            loss_YdY = sum(torch.mean(Y[:, i:i+1] * dY_dt_list[i])**2 for i in range(self.n_modes))
            MSE_constraint = loss_EY + loss_orth + loss_YdY
        else:  # BO
            loss_EY = sum(torch.mean(Y[:, i:i+1])**2 for i in range(self.n_modes))
            loss_sym_S = 0.0
            for i in range(self.n_modes):
                for j in range(self.n_modes):
                    Sij = torch.mean(dU_dt_list[i].squeeze() * U[:, j])
                    Sji = torch.mean(dU_dt_list[j].squeeze() * U[:, i])
                    loss_sym_S += (Sij + Sji)**2
            loss_sym_M = 0.0
            for i in range(self.n_modes):
                for j in range(self.n_modes):
                    Mij = torch.mean(Y[:, i:i+1] * dY_dt_list[j])
                    Mji = torch.mean(Y[:, j:j+1] * dY_dt_list[i])
                    loss_sym_M += (Mij + Mji)**2
            MSE_constraint = loss_EY + loss_sym_S + loss_sym_M

        total = MSE_0 + 100.0 * (MSE_IC + MSE_BC + MSE_constraint)
        return total, {
            'MSE_0': MSE_0.item(),
            'MSE_IC': MSE_IC.item(),
            'MSE_BC': MSE_BC.item(),
            'MSE_constraint': MSE_constraint.item(),
        }


def train_burgers_subdomain(method, subdomain_idx, n_epochs=50000):
    """Train one subdomain."""
    t_start_sub = subdomain_idx * SUBDOMAIN_LEN
    t_end_sub = (subdomain_idx + 1) * SUBDOMAIN_LEN

    model = BurgersNNDOBO(n_modes=N_MODES, method=method)
    optimizer = torch.optim.Adam(model.params, lr=0.001)

    # Training data
    n_x, n_t = 50, 30
    x_pts = np.linspace(-np.pi, np.pi, n_x)
    t_pts = np.sort(np.random.uniform(t_start_sub, t_end_sub, n_t))

    # GL quadrature for xi1, xi2 in [0,1] - 8th order
    gl_nodes, gl_weights = gauss_legendre_points(8, 0.0, 1.0)
    xi1_pts = gl_nodes
    xi2_pts = gl_nodes

    # Create collocation grid
    XX, TT, XI1, XI2 = np.meshgrid(x_pts, t_pts, xi1_pts, xi2_pts, indexing='ij')
    n_total = XX.size

    x_col = torch.tensor(XX.flatten(), dtype=torch.float32, device=device).unsqueeze(1)
    t_col = torch.tensor(TT.flatten(), dtype=torch.float32, device=device).unsqueeze(1)
    xi1_col = torch.tensor(XI1.flatten(), dtype=torch.float32, device=device).unsqueeze(1)
    xi2_col = torch.tensor(XI2.flatten(), dtype=torch.float32, device=device).unsqueeze(1)

    # Forcing term
    f_vals = compute_forcing(XX.flatten(), TT.flatten(), XI1.flatten(), XI2.flatten())
    f_col = torch.tensor(f_vals, dtype=torch.float32, device=device).unsqueeze(1)

    # IC at subdomain start
    x_ic = torch.tensor(x_pts, dtype=torch.float32, device=device).unsqueeze(1)
    u_bar_ic_vals = exact_mean(x_pts, t_start_sub)
    u_bar_ic = torch.tensor(u_bar_ic_vals, dtype=torch.float32, device=device).unsqueeze(1)

    u1_ic_vals = exact_u1(x_pts, t_start_sub)
    u2_ic_vals = exact_u2(x_pts, t_start_sub)
    u_ic = torch.tensor(np.stack([u1_ic_vals, u2_ic_vals], axis=1),
                         dtype=torch.float32, device=device)

    a1_ic = exact_a1(t_start_sub)
    a2_ic = exact_a2(t_start_sub)
    a_ic = torch.tensor([[a1_ic, a2_ic]], dtype=torch.float32, device=device)

    batch_size = min(8000, n_total)
    t_train_start = time.time()

    for epoch in range(n_epochs):
        model.u_nn.train()
        model.U_nn.train()
        model.A_nn.train()
        model.Y_nn.train()

        idx = torch.randperm(n_total, device=device)[:batch_size]

        optimizer.zero_grad()
        loss, loss_dict = model.compute_loss(
            x_col[idx], t_col[idx], xi1_col[idx], xi2_col[idx], f_col[idx],
            x_ic, None, a_ic, u_ic, None, u_bar_ic, t_start_sub
        )
        loss.backward()
        optimizer.step()

        if epoch % 10000 == 0:
            print(f"  Sub {subdomain_idx} Epoch {epoch:5d} | Loss: {loss.item():.6f} | "
                  f"MSE_0: {loss_dict['MSE_0']:.2e} | MSE_IC: {loss_dict['MSE_IC']:.2e}")

    return model, time.time() - t_train_start


def evaluate_burgers(models, method, save_dir='../results/burgers'):
    """Evaluate errors at T = 10*pi."""
    os.makedirs(save_dir, exist_ok=True)

    t_final = T_FINAL
    n_x_eval = 200
    x_eval = np.linspace(-np.pi, np.pi, n_x_eval)
    n_mc = 5000

    # Use the last subdomain's model
    model = models[-1]
    model.u_nn.eval()
    model.U_nn.eval()
    model.A_nn.eval()
    model.Y_nn.eval()

    with torch.no_grad():
        x_t = torch.tensor(x_eval, dtype=torch.float32, device=device).unsqueeze(1)
        t_t = torch.full((n_x_eval, 1), t_final, dtype=torch.float32, device=device)

        u_bar_pred = model.u_nn(torch.cat([x_t, t_t], dim=-1)).cpu().numpy().flatten()
        U_pred = model.U_nn(torch.cat([x_t, t_t], dim=-1)).cpu().numpy()
        A_pred = model.A_nn(t_t[:1]).cpu().numpy().flatten()

        # MC samples
        xi1_mc = np.random.uniform(0, 1, n_mc)
        xi2_mc = np.random.uniform(0, 1, n_mc)

        u_pred_samples = np.zeros((n_x_eval, n_mc))
        u_exact_samples = np.zeros((n_x_eval, n_mc))

        for j in range(n_mc):
            xi1_t = torch.full((n_x_eval, 1), xi1_mc[j], dtype=torch.float32, device=device)
            xi2_t = torch.full((n_x_eval, 1), xi2_mc[j], dtype=torch.float32, device=device)
            Y_pred = model.Y_nn(torch.cat([xi1_t, xi2_t, t_t], dim=-1)).cpu().numpy()

            u_j = u_bar_pred.copy()
            for i in range(N_MODES):
                u_j += A_pred[i] * U_pred[:, i] * Y_pred[:, i]
            u_pred_samples[:, j] = u_j
            u_exact_samples[:, j] = exact_solution(x_eval, t_final, xi1_mc[j], xi2_mc[j])

    mean_pred = np.mean(u_pred_samples, axis=1)
    mean_exact = exact_mean(x_eval, t_final)
    var_pred = np.var(u_pred_samples, axis=1)
    var_exact = exact_variance(x_eval, t_final)

    dx = x_eval[1] - x_eval[0]
    L2_mean = np.sqrt(np.sum((mean_pred - mean_exact)**2) * dx)
    L2_var = np.sqrt(np.sum((var_pred - var_exact)**2) * dx)
    rel_L2_mean = L2_mean / np.sqrt(np.sum(mean_exact**2) * dx) * 100
    rel_L2_var = L2_var / np.sqrt(np.sum(var_exact**2) * dx) * 100

    # Component errors
    a1_exact = exact_a1(t_final)
    a2_exact = exact_a2(t_final)
    u1_exact = exact_u1(x_eval, t_final)
    u2_exact = exact_u2(x_eval, t_final)

    L2_a1 = abs(A_pred[0] - a1_exact)
    L2_a2 = abs(A_pred[1] - a2_exact)
    L2_u1 = np.sqrt(np.sum((U_pred[:, 0] - u1_exact)**2) * dx)
    L2_u2 = np.sqrt(np.sum((U_pred[:, 1] - u2_exact)**2) * dx)

    rel_a1 = L2_a1 / abs(a1_exact) * 100
    rel_a2 = L2_a2 / abs(a2_exact) * 100
    rel_u1 = L2_u1 / np.sqrt(np.sum(u1_exact**2) * dx) * 100
    rel_u2 = L2_u2 / np.sqrt(np.sum(u2_exact**2) * dx) * 100

    results = {
        'E[u]_L2': float(L2_mean), 'E[u]_relL2': float(rel_L2_mean),
        'Var[u]_L2': float(L2_var), 'Var[u]_relL2': float(rel_L2_var),
        'a1_L2': float(L2_a1), 'a1_relL2': float(rel_a1),
        'a2_L2': float(L2_a2), 'a2_relL2': float(rel_a2),
        'u1_L2': float(L2_u1), 'u1_relL2': float(rel_u1),
        'u2_L2': float(L2_u2), 'u2_relL2': float(rel_u2),
    }

    print(f"\n=== Burgers NN-{method} Results at T=10pi ===")
    for k, v in results.items():
        if 'rel' in k:
            print(f"  {k}: {v:.2f}%")
        else:
            print(f"  {k}: {v:.4f}")

    with open(os.path.join(save_dir, f'burgers_nn{method.lower()}_results.json'), 'w') as f:
        json.dump(results, f, indent=2)

    return results


def train_burgers(method='DO', save_dir='../results/burgers'):
    """Train NN-DO/BO for Burgers across all subdomains."""
    os.makedirs(save_dir, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"Training Burgers NN-{method}")
    print(f"T=[0, {T_FINAL:.2f}], {N_SUBDOMAINS} subdomains")
    print(f"{'='*60}")

    models = []
    total_time = 0

    for sub_idx in range(N_SUBDOMAINS):
        print(f"\n--- Subdomain {sub_idx}/{N_SUBDOMAINS-1} ---")
        model, sub_time = train_burgers_subdomain(method, sub_idx)
        models.append(model)
        total_time += sub_time
        print(f"  Subdomain {sub_idx} done in {sub_time:.1f}s")

    print(f"\nTotal training time: {total_time:.1f}s")

    results = evaluate_burgers(models, method, save_dir)
    results['total_training_time'] = total_time
    return results


if __name__ == '__main__':
    import sys
    method = sys.argv[1] if len(sys.argv) > 1 else 'DO'
    train_burgers(method=method)
