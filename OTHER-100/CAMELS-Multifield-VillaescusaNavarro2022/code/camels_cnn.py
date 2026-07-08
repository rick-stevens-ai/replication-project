"""
CAMELS Multifield Dataset - CNN Replication
Villaescusa-Navarro et al. 2022, ApJS 259, 61

Replicates: CNN trained on Mgas maps to predict (Omega_m, sigma_8)
Architecture: model_e3_err (6-layer CNN with circular padding + moment network)
Loss: log(MSE_mean) + log(MSE_variance) - moment network loss
Split: 80/10/10 by simulation to avoid leakage
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
from tqdm import tqdm

# ============================================================
# CONFIGURATION
# ============================================================
DATA_DIR    = '/data/stevens/CAMELS/data'
OUT_DIR     = '/data/stevens/CAMELS/results'
CODE_DIR    = '/data/stevens/CAMELS/code'
REPORT_DIR  = '/data/stevens/CAMELS/report'

F_MAPS      = os.path.join(DATA_DIR, 'Maps_Mgas_IllustrisTNG_LH_z=0.00.npy')
F_PARAMS    = os.path.join(DATA_DIR, 'params_LH_IllustrisTNG.txt')

SEED        = 1
SPLITS      = 15       # maps per simulation
BATCH_SIZE  = 128
LR          = 1e-4
WD          = 1e-4
DR          = 0.2
HIDDEN      = 8
EPOCHS      = 50
NUM_WORKERS = 8

# Parameter indices: 0=Omega_m, 1=sigma_8
PARAMS_IDX  = [0, 1]

# Parameter normalization ranges (from paper data.py)
PARAM_MIN   = np.array([0.1, 0.6, 0.25, 0.25, 0.5, 0.5])
PARAM_MAX   = np.array([0.5, 1.0, 4.00, 4.00, 2.0, 2.0])

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(CODE_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(os.path.join(OUT_DIR, 'sanity'), exist_ok=True)


# ============================================================
# ARCHITECTURE - model_e3_err (from paper)
# 6-layer CNN with circular padding + moment network head
# ============================================================
class model_e3_err(nn.Module):
    """
    Architecture from Villaescusa-Navarro+2022 CMD paper.
    6 conv layers with circular padding (periodic boundary conditions).
    Output: 2*num_params (mean + uncertainty for each param).
    """
    def __init__(self, hidden, dr, channels=1, num_params=2):
        super(model_e3_err, self).__init__()
        
        self.num_params = num_params
        
        # 6 conv blocks with circular padding (respects periodic box BC)
        # input: channels x 256 x 256 -> output: hidden x 128 x 128
        self.C1 = nn.Conv2d(channels,    hidden,    kernel_size=4, stride=2, padding=1,
                            padding_mode='circular', bias=True)
        self.B1 = nn.BatchNorm2d(hidden)
        # hidden x 128 x 128 -> 2*hidden x 64 x 64
        self.C2 = nn.Conv2d(hidden,   2*hidden, kernel_size=5, stride=2, padding=2,
                            padding_mode='circular', bias=True)
        self.B2 = nn.BatchNorm2d(2*hidden)
        # 2*hidden x 64 x 64 -> 4*hidden x 32 x 32
        self.C3 = nn.Conv2d(2*hidden, 4*hidden, kernel_size=4, stride=2, padding=1,
                            padding_mode='circular', bias=True)
        self.B3 = nn.BatchNorm2d(4*hidden)
        # 4*hidden x 32 x 32 -> 8*hidden x 16 x 16
        self.C4 = nn.Conv2d(4*hidden, 8*hidden, kernel_size=5, stride=2, padding=2,
                            padding_mode='circular', bias=True)
        self.B4 = nn.BatchNorm2d(8*hidden)
        # 8*hidden x 16 x 16 -> 16*hidden x 8 x 8
        self.C5 = nn.Conv2d(8*hidden, 16*hidden, kernel_size=5, stride=2, padding=2,
                            padding_mode='circular', bias=True)
        self.B5 = nn.BatchNorm2d(16*hidden)
        # 16*hidden x 8 x 8 -> 32*hidden x 4 x 4
        self.C6 = nn.Conv2d(16*hidden, 32*hidden, kernel_size=5, stride=2, padding=2,
                            padding_mode='circular', bias=True)
        self.B6 = nn.BatchNorm2d(32*hidden)
        
        # Compute flattened size
        # 256 -> 128 -> 64 -> 32 -> 16 -> 8 -> 4  => 4x4 feature maps
        self.flat_size = 32 * hidden * 4 * 4
        
        self.FC1 = nn.Linear(self.flat_size, 256)
        self.FC2 = nn.Linear(256, 2 * num_params)   # mean + log_var for each param
        
        self.dropout   = nn.Dropout(p=dr)
        self.LeakyReLU = nn.LeakyReLU(0.2)
        
        # Kaiming init
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
        return x   # [batch, 2*num_params]: first num_params=mean, last num_params=log_var


# ============================================================
# DATASET
# ============================================================
class CAMELSDataset(Dataset):
    """
    CAMELS dataset for parameter inference.
    
    Key design: split by simulation to avoid data leakage.
    1000 simulations × 15 maps each = 15000 total maps at z=0.
    Split: 80/10/10 = 800/100/100 sims = 12000/1500/1500 maps.
    
    Maps are log10-transformed and z-score normalized.
    Data augmentation: random rotations + flips during training.
    """
    def __init__(self, mode, maps_data, params_all, sim_indices, augment=True, verbose=True):
        """
        mode: 'train', 'valid', or 'test'
        maps_data: normalized maps array [N_maps, H, W] 
        params_all: normalized params array [N_maps, num_params]
        sim_indices: array of simulation indices for this split
        """
        self.augment = augment
        
        # Build map indices from sim indices (each sim has SPLITS maps)
        map_indices = []
        for i in sim_indices:
            for j in range(SPLITS):
                map_indices.append(i * SPLITS + j)
        map_indices = np.array(map_indices, dtype=np.int64)
        
        # Load subset
        data   = maps_data[map_indices]     # [N, H, W]
        params = params_all[map_indices]    # [N, 6]
        
        # Only keep Omega_m and sigma_8
        params = params[:, PARAMS_IDX]     # [N, 2]
        
        if verbose:
            print(f'  {mode}: {len(sim_indices)} sims, {len(map_indices)} maps')
            print(f'  Omega_m: [{params[:,0].min():.3f}, {params[:,0].max():.3f}]')
            print(f'  sigma_8: [{params[:,1].min():.3f}, {params[:,1].max():.3f}]')
        
        self.x = torch.tensor(data[:, None, :, :], dtype=torch.float32)  # [N,1,H,W]
        self.y = torch.tensor(params, dtype=torch.float32)
        self.size = len(map_indices)

    def __len__(self):
        return self.size

    def __getitem__(self, idx):
        x = self.x[idx]
        y = self.y[idx]
        
        if self.augment:
            # Random rotation (0, 90, 180, 270 degrees)
            rot  = np.random.randint(0, 4)
            flip = np.random.randint(0, 2)
            x = torch.rot90(x, k=rot, dims=[1, 2])
            if flip == 1:
                x = torch.flip(x, dims=[1])
        
        return x, y


def load_and_normalize_maps(f_maps, f_params, verbose=True):
    """Load maps, log-transform, z-score normalize."""
    if verbose:
        print(f'Loading maps from {f_maps}...')
    
    maps = np.load(f_maps)  # [N_maps, H, W]
    if verbose:
        print(f'  Shape: {maps.shape}, dtype: {maps.dtype}')
        print(f'  Raw range: [{maps.min():.3e}, {maps.max():.3e}]')
    
    # Log10 transform (paper approach)
    maps = np.log10(maps)
    if verbose:
        print(f'  Log10 range: [{maps.min():.3f}, {maps.max():.3f}]')
    
    # Z-score normalization
    mean = np.mean(maps)
    std  = np.std(maps)
    maps = (maps - mean) / std
    if verbose:
        print(f'  Normalized range: [{maps.min():.3f}, {maps.max():.3f}]')
        print(f'  Normalization: mean={mean:.4f}, std={std:.4f}')
    
    # Load params
    params_sims = np.loadtxt(f_params)  # [N_sims, 6]
    total_sims  = params_sims.shape[0]
    total_maps  = total_sims * SPLITS
    
    # Expand: each sim -> SPLITS maps
    params_maps = np.zeros((total_maps, 6), dtype=np.float32)
    for i in range(total_sims):
        for j in range(SPLITS):
            params_maps[i*SPLITS + j] = params_sims[i]
    
    # Normalize params to [0,1] range
    params_maps = (params_maps - PARAM_MIN) / (PARAM_MAX - PARAM_MIN)
    
    if verbose:
        print(f'  Total sims: {total_sims}, total maps: {total_maps}')
    
    return maps.astype(np.float32), params_maps, total_sims


def build_split_indices(total_sims, seed=SEED):
    """Build train/val/test sim indices with shuffling."""
    np.random.seed(seed)
    sim_numbers = np.arange(total_sims)
    np.random.shuffle(sim_numbers)
    
    n_train = int(0.80 * total_sims)  # 800 sims
    n_valid = int(0.10 * total_sims)  # 100 sims
    # n_test  = rest                  # 100 sims
    
    train_idx = sim_numbers[:n_train]
    valid_idx = sim_numbers[n_train:n_train+n_valid]
    test_idx  = sim_numbers[n_train+n_valid:]
    
    return train_idx, valid_idx, test_idx


def moment_loss(pred, target):
    """
    Moment network loss from paper:
    L = log(MSE_mean) + log(MSE_variance)
    
    pred: [batch, 2*num_params] — first half=mean, second half=log_var
    target: [batch, num_params]
    """
    num_params = target.shape[1]
    y_pred = pred[:, :num_params]         # posterior mean
    e_pred = pred[:, num_params:]         # log uncertainty (actually variance prediction)
    
    # Per-parameter MSE
    mse1 = torch.mean((y_pred - target)**2, dim=0)
    mse2 = torch.mean(((y_pred - target)**2 - e_pred**2)**2, dim=0)
    
    # Sum of log losses
    loss = torch.mean(torch.log(mse1) + torch.log(mse2))
    return loss, mse1, mse2


def sanity_check_plots(maps_raw_path):
    """Save some sanity check plots of the maps."""
    print('Making sanity check plots...')
    maps = np.load(maps_raw_path, mmap_mode='r')
    
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    for i, ax in enumerate(axes.flat):
        img = np.log10(maps[i*125])  # sample every 125 maps
        im = ax.imshow(img, cmap='viridis', origin='lower')
        ax.set_title(f'Map {i*125}')
        plt.colorbar(im, ax=ax)
    plt.suptitle('CAMELS Mgas Maps (log10 scale)')
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, 'sanity', 'mgas_sample_maps.png'), dpi=100)
    plt.close()
    print('  Saved sanity/mgas_sample_maps.png')


# ============================================================
# TRAINING LOOP
# ============================================================
def train(model, loader, optimizer, scheduler, device, epoch):
    model.train()
    total_loss = 0
    n_points = 0
    
    for x, y in loader:
        x = x.to(device)
        y = y.to(device)
        
        pred = model(x)
        loss, _, _ = moment_loss(pred, y)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if scheduler is not None:
            scheduler.step()
        
        total_loss += loss.item() * x.shape[0]
        n_points   += x.shape[0]
    
    return total_loss / n_points


@torch.no_grad()
def evaluate(model, loader, device):
    model.eval()
    total_loss = 0
    n_points   = 0
    all_pred   = []
    all_true   = []
    
    for x, y in loader:
        x = x.to(device)
        y = y.to(device)
        
        pred = model(x)
        loss, _, _ = moment_loss(pred, y)
        
        total_loss += loss.item() * x.shape[0]
        n_points   += x.shape[0]
        
        num_params = y.shape[1]
        all_pred.append(pred[:, :num_params].cpu().numpy())
        all_true.append(y.cpu().numpy())
    
    all_pred = np.concatenate(all_pred, axis=0)
    all_true = np.concatenate(all_true, axis=0)
    
    return total_loss / n_points, all_pred, all_true


def compute_metrics(pred_norm, true_norm):
    """
    Denormalize and compute relative errors.
    Params order: [Omega_m, sigma_8]
    Normalization: (x - min) / (max - min)
    """
    param_min = PARAM_MIN[PARAMS_IDX]   # [0.1, 0.6]
    param_max = PARAM_MAX[PARAMS_IDX]   # [0.5, 1.0]
    
    pred = pred_norm * (param_max - param_min) + param_min
    true = true_norm * (param_max - param_min) + param_min
    
    rel_err = np.mean(np.abs(pred - true) / np.abs(true), axis=0)
    
    # R^2 scores
    ss_res = np.sum((pred - true)**2, axis=0)
    ss_tot = np.sum((true - np.mean(true, axis=0))**2, axis=0)
    r2 = 1 - ss_res / ss_tot
    
    return rel_err, r2, pred, true


def scatter_plot(pred, true, param_names, epoch, tag=''):
    """Make scatter plot comparing predicted vs true parameter values."""
    fig, axes = plt.subplots(1, len(param_names), figsize=(6*len(param_names), 6))
    if len(param_names) == 1:
        axes = [axes]
    
    for i, (ax, name) in enumerate(zip(axes, param_names)):
        ax.scatter(true[:, i], pred[:, i], alpha=0.3, s=5, c='steelblue')
        mn = min(true[:, i].min(), pred[:, i].min())
        mx = max(true[:, i].max(), pred[:, i].max())
        ax.plot([mn, mx], [mn, mx], 'r--', lw=1.5, label='1:1 line')
        
        rel_err = np.mean(np.abs(pred[:, i] - true[:, i]) / np.abs(true[:, i]))
        r2 = 1 - np.sum((pred[:, i] - true[:, i])**2) / np.sum((true[:, i] - np.mean(true[:, i]))**2)
        
        ax.set_xlabel(f'True {name}', fontsize=12)
        ax.set_ylabel(f'Predicted {name}', fontsize=12)
        ax.set_title(f'{name}: rel_err={rel_err:.3f}, R²={r2:.4f}')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.suptitle(f'CAMELS Mgas CNN - Epoch {epoch} {tag}')
    plt.tight_layout()
    fname = os.path.join(OUT_DIR, f'scatter_{tag}_epoch{epoch:03d}.png')
    plt.savefig(fname, dpi=120)
    plt.close()
    return fname


def plot_training_curves(train_losses, valid_losses, save_path):
    plt.figure(figsize=(10, 5))
    plt.plot(train_losses, label='Train loss', color='steelblue')
    plt.plot(valid_losses, label='Valid loss', color='orange')
    plt.xlabel('Epoch')
    plt.ylabel('Moment network loss')
    plt.title('CAMELS Mgas CNN Training Curves')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=120)
    plt.close()


# ============================================================
# MAIN
# ============================================================
def main():
    start_time = time.time()
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'Using device: {device}')
    if torch.cuda.is_available():
        print(f'GPU: {torch.cuda.get_device_name(0)}')
    cudnn.benchmark = True
    
    # ---- Phase 1: Load and prepare data ----
    print('\n=== Loading Data ===')
    maps, params_all, total_sims = load_and_normalize_maps(F_MAPS, F_PARAMS, verbose=True)
    
    # Sanity plots
    sanity_check_plots(F_MAPS)
    
    # ---- Build splits ----
    print('\n=== Building Splits ===')
    train_idx, valid_idx, test_idx = build_split_indices(total_sims, seed=SEED)
    print(f'Train: {len(train_idx)} sims, Valid: {len(valid_idx)} sims, Test: {len(test_idx)} sims')
    
    train_ds = CAMELSDataset('train', maps, params_all, train_idx, augment=True,  verbose=True)
    valid_ds = CAMELSDataset('valid', maps, params_all, valid_idx, augment=False, verbose=True)
    test_ds  = CAMELSDataset('test',  maps, params_all, test_idx,  augment=False, verbose=True)
    
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True,
                              num_workers=NUM_WORKERS, pin_memory=True)
    valid_loader = DataLoader(valid_ds, batch_size=BATCH_SIZE, shuffle=False,
                              num_workers=NUM_WORKERS, pin_memory=True)
    test_loader  = DataLoader(test_ds,  batch_size=BATCH_SIZE, shuffle=False,
                              num_workers=NUM_WORKERS, pin_memory=True)
    
    print(f'Train batches: {len(train_loader)}, Valid: {len(valid_loader)}, Test: {len(test_loader)}')
    
    # ---- Build model ----
    print('\n=== Building Model ===')
    model = model_e3_err(hidden=HIDDEN, dr=DR, channels=1, num_params=len(PARAMS_IDX))
    model = model.to(device)
    
    n_params = sum(p.numel() for p in model.parameters())
    print(f'Model parameters: {n_params:,}')
    
    # ---- Optimizer ----
    optimizer = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=WD,
                                  betas=(0.5, 0.999))
    # Cosine annealing
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=EPOCHS, eta_min=1e-7)
    
    # ---- Training ----
    print('\n=== Training ===')
    
    best_valid_loss = float('inf')
    train_losses    = []
    valid_losses    = []
    best_model_path = os.path.join(OUT_DIR, 'best_model_mgas.pt')
    
    loss_log_path = os.path.join(OUT_DIR, 'training_loss.txt')
    with open(loss_log_path, 'w') as f:
        f.write('epoch\ttrain_loss\tvalid_loss\n')
    
    for epoch in range(EPOCHS):
        t0 = time.time()
        
        train_loss = train(model, train_loader, optimizer, scheduler, device, epoch)
        valid_loss, valid_pred, valid_true = evaluate(model, valid_loader, device)
        
        train_losses.append(train_loss)
        valid_losses.append(valid_loss)
        
        dt = time.time() - t0
        improved = ''
        if valid_loss < best_valid_loss:
            best_valid_loss = valid_loss
            torch.save(model.state_dict(), best_model_path)
            improved = ' *** BEST ***'
        
        print(f'Epoch {epoch:3d}/{EPOCHS}: train={train_loss:.4f} valid={valid_loss:.4f} lr={scheduler.get_last_lr()[0]:.2e} t={dt:.1f}s{improved}')
        
        with open(loss_log_path, 'a') as f:
            f.write(f'{epoch}\t{train_loss:.6f}\t{valid_loss:.6f}\n')
        
        # Plot every 10 epochs
        if (epoch + 1) % 10 == 0:
            rel_err, r2, pred_phys, true_phys = compute_metrics(valid_pred, valid_true)
            print(f'  Valid metrics: Omega_m rel_err={rel_err[0]:.4f} R²={r2[0]:.4f} | sigma_8 rel_err={rel_err[1]:.4f} R²={r2[1]:.4f}')
            scatter_plot(pred_phys, true_phys, ['Omega_m', 'sigma_8'], epoch+1, tag='valid')
    
    # ---- Final Evaluation on Test Set ----
    print('\n=== Final Test Evaluation ===')
    model.load_state_dict(torch.load(best_model_path))
    model.eval()
    
    test_loss, test_pred, test_true = evaluate(model, test_loader, device)
    rel_err, r2, pred_phys, true_phys = compute_metrics(test_pred, test_true)
    
    print(f'\n=== TEST RESULTS ===')
    print(f'Test loss: {test_loss:.4f}')
    print(f'Omega_m: relative error = {rel_err[0]*100:.2f}%, R² = {r2[0]:.4f}')
    print(f'sigma_8: relative error = {rel_err[1]*100:.2f}%, R² = {r2[1]:.4f}')
    
    # Paper reported (Table 2, Mgas, IllustrisTNG): ~3-5% for Omega_m, ~4-6% for sigma_8
    
    # ---- Save plots ----
    scatter_plot(pred_phys, true_phys, ['Omega_m', 'sigma_8'], EPOCHS, tag='test_final')
    plot_training_curves(train_losses, valid_losses, os.path.join(OUT_DIR, 'training_curves.png'))
    
    # ---- Timing ----
    wall_hours = (time.time() - start_time) / 3600.0
    
    # ---- Save results JSON ----
    results = {
        'model': 'model_e3_err',
        'field': 'Mgas',
        'sim_suite': 'IllustrisTNG_LH',
        'n_sims_train': int(len(train_idx)),
        'n_sims_valid': int(len(valid_idx)),
        'n_sims_test':  int(len(test_idx)),
        'n_maps_train': len(train_ds),
        'n_maps_valid': len(valid_ds),
        'n_maps_test':  len(test_ds),
        'test_loss': float(test_loss),
        'Omega_m_rel_err': float(rel_err[0]),
        'Omega_m_r2':      float(r2[0]),
        'sigma_8_rel_err': float(rel_err[1]),
        'sigma_8_r2':      float(r2[1]),
        'wall_hours': wall_hours,
        'epochs': EPOCHS,
        'batch_size': BATCH_SIZE,
        'lr': LR,
        'hidden': HIDDEN,
        'dr': DR,
    }
    
    results_path = os.path.join(OUT_DIR, 'test_results.json')
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f'\nResults saved to {results_path}')
    print(f'Total wall time: {wall_hours:.2f} hours')
    
    return results


if __name__ == '__main__':
    results = main()
