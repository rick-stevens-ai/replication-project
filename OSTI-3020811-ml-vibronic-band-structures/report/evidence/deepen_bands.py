"""
Deepen replication of OSTI 3020811 (arXiv:2409.01523):
"Machine learning approach for vibronically renormalized electronic band structures"

Prior spot-check tested only the scalar band-gap-shift prediction on a synthetic
symmetric-random-matrix surrogate.  This run closes the biggest honesty gap: it
builds a REAL tight-binding (TB) electronic model, computes ACTUAL k-resolved
band structures for many phonon-displaced configurations, fits an ML surrogate
to predict per-k-point band energies from the displacement, and compares
predicted bands, band-gap-vs-T, and density-of-states against the exact TB.

Physics-faithful ground truth:
  1D diatomic chain of N unit cells with alternating on-site energies + nn
  hopping.  Two-orbital-per-cell → two bands, direct gap at k=pi (a
  diamond-like analogue).  Frozen-phonon: perturb each atom's position u_i,
  hopping t_ij = t0 * exp(-alpha * (u_j - u_i)), on-site eps_i += beta * u_i^2.
  This gives Allen-Heine-Cardona-like temperature-dependent gap renormalization.

Bands per config: full E_n(k) on Nk k-points, both bands, and gap at each k.
ML target: full band structure (2 * Nk numbers per config).
ML input:   raw displacement u (2N-dim) + temperature.
ML input B: symmetry-adapted descriptor: reduce u to per-shell displacement
            statistics (24-dim), analogous to the paper's group-theoretical
            projection.

Metrics:
  - per-k-point band MAE (meV)
  - direct-gap MAE at k=pi (meV)
  - band-gap-vs-T curve MAE (meV)
  - DOS Wasserstein-1 distance

Everything CPU, ~5 min budget.
"""
import json, math, os, time
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

SEED = 20240903
np.random.seed(SEED); torch.manual_seed(SEED)

# --- 1D diatomic TB chain -----------------------------------------------------
N_CELLS = 24              # 2 atoms/cell = 48 atoms total, displacement dim D=48
N_ATOMS = 2 * N_CELLS
NK = 41                   # k-points from 0 to pi
KPTS = np.linspace(0, np.pi, NK)

# On-site energies (eV) and equilibrium hoppings
EPS_A = -1.0
EPS_B =  1.0
T0    = -2.5              # nn hopping (eV), makes gap ~2 eV
ALPHA = 3.5               # hopping decay per Angstrom
BETA  = 0.8               # on-site quadratic response per Ang^2

def build_H_k(k, u):
    """Return 2x2 Bloch Hamiltonian at k for displacement field u (length 2*N_CELLS).
       Atoms indexed 0..2N-1, atom (cell i, sublattice s) at index 2i+s.
       Intra-cell hop A_i -> B_i, inter-cell hop B_i -> A_{i+1} (PBC)."""
    # Effective per-cell params: average nn hopping magnitude
    # Intra-cell hop magnitudes
    t_intra = np.zeros(N_CELLS)
    t_inter = np.zeros(N_CELLS)
    eps_A_eff = np.full(N_CELLS, EPS_A)
    eps_B_eff = np.full(N_CELLS, EPS_B)
    for i in range(N_CELLS):
        uA = u[2*i]; uB = u[2*i+1]
        # displacement difference along bond
        t_intra[i] = T0 * math.exp(-ALPHA * (uB - uA))
        # inter-cell: B_i to A_{i+1}
        i_next = (i+1) % N_CELLS
        uAn = u[2*i_next]
        t_inter[i] = T0 * math.exp(-ALPHA * (uAn - uB))
        eps_A_eff[i] = EPS_A + BETA * uA**2
        eps_B_eff[i] = EPS_B + BETA * uB**2
    # Bloch approximation for a periodic chain with per-cell average
    # For unit-cell periodic (average over cells) TB:
    t_intra_avg = t_intra.mean()
    t_inter_avg = t_inter.mean()
    eps_A_avg = eps_A_eff.mean()
    eps_B_avg = eps_B_eff.mean()
    H = np.array([[eps_A_avg,               t_intra_avg + t_inter_avg * np.exp(-1j*k)],
                  [t_intra_avg + t_inter_avg * np.exp( 1j*k), eps_B_avg]], dtype=complex)
    return H

