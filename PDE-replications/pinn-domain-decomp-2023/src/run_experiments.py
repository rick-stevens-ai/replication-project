#!/usr/bin/env python3
"""
Main experiment runner for PINN domain-decomposition preconditioning replication.
Kopaničáková et al. (2023), arXiv:2306.17648

Runs all four test cases with L-BFGS, Adam, ASPQN, and MSPQN.
Saves results to ../results/
"""

import sys
import os
import json
import time
import argparse
import numpy as np
import torch

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pinn_model import ResNetPINN
from problems import PROBLEMS
from optimizers import LBFGSTrainer, SPQNTrainer, AdamTrainer, compute_loss, compute_relative_error


def set_seed(seed=42):
    torch.manual_seed(seed)
    np.random.seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def run_single_experiment(problem_name, method, device='cpu', seed=42,
                          n_epochs=None, k_s=50, n_subdomains=None,
                          verbose=True):
    """
    Run a single experiment: one problem, one method.
    
    Returns dict with loss_history, error_history, time_history, final_loss, final_error.
    """
    set_seed(seed)

    problem = PROBLEMS[problem_name]

    if verbose:
        print(f"\n{'='*60}")
        print(f"Problem: {problem.name} | Method: {method} | Device: {device}")
        print(f"Network: depth={problem.depth}, width={problem.width}")
        print(f"{'='*60}")

    # Create model
    model = ResNetPINN(
        input_dim=problem.input_dim,
        output_dim=problem.output_dim,
        depth=problem.depth,
        width=problem.width,
    ).to(device)

    n_params = model.count_parameters()
    if verbose:
        print(f"  Parameters: {n_params}")

    # Generate collocation points
    X_int = problem.generate_collocation_points(n_int=10000, device=device)

    # Set up BC transform
    bc_transform = problem.bc_transform

    # Default epochs per method
    if n_epochs is None:
        if method == 'adam':
            n_epochs = 50000
        elif method == 'lbfgs':
            n_epochs = 1000
        elif method in ('aspqn', 'mspqn'):
            n_epochs = 200

    # Train
    start = time.time()

    if method == 'adam':
        trainer = AdamTrainer(model, problem, bc_transform, X_int,
                              device=device, lr=1e-3)
        log_every = max(1, n_epochs // 50)
        loss_hist, err_hist, time_hist = trainer.train(
            n_epochs=n_epochs, log_every=log_every, verbose=verbose)

    elif method == 'lbfgs':
        trainer = LBFGSTrainer(model, problem, bc_transform, X_int,
                               device=device, max_iter=20, history_size=50)
        log_every = max(1, n_epochs // 50)
        loss_hist, err_hist, time_hist = trainer.train(
            n_epochs=n_epochs, log_every=log_every, verbose=verbose)

    elif method == 'aspqn':
        trainer = SPQNTrainer(model, problem, bc_transform, X_int,
                              device=device, mode='additive',
                              n_subdomains=n_subdomains, k_s=k_s)
        log_every = max(1, n_epochs // 50)
        loss_hist, err_hist, time_hist = trainer.train(
            n_epochs=n_epochs, log_every=log_every, verbose=verbose)

    elif method == 'mspqn':
        trainer = SPQNTrainer(model, problem, bc_transform, X_int,
                              device=device, mode='multiplicative',
                              n_subdomains=n_subdomains, k_s=k_s)
        log_every = max(1, n_epochs // 50)
        loss_hist, err_hist, time_hist = trainer.train(
            n_epochs=n_epochs, log_every=log_every, verbose=verbose)
    else:
        raise ValueError(f"Unknown method: {method}")

    total_time = time.time() - start

    # Final loss
    final_loss = loss_hist[-1] if loss_hist else float('inf')
    final_error = err_hist[-1] if err_hist else None

    result = {
        'problem': problem_name,
        'method': method,
        'n_params': n_params,
        'n_epochs': len(loss_hist),
        'final_loss': final_loss,
        'final_error': final_error,
        'total_time_s': total_time,
        'loss_history': loss_hist,
        'error_history': err_hist,
        'time_history': time_hist,
        'k_s': k_s if method in ('aspqn', 'mspqn') else None,
        'n_subdomains': n_subdomains,
        'seed': seed,
    }

    if verbose:
        err_str = f"{final_error:.4e}" if final_error is not None else "N/A"
        print(f"\n  Final: loss={final_loss:.4e}, E_rel={err_str}, time={total_time:.1f}s")

    return result


def run_sensitivity_study(problem_name, device='cpu', verbose=True):
    """
    Sensitivity study: vary k_s and n_subdomains for ASPQN and MSPQN.
    Reproduces Figure 3-6 style data from the paper.
    """
    problem = PROBLEMS[problem_name]
    n_layers = problem.depth + 2  # input + hidden + output

    # Determine subdomain configurations
    # Paper uses: {2, ~half, max}
    sd_configs = [2]
    if n_layers // 2 > 2:
        sd_configs.append(n_layers // 2)
    sd_configs.append(n_layers)

    k_s_values = [10, 50, 100]

    results = []
    for method in ['aspqn', 'mspqn']:
        for n_sd in sd_configs:
            for ks in k_s_values:
                if verbose:
                    print(f"\n--- {method.upper()} | N_sd={n_sd} | k_s={ks} ---")
                result = run_single_experiment(
                    problem_name, method, device=device,
                    n_epochs=100, k_s=ks, n_subdomains=n_sd,
                    verbose=verbose)
                result['n_sd_actual'] = n_sd
                results.append(result)

    return results


def run_all_experiments(device='cpu', results_dir='../results', verbose=True):
    """Run the complete experiment suite."""
    os.makedirs(results_dir, exist_ok=True)

    all_results = {}
    problems = ['burgers', 'klein_gordon', 'allen_cahn', 'advection_diffusion']
    methods = ['adam', 'lbfgs', 'mspqn', 'aspqn']

    # Main comparison experiments
    for prob in problems:
        all_results[prob] = {}
        for method in methods:
            print(f"\n{'#'*70}")
            print(f"# Running: {prob} / {method}")
            print(f"{'#'*70}")

            result = run_single_experiment(prob, method, device=device, verbose=verbose)
            all_results[prob][method] = result

            # Save individual result
            fname = f"{prob}_{method}.json"
            result_serializable = {k: v for k, v in result.items()}
            # Convert numpy/tensor to list for JSON
            for k in ['loss_history', 'error_history', 'time_history']:
                if result_serializable[k] is not None:
                    result_serializable[k] = [
                        float(v) if v is not None else None
                        for v in result_serializable[k]
                    ]
            if result_serializable['final_error'] is not None:
                result_serializable['final_error'] = float(result_serializable['final_error'])

            with open(os.path.join(results_dir, fname), 'w') as f:
                json.dump(result_serializable, f, indent=2)

    # Sensitivity studies for each problem
    for prob in problems:
        print(f"\n{'#'*70}")
        print(f"# Sensitivity study: {prob}")
        print(f"{'#'*70}")

        sens_results = run_sensitivity_study(prob, device=device, verbose=verbose)

        # Save
        sens_serializable = []
        for r in sens_results:
            rs = {k: v for k, v in r.items()}
            for k in ['loss_history', 'error_history', 'time_history']:
                if rs[k] is not None:
                    rs[k] = [float(v) if v is not None else None for v in rs[k]]
            if rs['final_error'] is not None:
                rs['final_error'] = float(rs['final_error'])
            sens_serializable.append(rs)

        with open(os.path.join(results_dir, f"{prob}_sensitivity.json"), 'w') as f:
            json.dump(sens_serializable, f, indent=2)

    # Print summary table
    print_summary_table(all_results)

    return all_results


def print_summary_table(all_results):
    """Print a summary comparison table."""
    print("\n" + "=" * 90)
    print("SUMMARY TABLE: Final Loss and Relative Error")
    print("=" * 90)
    print(f"{'Problem':<25} {'Method':<10} {'Final Loss':<14} {'E_rel':<14} {'Time (s)':<12}")
    print("-" * 90)

    for prob in all_results:
        for method in all_results[prob]:
            r = all_results[prob][method]
            err_str = f"{r['final_error']:.4e}" if r['final_error'] is not None else "N/A"
            print(f"{prob:<25} {method:<10} {r['final_loss']:<14.4e} {err_str:<14} {r['total_time_s']:<12.1f}")
        print("-" * 90)

    # Paper reference values
    print("\nPaper Reference (Table 3):")
    print("-" * 90)
    refs = {
        'burgers': {'E_rel': '4.6e-4', 'lbfgs_time': '558.5 min', 'aspqn_time': '14.4 min', 'mspqn_time': '40.7 min'},
        'klein_gordon': {'E_rel': '6.1e-4', 'lbfgs_time': '236.5 min', 'aspqn_time': '6.8 min', 'mspqn_time': '26.9 min'},
        'allen_cahn': {'E_rel': '6.0e-4', 'lbfgs_time': '1001.6 min', 'aspqn_time': '79.2 min', 'mspqn_time': '117.5 min'},
        'advection_diffusion': {'E_rel': 'N/A (L-BFGS stagnates)', 'lbfgs_time': 'N/A', 'aspqn_time': 'N/A', 'mspqn_time': 'N/A'},
    }
    for prob, ref in refs.items():
        print(f"  {prob}: E_rel(L-BFGS)={ref['E_rel']}, "
              f"t_LBFGS={ref['lbfgs_time']}, "
              f"t_ASPQN={ref['aspqn_time']}, "
              f"t_MSPQN={ref['mspqn_time']}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PINN DD-Preconditioning Experiments')
    parser.add_argument('--problem', type=str, default='all',
                        choices=['all', 'burgers', 'allen_cahn', 'advection_diffusion', 'klein_gordon'])
    parser.add_argument('--method', type=str, default='all',
                        choices=['all', 'adam', 'lbfgs', 'aspqn', 'mspqn'])
    parser.add_argument('--device', type=str, default='cuda' if torch.cuda.is_available() else 'cpu')
    parser.add_argument('--results-dir', type=str, default='../results')
    parser.add_argument('--n-epochs', type=int, default=None)
    parser.add_argument('--k-s', type=int, default=50)
    parser.add_argument('--n-subdomains', type=int, default=None)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--quiet', action='store_true')
    args = parser.parse_args()

    if args.problem == 'all' and args.method == 'all':
        run_all_experiments(device=args.device, results_dir=args.results_dir,
                           verbose=not args.quiet)
    elif args.problem == 'all':
        for prob in ['burgers', 'klein_gordon', 'allen_cahn', 'advection_diffusion']:
            run_single_experiment(prob, args.method, device=args.device,
                                 n_epochs=args.n_epochs, k_s=args.k_s,
                                 n_subdomains=args.n_subdomains,
                                 verbose=not args.quiet)
    elif args.method == 'all':
        for method in ['adam', 'lbfgs', 'mspqn', 'aspqn']:
            run_single_experiment(args.problem, method, device=args.device,
                                 n_epochs=args.n_epochs, k_s=args.k_s,
                                 n_subdomains=args.n_subdomains,
                                 verbose=not args.quiet)
    else:
        result = run_single_experiment(args.problem, args.method, device=args.device,
                                       n_epochs=args.n_epochs, k_s=args.k_s,
                                       n_subdomains=args.n_subdomains,
                                       verbose=not args.quiet)
        # Save result
        os.makedirs(args.results_dir, exist_ok=True)
        fname = f"{args.problem}_{args.method}.json"
        result_s = {k: v for k, v in result.items()}
        for k in ['loss_history', 'error_history', 'time_history']:
            if result_s[k] is not None:
                result_s[k] = [float(v) if v is not None else None for v in result_s[k]]
        if result_s['final_error'] is not None:
            result_s['final_error'] = float(result_s['final_error'])
        with open(os.path.join(args.results_dir, fname), 'w') as f:
            json.dump(result_s, f, indent=2)
