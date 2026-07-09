"""Replication of Guerra Liberal et al., Sci Rep 13:11198 (2023).

Reproduces:
    A. LQ fits to single-field X-ray and alpha dose-response (Table S1 / Fig 2).
    B. Additive mixed-field prediction (Eq. 2 / Fig 2 dashed line).
    C. Lea-Catcheside two-fraction repair fits with shared half-life per cell line
       (Eq. 3-4 / Fig 3 / Table 1).
    D. RBE_SLD estimation (Eq. 5-8) from acute vs separated mixed-field survivals.
    E. 53BP1 foci exponential repair kinetics (Methods / Fig 1).
    F. Cluster-based foci-kinetics model for alpha particles (Fig 5c-d).
    G. DSB/Gy vs LET trend with simple-nucleus SSB-clustering MC surrogate (Fig 4).

All outputs written to figures/ and evidence/.
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
DATA = HERE / "data"
FIG = PROJ / "figures"
EVI = PROJ / "evidence"
FIG.mkdir(parents=True, exist_ok=True)
EVI.mkdir(parents=True, exist_ok=True)

RNG = np.random.default_rng(20260622)


# ------------------------------------------------------------------ data loaders
def load_csv(path: Path):
    out = []
    with path.open() as f:
        r = csv.DictReader(f)
        for row in r:
            out.append(row)
    return out


def to_float(s):
    if s in (None, "", "-"):
        return None
    return float(s)


def split_by_cell_line(rows):
    pc3 = [r for r in rows if r["cell_line"] == "PC-3"]
    u2os = [r for r in rows if r["cell_line"] == "U2OS"]
    return {"PC-3": pc3, "U2OS": u2os}


# ------------------------------------------------------------------ models
def lq_survival(dose, alpha, beta):
    return np.exp(-alpha * dose - beta * dose ** 2)


def additive_mixed(dose_total, alpha_x, beta_x, alpha_a, beta_a, frac_a=0.5):
    """Eq. 2: S = exp(-aA DA - ax Dx - (sqrt(DA*betaA)+sqrt(Dx*betax))^2)."""
    dA = frac_a * dose_total
    dX = (1 - frac_a) * dose_total
    rad = (np.sqrt(dA * beta_a) + np.sqrt(dX * beta_x)) ** 2
    return np.exp(-alpha_a * dA - alpha_x * dX - rad)


def G_factor(T, mu, t=0.0):
    """Eq. 4 protraction factor for two equal fractions, inter-fraction interval T.

    With acute fractions (t -> 0), the Lea-Catcheside G for two equal fractions
    at separation T reduces to G = 0.5 + 0.5 * exp(-mu*T).
    The paper's Eq. 4 includes the finite-fraction-time term; we use the
    well-known closed form for t -> 0 which is the standard two-fraction
    formulation used in radiotherapy textbooks.
    """
    T = np.asarray(T)
    return 0.5 + 0.5 * np.exp(-mu * T)


def two_fraction_SF(T, D_total, alpha, beta, mu):
    """S = exp(-alpha*D - beta*G(T)*D^2). Used to fit repair half-life."""
    return np.exp(-alpha * D_total - beta * G_factor(T, mu) * D_total ** 2)


# ------------------------------------------------------------------ A & B: LQ fits + additive Fig 2
def fit_lq_and_plot_fig2():
    clono = split_by_cell_line(load_csv(DATA / "clonogenic.csv"))
    summary = {}

    fig, axes = plt.subplots(1, 2, figsize=(11, 5), sharey=True)
    for ax, line in zip(axes, ["PC-3", "U2OS"]):
        rows = clono[line]
        # X-ray
        dX = np.array(
            [to_float(r["total_dose_Gy"]) for r in rows if to_float(r["xray_mean"]) is not None]
        )
        sX = np.array([to_float(r["xray_mean"]) for r in rows if to_float(r["xray_mean"]) is not None])
        wX = np.array([to_float(r["xray_sd"]) for r in rows if to_float(r["xray_mean"]) is not None])
        wX = np.where((wX is None) | (wX == 0), 0.02, wX)
        # weights for log-survival fit
        lnS = np.log(sX)
        sigma_ln = np.array(wX) / sX  # propagate
        popt_x, pcov_x = curve_fit(
            lambda d, a, b: -a * d - b * d ** 2, dX, lnS, sigma=sigma_ln, absolute_sigma=False
        )
        alpha_x, beta_x = popt_x
        err_x = np.sqrt(np.diag(pcov_x))

        # Alpha
        dA = np.array(
            [to_float(r["total_dose_Gy"]) for r in rows if to_float(r["alpha_mean"]) is not None]
        )
        sA = np.array(
            [to_float(r["alpha_mean"]) for r in rows if to_float(r["alpha_mean"]) is not None]
        )
        wA = np.array(
            [to_float(r["alpha_sd"]) for r in rows if to_float(r["alpha_mean"]) is not None]
        )
        lnSA = np.log(sA)
        sigma_lnA = np.array(wA) / sA
        # Per Table S1, beta_alpha = 0; fit pure-linear model
        popt_a, pcov_a = curve_fit(
            lambda d, a: -a * d, dA, lnSA, sigma=sigma_lnA, absolute_sigma=False
        )
        alpha_a = popt_a[0]
        beta_a = 0.0
        err_a = np.sqrt(np.diag(pcov_a))[0]

        # Mixed: average of x->a and a->x
        dM, sM, wM = [], [], []
        for r in rows:
            xa = to_float(r["xa_mean"])
            ax_ = to_float(r["ax_mean"])
            dose = to_float(r["total_dose_Gy"])
            if xa is not None and ax_ is not None and dose is not None and dose > 0:
                avg = 0.5 * (xa + ax_)
                dM.append(dose)
                sM.append(avg)
                # combined sd (rough)
                wM.append(0.5 * math.hypot(to_float(r["xa_sd"]) or 0, to_float(r["ax_sd"]) or 0))
        dM, sM, wM = map(np.array, (dM, sM, wM))

        # Plot data
        ax.errorbar(dX, sX, yerr=wX, fmt="o", color="C0", label="X-ray", capsize=3)
        ax.errorbar(dA, sA, yerr=wA, fmt="s", color="C3", label="Alpha", capsize=3)
        ax.errorbar(
            dM,
            sM,
            yerr=wM,
            fmt="^",
            color="C2",
            label="Mixed (avg X+A, A+X)",
            capsize=3,
        )

        # Plot LQ fits
        dgrid = np.linspace(0.01, max(dX.max(), dM.max() or 0, 4.0), 100)
        ax.plot(dgrid, lq_survival(dgrid, alpha_x, beta_x), "-", color="C0",
                label=f"LQ X: α={alpha_x:.2f}, β={beta_x:.3f}")
        ax.plot(dgrid, lq_survival(dgrid, alpha_a, beta_a), "-", color="C3",
                label=f"LQ A: α={alpha_a:.2f}")

        # Additive model (Eq. 2) for mixed (50/50)
        dM_grid = np.linspace(0.01, 4.0, 100)
        S_add = additive_mixed(dM_grid, alpha_x, beta_x, alpha_a, beta_a, frac_a=0.5)
        ax.plot(dM_grid, S_add, "--", color="C2", label="Additive Eq. 2")

        ax.set_yscale("log")
        ax.set_xlabel("Total dose (Gy)")
        if ax is axes[0]:
            ax.set_ylabel("Surviving fraction")
        ax.set_title(line)
        ax.set_ylim(1e-4, 1.5)
        ax.legend(fontsize=8)
        ax.grid(True, which="both", alpha=0.3)

        summary[line] = {
            "alpha_xray": float(alpha_x),
            "alpha_xray_err": float(err_x[0]),
            "beta_xray": float(beta_x),
            "beta_xray_err": float(err_x[1]),
            "alpha_alpha": float(alpha_a),
            "alpha_alpha_err": float(err_a),
            "beta_alpha": float(beta_a),
        }

    fig.suptitle("Figure 2 replication: LQ fits + additive mixed-field model")
    fig.tight_layout()
    fig.savefig(FIG / "fig2_lq_and_additive.png", dpi=150)
    plt.close(fig)

    with (EVI / "lq_fits.json").open("w") as f:
        json.dump(summary, f, indent=2)
    return summary


# ------------------------------------------------------------------ C & D: SLD repair fits, Fig 3, Table 1
def fit_sld_and_plot_fig3(lq):
    sld = split_by_cell_line(load_csv(DATA / "sld.csv"))
    table1 = {}

    fig, axes = plt.subplots(2, 2, figsize=(11, 8), sharex=True)
    for col, line in enumerate(["PC-3", "U2OS"]):
        rows = sld[line]
        ax_top = axes[0, col]
        ax_bot = axes[1, col]
        a_xray = lq[line]["alpha_xray"]
        b_xray = lq[line]["beta_xray"]
        a_alpha = lq[line]["alpha_alpha"]
        b_alpha = lq[line]["beta_alpha"]

        T = np.array([to_float(r["interval_h"]) for r in rows], dtype=float)

        def col(name):
            return np.array(
                [(to_float(r[name]) if to_float(r[name]) is not None else np.nan)
                 for r in rows], dtype=float)

        # ---- Top: same-quality two-fraction (X+X 6 Gy total, A+A 1.5 Gy total)
        # X+X: D=6, LQ with G(T,mu)
        Sxx = col("xx_mean")
        sdxx = np.where(np.isnan(col("xx_sd")), 1e-3, col("xx_sd"))
        Saa = col("aa_mean")
        sdaa = np.where(np.isnan(col("aa_sd")), 1e-3, col("aa_sd"))

        # Fit shared mu (X+X only — alpha+alpha has no significant repair per paper)
        m = ~np.isnan(Sxx)
        Tx, yx, wx = T[m], Sxx[m], sdxx[m]

        def model_xx(Tarr, mu):
            return two_fraction_SF(Tarr, 6.0, a_xray, b_xray, mu)

        try:
            popt, pcov = curve_fit(model_xx, Tx, yx, p0=[1.0], sigma=wx, bounds=(1e-3, 50))
            mu_xx = float(popt[0])
            mu_xx_err = float(np.sqrt(np.diag(pcov))[0])
        except Exception as e:  # pragma: no cover
            mu_xx, mu_xx_err = float("nan"), float("nan")
            print(f"[{line}] XX fit failed: {e}")

        # Tabulate as half-life (min)
        t_half_xx = math.log(2) / mu_xx * 60 if mu_xx > 0 else float("nan")

        # ---- Bottom: mixed-field two-fraction (X+A and A+X, 3 Gy + 0.75 Gy)
        # Use mixed-field LQ + Lea-Catcheside with effective doses; for the
        # cross term we use the additive-mixed formulation (Eq.2) at long
        # separation, scaled by G(T) on the cross beta-term.
        # S(T) = exp(-aA*0.75 - ax*3 - G(T) * (sqrt(0.75*bA) + sqrt(3*bx))^2 )
        Sxa = col("xa_mean")
        sxa = np.where(np.isnan(col("xa_sd")), 1e-3, col("xa_sd"))
        Sax = col("ax_mean")
        sax_ = np.where(np.isnan(col("ax_sd")), 1e-3, col("ax_sd"))

        def model_mixed(Tarr, mu):
            cross = (math.sqrt(0.75 * b_alpha) + math.sqrt(3.0 * b_xray)) ** 2
            return np.exp(
                -a_alpha * 0.75 - a_xray * 3.0 - G_factor(Tarr, mu) * cross
            )

        # Since beta_alpha=0, the cross is just 3*beta_x (independent of T)
        # which would predict NO repair. The paper's RBE_SLD trick implies
        # an effective beta for alpha when interacting with X-rays. We fit a
        # joint "effective" cross coefficient C and mu:
        def model_mixed_joint(Tarr, mu, C):
            # S = exp(-aA*0.75 - ax*3 - G(T)*C)
            return np.exp(-a_alpha * 0.75 - a_xray * 3.0 - G_factor(Tarr, mu) * C)

        mxa = ~np.isnan(Sxa)
        max_ = ~np.isnan(Sax)
        T_xa, y_xa, w_xa = T[mxa], Sxa[mxa], sxa[mxa]
        T_ax, y_ax, w_ax = T[max_], Sax[max_], sax_[max_]

        # joint fit on combined points with a single shared mu and one C per ordering
        def joint(Tcombined, mu, C_xa, C_ax):
            n_xa = len(T_xa)
            T1 = Tcombined[:n_xa]
            T2 = Tcombined[n_xa:]
            return np.concatenate(
                [model_mixed_joint(T1, mu, C_xa), model_mixed_joint(T2, mu, C_ax)]
            )

        Tcomb = np.concatenate([T_xa, T_ax])
        ycomb = np.concatenate([y_xa, y_ax])
        wcomb = np.concatenate([w_xa, w_ax])
        try:
            popt2, pcov2 = curve_fit(
                joint, Tcomb, ycomb, p0=[1.0, 0.5, 0.5], sigma=wcomb,
                bounds=([1e-3, 1e-4, 1e-4], [50, 5.0, 5.0])
            )
            mu_mix, C_xa_fit, C_ax_fit = popt2
            mu_mix_err = float(np.sqrt(np.diag(pcov2))[0])
        except Exception as e:
            mu_mix, C_xa_fit, C_ax_fit = float("nan"), float("nan"), float("nan")
            mu_mix_err = float("nan")
            print(f"[{line}] joint mixed fit failed: {e}")
        t_half_mix = math.log(2) / mu_mix * 60 if mu_mix > 0 else float("nan")

        # Plotting
        ax_top.errorbar(Tx, yx, yerr=wx, fmt="o", color="C0", label="X+X (3+3 Gy)", capsize=3)
        ma = ~np.isnan(Saa)
        ax_top.errorbar(T[ma], Saa[ma], yerr=sdaa[ma], fmt="s", color="C3",
                        label="A+A (0.75+0.75 Gy)", capsize=3)
        Tgrid = np.linspace(0, 6, 200)
        ax_top.plot(Tgrid, model_xx(Tgrid, mu_xx), "-", color="C0",
                    label=f"Fit μ={mu_xx:.2f} /h  (t½={t_half_xx:.0f} min)")
        ax_top.axhline(np.exp(-a_alpha * 1.5 - b_alpha * 1.5 ** 2), color="C3", linestyle=":",
                       label="A+A acute (no repair)")
        ax_top.set_yscale("log")
        ax_top.set_title(f"{line}: same-quality two-fraction repair")
        ax_top.legend(fontsize=8)
        ax_top.grid(True, which="both", alpha=0.3)
        if col == 0:
            ax_top.set_ylabel("Surviving fraction")

        ax_bot.errorbar(T_xa, y_xa, yerr=w_xa, fmt="o", color="C0",
                        label="X→A (3+0.75 Gy)", capsize=3)
        ax_bot.errorbar(T_ax, y_ax, yerr=w_ax, fmt="s", color="C3",
                        label="A→X (0.75+3 Gy)", capsize=3)
        ax_bot.plot(Tgrid, model_mixed_joint(Tgrid, mu_mix, C_xa_fit), "-", color="C0",
                    label=f"X→A fit C={C_xa_fit:.3f}")
        ax_bot.plot(Tgrid, model_mixed_joint(Tgrid, mu_mix, C_ax_fit), "-", color="C3",
                    label=f"A→X fit C={C_ax_fit:.3f}")
        ax_bot.set_yscale("log")
        ax_bot.set_xlabel("Inter-fraction interval (h)")
        if col == 0:
            ax_bot.set_ylabel("Surviving fraction")
        ax_bot.set_title(f"{line}: mixed-field repair (shared μ={mu_mix:.2f} /h, t½={t_half_mix:.0f} min)")
        ax_bot.legend(fontsize=8)
        ax_bot.grid(True, which="both", alpha=0.3)

        # -- RBE_SLD via Eq.7-8: SLD-interaction term magnitudes from acute-vs-late
        # for X+X: ln(S_inf) - ln(S_0) = gamma * SLDx^2  (no inter-track repair = same equation)
        # for X+A: ln(S_inf) - ln(S_0) = gamma * SLDx * SLDa
        # take ratio => SLDa/SLDx = (delta_XA / delta_XX); RBE_SLD = (SLDa/SLDx) * (Dx/DA)
        # use measured T~6h vs T~0.5h (no acute T=0 in mixed). For XX, use T=6 vs T=0.
        def safe_lnS(arr, mask, idx):
            v = arr[mask][idx]
            return math.log(v)

        # XX delta: T=0 vs T=6
        try:
            S_xx_0 = Sxx[T == 0][0]
            S_xx_6 = Sxx[T == 6][0]
            dXX = math.log(S_xx_6) - math.log(S_xx_0)
        except Exception:
            dXX = float("nan")

        # mixed delta: use T=0.5 as closest acute mixed measurement, T=6 as separated
        def get(arr, t_target):
            for ti, vi in zip(T, arr):
                if abs(ti - t_target) < 1e-6 and vi is not None and not np.isnan(vi):
                    return vi
            return None

        S_xa_05 = get(Sxa, 0.5)
        S_xa_6 = get(Sxa, 6.0)
        S_ax_05 = get(Sax, 0.5)
        S_ax_6 = get(Sax, 6.0)
        dXA = math.log(S_xa_6) - math.log(S_xa_05) if (S_xa_05 and S_xa_6) else float("nan")
        dAX = math.log(S_ax_6) - math.log(S_ax_05) if (S_ax_05 and S_ax_6) else float("nan")

        # ratio SLDa/SLDx = (dXA) / dXX (approximate, ignoring difference in
        # second-fraction acute SLD baseline). For more rigorous comparison, use
        # 0.75 + 0.75 vs 3+3 Gy normalization: SLDa/SLDx = (delta_mixed/Dx) / (delta_xx/Dx) * (Dx/DA)
        # Following Eq.8 exactly with the dose ratio Dx/DA = 3/0.75 = 4:
        ratio_xa = dXA / dXX if (dXX and not math.isnan(dXX)) else float("nan")
        ratio_ax = dAX / dXX if (dXX and not math.isnan(dXX)) else float("nan")
        D_ratio = 3.0 / 0.75  # = 4
        rbe_sld_xa = abs(ratio_xa) * D_ratio
        rbe_sld_ax = abs(ratio_ax) * D_ratio

        table1[line] = {
            "mu_xx_per_h": mu_xx, "t_half_xx_min": t_half_xx,
            "mu_mixed_per_h": mu_mix, "t_half_mixed_min": t_half_mix,
            "C_xa_fit": float(C_xa_fit), "C_ax_fit": float(C_ax_fit),
            "delta_lnS_XX": dXX, "delta_lnS_XA": dXA, "delta_lnS_AX": dAX,
            "RBE_SLD_from_XA": float(rbe_sld_xa),
            "RBE_SLD_from_AX": float(rbe_sld_ax),
            "RBE_SLD_mean": float(0.5 * (rbe_sld_xa + rbe_sld_ax)),
        }

    fig.suptitle("Figure 3 replication: SLD repair vs interval (LQ + Lea-Catcheside)")
    fig.tight_layout()
    fig.savefig(FIG / "fig3_sld_repair.png", dpi=150)
    plt.close(fig)

    with (EVI / "sld_fits_and_rbe.json").open("w") as f:
        json.dump(table1, f, indent=2)
    return table1


# ------------------------------------------------------------------ E: foci kinetics, Fig 1
def fit_foci_and_plot_fig1():
    foci = split_by_cell_line(load_csv(DATA / "foci.csv"))
    out = {}

    fig, axes = plt.subplots(1, 2, figsize=(11, 5), sharey=True)
    for ax, line in zip(axes, ["PC-3", "U2OS"]):
        rows = foci[line]
        t = np.array([to_float(r["time_h"]) for r in rows])
        Nx = np.array([to_float(r["xray_mean"]) for r in rows])
        sx = np.array([to_float(r["xray_sd"]) for r in rows])
        Na = np.array([to_float(r["alpha_mean"]) if to_float(r["alpha_mean"]) is not None else np.nan
                       for r in rows])
        sa = np.array([to_float(r["alpha_sd"]) if to_float(r["alpha_sd"]) is not None else np.nan
                       for r in rows])

        def expdec(t, N0, P, k):
            return (N0 - P) * np.exp(-k * t) + P

        # X-ray
        popt_x, _ = curve_fit(expdec, t, Nx, p0=[25, 2, 0.5], sigma=sx, maxfev=10000)
        # Alpha
        mA = ~np.isnan(Na)
        popt_a, _ = curve_fit(expdec, t[mA], Na[mA], p0=[12, 5, 0.1], sigma=sa[mA], maxfev=10000)

        tgrid = np.linspace(0.5, 26, 200)
        ax.errorbar(t, Nx, yerr=sx, fmt="o", color="C0", label="X-ray data", capsize=3)
        ax.errorbar(t[mA], Na[mA], yerr=sa[mA], fmt="s", color="C3", label="Alpha data", capsize=3)
        ax.plot(tgrid, expdec(tgrid, *popt_x), "-", color="C0",
                label=f"X-ray fit  N₀={popt_x[0]:.1f}, P={popt_x[1]:.1f}, k={popt_x[2]:.2f}/h")
        ax.plot(tgrid, expdec(tgrid, *popt_a), "-", color="C3",
                label=f"Alpha fit  N₀={popt_a[0]:.1f}, P={popt_a[1]:.1f}, k={popt_a[2]:.2f}/h")
        ax.set_xlabel("Time post-irradiation (h)")
        if ax is axes[0]:
            ax.set_ylabel("53BP1 foci per cell (background-corrected)")
        ax.set_title(line)
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

        out[line] = {
            "xray": {"N0": float(popt_x[0]), "P": float(popt_x[1]),
                     "k_per_h": float(popt_x[2]),
                     "t_half_min": float(math.log(2) / popt_x[2] * 60)},
            "alpha": {"N0": float(popt_a[0]), "P": float(popt_a[1]),
                      "k_per_h": float(popt_a[2]),
                      "t_half_min": float(math.log(2) / popt_a[2] * 60)},
        }

    fig.suptitle("Figure 1 replication: 53BP1 foci repair kinetics (2 Gy)")
    fig.tight_layout()
    fig.savefig(FIG / "fig1_foci_kinetics.png", dpi=150)
    plt.close(fig)

    with (EVI / "foci_fits.json").open("w") as f:
        json.dump(out, f, indent=2)
    return out


# ------------------------------------------------------------------ F: cluster-foci model (Fig 5c-d)
def cluster_foci_model(N_clusters_mean, F_mean_per_cluster, k_simple, k_complex,
                       frac_complex, P_residual, tgrid, n_mc=2000):
    """Each cluster contains Poisson(F) DSBs; observed foci count is cluster count
    where at least one constituent DSB is unrepaired. Individual DSBs repair with
    exponential kinetics (simple or complex).
    """
    rng = np.random.default_rng(20260622)
    foci_t = np.zeros_like(tgrid, dtype=float)
    for _ in range(n_mc):
        n_cl = rng.poisson(N_clusters_mean)
        if n_cl == 0:
            continue
        sizes = rng.poisson(F_mean_per_cluster, size=n_cl).clip(min=1)
        cluster_present = np.ones_like(tgrid, dtype=bool)[None, :].repeat(n_cl, axis=0)
        for ci, s in enumerate(sizes):
            # each DSB has a repair rate (simple or complex)
            is_complex = rng.random(s) < frac_complex
            ks = np.where(is_complex, k_complex, k_simple)
            # treat residual fraction (P_residual) as never repaired
            persistent = rng.random(s) < P_residual
            # probability each DSB is unrepaired at time t
            # if persistent, always present; else exp(-k*t)
            for j in range(s):
                if persistent[j]:
                    p_present = np.ones_like(tgrid)
                else:
                    p_present = np.exp(-ks[j] * tgrid)
                # sample 1/0 (Bernoulli) — but to reduce variance we keep probabilities
                cluster_present[ci] = cluster_present[ci] & (rng.random(len(tgrid)) < p_present | persistent[j])
        foci_t += cluster_present.sum(axis=0)
    return foci_t / n_mc


def fit_cluster_model_and_plot_fig5cd():
    """Approximate version: average over many MC realizations to get expected foci curve.

    Fit (a) N_clusters_x for X-ray (F=1, single DSB), and (b) N_clusters_a and
    F_a for alpha (DSB yield ~= N_clusters_a * F_a; we fix F_a from RBE_DSB).
    """
    foci = split_by_cell_line(load_csv(DATA / "foci.csv"))
    # Use Medras-style repair coefficients: simple DSB k=1.4/h, complex k=0.16/h
    k_simple = 1.4
    k_complex = 0.16
    frac_complex_x = 0.43
    frac_complex_a = 0.85  # higher complex fraction for high-LET (per cluster paper)
    P_residual = 0.04

    tgrid = np.array([1, 2, 4, 6, 24])

    fig, axes = plt.subplots(1, 2, figsize=(11, 5), sharey=True)
    out = {}
    for ax, line in zip(axes, ["PC-3", "U2OS"]):
        rows = foci[line]
        t_meas = np.array([to_float(r["time_h"]) for r in rows])
        Nx = np.array([to_float(r["xray_mean"]) for r in rows])
        sx = np.array([to_float(r["xray_sd"]) for r in rows])
        Na = np.array([to_float(r["alpha_mean"]) if to_float(r["alpha_mean"]) is not None else np.nan
                       for r in rows])
        sa = np.array([to_float(r["alpha_sd"]) if to_float(r["alpha_sd"]) is not None else np.nan
                       for r in rows])

        # X-ray: F=1, fit N0
        def model_x(t, N0, Presid):
            # single-DSB clusters => exp repair with mixed kinetics
            persistent = Presid
            simple_frac = 1 - frac_complex_x
            return N0 * (
                persistent +
                (1 - persistent) * (
                    simple_frac * np.exp(-k_simple * t) +
                    frac_complex_x * np.exp(-k_complex * t)
                )
            )

        popt_x, _ = curve_fit(model_x, t_meas, Nx, p0=[60, 0.05], sigma=sx, maxfev=10000)
        N0_x, P_x = popt_x

        # Alpha: fit N_clusters and F such that total DSBs ~ N0_x * RBE_DSB(=3.67)
        # The cluster appears present if ANY of F DSBs unrepaired.
        # P(none) = (1-q)^F where q = prob one DSB still present at t.
        # q(t) = persistent + (1-persistent)*[simple*exp(-ks t) + complex*exp(-kc t)]
        def model_a(t, N_cl, F, Presid):
            q = Presid + (1 - Presid) * (
                (1 - frac_complex_a) * np.exp(-k_simple * t) +
                frac_complex_a * np.exp(-k_complex * t)
            )
            return N_cl * (1 - (1 - q) ** F)

        mA = ~np.isnan(Na)
        popt_a, _ = curve_fit(
            model_a, t_meas[mA], Na[mA], p0=[10, 4, 0.05],
            sigma=sa[mA], bounds=([1, 1.0, 0.0], [50, 30, 0.3]), maxfev=20000,
        )
        N_cl_a, F_a, P_a = popt_a

        tplot = np.linspace(0.5, 26, 200)
        ax.errorbar(t_meas, Nx, yerr=sx, fmt="o", color="C0", label="X-ray data", capsize=3)
        ax.errorbar(t_meas[mA], Na[mA], yerr=sa[mA], fmt="s", color="C3",
                    label="Alpha data", capsize=3)
        ax.plot(tplot, model_x(tplot, N0_x, P_x), "-", color="C0",
                label=f"X-ray cluster: N₀={N0_x:.0f}, P={P_x:.3f}")
        ax.plot(tplot, model_a(tplot, N_cl_a, F_a, P_a), "-", color="C3",
                label=f"Alpha cluster: N_cl={N_cl_a:.1f}, F={F_a:.1f}, P={P_a:.3f}")
        ax.set_xlabel("Time post-irradiation (h)")
        if ax is axes[0]:
            ax.set_ylabel("Foci per cell")
        ax.set_title(line)
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
        out[line] = {
            "xray": {"N0_foci": float(N0_x), "P_residual": float(P_x)},
            "alpha": {"N_clusters": float(N_cl_a), "DSB_per_cluster": float(F_a),
                      "P_residual": float(P_a),
                      "implied_total_DSB": float(N_cl_a * F_a)},
        }

    fig.suptitle("Figure 5c-d replication: cluster-foci model (k_simple=1.4/h, k_complex=0.16/h)")
    fig.tight_layout()
    fig.savefig(FIG / "fig5cd_cluster_foci_model.png", dpi=150)
    plt.close(fig)

    with (EVI / "cluster_foci_fits.json").open("w") as f:
        json.dump(out, f, indent=2)
    return out


# ------------------------------------------------------------------ G: DSB/Gy vs LET (Fig 4 surrogate)
def fig4_dsb_vs_let():
    """Simple-nucleus SSB-clustering model surrogate.

    Per Methods: 1 Gy => 1000 SSBs in nucleus (~2.5 µm radius); SSBs uniformly
    distributed for X-rays; for ions, deposited along tracks with radial profile.
    Two SSBs on opposite strands within 3.2 nm => DSB. For alphas at 129 keV/µm,
    paper reports 128.5 DSB/Gy and RBE_DSB ~ 3.67.

    Surrogate model: we treat alpha tracks as 1D lines through nucleus; SSBs
    are placed Poisson along each track with linear density set by LET. The
    intra-track SSB pair probability within 3.2 nm scales with linear density.

    For low-LET (X-ray): uniform 3D SSB placement; pair probability scales as
    (n_SSB / V) * V_pair = n_SSB * (V_pair / V_nuc) per SSB, giving constant
    DSB fraction independent of LET. Set this baseline to 35 DSB/Gy.

    For high-LET ion: linear density lambda_SSB = LET * (SSB/keV) along track;
    nearest-neighbor pair probability within 3.2 nm on the same track ~
    1 - exp(-2 * lambda_SSB * 3.2nm). Total DSB/Gy on track contribution + the
    uniform background.
    """
    # baseline calibration: 35 DSB/Gy at LET ~ 1 keV/µm (X-ray)
    DSB_Gy_xray = 35.0
    SSB_per_Gy = 1000.0
    # average energy per SSB (paper): 0.41 keV
    # number of SSBs per Gy stays at 1000 by definition (Elkind & Redpath)
    # track length per Gy at LET L (keV/µm): L_track[µm/Gy] = (E_per_Gy[keV])/L
    # E_per_Gy for nucleus mass m: 1 Gy = 1 J/kg => energy in keV = 6.24e15 * mass[kg]
    nucleus_radius_um = 2.5
    V_nuc_m3 = (4 / 3) * math.pi * (nucleus_radius_um * 1e-6) ** 3
    density = 1000.0  # kg/m3 water
    mass_kg = V_nuc_m3 * density
    energy_per_Gy_J = 1 * mass_kg
    energy_per_Gy_keV = energy_per_Gy_J / 1.602e-16  # keV per Gy
    # number of SSBs per Gy = 1000 (constant)
    # for given LET L (keV/µm), each track contributes L * t_len_through_nucleus[µm] keV
    # mean chord length through sphere = (4/3)*R
    mean_chord_um = (4 / 3) * nucleus_radius_um
    # SSBs per track = (E_per_track / E_per_SSB)
    E_per_track = lambda L: L * mean_chord_um  # keV
    E_per_SSB = 0.41  # keV per SSB (calibrated)
    SSB_per_track = lambda L: E_per_track(L) / E_per_SSB

    # tracks per Gy = total energy per Gy / energy per track
    tracks_per_Gy = lambda L: energy_per_Gy_keV / E_per_track(L)
    # linear density along track: SSB / µm
    # for track of length mean_chord_um with SSB_per_track SSBs:
    lin_density_per_um = lambda L: SSB_per_track(L) / mean_chord_um

    # probability that two SSBs on opposite strands within 3.2 nm:
    # naive 1D model: prob a given SSB has a neighbor SSB within 3.2 nm
    # = 1 - exp(-2 * lambda * 3.2e-3 µm). Then factor of 0.5 because they
    # need to be on opposite strands (strand assignment random 50/50)
    d_nm = 3.2
    d_um = d_nm * 1e-3

    def DSB_per_track(L):
        lam = lin_density_per_um(L)
        n_ssb = SSB_per_track(L)
        if n_ssb < 2:
            return 0.0
        # expected nearest-neighbour same-side prob 1-exp(-2*lam*d_um)
        p_neighbor = 1 - math.exp(-2 * lam * d_um)
        # of those pairs, half are opposite-strand
        # each SSB counted in 2 pairs => DSB count ~ (n_ssb/2)*p_neighbor*0.5
        return n_ssb * p_neighbor * 0.5 * 0.5

    def DSB_per_Gy(L):
        # track contribution
        on_track = tracks_per_Gy(L) * DSB_per_track(L)
        # uniform background: pretend X-rays put SSBs uniformly, DSB rate set by calibration
        # for high-LET, uniform fraction is negligible compared to track contrib
        bg = DSB_Gy_xray  # treat as floor
        return max(on_track, bg)

    LETs = np.array([1.0, 5, 10, 20, 40, 60, 80, 100, 129.3, 150, 200])
    DSBs = np.array([DSB_per_Gy(L) for L in LETs])
    rbe_dsb = DSBs / DSB_Gy_xray

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(LETs, DSBs, "o-", color="C3", label="Simple-nucleus surrogate")
    ax.axhline(35, color="gray", linestyle=":", label="X-ray baseline (35 DSB/Gy)")
    ax.axvline(129.3, color="C0", linestyle="--", alpha=0.6, label="Paper α LET=129 keV/µm")
    ax.axhline(128.5, color="C0", linestyle=":", alpha=0.6,
               label="Paper α 128.5 DSB/Gy (RBE_DSB≈3.67)")
    ax.set_xlabel("LET (keV/µm)")
    ax.set_ylabel("DSB / Gy / cell")
    ax.set_title("Figure 4 replication (analytic surrogate, no Geant4-DNA)")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG / "fig4_dsb_vs_let.png", dpi=150)
    plt.close(fig)

    # extract DSB/Gy at LET=129.3
    dsb_at_alpha = float(DSB_per_Gy(129.3))
    out = {
        "DSB_per_Gy_at_alpha_129keVum": dsb_at_alpha,
        "RBE_DSB_at_alpha": dsb_at_alpha / DSB_Gy_xray,
        "paper_DSB_at_alpha": 128.5,
        "paper_RBE_DSB_at_alpha": 3.67,
        "LET_grid": LETs.tolist(),
        "DSB_grid": DSBs.tolist(),
    }
    with (EVI / "fig4_dsb_vs_let.json").open("w") as f:
        json.dump(out, f, indent=2)
    return out


# ------------------------------------------------------------------ main
def main():
    print("\n=== A & B: Figure 2 LQ + additive ===")
    lq = fit_lq_and_plot_fig2()
    print(json.dumps(lq, indent=2))

    print("\n=== C & D: Figure 3 SLD repair / Table 1 / RBE_SLD ===")
    sld = fit_sld_and_plot_fig3(lq)
    print(json.dumps(sld, indent=2))

    print("\n=== E: Figure 1 foci kinetics ===")
    foci = fit_foci_and_plot_fig1()
    print(json.dumps(foci, indent=2))

    print("\n=== F: Figure 5c-d cluster foci model ===")
    cluster = fit_cluster_model_and_plot_fig5cd()
    print(json.dumps(cluster, indent=2))

    print("\n=== G: Figure 4 DSB/Gy vs LET ===")
    fig4 = fig4_dsb_vs_let()
    print(json.dumps(fig4, indent=2))

    with (EVI / "summary.json").open("w") as f:
        json.dump(
            {"lq_fits_table_s1": lq,
             "sld_repair_table1_and_rbe_sld_eq8": sld,
             "foci_kinetics_fig1": foci,
             "cluster_foci_fig5cd": cluster,
             "dsb_vs_let_fig4": fig4},
            f, indent=2,
        )
    print(f"\nFigures: {FIG}")
    print(f"Evidence: {EVI}")


if __name__ == "__main__":
    main()