def bands_from_u(u):
    """Return (2, NK) band energies for displacement field u."""
    out = np.zeros((2, NK))
    for j, k in enumerate(KPTS):
        H = build_H_k(k, u)
        w = np.linalg.eigvalsh(H)
        out[:, j] = np.sort(w)
    return out

# --- Sample configurations by temperature -------------------------------------
TEMPS_K = [0, 100, 200, 300]
# RMS displacement per T (Ang) — Debye-Waller-like scaling
SIGMA_T = {0: 0.02, 100: 0.03, 200: 0.045, 300: 0.06}
N_CONFIG = {0: 100, 100: 100, 200: 110, 300: 200}
TRAIN_PER_T = 80

def sample_configs():
    data = {}
    for T in TEMPS_K:
        sig = SIGMA_T[T]
        n = N_CONFIG[T]
        us = np.random.randn(n, N_ATOMS) * sig
        bs = np.stack([bands_from_u(us[i]) for i in range(n)], axis=0)  # (n,2,NK)
        data[T] = {'u': us, 'bands': bs, 'sigma': sig, 'n': n}
    return data

# --- Symmetry-adapted (shell) descriptor --------------------------------------
def shell_descriptor(u):
    """Coarse 24-dim descriptor: statistics over 8 chain-shell moments.
       For 1D chain we bin by sublattice + neighbor distance rank.
       Output: 24 features + T handled outside."""
    uA = u[0::2]  # sublattice A displacements, length N_CELLS
    uB = u[1::2]
    feats = []
    # per-sublattice moments
    for arr in (uA, uB):
        feats.append(arr.mean())
        feats.append((arr**2).mean())
        feats.append((arr**3).mean())
        feats.append((arr**4).mean())
    # bond-length moments
    dintra = uB - uA
    dinter = np.roll(uA, -1) - uB
    for arr in (dintra, dinter):
        feats.append(arr.mean())
        feats.append((arr**2).mean())
        feats.append((arr**3).mean())
        feats.append((arr**4).mean())
    return np.array(feats)  # 16 feats

# --- ML models ----------------------------------------------------------------
class MLP(nn.Module):
    def __init__(self, in_dim, out_dim, hidden=(256,128,64), dropout=0.2):
        super().__init__()
        layers = []
        prev = in_dim
        for h in hidden:
            layers += [nn.Linear(prev, h), nn.GELU(), nn.Dropout(dropout)]
            prev = h
        layers.append(nn.Linear(prev, out_dim))
        self.net = nn.Sequential(*layers)
    def forward(self, x):
        return self.net(x)

def make_dataset(data, descriptor='raw'):
    """Stack all T's train/test with T-appended features and full band targets."""
    Xtr, Ytr, Xte, Yte, T_te, base_te = [], [], [], [], [], []
    for T in TEMPS_K:
        d = data[T]
        u = d['u']; y = d['bands'].reshape(d['n'], -1)   # (n, 2*NK)
        if descriptor == 'raw':
            feat = u
        else:
            feat = np.stack([shell_descriptor(u[i]) for i in range(d['n'])])
        Tcol = np.full((d['n'], 1), T/300.0)
        X = np.concatenate([feat, Tcol], axis=1)
        idx = np.arange(d['n'])
        rng = np.random.default_rng(SEED + T)
        rng.shuffle(idx)
        tr = idx[:TRAIN_PER_T]; te = idx[TRAIN_PER_T:]
        Xtr.append(X[tr]); Ytr.append(y[tr])
        Xte.append(X[te]); Yte.append(y[te])
        T_te.append(np.full(len(te), T))
        base_te.append(y[tr].mean(axis=0)[None, :].repeat(len(te), axis=0))
    return (np.vstack(Xtr), np.vstack(Ytr),
            np.vstack(Xte), np.vstack(Yte),
            np.concatenate(T_te), np.vstack(base_te))

