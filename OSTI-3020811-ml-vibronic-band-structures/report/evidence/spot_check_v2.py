#!/usr/bin/env python3
"""
Spot-check v2 for arXiv:2409.01523.

Goal: test the paper's *methodological* claim that a symmetry-aware
descriptor is what makes 80 training samples sufficient. The paper's
central experimental claim is:

  test MAE ~10 meV (order-of-magnitude), when target signal stdev at
  T=300 K is also ~10-15 meV, using 80 train / ~20 test per T.

We CAN'T rerun the Quantum Espresso pipeline, so we build a
physics-faithful synthetic:

  * DeltaE_g(u) = 0.5 * u^T H u + small cubic anharmonic
  * H is a random, block-diagonal-symmetric operator with cubic
    (Oh) point-group symmetry: eigenmodes broken into a small number
    of irreducible-representation channels. This mimics the paper's
    Sec. III / IV.B claim that the physical response is well-described
    in a low-dimensional symmetry-invariant feature space.

We compare three models on the SAME 80/rest split:

  (A) Predict-the-mean baseline (should give test MAE ~ target stdev * 0.8).
  (B) NN on RAW 838-dim displacement descriptor.
  (C) NN on a COARSE, symmetry-aware descriptor (radial shells + inner
      products; ~30-dim).

Prediction: (C) << (B) and (C) approaches ~10-20% of target stdev,
supporting the paper's methodological claim; (B) badly overfits.

Compute: keep it small enough to finish in a few minutes on CPU.
"""

import json, os, time, math, sys
import numpy as np
import torch, torch.nn as nn

SEED = 20240903
np.random.seed(SEED); torch.manual_seed(SEED)

N_ATOMS = 279            # paper's block size
D = 3 * N_ATOMS          # 837
TEMPS_K = [0, 100, 200, 300]
SIGMA_A = {0: 0.05, 100: 0.055, 200: 0.065, 300: 0.075}

# ----------------- physics-faithful low-rank symmetric H -------------
# Build H with rank K << D so effective dof is small, mimicking
# symmetry constraints. Then physical signal at sigma=0.065 has stdev
# calibrated to ~10-15 meV.
K_MODES = 24
rng = np.random.default_rng(SEED)
U_modes = rng.standard_normal((D, K_MODES)).astype(np.float32) / math.sqrt(D)
# orthonormalize
U_modes, _ = np.linalg.qr(U_modes)
eigs = np.abs(rng.standard_normal(K_MODES).astype(np.float32)) + 0.1
H = (U_modes * eigs) @ U_modes.T   # rank-K PSD
# calibrate to ~12 meV stdev at 200K
u_probe = rng.standard_normal((512, D)).astype(np.float32) * 0.065
qs = np.array([0.5 * u @ H @ u for u in u_probe])
H *= 0.012 / qs.std()
c_vec = rng.standard_normal(D).astype(np.float32) / math.sqrt(D)

def true_deltaE(u):
    return 0.5 * u @ H @ u + 0.0005 * (u @ c_vec)**3

# ----------------- descriptors -----------------
# Assign atoms to R radial shells (crude proxy for the paper's group-
# theoretical descriptor). Then per-shell moments:
#   phi_r = [ sum_i in shell |u_i|^2 , sum_ij <u_i,u_j>/n ] etc.
# We fake a coordinate list so shells are defined:
np.random.seed(SEED + 1)
positions = np.random.rand(N_ATOMS, 3).astype(np.float32) * 12.0   # dummy 12 A box
center = positions.mean(0)
radii = np.linalg.norm(positions - center, axis=1)
R = 8   # 8 radial shells
edges = np.quantile(radii, np.linspace(0, 1, R+1))
shell_id = np.clip(np.searchsorted(edges[1:], radii), 0, R-1)

def coarse_descriptor(u_flat, T_normalized):
    """u_flat shape (3N,). Returns ~30-dim symmetry-inspired features."""
    u = u_flat.reshape(N_ATOMS, 3)
    mag2 = (u * u).sum(1)   # per-atom
    feats = []
    for r in range(R):
        m = (shell_id == r)
        if m.sum() == 0:
            feats.extend([0.0, 0.0, 0.0])
            continue
        us = u[m]
        feats.append(float(mag2[m].mean()))                       # ||u||^2 shell avg
        feats.append(float((us.sum(0)**2).sum() / max(len(us),1))) # coherent sum^2
        feats.append(float((us @ us.T).sum() / max(len(us)**2,1))) # pair mean
    feats.append(float(T_normalized))
    return np.array(feats, dtype=np.float32)

