#!/usr/bin/env python3
"""
Full experiment run for the PINN DD-Preconditioning replication.
Kopaničáková et al. (2023), arXiv:2306.17648

Key implementation details from paper:
- L-BFGS with m=3 history, cubic backtracking + strong Wolfe
- 10,000 Hammersley collocation points
- Xavier initialization
- Adaptive tanh activation  
- Penalty-free BC enforcement
- Layer-wise Schwarz decomposition

Usage on uicgpu:
  source ~/env.sh
  CUDA_VISIBLE_DEVICES=0 python3 -u run_full.py
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

RESULTS_DIR = '/data/stevens/projects-active/pinn-dd-precond/results'
os.makedirs(RESULTS_DIR, exist_ok=True)


def save_result(result, filename):
    r = {}
    for k, v in result.items():
        if isinstance(v, (list, tuple)):
            r[k] = [float(x) if x is not None and not isinstance(x, str) else x for x in v]
        elif isinstance(v, (np.floating, np.integer)):
            r[k] = float(v)
        elif isinstance(v, torch.Tensor):
            r[k] = v.item()
        else:
            r[k] = v
    with open(os.path.join(RESULTS_DIR, filename), 'w') as f:
        json.dump(r, f, indent=2)


def compute_pde_loss(model, X_base, problem):
    """Compute PDE residual loss, ensuring proper gradient flow."""
    X = X_base.detach().requires_grad_(True)
    residual = problem.pde_residual(model, X, bc_transform=problem.bc_transform)
    return torch.mean(residual ** 2)


def compute_error(model, problem, device, n_test=10000, ref_interp=None):
    """Compute E_rel = ||u_NN - u*||/||u_NN|| as in the paper."""
    with torch.no_grad():
        X_test = problem.generate_collocation_points(n_int=n_test, device=device)
        u_raw = model(X_test)
        u_pred = problem.bc_transform(u_raw, X_test)

        if problem.exact_solution_available():
            u_exact = problem.exact_solution(X_test)
            e_rel = (torch.norm(u_pred - u_exact) / (torch.norm(u_pred) + 1e-30)).item()
            return e_rel
        elif ref_interp is not None:
            X_np = X_test.cpu().numpy()
            u_ref = torch.tensor(ref_interp(X_np), dtype=torch.float32,
                                 device=device).reshape(-1, 1)
            e_rel = (torch.norm(u_pred - u_ref) / (torch.norm(u_pred) + 1e-30)).item()
            return e_rel
    return None


def train_adam(model, X_base, problem, device, n_epochs=50000, lr=1e-3,
              ref_interp=None, verbose=True):
    """Train with Adam optimizer."""
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(opt, patience=2000, factor=0.5)

    loss_h, err_h, time_h = [], [], []
    t0 = time.time()
    log_every = max(1, n_epochs // 30)

    for ep in range(n_epochs):
        opt.zero_grad()
        loss = compute_pde_loss(model, X_base, problem)
        loss.backward()
        opt.step()
        scheduler.step(loss.item())

        loss_h.append(loss.item())
        time_h.append(time.time() - t0)
        if ep % log_every == 0 or ep == n_epochs - 1:
            e_rel = compute_error(model, problem, device, ref_interp=ref_interp)
            err_h.append(e_rel)
            e_str = f", E_rel={e_rel:.4e}" if e_rel is not None else ""
            if verbose:
                print(f"  Adam {ep:6d}: loss={loss.item():.4e}{e_str} | {time_h[-1]:.1f}s")
        else:
            err_h.append(None)

    return loss_h, err_h, time_h


def train_lbfgs(model, X_base, problem, device, n_epochs=1000,
                history_size=3, max_iter=20, ref_interp=None, verbose=True):
    """Train with L-BFGS optimizer (m=3 as in paper)."""
    optimizer = torch.optim.LBFGS(
        model.parameters(),
        max_iter=max_iter,
        history_size=history_size,
        lr=1.0,
        line_search_fn='strong_wolfe',
        tolerance_grad=1e-16,
        tolerance_change=1e-16,
    )

    loss_h, err_h, time_h = [], [], []
    t0 = time.time()
    log_every = max(1, n_epochs // 30)
    stag_count = 0
    prev_loss = float('inf')

    for ep in range(n_epochs):
        loss_val = [0.0]

        def closure():
            optimizer.zero_grad()
            loss = compute_pde_loss(model, X_base, problem)
            loss.backward()
            loss_val[0] = loss.item()
            return loss

        optimizer.step(closure)
        loss_h.append(loss_val[0])
        time_h.append(time.time() - t0)

        # Stagnation detection
        if abs(prev_loss - loss_val[0]) / (abs(prev_loss) + 1e-30) < 1e-10:
            stag_count += 1
        else:
            stag_count = 0
        prev_loss = loss_val[0]

        if stag_count >= 30:
            # Reset optimizer with smaller lr
            new_lr = optimizer.defaults['lr'] * 0.5
            if new_lr > 1e-6:
                optimizer = torch.optim.LBFGS(
                    model.parameters(), max_iter=max_iter,
                    history_size=history_size, lr=new_lr,
                    line_search_fn='strong_wolfe',
                    tolerance_grad=1e-16, tolerance_change=1e-16,
                )
                stag_count = 0
                if verbose:
                    print(f"  L-BFGS reset at ep {ep}, new lr={new_lr:.1e}")

        if ep % log_every == 0 or ep == n_epochs - 1:
            e_rel = compute_error(model, problem, device, ref_interp=ref_interp)
            err_h.append(e_rel)
            e_str = f", E_rel={e_rel:.4e}" if e_rel is not None else ""
            if verbose:
                print(f"  L-BFGS {ep:5d}: loss={loss_val[0]:.4e}{e_str} | {time_h[-1]:.1f}s")
        else:
            err_h.append(None)

    return loss_h, err_h, time_h


def train_spqn(model, X_base, problem, device, mode='multiplicative',
               n_epochs=200, k_s=50, n_subdomains=None,
               ref_interp=None, verbose=True):
    """
    Train with SPQN (Schwarz Preconditioned Quasi-Newton).
    mode: 'additive' (ASPQN) or 'multiplicative' (MSPQN)
    """
    layer_groups = model.get_layer_params()
    n_layers = len(layer_groups)

    # Build subdomains
    if n_subdomains is None or n_subdomains >= n_layers:
        subdomains = layer_groups
    else:
        subdomains = []
        layers_per = n_layers // n_subdomains
        rem = n_layers % n_subdomains
        idx = 0
        for s in range(n_subdomains):
            n_this = layers_per + (1 if s < rem else 0)
            group = []
            for _ in range(n_this):
                if idx < n_layers:
                    group.extend(layer_groups[idx])
                    idx += 1
            subdomains.append(group)

    n_sd = len(subdomains)

    # Global L-BFGS
    global_opt = torch.optim.LBFGS(
        model.parameters(), max_iter=20, history_size=3, lr=1.0,
        line_search_fn='strong_wolfe',
        tolerance_grad=1e-16, tolerance_change=1e-16,
    )

    loss_h, err_h, time_h = [], [], []
    t0 = time.time()
    log_every = max(1, n_epochs // 30)
    mname = "ASPQN" if mode == 'additive' else "MSPQN"

    for ep in range(n_epochs):
        # ---- Preconditioning step ----
        all_params = list(model.parameters())

        if mode == 'additive':
            saved_params = [p.data.clone() for p in all_params]
            all_updates = []

            for sd_params in subdomains:
                # Reset
                for p, sp in zip(all_params, saved_params):
                    p.data.copy_(sp)

                # Solve local subproblem
                sd_ids = {id(p) for p in sd_params}
                for p in all_params:
                    p.requires_grad_(id(p) in sd_ids)

                active = [p for p in sd_params if p.requires_grad]
                if active:
                    local_opt = torch.optim.LBFGS(
                        active, max_iter=k_s, history_size=3, lr=1.0,
                        line_search_fn='strong_wolfe',
                        tolerance_grad=1e-16, tolerance_change=1e-16,
                    )

                    def local_closure():
                        local_opt.zero_grad()
                        loss = compute_pde_loss(model, X_base, problem)
                        loss.backward()
                        return loss

                    local_opt.step(local_closure)

                for p in all_params:
                    p.requires_grad_(True)

                update = [(p.data - sp).clone() for p, sp in zip(all_params, saved_params)]
                all_updates.append(update)

            # Combine updates additively
            for p, sp in zip(all_params, saved_params):
                p.data.copy_(sp)
            for update in all_updates:
                for p, du in zip(all_params, update):
                    p.data.add_(du)

        elif mode == 'multiplicative':
            for sd_params in subdomains:
                sd_ids = {id(p) for p in sd_params}
                for p in all_params:
                    p.requires_grad_(id(p) in sd_ids)

                active = [p for p in sd_params if p.requires_grad]
                if active:
                    local_opt = torch.optim.LBFGS(
                        active, max_iter=k_s, history_size=3, lr=1.0,
                        line_search_fn='strong_wolfe',
                        tolerance_grad=1e-16, tolerance_change=1e-16,
                    )

                    def local_closure():
                        local_opt.zero_grad()
                        loss = compute_pde_loss(model, X_base, problem)
                        loss.backward()
                        return loss

                    local_opt.step(local_closure)

                for p in all_params:
                    p.requires_grad_(True)

        # ---- Global L-BFGS step ----
        loss_val = [0.0]

        def closure():
            global_opt.zero_grad()
            loss = compute_pde_loss(model, X_base, problem)
            loss.backward()
            loss_val[0] = loss.item()
            return loss

        global_opt.step(closure)

        loss_h.append(loss_val[0])
        time_h.append(time.time() - t0)

        if ep % log_every == 0 or ep == n_epochs - 1:
            e_rel = compute_error(model, problem, device, ref_interp=ref_interp)
            err_h.append(e_rel)
            e_str = f", E_rel={e_rel:.4e}" if e_rel is not None else ""
            if verbose:
                print(f"  {mname} {ep:5d}: loss={loss_val[0]:.4e}{e_str} | {time_h[-1]:.1f}s")
        else:
            err_h.append(None)

    return loss_h, err_h, time_h


def run_experiment(problem_name, method, device, ref_interp=None, seed=42):
    """Run a single experiment and save results."""
    problem = PROBLEMS[problem_name]

    torch.manual_seed(seed)
    np.random.seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    model = ResNetPINN(problem.input_dim, problem.output_dim,
                       problem.depth, problem.width).to(device)
    n_params = model.count_parameters()
    X_int = problem.generate_collocation_points(n_int=10000, device=device)

    print(f"\n{'='*70}")
    print(f"  {problem.name} | {method.upper()} | params={n_params}")
    print(f"{'='*70}")

    t_start = time.time()

    if method == 'adam':
        loss_h, err_h, time_h = train_adam(
            model, X_int, problem, device, n_epochs=50000, lr=1e-3,
            ref_interp=ref_interp)
    elif method == 'lbfgs':
        loss_h, err_h, time_h = train_lbfgs(
            model, X_int, problem, device, n_epochs=2000,
            history_size=3, max_iter=20, ref_interp=ref_interp)
    elif method == 'mspqn':
        loss_h, err_h, time_h = train_spqn(
            model, X_int, problem, device, mode='multiplicative',
            n_epochs=200, k_s=50, ref_interp=ref_interp)
    elif method == 'aspqn':
        loss_h, err_h, time_h = train_spqn(
            model, X_int, problem, device, mode='additive',
            n_epochs=200, k_s=50, ref_interp=ref_interp)

    total_time = time.time() - t_start
    valid_err = [e for e in err_h if e is not None]

    result = {
        'problem': problem_name,
        'method': method,
        'n_params': n_params,
        'depth': problem.depth,
        'width': problem.width,
        'n_epochs': len(loss_h),
        'final_loss': loss_h[-1] if loss_h else None,
        'min_loss': min(loss_h) if loss_h else None,
        'final_error': valid_err[-1] if valid_err else None,
        'min_error': min(valid_err) if valid_err else None,
        'total_time_s': total_time,
        'loss_history': loss_h,
        'error_history': err_h,
        'time_history': time_h,
    }

    me = f"{result['min_error']:.4e}" if result['min_error'] else "N/A"
    print(f"\n  Result: min_loss={result['min_loss']:.4e}, min_E_rel={me}, "
          f"time={total_time:.1f}s")

    save_result(result, f"{problem_name}_{method}.json")
    return result


def run_sensitivity(problem_name, device, ref_interp=None, seed=42):
    """Sensitivity study: vary k_s and n_subdomains."""
    problem = PROBLEMS[problem_name]
    n_layers = problem.depth + 2

    sd_configs = sorted(set([2, max(2, n_layers // 2), n_layers]))
    k_s_values = [10, 50, 100]

    results = []
    print(f"\n{'#'*70}")
    print(f"# Sensitivity: {problem.name}")
    print(f"{'#'*70}")

    for method_mode in [('mspqn', 'multiplicative'), ('aspqn', 'additive')]:
        mname, mode = method_mode
        for n_sd in sd_configs:
            for ks in k_s_values:
                torch.manual_seed(seed)
                np.random.seed(seed)
                if torch.cuda.is_available():
                    torch.cuda.manual_seed_all(seed)

                model = ResNetPINN(problem.input_dim, problem.output_dim,
                                   problem.depth, problem.width).to(device)
                X_int = problem.generate_collocation_points(n_int=10000, device=device)

                loss_h, err_h, time_h = train_spqn(
                    model, X_int, problem, device, mode=mode,
                    n_epochs=50, k_s=ks, n_subdomains=n_sd,
                    ref_interp=ref_interp, verbose=False)

                valid_err = [e for e in err_h if e is not None]
                entry = {
                    'method': mname, 'n_sd': n_sd, 'k_s': ks,
                    'final_loss': float(loss_h[-1]) if loss_h else None,
                    'min_loss': float(min(loss_h)) if loss_h else None,
                    'min_error': float(min(valid_err)) if valid_err else None,
                    'total_time_s': float(time_h[-1]) if time_h else 0,
                }
                results.append(entry)
                me = f"{entry['min_error']:.4e}" if entry['min_error'] else "N/A"
                print(f"  {mname} N_sd={n_sd:2d} k_s={ks:3d}: "
                      f"min_loss={entry['min_loss']:.4e}, min_E_rel={me}, "
                      f"time={entry['total_time_s']:.1f}s")

    save_result({'problem': problem_name, 'sensitivity': results},
                f"{problem_name}_sensitivity.json")
    return results


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
        print(f"  Reference solutions failed: {e}")
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

    for prob in problems:
        all_results[prob] = {}
        ref = refs.get(prob)
        for method in methods:
            result = run_experiment(prob, method, device, ref_interp=ref)
            all_results[prob][method] = result

    # Sensitivity
    for prob in problems:
        run_sensitivity(prob, device, ref_interp=refs.get(prob))

    # Summary
    print("\n" + "=" * 110)
    print("SUMMARY")
    print("=" * 110)
    hdr = f"{'Problem':<25} {'Method':<8} {'Min Loss':<13} {'Min E_rel':<13} {'Time(s)':<10}"
    print(hdr)
    print("-" * 110)
    for prob in problems:
        for m in methods:
            r = all_results[prob][m]
            ml = f"{r['min_loss']:.4e}" if r['min_loss'] else "N/A"
            me = f"{r['min_error']:.4e}" if r['min_error'] else "N/A"
            print(f"{prob:<25} {m:<8} {ml:<13} {me:<13} {r['total_time_s']:.1f}")
        print("-" * 110)

    print("\nPaper Table 3 (L-BFGS E_rel):")
    print("  burgers=4.6e-4, klein_gordon=6.1e-4, allen_cahn=6.0e-4, advection=stagnates")


if __name__ == '__main__':
    main()
