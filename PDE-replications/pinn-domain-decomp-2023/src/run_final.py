#!/usr/bin/env python3
"""
Final experiment run using scipy L-BFGS-B for more robust L-BFGS optimization.
Kopaničáková et al. (2023), arXiv:2306.17648

Usage: CUDA_VISIBLE_DEVICES=0 python3 -u run_final.py
"""

import sys
import os
import json
import time
import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pinn_model import ResNetPINN
from problems import PROBLEMS
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


def make_loss_fn(model, X_base, problem):
    """Create a loss function closure."""
    def loss_fn():
        X = X_base.detach().requires_grad_(True)
        residual = problem.pde_residual(model, X, bc_transform=problem.bc_transform)
        return torch.mean(residual ** 2)
    return loss_fn


def compute_error(model, problem, device, ref_interp=None):
    """Compute E_rel = ||u_NN - u*||/||u_NN||."""
    with torch.no_grad():
        X = problem.generate_collocation_points(n_int=10000, device=device)
        u_raw = model(X)
        u_pred = problem.bc_transform(u_raw, X)

        if problem.exact_solution_available():
            u_exact = problem.exact_solution(X)
        elif ref_interp is not None:
            X_np = X.cpu().numpy()
            u_exact = torch.tensor(ref_interp(X_np), dtype=torch.float32,
                                   device=device).reshape(-1, 1)
        else:
            return None

        return (torch.norm(u_pred - u_exact) / (torch.norm(u_pred) + 1e-30)).item()


# ============================================================
# Training methods
# ============================================================

