#!/usr/bin/env python3
"""
Run PINN experiments using penalized loss (standard approach) instead of
penalty-free BC enforcement. This allows us to test the SPQN preconditioning
claims independently of the BC enforcement implementation.

Usage: CUDA_VISIBLE_DEVICES=0 python3 -u run_penalized.py
"""

import sys
import os
import json
import time
import numpy as np
import torch
import torch.nn as nn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pinn_model import ResNetPINN
from problems import hammersley_sequence
from scipy_lbfgs import ScipyLBFGS, ScipyLBFGSSubset

RESULTS_DIR = '/data/stevens/projects-active/pinn-dd-precond/results'
os.makedirs(RESULTS_DIR, exist_ok=True)


def save_json(data, filename):
    def convert(obj):
        if isinstance(obj, (np.floating, np.integer)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, torch.Tensor):
            return obj.item()
        return obj
    with open(os.path.join(RESULTS_DIR, filename), 'w') as f:
        json.dump(data, f, indent=2, default=convert)


# ============================================================
# Problem definitions with penalized loss
# ============================================================

class PenalizedProblem:
    """Base class for problems using penalized BC enforcement."""

    def __init__(self, device='cuda'):
        self.device = device
        self._generate_data()

    def _generate_data(self):
        raise NotImplementedError

    def compute_loss(self, model):
        """Compute total loss = PDE residual + lambda * BC loss."""
        raise NotImplementedError

    def compute_error(self, model, n_test=10000):
        """Compute E_rel if reference is available."""
        return None


class BurgersP(PenalizedProblem):
    name = "Burgers"
    depth, width = 8, 20
    input_dim, output_dim = 2, 1
    nu = 0.01 / np.pi

    def _generate_data(self):
        n_int = 10000
        pts = hammersley_sequence(n_int, 2)
        self.X_int = torch.tensor(
            np.column_stack([pts[:, 0], pts[:, 1] * 2 - 1]),
            dtype=torch.float32, device=self.device
        )
        # IC: t=0
        n_bc = 500
        x_ic = torch.linspace(-1, 1, n_bc, device=self.device)
        self.X_ic = torch.stack([torch.zeros(n_bc, device=self.device), x_ic], dim=1)
        self.u_ic = -torch.sin(np.pi * x_ic).unsqueeze(1)
        # Left/right BC
        t_bc = torch.linspace(0.001, 1, n_bc, device=self.device)
        self.X_left = torch.stack([t_bc, -torch.ones(n_bc, device=self.device)], dim=1)
        self.X_right = torch.stack([t_bc, torch.ones(n_bc, device=self.device)], dim=1)
        self.lam = 100.0  # BC penalty weight

    def compute_loss(self, model):
        X = self.X_int.detach().requires_grad_(True)
        u = model(X)
        gu = torch.autograd.grad(u, X, torch.ones_like(u), create_graph=True)[0]
        u_t, u_x = gu[:, 0:1], gu[:, 1:2]
        gux = torch.autograd.grad(u_x, X, torch.ones_like(u_x), create_graph=True)[0]
        u_xx = gux[:, 1:2]
        res = u_t + u * u_x - self.nu * u_xx
        L_pde = torch.mean(res ** 2)

        L_ic = torch.mean((model(self.X_ic) - self.u_ic) ** 2)
        L_bc = torch.mean(model(self.X_left) ** 2) + torch.mean(model(self.X_right) ** 2)

        return L_pde + self.lam * (L_ic + L_bc)

    def compute_error(self, model, n_test=10000):
        try:
            from reference_solutions import burgers_reference
            interp, _, _, _ = burgers_reference()
            with torch.no_grad():
                pts = hammersley_sequence(n_test, 2)
                X = torch.tensor(np.column_stack([pts[:, 0], pts[:, 1] * 2 - 1]),
                                 dtype=torch.float32, device=self.device)
                u_pred = model(X)
                u_ref = torch.tensor(interp(X.cpu().numpy()), dtype=torch.float32,
                                     device=self.device).reshape(-1, 1)
                return (torch.norm(u_pred - u_ref) / (torch.norm(u_pred) + 1e-30)).item()
        except:
            return None