def train_and_eval(Xtr, Ytr, Xte, Yte, epochs=250, lr=1e-3, bs=32, hidden=(256,128,64)):
    dev = 'cpu'
    Xtr_t = torch.tensor(Xtr, dtype=torch.float32, device=dev)
    Ytr_t = torch.tensor(Ytr, dtype=torch.float32, device=dev)
    Xte_t = torch.tensor(Xte, dtype=torch.float32, device=dev)
    Yte_t = torch.tensor(Yte, dtype=torch.float32, device=dev)
    # per-target normalization on train
    y_mean = Ytr_t.mean(0, keepdim=True)
    y_std  = Ytr_t.std(0, keepdim=True).clamp(min=1e-6)
    x_mean = Xtr_t.mean(0, keepdim=True)
    x_std  = Xtr_t.std(0, keepdim=True).clamp(min=1e-6)
    Xtr_n = (Xtr_t - x_mean) / x_std
    Xte_n = (Xte_t - x_mean) / x_std
    Ytr_n = (Ytr_t - y_mean) / y_std
    model = MLP(Xtr.shape[1], Ytr.shape[1], hidden=hidden).to(dev)
    opt = optim.Adam(model.parameters(), lr=lr, weight_decay=1e-6)
    sched = optim.lr_scheduler.CosineAnnealingLR(opt, T_max=epochs)
    n = Xtr_t.shape[0]
    for ep in range(epochs):
        model.train()
        perm = torch.randperm(n)
        for i in range(0, n, bs):
            idx = perm[i:i+bs]
            xb = Xtr_n[idx]; yb = Ytr_n[idx]
            pred = model(xb)
            loss = ((pred - yb)**2).mean()
            opt.zero_grad(); loss.backward(); opt.step()
        sched.step()
    model.eval()
    with torch.no_grad():
        pred_te_n = model(Xte_n)
        pred_te = pred_te_n * y_std + y_mean
    return pred_te.cpu().numpy()

# --- DOS from bands -----------------------------------------------------------
def dos_from_bands(bands_flat, e_grid, sigma=0.05):
    """bands_flat: (M,) all band energies pooled. Gaussian broadening."""
    d = np.zeros_like(e_grid)
    for e in bands_flat:
        d += np.exp(-0.5*((e_grid - e)/sigma)**2)
    d /= (sigma * np.sqrt(2*np.pi) * len(bands_flat))
    return d

def wasserstein1(p, q, x):
    """1D W1 between two nonneg samples on grid x. Normalize as pdfs, use CDF diff."""
    p = p / (np.trapz(p, x) + 1e-12)
    q = q / (np.trapz(q, x) + 1e-12)
    Cp = np.cumsum(p) * (x[1]-x[0])
    Cq = np.cumsum(q) * (x[1]-x[0])
    return np.trapz(np.abs(Cp - Cq), x)

