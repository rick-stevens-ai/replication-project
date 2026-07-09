"""Replicate Figures 1–3 of Cordoni 2023 (Entropy 25, 1322).

Saves JSON/CSV summaries in ../results/ and PNG figures in ../figures/.

Run with:
    python run_replication.py
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from gsm2_model import (
    PAPER_PARAMS,
    macro_ode,
    moment_ode,
    ssa_ensemble,
    time_dep_ou_paths,
)


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RES = ROOT / "results"
FIG = ROOT / "figures"
RES.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# 0.  Parameters
# ---------------------------------------------------------------------------
P = dict(PAPER_PARAMS)
T_MAX = 1.5  # paper plots cover 0..~1.5 a.u.; histograms at 0.5/0.7/0.9
N_T = 301
T_GRID = np.linspace(0.0, T_MAX, N_T)
HIST_TIMES = np.array([0.5, 0.7, 0.9])

N_SSA = 20_000          # ensemble size for histograms / moments
N_OU = 20_000           # OU paths for the Gaussian approximation
N_DISPLAY = 10          # paths shown in Fig. 3


# ---------------------------------------------------------------------------
# 1.  Deterministic mean + moment ODEs
# ---------------------------------------------------------------------------
print("[1/5] integrating macroscopic mean + moment ODEs ...")
moments = moment_ode(
    x0=P["x0"], y0=P["y0"], r=P["r"], a=P["a"], b=P["b_tilde"],
    t_eval=T_GRID,
    c_init=(0.0, 0.0, 0.0),   # deterministic initial condition
)
xbar = moments["x"]
ybar = moments["y"]
c_vv = moments["c_vv"]
c_xv = moments["c_xi_v"]
c_xx = moments["c_xi_xi"]


# ---------------------------------------------------------------------------
# 2.  SSA ensemble
# ---------------------------------------------------------------------------
print(f"[2/5] running {N_SSA:,} Gillespie realizations ...")
ssa = ssa_ensemble(
    x0=P["x0"], y0=P["y0"], r=P["r"], a=P["a"], b_tilde=P["b_tilde"],
    t_eval=T_GRID, n_paths=N_SSA, seed=20260529,
)
X_ssa = ssa["X"]   # (N_SSA, N_T)
Y_ssa = ssa["Y"]


# Empirical moments from SSA
mean_X_ssa = X_ssa.mean(axis=0)
mean_Y_ssa = Y_ssa.mean(axis=0)
var_X_ssa = X_ssa.var(axis=0, ddof=1)
var_Y_ssa = Y_ssa.var(axis=0, ddof=1)
cov_XY_ssa = np.array(
    [np.cov(X_ssa[:, k], Y_ssa[:, k], ddof=1)[0, 1] for k in range(N_T)]
)


# ---------------------------------------------------------------------------
# 3.  OU sample paths (for Fig. 3 + sanity)
# ---------------------------------------------------------------------------
print(f"[3/5] simulating {N_OU:,} OU sample paths ...")
ou = time_dep_ou_paths(
    x0=P["x0"], y0=P["y0"], r=P["r"], a=P["a"], b=P["b_tilde"],
    t_eval=T_GRID, n_paths=N_OU,
    rng=np.random.default_rng(420),
)
X_ou = ou["X"]
Y_ou = ou["Y"]


# ---------------------------------------------------------------------------
# 4.  Save numerical results
# ---------------------------------------------------------------------------
print("[4/5] saving numerical results ...")

# CSV — full moment trajectory
np.savetxt(
    RES / "moments_vs_time.csv",
    np.column_stack([
        T_GRID,
        xbar, ybar,
        c_xx, c_xv, c_vv,
        mean_X_ssa, mean_Y_ssa,
        var_X_ssa, var_Y_ssa, cov_XY_ssa,
    ]),
    header=(
        "t,xbar_ODE,ybar_ODE,c_xi_xi_ODE,c_xi_v_ODE,c_vv_ODE,"
        "mean_X_SSA,mean_Y_SSA,var_X_SSA,var_Y_SSA,cov_XY_SSA"
    ),
    delimiter=",",
    comments="",
)

# JSON — headline numbers
summary = {
    "paper": "Cordoni 2023 Entropy 25 1322",
    "doi": "10.3390/e25091322",
    "parameters": {**P, "K_convention": "b_tilde absorbs K; SSA at K=1"},
    "t_max": T_MAX,
    "n_t": int(N_T),
    "n_ssa": int(N_SSA),
    "n_ou": int(N_OU),
    "hist_times": HIST_TIMES.tolist(),
    "endpoint": {
        "t": float(T_GRID[-1]),
        "xbar_ODE": float(xbar[-1]),
        "ybar_ODE": float(ybar[-1]),
        "c_xi_xi_ODE": float(c_xx[-1]),
        "c_xi_v_ODE": float(c_xv[-1]),
        "c_vv_ODE": float(c_vv[-1]),
        "mean_X_SSA": float(mean_X_ssa[-1]),
        "mean_Y_SSA": float(mean_Y_ssa[-1]),
        "var_X_SSA": float(var_X_ssa[-1]),
        "var_Y_SSA": float(var_Y_ssa[-1]),
        "cov_XY_SSA": float(cov_XY_ssa[-1]),
        "fano_Y_SSA": float(var_Y_ssa[-1] / mean_Y_ssa[-1])
            if mean_Y_ssa[-1] > 0 else None,
        "fano_Y_LNA": float(c_vv[-1] / ybar[-1]) if ybar[-1] > 0 else None,
    },
    # Closed-form long-time limit for ybar from Eq. (above Remark 2):
    #   ybar_inf = y0 - (r / 2b) * log( (a+r)/x0 + 2b ) / ... 
    # Easier: report the simulated long-time limit.
    "claim_subpoissonian_lethal": {
        "description": "Variance of Y is strictly below the mean Y at large t",
        "var_Y_SSA_endpoint": float(var_Y_ssa[-1]),
        "mean_Y_SSA_endpoint": float(mean_Y_ssa[-1]),
        "delta_t_endpoint": float(mean_Y_ssa[-1] - var_Y_ssa[-1]),
        "subpoissonian": bool(var_Y_ssa[-1] < mean_Y_ssa[-1]),
    },
    "claim_negative_covariance": {
        "min_cov_XY_SSA": float(cov_XY_ssa.min()),
        "min_cov_XY_LNA": float(c_xv.min()),
        "always_nonpositive_SSA": bool((cov_XY_ssa <= 0).all()),
        "always_nonpositive_LNA": bool((c_xv <= 0).all()),
    },
    "claim_mkm_macroscopic_limit": {
        "xbar_endpoint_ODE": float(xbar[-1]),
        "xbar_endpoint_SSA": float(mean_X_ssa[-1]),
        "ybar_endpoint_ODE": float(ybar[-1]),
        "ybar_endpoint_SSA": float(mean_Y_ssa[-1]),
        "abs_err_xbar": float(abs(xbar[-1] - mean_X_ssa[-1])),
        "abs_err_ybar": float(abs(ybar[-1] - mean_Y_ssa[-1])),
    },
}

with open(RES / "summary.json", "w") as fh:
    json.dump(summary, fh, indent=2)


# Per-time histogram data (lethal + sublethal) at the three reported times
hist_data = {}
for tval in HIST_TIMES:
    idx = int(np.argmin(np.abs(T_GRID - tval)))
    Xk = X_ssa[:, idx]
    Yk = Y_ssa[:, idx]
    # LNA Gaussian parameters at this time
    g_idx = idx
    g_mean_X = xbar[g_idx]
    g_var_X = c_xx[g_idx]
    g_mean_Y = ybar[g_idx]
    g_var_Y = c_vv[g_idx]
    hist_data[f"t={tval}"] = {
        "t_actual": float(T_GRID[idx]),
        "SSA_mean_X": float(Xk.mean()),
        "SSA_var_X": float(Xk.var(ddof=1)),
        "SSA_mean_Y": float(Yk.mean()),
        "SSA_var_Y": float(Yk.var(ddof=1)),
        "LNA_mean_X": float(g_mean_X),
        "LNA_var_X": float(g_var_X),
        "LNA_mean_Y": float(g_mean_Y),
        "LNA_var_Y": float(g_var_Y),
        "Fano_Y_SSA": float(Yk.var(ddof=1) / Yk.mean()) if Yk.mean() > 0 else None,
        "Fano_Y_LNA": float(g_var_Y / g_mean_Y) if g_mean_Y > 0 else None,
    }
with open(RES / "histogram_summary.json", "w") as fh:
    json.dump(hist_data, fh, indent=2)


# ---------------------------------------------------------------------------
# 5.  Figures
# ---------------------------------------------------------------------------
print("[5/5] rendering figures ...")

# ---- Figure 1: SSA histograms vs LNA Gaussian at three times ----
fig, axes = plt.subplots(2, 3, figsize=(13, 7), sharey="row")
for col, tval in enumerate(HIST_TIMES):
    idx = int(np.argmin(np.abs(T_GRID - tval)))
    Xk = X_ssa[:, idx]
    Yk = Y_ssa[:, idx]

    # ---- sub-lethal X (top row) ----
    ax = axes[0, col]
    xx_min, xx_max = Xk.min(), Xk.max()
    bins = np.arange(xx_min, xx_max + 2) - 0.5
    ax.hist(Xk, bins=bins, density=True, color="steelblue",
            alpha=0.85, edgecolor="white", linewidth=0.4,
            label="SSA")
    # Gaussian curve (LNA), centered at xbar, var = c_xi_xi
    mu, sig2 = xbar[idx], max(c_xx[idx], 1e-6)
    xx = np.linspace(xx_min, xx_max, 400)
    g = (1.0 / np.sqrt(2.0 * np.pi * sig2)) * np.exp(-0.5 * (xx - mu) ** 2 / sig2)
    ax.plot(xx, g, color="gold", lw=2.2, label="LNA (Gaussian)")
    ax.set_title(f"X (sub-lethal), t = {tval} a.u.")
    ax.set_xlabel("X")
    if col == 0:
        ax.set_ylabel("density")
    ax.legend(fontsize=8, loc="upper right")

    # ---- lethal Y (bottom row) ----
    ax = axes[1, col]
    yy_min, yy_max = Yk.min(), Yk.max()
    bins = np.arange(yy_min, yy_max + 2) - 0.5
    ax.hist(Yk, bins=bins, density=True, color="indianred",
            alpha=0.85, edgecolor="white", linewidth=0.4,
            label="SSA")
    mu, sig2 = ybar[idx], max(c_vv[idx], 1e-6)
    yy = np.linspace(yy_min, yy_max, 400)
    g = (1.0 / np.sqrt(2.0 * np.pi * sig2)) * np.exp(-0.5 * (yy - mu) ** 2 / sig2)
    ax.plot(yy, g, color="gold", lw=2.2, label="LNA (Gaussian)")
    # overlay Poisson(ybar) for visual deviation
    from math import lgamma
    k_arr = np.arange(max(0, int(yy_min)), int(yy_max) + 1)
    log_pois = -mu + k_arr * np.log(max(mu, 1e-12)) - np.array(
        [lgamma(k + 1) for k in k_arr]
    )
    ax.plot(k_arr, np.exp(log_pois), color="black", lw=1.2, linestyle="--",
            label=f"Poisson(ȳ={mu:.1f})")
    ax.set_title(f"Y (lethal), t = {tval} a.u.")
    ax.set_xlabel("Y")
    if col == 0:
        ax.set_ylabel("density")
    ax.legend(fontsize=8, loc="upper right")

fig.suptitle(
    "Fig. 1 — SSA vs linear-noise Gaussian (vs Poisson reference); "
    f"x₀={P['x0']}, y₀={P['y0']}, r={P['r']}, a={P['a']}, b̃={P['b_tilde']}",
    fontsize=11,
)
fig.tight_layout(rect=(0, 0, 1, 0.96))
fig.savefig(FIG / "fig1_histograms.png", dpi=150)
plt.close(fig)


# ---- Figure 2: time evolution of means and (co)variances ----
fig, ax = plt.subplots(1, 1, figsize=(9, 5.5))
ax.plot(T_GRID, xbar, color="gold", lw=2.0, label=r"$\bar{x}$ (LNA mean, sub-lethal)")
ax.plot(T_GRID, c_xx, color="purple", lw=1.6, label=r"$c_{\xi\xi}$ (var sub-lethal)")
ax.plot(T_GRID, ybar, color="steelblue", lw=2.0, label=r"$\bar{y}$ (LNA mean, lethal)")
ax.plot(T_GRID, c_vv, color="crimson", lw=1.6, label=r"$c_{vv}$ (var lethal)")
ax.plot(T_GRID, c_xv, color="black", lw=1.4, label=r"$c_{\xi v}$ (covariance)")
ax.axhline(0, color="grey", lw=0.6, linestyle=":")

# overlay SSA empirical moments as faint markers
mark_every = max(1, N_T // 30)
ax.plot(T_GRID[::mark_every], mean_X_ssa[::mark_every], "o",
        color="gold", mec="k", mew=0.4, ms=4, alpha=0.85,
        label="SSA $\\langle X \\rangle$")
ax.plot(T_GRID[::mark_every], mean_Y_ssa[::mark_every], "o",
        color="steelblue", mec="k", mew=0.4, ms=4, alpha=0.85,
        label="SSA $\\langle Y \\rangle$")
ax.plot(T_GRID[::mark_every], var_Y_ssa[::mark_every], "s",
        color="crimson", mec="k", mew=0.4, ms=4, alpha=0.85,
        label="SSA Var(Y)")
ax.plot(T_GRID[::mark_every], cov_XY_ssa[::mark_every], "v",
        color="black", mec="k", mew=0.4, ms=4, alpha=0.85,
        label="SSA Cov(X,Y)")

ax.set_xlabel("time [a.u.]")
ax.set_ylabel("moments")
ax.set_title("Fig. 2 — Time evolution of means and (co)variances "
             "(LNA lines, SSA markers)")
ax.legend(fontsize=8, ncol=2, loc="upper right")
fig.tight_layout()
fig.savefig(FIG / "fig2_moments_vs_time.png", dpi=150)
plt.close(fig)


# ---- Figure 3: 10 sample paths SSA vs OU vs mean ----
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
rng_disp = np.random.default_rng(0)
sel = rng_disp.choice(min(N_SSA, N_OU), size=N_DISPLAY, replace=False)

ax = axes[0]
for k in sel:
    ax.plot(T_GRID, X_ssa[k], color="gold", lw=0.9, alpha=0.7)
    ax.plot(T_GRID, X_ou[k], color="steelblue", lw=0.9, alpha=0.7)
ax.plot(T_GRID, xbar, color="black", lw=2.2, label=r"mean $\bar{x}(t)$")
ax.plot([], [], color="gold", lw=2, label="GSM² SSA")
ax.plot([], [], color="steelblue", lw=2, label="LNA (OU)")
ax.set_title("Sub-lethal X(t)")
ax.set_xlabel("time [a.u.]")
ax.set_ylabel("X")
ax.legend(fontsize=9)

ax = axes[1]
for k in sel:
    ax.plot(T_GRID, Y_ssa[k], color="gold", lw=0.9, alpha=0.7)
    ax.plot(T_GRID, Y_ou[k], color="steelblue", lw=0.9, alpha=0.7)
ax.plot(T_GRID, ybar, color="black", lw=2.2, label=r"mean $\bar{y}(t)$")
ax.plot([], [], color="gold", lw=2, label="GSM² SSA")
ax.plot([], [], color="steelblue", lw=2, label="LNA (OU)")
ax.set_title("Lethal Y(t)")
ax.set_xlabel("time [a.u.]")
ax.set_ylabel("Y")
ax.legend(fontsize=9)

fig.suptitle("Fig. 3 — Sample paths: GSM² SSA vs linear-noise Ornstein–Uhlenbeck",
             fontsize=11)
fig.tight_layout(rect=(0, 0, 1, 0.96))
fig.savefig(FIG / "fig3_sample_paths.png", dpi=150)
plt.close(fig)


# ---- Bonus Figure: Fano factor of lethal lesions vs time (Poisson deviation) ----
fig, ax = plt.subplots(1, 1, figsize=(9, 5))
# Avoid division by zero for very small ybar
mask = ybar > 1e-3
fano_lna = np.where(mask, c_vv / np.where(mask, ybar, 1.0), np.nan)
mask_ssa = mean_Y_ssa > 1e-3
fano_ssa = np.where(mask_ssa, var_Y_ssa / np.where(mask_ssa, mean_Y_ssa, 1.0),
                    np.nan)
ax.plot(T_GRID, fano_lna, color="crimson", lw=2.0,
        label=r"LNA: $c_{vv}/\bar{y}$")
ax.plot(T_GRID, fano_ssa, "o", color="black", ms=3, mfc="white",
        label="SSA: Var(Y)/E[Y]")
ax.axhline(1.0, color="grey", lw=1.2, linestyle="--",
           label="Poisson (Fano = 1)")
ax.set_xlabel("time [a.u.]")
ax.set_ylabel("Fano factor of lethal lesions Y")
ax.set_title("Bonus — Poisson-deviation diagnostic for lethal lesions\n"
             "(Fano < 1 ⇒ sub-Poissonian, the paper's central claim)")
ax.legend(fontsize=9, loc="lower right")
ax.set_ylim(bottom=0.0)
fig.tight_layout()
fig.savefig(FIG / "fig4_fano_factor.png", dpi=150)
plt.close(fig)


print("\nDone.\n")
print(f"  results/     -> {RES}")
print(f"  figures/     -> {FIG}")
print("\nEndpoint (t = %.2f) summary:" % T_GRID[-1])
print(f"  xbar (ODE) = {xbar[-1]:.4f}   <X> (SSA) = {mean_X_ssa[-1]:.4f}")
print(f"  ybar (ODE) = {ybar[-1]:.4f}   <Y> (SSA) = {mean_Y_ssa[-1]:.4f}")
print(f"  c_vv (ODE) = {c_vv[-1]:.4f}   Var(Y) (SSA) = {var_Y_ssa[-1]:.4f}")
print(f"  Fano Y (SSA) = {var_Y_ssa[-1]/mean_Y_ssa[-1]:.4f}"
      f"   (Poisson would be 1.0)")
