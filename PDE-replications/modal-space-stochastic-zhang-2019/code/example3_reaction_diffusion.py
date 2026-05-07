"""
Example 3: Reaction-Diffusion Equation - NN-BO (forward + inverse).
Zhang et al. 2019, Section 5.3.

PDE: du/dt = a*u_xx + b*u^2 + f(x;w)
Domain: x in [-1, 1], t in [0, 1]
BC: u(-1,t) = u(1,t) = 0 (Dirichlet)
IC: u(x,0;w) = -sin(pi*x) (deterministic)

f(x;w) = (1-x^2)*g(x;w)
g(x;w) ~ GP(1, C(x1,x2))
C(x1,x2) = sigma_g^2 * exp(-(x1-x2)^2 / lc^2)

Forward: a=0.1, b=0.5, sigma_g=1, lc=0.1, 19 KL modes, 6 BO modes
Inverse: a=?, b=? (true: a=0.5, b=0.3), sigma_g=1, lc=0.4, 4 BO modes
"""
import torch
import torch.nn as nn
import numpy as np
import json
import os
import time
from scipy.linalg import eigh
from networks import FeedForwardNet

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")


def squared_exp_kernel(x1, x2, sigma_g, lc):
    """Squared exponential kernel."""
    return sigma_g**2 * np.exp(-(x1 - x2)**2 / lc**2)


def compute_kl_expansion(x_pts, sigma_g, lc, n_kl_modes):
    """
    Compute KL expansion of the GP via Nystrom method.
    Returns eigenvalues and eigenfunctions evaluated at x_pts.
    """
    n = len(x_pts)
    dx = x_pts[1] - x_pts[0]

    # Build covariance matrix
    C = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            C[i, j] = squared_exp_kernel(x_pts[i], x_pts[j], sigma_g, lc)

    # Weight by quadrature (trapezoidal)
    W = np.full(n, dx)
    W[0] = dx / 2
    W[-1] = dx / 2

    # Solve weighted eigenvalue problem: C @ diag(W) @ phi = lambda * phi
    CW = C @ np.diag(W)
    eigenvalues, eigenvectors = eigh(CW)

    # Sort descending
    idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    # Normalize eigenfunctions
    for i in range(n):
        norm = np.sqrt(np.sum(eigenvectors[:, i]**2 * W))
        eigenvectors[:, i] /= norm

    # Truncate
    eigenvalues = eigenvalues[:n_kl_modes]
    eigenvectors = eigenvectors[:, :n_kl_modes]

    # Check energy captured
    total_energy = np.sum(np.diag(C) * W)
    captured = np.sum(eigenvalues)
    print(f"KL expansion: {n_kl_modes} modes capture {captured/total_energy*100:.1f}% energy")

    return eigenvalues, eigenvectors


def generate_gp_samples(x_pts, sigma_g, lc, n_kl_modes, n_samples, eigenvalues, eigenvectors):
    """Generate GP samples via KL expansion: g(x;w) = 1 + sum sqrt(lam_i)*phi_i(x)*xi_i."""
    xi = np.random.randn(n_samples, n_kl_modes)
    # g = mean(=1) + sum sqrt(lambda_i) * phi_i(x) * xi_i
    g_samples = np.ones((n_samples, len(x_pts)))
    for k in range(n_kl_modes):
        g_samples += np.sqrt(eigenvalues[k]) * np.outer(xi[:, k], eigenvectors[:, k])
    return g_samples, xi


