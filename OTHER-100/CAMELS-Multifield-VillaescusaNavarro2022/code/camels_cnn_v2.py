"""
CAMELS Multifield Dataset - CNN Replication v2
Villaescusa-Navarro et al. 2022, ApJS 259, 61

Improved training with:
- 100 epochs
- ReduceLROnPlateau (saves best model properly)
- Hidden=12 (larger model)
- dr=0.15
"""

import numpy as np
import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
from torch.utils.data import Dataset, DataLoader
import os, sys, time, json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ============================================================
# CONFIGURATION
# ============================================================
DATA_DIR    = '/data/stevens/CAMELS/data'
OUT_DIR     = '/data/stevens/CAMELS/results'

F_MAPS      = os.path.join(DATA_DIR, 'Maps_Mgas_IllustrisTNG_LH_z=0.00.npy')
F_PARAMS    = os.path.join(DATA_DIR, 'params_LH_IllustrisTNG.txt')

SEED        = 1
SPLITS      = 15
BATCH_SIZE  = 128
LR          = 5e-4   # higher initial LR
WD          = 1e-4
DR          = 0.15
HIDDEN      = 12     # larger
EPOCHS      = 100
NUM_WORKERS = 8

PARAMS_IDX  = [0, 1]
PARAM_MIN   = np.array([0.1, 0.6, 0.25, 0.25, 0.5, 0.5])
PARAM_MAX   = np.array([0.5, 1.0, 4.00, 4.00, 2.0, 2.0])

os.makedirs(OUT_DIR, exist_ok=True)


# ============================================================
# ARCHITECTURE
# ============================================================
class model_e3_err(nn.Module):
    def __init__(self, hidden, dr, channels=1, num_params=2):
        super(model_e3_err, self).__init__()
        self.num_params = num_params
        
        self.C1 = nn.Conv2d(channels, hidden, kernel_size=4, stride=2, padding=1,
                            padding_mode='circular', bias=True)
        self.B1 = nn.BatchNorm2d(hidden)
        self.C2 = nn.Conv2d(hidden, 2*hidden, kernel_size=5, stride=2, padding=2,
                            padding_mode='circular', bias=True)
        self.B2 = nn.BatchNorm2d(2*hidden)
        self.C3 = nn.Conv2d(2*hidden, 4*hidden, kernel_size=4, stride=2, padding=1,
                            padding_mode='circular', bias=True)
        self.B3 = nn.BatchNorm2d(4*hidden)
        self.C4 = nn.Conv2d(4*hidden, 8*hidden, kernel_size=5, stride=2, padding=2,
                            padding_mode='circular', bias=True)
        self.B4 = nn.BatchNorm2d(8*hidden)
        self.C5 = nn.Conv2d(8*hidden, 16*hidden, kernel_size=5, stride=2, padding=2,
                            padding_mode='circular', bias=True)
        self.B5 = nn.BatchNorm2d(16*hidden)
        self.C6 = nn.Conv2d(16*hidden, 32*hidden, kernel_size=5, stride=2, padding=2,
                            padding_mode='circular', bias=True)
        self.B6 = nn.BatchNorm2d(32*hidden)
        
        self.flat_size = 32 * hidden * 4 * 4
        self.FC1 = nn.Linear(self.flat_size, 256)
        self.FC2 = nn.Linear(256, 2 * num_params)
        
        self.dropout   = nn.Dropout(p=dr)
        self.LeakyReLU = nn.LeakyReLU(0.2)
        
        for m in self.modules():
            if isinstance(m, (nn.BatchNorm2d, nn.BatchNorm1d)):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
            elif isinstance(m, (nn.Conv2d, nn.Linear)):
                nn.init.kaiming_normal_(m.weight)
                if m.bias is not None:
                    nn.init.zeros_(m.bias)

    def forward(self, x):
        x = self.LeakyReLU(self.B1(self.C1(x)))
        x = self.LeakyReLU(self.B2(self.C2(x)))
        x = self.LeakyReLU(self.B3(self.C3(x)))
        x = self.LeakyReLU(self.B4(self.C4(x)))
        x = self.LeakyReLU(self.B5(self.C5(x)))
        x = self.LeakyReLU(self.B6(self.C6(x)))
        x = x.view(x.shape[0], -1)
        x = self.dropout(self.LeakyReLU(self.FC1(x)))
        x = self.FC2(x)
        return x


# ============================================================
# DATASET
# ============================================================
class CAMELSDataset(Dataset):
    def __init__(self, mode, maps_data, params_all, sim_indices, augment=True, verbose=True):
        self.augment = augment
        
        map_indices = []
        for i in sim_indices:
            for j in range(SPLITS):
                map_indices.append(i * SPLITS + j)
        map_indices = np.array(map_indices, dtype=np.int64)
        
        data   = maps_data[map_indices]
        params = params_all[map_indices][:, PARAMS_IDX]
        
        if verbose:
            print(f'  {mode}: {len(sim_indices)} sims, {len(map_indices)} maps')
        
        self.x = torch.tensor(data[:, None, :, :], dtype=torch.float32)
        self.y = torch.tensor(params, dtype=torch.float32)
        self.size = len(map_indices)

    def __len__(self):
        return self.size

    def __getitem__(self, idx):
        x = self.x[idx]
        y = self.y[idx]
        if self.augment:
            rot  = np.random.randint(0, 4)
            flip = np.random.randint(0, 2)
            x = torch.rot90(x, k=rot, dims=[1, 2])
            if flip == 1:
                x = torch.flip(x, dims=[1])
        return x, y


