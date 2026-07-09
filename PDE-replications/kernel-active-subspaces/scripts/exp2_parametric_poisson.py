"""
Experiment 2 — Parametric Poisson on the unit square as a CFD-DG surrogate.

This stands in for the paper's Discontinuous-Galerkin CFD application (which
requires HopeFOAM/OpenFOAM and is far too heavy for honest replication here).
We disclose the substitution: the *claim* under test ("KAS gives better
nonlinear low-dim structure than linear AS on a parametric PDE forward map")
is exercised on a problem of the same shape — parameter-to-QoI map of an
elliptic PDE with a parametric diffusion coefficient — but solved with a
lightweight finite-difference solver instead of DG.

PDE:    -div(a(x; s) grad u) = 1   on (0,1)^2,    u = 0 on boundary
Diffusion: log a(x; s) = sum_{i=1..d} s_i * phi_i(x)
           where phi_i are the first d Karhunen-Loève modes of an exponential
           covariance kernel; s_i ~ Uniform(-1, 1).
QoI:    Q(s) = mean of u over the domain

We compute QoI samples and gradients (via centered finite differences in s),
then run AS vs KAS and compare 1-D ridge surrogate test RMSE.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import diags, kron, eye, lil_matrix
from scipy.sparse.linalg import spsolve
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel, WhiteKernel

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

LOG_PATH = LOGS / "exp2_parametric_poisson.log"


def log(msg: str) -> None:
    print(msg, flush=True)
    with open(LOG_PATH, "a") as f:
        f.write(msg + "\n")


# --- finite-difference Poisson solver ---------------------------------------

def build_grid(n):
    """n interior nodes per dim (so total interior unknowns n*n)."""
    h = 1.0 / (n + 1)
    xs = np.linspace(h, 1 - h, n)
    X, Y = np.meshgrid(xs, xs, indexing="ij")
    return xs, X, Y, h


def kl_modes(X, Y, n_modes, corr_len=0.25, var=1.0):
    """First n_modes Karhunen-Loève modes of an exponential covariance
    C(p,q) = var * exp(-||p-q||/corr_len) on the unit square.

    Builds the dense covariance matrix on the grid, eigen-decomposes once.
    """
    pts = np.column_stack([X.ravel(), Y.ravel()])
    d = np.sqrt(((pts[:, None, :] - pts[None, :, :]) ** 2).sum(-1))
    C = var * np.exp(-d / corr_len)
    # eigendecomposition (descending)
    w, v = np.linalg.eigh(C)
    idx = np.argsort(w)[::-1]
    w = w[idx][:n_modes]
    v = v[:, idx][:, :n_modes]
    # mode shape on the grid; scale by sqrt(eigenvalue) so log-a has unit-ish
    # variance per mode coefficient
    phi = v * np.sqrt(np.maximum(w, 0))  # (N, n_modes)
    phi = phi.reshape(X.shape + (n_modes,))
    return phi  # shape (n, n, n_modes)


def assemble_poisson(a_field, h):
    """Five-point FD stencil for -div(a grad u) = f with Dirichlet 0 on
    boundary. Harmonic averaging at faces; phantom outside = same value.
    Vectorized COO assembly.
    """
    from scipy.sparse import coo_matrix

    n = a_field.shape[0]
    a = a_field
    inv_h2 = 1.0 / (h * h)

    # harmonic averages at faces (with phantom = same value at boundary)
    ae = np.empty_like(a)
    ae[:, :-1] = 2 * a[:, :-1] * a[:, 1:] / (a[:, :-1] + a[:, 1:])
    ae[:, -1] = a[:, -1]
    aw = np.empty_like(a)
    aw[:, 1:] = 2 * a[:, 1:] * a[:, :-1] / (a[:, 1:] + a[:, :-1])
    aw[:, 0] = a[:, 0]
    an = np.empty_like(a)
    an[:-1, :] = 2 * a[:-1, :] * a[1:, :] / (a[:-1, :] + a[1:, :])
    an[-1, :] = a[-1, :]
    as_ = np.empty_like(a)
    as_[1:, :] = 2 * a[1:, :] * a[:-1, :] / (a[1:, :] + a[:-1, :])
    as_[0, :] = a[0, :]

    diag = (ae + aw + an + as_) * inv_h2

    I = np.arange(n * n)
    rows = [I]
    cols = [I]
    data = [diag.ravel()]

    # east neighbour (j+1)
    mask = np.zeros((n, n), dtype=bool); mask[:, :-1] = True
    src = I[mask.ravel()]
    dst = src + 1
    rows.append(src); cols.append(dst); data.append(-ae[mask] * inv_h2)
    # west (j-1)
    mask = np.zeros((n, n), dtype=bool); mask[:, 1:] = True
    src = I[mask.ravel()]
    dst = src - 1
    rows.append(src); cols.append(dst); data.append(-aw[mask] * inv_h2)
    # north (i+1)
    mask = np.zeros((n, n), dtype=bool); mask[:-1, :] = True
    src = I[mask.ravel()]
    dst = src + n
    rows.append(src); cols.append(dst); data.append(-an[mask] * inv_h2)
    # south (i-1)
    mask = np.zeros((n, n), dtype=bool); mask[1:, :] = True
    src = I[mask.ravel()]
    dst = src - n
    rows.append(src); cols.append(dst); data.append(-as_[mask] * inv_h2)

    A = coo_matrix(
        (np.concatenate(data), (np.concatenate(rows), np.concatenate(cols))),
        shape=(n * n, n * n),
    ).tocsr()
    return A


def solve_poisson(s, phi, h):
    """Solve -div(a(s) grad u) = 1, return QoI = mean(u)."""
    log_a = (phi * s).sum(axis=-1)  # (n,n)
    a = np.exp(log_a)
    n = a.shape[0]
    A = assemble_poisson(a, h)
    rhs = np.ones(n * n)
    u = spsolve(A, rhs)
    return float(u.mean()), u.reshape(n, n)


def gradient_fd(s, phi, h, eps=1e-3):
    """Centered FD gradient of Q(s) wrt s."""
    d = len(s)
    g = np.zeros(d)
    for i in range(d):
        sp = s.copy(); sp[i] += eps
        sm = s.copy(); sm[i] -= eps
        Qp, _ = solve_poisson(sp, phi, h)
        Qm, _ = solve_poisson(sm, phi, h)
        g[i] = (Qp - Qm) / (2 * eps)
    return g


def gp_surrogate_rmse(z_train, f_train, z_test, f_test):
    kernel = (
        ConstantKernel(1.0, (1e-3, 1e3))
        * RBF(length_scale=0.5, length_scale_bounds=(1e-2, 1e2))
        + WhiteKernel(noise_level=1e-5, noise_level_bounds=(1e-8, 1e-1))
    )
    gp = GaussianProcessRegressor(kernel=kernel, normalize_y=True, n_restarts_optimizer=3)
    gp.fit(z_train, f_train)
    f_hat = gp.predict(z_test)
    return float(np.sqrt(np.mean((f_hat - f_test) ** 2))), f_hat


def main():
    if LOG_PATH.exists():
        LOG_PATH.unlink()
    log("Experiment 2: Parametric Poisson (CFD-DG surrogate)")
    log(
        "  NOTE: substituted for HopeFOAM/OpenFOAM DG run. Same claim shape: "
        "parameter-to-QoI map of an elliptic PDE with parametric diffusion."
    )

    seed = 7
    rng = np.random.default_rng(seed)
    np.random.seed(seed)

    # ---- problem setup ----
    n_grid = 24  # interior nodes per dim
    n_modes = 5  # parameter dimension
    n_train = 220
    n_test = 100
    xs, X, Y, h = build_grid(n_grid)
    log(f"Grid: {n_grid}x{n_grid} interior nodes ({n_grid**2} dofs)  h={h:.4f}")
    log(f"Parameter dimension d = {n_modes}  (KL of exp covariance, corr_len=0.25)")
    log(f"n_train = {n_train}  n_test = {n_test}")

    phi = kl_modes(X, Y, n_modes=n_modes, corr_len=0.25, var=0.5)
    # rescale modes so log-a is order O(1)
    log(f"KL mode RMS: {[float(np.sqrt(np.mean(phi[..., i]**2))) for i in range(n_modes)]}")

    # ---- generate train data ----
    S_train = rng.uniform(-1, 1, (n_train, n_modes))
    Q_train = np.zeros(n_train)
    dQ_train = np.zeros((n_train, n_modes))
    for k in range(n_train):
        Q_train[k], _ = solve_poisson(S_train[k], phi, h)
        dQ_train[k] = gradient_fd(S_train[k], phi, h, eps=1e-3)
        if (k + 1) % 50 == 0:
            log(f"  train {k+1}/{n_train}  Q mean so far={Q_train[:k+1].mean():.4f}")
    log(f"Q range: [{Q_train.min():.4f}, {Q_train.max():.4f}]  std={Q_train.std():.4f}")

    # ---- generate test data ----
    S_test = rng.uniform(-1, 1, (n_test, n_modes))
    Q_test = np.zeros(n_test)
    for k in range(n_test):
        Q_test[k], _ = solve_poisson(S_test[k], phi, h)
    log(f"Q_test range: [{Q_test.min():.4f}, {Q_test.max():.4f}]")

    np.savez(
        ROOT / "data" / "poisson_kl_dataset.npz",
        S_train=S_train, Q_train=Q_train, dQ_train=dQ_train,
        S_test=S_test, Q_test=Q_test, phi=phi, h=h, xs=xs,
    )

    # ---- linear AS ----
    ss = ActiveSubspaces(dim=1, method="exact", n_boot=50)
    ss.fit(gradients=dQ_train, outputs=Q_train, inputs=S_train)
    lin_eigs = np.asarray(ss.evals).flatten()
    log(f"Linear-AS eigenvalues: {lin_eigs}")

    # try a few reduced dims
    rmse_lin = {}
    for r in [1, 2, 3]:
        Wr = ss.evects[:, :r]
        z_tr = S_train @ Wr
        z_te = S_test @ Wr
        rmse, _ = gp_surrogate_rmse(z_tr, Q_train, z_te, Q_test)
        rmse_lin[r] = rmse
        log(f"  linear-AS r={r}  ridge RMSE={rmse:.6f}")

    # ---- kernel AS tuning (held out) ----
    n_features = 400
    n_val = 50
    perm = rng.permutation(n_train)
    val_idx, tr_idx = perm[:n_val], perm[n_val:]
    S_val_k, Q_val_k = S_train[val_idx], Q_train[val_idx]
    S_tr_k, Q_tr_k, dQ_tr_k = S_train[tr_idx], Q_train[tr_idx], dQ_train[tr_idx]

    log_param_grid = np.arange(-1.5, 0.6, 0.25)
    best = None
    log("KAS tuning (held-out RMSE), r=1:")
    for lp in log_param_grid:
        param = 10.0 ** lp
        rmses = []
        for _ in range(2):
            bias = rng.uniform(0, 2 * np.pi, n_features)
            fm = FeatureMap(
                distr="laplace", bias=bias, input_dim=n_modes,
                n_features=n_features, params=np.array([param]),
                sigma_f=float(Q_train.var()),
            )
            kss = KernelActiveSubspaces(feature_map=fm, dim=1, n_features=n_features)
            kss.fit(gradients=dQ_tr_k.reshape(-1, 1, n_modes),
                    outputs=Q_tr_k, inputs=S_tr_k)
            z_tr = kss.transform(S_tr_k)[0]
            z_val = kss.transform(S_val_k)[0]
            try:
                rmse, _ = gp_surrogate_rmse(z_tr, Q_tr_k, z_val, Q_val_k)
            except Exception:
                rmse = float("inf")
            rmses.append(rmse)
        mean_rmse = float(np.mean(rmses))
        log(f"  log10(param)={lp:+.2f}  param={param:.4g}  mean RMSE={mean_rmse:.6f}")
        if best is None or mean_rmse < best["rmse"]:
            best = {"rmse": mean_rmse, "log_param": float(lp), "param": float(param)}
    log(f"Best KAS param: log10={best['log_param']:+.2f} → {best['param']:.4g}  val RMSE={best['rmse']:.6f}")

    # final KAS fit on full training set, evaluate on test
    rmse_kas = {}
    final_eigs = None
    for r in [1, 2, 3]:
        bias = rng.uniform(0, 2 * np.pi, n_features)
        fm = FeatureMap(
            distr="laplace", bias=bias, input_dim=n_modes,
            n_features=n_features, params=np.array([best["param"]]),
            sigma_f=float(Q_train.var()),
        )
        kss = KernelActiveSubspaces(feature_map=fm, dim=r, n_features=n_features)
        kss.fit(gradients=dQ_train.reshape(-1, 1, n_modes),
                outputs=Q_train, inputs=S_train)
        if r == 1:
            final_eigs = np.asarray(kss.evals).flatten()
        z_tr = kss.transform(S_train)[0]
        z_te = kss.transform(S_test)[0]
        rmse, _ = gp_surrogate_rmse(z_tr, Q_train, z_te, Q_test)
        rmse_kas[r] = rmse
        log(f"  kernel-AS r={r}  ridge RMSE={rmse:.6f}")

    # ---- figures ----
    fig, ax = plt.subplots(figsize=(5, 4))
    rs = [1, 2, 3]
    ax.semilogy(rs, [rmse_lin[r] for r in rs], "o-", label="linear AS")
    ax.semilogy(rs, [rmse_kas[r] for r in rs], "s-", label="kernel AS")
    ax.set_xlabel("reduced dim r")
    ax.set_ylabel("test ridge RMSE")
    ax.set_title("Parametric Poisson: AS vs KAS")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIGS / "exp2_rmse_vs_dim.png", dpi=140)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(5, 4))
    k = min(n_modes, len(final_eigs))
    eig_l = lin_eigs[:k]
    eig_k = np.where(final_eigs[:k] > 0, final_eigs[:k], np.nan)
    ax.semilogy(range(1, k + 1), eig_l, "o-", label="linear AS")
    ax.semilogy(range(1, k + 1), eig_k, "s-", label="kernel AS (top n_modes)")
    ax.set_xlabel("index")
    ax.set_ylabel("eigenvalue")
    ax.set_title("Eigenvalue spectra — parametric Poisson")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIGS / "exp2_eigenvalue_comparison.png", dpi=140)
    plt.close(fig)

    # diffusion-field sample plot
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.5))
    for ax, k in zip(axs, [0, 1, 2]):
        log_a = (phi * S_train[k]).sum(axis=-1)
        im = ax.imshow(np.exp(log_a), origin="lower", extent=(0, 1, 0, 1), cmap="viridis")
        ax.set_title(f"sample s_{k+1}  Q={Q_train[k]:.3f}")
        plt.colorbar(im, ax=ax, shrink=0.8)
    fig.suptitle("Three random diffusion fields a(x;s)")
    fig.tight_layout()
    fig.savefig(FIGS / "exp2_sample_diffusions.png", dpi=140)
    plt.close(fig)

    results = {
        "experiment": "exp2_parametric_poisson",
        "seed": seed,
        "n_grid": n_grid,
        "n_modes": n_modes,
        "n_train": n_train,
        "n_test": n_test,
        "n_features_kas": n_features,
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
    out = RESULTS / "exp2_parametric_poisson.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    log(f"Wrote {out}")
    log(
        "SUMMARY  linear-AS RMSE @ r=1,2,3 = "
        f"{rmse_lin[1]:.4f}, {rmse_lin[2]:.4f}, {rmse_lin[3]:.4f}  |  "
        f"kernel-AS RMSE @ r=1,2,3 = "
        f"{rmse_kas[1]:.4f}, {rmse_kas[2]:.4f}, {rmse_kas[3]:.4f}"
    )


if __name__ == "__main__":
    main()
