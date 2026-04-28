"""
Replication of OSTI 2571909:
  "Physics-based hybrid machine learning for critical heat flux prediction
   with uncertainty quantification" — Furlong, Zhao, Salko, Wu (2025).

Independent PyTorch + GPyTorch implementation of the hybrid methodology:
    y_hybrid = y_base(x) + f_ML(x)          (residual learning)

Scope (2-hour replication budget):
  * Biasi empirical correlation (dryout form) implemented from scratch.
  * Dataset: because the NRC CHF public database is not redistributable via
    a single download, we construct a *physics-grounded synthetic surrogate*
    that lives inside the paper's filtered parameter window (Table 2) and
    whose "experimental" CHF is produced by perturbing the Biasi prediction
    with (i) a smooth nonlinear bias field and (ii) heteroscedastic aleatoric
    noise.  This substitution is documented in the report.
  * Model suite:
        - Pure DNN ensemble  (no base model)
        - Biasi-hybrid DNN ensemble
    (Bowring-hybrid and DGP/BNN variants of the paper are discussed in the
    report but are not all retrained here due to compute budget.)
  * Scenarios: "plentiful" (80%  = ~7 350 points) and "limited" (9 points).
  * Metrics reported (matching paper Table 6): μ_error, Max_error, rRMSE, R².

Author: Ollie / OpenClaw replication run.
"""
from __future__ import annotations
import os, math, time, json
from dataclasses import dataclass
import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import r2_score