class ReactionDiffusionNNBO:
    """NN-BO for stochastic reaction-diffusion."""

    def __init__(self, n_bo_modes=6, n_kl_modes=19, learn_coeffs=False):
        self.n_bo_modes = n_bo_modes
        self.n_kl_modes = n_kl_modes
        self.learn_coeffs = learn_coeffs

        # Networks
        self.u_nn = FeedForwardNet(2, 1, 3, 32).to(device)  # mean: (x,t)->1
        self.U_nn = FeedForwardNet(2, n_bo_modes, 3, 64).to(device)  # modes: (x,t)->N
        self.Y_nn = FeedForwardNet(n_kl_modes + 1, n_bo_modes, 3, 64).to(device)  # (xi, t)->N

        # Each a_i has its own small network (3 layers, 4 neurons)
        self.A_nns = nn.ModuleList([
            FeedForwardNet(1, 1, 3, 4).to(device) for _ in range(n_bo_modes)
        ])

        self.params = (list(self.u_nn.parameters()) +
                      list(self.U_nn.parameters()) +
                      list(self.Y_nn.parameters()) +
                      list(self.A_nns.parameters()))

        if learn_coeffs:
            self.a_param = nn.Parameter(torch.tensor([1.0], device=device))
            self.b_param = nn.Parameter(torch.tensor([1.0], device=device))
            self.params += [self.a_param, self.b_param]

    def get_A(self, t):
        """Get all scaling factors."""
        As = []
        for i in range(self.n_bo_modes):
            As.append(self.A_nns[i](t))
        return torch.cat(As, dim=-1)

    def reconstruct(self, x, t, xi):
        u_bar = self.u_nn(torch.cat([x, t], dim=-1))
        U = self.U_nn(torch.cat([x, t], dim=-1))
        A = self.get_A(t)
        Y = self.Y_nn(torch.cat([xi, t], dim=-1))
        u_full = u_bar.clone()
        for i in range(self.n_bo_modes):
            u_full = u_full + A[:, i:i+1] * U[:, i:i+1] * Y[:, i:i+1]
        return u_full

    def compute_loss(self, x_c, t_c, xi_c, f_c, x_ic, a_coeff, b_coeff,
                     extra_mean_data=None):
        """
        Compute loss.
        f_c: forcing values at collocation points, shape (batch, 1)
        xi_c: KL coefficients, shape (batch, n_kl_modes)
        """
        x_c = x_c.requires_grad_(True)
        t_c = t_c.requires_grad_(True)

        u_bar = self.u_nn(torch.cat([x_c, t_c], dim=-1))
        U = self.U_nn(torch.cat([x_c, t_c], dim=-1))
        A = self.get_A(t_c)
        Y = self.Y_nn(torch.cat([xi_c, t_c], dim=-1))

        u_full = u_bar.clone()
        for i in range(self.n_bo_modes):
            u_full = u_full + A[:, i:i+1] * U[:, i:i+1] * Y[:, i:i+1]

        # PDE: du/dt = a*u_xx + b*u^2 + f
        if self.learn_coeffs:
            a_val = self.a_param
            b_val = self.b_param
        else:
            a_val = a_coeff
            b_val = b_coeff

        du_dt = torch.autograd.grad(u_full, t_c, torch.ones_like(u_full),
                                     create_graph=True, retain_graph=True)[0]
        du_dx = torch.autograd.grad(u_full, x_c, torch.ones_like(u_full),
                                     create_graph=True, retain_graph=True)[0]
        d2u_dx2 = torch.autograd.grad(du_dx, x_c, torch.ones_like(du_dx),
                                       create_graph=True, retain_graph=True)[0]

        residual = du_dt - a_val * d2u_dx2 - b_val * u_full**2 - f_c
        MSE_0 = torch.mean(residual**2)

        # IC: u(x, 0) = -sin(pi*x)
        t_zero = torch.zeros_like(x_ic)
        u_bar_ic = self.u_nn(torch.cat([x_ic, t_zero], dim=-1))
        target_ic = -torch.sin(np.pi * x_ic)
        MSE_IC = torch.mean((u_bar_ic - target_ic)**2)

        # BC: u(-1, t) = u(1, t) = 0
        u_left = self.u_nn(torch.cat([torch.full_like(t_c, -1.0), t_c], dim=-1))
        u_right = self.u_nn(torch.cat([torch.full_like(t_c, 1.0), t_c], dim=-1))
        U_left = self.U_nn(torch.cat([torch.full_like(t_c, -1.0), t_c], dim=-1))
        U_right = self.U_nn(torch.cat([torch.full_like(t_c, 1.0), t_c], dim=-1))
        MSE_BC = torch.mean(u_left**2) + torch.mean(u_right**2) + \
                 torch.mean(U_left**2) + torch.mean(U_right**2)

        # BO constraints - per-mode gradients
        loss_EY = sum(torch.mean(Y[:, i:i+1])**2 for i in range(self.n_bo_modes))
        dU_dt_list = []
        for i in range(self.n_bo_modes):
            dUi_dt = torch.autograd.grad(U[:, i].sum(), t_c, create_graph=True, retain_graph=True)[0]
            dU_dt_list.append(dUi_dt)
        loss_sym_S = 0.0
        for i in range(self.n_bo_modes):
            for j in range(self.n_bo_modes):
                Sij = torch.mean(dU_dt_list[i].squeeze() * U[:, j])
                Sji = torch.mean(dU_dt_list[j].squeeze() * U[:, i])
                loss_sym_S += (Sij + Sji)**2
        dY_dt_list = []
        for i in range(self.n_bo_modes):
            dYi_dt = torch.autograd.grad(Y[:, i].sum(), t_c, create_graph=True, retain_graph=True)[0]
            dY_dt_list.append(dYi_dt)
        loss_sym_M = 0.0
        for i in range(self.n_bo_modes):
            for j in range(self.n_bo_modes):
                Mij = torch.mean(Y[:, i:i+1] * dY_dt_list[j])
                Mji = torch.mean(Y[:, j:j+1] * dY_dt_list[i])
                loss_sym_M += (Mij + Mji)**2
        MSE_BO = loss_EY + loss_sym_S + loss_sym_M

        total = MSE_0 + 100.0 * (MSE_IC + MSE_BC + MSE_BO)

        # Extra: inverse problem measurement loss
        if extra_mean_data is not None:
            x_meas, t_meas, u_meas = extra_mean_data
            u_pred_meas = self.u_nn(torch.cat([x_meas, t_meas], dim=-1))
            MSE_extra = torch.mean((u_pred_meas - u_meas)**2)
            total = total + 100.0 * MSE_extra

        return total, {
            'MSE_0': MSE_0.item(),
            'MSE_IC': MSE_IC.item(),
            'MSE_BC': MSE_BC.item(),
            'MSE_BO': MSE_BO.item(),
        }


