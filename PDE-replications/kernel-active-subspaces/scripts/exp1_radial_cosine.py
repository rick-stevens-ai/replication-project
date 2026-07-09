"""
Experiment 1 — Radial cosine ridge (canonical KAS sanity test).

Replication of Romor, Tezzele, Lario, Rozza (2020), §4 archetype: the response
f(x) = cos(||x||^2) has no 1-D *linear* active subspace but has a 1-D
*nonlinear* one (concentric circles).

Expectation:
  - Linear AS eigenvalues do NOT show a clean gap; 1-D linear ridge surrogate
    has high RMSE because the sufficient summary is multi-valued (folded).
  - Kernel AS with a tuned random-Fourier feature map (Laplace spectral
    distribution, n_features=1000) finds a clean 1-D nonlinear summary and
    the surrogate RMSE drops sharply.

NOTE: ATHENA's built-in CV (utils.CrossValidation.run) has a bug — the
training mask is computed with ``~v_mask`` (bitwise-not of indices) instead
of ``np.setdiff1d`` — so its ``average_rrmse``-based tuning is degenerate.
We replace it with an explicit held-out RMSE tuning loop here.

All code is MIT-licensed (ATHENA) or stdlib; no proprietary deps; offline.
"""

from __future__ import annotations

import json
from functools import partial
from pathlib import Path

import autograd.numpy as anp
from autograd import elementwise_grad as egrad
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel, WhiteKernel

from athena.active import ActiveSubspaces
from athena.kas import KernelActiveSubspaces
from athena.feature_map import FeatureMap
from athena.utils import Normalizer

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RESULTS = ROOT / "results"
FIGS = ROOT / "figures"
LOGS = ROOT / "logs"
for d in (RESULTS, FIGS, LOGS):
    d.mkdir(parents=True, exist_ok=True)

LOG_PATH = LOGS / "exp1_radial_cosine.log"


def log(msg: str) -> None:
    print(msg, flush=True)
    with open(LOG_PATH, "a") as f:
        f.write(msg + "\n")


# --- target ---
def radial(x, generatrix, normalizer):
    x = normalizer.inverse_transform(x)
    return generatrix(anp.linalg.norm(x, axis=1) ** 2)


def sample_in_out(input_dim, n_samples, rng):
    lb = -3.0 * np.ones(input_dim)
    ub = 3.0 * np.ones(input_dim)
    raw = rng.uniform(lb, ub, (n_samples, input_dim))
    nor = Normalizer(lb, ub)
    x = nor.fit_transform(raw)
    func = partial(radial, normalizer=nor, generatrix=lambda r: anp.cos(r))
    f = func(x)
    df = egrad(func)(x)
    return x, f, df


def gp_surrogate_rmse(z_train, f_train, z_test, f_test):
    kernel = (
        ConstantKernel(1.0, (1e-3, 1e3))
        * RBF(length_scale=0.5, length_scale_bounds=(1e-2, 1e2))
        + WhiteKernel(noise_level=1e-3, noise_level_bounds=(1e-6, 1.0))
    )
    gp = GaussianProcessRegressor(kernel=kernel, normalize_y=True, n_restarts_optimizer=3)
    gp.fit(z_train, f_train)
    f_hat = gp.predict(z_test)
    return float(np.sqrt(np.mean((f_hat - f_test) ** 2))), f_hat