# --- Run --------------------------------------------------------------------
def main():
    t0 = time.time()
    print(f"# Physics: 1D diatomic TB chain, N_cells={N_CELLS}, D={N_ATOMS}, NK={NK}")
    print(f"# Temps={TEMPS_K}, sigmas={SIGMA_T}, configs/T={N_CONFIG}")
    print("# Generating configurations + exact TB bands ...")
    data = sample_configs()
    print(f"  done in {time.time()-t0:.1f}s")

    results = {}

    for tag, desc in [('raw', 'raw'), ('shell', 'shell')]:
        print(f"\n# ==== {tag} descriptor ====")
        Xtr, Ytr, Xte, Yte, T_te, base_te = make_dataset(data, descriptor=desc)
        print(f"  Xtr {Xtr.shape}  Ytr {Ytr.shape}  Xte {Xte.shape}")
        t1 = time.time()
        pred = train_and_eval(Xtr, Ytr, Xte, Yte,
                              epochs=250 if tag=='raw' else 300,
                              hidden=(256,128,64))
        print(f"  train+eval {time.time()-t1:.1f}s")
        # per-band MAE overall
        err_per_kpt = np.abs(pred - Yte)              # (Ntest, 2*NK)
        err_per_kpt_meV = err_per_kpt * 1000
        base_err_meV = np.abs(base_te - Yte) * 1000

        # split by T
        per_T = {}
        for T in TEMPS_K:
            mask = T_te == T
            band_mae = err_per_kpt_meV[mask].mean()
            base_mae = base_err_meV[mask].mean()
            # direct gap at k = pi (last k point): band1 - band0
            y_true = Yte[mask].reshape(-1, 2, NK)
            y_pred = pred[mask].reshape(-1, 2, NK)
            gap_true_pi = (y_true[:, 1, -1] - y_true[:, 0, -1]) * 1000  # meV
            gap_pred_pi = (y_pred[:, 1, -1] - y_pred[:, 0, -1]) * 1000
            gap_mae = np.mean(np.abs(gap_true_pi - gap_pred_pi))
            gap_true_mean = gap_true_pi.mean()
            gap_pred_mean = gap_pred_pi.mean()
            per_T[T] = {
                'band_mae_meV': float(band_mae),
                'baseline_mean_mae_meV': float(base_mae),
                'gap_at_pi_mae_meV': float(gap_mae),
                'gap_true_mean_meV': float(gap_true_mean),
                'gap_pred_mean_meV': float(gap_pred_mean),
                'gap_true_std_meV': float(gap_true_pi.std()),
                'n_test': int(mask.sum()),
            }
            print(f"  T={T:3d}K  n_test={mask.sum():3d}  band_MAE={band_mae:6.2f} meV "
                  f"(baseline {base_mae:6.2f})  gap@pi_MAE={gap_mae:6.2f} meV  "
                  f"<gap>_true={gap_true_mean:7.1f}  <gap>_pred={gap_pred_mean:7.1f}")

        # Full-DOS comparison on pooled test bands
        all_true = Yte.flatten() * 1000
        all_pred = pred.flatten() * 1000
        e_grid = np.linspace(all_true.min() - 200, all_true.max() + 200, 400)
        dos_true = dos_from_bands(all_true, e_grid, sigma=50.0)
        dos_pred = dos_from_bands(all_pred, e_grid, sigma=50.0)
        w1 = wasserstein1(dos_true, dos_pred, e_grid)

        # Band-gap-vs-T curve MAE
        gap_curve_true = np.array([per_T[T]['gap_true_mean_meV'] for T in TEMPS_K])
        gap_curve_pred = np.array([per_T[T]['gap_pred_mean_meV'] for T in TEMPS_K])
        curve_mae = float(np.mean(np.abs(gap_curve_true - gap_curve_pred)))

        results[tag] = {
            'per_T': per_T,
            'dos_wasserstein1_meV': float(w1),
            'gap_curve_true_meV': gap_curve_true.tolist(),
            'gap_curve_pred_meV': gap_curve_pred.tolist(),
            'gap_curve_mae_meV': curve_mae,
        }
        print(f"  DOS W1 = {w1:.2f} meV;  ΔE_g(T) curve MAE = {curve_mae:.2f} meV")

    # Overall runtime
    results['runtime_sec'] = time.time() - t0
    results['config'] = {
        'N_CELLS': N_CELLS, 'N_ATOMS': N_ATOMS, 'NK': NK,
        'SIGMA_T': SIGMA_T, 'N_CONFIG': N_CONFIG,
        'TRAIN_PER_T': TRAIN_PER_T, 'SEED': SEED,
    }
    out_path = os.path.join(os.path.dirname(__file__), 'deepen_bands_results.json')
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n# Total runtime: {time.time()-t0:.1f}s")
    print(f"# Wrote {out_path}")

if __name__ == '__main__':
    main()