def train_lbfgs(model, X_base, problem, device, ref_interp=None,
                maxiter=20000, m=3):
    """Train with scipy L-BFGS-B (m=3 per paper)."""
    loss_fn = make_loss_fn(model, X_base, problem)
    optimizer = ScipyLBFGS(model, loss_fn, maxiter=maxiter, m=m)

    # Track progress
    checkpoints = {'loss': [], 'error': [], 'time': [], 'iter': []}
    t0 = time.time()
    check_interval = max(100, maxiter // 30)

    def callback(x):
        n = optimizer._iter_count
        if n % check_interval == 0 or n == 1:
            e_rel = compute_error(model, problem, device, ref_interp)
            loss_val = optimizer.loss_history[-1] if optimizer.loss_history else None
            elapsed = time.time() - t0
            checkpoints['loss'].append(loss_val)
            checkpoints['error'].append(e_rel)
            checkpoints['time'].append(elapsed)
            checkpoints['iter'].append(n)
            e_str = f", E_rel={e_rel:.4e}" if e_rel is not None else ""
            print(f"  L-BFGS iter {n:6d}: loss={loss_val:.4e}{e_str} | {elapsed:.1f}s")

    print(f"  Starting scipy L-BFGS-B (m={m}, maxiter={maxiter})...")
    result = optimizer.optimize(callback=callback)
    elapsed = time.time() - t0

    final_error = compute_error(model, problem, device, ref_interp)
    final_loss = optimizer.loss_history[-1] if optimizer.loss_history else None

    print(f"  Done: {result.message.decode() if isinstance(result.message, bytes) else result.message}")
    print(f"  iters={result.nit}, f_evals={result.nfev}")
    e_str = f"{final_error:.4e}" if final_error is not None else "N/A"
    print(f"  Final: loss={final_loss:.4e}, E_rel={e_str}, time={elapsed:.1f}s")

    return {
        'loss_history': optimizer.loss_history,
        'checkpoints': checkpoints,
        'final_loss': final_loss,
        'final_error': final_error,
        'min_loss': min(optimizer.loss_history) if optimizer.loss_history else None,
        'total_time_s': elapsed,
        'nit': result.nit,
        'nfev': result.nfev,
        'scipy_message': str(result.message),
    }


def train_adam(model, X_base, problem, device, ref_interp=None, n_epochs=50000):
    """Train with Adam optimizer."""
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    sched = torch.optim.lr_scheduler.ReduceLROnPlateau(opt, patience=2000, factor=0.5)

    checkpoints = {'loss': [], 'error': [], 'time': [], 'iter': []}
    loss_all = []
    t0 = time.time()
    log_every = max(1, n_epochs // 30)

    for ep in range(n_epochs):
        opt.zero_grad()
        loss = make_loss_fn(model, X_base, problem)()
        loss.backward()
        opt.step()
        sched.step(loss.item())

        loss_all.append(loss.item())

        if ep % log_every == 0 or ep == n_epochs - 1:
            e_rel = compute_error(model, problem, device, ref_interp)
            elapsed = time.time() - t0
            checkpoints['loss'].append(loss.item())
            checkpoints['error'].append(e_rel)
            checkpoints['time'].append(elapsed)
            checkpoints['iter'].append(ep)
            e_str = f", E_rel={e_rel:.4e}" if e_rel is not None else ""
            print(f"  Adam {ep:6d}: loss={loss.item():.4e}{e_str} | {elapsed:.1f}s")

    elapsed = time.time() - t0
    final_error = compute_error(model, problem, device, ref_interp)

    return {
        'loss_history': loss_all,
        'checkpoints': checkpoints,
        'final_loss': loss_all[-1] if loss_all else None,
        'final_error': final_error,
        'min_loss': min(loss_all) if loss_all else None,
        'total_time_s': elapsed,
    }


def train_spqn(model, X_base, problem, device, mode='multiplicative',
               n_epochs=200, k_s=50, n_subdomains=None, ref_interp=None):
    """Train with SPQN using scipy L-BFGS for both local and global steps."""
    mname = "ASPQN" if mode == 'additive' else "MSPQN"

    # Build layer groups
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
    loss_fn = make_loss_fn(model, X_base, problem)
    all_params = list(model.parameters())

    checkpoints = {'loss': [], 'error': [], 'time': [], 'iter': []}
    loss_all = []
    t0 = time.time()
    log_every = max(1, n_epochs // 30)

    for ep in range(n_epochs):
        # ---- Preconditioning step ----
        if mode == 'additive':
            saved = [p.data.clone() for p in all_params]
            all_updates = []

            for sd_params in subdomains:
                # Reset
                for p, s in zip(all_params, saved):
                    p.data.copy_(s)

                # Local solve
                local_opt = ScipyLBFGSSubset(model, sd_params, loss_fn, maxiter=k_s, m=3)
                local_opt.optimize()

                update = [(p.data - s).clone() for p, s in zip(all_params, saved)]
                all_updates.append(update)

            # Combine
            for p, s in zip(all_params, saved):
                p.data.copy_(s)
            for update in all_updates:
                for p, du in zip(all_params, update):
                    p.data.add_(du)

        elif mode == 'multiplicative':
            for sd_params in subdomains:
                local_opt = ScipyLBFGSSubset(model, sd_params, loss_fn, maxiter=k_s, m=3)
                local_opt.optimize()

        # ---- Global L-BFGS step ----
        global_opt = ScipyLBFGS(model, loss_fn, maxiter=20, m=3)
        global_opt.optimize()

        loss_val = global_opt.loss_history[-1] if global_opt.loss_history else None
        loss_all.append(loss_val)

        if ep % log_every == 0 or ep == n_epochs - 1:
            e_rel = compute_error(model, problem, device, ref_interp)
            elapsed = time.time() - t0
            checkpoints['loss'].append(loss_val)
            checkpoints['error'].append(e_rel)
            checkpoints['time'].append(elapsed)
            checkpoints['iter'].append(ep)
            e_str = f", E_rel={e_rel:.4e}" if e_rel is not None else ""
            print(f"  {mname} {ep:5d}: loss={loss_val:.4e}{e_str} | {elapsed:.1f}s")

    elapsed = time.time() - t0
    final_error = compute_error(model, problem, device, ref_interp)

    return {
        'loss_history': loss_all,
        'checkpoints': checkpoints,
        'final_loss': loss_all[-1] if loss_all else None,
        'final_error': final_error,
        'min_loss': min([l for l in loss_all if l is not None]) if loss_all else None,
        'total_time_s': elapsed,
        'n_subdomains': n_sd,
        'k_s': k_s,
    }


# ============================================================
# Main
# ============================================================

def compute_references():
    """Compute FEM reference solutions."""
    refs = {}
    try:
        from reference_solutions import (
            burgers_reference, allen_cahn_reference, advection_diffusion_reference
        )
        print("Computing reference solutions...")
        refs['burgers'], _, _, _ = burgers_reference()
        refs['allen_cahn'], _, _, _ = allen_cahn_reference()
        refs['advection_diffusion'], _, _, _ = advection_diffusion_reference()
        print("  Done.")
    except Exception as e:
        print(f"  Reference solution error: {e}")
    refs['klein_gordon'] = None
    return refs


def main():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Device: {device}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")

    refs = compute_references()

    problems = ['klein_gordon', 'burgers', 'allen_cahn', 'advection_diffusion']
    methods = ['lbfgs', 'mspqn', 'aspqn', 'adam']

    all_results = {}

    for prob_name in problems:
        all_results[prob_name] = {}
        problem = PROBLEMS[prob_name]
        ref = refs.get(prob_name)

        for method in methods:
            print(f"\n{'='*70}")
            print(f"  {problem.name} | {method.upper()} | depth={problem.depth}, width={problem.width}")
            print(f"{'='*70}")

            torch.manual_seed(42)
            np.random.seed(42)
            if torch.cuda.is_available():
                torch.cuda.manual_seed_all(42)

            model = ResNetPINN(problem.input_dim, problem.output_dim,
                               problem.depth, problem.width).to(device)
            X = problem.generate_collocation_points(n_int=10000, device=device)
            n_params = model.count_parameters()
            print(f"  Parameters: {n_params}")

            if method == 'lbfgs':
                result = train_lbfgs(model, X, problem, device, ref_interp=ref,
                                     maxiter=20000, m=3)
            elif method == 'mspqn':
                result = train_spqn(model, X, problem, device, mode='multiplicative',
                                    n_epochs=100, k_s=50, ref_interp=ref)
            elif method == 'aspqn':
                result = train_spqn(model, X, problem, device, mode='additive',
                                    n_epochs=100, k_s=50, ref_interp=ref)
            elif method == 'adam':
                result = train_adam(model, X, problem, device, ref_interp=ref,
                                   n_epochs=30000)

            result['problem'] = prob_name
            result['method'] = method
            result['n_params'] = n_params
            all_results[prob_name][method] = result
            save_json(result, f"final_{prob_name}_{method}.json")

    # Sensitivity
    for prob_name in problems:
        problem = PROBLEMS[prob_name]
        n_layers = problem.depth + 2
        sd_configs = sorted(set([2, max(2, n_layers//2), n_layers]))

        print(f"\n{'#'*70}")
        print(f"# Sensitivity: {problem.name}")
        print(f"{'#'*70}")

        sens = []
        for method, mode in [('mspqn', 'multiplicative'), ('aspqn', 'additive')]:
            for n_sd in sd_configs:
                for ks in [10, 50, 100]:
                    torch.manual_seed(42)
                    np.random.seed(42)
                    if torch.cuda.is_available():
                        torch.cuda.manual_seed_all(42)

                    model = ResNetPINN(problem.input_dim, problem.output_dim,
                                       problem.depth, problem.width).to(device)
                    X = problem.generate_collocation_points(n_int=10000, device=device)

                    result = train_spqn(model, X, problem, device, mode=mode,
                                        n_epochs=30, k_s=ks, n_subdomains=n_sd,
                                        ref_interp=refs.get(prob_name), verbose=False)

                    entry = {
                        'method': method, 'n_sd': n_sd, 'k_s': ks,
                        'min_loss': result['min_loss'],
                        'final_error': result['final_error'],
                        'time_s': result['total_time_s'],
                    }
                    sens.append(entry)
                    me = f"{entry['final_error']:.4e}" if entry['final_error'] else "N/A"
                    print(f"  {method} N_sd={n_sd:2d} k_s={ks:3d}: "
                          f"loss={entry['min_loss']:.4e}, E_rel={me}, "
                          f"time={entry['time_s']:.1f}s")

        save_json({'sensitivity': sens}, f"final_{prob_name}_sensitivity.json")

    # Summary table
    print("\n" + "=" * 100)
    print("SUMMARY")
    print("=" * 100)
    print(f"{'Problem':<22} {'Method':<8} {'Min Loss':<13} {'E_rel':<13} {'Time(s)':<10}")
    print("-" * 100)
    for prob in problems:
        for m in methods:
            r = all_results[prob][m]
            ml = f"{r['min_loss']:.4e}" if r['min_loss'] else "N/A"
            me = f"{r['final_error']:.4e}" if r.get('final_error') else "N/A"
            print(f"{prob:<22} {m:<8} {ml:<13} {me:<13} {r['total_time_s']:.1f}")
        print("-" * 100)

    print("\nPaper Table 3 reference:")
    print("  klein_gordon: E_rel=6.1e-4 (L-BFGS 236.5min, ASPQN 6.8min, MSPQN 26.9min)")
    print("  burgers:      E_rel=4.6e-4 (L-BFGS 558.5min, ASPQN 14.4min, MSPQN 40.7min)")
    print("  allen_cahn:   E_rel=6.0e-4 (L-BFGS 1001.6min, ASPQN 79.2min, MSPQN 117.5min)")
    print("  advection:    L-BFGS stagnates")


if __name__ == '__main__':
    main()
