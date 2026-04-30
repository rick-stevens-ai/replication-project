"""
Train neural network time-stepper with standard MSE loss.
Baseline for comparison with Godunov loss.

Paper: Cassia & Kerswell, arXiv:2405.11674
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

# Add code directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nn_models import BurgersMLPTimestepper, BurgersFNOTimestepper
from burgers_solver import generate_training_data, generate_test_cases, solve_burgers_godunov


def compute_metrics(u_pred, u_ref):
    """Compute L1, Linf, TV errors."""
    l1 = np.mean(np.abs(u_pred - u_ref))
    linf = np.max(np.abs(u_pred - u_ref))
    
    # Total variation
    tv_pred = np.sum(np.abs(np.diff(u_pred)))
    tv_ref = np.sum(np.abs(np.diff(u_ref)))
    tv_error = np.abs(tv_pred - tv_ref) / (tv_ref + 1e-10)
    
    return {
        'L1': float(l1),
        'Linf': float(linf),
        'TV_pred': float(tv_pred),
        'TV_ref': float(tv_ref),
        'TV_relative_error': float(tv_error),
    }


def multi_step_rollout(model, u0, num_steps, device):
    """
    Roll out model for multiple time steps.
    u^0 -> u^1 -> ... -> u^N
    """
    u = torch.tensor(u0, dtype=torch.float32, device=device).unsqueeze(0)
    trajectory = [u0.copy()]
    
    with torch.no_grad():
        for _ in range(num_steps):
            u = model(u)
            trajectory.append(u.cpu().numpy().squeeze())
    
    return trajectory


def train_mse(
    Nx=256,
    hidden_dim=256,
    num_layers=5,
    model_type='mlp',
    num_epochs=500,
    batch_size=64,
    lr=1e-3,
    weight_decay=1e-5,
    device='cuda',
    save_dir=None,
):
    """Train with MSE loss."""
    print("=" * 60)
    print("TRAINING WITH MSE LOSS")
    print("=" * 60)
    
    # Generate data
    print("\n1. Generating training data...")
    data = generate_training_data(Nx=Nx, num_ic=60, T_final=0.5, num_snapshots=25)
    x = data['x']
    dx = data['dx']
    dt_data = data['dt']
    
    u_n_all = np.array([s['u_n'] for s in data['samples']])
    u_np1_all = np.array([s['u_np1'] for s in data['samples']])
    
    # Split train/val
    N = len(u_n_all)
    idx = np.random.RandomState(123).permutation(N)
    n_train = int(0.85 * N)
    train_idx, val_idx = idx[:n_train], idx[n_train:]
    
    u_n_train = torch.tensor(u_n_all[train_idx], dtype=torch.float32)
    u_np1_train = torch.tensor(u_np1_all[train_idx], dtype=torch.float32)
    u_n_val = torch.tensor(u_n_all[val_idx], dtype=torch.float32)
    u_np1_val = torch.tensor(u_np1_all[val_idx], dtype=torch.float32)
    
    print(f"   Train: {len(train_idx)}, Val: {len(val_idx)}")
    
    train_ds = TensorDataset(u_n_train, u_np1_train)
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
    val_losses = []
    best_val_loss = float('inf')
    
    t_start = time.time()
    
    for epoch in range(num_epochs):
        model.train()
        epoch_loss = 0.0
        n_batches = 0
        
        for u_n_batch, u_np1_batch in train_dl:
            u_n_batch = u_n_batch.to(device)
            u_np1_batch = u_np1_batch.to(device)
            
            optimizer.zero_grad()
            u_pred = model(u_n_batch)
            loss = nn.functional.mse_loss(u_pred, u_np1_batch)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            
            epoch_loss += loss.item()
            n_batches += 1
        
        scheduler.step()
        
        avg_loss = epoch_loss / max(n_batches, 1)
        train_losses.append(avg_loss)
        
        # Validation
        model.eval()
        with torch.no_grad():
            u_pred_val = model(u_n_val.to(device))
            val_loss = nn.functional.mse_loss(u_pred_val, u_np1_val.to(device)).item()
        val_losses.append(val_loss)
        
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            if save_dir:
                torch.save(model.state_dict(), os.path.join(save_dir, 'model_mse_best.pt'))
        
        if (epoch + 1) % 50 == 0 or epoch == 0:
            elapsed = time.time() - t_start
            print(f"   Epoch {epoch+1:4d}/{num_epochs} | "
                  f"Train: {avg_loss:.6e} | Val: {val_loss:.6e} | "
                  f"Time: {elapsed:.1f}s")
    
    total_time = time.time() - t_start
    print(f"\n   Training complete in {total_time:.1f}s")
    
    # Save final model
    if save_dir:
        torch.save(model.state_dict(), os.path.join(save_dir, 'model_mse_final.pt'))
    
    # Evaluate on test cases
    print("\n3. Evaluating on test cases...")
    x_test, dx_test, test_cases = generate_test_cases(Nx=Nx)
    
    results = {}
    for tc in test_cases:
        # Run multi-step rollout
        # Determine number of steps
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
        'loss_type': 'MSE',
        'train_losses': train_losses,
        'val_losses': val_losses,
        'test_results': results,
        'total_time': total_time,
        'n_params': n_params,
        'config': {
            'Nx': Nx, 'hidden_dim': hidden_dim, 'num_layers': num_layers,
            'num_epochs': num_epochs, 'batch_size': batch_size, 'lr': lr,
        }
    }


if __name__ == '__main__':
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    save_dir = os.path.join(base_dir, 'results')
    os.makedirs(save_dir, exist_ok=True)
    
    results = train_mse(
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
    
    # Save results (convert non-serializable items)
    results_save = {k: v for k, v in results.items() if k not in ('train_losses', 'val_losses')}
    results_save['train_losses'] = [float(x) for x in results['train_losses']]
    results_save['val_losses'] = [float(x) for x in results['val_losses']]
    
    with open(os.path.join(save_dir, 'results_mse.json'), 'w') as f:
        json.dump(results_save, f, indent=2)
    
    # Also save losses as numpy for plotting
    np.savez(os.path.join(save_dir, 'losses_mse.npz'),
             train=results['train_losses'],
             val=results['val_losses'])
    
    print(f"\nResults saved to {save_dir}/")
