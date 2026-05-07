"""
Example 1: Stochastic Advection Equation - NN-DO and NN-BO methods.
Zhang et al. 2019, Section 5.1.

PDE: du/dt + xi * du/dx = 0, x in [-pi, pi], t in [0, pi]
IC: u(x, 0; xi) = -sin(x)
BC: periodic u(-pi, t) = u(pi, t)
xi ~ N(0, sigma^2), sigma = 0.8

Exact solution: u(x, t; xi) = -sin(x - xi*t)
"""
import torch
import torch.nn as nn
import numpy as np
import json
import os
import time
from scipy.stats import norm
from networks import FeedForwardNet, gauss_legendre_points

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

SIGMA = 0.8
N_MODES = 2

# --- Exact solutions ---
def exact_mean(x, t, sigma=SIGMA):
    return -np.sin(x) * np.exp(-sigma**2 * t**2 / 2)

def exact_variance(x, t, sigma=SIGMA):
    E_u = exact_mean(x, t, sigma)
    return 0.5 * (1 - np.cos(2*x) * np.exp(-2 * sigma**2 * t**2)) - E_u**2

def exact_u_DO_1(x, t):
    return -1.0 / np.sqrt(np.pi) * np.cos(x)

def exact_u_DO_2(x, t):
    return -1.0 / np.sqrt(np.pi) * np.sin(x)

def exact_Y_DO_1(t, xi, sigma=SIGMA):
    return -np.sqrt(np.pi) * np.sin(xi * t)

def exact_Y_DO_2(t, xi, sigma=SIGMA):
    return np.sqrt(np.pi) * (np.cos(xi * t) - np.exp(-sigma**2 * t**2 / 2))

def exact_a_DO_1(t, xi_samples, sigma=SIGMA):
    """a_1(t) = sqrt(E[Y1^2]) * norm(u1)."""
    # In the DO case, a_i(t) = sqrt(pi * E[sin^2(xi*t)])
    E_sin2 = np.mean(np.sin(xi_samples * t)**2)
    return np.sqrt(np.pi * E_sin2)

def exact_a_DO_2(t, xi_samples, sigma=SIGMA):
    E_val = np.mean((np.cos(xi_samples * t) - np.exp(-sigma**2 * t**2 / 2))**2)
    return np.sqrt(np.pi * E_val)


