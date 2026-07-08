"""
Yuval & O'Gorman 2020 — Methodology replication / sanity check
================================================================

The paper's actual training and test data is unavailable on OSF and Google Drive
(see notes/PAPER_NOTES.md). What we *can* do is verify the paper's stated RF
architecture and hyperparameter choices behave as claimed:

  - sklearn RandomForestRegressor, 10 trees, min_samples_leaf=20, max_depth=27
  - 5,000,000 training samples (or scaled down for budget)
  - Inputs: T, q_n, q_p (48 levels each) + distance from equator = 145 features
  - Outputs: dh_L/dt, dq_T/dt, dq_p/dt (48 levels each) = 144 targets
  - Standardize outputs (zero mean, unit variance) before training
  - Training claim: "less than an hour on 10 CPU cores"
  - RF size claim: ~0.75 GB for RF-tend at x8 (single precision)
  - R² on test data: ≈ 0.7-0.8 for q_T tendency (Supp Tab 2), ≈ 0.99 for precipitation

We construct a *physics-flavored synthetic dataset* with the same shape and
realistic vertical structure (height-dependent variance, mass-weighted
correlations between levels, nonlinear coupling of T/q to tendencies), then
train the paper's exact RF spec. The aim is NOT to reproduce the paper's
numerical R² (the dataset is synthetic) — it is to confirm the architecture
trains as claimed, fits in memory as claimed, and that the same code structure
used in the paper's `run_qp_production_x8.py` works end-to-end with modern
sklearn.

Output: a JSON with timing, memory, and offline R² per output and per level.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import time
from pathlib import Path

import numpy as np
import sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler


N_LEVELS = 48                          # SAM vertical levels (paper)
N_INPUTS = 3 * N_LEVELS + 1            # T, q_n, q_p (48 each) + dist-from-eq
N_OUTPUTS = 3 * N_LEVELS               # dh_L, dq_T, dq_p tendencies

# Heights (m) — rough log spacing 50 m to 25 km, mimicking SAM stretched grid
def model_heights() -> np.ndarray:
    z_bot, z_top = 50.0, 25000.0
    return np.geomspace(z_bot, z_top, N_LEVELS)


def make_synthetic_dataset(
    n_samples: int,
    seed: int = 0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Generate (X, Y, z) with physically-plausible structure.

    Inputs are smooth temperature & moisture profiles plus a latitude.
    Outputs are nonlinear, height-dependent transformations + noise, so a
    finite-tree RF can learn most but not all of the variance — mimicking
    the paper's R² of ~0.7-0.8 on tendency.
    """
    rng = np.random.default_rng(seed)
    z = model_heights()

    # Vertical T profile: surface T ~ 290 + 20*cos(lat), lapse rate ~ -7 K/km
    surf_T_mean = 290.0
    lat = rng.uniform(-1.0, 1.0, size=n_samples)            # normalized dist from eq
    surf_T = surf_T_mean + 15.0 * (1.0 - np.abs(lat)) + rng.normal(0, 2.0, n_samples)
    lapse = -7.0e-3                                          # K/m
    # base T(z)
    T = surf_T[:, None] + lapse * z[None, :]                 # (N, 48)
    # add baroclinic perturbations (mostly low/mid trop)
    perturb_amp = 6.0 * np.exp(-z[None, :] / 8000.0)
    T += rng.normal(0, 1.0, (n_samples, N_LEVELS)) * perturb_amp

    # q_n (non-precip water, kg/kg): decreases roughly exponentially with height
    q_n_surf = 0.015 * (1.0 - 0.6 * np.abs(lat)) + rng.normal(0, 0.002, n_samples).clip(-0.005, 0.005)
    q_n_surf = np.clip(q_n_surf, 1e-4, None)
    H_q = 2500.0
    q_n = q_n_surf[:, None] * np.exp(-z[None, :] / H_q)
    q_n *= (1.0 + 0.15 * rng.normal(0, 1.0, (n_samples, N_LEVELS)))
    q_n = np.clip(q_n, 0, None)

    # q_p (precipitating water): smaller, mostly in lower troposphere
    q_p_surf = 1e-4 * (1.0 - 0.5 * np.abs(lat)) + rng.uniform(0, 1e-4, n_samples)
    q_p = q_p_surf[:, None] * np.exp(-z[None, :] / 3500.0)
    q_p *= (1.0 + 0.5 * rng.normal(0, 1.0, (n_samples, N_LEVELS)))
    q_p = np.clip(q_p, 0, None)

    X = np.concatenate([T, q_n, q_p, lat[:, None]], axis=1).astype(np.float32)
    assert X.shape == (n_samples, N_INPUTS), X.shape

    # OUTPUTS:
    # dh_L/dt mostly tracks T deviation from base + nonlinear moisture coupling
    T_base = surf_T[:, None] + lapse * z[None, :]
    T_anom = T - T_base
    # dq_T/dt tracks vertical structure of q_n (moisture convergence in lower trop, drying upper)
    # dq_p/dt forced by q_n and a convective trigger (CAPE-like nonlinearity)
    CAPE_like = np.maximum(0.0, (q_n[:, :5].sum(axis=1) - 0.04)) * np.maximum(0.0, surf_T - 295.0)

    # dh_L tendency
    dhL = -1.2e-4 * T_anom * np.exp(-z[None, :] / 12000.0)
    dhL += 5.0e-4 * (q_n - q_n.mean(axis=0, keepdims=True))[:, ::-1]    # mid-trop heating from moisture
    dhL += 3.0e-5 * CAPE_like[:, None] * np.exp(-((z[None, :] - 6000) ** 2) / (3000.0 ** 2))
    dhL += rng.normal(0, 1.0e-4, (n_samples, N_LEVELS)) * np.exp(-z[None, :] / 10000.0)

    # dq_T tendency
    dqT = -2.0e-6 * q_n * np.tanh((T - 273.15) / 30.0)
    dqT += 1.5e-7 * CAPE_like[:, None] * np.exp(-((z[None, :] - 4000) ** 2) / (2500.0 ** 2))
    dqT += rng.normal(0, 3.0e-7, (n_samples, N_LEVELS)) * np.exp(-z[None, :] / 8000.0)

    # dq_p tendency
    dqP = 3.0e-7 * q_n * np.exp(-z[None, :] / 4500.0)
    dqP += 2.0e-7 * CAPE_like[:, None] * np.exp(-z[None, :] / 5000.0)
    dqP += rng.normal(0, 1.5e-7, (n_samples, N_LEVELS)) * np.exp(-z[None, :] / 5000.0)

    Y = np.concatenate([dhL, dqT, dqP], axis=1).astype(np.float32)
    assert Y.shape == (n_samples, N_OUTPUTS), Y.shape
    return X, Y, z


