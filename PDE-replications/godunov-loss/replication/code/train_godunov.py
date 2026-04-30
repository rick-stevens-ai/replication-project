"""
Train neural network time-stepper with Godunov loss.
Implements the core idea from Cassia & Kerswell (arXiv:2405.11674):
  Physics-informed loss using Godunov-type FVM residual.

The Godunov loss penalizes violations of the discrete conservation law:
  u_i^{n+1} = u_i^n - (dt/dx) * [F_{i+1/2} - F_{i-1/2}]
where F is the Godunov flux (exact Riemann solver for scalar Burgers).

We train in two modes:
  1. Hybrid: L = L_MSE + lambda_G * L_Godunov  (semi-supervised)
  2. Pure Godunov: L = L_Godunov  (unsupervised, as in paper)
"""

import os
import sys
import json
import time
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nn_models import (BurgersMLPTimestepper, BurgersFNOTimestepper,
                       compute_godunov_residual, godunov_flux_burgers_torch)
from burgers_solver import generate_training_data, generate_test_cases, solve_burgers_godunov
from train_mse import compute_metrics, multi_step_rollout


def compute_tv_penalty(u):
    """Total variation penalty: encourages TVD property."""
    return torch.mean(torch.sum(torch.abs(u[:, 1:] - u[:, :-1]), dim=1))