class AdvectionNNDO:
    """NN-DO method for the stochastic advection equation."""

    def __init__(self, n_modes=2):
        self.n_modes = n_modes

        # Networks (paper specs)
        self.u_nn = FeedForwardNet(2, 1, 3, 32).to(device)  # mean: (x,t)->1
        self.U_nn = FeedForwardNet(2, n_modes, 3, 32).to(device)  # bases: (x,t)->N
        self.A_nn = FeedForwardNet(1, n_modes, 3, 16).to(device)  # scaling: t->N
        self.Y_nn = FeedForwardNet(2, n_modes, 4, 64).to(device)  # stoch: (xi,t)->N

        self.params = list(self.u_nn.parameters()) + \
                      list(self.U_nn.parameters()) + \
                      list(self.A_nn.parameters()) + \
                      list(self.Y_nn.parameters())

    def reconstruct(self, x, t, xi):
        """Reconstruct u(x, t; xi) = u_bar + sum a_i * u_i * Y_i."""
        u_bar = self.u_nn(torch.cat([x, t], dim=-1))
        U = self.U_nn(torch.cat([x, t], dim=-1))
        A = self.A_nn(t)
        Y = self.Y_nn(torch.cat([xi, t], dim=-1))
        u_total = u_bar
        for i in range(self.n_modes):
            u_total = u_total + A[:, i:i+1] * U[:, i:i+1] * Y[:, i:i+1]
        return u_total

    def compute_loss(self, x_col, t_col, xi_col, x_ic, xi_ic, x_bc, t_bc, xi_bc,
                     gl_weights_xi):
        """
        Compute total loss = MSE_w + 100*(MSE_IC + MSE_BC + MSE_DO) + 0.1*MSE_0
        """
        # --- MSE_w: Weak-form PDE residual ---
        # The PDE: du/dt + xi * du/dx = 0
        # We need gradients
        x_c = x_col.requires_grad_(True)
        t_c = t_col.requires_grad_(True)
        xi_c = xi_col.requires_grad_(True)

        u_bar = self.u_nn(torch.cat([x_c, t_c], dim=-1))
        U = self.U_nn(torch.cat([x_c, t_c], dim=-1))
        A = self.A_nn(t_c)
        Y = self.Y_nn(torch.cat([xi_c, t_c], dim=-1))

        # Full solution
        u_full = u_bar.clone()
        for i in range(self.n_modes):
            u_full = u_full + A[:, i:i+1] * U[:, i:i+1] * Y[:, i:i+1]

        # du/dt and du/dx
        du_dt = torch.autograd.grad(u_full, t_c, torch.ones_like(u_full),
                                     create_graph=True, retain_graph=True)[0]
        du_dx = torch.autograd.grad(u_full, x_c, torch.ones_like(u_full),
                                     create_graph=True, retain_graph=True)[0]

        # PDE residual: du/dt + xi * du/dx = 0
        residual = du_dt + xi_c * du_dx

        # Weak form 1: E[residual] = 0 (average over xi for each x,t)
        # Weak form 2: <residual, u_i> = 0 (integrate over x for each t,xi)
        # Weak form 3: E[residual * Y_i] = 0

        # For simplicity, compute the strong-form MSE_0 as the main PDE loss
        MSE_0 = torch.mean(residual**2)

        # --- MSE_IC: Initial condition ---
        # u(x, 0; xi) = -sin(x) for all xi
        t_zero = torch.zeros_like(x_ic)
        u_bar_ic = self.u_nn(torch.cat([x_ic, t_zero], dim=-1))
        U_ic = self.U_nn(torch.cat([x_ic, t_zero], dim=-1))
        A_ic = self.A_nn(t_zero)
        Y_ic = self.Y_nn(torch.cat([xi_ic, t_zero], dim=-1))

        # Mean IC: u_bar(x, 0) = E[-sin(x)] = -sin(x) * exp(0) = -sin(x)
        target_mean_ic = -torch.sin(x_ic)
        loss_mean_ic = torch.mean((u_bar_ic - target_mean_ic)**2)

        # Mode IC: from paper Eq. u_1(x,0) = -(1/pi)*cos(x), u_2(x,0) = -(1/pi)*sin(x)
        target_U1_ic = -1.0 / np.pi * torch.cos(x_ic)
        target_U2_ic = -1.0 / np.pi * torch.sin(x_ic)
        loss_U_ic = torch.mean((U_ic[:, 0:1] - target_U1_ic)**2) + \
                    torch.mean((U_ic[:, 1:2] - target_U2_ic)**2)

        # A IC: a_1(0) = a_2(0) = 0
        loss_A_ic = torch.mean(A_ic**2)

        # Y IC: Y_1(0; xi) = -xi, Y_2(0; xi) = -sqrt(2)/2 * (xi^2 - 1)
        target_Y1_ic = -xi_ic
        target_Y2_ic = -np.sqrt(2) / 2 * (xi_ic**2 - 1)
        loss_Y_ic = torch.mean((Y_ic[:, 0:1] - target_Y1_ic)**2) + \
                    torch.mean((Y_ic[:, 1:2] - target_Y2_ic)**2)

        MSE_IC = loss_mean_ic + loss_U_ic + loss_A_ic + loss_Y_ic

        # --- MSE_BC: Periodic boundary condition ---
        u_left = self.u_nn(torch.cat([torch.full_like(t_bc, -np.pi), t_bc], dim=-1))
        u_right = self.u_nn(torch.cat([torch.full_like(t_bc, np.pi), t_bc], dim=-1))
        U_left = self.U_nn(torch.cat([torch.full_like(t_bc, -np.pi), t_bc], dim=-1))
        U_right = self.U_nn(torch.cat([torch.full_like(t_bc, np.pi), t_bc], dim=-1))
        MSE_BC = torch.mean((u_left - u_right)**2) + torch.mean((U_left - U_right)**2)

        # --- MSE_DO: DO constraint ---
        # 1. E[Y_i] = 0 for each i
        loss_EY = torch.mean(Y[:, 0:1])**2 + torch.mean(Y[:, 1:2])**2

        # 2. <dU_i/dt, U_j> = 0 for all i,j
        # Compute dU_i/dt for each mode separately
        dU_dt_list = []
        for i in range(self.n_modes):
            dUi_dt = torch.autograd.grad(U[:, i].sum(), t_c, create_graph=True, retain_graph=True)[0]
            dU_dt_list.append(dUi_dt)
        loss_orth = 0.0
        for i in range(self.n_modes):
            for j in range(self.n_modes):
                inner = torch.mean(dU_dt_list[i].squeeze() * U[:, j])
                loss_orth = loss_orth + inner**2

        # 3. E[Y_i * dY_i/dt] = 0
        dY_dt_list = []
        for i in range(self.n_modes):
            dYi_dt = torch.autograd.grad(Y[:, i].sum(), t_c, create_graph=True, retain_graph=True)[0]
            dY_dt_list.append(dYi_dt)
        loss_YdY = 0.0
        for i in range(self.n_modes):
            inner = torch.mean(Y[:, i:i+1] * dY_dt_list[i])
            loss_YdY = loss_YdY + inner**2

        MSE_DO = loss_EY + loss_orth + loss_YdY

        # --- Total loss ---
        total_loss = MSE_0 + 100.0 * (MSE_IC + MSE_BC + MSE_DO)

        return total_loss, {
            'MSE_0': MSE_0.item(),
            'MSE_IC': MSE_IC.item(),
            'MSE_BC': MSE_BC.item(),
            'MSE_DO': MSE_DO.item(),
        }