def load_and_normalize_maps(verbose=True):
    if verbose: print(f'Loading maps...')
    maps = np.load(F_MAPS)
    maps = np.log10(maps)
    mean = np.mean(maps)
    std  = np.std(maps)
    maps = ((maps - mean) / std).astype(np.float32)
    
    params_sims = np.loadtxt(F_PARAMS)
    total_sims  = params_sims.shape[0]
    total_maps  = total_sims * SPLITS
    params_maps = np.zeros((total_maps, 6), dtype=np.float32)
    for i in range(total_sims):
        for j in range(SPLITS):
            params_maps[i*SPLITS + j] = params_sims[i]
    params_maps = (params_maps - PARAM_MIN) / (PARAM_MAX - PARAM_MIN)
    
    if verbose: print(f'  Shape: {maps.shape}, sims: {total_sims}')
    return maps, params_maps, total_sims


def build_split_indices(total_sims):
    np.random.seed(SEED)
    sims = np.arange(total_sims)
    np.random.shuffle(sims)
    n_train = int(0.80 * total_sims)
    n_valid = int(0.10 * total_sims)
    return sims[:n_train], sims[n_train:n_train+n_valid], sims[n_train+n_valid:]


def moment_loss(pred, target):
    num_params = target.shape[1]
    y_pred = pred[:, :num_params]
    e_pred = pred[:, num_params:]
    mse1 = torch.mean((y_pred - target)**2, dim=0)
    mse2 = torch.mean(((y_pred - target)**2 - e_pred**2)**2, dim=0)
    loss = torch.mean(torch.log(mse1) + torch.log(mse2))
    return loss, mse1


