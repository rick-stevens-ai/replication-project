"""Quick evaluation of Example 3 forward + inverse."""
import os, sys, json, time, warnings
import numpy as np
import torch
import torch.nn as nn
warnings.filterwarnings('ignore')

sys.path.insert(0, '.')
from example3_reaction_diffusion_pinn import (
    ModifiedMLP, compute_kl_expansion, generate_ic,
    solve_rd_reference, N_KL, SIGMA_KL, L_KL, A_TRUE, B_TRUE
)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Device: {device}")

# Load forward model
eigenvalues, eigenfunctions, x_kl = compute_kl_expansion(N_KL, 200, SIGMA_KL, L_KL)
input_dim = 2 + N_KL
net = ModifiedMLP(input_dim=input_dim, output_dim=1, n_layers=6, hidden_dim=160).to(device)
net.load_state_dict(torch.load('results/best_rd_forward.pt', map_location=device))
net.eval()
print("Forward model loaded.")

# MC evaluation of PINN
n_mc = 1000
x_eval = np.linspace(0, 1, 100)
print(f"\nPINN MC evaluation ({n_mc} samples)...")
all_u = []
with torch.no_grad():
    for i in range(n_mc):
        xi = np.random.randn(1, N_KL)
        xi_rep = np.tile(xi, (len(x_eval), 1))
        inp = np.column_stack([x_eval, np.ones_like(x_eval), xi_rep])
        inp_t = torch.tensor(inp, dtype=torch.float32, device=device)
        u = net(inp_t).cpu().numpy().flatten()
        all_u.append(u)

all_u = np.array(all_u)
E_u = np.mean(all_u, axis=0)
Var_u = np.var(all_u, axis=0)
print(f"  PINN E[u] range: [{E_u.min():.6f}, {E_u.max():.6f}]")
print(f"  PINN Var[u] range: [{Var_u.min():.6f}, {Var_u.max():.6f}]")

# FD reference - use fewer samples and coarser grid
n_ref = 200
print(f"\nFD reference ({n_ref} samples, nx=101)...")
t0 = time.time()
u_ref = np.zeros((len(x_eval), n_ref))
for j in range(n_ref):
    xi = np.random.randn(1, N_KL)
    u0 = generate_ic(x_eval, np.tile(xi, (len(x_eval), 1)), eigenvalues, eigenfunctions, x_kl)
    u_ref[:, j] = solve_rd_reference(A_TRUE, B_TRUE, x_eval, 1.0, u0, nx_fine=101)

# Filter NaN
valid = ~np.any(np.isnan(u_ref), axis=0)
if valid.sum() < n_ref:
    print(f"  Warning: {n_ref - valid.sum()}/{n_ref} samples had NaN")
u_ref = u_ref[:, valid]
print(f"  FD reference time: {time.time()-t0:.0f}s")

E_ref = np.mean(u_ref, axis=1)
Var_ref = np.var(u_ref, axis=1)
print(f"  FD E[u] range: [{E_ref.min():.6f}, {E_ref.max():.6f}]")
print(f"  FD Var[u] range: [{Var_ref.min():.6f}, {Var_ref.max():.6f}]")

dx = x_eval[1] - x_eval[0]
rel_E = np.sqrt(np.sum((E_u - E_ref)**2)*dx) / max(np.sqrt(np.sum(E_ref**2)*dx), 1e-15) * 100
rel_V = np.sqrt(np.sum((Var_u - Var_ref)**2)*dx) / max(np.sqrt(np.sum(Var_ref**2)*dx), 1e-15) * 100
print(f"\n  E[u] rel L2 vs FD: {rel_E:.4f}%")
print(f"  Var[u] rel L2 vs FD: {rel_V:.4f}%")

# Now do inverse problem
print("\n" + "="*50)
print("INVERSE PROBLEM")
print("="*50)

# Generate observations with FD
n_obs = 100
print(f"Generating {n_obs} observations...")
x_obs = np.random.rand(n_obs)
t_obs = np.random.rand(n_obs)
xi_obs = np.random.randn(n_obs, N_KL)
u_obs = np.zeros(n_obs)
for i in range(n_obs):
    x_fine = np.linspace(0, 1, 101)
    u0 = generate_ic(x_fine, xi_obs[i:i+1].repeat(101, axis=0), eigenvalues, eigenfunctions, x_kl)
    u_solved = solve_rd_reference(A_TRUE, B_TRUE, x_fine, t_obs[i], u0, nx_fine=101)
    u_obs[i] = np.interp(x_obs[i], x_fine, u_solved)

valid_obs = ~np.isnan(u_obs)
if valid_obs.sum() < n_obs:
    print(f"  Warning: {n_obs - valid_obs.sum()}/{n_obs} NaN obs filtered")
    x_obs = x_obs[valid_obs]
    t_obs = t_obs[valid_obs]
    xi_obs = xi_obs[valid_obs]
    u_obs = u_obs[valid_obs]
    n_obs = len(u_obs)
print(f"  {n_obs} valid observations. u range: [{u_obs.min():.4f}, {u_obs.max():.4f}]")

# Train inverse
net_inv = ModifiedMLP(input_dim=input_dim, output_dim=1, n_layers=6, hidden_dim=160).to(device)
log_a = nn.Parameter(torch.tensor(0.0, device=device))
log_b = nn.Parameter(torch.tensor(0.0, device=device))
all_params = list(net_inv.parameters()) + [log_a, log_b]
opt = torch.optim.Adam(all_params, lr=1e-3)
sched = torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(opt, T_0=10000, eta_min=1e-6)

