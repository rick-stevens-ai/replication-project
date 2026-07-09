"""
Experiment 3 — Nonlinear QoI on the parametric Poisson problem.

Goal: stress the kernel-AS advantage on the PDE surrogate. The naive QoI
(domain mean of u) is too close to affine in s for KAS to help (see exp2).
Here we use a deliberately nonlinear QoI:

    Q(s) = log( integral |grad u|^2 dx ) + 0.5 * (s_1^2 + s_3^2)

The (s_1^2 + s_3^2) term has no linear active subspace by construction
(symmetric in sign of s_1, s_3), so 1-D linear AS must fail and KAS should
succeed.

We reuse the same KL diffusion field and Poisson solver as exp2.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel, WhiteKernel

sys.path.insert(0, str(Path(__file__).resolve().parent))
from exp2_parametric_poisson import build_grid, kl_modes, solve_poisson, assemble_poisson  # noqa: E402

from athena.active import ActiveSubspaces
from athena.kas import KernelActiveSubspaces
from athena.feature_map import FeatureMap

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RESULTS = ROOT / "results"
FIGS = ROOT / "figures"
LOGS = ROOT / "logs"
for d in (RESULTS, FIGS, LOGS):
    d.mkdir(parents=True, exist_ok=True)
LOG_PATH = LOGS / "exp3_nonlinear_qoi.log"


def log(msg: str) -> None:
    print(msg, flush=True)
    with open(LOG_PATH, "a") as f:
        f.write(msg + "\n")


def grad_mag_integral(u, h):
    """integral over (0,1)^2 of |grad u|^2 with FD gradients and trap rule."""
    n = u.shape[0]
    # central differences on interior (boundary u = 0 from solver setup)
    # Pad with zeros on boundary so the gradient is well-defined.
    up = np.zeros((n + 2, n + 2))
    up[1:-1, 1:-1] = u
    dux = (up[1:-1, 2:] - up[1:-1, :-2]) / (2 * h)
    duy = (up[2:, 1:-1] - up[:-2, 1:-1]) / (2 * h)
    return float(((dux ** 2 + duy ** 2) * h * h).sum())


def QoI_and_solution(s, phi, h):
    Qmean, u = solve_poisson(s, phi, h)
    e = grad_mag_integral(u, h)  # > 0
    return float(np.log(e + 1e-12) + 0.5 * (s[0] ** 2 + s[2] ** 2)), u


def grad_QoI_fd(s, phi, h, eps=1e-3):
    d = len(s)
    g = np.zeros(d)
    for i in range(d):
        sp = s.copy(); sp[i] += eps
        sm = s.copy(); sm[i] -= eps
        Qp, _ = QoI_and_solution(sp, phi, h)
        Qm, _ = QoI_and_solution(sm, phi, h)
        g[i] = (Qp - Qm) / (2 * eps)
    return g


def gp_rmse(z_tr, f_tr, z_te, f_te):
    kernel = (
        ConstantKernel(1.0, (1e-3, 1e3))
        * RBF(length_scale=0.5, length_scale_bounds=(1e-2, 1e2))
        + WhiteKernel(noise_level=1e-4, noise_level_bounds=(1e-7, 1.0))
    )
    gp = GaussianProcessRegressor(kernel=kernel, normalize_y=True, n_restarts_optimizer=3)
    gp.fit(z_tr, f_tr)
    f_hat = gp.predict(z_te)
    return float(np.sqrt(np.mean((f_hat - f_te) ** 2))), f_hat


def main():
    if LOG_PATH.exists():
        LOG_PATH.unlink()
    log("Experiment 3: Nonlinear QoI on the parametric Poisson surrogate")
    log("  QoI = log(integral |grad u|^2) + 0.5*(s_1^2 + s_3^2)")
    log("  By construction the (s_1^2 + s_3^2) term has no 1-D linear AS.")

    seed = 11
    rng = np.random.default_rng(seed)
    np.random.seed(seed)

    n_grid = 24
    n_modes = 5
    n_train = 220
    n_test = 100
    xs, X, Y, h = build_grid(n_grid)
    phi = kl_modes(X, Y, n_modes=n_modes, corr_len=0.25, var=0.5)

    S_train = rng.uniform(-1, 1, (n_train, n_modes))
    Q_train = np.zeros(n_train)
    dQ_train = np.zeros((n_train, n_modes))
    for k in range(n_train):
        Q_train[k], _ = QoI_and_solution(S_train[k], phi, h)
        dQ_train[k] = grad_QoI_fd(S_train[k], phi, h, eps=1e-3)
        if (k + 1) % 50 == 0:
            log(f"  train {k+1}/{n_train}  Q std so far={Q_train[:k+1].std():.4f}")
    log(f"Q range: [{Q_train.min():.4f}, {Q_train.max():.4f}]  std={Q_train.std():.4f}")

    S_test = rng.uniform(-1, 1, (n_test, n_modes))
    Q_test = np.zeros(n_test)
    for k in range(n_test):
        Q_test[k], _ = QoI_and_solution(S_test[k], phi, h)

    # ---- linear AS ----
    ss = ActiveSubspaces(dim=1, method="exact", n_boot=50)
    ss.fit(gradients=dQ_train, outputs=Q_train, inputs=S_train)
    lin_eigs = np.asarray(ss.evals).flatten()
    log(f"Linear-AS eigenvalues: {lin_eigs}")

    rmse_lin = {}
    for r in [1, 2, 3]:
        Wr = ss.evects[:, :r]
        z_tr = S_train @ Wr; z_te = S_test @ Wr
        rmse, _ = gp_rmse(z_tr, Q_train, z_te, Q_test)
        rmse_lin[r] = rmse
        log(f"  linear-AS r={r}  test RMSE={rmse:.6f}")

    # ---- KAS tune ----
    n_features = 400
    n_val = 50
    perm = rng.permutation(n_train)
    val_idx, tr_idx = perm[:n_val], perm[n_val:]
    S_val_k, Q_val_k = S_train[val_idx], Q_train[val_idx]
    S_tr_k, Q_tr_k, dQ_tr_k = S_train[tr_idx], Q_train[tr_idx], dQ_train[tr_idx]

    log_param_grid = np.arange(-1.5, 0.8, 0.25)
    best = None
    log("KAS tuning (held-out RMSE) r=1:")
    for lp in log_param_grid:
        param = 10.0 ** lp
        rmses = []
        for _ in range(2):
            bias = rng.uniform(0, 2 * np.pi, n_features)
            fm = FeatureMap(distr="laplace", bias=bias, input_dim=n_modes,
                            n_features=n_features, params=np.array([param]),
                            sigma_f=float(Q_train.var()))
            kss = KernelActiveSubspaces(feature_map=fm, dim=1, n_features=n_features)
            kss.fit(gradients=dQ_tr_k.reshape(-1, 1, n_modes),
                    outputs=Q_tr_k, inputs=S_tr_k)
            z_tr = kss.transform(S_tr_k)[0]
            z_val = kss.transform(S_val_k)[0]
            try:
                rmse, _ = gp_rmse(z_tr, Q_tr_k, z_val, Q_val_k)
            except Exception:
                rmse = float("inf")
            rmses.append(rmse)
        mean_rmse = float(np.mean(rmses))
        log(f"  log10(param)={lp:+.2f}  param={param:.4g}  mean RMSE={mean_rmse:.6f}")
        if best is None or mean_rmse < best["rmse"]:
            best = {"rmse": mean_rmse, "log_param": float(lp), "param": float(param)}
    log(f"Best KAS param: log10={best['log_param']:+.2f}  val RMSE={best['rmse']:.6f}")

    rmse_kas = {}
    final_eigs = None
    for r in [1, 2, 3]:
        bias = rng.uniform(0, 2 * np.pi, n_features)
        fm = FeatureMap(distr="laplace", bias=bias, input_dim=n_modes,
                        n_features=n_features, params=np.array([best["param"]]),
                        sigma_f=float(Q_train.var()))
        kss = KernelActiveSubspaces(feature_map=fm, dim=r, n_features=n_features)
        kss.fit(gradients=dQ_train.reshape(-1, 1, n_modes),
                outputs=Q_train, inputs=S_train)
        if r == 1:
            final_eigs = np.asarray(kss.evals).flatten()
        z_tr = kss.transform(S_train)[0]
        z_te = kss.transform(S_test)[0]
        rmse, _ = gp_rmse(z_tr, Q_train, z_te, Q_test)
        rmse_kas[r] = rmse
        log(f"  kernel-AS r={r}  test RMSE={rmse:.6f}")

    # ---- figures ----
    fig, ax = plt.subplots(figsize=(5, 4))
    rs = [1, 2, 3]
    ax.semilogy(rs, [rmse_lin[r] for r in rs], "o-", label="linear AS")
    ax.semilogy(rs, [rmse_kas[r] for r in rs], "s-", label="kernel AS")
    ax.set_xlabel("reduced dim r")
    ax.set_ylabel("test ridge RMSE")
    ax.set_title("Nonlinear QoI Poisson: AS vs KAS")
    ax.legend(); ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout(); fig.savefig(FIGS / "exp3_rmse_vs_dim.png", dpi=140); plt.close(fig)

    fig, ax = plt.subplots(figsize=(5, 4))
    k = n_modes
    eig_l = lin_eigs[:k]; eig_k = np.where(final_eigs[:k] > 0, final_eigs[:k], np.nan)
    ax.semilogy(range(1, k + 1), eig_l, "o-", label="linear AS")
    ax.semilogy(range(1, k + 1), eig_k, "s-", label="kernel AS")
    ax.set_xlabel("index"); ax.set_ylabel("eigenvalue")
    ax.set_title("Nonlinear QoI: eigenvalue spectra")
    ax.legend(); ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout(); fig.savefig(FIGS / "exp3_eigenvalue_comparison.png", dpi=140); plt.close(fig)

    # sufficient summaries side by side
    Wlin1 = ss.evects[:, :1]
    z_lin = S_test @ Wlin1
    bias = rng.uniform(0, 2 * np.pi, n_features)
    fm = FeatureMap(distr="laplace", bias=bias, input_dim=n_modes,
                    n_features=n_features, params=np.array([best["param"]]),
                    sigma_f=float(Q_train.var()))
    kss = KernelActiveSubspaces(feature_map=fm, dim=1, n_features=n_features)
    kss.fit(gradients=dQ_train.reshape(-1, 1, n_modes),
            outputs=Q_train, inputs=S_train)
    z_kas = kss.transform(S_test)[0]

    fig, axs = plt.subplots(1, 2, figsize=(10, 4))
    axs[0].scatter(z_lin, Q_test, s=14, alpha=0.7)
    axs[0].set_xlabel("linear AS coord"); axs[0].set_ylabel("Q(s)")
    axs[0].set_title(f"Linear AS (RMSE={rmse_lin[1]:.4f})")
    axs[1].scatter(z_kas, Q_test, s=14, alpha=0.7)
    axs[1].set_xlabel("kernel AS coord"); axs[1].set_ylabel("Q(s)")
    axs[1].set_title(f"Kernel AS (RMSE={rmse_kas[1]:.4f})")
    fig.tight_layout(); fig.savefig(FIGS / "exp3_sufficient_summaries.png", dpi=140); plt.close(fig)

    results = {
        "experiment": "exp3_nonlinear_qoi",
        "seed": seed,
        "n_grid": n_grid, "n_modes": n_modes,
        "n_train": n_train, "n_test": n_test, "n_features_kas": n_features,
        "linear_AS_eigvals": lin_eigs.tolist(),
        "kernel_AS_top_eigvals": final_eigs[:n_modes].tolist(),
        "linear_AS_rmse_by_r": rmse_lin,
        "kernel_AS_rmse_by_r": rmse_kas,
        "best_kas_log_param": best["log_param"],
        "best_kas_param": best["param"],
        "best_kas_val_rmse": best["rmse"],
        "Q_train_std": float(Q_train.std()),
        "Q_test_std": float(Q_test.std()),
    }
    out = RESULTS / "exp3_nonlinear_qoi.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    log(f"Wrote {out}")
    log(
        f"SUMMARY linear-AS r=1,2,3: {rmse_lin[1]:.4f}, {rmse_lin[2]:.4f}, {rmse_lin[3]:.4f}  |  "
        f"kernel-AS r=1,2,3: {rmse_kas[1]:.4f}, {rmse_kas[2]:.4f}, {rmse_kas[3]:.4f}"
    )


if __name__ == "__main__":
    main()