def train_epoch(model, loader, optimizer, device):
    model.train()
    total_loss, n = 0.0, 0
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        pred = model(x)
        loss, _ = moment_loss(pred, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * x.shape[0]
        n += x.shape[0]
    return total_loss / n


@torch.no_grad()
def evaluate(model, loader, device):
    model.eval()
    total_loss, n = 0.0, 0
    all_pred, all_true = [], []
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        pred = model(x)
        loss, _ = moment_loss(pred, y)
        total_loss += loss.item() * x.shape[0]
        n += x.shape[0]
        num_params = y.shape[1]
        all_pred.append(pred[:, :num_params].cpu().numpy())
        all_true.append(y.cpu().numpy())
    return total_loss / n, np.concatenate(all_pred), np.concatenate(all_true)


def compute_metrics(pred_norm, true_norm):
    param_min = PARAM_MIN[PARAMS_IDX]
    param_max = PARAM_MAX[PARAMS_IDX]
    pred = pred_norm * (param_max - param_min) + param_min
    true = true_norm * (param_max - param_min) + param_min
    rel_err = np.mean(np.abs(pred - true) / np.abs(true), axis=0)
    ss_res = np.sum((pred - true)**2, axis=0)
    ss_tot = np.sum((true - np.mean(true, axis=0))**2, axis=0)
    r2 = 1 - ss_res / ss_tot
    return rel_err, r2, pred, true


def scatter_plot(pred, true, fname):
    names = ['Omega_m', 'sigma_8']
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    for i, (ax, name) in enumerate(zip(axes, names)):
        ax.scatter(true[:, i], pred[:, i], alpha=0.3, s=5, c='steelblue')
        mn = min(true[:, i].min(), pred[:, i].min()) - 0.02
        mx = max(true[:, i].max(), pred[:, i].max()) + 0.02
        ax.plot([mn, mx], [mn, mx], 'r--', lw=1.5)
        rel_err = np.mean(np.abs(pred[:, i] - true[:, i]) / np.abs(true[:, i]))
        r2 = 1 - np.sum((pred[:, i] - true[:, i])**2) / np.sum((true[:, i] - np.mean(true[:, i]))**2)
        ax.set_xlabel(f'True {name}', fontsize=12)
        ax.set_ylabel(f'Predicted {name}', fontsize=12)
        ax.set_title(f'{name}: ε={rel_err*100:.2f}%, R²={r2:.4f}')
        ax.grid(True, alpha=0.3)
    plt.suptitle('CAMELS Mgas CNN - Test Set Results\n(Paper target: ~3-5% Omega_m, ~4-6% sigma_8)')
    plt.tight_layout()
    plt.savefig(fname, dpi=150)
    plt.close()
    print(f'  Saved scatter plot: {fname}')


def main():
    t0 = time.time()
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'Device: {device}')
    if torch.cuda.is_available():
        print(f'GPU: {torch.cuda.get_device_name(0)}')
    cudnn.benchmark = True
    
    print('\n=== Loading Data ===')
    maps, params_all, total_sims = load_and_normalize_maps()
    
    print('\n=== Splits ===')
    train_idx, valid_idx, test_idx = build_split_indices(total_sims)
    
    train_ds = CAMELSDataset('train', maps, params_all, train_idx, augment=True)
    valid_ds = CAMELSDataset('valid', maps, params_all, valid_idx, augment=False)
    test_ds  = CAMELSDataset('test',  maps, params_all, test_idx,  augment=False)
    
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True,  num_workers=NUM_WORKERS, pin_memory=True)
    valid_loader = DataLoader(valid_ds, batch_size=BATCH_SIZE, shuffle=False, num_workers=NUM_WORKERS, pin_memory=True)
    test_loader  = DataLoader(test_ds,  batch_size=BATCH_SIZE, shuffle=False, num_workers=NUM_WORKERS, pin_memory=True)
    
    print(f'Train: {len(train_ds)}, Valid: {len(valid_ds)}, Test: {len(test_ds)}')
    
    print('\n=== Model ===')
    model = model_e3_err(hidden=HIDDEN, dr=DR, channels=1, num_params=2).to(device)
    print(f'Parameters: {sum(p.numel() for p in model.parameters()):,}')
    
    optimizer = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=WD, betas=(0.5, 0.999))
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5,
                                                           patience=7, min_lr=1e-7, verbose=True)
    
    print('\n=== Training ===')
    best_val  = float('inf')
    best_path = os.path.join(OUT_DIR, 'best_model_v2.pt')
    train_losses, valid_losses = [], []
    
    with open(os.path.join(OUT_DIR, 'loss_v2.txt'), 'w') as f:
        f.write('epoch\ttrain\tvalid\n')
    
    for epoch in range(EPOCHS):
        tl = train_epoch(model, train_loader, optimizer, device)
        vl, vp, vt = evaluate(model, valid_loader, device)
        scheduler.step(vl)
        
        train_losses.append(tl)
        valid_losses.append(vl)
        
        flag = ''
        if vl < best_val:
            best_val = vl
            torch.save(model.state_dict(), best_path)
            flag = ' *** BEST ***'
        
        lr_now = optimizer.param_groups[0]['lr']
        print(f'Epoch {epoch:3d}/{EPOCHS}: train={tl:.4f} valid={vl:.4f} lr={lr_now:.2e}{flag}')
        
        with open(os.path.join(OUT_DIR, 'loss_v2.txt'), 'a') as f:
            f.write(f'{epoch}\t{tl:.6f}\t{vl:.6f}\n')
        
        if (epoch + 1) % 20 == 0:
            rel_err, r2, pred_p, true_p = compute_metrics(vp, vt)
            print(f'  Valid: Omega_m err={rel_err[0]*100:.2f}% R²={r2[0]:.4f} | sigma_8 err={rel_err[1]*100:.2f}% R²={r2[1]:.4f}')
    
    print('\n=== Test Evaluation ===')
    model.load_state_dict(torch.load(best_path, weights_only=False))
    tl_test, tp, tt = evaluate(model, test_loader, device)
    rel_err, r2, pred_p, true_p = compute_metrics(tp, tt)
    
    print(f'\n=== TEST RESULTS ===')
    print(f'Test loss: {tl_test:.4f}')
    print(f'Omega_m: relative error = {rel_err[0]*100:.2f}%, R² = {r2[0]:.4f}')
    print(f'sigma_8: relative error = {rel_err[1]*100:.2f}%, R² = {r2[1]:.4f}')
    print(f'\nPaper target (Table 2, Mgas, TNG): ~3-5% Omega_m, ~4-6% sigma_8')
    
    scatter_plot(pred_p, true_p, os.path.join(OUT_DIR, 'scatter_test_v2_final.png'))
    
    # Training curves
    plt.figure(figsize=(10, 5))
    plt.plot(train_losses, label='Train')
    plt.plot(valid_losses, label='Valid')
    plt.xlabel('Epoch')
    plt.ylabel('Moment network loss')
    plt.title('Training curves v2')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(OUT_DIR, 'training_curves_v2.png'), dpi=120)
    plt.close()
    
    wall = (time.time() - t0) / 3600
    
    results = {
        'run': 'v2_improved',
        'field': 'Mgas',
        'test_loss': float(tl_test),
        'Omega_m_rel_err_pct': float(rel_err[0] * 100),
        'Omega_m_r2': float(r2[0]),
        'sigma_8_rel_err_pct': float(rel_err[1] * 100),
        'sigma_8_r2': float(r2[1]),
        'wall_hours': wall,
        'epochs': EPOCHS,
        'hidden': HIDDEN,
        'dr': DR,
        'lr_init': LR,
        'paper_target_Om_pct': '3-5%',
        'paper_target_s8_pct': '4-6%',
    }
    with open(os.path.join(OUT_DIR, 'test_results_v2.json'), 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f'\nDone. Wall time: {wall:.3f} hours')
    return results


if __name__ == '__main__':
    main()