class KleinGordonP(PenalizedProblem):
    name = "Klein-Gordon"
    depth, width = 6, 50
    input_dim, output_dim = 2, 1

    def _generate_data(self):
        n_int = 10000
        pts = hammersley_sequence(n_int, 2)
        self.X_int = torch.tensor(
            np.column_stack([pts[:, 0] * 12, pts[:, 1] * 2 - 1]),
            dtype=torch.float32, device=self.device
        )
        n_bc = 500
        # IC: t=0, u=x
        x_ic = torch.linspace(-1, 1, n_bc, device=self.device)
        self.X_ic = torch.stack([torch.zeros(n_bc, device=self.device), x_ic], dim=1)
        self.u_ic = x_ic.unsqueeze(1)
        # IC velocity: t=0, u_t=0
        self.X_ic_v = self.X_ic.clone()
        # Left BC: x=-1, u=-cos(t)
        t_bc = torch.linspace(0.01, 12, n_bc, device=self.device)
        self.X_left = torch.stack([t_bc, -torch.ones(n_bc, device=self.device)], dim=1)
        self.u_left = -torch.cos(t_bc).unsqueeze(1)
        # Right BC: x=1, u=cos(t)
        self.X_right = torch.stack([t_bc, torch.ones(n_bc, device=self.device)], dim=1)
        self.u_right = torch.cos(t_bc).unsqueeze(1)
        self.lam = 100.0

    def compute_loss(self, model):
        X = self.X_int.detach().requires_grad_(True)
        u = model(X)
        gu = torch.autograd.grad(u, X, torch.ones_like(u), create_graph=True)[0]
        u_t, u_x = gu[:, 0:1], gu[:, 1:2]
        gut = torch.autograd.grad(u_t, X, torch.ones_like(u_t), create_graph=True)[0]
        u_tt = gut[:, 0:1]
        gux = torch.autograd.grad(u_x, X, torch.ones_like(u_x), create_graph=True)[0]
        u_xx = gux[:, 1:2]

        t, x = X[:, 0:1], X[:, 1:2]
        f = -x * torch.cos(t) + x ** 2 * torch.cos(t) ** 2
        res = u_tt - u_xx + u ** 2 - f
        L_pde = torch.mean(res ** 2)

        L_ic = torch.mean((model(self.X_ic) - self.u_ic) ** 2)

        # IC velocity
        X_v = self.X_ic_v.detach().requires_grad_(True)
        u_v = model(X_v)
        gu_v = torch.autograd.grad(u_v, X_v, torch.ones_like(u_v), create_graph=True)[0]
        L_icv = torch.mean(gu_v[:, 0:1] ** 2)

        L_left = torch.mean((model(self.X_left) - self.u_left) ** 2)
        L_right = torch.mean((model(self.X_right) - self.u_right) ** 2)

        return L_pde + self.lam * (L_ic + L_icv + L_left + L_right)

    def compute_error(self, model, n_test=10000):
        with torch.no_grad():
            pts = hammersley_sequence(n_test, 2)
            X = torch.tensor(np.column_stack([pts[:, 0] * 12, pts[:, 1] * 2 - 1]),
                             dtype=torch.float32, device=self.device)
            u_pred = model(X)
            t, x = X[:, 0:1], X[:, 1:2]
            u_exact = x * torch.cos(t)
            return (torch.norm(u_pred - u_exact) / (torch.norm(u_pred) + 1e-30)).item()