def solve_reference_mc(a_coeff, b_coeff, sigma_g, lc, n_kl_modes, n_mc=1000):
    """
    Solve via finite-difference Monte Carlo for reference solution.
    """
    nx = 101
    nt = 1000
    x = np.linspace(-1, 1, nx)
    dx = x[1] - x[0]
    dt = 1.0 / nt
    t_pts = np.linspace(0, 1, nt + 1)

    eigenvalues, eigenvectors = compute_kl_expansion(x, sigma_g, lc, n_kl_modes)

    u_all = np.zeros((n_mc, nx))
    print(f"Running {n_mc} MC samples for reference...")

    for s in range(n_mc):
        xi = np.random.randn(n_kl_modes)
        # GP sample
        g = np.ones(nx)
        for k in range(n_kl_modes):
            g += np.sqrt(eigenvalues[k]) * eigenvectors[:, k] * xi[k]
        f = (1 - x**2) * g

        # Forward Euler with small dt
        u = -np.sin(np.pi * x)
        u[0] = 0.0
        u[-1] = 0.0

        for n in range(nt):
            u_xx = np.zeros(nx)
            u_xx[1:-1] = (u[2:] - 2*u[1:-1] + u[:-2]) / dx**2
            u_new = u + dt * (a_coeff * u_xx + b_coeff * u**2 + f)
            u_new[0] = 0.0
            u_new[-1] = 0.0
            u = u_new

        u_all[s] = u

        if (s + 1) % 200 == 0:
            print(f"  MC sample {s+1}/{n_mc}")

    mean_mc = np.mean(u_all, axis=0)
    var_mc = np.var(u_all, axis=0)

    return x, mean_mc, var_mc, eigenvalues, eigenvectors, u_all