def standardize(Y_train: np.ndarray, Y_test: np.ndarray) -> tuple[np.ndarray, np.ndarray, StandardScaler]:
    """Paper standardizes each output variable by removing mean and rescaling to unit variance,
    with mean/var computed across all levels used for that output variable."""
    # Apply per-variable (3 outputs of 48 levels each), pooled across levels — paper's choice
    scaler_means = np.zeros(N_OUTPUTS, dtype=np.float32)
    scaler_stds = np.ones(N_OUTPUTS, dtype=np.float32)
    for v in range(3):
        s, e = v * N_LEVELS, (v + 1) * N_LEVELS
        block = Y_train[:, s:e]
        m = block.mean()
        sd = block.std()
        scaler_means[s:e] = m
        scaler_stds[s:e] = sd
    Y_train_s = (Y_train - scaler_means) / scaler_stds
    Y_test_s = (Y_test - scaler_means) / scaler_stds
    return Y_train_s, Y_test_s, (scaler_means, scaler_stds)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-train", type=int, default=500_000,
                    help="training samples (paper used 5,000,000; we scale down for budget)")
    ap.add_argument("--n-test", type=int, default=50_000)
    ap.add_argument("--n-trees", type=int, default=10, help="paper: 10")
    ap.add_argument("--min-samples-leaf", type=int, default=20, help="paper: 20")
    ap.add_argument("--max-depth", type=int, default=27, help="paper: 27")
    ap.add_argument("--n-jobs", type=int, default=10, help="paper: 10 CPU cores")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", type=str, default="results.json")
    args = ap.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    info = {
        "platform": {
            "system": platform.system(),
            "machine": platform.machine(),
            "cpu_count_logical": os.cpu_count(),
            "python": platform.python_version(),
            "sklearn": sklearn.__version__,
            "numpy": np.__version__,
        },
        "args": vars(args),
        "paper_spec": {
            "n_trees": 10,
            "min_samples_leaf": 20,
            "max_depth": 27,
            "n_train_paper": 5_000_000,
            "n_jobs_paper": 10,
            "rf_tend_x8_size_gb": 0.75,
        },
    }

    print("== Yuval & O'Gorman 2020 methodology check ==")
    for k, v in info["platform"].items():
        print(f"  {k}: {v}")
    print()

    t0 = time.time()
    print(f"Generating synthetic dataset: train={args.n_train}, test={args.n_test} ...")
    X_train, Y_train, z = make_synthetic_dataset(args.n_train, seed=args.seed)
    X_test, Y_test, _ = make_synthetic_dataset(args.n_test, seed=args.seed + 1)
    t_data = time.time() - t0
    print(f"  data: X_train={X_train.shape} Y_train={Y_train.shape}  ({t_data:.1f} s)")
    print(f"  memory: X_train={X_train.nbytes/1e6:.1f} MB, Y_train={Y_train.nbytes/1e6:.1f} MB")

    Y_train_s, Y_test_s, (mu, sd) = standardize(Y_train, Y_test)

    rf = RandomForestRegressor(
        n_estimators=args.n_trees,
        min_samples_leaf=args.min_samples_leaf,
        max_depth=args.max_depth,
        n_jobs=args.n_jobs,
        random_state=args.seed,
        verbose=0,
    )

    t1 = time.time()
    print(f"Training RF: n_trees={args.n_trees}, min_samples_leaf={args.min_samples_leaf}, "
          f"max_depth={args.max_depth}, n_jobs={args.n_jobs} ...")
    rf.fit(X_train, Y_train_s)
    t_train = time.time() - t1
    print(f"  trained in {t_train:.1f} s ({t_train/60:.2f} min)")

    # Predict + unstandardize
    Y_pred_s = rf.predict(X_test)
    Y_pred = Y_pred_s * sd + mu

    # R² overall and per variable
    var_names = ["dh_L_dt", "dq_T_dt", "dq_p_dt"]
    per_var_r2 = {}
    per_level_r2 = {}
    for v, name in enumerate(var_names):
        s, e = v * N_LEVELS, (v + 1) * N_LEVELS
        # R² pooling all levels of this variable
        per_var_r2[name] = float(r2_score(Y_test[:, s:e].ravel(), Y_pred[:, s:e].ravel()))
        # R² per level
        per_level_r2[name] = [float(r2_score(Y_test[:, s + k], Y_pred[:, s + k])) for k in range(N_LEVELS)]

    # Approx in-memory RF size
    import pickle
    rf_bytes = len(pickle.dumps(rf, protocol=4))
    rf_size_gb = rf_bytes / 1024**3

    info.update({
        "timing_seconds": {
            "data_generation": t_data,
            "rf_training": t_train,
        },
        "rf_size_pickled_gb": rf_size_gb,
        "r2_per_variable_pooled": per_var_r2,
        "r2_per_level": per_level_r2,
        "z_levels_m": z.tolist(),
    })

    print("\n== Results ==")
    for name in var_names:
        levels_r2 = per_level_r2[name]
        print(f"  {name}:  pooled R²={per_var_r2[name]:+.4f}   "
              f"per-level mean={np.mean(levels_r2):+.4f}  min={np.min(levels_r2):+.4f}  max={np.max(levels_r2):+.4f}")
    print(f"  RF pickled size: {rf_size_gb*1024:.1f} MB ({rf_size_gb:.3f} GB)")
    print(f"  vs paper RF-tend x8: 0.75 GB at full 5M samples / 10 trees / single precision netcdf")

    with out_path.open("w") as f:
        json.dump(info, f, indent=2)
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