class AllenCahnP(PenalizedProblem):
    name = "Allen-Cahn"
    depth, width = 6, 64
    input_dim, output_dim = 2, 1
    D = 0.001

    def _generate_data(self):
        n_int = 10000
        pts = hammersley_sequence(n_int, 2)
        self.X_int = torch.tensor(
            np.column_stack([pts[:, 0], pts[:, 1] * 2 - 1]),
            dtype=torch.float32, device=self.device
        )
        n_bc = 500
        x_ic = torch.linspace(-1, 1, n_bc, device=self.device)
        self.X_ic = torch.stack([torch.zeros(n_bc, device=self.device), x_ic], dim=1)
        self.u_ic = (x_ic ** 2 * torch.cos(np.pi * x_ic)).unsqueeze(1)

        t_bc = torch.linspace(0.001, 1, n_bc, device=self.device)
        self.X_left = torch.stack([t_bc, -torch.ones(n_bc, device=self.device)], dim=1)
        self.X_right = torch.stack([t_bc, torch.ones(n_bc, device=self.device)], dim=1)
        self.lam = 100.0

    def compute_loss(self, model):
        X = self.X_int.detach().requires_grad_(True)
        u = model(X)
        gu = torch.autograd.grad(u, X, torch.ones_like(u), create_graph=True)[0]
        u_t, u_x = gu[:, 0:1], gu[:, 1:2]
        gux = torch.autograd.grad(u_x, X, torch.ones_like(u_x), create_graph=True)[0]
        u_xx = gux[:, 1:2]
        res = u_t - self.D * u_xx - 5 * (u - u ** 3)
        L_pde = torch.mean(res ** 2)

        L_ic = torch.mean((model(self.X_ic) - self.u_ic) ** 2)
        L_left = torch.mean((model(self.X_left) + 1) ** 2)
        L_right = torch.mean((model(self.X_right) + 1) ** 2)

        return L_pde + self.lam * (L_ic + L_left + L_right)

    def compute_error(self, model, n_test=10000):
        try:
            from reference_solutions import allen_cahn_reference
            interp, _, _, _ = allen_cahn_reference()
            with torch.no_grad():
                pts = hammersley_sequence(n_test, 2)
                X = torch.tensor(np.column_stack([pts[:, 0], pts[:, 1] * 2 - 1]),
                                 dtype=torch.float32, device=self.device)
                u_pred = model(X)
                u_ref = torch.tensor(interp(X.cpu().numpy()), dtype=torch.float32,
                                     device=self.device).reshape(-1, 1)
                return (torch.norm(u_pred - u_ref) / (torch.norm(u_pred) + 1e-30)).item()
        except:
            return None


class AdvDiffP(PenalizedProblem):
    name = "Advection-Diffusion"
    depth, width = 10, 50
    input_dim, output_dim = 2, 1
    mu = 1e-2

    def _generate_data(self):
        n_int = 10000
        pts = hammersley_sequence(n_int, 2)
        self.X_int = torch.tensor(pts, dtype=torch.float32, device=self.device)

        n_bc = 500
        # 4 boundaries of [0,1]^2
        s = torch.linspace(0.001, 0.999, n_bc, device=self.device)
        self.X_bc = torch.cat([
            torch.stack([torch.zeros(n_bc, device=self.device), s], dim=1),
            torch.stack([torch.ones(n_bc, device=self.device), s], dim=1),
            torch.stack([s, torch.zeros(n_bc, device=self.device)], dim=1),
            torch.stack([s, torch.ones(n_bc, device=self.device)], dim=1),
        ], dim=0)
        self.lam = 100.0

    def compute_loss(self, model):
        X = self.X_int.detach().requires_grad_(True)
        u = model(X)
        gu = torch.autograd.grad(u, X, torch.ones_like(u), create_graph=True)[0]
        u_x1, u_x2 = gu[:, 0:1], gu[:, 1:2]
        gux1 = torch.autograd.grad(u_x1, X, torch.ones_like(u_x1), create_graph=True)[0]
        u_x1x1 = gux1[:, 0:1]
        gux2 = torch.autograd.grad(u_x2, X, torch.ones_like(u_x2), create_graph=True)[0]
        u_x2x2 = gux2[:, 1:2]
        res = -self.mu * (u_x1x1 + u_x2x2) + u_x1 + u_x2 - 1.0
        L_pde = torch.mean(res ** 2)

        L_bc = torch.mean(model(self.X_bc) ** 2)

        return L_pde + self.lam * L_bc

    def compute_error(self, model, n_test=10000):
        try:
            from reference_solutions import advection_diffusion_reference
            interp, _, _, _ = advection_diffusion_reference()
            with torch.no_grad():
                pts = hammersley_sequence(n_test, 2)
                X = torch.tensor(pts, dtype=torch.float32, device=self.device)
                u_pred = model(X)
                u_ref = torch.tensor(interp(X.cpu().numpy()), dtype=torch.float32,
                                     device=self.device).reshape(-1, 1)
                return (torch.norm(u_pred - u_ref) / (torch.norm(u_pred) + 1e-30)).item()
        except:
            return None


PROBLEMS_P = {
    'klein_gordon': KleinGordonP,
    'burgers': BurgersP,
    'allen_cahn': AllenCahnP,
    'advection_diffusion': AdvDiffP,
}