def tune_kas(
    x_train, f_train, df_train, x_val, f_val,
    input_dim, n_features, sigma_f, log_param_grid, rng,
):
    """Tune KAS feature-map hyperparameter via held-out validation RMSE.

    For each log10(bandwidth) in the grid, build a fresh feature map (fresh
    bias + projection-matrix random sample drawn inside the FeatureMap), fit
    KAS, fit a GP on the 1-D reduced coord, score on validation set. Repeat
    `n_resample` times per grid point to average out projection-matrix noise.
    Return the best feature map and its fitted KAS.
    """
    n_resample = 3
    best = None
    log("KAS tuning (held-out RMSE):")
    for lp in log_param_grid:
        param = 10.0 ** lp
        rmses = []
        for r in range(n_resample):
            bias = rng.uniform(0, 2 * np.pi, n_features)
            fm = FeatureMap(
                distr="laplace",
                bias=bias,
                input_dim=input_dim,
                n_features=n_features,
                params=np.array([param]),
                sigma_f=sigma_f,
            )
            kss = KernelActiveSubspaces(feature_map=fm, dim=1, n_features=n_features)
            kss.fit(
                gradients=df_train.reshape(-1, 1, input_dim),
                outputs=f_train,
                inputs=x_train,
            )
            z_tr = kss.transform(x_train)[0]
            z_val = kss.transform(x_val)[0]
            try:
                rmse, _ = gp_surrogate_rmse(z_tr, f_train, z_val, f_val)
            except Exception as e:  # pragma: no cover
                rmse = float("inf")
            rmses.append(rmse)
        mean_rmse = float(np.mean(rmses))
        log(f"  log10(param)={lp:+.2f}  param={param:.4g}  mean held-out RMSE={mean_rmse:.4f}")
        if best is None or mean_rmse < best["rmse"]:
            # refit with last seed of best param to keep a usable kss
            bias = rng.uniform(0, 2 * np.pi, n_features)
            fm = FeatureMap(
                distr="laplace",
                bias=bias,
                input_dim=input_dim,
                n_features=n_features,
                params=np.array([param]),
                sigma_f=sigma_f,
            )
            kss = KernelActiveSubspaces(feature_map=fm, dim=1, n_features=n_features)
            kss.fit(
                gradients=df_train.reshape(-1, 1, input_dim),
                outputs=f_train,
                inputs=x_train,
            )
            best = {"rmse": mean_rmse, "log_param": lp, "param": param, "fm": fm, "kss": kss}
    log(f"  best log10(param)={best['log_param']:+.2f}  RMSE={best['rmse']:.4f}")
    return best


