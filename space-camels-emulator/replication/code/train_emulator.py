#!/usr/bin/env python3
"""
Train the final P(k) emulator with tuned hyperparameters.

Architecture: 6 → 256 → 256 → 256 → 256 → 50 (~200k params)
Key improvements over v1:
- GELU activations
- Cosine annealing LR
- Longer training with more patience  
- Proper weight decay
"""

import os
import json
import time
import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

SEED = 42
BATCH_SIZE = 64
LR = 1e-3
N_EPOCHS = 10000
HIDDEN_DIM = 256
N_HIDDEN = 4
TEST_FRAC = 0.2
PATIENCE = 1500

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

np.random.seed(SEED)
torch.manual_seed(SEED)

class PKEmulator(nn.Module):
    """MLP with GELU activations."""
    def __init__(self, n_input=6, n_output=50, hidden_dim=256, n_hidden=4):
        super().__init__()
        layers = [nn.Linear(n_input, hidden_dim), nn.GELU()]
        for _ in range(n_hidden - 1):
            layers += [nn.Linear(hidden_dim, hidden_dim), nn.GELU()]
        layers.append(nn.Linear(hidden_dim, n_output))
        self.net = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.net(x)

def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    params = np.load(os.path.join(DATA_DIR, "params.npy"))
    pks = np.load(os.path.join(DATA_DIR, "pks.npy"))
    k_bins = np.load(os.path.join(DATA_DIR, "k_bins.npy"))
    
    valid = ~np.any(np.isnan(pks), axis=1)
    params = params[valid]
    pks = pks[valid]
    print(f"Data: {params.shape[0]} cosmologies, {len(k_bins)} k-bins")
    
    log_pks = np.log10(pks)
    
    param_mean = params.mean(axis=0)
    param_std = params.std(axis=0)
    params_norm = (params - param_mean) / param_std
    
    logpk_mean = log_pks.mean(axis=0)
    logpk_std = log_pks.std(axis=0)
    logpk_norm = (log_pks - logpk_mean) / logpk_std
    
    n = params.shape[0]
    n_test = int(n * TEST_FRAC)
    n_train = n - n_test
    
    rng = np.random.RandomState(SEED)
    idx = rng.permutation(n)
    train_idx = idx[:n_train]
    test_idx = idx[n_train:]
    
    X_train = torch.tensor(params_norm[train_idx], dtype=torch.float32)
    Y_train = torch.tensor(logpk_norm[train_idx], dtype=torch.float32)
    X_test = torch.tensor(params_norm[test_idx], dtype=torch.float32)
    Y_test = torch.tensor(logpk_norm[test_idx], dtype=torch.float32)
    
    print(f"Train: {n_train}, Test: {n_test}")
    
    train_ds = TensorDataset(X_train, Y_train)
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
    
    model = PKEmulator(n_input=6, n_output=len(k_bins), 
                       hidden_dim=HIDDEN_DIM, n_hidden=N_HIDDEN).to(device)
    n_params = count_parameters(model)
    print(f"Model: {n_params:,} parameters")
    
    optimizer = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=1e-5)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(
        optimizer, T_0=1000, T_mult=2, eta_min=1e-6
    )
    criterion = nn.MSELoss()
    
    best_test_loss = float('inf')
    best_epoch = 0
    train_losses = []
    test_losses = []
    
    t0 = time.time()
    for epoch in range(N_EPOCHS):
        model.train()
        epoch_loss = 0
        for xb, yb in train_loader:
            xb, yb = xb.to(device), yb.to(device)
            pred = model(xb)
            loss = criterion(pred, yb)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item() * xb.size(0)
        epoch_loss /= n_train
        train_losses.append(epoch_loss)
        
        scheduler.step()
        
        model.eval()
        with torch.no_grad():
            pred_test = model(X_test.to(device))
            test_loss = criterion(pred_test, Y_test.to(device)).item()
        test_losses.append(test_loss)
        
        if test_loss < best_test_loss:
            best_test_loss = test_loss
            best_epoch = epoch
            torch.save({
                'model_state_dict': model.state_dict(),
                'param_mean': param_mean,
                'param_std': param_std,
                'logpk_mean': logpk_mean,
                'logpk_std': logpk_std,
                'k_bins': k_bins,
                'train_idx': train_idx,
                'test_idx': test_idx,
                'n_params': n_params,
                'model_type': 'final',
                'hidden_dim': HIDDEN_DIM,
                'n_hidden': N_HIDDEN,
            }, os.path.join(DATA_DIR, "emulator_best.pt"))
        
        if epoch - best_epoch > PATIENCE:
            print(f"\nEarly stopping at epoch {epoch} (best: {best_epoch})")
            break
        
        if (epoch + 1) % 500 == 0:
            elapsed = time.time() - t0
            lr_now = optimizer.param_groups[0]['lr']
            print(f"  Epoch {epoch+1:5d}: train={epoch_loss:.6f} test={test_loss:.6f} "
                  f"best={best_test_loss:.6f} (ep {best_epoch}) lr={lr_now:.1e} {elapsed:.0f}s")
    
    total_time = time.time() - t0
    print(f"\nDone in {total_time:.1f}s. Best test loss: {best_test_loss:.6f} at epoch {best_epoch}")
    
    history = {
        'train_losses': [float(x) for x in train_losses],
        'test_losses': [float(x) for x in test_losses],
        'best_epoch': int(best_epoch),
        'best_test_loss': float(best_test_loss),
        'n_params': int(n_params),
        'n_train': int(n_train),
        'n_test': int(n_test),
        'training_time_s': float(total_time),
    }
    with open(os.path.join(RESULTS_DIR, "training_history.json"), 'w') as f:
        json.dump(history, f, indent=2)

if __name__ == "__main__":
    main()
