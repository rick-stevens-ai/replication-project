#!/usr/bin/env python3
"""
Run a single problem + method. Fast targeted experiments.

Usage: CUDA_VISIBLE_DEVICES=X python3 -u run_single.py <problem> <method> [maxiter]
  problem: klein_gordon, burgers, allen_cahn, advection_diffusion
  method:  lbfgs, mspqn, aspqn, adam
  maxiter: optional, default varies by method
"""

import sys
import os
import json
import time
import numpy as np
import torch

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

class ProblemBase:
    name = "?"
    depth = 6
    width = 50
    input_dim = 2
    output_dim = 1

    def __init__(self, device='cuda'):
        self.device = device
        self._generate_data()

    def _generate_data(self):
        raise NotImplementedError

    def compute_loss(self, model):
        raise NotImplementedError

    def compute_error(self, model, n_test=10000):
        return None


class KleinGordonP(ProblemBase):
    name = "Klein-Gordon"
    depth, width = 6, 50

    def _generate_data(self):
        n_int = 10000
        pts = hammersley_sequence(n_int, 2)
        self.X_int = torch.tensor(
            np.column_stack([pts[:, 0] * 12, pts[:, 1] * 2 - 1]),
            dtype=torch.float32, device=self.device)
        n_bc = 500
        x_ic = torch.linspace(-1, 1, n_bc, device=self.device)
        self.X_ic = torch.stack([torch.zeros(n_bc, device=self.device), x_ic], dim=1)
        self.u_ic = x_ic.unsqueeze(1)
        self.X_ic_v = self.X_ic.clone()
        t_bc = torch.linspace(0.01, 12, n_bc, device=self.device)
        self.X_left = torch.stack([t_bc, -torch.ones(n_bc, device=self.device)], dim=1)
        self.u_left = -torch.cos(t_bc).unsqueeze(1)
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


class BurgersP(ProblemBase):
    name = "Burgers"
    depth, width = 8, 20
    nu = 0.01 / np.pi

    def _generate_data(self):
        n_int = 10000
        pts = hammersley_sequence(n_int, 2)
        self.X_int = torch.tensor(
            np.column_stack([pts[:, 0], pts[:, 1] * 2 - 1]),
            dtype=torch.float32, device=self.device)
        n_bc = 500
        x_ic = torch.linspace(-1, 1, n_bc, device=self.device)
        self.X_ic = torch.stack([torch.zeros(n_bc, device=self.device), x_ic], dim=1)
        self.u_ic = -torch.sin(np.pi * x_ic).unsqueeze(1)
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


class AllenCahnP(ProblemBase):
    name = "Allen-Cahn"
    depth, width = 6, 64
    D = 0.001

    def _generate_data(self):
        n_int = 10000
        pts = hammersley_sequence(n_int, 2)
        self.X_int = torch.tensor(
            np.column_stack([pts[:, 0], pts[:, 1] * 2 - 1]),
            dtype=torch.float32, device=self.device)
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


class AdvDiffP(ProblemBase):
    name = "Advection-Diffusion"
    depth, width = 10, 50

    def _generate_data(self):
        n_int = 10000
        pts = hammersley_sequence(n_int, 2)
        self.X_int = torch.tensor(pts, dtype=torch.float32, device=self.device)
        n_bc = 500
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
        mu = 0.01
        res = -mu * (u_x1x1 + u_x2x2) + u_x1 + u_x2 - 1.0
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


PROBLEMS = {
    'klein_gordon': KleinGordonP,
    'burgers': BurgersP,
    'allen_cahn': AllenCahnP,
    'advection_diffusion': AdvDiffP,
}


# ============================================================
# Training
# ============================================================