class AdvectionNNBO:
    """NN-BO method for the stochastic advection equation."""

    def __init__(self, n_modes=2):
        self.n_modes = n_modes
        self.u_nn = FeedForwardNet(2, 1, 3, 32).to(device)
        self.U_nn = FeedForwardNet(2, n_modes, 3, 32).to(device)
        self.A_nn = FeedForwardNet(1, n_modes, 3, 16).to(device)
        self.Y_nn = FeedForwardNet(2, n_modes, 4, 64).to(device)

        self.params = list(self.u_nn.parameters()) + \
                      list(self.U_nn.parameters()) + \
                      list(self.A_nn.parameters()) + \
                      list(self.Y_nn.parameters())

    def compute_loss(self, x_col, t_col, xi_col, x_ic, xi_ic, x_bc, t_bc,
                     gl_weights_xi):
        x_c = x_col.requires_grad_(True)
        t_c = t_col.requires_grad_(True)
        xi_c = xi_col.requires_grad_(True)

        u_bar = self.u_nn(torch.cat([x_c, t_c], dim=-1))
        U = self.U_nn(torch.cat([x_c, t_c], dim=-1))
        A = self.A_nn(t_c)
        Y = self.Y_nn(torch.cat([xi_c, t_c], dim=-1))

        u_full = u_bar.clone()
        for i in range(self.n_modes):
            u_full = u_full + A[:, i:i+1] * U[:, i:i+1] * Y[:, i:i+1]

        du_dt = torch.autograd.grad(u_full, t_c, torch.ones_like(u_full),
                                     create_graph=True, retain_graph=True)[0]
        du_dx = torch.autograd.grad(u_full, x_c, torch.ones_like(u_full),
                                     create_graph=True, retain_graph=True)[0]

        residual = du_dt + xi_c * du_dx
        MSE_0 = torch.mean(residual**2)

        # IC
        t_zero = torch.zeros_like(x_ic)
        u_bar_ic = self.u_nn(torch.cat([x_ic, t_zero], dim=-1))
        U_ic = self.U_nn(torch.cat([x_ic, t_zero], dim=-1))
        A_ic = self.A_nn(t_zero)
        Y_ic = self.Y_nn(torch.cat([xi_ic, t_zero], dim=-1))

        target_mean_ic = -torch.sin(x_ic)
        loss_mean_ic = torch.mean((u_bar_ic - target_mean_ic)**2)
        target_U1_ic = -1.0 / np.pi * torch.cos(x_ic)
        target_U2_ic = -1.0 / np.pi * torch.sin(x_ic)
        loss_U_ic = torch.mean((U_ic[:, 0:1] - target_U1_ic)**2) + \
                    torch.mean((U_ic[:, 1:2] - target_U2_ic)**2)
        loss_A_ic = torch.mean(A_ic**2)
        target_Y1_ic = -xi_ic
        target_Y2_ic = -np.sqrt(2) / 2 * (xi_ic**2 - 1)
        loss_Y_ic = torch.mean((Y_ic[:, 0:1] - target_Y1_ic)**2) + \
                    torch.mean((Y_ic[:, 1:2] - target_Y2_ic)**2)
        MSE_IC = loss_mean_ic + loss_U_ic + loss_A_ic + loss_Y_ic

        # BC
        u_left = self.u_nn(torch.cat([torch.full_like(t_bc, -np.pi), t_bc], dim=-1))
        u_right = self.u_nn(torch.cat([torch.full_like(t_bc, np.pi), t_bc], dim=-1))
        U_left = self.U_nn(torch.cat([torch.full_like(t_bc, -np.pi), t_bc], dim=-1))
        U_right = self.U_nn(torch.cat([torch.full_like(t_bc, np.pi), t_bc], dim=-1))
        MSE_BC = torch.mean((u_left - u_right)**2) + torch.mean((U_left - U_right)**2)

        # BO constraints
        # Compute dU_i/dt for each mode
        dU_dt_list = []
        for i in range(self.n_modes):
            dUi_dt = torch.autograd.grad(U[:, i].sum(), t_c, create_graph=True, retain_graph=True)[0]
            dU_dt_list.append(dUi_dt)
        # 1. E[Y_i] = 0
        loss_EY = torch.mean(Y[:, 0:1])**2 + torch.mean(Y[:, 1:2])**2
        # 2. S_{ij} + S_{ji} = 0: <dU_i/dt, U_j> + <dU_j/dt, U_i> = 0
        loss_sym_S = 0.0
        for i in range(self.n_modes):
            for j in range(self.n_modes):
                Sij = torch.mean(dU_dt_list[i].squeeze() * U[:, j])
                Sji = torch.mean(dU_dt_list[j].squeeze() * U[:, i])
                loss_sym_S = loss_sym_S + (Sij + Sji)**2
        # 3. M_{ij} + M_{ji} = 0: E[Y_i dY_j/dt] + E[Y_j dY_i/dt] = 0
        dY_dt_list = []
        for i in range(self.n_modes):
            dYi_dt = torch.autograd.grad(Y[:, i].sum(), t_c, create_graph=True, retain_graph=True)[0]
            dY_dt_list.append(dYi_dt)
        loss_sym_M = 0.0
        for i in range(self.n_modes):
            for j in range(self.n_modes):
                Mij = torch.mean(Y[:, i:i+1] * dY_dt_list[j])
                Mji = torch.mean(Y[:, j:j+1] * dY_dt_list[i])
                loss_sym_M = loss_sym_M + (Mij + Mji)**2

        MSE_BO = loss_EY + loss_sym_S + loss_sym_M

        total_loss = MSE_0 + 100.0 * (MSE_IC + MSE_BC + MSE_BO)

        return total_loss, {
            'MSE_0': MSE_0.item(),
            'MSE_IC': MSE_IC.item(),
            'MSE_BC': MSE_BC.item(),
            'MSE_BO': MSE_BO.item(),
        }