# Convert obs to tensors
x_obs_t = torch.tensor(x_obs, dtype=torch.float32, device=device).unsqueeze(1)
t_obs_t = torch.tensor(t_obs, dtype=torch.float32, device=device).unsqueeze(1)
xi_obs_t = torch.tensor(xi_obs, dtype=torch.float32, device=device)
u_obs_t = torch.tensor(u_obs, dtype=torch.float32, device=device).unsqueeze(1)

print("Training inverse (40000 epochs)...")
best_loss = float('inf')
for ep in range(1, 40001):
    # PDE collocation
    x_p = torch.rand(5000, 1, device=device, requires_grad=True)
    t_p = torch.rand(5000, 1, device=device, requires_grad=True)
    xi_p = torch.randn(5000, N_KL, device=device)
    inp_p = torch.cat([x_p, t_p, xi_p], dim=1)
    u = net_inv(inp_p)
    
    du_dt = torch.autograd.grad(u, t_p, torch.ones_like(u), create_graph=True)[0]
    du_dx = torch.autograd.grad(u, x_p, torch.ones_like(u), create_graph=True)[0]
    d2u_dx2 = torch.autograd.grad(du_dx, x_p, torch.ones_like(du_dx), create_graph=True)[0]
    
    a_val = torch.exp(log_a)
    b_val = torch.exp(log_b)
    pde_res = du_dt - a_val * d2u_dx2 - b_val * u * (1 - u)
    loss_pde = (pde_res**2).mean()
    
    # Data loss
    inp_obs = torch.cat([x_obs_t, t_obs_t, xi_obs_t], dim=1)
    u_pred = net_inv(inp_obs)
    loss_data = ((u_pred - u_obs_t)**2).mean()
    
    # IC
    x_ic = torch.rand(2000, 1, device=device)
    xi_ic = torch.randn(2000, N_KL, device=device)
    t_zero = torch.zeros(2000, 1, device=device)
    inp_ic = torch.cat([x_ic, t_zero, xi_ic], dim=1)
    u_ic = net_inv(inp_ic)
    
    x_np = x_ic.detach().cpu().numpy()
    xi_np = xi_ic.detach().cpu().numpy()
    u0_exact = generate_ic(x_np.flatten(), xi_np, eigenvalues, eigenfunctions, x_kl)
    u0_t = torch.tensor(u0_exact, dtype=torch.float32, device=device).unsqueeze(1)
    loss_ic = ((u_ic - u0_t)**2).mean()
    
    # BC: Neumann du/dx=0 at x=0,1
    x_bc0 = torch.zeros(500, 1, device=device, requires_grad=True)
    x_bc1 = torch.ones(500, 1, device=device, requires_grad=True)
    t_bc = torch.rand(500, 1, device=device)
    xi_bc = torch.randn(500, N_KL, device=device)
    
    u_bc0 = net_inv(torch.cat([x_bc0, t_bc, xi_bc], dim=1))
    du0 = torch.autograd.grad(u_bc0, x_bc0, torch.ones_like(u_bc0), create_graph=True)[0]
    u_bc1 = net_inv(torch.cat([x_bc1, t_bc, xi_bc], dim=1))
    du1 = torch.autograd.grad(u_bc1, x_bc1, torch.ones_like(u_bc1), create_graph=True)[0]
    loss_bc = (du0**2).mean() + (du1**2).mean()
    
    loss = loss_pde + 10*loss_data + 10*loss_ic + loss_bc
    
    opt.zero_grad()
    loss.backward()
    torch.nn.utils.clip_grad_norm_(all_params, 1.0)
    opt.step()
    sched.step()
    
    if loss.item() < best_loss:
        best_loss = loss.item()
        best_a = a_val.item()
        best_b = b_val.item()
        torch.save(net_inv.state_dict(), 'results/best_rd_inverse.pt')
    
    if ep % 10000 == 0:
        print(f"  Ep {ep} | L={loss.item():.3e} PDE={loss_pde.item():.3e} "
              f"Data={loss_data.item():.3e} IC={loss_ic.item():.3e} | "
              f"a={a_val.item():.4f} (true={A_TRUE}) b={b_val.item():.4f} (true={B_TRUE})")

print(f"\nBest recovered: a={best_a:.6f} (true={A_TRUE}), b={best_b:.6f} (true={B_TRUE})")
print(f"  a error: {abs(best_a - A_TRUE)/A_TRUE*100:.2f}%")
print(f"  b error: {abs(best_b - B_TRUE)/B_TRUE*100:.2f}%")

# Save all results
results = {
    'forward': {
        'E_relL2_vs_FD': float(rel_E),
        'Var_relL2_vs_FD': float(rel_V),
        'E_u_range': [float(E_u.min()), float(E_u.max())],
        'Var_u_range': [float(Var_u.min()), float(Var_u.max())],
    },
    'inverse': {
        'a_true': A_TRUE, 'b_true': B_TRUE,
        'a_recovered': best_a, 'b_recovered': best_b,
        'a_error_pct': abs(best_a - A_TRUE)/A_TRUE*100,
        'b_error_pct': abs(best_b - B_TRUE)/B_TRUE*100,
    }
}
with open('results/example3_result.json', 'w') as f:
    json.dump(results, f, indent=2)
print(f"\nResults saved to results/example3_result.json")