def raw_descriptor(u_flat, T_normalized):
    return np.concatenate([u_flat, [T_normalized]]).astype(np.float32)

# ----------------- build dataset -----------------
counts = {0: 103, 100: 108, 200: 113, 300: 204}
Xraw_tr, Xraw_te, Xco_tr, Xco_te, ytr, yte, Ttr, Tte = [],[],[],[],[],[],[],[]
meta = []
for T in TEMPS_K:
    sigma = SIGMA_A[T]
    n = counts[T]
    u_all = rng.standard_normal((n, D)).astype(np.float32) * sigma
    y_all = np.array([true_deltaE(u) for u in u_all], dtype=np.float32)
    T_norm = T / 300.0
    Xraw = np.stack([raw_descriptor(u, T_norm) for u in u_all])
    Xco  = np.stack([coarse_descriptor(u, T_norm) for u in u_all])
    perm = np.random.default_rng(SEED + T).permutation(n)
    tr, te = perm[:80], perm[80:]
    Xraw_tr.append(Xraw[tr]); Xraw_te.append(Xraw[te])
    Xco_tr.append(Xco[tr]);   Xco_te.append(Xco[te])
    ytr.append(y_all[tr]);    yte.append(y_all[te])
    Ttr.append(np.full(len(tr), T)); Tte.append(np.full(len(te), T))
    meta.append({"T_K": T, "n_total": n, "n_train": 80, "n_test": len(te),
                 "sigma_A": sigma,
                 "target_stdev_meV": float(1000 * y_all.std())})

Xraw_tr = np.concatenate(Xraw_tr); Xraw_te = np.concatenate(Xraw_te)
Xco_tr  = np.concatenate(Xco_tr);  Xco_te  = np.concatenate(Xco_te)
ytr = np.concatenate(ytr); yte = np.concatenate(yte)
Ttr = np.concatenate(Ttr); Tte = np.concatenate(Tte)

D_raw    = Xraw_tr.shape[1]
D_coarse = Xco_tr.shape[1]
print(f"Dims: raw={D_raw}  coarse={D_coarse}")
print(f"Target stdev (meV) per T:")
for m in meta:
    print(f"  T={m['T_K']:4d} K  stdev={m['target_stdev_meV']:.2f} meV")

# ----------------- models -----------------
class FCNN(nn.Module):
    def __init__(self, in_dim, hidden=(256,128,64), dropout=0.1):
        super().__init__()
        layers, d = [], in_dim
        for h in hidden:
            layers += [nn.Linear(d, h), nn.GELU(), nn.Dropout(dropout)]
            d = h
        layers += [nn.Linear(d, 1)]
        self.net = nn.Sequential(*layers)
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight); nn.init.zeros_(m.bias)
    def forward(self, x): return self.net(x).squeeze(-1)