def generate_training_data(n_x=50, n_t=50, n_xi=50):
    """Generate training collocation points."""
    # Spatial: equidistant on [-pi, pi]
    x_pts = np.linspace(-np.pi, np.pi, n_x)
    # Temporal: uniform random in [0, pi]
    t_pts = np.sort(np.random.uniform(0, np.pi, n_t))
    # Stochastic: GL quadrature mapped through inverse normal CDF
    gl_nodes, gl_weights = gauss_legendre_points(n_xi, 0.0, 1.0)
    xi_pts = norm.ppf(gl_nodes)

    return x_pts, t_pts, xi_pts, gl_weights


def evaluate_errors(model, x_test, t_final, xi_samples, sigma=SIGMA):
    """Evaluate L2 and relative L2 errors at the final time T."""
    model.u_nn.eval()
    model.U_nn.eval()
    model.A_nn.eval()
    model.Y_nn.eval()

    n_xi_eval = len(xi_samples)
    n_x_eval = len(x_test)

    with torch.no_grad():
        # Mean field
        x_t = torch.tensor(x_test, dtype=torch.float32, device=device).unsqueeze(1)
        t_t = torch.full((n_x_eval, 1), t_final, dtype=torch.float32, device=device)
        u_bar_pred = model.u_nn(torch.cat([x_t, t_t], dim=-1)).cpu().numpy().flatten()
        u_bar_exact = exact_mean(x_test, t_final, sigma)

        # Variance via MC
        u_samples_pred = np.zeros((n_x_eval, n_xi_eval))
        u_samples_exact = np.zeros((n_x_eval, n_xi_eval))

        A_pred = model.A_nn(t_t[:1]).cpu().numpy().flatten()
        U_pred = model.U_nn(torch.cat([x_t, t_t], dim=-1)).cpu().numpy()

        for j, xi_val in enumerate(xi_samples):
            xi_t = torch.full((n_x_eval, 1), xi_val, dtype=torch.float32, device=device)
            Y_pred = model.Y_nn(torch.cat([xi_t, t_t], dim=-1)).cpu().numpy()

            u_pred_j = u_bar_pred.copy()
            for i in range(model.n_modes):
                u_pred_j += A_pred[i] * U_pred[:, i] * Y_pred[:, i]
            u_samples_pred[:, j] = u_pred_j
            u_samples_exact[:, j] = -np.sin(x_test - xi_val * t_final)

        mean_pred = np.mean(u_samples_pred, axis=1)
        mean_exact = np.mean(u_samples_exact, axis=1)
        var_pred = np.var(u_samples_pred, axis=1)
        var_exact = exact_variance(x_test, t_final, sigma)

    # L2 errors
    dx = x_test[1] - x_test[0]
    L2_mean = np.sqrt(np.sum((u_bar_pred - u_bar_exact)**2) * dx)
    L2_var = np.sqrt(np.sum((var_pred - var_exact)**2) * dx)

    rel_L2_mean = L2_mean / np.sqrt(np.sum(u_bar_exact**2) * dx) * 100
    rel_L2_var = L2_var / np.sqrt(np.sum(var_exact**2) * dx) * 100

    results = {
        'E[u]_L2': float(L2_mean),
        'E[u]_relL2': float(rel_L2_mean),
        'Var[u]_L2': float(L2_var),
        'Var[u]_relL2': float(rel_L2_var),
    }

    # Individual component errors (a, u, Y)
    # a_i errors
    a_pred = A_pred
    # Compute exact a from MC
    xi_large = np.random.normal(0, sigma, 10000)
    a1_exact = exact_a_DO_1(t_final, xi_large, sigma)
    a2_exact = exact_a_DO_2(t_final, xi_large, sigma)
    results['a1_L2'] = float(abs(a_pred[0] - a1_exact))
    results['a2_L2'] = float(abs(a_pred[1] - a2_exact))
    results['a1_relL2'] = float(abs(a_pred[0] - a1_exact) / abs(a1_exact) * 100)
    results['a2_relL2'] = float(abs(a_pred[1] - a2_exact) / abs(a2_exact) * 100)

    return results