def train_godunov(
    Nx=256,
    hidden_dim=256,
    num_layers=5,
    model_type='mlp',
    num_epochs=500,
    batch_size=64,
    lr=1e-3,
    weight_decay=1e-5,
    lambda_g=1.0,
    lambda_tv=0.0,
    mode='hybrid',  # 'hybrid', 'pure_godunov', 'godunov_mse'
    device='cuda',
    save_dir=None,
):
    """
    Train with Godunov-informed loss.
    
    Modes:
      'hybrid': L = L_MSE + lambda_g * L_Godunov
      'pure_godunov': L = L_Godunov (unsupervised, like paper)
      'godunov_mse': L = L_Godunov + lambda_g * L_MSE (Godunov-primary)
    """
    mode_label = f"GODUNOV ({mode})"
    print("=" * 60)
    print(f"TRAINING WITH {mode_label}")
    print(f"  lambda_g={lambda_g}, lambda_tv={lambda_tv}")
    print("=" * 60)
    
    # Generate data
    print("\n1. Generating training data...")
    data = generate_training_data(Nx=Nx, num_ic=60, T_final=0.5, num_snapshots=25)
    x = data['x']
    dx = data['dx']
    dt_data = data['dt']
    
    u_n_all = np.array([s['u_n'] for s in data['samples']])
    u_np1_all = np.array([s['u_np1'] for s in data['samples']])
    dt_all = np.array([s['t_np1'] - s['t_n'] for s in data['samples']])
    
    # Split train/val
    N = len(u_n_all)
    idx = np.random.RandomState(123).permutation(N)
    n_train = int(0.85 * N)
    train_idx, val_idx = idx[:n_train], idx[n_train:]
    
    u_n_train = torch.tensor(u_n_all[train_idx], dtype=torch.float32)
    u_np1_train = torch.tensor(u_np1_all[train_idx], dtype=torch.float32)
    dt_train = torch.tensor(dt_all[train_idx], dtype=torch.float32)
    u_n_val = torch.tensor(u_n_all[val_idx], dtype=torch.float32)
    u_np1_val = torch.tensor(u_np1_all[val_idx], dtype=torch.float32)
    dt_val = torch.tensor(dt_all[val_idx], dtype=torch.float32)
    
    print(f"   Train: {len(train_idx)}, Val: {len(val_idx)}")
    
    train_ds = TensorDataset(u_n_train, u_np1_train, dt_train)
    train_dl = DataLoader(train_ds, batch_size=batch_size, shuffle=True, drop_last=True)
    
    # Model
    if model_type == 'mlp':
        model = BurgersMLPTimestepper(Nx, hidden_dim=hidden_dim, num_layers=num_layers, dt=dt_data)
    else:
        model = BurgersFNOTimestepper(Nx, modes=16, width=32, num_layers=4, dt=dt_data)
    
    model = model.to(device)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"   Model: {model_type}, params: {n_params:,}")
    
    optimizer = optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=num_epochs)
    
    # Training loop
    print("\n2. Training...")
    train_losses = []
    train_mse_losses = []
    train_god_losses = []
    val_losses = []
    best_val_loss = float('inf')
    
    t_start = time.time()
    
    for epoch in range(num_epochs):
        model.train()
        epoch_loss = 0.0
        epoch_mse = 0.0
        epoch_god = 0.0
        n_batches = 0
        
        for u_n_batch, u_np1_batch, dt_batch in train_dl:
            u_n_batch = u_n_batch.to(device)
            u_np1_batch = u_np1_batch.to(device)
            dt_batch = dt_batch.to(device)
            
            optimizer.zero_grad()
            
            # Forward pass
            u_pred = model(u_n_batch)
            
            # MSE loss
            loss_mse = nn.functional.mse_loss(u_pred, u_np1_batch)
            
            # Godunov loss: use the per-sample dt
            # For simplicity, use mean dt for the batch
            dt_mean = dt_batch.mean().item()
            residual = compute_godunov_residual(u_n_batch, u_pred, dx, dt_mean)
            loss_god = torch.mean(residual ** 2)
            
            # TV penalty
            loss_tv = compute_tv_penalty(u_pred) if lambda_tv > 0 else torch.tensor(0.0)
            
            # Combined loss
            if mode == 'hybrid':
                loss = loss_mse + lambda_g * loss_god + lambda_tv * loss_tv
            elif mode == 'pure_godunov':
                loss = loss_god + lambda_tv * loss_tv
            elif mode == 'godunov_mse':
                loss = loss_god + lambda_g * loss_mse + lambda_tv * loss_tv
            else:
                raise ValueError(f"Unknown mode: {mode}")
            
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            
            epoch_loss += loss.item()
            epoch_mse += loss_mse.item()
            epoch_god += loss_god.item()
            n_batches += 1
        
        scheduler.step()
        
        avg_loss = epoch_loss / max(n_batches, 1)
        avg_mse = epoch_mse / max(n_batches, 1)
        avg_god = epoch_god / max(n_batches, 1)
        train_losses.append(avg_loss)
        train_mse_losses.append(avg_mse)
        train_god_losses.append(avg_god)
        
        # Validation (MSE for fair comparison)
        model.eval()
        with torch.no_grad():
            u_pred_val = model(u_n_val.to(device))
            val_loss = nn.functional.mse_loss(u_pred_val, u_np1_val.to(device)).item()
        val_losses.append(val_loss)
        
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            if save_dir:
                torch.save(model.state_dict(), 
                          os.path.join(save_dir, f'model_godunov_{mode}_best.pt'))
        
        if (epoch + 1) % 50 == 0 or epoch == 0:
            elapsed = time.time() - t_start
            print(f"   Epoch {epoch+1:4d}/{num_epochs} | "
                  f"Total: {avg_loss:.6e} | MSE: {avg_mse:.6e} | "
                  f"God: {avg_god:.6e} | Val: {val_loss:.6e} | "
                  f"Time: {elapsed:.1f}s")
    
    total_time = time.time() - t_start
    print(f"\n   Training complete in {total_time:.1f}s")
    
    # Save final model
    if save_dir:
        torch.save(model.state_dict(), 
                  os.path.join(save_dir, f'model_godunov_{mode}_final.pt'))
    
    # Evaluate on test cases
    print("\n3. Evaluating on test cases...")
    x_test, dx_test, test_cases = generate_test_cases(Nx=Nx)
    
    results = {}
    for tc in test_cases:
        amax = max(np.max(np.abs(tc['u0'])), 0.5)
        dt_step = 0.4 * dx_test / amax
        num_steps = int(tc['T'] / dt_step) + 1
        
        trajectory = multi_step_rollout(model, tc['u0'], num_steps, device)
        u_pred = trajectory[-1]
        u_ref = tc['u_ref']
        
        metrics = compute_metrics(u_pred, u_ref)
        results[tc['name']] = metrics
        print(f"   {tc['name']:20s} | L1={metrics['L1']:.6e} | "
              f"Linf={metrics['Linf']:.6e} | TV_err={metrics['TV_relative_error']:.4f}")
    
    return {
        'model_type': model_type,
        'loss_type': f'Godunov_{mode}',
        'train_losses': train_losses,
        'train_mse_losses': train_mse_losses,
        'train_god_losses': train_god_losses,
        'val_losses': val_losses,
        'test_results': results,
        'total_time': total_time,
        'n_params': n_params,
        'config': {
            'Nx': Nx, 'hidden_dim': hidden_dim, 'num_layers': num_layers,
            'num_epochs': num_epochs, 'batch_size': batch_size, 'lr': lr,
            'lambda_g': lambda_g, 'lambda_tv': lambda_tv, 'mode': mode,
        }
    }


if __name__ == '__main__':
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    save_dir = os.path.join(base_dir, 'results')
    os.makedirs(save_dir, exist_ok=True)
    
    # Train with hybrid loss (MSE + Godunov)
    results = train_godunov(
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
    
    results_save = {k: v for k, v in results.items() 
                    if k not in ('train_losses', 'val_losses', 'train_mse_losses', 'train_god_losses')}
    results_save['train_losses'] = [float(x) for x in results['train_losses']]
    results_save['val_losses'] = [float(x) for x in results['val_losses']]
    results_save['train_mse_losses'] = [float(x) for x in results['train_mse_losses']]
    results_save['train_god_losses'] = [float(x) for x in results['train_god_losses']]
    
    with open(os.path.join(save_dir, 'results_godunov.json'), 'w') as f:
        json.dump(results_save, f, indent=2)
    
    np.savez(os.path.join(save_dir, 'losses_godunov.npz'),
             train=results['train_losses'],
             val=results['val_losses'],
             train_mse=results['train_mse_losses'],
             train_god=results['train_god_losses'])
    
    print(f"\nResults saved to {save_dir}/")