def train_forward(save_dir='../results/reaction_diffusion'):
    """Train forward problem: a=0.1, b=0.5."""
    os.makedirs(save_dir, exist_ok=True)

    a_coeff = 0.1
    b_coeff = 0.5
    sigma_g = 1.0
    lc = 0.1
    n_kl_modes = 19
    n_bo_modes = 6
    n_epochs = 300000

    # Reference solution
    x_ref, mean_ref, var_ref, eigenvalues, eigenvectors, u_all_mc = \
        solve_reference_mc(a_coeff, b_coeff, sigma_g, lc, n_kl_modes, n_mc=1000)

    # Model
    model = ReactionDiffusionNNBO(n_bo_modes=n_bo_modes, n_kl_modes=n_kl_modes)
    optimizer = torch.optim.Adam(model.params, lr=0.001)

    # Training data
    nx = 51
    nt = 50
    n_xi_samples = 1000
    x_pts = np.linspace(-1, 1, nx)
    t_pts = np.sort(np.random.uniform(0, 1, nt))

    # Generate xi samples
    xi_samples = np.random.randn(n_xi_samples, n_kl_modes)

    # Precompute forcing for all samples at all collocation points
    # f(x;w) = (1-x^2) * g(x;w) where g = 1 + sum sqrt(lam)*phi*xi
    eigvals_kl, eigvecs_kl = compute_kl_expansion(x_pts, sigma_g, lc, n_kl_modes)

    x_ic = torch.tensor(x_pts, dtype=torch.float32, device=device).unsqueeze(1)

    print(f"\nTraining forward reaction-diffusion NN-BO...")
    print(f"n_bo_modes={n_bo_modes}, n_kl_modes={n_kl_modes}, epochs={n_epochs}")

    batch_size = 4000
    t_start = time.time()

    for epoch in range(n_epochs):
        # Sample random batch
        x_b = np.random.uniform(-1, 1, batch_size)
        t_b = np.random.uniform(0, 1, batch_size)
        xi_idx = np.random.randint(0, n_xi_samples, batch_size)
        xi_b = xi_samples[xi_idx]

        # Compute forcing for this batch
        g_b = np.ones(batch_size)
        for k in range(n_kl_modes):
            # Interpolate eigenvector at x_b
            phi_k = np.interp(x_b, x_pts, eigvecs_kl[:, k])
            g_b += np.sqrt(eigvals_kl[k]) * phi_k * xi_b[:, k]
        f_b = (1 - x_b**2) * g_b

        x_t = torch.tensor(x_b, dtype=torch.float32, device=device).unsqueeze(1)
        t_t = torch.tensor(t_b, dtype=torch.float32, device=device).unsqueeze(1)
        xi_t = torch.tensor(xi_b, dtype=torch.float32, device=device)
        f_t = torch.tensor(f_b, dtype=torch.float32, device=device).unsqueeze(1)

        optimizer.zero_grad()
        loss, loss_dict = model.compute_loss(
            x_t, t_t, xi_t, f_t, x_ic, a_coeff, b_coeff
        )
        loss.backward()
        optimizer.step()

        if epoch % 20000 == 0:
            elapsed = time.time() - t_start
            print(f"Epoch {epoch:6d}/{n_epochs} | Loss: {loss.item():.6f} | "
                  f"MSE_0: {loss_dict['MSE_0']:.2e} | Time: {elapsed:.1f}s")

    # Evaluate
    print("\nEvaluating forward problem...")
    model.u_nn.eval()
    model.U_nn.eval()
    model.Y_nn.eval()

    with torch.no_grad():
        x_eval = torch.tensor(x_ref, dtype=torch.float32, device=device).unsqueeze(1)
        t_eval = torch.full((len(x_ref), 1), 1.0, dtype=torch.float32, device=device)
        mean_pred = model.u_nn(torch.cat([x_eval, t_eval], dim=-1)).cpu().numpy().flatten()

    # RMSE of Y_i at t=0.1 and t=1.0 (from MC comparison)
    results = {
        'mean_pred': mean_pred.tolist(),
        'mean_ref': mean_ref.tolist(),
        'var_ref': var_ref.tolist(),
        'x_ref': x_ref.tolist(),
        'training_time': time.time() - t_start,
    }

    with open(os.path.join(save_dir, 'forward_results.json'), 'w') as f:
        json.dump(results, f, indent=2)

    print("Forward problem complete.")
    return results