def train_lbfgs(model, problem, maxiter=10000, m=3):
    loss_fn = lambda: problem.compute_loss(model)
    opt = ScipyLBFGS(model, loss_fn, maxiter=maxiter, m=m)
    t0 = time.time()
    ck = []

    def cb(x):
        n = opt._iter_count
        if n % max(1, maxiter // 20) == 0:
            e = problem.compute_error(model)
            el = time.time() - t0
            loss = opt.loss_history[-1]
            ck.append({'iter': n, 'loss': loss, 'e_rel': e, 'time': el})
            es = f", E_rel={e:.4e}" if e is not None else ""
            print(f"  L-BFGS {n:6d}: loss={loss:.4e}{es} | {el:.1f}s")

    result = opt.optimize(callback=cb)
    el = time.time() - t0
    fe = problem.compute_error(model)
    msg = result.message.decode() if isinstance(result.message, bytes) else str(result.message)
    es = f"{fe:.4e}" if fe is not None else "N/A"
    print(f"  Done: {msg}, nit={result.nit}")
    print(f"  Final: loss={opt.loss_history[-1]:.4e}, E_rel={es}, time={el:.1f}s")

    return {
        'method': 'lbfgs', 'checkpoints': ck,
        'final_loss': opt.loss_history[-1],
        'min_loss': min(opt.loss_history),
        'final_error': fe, 'total_time_s': el, 'nit': result.nit,
    }


def train_adam(model, problem, n_epochs=30000, lr=1e-3):
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    sched = torch.optim.lr_scheduler.ReduceLROnPlateau(opt, patience=2000, factor=0.5)
    t0 = time.time()
    loss_all = []
    ck = []
    le = max(1, n_epochs // 25)

    for ep in range(n_epochs):
        opt.zero_grad()
        loss = problem.compute_loss(model)
        loss.backward()
        opt.step()
        sched.step(loss.item())
        loss_all.append(loss.item())
        if ep % le == 0 or ep == n_epochs - 1:
            e = problem.compute_error(model)
            el = time.time() - t0
            ck.append({'iter': ep, 'loss': loss.item(), 'e_rel': e, 'time': el})
            es = f", E_rel={e:.4e}" if e is not None else ""
            print(f"  Adam {ep:6d}: loss={loss.item():.4e}{es} | {el:.1f}s")

    el = time.time() - t0
    fe = problem.compute_error(model)
    return {
        'method': 'adam', 'checkpoints': ck,
        'final_loss': loss_all[-1], 'min_loss': min(loss_all),
        'final_error': fe, 'total_time_s': el,
    }


def train_spqn(model, problem, mode='multiplicative', n_epochs=100, k_s=50):
    mname = "ASPQN" if mode == 'additive' else "MSPQN"
    layer_groups = model.get_layer_params()
    subdomains = layer_groups  # maximal decomposition
    n_sd = len(subdomains)
    loss_fn = lambda: problem.compute_loss(model)
    all_params = list(model.parameters())
    t0 = time.time()
    loss_all = []
    ck = []
    le = max(1, n_epochs // 25)

    for ep in range(n_epochs):
        if mode == 'additive':
            saved = [p.data.clone() for p in all_params]
            updates = []
            for sd in subdomains:
                for p, s in zip(all_params, saved):
                    p.data.copy_(s)
                local = ScipyLBFGSSubset(model, sd, loss_fn, maxiter=k_s, m=3)
                local.optimize()
                updates.append([(p.data - s).clone() for p, s in zip(all_params, saved)])
            for p, s in zip(all_params, saved):
                p.data.copy_(s)
            for upd in updates:
                for p, du in zip(all_params, upd):
                    p.data.add_(du)
        else:
            for sd in subdomains:
                local = ScipyLBFGSSubset(model, sd, loss_fn, maxiter=k_s, m=3)
                local.optimize()

        gopt = ScipyLBFGS(model, loss_fn, maxiter=20, m=3)
        gopt.optimize()
        lv = gopt.loss_history[-1] if gopt.loss_history else problem.compute_loss(model).item()
        loss_all.append(lv)

        if ep % le == 0 or ep == n_epochs - 1:
            e = problem.compute_error(model)
            el = time.time() - t0
            ck.append({'iter': ep, 'loss': lv, 'e_rel': e, 'time': el})
            es = f", E_rel={e:.4e}" if e is not None else ""
            print(f"  {mname} {ep:5d}: loss={lv:.4e}{es} | {el:.1f}s")

    el = time.time() - t0
    fe = problem.compute_error(model)
    return {
        'method': mname.lower(), 'checkpoints': ck,
        'final_loss': loss_all[-1] if loss_all else None,
        'min_loss': min(loss_all) if loss_all else None,
        'final_error': fe, 'total_time_s': el,
        'n_subdomains': n_sd, 'k_s': k_s,
    }


def sensitivity(model_cls, problem, depth, width, device):
    """Quick sensitivity: vary k_s and n_subdomains for MSPQN."""
    n_layers = depth + 2
    configs = []
    for n_sd in sorted(set([2, max(2, n_layers // 2), n_layers])):
        for ks in [10, 50, 100]:
            torch.manual_seed(42); np.random.seed(42)
            if torch.cuda.is_available(): torch.cuda.manual_seed_all(42)
            model = ResNetPINN(2, 1, depth, width).to(device)
            layer_groups = model.get_layer_params()

            if n_sd >= len(layer_groups):
                subs = layer_groups
            else:
                subs = []
                lp_count = len(layer_groups) // n_sd
                rem = len(layer_groups) % n_sd
                idx = 0
                for s in range(n_sd):
                    nt = lp_count + (1 if s < rem else 0)
                    grp = []
                    for _ in range(nt):
                        if idx < len(layer_groups):
                            grp.extend(layer_groups[idx])
                            idx += 1
                    subs.append(grp)

            loss_fn = lambda: problem.compute_loss(model)
            all_params = list(model.parameters())
            t0 = time.time()

            for ep in range(20):  # short run
                for sd in subs:
                    local = ScipyLBFGSSubset(model, sd, loss_fn, maxiter=ks, m=3)
                    local.optimize()
                gopt = ScipyLBFGS(model, loss_fn, maxiter=20, m=3)
                gopt.optimize()

            el = time.time() - t0
            lv = problem.compute_loss(model).item()
            e = problem.compute_error(model)
            es = f"{e:.4e}" if e is not None else "N/A"
            print(f"    MSPQN n_sd={n_sd:2d} k_s={ks:3d}: loss={lv:.4e}, E_rel={es}, time={el:.1f}s")
            configs.append({'n_sd': n_sd, 'k_s': ks, 'loss': lv, 'e_rel': e, 'time': el})

    return configs


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 run_single.py <problem> <method> [maxiter]")
        print("  problem: klein_gordon, burgers, allen_cahn, advection_diffusion")
        print("  method:  lbfgs, mspqn, aspqn, adam, sensitivity, all")
        sys.exit(1)

    prob_name = sys.argv[1]
    method = sys.argv[2]
    maxiter = int(sys.argv[3]) if len(sys.argv) > 3 else None

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Device: {device}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")

    ProbClass = PROBLEMS[prob_name]
    problem = ProbClass(device=device)

    if method == 'sensitivity':
        print(f"\n{'='*60}")
        print(f"  Sensitivity: {problem.name}")
        print(f"{'='*60}")
        configs = sensitivity(ResNetPINN, problem, problem.depth, problem.width, device)
        save_json({'sensitivity': configs, 'problem': prob_name},
                  f"pen_{prob_name}_sensitivity.json")
        return

    methods_to_run = ['lbfgs', 'mspqn', 'aspqn', 'adam'] if method == 'all' else [method]

    for m in methods_to_run:
        print(f"\n{'='*60}")
        print(f"  {problem.name} | {m.upper()} | d={problem.depth}, w={problem.width}")
        print(f"{'='*60}")

        torch.manual_seed(42); np.random.seed(42)
        if torch.cuda.is_available(): torch.cuda.manual_seed_all(42)

        model = ResNetPINN(problem.input_dim, problem.output_dim,
                           problem.depth, problem.width).to(device)
        n_params = model.count_parameters()
        print(f"  Parameters: {n_params}")

        if m == 'lbfgs':
            result = train_lbfgs(model, problem, maxiter=maxiter or 10000, m=3)
        elif m == 'mspqn':
            result = train_spqn(model, problem, mode='multiplicative',
                                n_epochs=maxiter or 100, k_s=50)
        elif m == 'aspqn':
            result = train_spqn(model, problem, mode='additive',
                                n_epochs=maxiter or 100, k_s=50)
        elif m == 'adam':
            result = train_adam(model, problem, n_epochs=maxiter or 30000)

        result['problem'] = prob_name
        result['n_params'] = n_params
        save_json(result, f"pen_{prob_name}_{m}.json")


if __name__ == '__main__':
    main()