def main():
    if LOG_PATH.exists():
        LOG_PATH.unlink()
    log("Experiment 1: Radial cosine ridge — replication of Romor et al. §4 archetype")

    seed = 42
    rng = np.random.default_rng(seed)
    np.random.seed(seed)
    input_dim = 2
    n_samples = 800
    N_test = 500
    n_features = 1000

    x_train, f_train, df_train = sample_in_out(input_dim, n_samples, rng)
    x_test, f_test, df_test = sample_in_out(input_dim, N_test, rng)
    log(f"input_dim={input_dim}  n_train={n_samples}  n_test={N_test}  n_features={n_features}")

    # ---- linear AS ----
    ss = ActiveSubspaces(dim=1, method="exact", n_boot=50)
    ss.fit(gradients=df_train, outputs=f_train, inputs=x_train)
    lin_eigs = np.asarray(ss.evals).flatten()
    log(f"Linear-AS eigenvalues (top 4): {lin_eigs[:4]}")

    W_lin = ss.evects[:, :1]
    z_lin_train = x_train @ W_lin
    z_lin_test = x_test @ W_lin
    rmse_lin, f_hat_lin = gp_surrogate_rmse(z_lin_train, f_train, z_lin_test, f_test)
    log(f"Linear-AS 1-D ridge RMSE (held out): {rmse_lin:.6f}")

    fig, ax = plt.subplots(figsize=(5, 4))
    order = np.argsort(z_lin_test.ravel())
    ax.scatter(z_lin_test, f_test, s=10, alpha=0.6, label="truth")
    ax.plot(z_lin_test[order], f_hat_lin[order], "r-", lw=2, label="GP ridge surrogate")
    ax.set_xlabel(r"linear AS coord $W_1^\top x$")
    ax.set_ylabel("f(x)")
    ax.set_title(f"Linear AS — radial cosine (RMSE={rmse_lin:.3f})")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGS / "exp1_linear_AS_summary.png", dpi=140)
    plt.close(fig)

    # ---- kernel AS ----
    # split train into train/val for KAS tuning
    n_val = 200
    perm = rng.permutation(n_samples)
    val_idx, tr_idx = perm[:n_val], perm[n_val:]
    x_val_k = x_train[val_idx]
    f_val_k = f_train[val_idx]
    x_tr_k = x_train[tr_idx]
    f_tr_k = f_train[tr_idx]
    df_tr_k = df_train[tr_idx]

    log_param_grid = np.arange(-2.0, 0.2, 0.2)
    best = tune_kas(
        x_tr_k, f_tr_k, df_tr_k, x_val_k, f_val_k,
        input_dim, n_features, float(np.var(f_train)), log_param_grid, rng,
    )

    # refit on full training set with best hyperparam
    final_fm = FeatureMap(
        distr="laplace",
        bias=rng.uniform(0, 2 * np.pi, n_features),
        input_dim=input_dim,
        n_features=n_features,
        params=np.array([best["param"]]),
        sigma_f=float(np.var(f_train)),
    )
    final_kss = KernelActiveSubspaces(feature_map=final_fm, dim=1, n_features=n_features)
    final_kss.fit(
        gradients=df_train.reshape(-1, 1, input_dim),
        outputs=f_train,
        inputs=x_train,
    )
    kas_eigs = np.asarray(final_kss.evals).flatten()
    log(f"Kernel-AS eigenvalues (top 4): {kas_eigs[:4]}")

    z_kas_train = final_kss.transform(x_train)[0]
    z_kas_test = final_kss.transform(x_test)[0]
    rmse_kas, f_hat_kas = gp_surrogate_rmse(z_kas_train, f_train, z_kas_test, f_test)
    log(f"Kernel-AS 1-D ridge RMSE (held out): {rmse_kas:.6f}")

    fig, ax = plt.subplots(figsize=(5, 4))
    order = np.argsort(z_kas_test.ravel())
    ax.scatter(z_kas_test, f_test, s=10, alpha=0.6, label="truth")
    ax.plot(z_kas_test[order], f_hat_kas[order], "r-", lw=2, label="GP ridge surrogate")
    ax.set_xlabel("kernel AS coord (KAS reduced)")
    ax.set_ylabel("f(x)")
    ax.set_title(f"Kernel AS — radial cosine (RMSE={rmse_kas:.3f})")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGS / "exp1_kernel_AS_summary.png", dpi=140)
    plt.close(fig)

    # eigenvalue comparison
    fig, ax = plt.subplots(figsize=(5, 4))
    k = min(8, len(lin_eigs), len(kas_eigs))
    # avoid log of zero
    eig_l = np.where(lin_eigs[:k] > 0, lin_eigs[:k], np.nan)
    eig_k = np.where(kas_eigs[:k] > 0, kas_eigs[:k], np.nan)
    ax.semilogy(range(1, k + 1), eig_l, "o-", label="linear AS")
    ax.semilogy(range(1, k + 1), eig_k, "s-", label="kernel AS")
    ax.set_xlabel("index")
    ax.set_ylabel("eigenvalue")
    ax.set_title("Eigenvalue spectra (radial cosine)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGS / "exp1_eigenvalue_comparison.png", dpi=140)
    plt.close(fig)

    results = {
        "experiment": "exp1_radial_cosine",
        "seed": seed,
        "input_dim": input_dim,
        "n_train": n_samples,
        "n_test": N_test,
        "n_features": n_features,
        "linear_AS_top4_eigvals": lin_eigs[:4].tolist(),
        "kernel_AS_top4_eigvals": kas_eigs[:4].tolist(),
        "linear_AS_ridge_rmse": rmse_lin,
        "kernel_AS_ridge_rmse": rmse_kas,
        "rmse_improvement_factor": rmse_lin / max(rmse_kas, 1e-12),
        "best_kas_log_param": float(best["log_param"]),
        "best_kas_param": float(best["param"]),
        "notes": (
            "ATHENA's built-in CrossValidation.run has a bug "
            "(t_mask = ~v_mask gives wrap-around negative indices); "
            "we use an explicit held-out tuning loop instead."
        ),
    }
    out = RESULTS / "exp1_radial_cosine.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    log(f"Wrote {out}")
    log(
        f"SUMMARY  linear-AS RMSE = {rmse_lin:.4f}  kernel-AS RMSE = {rmse_kas:.4f}  "
        f"improvement factor = {rmse_lin / max(rmse_kas, 1e-12):.2f}x"
    )


if __name__ == "__main__":
    main()