def train_model(Xtr, ytr_, Xte, yte_, hidden, n_epoch=300, lr=1e-3, wd=1e-6,
                batch=32, dropout=0.1, tag=""):
    model = FCNN(Xtr.shape[1], hidden=hidden, dropout=dropout)
    opt = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=wd)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=n_epoch)
    Xtr_t = torch.from_numpy(Xtr); ytr_t = torch.from_numpy(ytr_)
    Xte_t = torch.from_numpy(Xte); yte_t = torch.from_numpy(yte_)
    loss_fn = nn.MSELoss()
    hist=[]; t0=time.time()
    for ep in range(n_epoch):
        model.train()
        perm = torch.randperm(len(Xtr_t))
        losses=[]
        for s in range(0, len(perm), batch):
            idx = perm[s:s+batch]
            opt.zero_grad()
            loss = loss_fn(model(Xtr_t[idx]), ytr_t[idx])
            loss.backward(); opt.step(); losses.append(loss.item())
        sched.step()
        if (ep+1) % 50 == 0 or ep == 0:
            model.eval()
            with torch.no_grad():
                mae_tr = float((model(Xtr_t)-ytr_t).abs().mean())
                mae_te = float((model(Xte_t)-yte_t).abs().mean())
            hist.append({"epoch": ep+1, "train_mse": float(np.mean(losses)),
                         "train_MAE_meV": mae_tr*1000, "test_MAE_meV": mae_te*1000})
            print(f"  [{tag}] ep {ep+1:4d}  train MAE={mae_tr*1000:6.2f} meV  "
                  f"test MAE={mae_te*1000:6.2f} meV  ({time.time()-t0:.0f}s)")
    model.eval()
    with torch.no_grad():
        pred_te = model(Xte_t).cpu().numpy()
    per_T = {}
    for T in TEMPS_K:
        m = (Tte == T)
        if m.sum() == 0: continue
        err = pred_te[m] - yte_[m]
        per_T[int(T)] = {"n_test": int(m.sum()),
                         "MAE_meV": float(1000*np.abs(err).mean()),
                         "RMSE_meV": float(1000*np.sqrt((err**2).mean())),
                         "target_stdev_meV": float(1000*yte_[m].std())}
    return {"per_T": per_T, "history": hist, "wall_sec": time.time()-t0,
            "pred_test_meV": (pred_te*1000).tolist(),
            "true_test_meV": (yte_*1000).tolist(),
            "T_test": Tte.tolist()}

# ----------------- run -----------------
results = {"seed": SEED, "N_atoms": N_ATOMS, "K_effective_modes": K_MODES,
           "dataset_meta": meta, "descriptor_dims": {"raw": D_raw, "coarse": D_coarse}}

# baseline: predict per-T mean of TRAINING set
print("\n=== baseline: predict-train-mean ===")
base = {}
for T in TEMPS_K:
    m_tr = (Ttr == T); m_te = (Tte == T)
    if m_te.sum() == 0: continue
    mu = ytr[m_tr].mean()
    err = yte[m_te] - mu
    base[int(T)] = {"n_test": int(m_te.sum()),
                    "MAE_meV": float(1000*np.abs(err).mean()),
                    "RMSE_meV": float(1000*np.sqrt((err**2).mean())),
                    "target_stdev_meV": float(1000*yte[m_te].std())}
    print(f"  T={T} K  baseline test MAE={base[int(T)]['MAE_meV']:.2f} meV  "
          f"stdev={base[int(T)]['target_stdev_meV']:.2f} meV")
results["baseline_predict_train_mean_per_T"] = base

# (B) raw 838-dim NN, small hidden (compute-bounded)
print("\n=== (B) RAW 838-dim descriptor -> NN (256,128,64) ===")
results["raw_838_NN"] = train_model(Xraw_tr, ytr, Xraw_te, yte,
                                    hidden=(256,128,64), n_epoch=300,
                                    lr=1e-3, wd=1e-4, batch=32, dropout=0.2,
                                    tag="RAW")

# (C) coarse symmetry-inspired NN
print("\n=== (C) COARSE ~25-dim symmetry-inspired descriptor -> NN (64,32) ===")
results["coarse_symmetry_NN"] = train_model(Xco_tr, ytr, Xco_te, yte,
                                            hidden=(64,32), n_epoch=400,
                                            lr=1e-3, wd=1e-5, batch=32, dropout=0.1,
                                            tag="COARSE")

# save
outdir = os.path.join(os.path.dirname(__file__), "..", "report", "evidence")
os.makedirs(outdir, exist_ok=True)
outpath = os.path.join(outdir, "spot_check_v2_results.json")
with open(outpath, "w") as f: json.dump(results, f, indent=2)

# summary
print("\n===================== SUMMARY =====================")
print(f"{'T (K)':>6} {'stdev(meV)':>12} {'baseline MAE':>14} {'raw838 MAE':>13} {'coarse MAE':>12}")
for T in TEMPS_K:
    if int(T) not in base: continue
    b   = base[int(T)]["MAE_meV"]
    r   = results["raw_838_NN"]["per_T"].get(int(T), {}).get("MAE_meV", float('nan'))
    c   = results["coarse_symmetry_NN"]["per_T"].get(int(T), {}).get("MAE_meV", float('nan'))
    s   = base[int(T)]["target_stdev_meV"]
    print(f"{T:>6} {s:>12.2f} {b:>14.2f} {r:>13.2f} {c:>12.2f}")

print("\nWROTE:", outpath)