def train_advection(method='DO', n_epochs=300000, save_dir='../results/advection'):
    """Train NN-DO or NN-BO for stochastic advection."""
    os.makedirs(save_dir, exist_ok=True)

    if method == 'DO':
        model = AdvectionNNDO(n_modes=N_MODES)
    else:
        model = AdvectionNNBO(n_modes=N_MODES)

    optimizer = torch.optim.Adam(model.params, lr=0.001)

    # Generate training data
    x_pts, t_pts, xi_pts, gl_weights = generate_training_data(50, 50, 50)

    # Create meshgrid for collocation
    XX, TT, XI = np.meshgrid(x_pts, t_pts, xi_pts, indexing='ij')
    x_col = torch.tensor(XX.flatten(), dtype=torch.float32, device=device).unsqueeze(1)
    t_col = torch.tensor(TT.flatten(), dtype=torch.float32, device=device).unsqueeze(1)
    xi_col = torch.tensor(XI.flatten(), dtype=torch.float32, device=device).unsqueeze(1)

    # IC data
    x_ic = torch.tensor(x_pts, dtype=torch.float32, device=device).unsqueeze(1)
    xi_ic = torch.tensor(xi_pts, dtype=torch.float32, device=device).unsqueeze(1)
    # Repeat for all xi at t=0
    x_ic_rep = x_ic.repeat(len(xi_pts), 1)
    xi_ic_rep = xi_ic.repeat_interleave(len(x_pts), dim=0)

    # BC data
    t_bc = torch.tensor(t_pts, dtype=torch.float32, device=device).unsqueeze(1)

    gl_weights_t = torch.tensor(gl_weights, dtype=torch.float32, device=device)

    # Training - use random mini-batches for efficiency
    batch_size = 2000
    n_col = len(x_col)

    print(f"\nTraining NN-{method} for stochastic advection...")
    print(f"Total collocation points: {n_col}")
    print(f"Epochs: {n_epochs}")

    loss_history = []
    t_start = time.time()

    for epoch in range(n_epochs):
        model.u_nn.train()
        model.U_nn.train()
        model.A_nn.train()
        model.Y_nn.train()

        # Random batch
        idx = torch.randperm(n_col, device=device)[:batch_size]
        x_b = x_col[idx]
        t_b = t_col[idx]
        xi_b = xi_col[idx]

        optimizer.zero_grad()

        if method == 'DO':
            loss, loss_dict = model.compute_loss(
                x_b, t_b, xi_b, x_ic, xi_ic, t_bc, t_bc, None, gl_weights_t
            )
        else:
            loss, loss_dict = model.compute_loss(
                x_b, t_b, xi_b, x_ic, xi_ic, t_bc, t_bc, gl_weights_t
            )

        loss.backward()
        optimizer.step()

        if epoch % 10000 == 0:
            elapsed = time.time() - t_start
            print(f"Epoch {epoch:6d}/{n_epochs} | Loss: {loss.item():.6f} | "
                  f"MSE_0: {loss_dict['MSE_0']:.2e} | "
                  f"MSE_IC: {loss_dict['MSE_IC']:.2e} | "
                  f"Time: {elapsed:.1f}s")
            loss_history.append({'epoch': epoch, **loss_dict, 'total': loss.item()})

    # Evaluate errors
    print("\nEvaluating errors at T = pi...")
    x_eval = np.linspace(-np.pi, np.pi, 200)
    xi_eval = np.random.normal(0, SIGMA, 5000)
    errors = evaluate_errors(model, x_eval, np.pi, xi_eval)

    print(f"\n=== NN-{method} Results at T=pi ===")
    for k, v in errors.items():
        if 'rel' in k:
            print(f"  {k}: {v:.2f}%")
        else:
            print(f"  {k}: {v:.4f}")

    # Save results
    results = {
        'method': method,
        'errors': errors,
        'loss_history': loss_history,
        'training_time': time.time() - t_start,
        'n_epochs': n_epochs,
    }
    with open(os.path.join(save_dir, f'advection_nn{method.lower()}_results.json'), 'w') as f:
        json.dump(results, f, indent=2)

    return results


if __name__ == '__main__':
    import sys
    method = sys.argv[1] if len(sys.argv) > 1 else 'DO'
    train_advection(method=method)