# ============================================================
# Training functions
# ============================================================

def train_scipy_lbfgs(model, problem, maxiter=10000, m=3):
    """Standard L-BFGS baseline using scipy."""
    loss_fn = lambda: problem.compute_loss(model)
    opt = ScipyLBFGS(model, loss_fn, maxiter=maxiter, m=m)

    t0 = time.time()
    checkpoints = []

    def cb(x):
        n = opt._iter_count
        if n % max(1, maxiter // 20) == 0:
            e = problem.compute_error(model)
            elapsed = time.time() - t0
            loss = opt.loss_history[-1]
            checkpoints.append({'iter': n, 'loss': loss, 'e_rel': e, 'time': elapsed})
            e_str = f", E_rel={e:.4e}" if e is not None else ""
            print(f"  L-BFGS {n:6d}: loss={loss:.4e}{e_str} | {elapsed:.1f}s")

    result = opt.optimize(callback=cb)
    elapsed = time.time() - t0
    final_e = problem.compute_error(model)

    print(f"  scipy: {result.message}, nit={result.nit}")
    e_str = f"{final_e:.4e}" if final_e is not None else "N/A"
    print(f"  Final: loss={opt.loss_history[-1]:.4e}, E_rel={e_str}, time={elapsed:.1f}s")

    return {
        'method': 'lbfgs',
        'loss_history': opt.loss_history,
        'checkpoints': checkpoints,
        'final_loss': opt.loss_history[-1],
        'min_loss': min(opt.loss_history),
        'final_error': final_e,
        'total_time_s': elapsed,
        'nit': result.nit,
    }


def train_adam(model, problem, n_epochs=50000, lr=1e-3):
    """Adam baseline."""
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    sched = torch.optim.lr_scheduler.ReduceLROnPlateau(opt, patience=2000, factor=0.5)

    t0 = time.time()
    loss_all = []
    checkpoints = []
    log_every = max(1, n_epochs // 25)

    for ep in range(n_epochs):
        opt.zero_grad()
        loss = problem.compute_loss(model)
        loss.backward()
        opt.step()
        sched.step(loss.item())
        loss_all.append(loss.item())

        if ep % log_every == 0 or ep == n_epochs - 1:
            e = problem.compute_error(model)
            elapsed = time.time() - t0
            checkpoints.append({'iter': ep, 'loss': loss.item(), 'e_rel': e, 'time': elapsed})
            e_str = f", E_rel={e:.4e}" if e is not None else ""
            print(f"  Adam {ep:6d}: loss={loss.item():.4e}{e_str} | {elapsed:.1f}s")

    elapsed = time.time() - t0
    final_e = problem.compute_error(model)

    return {
        'method': 'adam',
        'loss_history': loss_all,
        'checkpoints': checkpoints,
        'final_loss': loss_all[-1],
        'min_loss': min(loss_all),
        'final_error': final_e,
        'total_time_s': elapsed,
    }


def train_spqn(model, problem, mode='multiplicative', n_epochs=100, k_s=50,
               n_subdomains=None):
    """SPQN training with scipy L-BFGS."""
    mname = "ASPQN" if mode == 'additive' else "MSPQN"

    layer_groups = model.get_layer_params()
    n_layers = len(layer_groups)

    if n_subdomains is None or n_subdomains >= n_layers:
        subdomains = layer_groups
    else:
        subdomains = []
        lp = n_layers // n_subdomains
        rem = n_layers % n_subdomains
        idx = 0
        for s in range(n_subdomains):
            nt = lp + (1 if s < rem else 0)
            grp = []
            for _ in range(nt):
                if idx < n_layers:
                    grp.extend(layer_groups[idx])
                    idx += 1
            subdomains.append(grp)

    n_sd = len(subdomains)
    loss_fn = lambda: problem.compute_loss(model)
    all_params = list(model.parameters())

    t0 = time.time()
    loss_all = []
    checkpoints = []
    log_every = max(1, n_epochs // 25)

    for ep in range(n_epochs):
        # Preconditioning step
        if mode == 'additive':
            saved = [p.data.clone() for p in all_params]
            all_updates = []
            for sd in subdomains:
                for p, s in zip(all_params, saved):
                    p.data.copy_(s)
                local = ScipyLBFGSSubset(model, sd, loss_fn, maxiter=k_s, m=3)
                local.optimize()
                all_updates.append([(p.data - s).clone() for p, s in zip(all_params, saved)])
            for p, s in zip(all_params, saved):
                p.data.copy_(s)
            for upd in all_updates:
                for p, du in zip(all_params, upd):
                    p.data.add_(du)
        else:
            for sd in subdomains:
                local = ScipyLBFGSSubset(model, sd, loss_fn, maxiter=k_s, m=3)
                local.optimize()

        # Global step
        gopt = ScipyLBFGS(model, loss_fn, maxiter=20, m=3)
        gopt.optimize()

        loss_val = gopt.loss_history[-1] if gopt.loss_history else problem.compute_loss(model).item()
        loss_all.append(loss_val)

        if ep % log_every == 0 or ep == n_epochs - 1:
            e = problem.compute_error(model)
            elapsed = time.time() - t0
            checkpoints.append({'iter': ep, 'loss': loss_val, 'e_rel': e, 'time': elapsed})
            e_str = f", E_rel={e:.4e}" if e is not None else ""
            print(f"  {mname} {ep:5d}: loss={loss_val:.4e}{e_str} | {elapsed:.1f}s")

    elapsed = time.time() - t0
    final_e = problem.compute_error(model)

    return {
        'method': mname.lower(),
        'loss_history': loss_all,
        'checkpoints': checkpoints,
        'final_loss': loss_all[-1] if loss_all else None,
        'min_loss': min(loss_all) if loss_all else None,
        'final_error': final_e,
        'total_time_s': elapsed,
        'n_subdomains': n_sd,
        'k_s': k_s,
    }


# ============================================================
# Main
# ============================================================

def main():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Device: {device}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")

    problems_order = ['klein_gordon', 'burgers', 'allen_cahn', 'advection_diffusion']
    methods = ['lbfgs', 'mspqn', 'aspqn', 'adam']

    all_results = {}

    for prob_name in problems_order:
        ProbClass = PROBLEMS_P[prob_name]
        problem = ProbClass(device=device)
        all_results[prob_name] = {}

        for method in methods:
            print(f"\n{'='*70}")
            print(f"  {problem.name} | {method.upper()}")
            print(f"  depth={problem.depth}, width={problem.width}")
            print(f"{'='*70}")

            torch.manual_seed(42)
            np.random.seed(42)
            if torch.cuda.is_available():
                torch.cuda.manual_seed_all(42)

            model = ResNetPINN(problem.input_dim, problem.output_dim,
                               problem.depth, problem.width).to(device)
            n_params = model.count_parameters()
            print(f"  Parameters: {n_params}")

            if method == 'lbfgs':
                result = train_scipy_lbfgs(model, problem, maxiter=10000, m=3)
            elif method == 'mspqn':
                result = train_spqn(model, problem, mode='multiplicative',
                                    n_epochs=100, k_s=50)
            elif method == 'aspqn':
                result = train_spqn(model, problem, mode='additive',
                                    n_epochs=100, k_s=50)
            elif method == 'adam':
                result = train_adam(model, problem, n_epochs=30000)

            result['problem'] = prob_name
            result['n_params'] = n_params
            all_results[prob_name][method] = result
            save_json(result, f"pen_{prob_name}_{method}.json")

    # Summary
    print("\n" + "=" * 100)
    print("SUMMARY (penalized loss)")
    print("=" * 100)
    print(f"{'Problem':<22} {'Method':<8} {'Min Loss':<13} {'E_rel':<13} {'Time(s)':<10}")
    print("-" * 100)
    for p in problems_order:
        for m in methods:
            r = all_results[p][m]
            ml = f"{r['min_loss']:.4e}" if r.get('min_loss') else "N/A"
            me = f"{r['final_error']:.4e}" if r.get('final_error') else "N/A"
            print(f"{p:<22} {m:<8} {ml:<13} {me:<13} {r.get('total_time_s', 0):.1f}")
        print("-" * 100)

    print("\nPaper Table 3 reference (penalty-free BC):")
    print("  klein_gordon: E_rel=6.1e-4 | burgers: E_rel=4.6e-4")
    print("  allen_cahn:   E_rel=6.0e-4 | advection: L-BFGS stagnates")
    print("\nKey comparison: SPQN should show better convergence than L-BFGS")


if __name__ == '__main__':
    main()