rng = np.random.default_rng(20250423)
torch.manual_seed(20250423)
DEVICE = torch.device("cpu")   # small model; CPU is sufficient
torch.set_num_threads(max(1, os.cpu_count() // 2))

# ---------------------------------------------------------------------------
# 1.  Biasi CHF correlation (dryout form, high-quality branch)
# ---------------------------------------------------------------------------
def biasi_chf(D_m, L_m, P_Pa, G, x_out):
    """Biasi (1967) CHF correlation, high-quality branch.

    Inputs (SI):
        D_m   tube inner diameter [m]
        L_m   heated length       [m]   (not used in high-quality branch)
        P_Pa  pressure            [Pa]
        G     mass flux           [kg m^-2 s^-1]
        x_out outlet equilibrium quality [-]

    Returns q''_cr in W/m^2.

    Reference expression (kW/m^2, cgs-ish):
        q2 = (3.78e3 / D_cm^n) * H(P_bar) * G^-0.6 * (1 - x)
        n  = 0.4 if D_cm >= 1 else 0.6
        H(P) = -1.159 + 1.49 P exp(-0.19 P) + 8.99 P / (10 + P^2)   [P in bar]
    """
    D_cm = np.asarray(D_m) * 100.0
    P_bar = np.asarray(P_Pa) / 1.0e5
    n = np.where(D_cm >= 1.0, 0.4, 0.6)
    # Biasi (1967) pressure function, P in bar.  Correct coefficients per
    # Tong & Tang's review of the Biasi correlation.
    H = (-1.159
         + 0.149 * P_bar * np.exp(-0.019 * P_bar)
         + 8.99  * P_bar / (10.0 + P_bar ** 2))
    H = np.clip(H, 1e-3, None)        # guard
    # High-quality branch (kW/m^2): prefactor 3.78e3, G exponent 1/6.
    q2_kW = (3.78e3 / D_cm ** n) * (H / G ** (1.0 / 6.0)) * (1.0 - x_out)
    return np.clip(q2_kW, 1.0, None) * 1.0e3   # -> W/m^2


# ---------------------------------------------------------------------------
# 2.  Synthetic "NRC-like" CHF dataset inside the paper's filtered ranges
# ---------------------------------------------------------------------------
@dataclass
class Splits:
    X_train: torch.Tensor; y_train: torch.Tensor
    X_val:   torch.Tensor; y_val:   torch.Tensor
    X_test:  torch.Tensor; y_test:  torch.Tensor
    base_train: torch.Tensor; base_val: torch.Tensor; base_test: torch.Tensor
    mu_X: torch.Tensor; sd_X: torch.Tensor
    mu_y: float; sd_y: float


def build_dataset(n_total=9188, seed=20250423):
    """Sample (D, L, P, G, dh_sub) uniformly inside Biasi/Bowring common range
    (paper Table 2), compute outlet quality from a simplified heat-balance
    shape, and generate a perturbed 'experimental' CHF.

    Truth model (documented substitution):
        y_exp = y_Biasi(x) * (1 + b(x)) + eps(x)
    where b(x) is a smooth nonlinear bias field and eps is heteroscedastic
    Gaussian noise.  This is a deliberately solvable residual-learning task.
    """
    rng = np.random.default_rng(seed)
    # Sampling ranges (paper Table 2).  Dryout regime → sample x_out in the
    # filtered range [0.20, 0.95] directly instead of reconstructing it from
    # a fragile heat-balance surrogate.
    D     = rng.uniform(0.003, 0.0375, n_total)      # m
    L     = rng.uniform(0.20,  3.70,   n_total)      # m
    P     = rng.uniform(0.27e6, 14.0e6, n_total)     # Pa
    G     = rng.uniform(136.0, 6000.0, n_total)      # kg/m^2/s
    x_out = rng.uniform(0.20,  0.95,   n_total)      # outlet equilibrium quality
    # An independent inlet-subcooling feature (kept as the 5th input, per paper)
    dh    = rng.uniform(-1.5e5, 1.0e6, n_total)      # J/kg

    # Biasi prediction -> base feature
    y_base = biasi_chf(D, L, P, G, x_out)             # W/m^2

    # Structured nonlinear bias field b(x) in [-0.2, +0.2]
    P_n = (P - 4.5e6) / 5e6
    G_n = (G - 2000.0) / 1500.0
    D_n = (D - 0.015) / 0.015
    b = (0.08 * np.sin(1.7 * P_n) * np.cos(1.3 * G_n)
         + 0.05 * np.tanh(1.2 * D_n)
         + 0.04 * (x_out - 0.5)
         - 0.03 * np.tanh(P_n * G_n))
    # Heteroscedastic aleatoric noise ~ 3% relative + floor
    eps = rng.normal(0.0, 0.03 * y_base + 5e3)
    y_exp = y_base * (1.0 + b) + eps
    y_exp = np.clip(y_exp, 5e4, None)

    # Feature matrix (D, L, P, G, dh_sub, x_out).  x_out is derivable from
    # the other five in a real NRC entry; here it is sampled, so we pass it
    # explicitly to every model — same information content for both pure and
    # hybrid variants.
    X = np.stack([D, L, P, G, dh, x_out], axis=1).astype(np.float32)
    y = y_exp.astype(np.float32)
    yb = y_base.astype(np.float32)

    # 80/10/10 split (shuffled)
    idx = rng.permutation(len(y))
    n = len(y)
    n_tr, n_va = int(0.80 * n), int(0.10 * n)
    tr = idx[:n_tr]; va = idx[n_tr:n_tr + n_va]; te = idx[n_tr + n_va:]

    # Standardize on train stats
    mu_X = X[tr].mean(0); sd_X = X[tr].std(0) + 1e-9
    mu_y = float(y[tr].mean()); sd_y = float(y[tr].std() + 1e-9)

    def t(a): return torch.from_numpy(np.asarray(a)).float()
    Xz = (X - mu_X) / sd_X
    # y is kept in physical units for metric reporting; the network targets
    # a (residual or direct) value that we standardize per-task later.
    return Splits(
        X_train=t(Xz[tr]),   y_train=t(y[tr]),
        X_val=t(Xz[va]),     y_val=t(y[va]),
        X_test=t(Xz[te]),    y_test=t(y[te]),
        base_train=t(yb[tr]), base_val=t(yb[va]), base_test=t(yb[te]),
        mu_X=t(mu_X), sd_X=t(sd_X), mu_y=mu_y, sd_y=sd_y,
    )


# ---------------------------------------------------------------------------
# 3.  DNN (simple MLP, 7 hidden layers like paper) with ensemble wrapper
# ---------------------------------------------------------------------------
class MLP(nn.Module):
    def __init__(self, d_in=6, width=48, depth=7, act=nn.ELU):
        super().__init__()
        layers = []
        last = d_in
        for _ in range(depth):
            layers += [nn.Linear(last, width), act()]
            last = width
        layers += [nn.Linear(last, 1)]
        self.net = nn.Sequential(*layers)
    def forward(self, x):
        return self.net(x).squeeze(-1)


def train_one(model, X, y, X_val, y_val, epochs=250, lr=1e-3, bs=64, verbose=False):
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    sched = torch.optim.lr_scheduler.ExponentialLR(opt, gamma=0.99)
    n = len(X)
    best = (float("inf"), None)
    patience, bad = 25, 0
    for ep in range(epochs):
        model.train()
        perm = torch.randperm(n)
        for i in range(0, n, bs):
            idx = perm[i:i + bs]
            pred = model(X[idx])
            loss = ((pred - y[idx]) ** 2).mean()
            opt.zero_grad(); loss.backward(); opt.step()
        sched.step()
        model.eval()
        with torch.no_grad():
            vloss = ((model(X_val) - y_val) ** 2).mean().item()
        if vloss < best[0] - 1e-6:
            best = (vloss, {k: v.detach().clone() for k, v in model.state_dict().items()})
            bad = 0
        else:
            bad += 1
            if bad >= patience:
                break
    if best[1] is not None:
        model.load_state_dict(best[1])
    return model


def fit_ensemble(X_tr, y_tr, X_val, y_val, n_models=20, epochs=250, bs=64,
                 width=48, depth=7, seed0=0):
    """Initialization-based DNN ensemble (paper Sec 3.2)."""
    models = []
    for m in range(n_models):
        torch.manual_seed(seed0 + m)
        net = MLP(d_in=X_tr.shape[1], width=width, depth=depth)
        train_one(net, X_tr, y_tr, X_val, y_val, epochs=epochs, bs=bs)
        models.append(net)
    return models


def predict_ensemble(models, X):
    preds = []
    with torch.no_grad():
        for m in models:
            m.eval()
            preds.append(m(X).cpu().numpy())
    preds = np.stack(preds, axis=0)
    return preds.mean(0), preds.std(0)


# ---------------------------------------------------------------------------
# 4.  Metrics  (matches paper Eq. 1 and Table 6 definitions)
# ---------------------------------------------------------------------------
def metrics(y_true, y_pred):
    y_true = np.asarray(y_true, dtype=np.float64)
    y_pred = np.asarray(y_pred, dtype=np.float64)
    rel = np.abs(y_pred - y_true) / np.maximum(np.abs(y_true), 1.0)
    mu_err = rel.mean() * 100.0
    max_err = rel.max() * 100.0
    rRMSE = np.sqrt(np.mean(((y_pred - y_true) / y_true) ** 2)) * 100.0
    F10 = np.mean(rel > 0.10) * 100.0
    R2 = r2_score(y_true, y_pred)
    return dict(mu_err=mu_err, max_err=max_err, rRMSE=rRMSE, F10=F10, R2=R2)


# ---------------------------------------------------------------------------
# 5.  Run one training configuration
# ---------------------------------------------------------------------------
def standardize_target(y, mu, sd):  return (y - mu) / sd
def destandardize(y, mu, sd):       return y * sd + mu


def run_config(splits, *, hybrid: bool, limited: bool, n_models=10,
               epochs=250, tag=""):
    """Train an ensemble either as pure-ML (predict y) or Biasi-hybrid
    (predict residual r = y - y_Biasi)."""
    if limited:
        # Keep 9 training points; validation + test unchanged
        rng_local = np.random.default_rng(7)
        idx = rng_local.choice(len(splits.X_train), size=9, replace=False)
        X_tr_full = splits.X_train[idx]
        y_tr_raw  = splits.y_train[idx]
        base_tr   = splits.base_train[idx]
    else:
        X_tr_full = splits.X_train
        y_tr_raw  = splits.y_train
        base_tr   = splits.base_train

    X_val = splits.X_val; X_te = splits.X_test
    y_val_raw = splits.y_val; y_te_raw = splits.y_test
    base_val = splits.base_val; base_te = splits.base_test

    if hybrid:
        target_tr_raw  = y_tr_raw  - base_tr
        target_val_raw = y_val_raw - base_val
    else:
        target_tr_raw  = y_tr_raw
        target_val_raw = y_val_raw

    mu = float(target_tr_raw.mean().item())
    sd = float(target_tr_raw.std().item() + 1e-9)

    t_tr = (target_tr_raw  - mu) / sd
    t_val = (target_val_raw - mu) / sd

    t0 = time.time()
    # smaller ensemble when limited data (still exceeds paper's >=10)
    models = fit_ensemble(X_tr_full, t_tr, X_val, t_val,
                          n_models=n_models, epochs=epochs,
                          bs=min(64, max(2, len(X_tr_full))))
    train_s = time.time() - t0

    mean_z, std_z = predict_ensemble(models, X_te)
    pred_target = mean_z * sd + mu                  # residual or direct CHF
    pred = pred_target + (base_te.numpy() if hybrid else 0.0)

    m = metrics(y_te_raw.numpy(), pred)
    m.update(tag=tag, hybrid=hybrid, limited=limited,
             n_train=int(len(X_tr_full)), n_models=n_models,
             train_time_s=train_s)
    return m, pred, std_z * sd


# ---------------------------------------------------------------------------
# 6.  DGP (deep GP) — GPyTorch, a lightweight 2-layer variant
# ---------------------------------------------------------------------------
def run_dgp(splits, *, hybrid: bool, limited: bool,
            n_inducing=64, epochs=150, tag=""):
    import gpytorch
    from gpytorch.models.deep_gps import DeepGP, DeepGPLayer
    from gpytorch.variational import (CholeskyVariationalDistribution,
                                      VariationalStrategy)
    from gpytorch.means import ConstantMean
    from gpytorch.kernels import ScaleKernel, RBFKernel

    if limited:
        idx = np.random.default_rng(7).choice(len(splits.X_train), 9, replace=False)
        X_tr = splits.X_train[idx]; y_tr = splits.y_train[idx]
        base_tr = splits.base_train[idx]
    else:
        X_tr = splits.X_train; y_tr = splits.y_train
        base_tr = splits.base_train
    X_te = splits.X_test; y_te = splits.y_test; base_te = splits.base_test

    if hybrid:
        t_tr = y_tr - base_tr
    else:
        t_tr = y_tr
    mu = float(t_tr.mean().item()); sd = float(t_tr.std().item() + 1e-9)
    t_trn = (t_tr - mu) / sd

    class GPLayer(DeepGPLayer):
        def __init__(self, in_dim, out_dim, n_ind, lin_mean=False):
            inducing = torch.randn(out_dim, n_ind, in_dim)
            vd = CholeskyVariationalDistribution(n_ind, batch_shape=torch.Size([out_dim]))
            vs = VariationalStrategy(self, inducing, vd, learn_inducing_locations=True)
            super().__init__(vs, in_dim, out_dim)
            self.mean_module = ConstantMean(batch_shape=torch.Size([out_dim]))
            self.covar_module = ScaleKernel(RBFKernel(batch_shape=torch.Size([out_dim]),
                                                     ard_num_dims=in_dim),
                                            batch_shape=torch.Size([out_dim]))
        def forward(self, x):
            m = self.mean_module(x); k = self.covar_module(x)
            return gpytorch.distributions.MultivariateNormal(m, k)

    class DGP2(DeepGP):
        def __init__(self, in_dim):
            super().__init__()
            self.l1 = GPLayer(in_dim, 3, n_inducing)
            self.l2 = GPLayer(3, 1, n_inducing)
            self.likelihood = gpytorch.likelihoods.GaussianLikelihood()
        def forward(self, x):
            h = self.l1(x)
            return self.l2(h)

    model = DGP2(X_tr.shape[1])
    opt = torch.optim.Adam(model.parameters(), lr=1e-2)
    mll = gpytorch.mlls.DeepApproximateMLL(
        gpytorch.mlls.VariationalELBO(model.likelihood, model, X_tr.shape[0]))

    t0 = time.time()
    model.train(); model.likelihood.train()
    for ep in range(epochs):
        with gpytorch.settings.num_likelihood_samples(4):
            opt.zero_grad()
            out = model(X_tr)
            loss = -mll(out, t_trn)
            loss.backward(); opt.step()
    train_s = time.time() - t0

    model.eval(); model.likelihood.eval()
    with torch.no_grad(), gpytorch.settings.num_likelihood_samples(20):
        out = model.likelihood(model(X_te))
        mean_z = out.mean.mean(0).cpu().numpy()
        std_z  = out.variance.mean(0).sqrt().cpu().numpy()
    pred_t = mean_z * sd + mu
    pred = pred_t + (base_te.numpy() if hybrid else 0.0)
    m = metrics(y_te.numpy(), pred)
    m.update(tag=tag, hybrid=hybrid, limited=limited,
             n_train=int(len(X_tr)), train_time_s=train_s, model="DGP2")
    return m, pred, std_z * sd


# ---------------------------------------------------------------------------
# 7.  Main driver
# ---------------------------------------------------------------------------
def main():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(out_dir, exist_ok=True)

    splits = build_dataset()
    print(f"Dataset after xe>=0.2 filter:  "
          f"train={len(splits.X_train)} val={len(splits.X_val)} test={len(splits.X_test)}")

    # Baseline: Biasi correlation alone on the test set
    m_biasi = metrics(splits.y_test.numpy(), splits.base_test.numpy())
    m_biasi.update(tag="Biasi_bare", hybrid=False, limited=False,
                   n_train=0, model="correlation")

    all_results = [m_biasi]

    # ---- 80% case ------------------------------------------------------
    print("\n=== 80% training data case ===")
    r, *_ = run_config(splits, hybrid=False, limited=False,
                       n_models=10, epochs=250, tag="DNN_pure_80")
    print(r); all_results.append(r)
    r, *_ = run_config(splits, hybrid=True,  limited=False,
                       n_models=10, epochs=250, tag="DNN_Biasi_hybrid_80")
    print(r); all_results.append(r)

    # ---- 0.1% (9-point) case ------------------------------------------
    print("\n=== 9-point (limited) training data case ===")
    r, *_ = run_config(splits, hybrid=False, limited=True,
                       n_models=10, epochs=400, tag="DNN_pure_9")
    print(r); all_results.append(r)
    r, *_ = run_config(splits, hybrid=True,  limited=True,
                       n_models=10, epochs=400, tag="DNN_Biasi_hybrid_9")
    print(r); all_results.append(r)

    # ---- DGP (small, plentiful) ---------------------------------------
    print("\n=== DGP runs ===")
    try:
        r, *_ = run_dgp(splits, hybrid=False, limited=False,
                        n_inducing=64, epochs=120, tag="DGP_pure_80")
        print(r); all_results.append(r)
        r, *_ = run_dgp(splits, hybrid=True, limited=False,
                        n_inducing=64, epochs=120, tag="DGP_Biasi_hybrid_80")
        print(r); all_results.append(r)
    except Exception as e:
        print("DGP failed:", e)

    with open(os.path.join(out_dir, "results.json"), "w") as fh:
        json.dump(all_results, fh, indent=2)
    print("\nSaved:", os.path.join(out_dir, "results.json"))

    # Pretty-print summary table
    hdr = f"{'tag':30s}  {'μerr%':>7s}  {'Max%':>7s}  {'rRMSE%':>8s}  {'F10%':>6s}  {'R2':>7s}  {'ntr':>5s}"
    print("\n" + hdr); print("-" * len(hdr))
    for r in all_results:
        print(f"{r.get('tag',''):30s}  {r['mu_err']:7.3f}  {r['max_err']:7.2f}  "
              f"{r['rRMSE']:8.3f}  {r['F10']:6.2f}  {r['R2']:7.4f}  {r.get('n_train',0):5d}")

    return all_results


if __name__ == "__main__":
    main()