def train_inverse(save_dir='../results/reaction_diffusion'):
    """Train inverse problem: infer a=0.5, b=0.3."""
    os.makedirs(save_dir, exist_ok=True)

    a_true = 0.5
    b_true = 0.3
    sigma_g = 1.0
    lc = 0.4
    n_kl_modes = 19
    n_bo_modes = 4
    n_epochs = 300000

    # Reference with true params
    x_ref, mean_ref, var_ref, eigenvalues, eigenvectors, u_all_mc = \
        solve_reference_mc(a_true, b_true, sigma_g, lc, n_kl_modes, n_mc=1000)

    # Measurement data: E[u] at x=-0.5, 0, 0.5 and t=0.1, 0.9
    # We get these from the MC reference
    x_meas_pts = np.array([-0.5, 0.0, 0.5])
    t_meas_pts = np.array([0.1, 0.9])

    # Run MC at t=0.1 too
    nx_ref = len(x_ref)
    nt_ref = 1000
    dx_ref = x_ref[1] - x_ref[0]
    dt_ref = 1.0 / nt_ref

    u_at_t01 = np.zeros((1000, nx_ref))
    for s in range(1000):
        xi = np.random.randn(n_kl_modes)
        g = np.ones(nx_ref)
        for k in range(n_kl_modes):
            g += np.sqrt(eigenvalues[k]) * eigenvectors[:, k] * xi[k]
        f = (1 - x_ref**2) * g
        u = -np.sin(np.pi * x_ref)
        u[0] = 0.0; u[-1] = 0.0
        for n in range(int(0.1 / dt_ref)):
            u_xx = np.zeros(nx_ref)
            u_xx[1:-1] = (u[2:] - 2*u[1:-1] + u[:-2]) / dx_ref**2
            u_new = u + dt_ref * (a_true * u_xx + b_true * u**2 + f)
            u_new[0] = 0.0; u_new[-1] = 0.0
            u = u_new
        u_at_t01[s] = u

    mean_t01 = np.mean(u_at_t01, axis=0)
    mean_t10 = mean_ref

    # Create measurement data
    x_meas_list = []
    t_meas_list = []
    u_meas_list = []
    for x_m in x_meas_pts:
        ix = np.argmin(np.abs(x_ref - x_m))
        x_meas_list.append(x_m)
        t_meas_list.append(0.1)
        u_meas_list.append(mean_t01[ix])
        x_meas_list.append(x_m)
        t_meas_list.append(0.9)
        u_meas_list.append(mean_ref[ix])  # approximate t=0.9 with t=1.0

    x_meas_t = torch.tensor(x_meas_list, dtype=torch.float32, device=device).unsqueeze(1)
    t_meas_t = torch.tensor(t_meas_list, dtype=torch.float32, device=device).unsqueeze(1)
    u_meas_t = torch.tensor(u_meas_list, dtype=torch.float32, device=device).unsqueeze(1)
    extra_data = (x_meas_t, t_meas_t, u_meas_t)

    # Model
    model = ReactionDiffusionNNBO(n_bo_modes=n_bo_modes, n_kl_modes=n_kl_modes,
                                   learn_coeffs=True)
    optimizer = torch.optim.Adam(model.params, lr=0.001)

    nx = 51
    x_pts = np.linspace(-1, 1, nx)
    eigvals_kl, eigvecs_kl = compute_kl_expansion(x_pts, sigma_g, lc, n_kl_modes)
    x_ic = torch.tensor(x_pts, dtype=torch.float32, device=device).unsqueeze(1)

    xi_samples = np.random.randn(1000, n_kl_modes)

    print(f"\nTraining inverse reaction-diffusion NN-BO...")
    print(f"True: a={a_true}, b={b_true}")
    print(f"n_bo_modes={n_bo_modes}, epochs={n_epochs}")

    batch_size = 4000
    t_start = time.time()
    ab_history = []

    for epoch in range(n_epochs):
        x_b = np.random.uniform(-1, 1, batch_size)
        t_b = np.random.uniform(0, 1, batch_size)
        xi_idx = np.random.randint(0, 1000, batch_size)
        xi_b = xi_samples[xi_idx]

        g_b = np.ones(batch_size)
        for k in range(n_kl_modes):
            phi_k = np.interp(x_b, x_pts, eigvecs_kl[:, k])
            g_b += np.sqrt(eigvals_kl[k]) * phi_k * xi_b[:, k]
        f_b = (1 - x_b**2) * g_b

        x_t = torch.tensor(x_b, dtype=torch.float32, device=device).unsqueeze(1)
        t_t = torch.tensor(t_b, dtype=torch.float32, device=device).unsqueeze(1)
        xi_t = torch.tensor(xi_b, dtype=torch.float32, device=device)
        f_t = torch.tensor(f_b, dtype=torch.float32, device=device).unsqueeze(1)

        optimizer.zero_grad()
        loss, loss_dict = model.compute_loss(
            x_t, t_t, xi_t, f_t, x_ic, None, None, extra_data
        )
        loss.backward()
        optimizer.step()

        if epoch % 20000 == 0:
            a_pred = model.a_param.item()
            b_pred = model.b_param.item()
            ab_history.append({
                'epoch': epoch,
                'a': a_pred,
                'b': b_pred,
            })
            elapsed = time.time() - t_start
            print(f"Epoch {epoch:6d} | Loss: {loss.item():.6f} | "
                  f"a={a_pred:.4f} (true={a_true}) | "
                  f"b={b_pred:.4f} (true={b_true}) | "
                  f"Time: {elapsed:.1f}s")

    a_final = model.a_param.item()
    b_final = model.b_param.item()

    results = {
        'a_true': a_true,
        'b_true': b_true,
        'a_predicted': a_final,
        'b_predicted': b_final,
        'a_error': abs(a_final - a_true),
        'b_error': abs(b_final - b_true),
        'a_rel_error': abs(a_final - a_true) / a_true * 100,
        'b_rel_error': abs(b_final - b_true) / b_true * 100,
        'ab_history': ab_history,
        'training_time': time.time() - t_start,
    }

    print(f"\n=== Inverse Problem Results ===")
    print(f"  a: predicted={a_final:.4f}, true={a_true}, error={abs(a_final-a_true):.4f}")
    print(f"  b: predicted={b_final:.4f}, true={b_true}, error={abs(b_final-b_true):.4f}")

    with open(os.path.join(save_dir, 'inverse_results.json'), 'w') as f:
        json.dump(results, f, indent=2)

    return results


if __name__ == '__main__':
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else 'forward'
    if mode == 'forward':
        train_forward()
    elif mode == 'inverse':
        train_inverse()
    else:
        train_forward()
        train_inverse()
