#!/usr/bin/env python3
"""
Master script: generates data, trains both models, produces figures.
Run on GPU (uicgpu A100).
"""

import os
import sys
import json
import numpy as np
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import torch


def main():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Device: {device}")
    if device == 'cuda':
        print(f"GPU: {torch.cuda.get_device_name(0)}")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    save_dir = os.path.join(base_dir, 'results')
    fig_dir = os.path.join(base_dir, 'figures')
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)
    
    t_total_start = time.time()
    
    # ---- Step 1: Generate data ----
    print("\n" + "=" * 60)
    print("STEP 1: Generate training data and test cases")
    print("=" * 60)
    from burgers_solver import generate_training_data, generate_test_cases
    
    data = generate_training_data(Nx=256, num_ic=60, T_final=0.5, num_snapshots=25)
    print(f"Training samples: {len(data['samples'])}")
    
    x_test, dx_test, test_cases = generate_test_cases(Nx=256)
    print(f"Test cases: {len(test_cases)}")
    
    # ---- Step 2: Train MSE model ----
    print("\n" + "=" * 60)
    print("STEP 2: Train MSE model")
    print("=" * 60)
    from train_mse import train_mse
    
    results_mse = train_mse(
        Nx=256,
        hidden_dim=256,
        num_layers=5,
        model_type='mlp',
        num_epochs=500,
        batch_size=64,
        lr=1e-3,
        device=device,
        save_dir=save_dir,
    )
    
    # Save MSE results
    results_mse_save = {k: v for k, v in results_mse.items() 
                        if k not in ('train_losses', 'val_losses')}
    results_mse_save['train_losses'] = [float(x) for x in results_mse['train_losses']]
    results_mse_save['val_losses'] = [float(x) for x in results_mse['val_losses']]
    with open(os.path.join(save_dir, 'results_mse.json'), 'w') as f:
        json.dump(results_mse_save, f, indent=2)
    np.savez(os.path.join(save_dir, 'losses_mse.npz'),
             train=results_mse['train_losses'], val=results_mse['val_losses'])
    
    # ---- Step 3: Train Godunov model (hybrid) ----
    print("\n" + "=" * 60)
    print("STEP 3: Train Godunov model (hybrid MSE+Godunov)")
    print("=" * 60)
    from train_godunov import train_godunov
    
    results_god = train_godunov(
        Nx=256,
        hidden_dim=256,
        num_layers=5,
        model_type='mlp',
        num_epochs=500,
        batch_size=64,
        lr=1e-3,
        lambda_g=10.0,
        lambda_tv=0.001,
        mode='hybrid',
        device=device,
        save_dir=save_dir,
    )
    
    results_god_save = {k: v for k, v in results_god.items() 
                        if k not in ('train_losses', 'val_losses', 'train_mse_losses', 'train_god_losses')}
    results_god_save['train_losses'] = [float(x) for x in results_god['train_losses']]
    results_god_save['val_losses'] = [float(x) for x in results_god['val_losses']]
    results_god_save['train_mse_losses'] = [float(x) for x in results_god['train_mse_losses']]
    results_god_save['train_god_losses'] = [float(x) for x in results_god['train_god_losses']]
    with open(os.path.join(save_dir, 'results_godunov.json'), 'w') as f:
        json.dump(results_god_save, f, indent=2)
    np.savez(os.path.join(save_dir, 'losses_godunov.npz'),
             train=results_god['train_losses'], val=results_god['val_losses'],
             train_mse=results_god['train_mse_losses'],
             train_god=results_god['train_god_losses'])
    
    # ---- Step 4: Generate prediction data for plotting ----
    print("\n" + "=" * 60)
    print("STEP 4: Generating prediction data for figures")
    print("=" * 60)
    from nn_models import BurgersMLPTimestepper
    from train_mse import multi_step_rollout
    
    # Reload best models
    model_mse = BurgersMLPTimestepper(256, hidden_dim=256, num_layers=5, dt=data['dt']).to(device)
    model_god = BurgersMLPTimestepper(256, hidden_dim=256, num_layers=5, dt=data['dt']).to(device)
    
    mse_ckpt = os.path.join(save_dir, 'model_mse_best.pt')
    god_ckpt = os.path.join(save_dir, 'model_godunov_hybrid_best.pt')
    
    if os.path.exists(mse_ckpt):
        model_mse.load_state_dict(torch.load(mse_ckpt, map_location=device))
    if os.path.exists(god_ckpt):
        model_god.load_state_dict(torch.load(god_ckpt, map_location=device))
    
    model_mse.eval()
    model_god.eval()
    
    # Generate predictions for each test case
    pred_data = {}
    for tc in test_cases:
        amax = max(np.max(np.abs(tc['u0'])), 0.5)
        dt_step = 0.4 * dx_test / amax
        num_steps = int(tc['T'] / dt_step) + 1
        
        traj_mse = multi_step_rollout(model_mse, tc['u0'], num_steps, device)
        traj_god = multi_step_rollout(model_god, tc['u0'], num_steps, device)
        
        pred_data[tc['name']] = {
            'u0': tc['u0'],
            'u_ref': tc['u_ref'],
            'u_mse': traj_mse[-1],
            'u_god': traj_god[-1],
            'description': tc['description'],
        }
    
    np.savez(os.path.join(save_dir, 'predictions.npz'),
             x=x_test,
             **{f"{name}_u0": d['u0'] for name, d in pred_data.items()},
             **{f"{name}_ref": d['u_ref'] for name, d in pred_data.items()},
             **{f"{name}_mse": d['u_mse'] for name, d in pred_data.items()},
             **{f"{name}_god": d['u_god'] for name, d in pred_data.items()})
    
    # ---- Step 5: Summary ----
    total_time = time.time() - t_total_start
    print("\n" + "=" * 60)
    print(f"ALL DONE in {total_time:.1f}s ({total_time/60:.1f} min)")
    print("=" * 60)
    
    # Summary comparison
    print("\nTest Results Comparison:")
    print(f"{'Test Case':20s} | {'Metric':8s} | {'MSE Loss':12s} | {'Godunov Loss':12s} | {'Winner':8s}")
    print("-" * 75)
    
    summary = {}
    for name in results_mse['test_results']:
        mse_metrics = results_mse['test_results'][name]
        god_metrics = results_god['test_results'][name]
        
        summary[name] = {}
        for metric in ['L1', 'Linf', 'TV_relative_error']:
            m_val = mse_metrics[metric]
            g_val = god_metrics[metric]
            winner = 'Godunov' if g_val < m_val else 'MSE'
            summary[name][metric] = {
                'mse': m_val, 'godunov': g_val, 'winner': winner
            }
            print(f"{name:20s} | {metric:8s} | {m_val:12.6e} | {g_val:12.6e} | {winner:8s}")
    
    with open(os.path.join(save_dir, 'summary.json'), 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nAll results saved to {save_dir}/")
    
    # ---- Step 6: Generate figures ----
    print("\n" + "=" * 60)
    print("STEP 6: Generating figures")
    print("=" * 60)
    from plot_results import plot_shock_comparison, plot_shock_detail, plot_loss_curves, plot_error_bars
    plot_shock_comparison(save_dir, fig_dir)
    plot_shock_detail(save_dir, fig_dir)
    plot_loss_curves(save_dir, fig_dir)
    plot_error_bars(save_dir, fig_dir)
    print(f"Figures saved to {fig_dir}/")


if __name__ == '__main__':
    main()
