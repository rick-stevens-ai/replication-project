"""
Replication script for Friedrich/Durante/Scholz 2012 (GLOBLE).
Generates the figures and quantitative checks reported in REPORT.md.
"""

from __future__ import annotations
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from globle_model import (
    GLOBLEParams, ALPHA_DSB_DEFAULT, N_L_DEFAULT,
    hit_domains, survival, neg_log_survival,
    lq_from_globle, globle_from_lq, lq_curve,
    high_dose_intermediate_slope, saturation_value,
)

HERE      = os.path.dirname(os.path.abspath(__file__))
ROOT      = os.path.dirname(HERE)
FIG_DIR   = os.path.join(ROOT, "figures")
RES_DIR   = os.path.join(ROOT, "results")
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(RES_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Figure 1 — Two-class damage decomposition (n_i and n_c vs dose)
# ---------------------------------------------------------------------------
def fig_two_class_damage():
    D = np.linspace(0, 200, 401)
    p = GLOBLEParams(eps_i=0.005, eps_c=0.4)
    n_i, n_c = hit_domains(D, p)
    n_T = n_i + n_c

    fig, ax = plt.subplots(figsize=(6, 4.4))
    ax.plot(D, n_i, label=r"$n_i$ : isolated (1 DSB / loop)")
    ax.plot(D, n_c, label=r"$n_c$ : clustered ($\geq 2$ DSB / loop)")
    ax.plot(D, n_T, "k--", label=r"$n_T = n_i + n_c$ : hit loops")
    ax.axhline(p.n_l, color="grey", ls=":", lw=1, label=f"$N_L$={p.n_l}")
    ax.set_xlabel("Dose D  (Gy)")
    ax.set_ylabel("Mean number of loops")
    ax.set_title("GLOBLE damage classes vs dose\n"
                 r"$\alpha_{DSB}=30$ DSB/Gy, $N_L=3000$ (2 Mbp loops)")
    ax.legend()
    ax.grid(alpha=0.3)
    out = os.path.join(FIG_DIR, "fig1_damage_classes.png")
    fig.tight_layout(); fig.savefig(out, dpi=140); plt.close(fig)
    return out


# ---------------------------------------------------------------------------
# Figure 2 — Survival curves: GLOBLE vs LQ for several cell-line-like ε pairs
# ---------------------------------------------------------------------------
def fig_survival_vs_lq():
    """
    Three (ε_i, ε_c) sets chosen to span sensitive → resistant cell behaviour.
    For each we plot GLOBLE S(D) (solid) and the corresponding LQ extrapolation
    (dashed) using α, β derived from eq. (8)-(9).
    """
    presets = {
        "Sensitive (α≈0.45, β≈0.06)":
            GLOBLEParams(eps_i=0.015, eps_c=0.45),
        "Intermediate (α≈0.15, β≈0.06)":
            GLOBLEParams(eps_i=0.005, eps_c=0.40),
        "Resistant (α≈0.05, β≈0.03)":
            GLOBLEParams(eps_i=0.0017, eps_c=0.20),
    }
    D = np.linspace(0, 20, 401)

    fig, ax = plt.subplots(figsize=(6.5, 5))
    for label, p in presets.items():
        a, b = lq_from_globle(p)
        S_globle = survival(D, p)
        S_lq     = lq_curve(D, a, b)
        line, = ax.semilogy(D, S_globle, label=f"{label}: GLOBLE")
        ax.semilogy(D, S_lq, "--", color=line.get_color(),
                    label=f"   LQ (α={a:.3f}, β={b:.3f})")
    ax.set_xlabel("Dose D  (Gy)")
    ax.set_ylabel("Surviving fraction  S")
    ax.set_title("GLOBLE vs equivalent LQ extrapolation\n"
                 "(low-D agreement, transition to ~linear at high D)")
    ax.set_ylim(1e-6, 1.2)
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, which="both")
    out = os.path.join(FIG_DIR, "fig2_survival_vs_lq.png")
    fig.tight_layout(); fig.savefig(out, dpi=140); plt.close(fig)
    return out


# ---------------------------------------------------------------------------
# Figure 3 — High-dose linear transition (key 2012 claim)
# ---------------------------------------------------------------------------
def fig_high_dose_linear():
    """
    Plot -ln S(D) on linear-D axes for a broad dose range and overlay the
    asymptotic linear tangent at high dose, illustrating the 'linear at
    high dose' claim from the 2012 abstract.
    """
    p = GLOBLEParams(eps_i=0.005, eps_c=0.40)
    D = np.linspace(0, 50, 501)
    nlnS = neg_log_survival(D, p)
    # Local linear fit in the intermediate regime [15, 40] Gy where the
    # curve is approximately linear (transition zone of Friedrich 2012):
    mask = (D >= 15) & (D <= 40)
    slope, intercept = np.polyfit(D[mask], nlnS[mask], 1)
    a_lq, b_lq = lq_from_globle(p)

    fig, ax = plt.subplots(figsize=(6, 4.4))
    ax.plot(D, nlnS, label=r"GLOBLE $-\ln S(D)$")
    ax.plot(D, a_lq * D + b_lq * D**2, "--",
            label=fr"LQ:  $\alpha D + \beta D^2$  (α={a_lq:.3f}, β={b_lq:.3f})")
    ax.plot(D, slope * D + intercept, ":k",
            label=f"high-D linear tangent: slope={slope:.3f}/Gy")
    ax.set_xlabel("Dose D  (Gy)")
    ax.set_ylabel(r"$-\ln S(D)$")
    ax.set_title("Low-D quadratic → high-D linear behaviour\n"
                 "(qualitative claim of Friedrich 2012 abstract)")
    ax.legend(fontsize=9); ax.grid(alpha=0.3)
    out = os.path.join(FIG_DIR, "fig3_lowD_quadratic_highD_linear.png")
    fig.tight_layout(); fig.savefig(out, dpi=140); plt.close(fig)
    return out, slope, intercept


# ---------------------------------------------------------------------------
# Figure 4 — β–α anticorrelation predicted by GLOBLE
# ---------------------------------------------------------------------------
def fig_alpha_beta_anticorrelation():
    """
    GLOBLE-style prediction tested two ways:

      (A) UNCONSTRAINED scan: sample ε_i and ε_c independently across the
          working ranges (ε_i ∈ [1e-4, 3e-2], ε_c ∈ [0.05, 0.6]) and look
          at the induced (α, β) cloud.  Because α is set by ε_i alone and
          β is dominated by ε_c·α²_DSB / (2 N_L), the two are nearly
          independent in this regime and the cloud shows no structural
          anticorrelation by itself.

      (B) FIXED-ε_c slice: hold the clustered-lethality ε_c at typical
          values (0.2, 0.4, 0.6) and sweep ε_i. From eq.9 with constant
          ε_c:
               β = (ε_c/2 - ε_i) · α_DSB² / N_L
          i.e.  β = const − (α_DSB / N_L) · α
          → perfect linear anticorrelation between α and β at fixed ε_c.
          This is the *mechanism* by which GLOBLE produces the empirical
          β-vs-α anticorrelation Friedrich 2012 reports across 150+ cell
          lines: differences between cell lines that share a similar
          repair-fidelity for clustered DSBs but differ in handling of
          isolated DSBs trace out an anticorrelated line in (α, β) space.
    """
    rng = np.random.default_rng(20260621)
    n = 600
    eps_i_u = 10 ** rng.uniform(-4, np.log10(3e-2), n)
    eps_c_u = rng.uniform(0.05, 0.6, n)
    a_u = np.empty(n); b_u = np.empty(n)
    for k in range(n):
        a_u[k], b_u[k] = lq_from_globle(
            GLOBLEParams(eps_i=eps_i_u[k], eps_c=eps_c_u[k]))
    keep_u    = b_u >= 0
    a_u, b_u  = a_u[keep_u], b_u[keep_u]
    eps_c_u_k = eps_c_u[keep_u]
    r_unconstrained = float(np.corrcoef(a_u, b_u)[0, 1])

    # Fixed-ε_c slices
    eps_c_values = [0.20, 0.40, 0.60]
    eps_i_grid   = np.linspace(1e-4, 2e-2, 200)
    slices = []
    r_fixed = {}
    for ec in eps_c_values:
        a_s = np.empty_like(eps_i_grid); b_s = np.empty_like(eps_i_grid)
        for k, ei in enumerate(eps_i_grid):
            a_s[k], b_s[k] = lq_from_globle(
                GLOBLEParams(eps_i=ei, eps_c=ec))
        m = b_s >= 0
        slices.append((ec, a_s[m], b_s[m]))
        r_fixed[ec] = float(np.corrcoef(a_s[m], b_s[m])[0, 1])

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.4))

    ax = axes[0]
    sc = ax.scatter(a_u, b_u, s=8, alpha=0.55, c=np.log10(eps_c_u_k),
                    cmap="viridis")
    cb = plt.colorbar(sc, ax=ax); cb.set_label(r"$\log_{10}\,\varepsilon_c$")
    ax.set_xlabel(r"$\alpha$  (Gy$^{-1}$)")
    ax.set_ylabel(r"$\beta$  (Gy$^{-2}$)")
    ax.set_title("(A) Unconstrained random scan\n"
                 fr"Pearson r($\alpha$, $\beta$) = {r_unconstrained:+.3f}")
    ax.grid(alpha=0.3)

    ax = axes[1]
    for ec, a_s, b_s in slices:
        ax.plot(a_s, b_s, label=fr"$\varepsilon_c$={ec},  r={r_fixed[ec]:+.3f}")
    ax.set_xlabel(r"$\alpha$  (Gy$^{-1}$)")
    ax.set_ylabel(r"$\beta$  (Gy$^{-2}$)")
    ax.set_title("(B) Fixed-$\\varepsilon_c$ slice\n(GLOBLE predicts "
                 r"$\beta = $ const $- (\alpha_{DSB}/N_L)\,\alpha$)")
    ax.legend(fontsize=9); ax.grid(alpha=0.3)

    out = os.path.join(FIG_DIR, "fig4_alpha_beta_cloud.png")
    fig.tight_layout(); fig.savefig(out, dpi=140); plt.close(fig)
    return out, r_unconstrained, r_fixed


# ---------------------------------------------------------------------------
# Monte-Carlo independent check of n_i/n_c
# ---------------------------------------------------------------------------
def mc_check(p: GLOBLEParams, doses: np.ndarray, n_nuclei: int = 5000,
             seed: int = 20260621) -> dict:
    """
    Independent stochastic simulation: for each dose draw the total number
    of induced DSBs ~ Poisson(α_DSB · D), distribute them uniformly over
    N_L loops, count loops with exactly 1 DSB (isolated) vs >=2 (clustered),
    and compare to the analytic n_i, n_c.
    """
    rng = np.random.default_rng(seed)
    ni_mc = np.zeros_like(doses, float)
    nc_mc = np.zeros_like(doses, float)
    for i, D in enumerate(doses):
        mean_dsb = p.alpha_dsb * D
        for _ in range(n_nuclei):
            n_dsb = rng.poisson(mean_dsb)
            if n_dsb == 0: continue
            loops = rng.integers(0, p.n_l, size=n_dsb)
            counts = np.bincount(loops, minlength=p.n_l)
            ni_mc[i] += (counts == 1).sum()
            nc_mc[i] += (counts >= 2).sum()
    ni_mc /= n_nuclei
    nc_mc /= n_nuclei
    ni_an, nc_an = hit_domains(doses, p)
    return {"doses": doses.tolist(),
            "n_i_MC": ni_mc.tolist(),  "n_i_analytic": ni_an.tolist(),
            "n_c_MC": nc_mc.tolist(),  "n_c_analytic": nc_an.tolist()}


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
def main():
    out = {}

    print("[1] Generating Fig 1 (damage classes)…")
    out["fig1"] = fig_two_class_damage()

    print("[2] Generating Fig 2 (survival vs LQ)…")
    out["fig2"] = fig_survival_vs_lq()

    print("[3] Generating Fig 3 (low-D quadratic, high-D linear)…")
    f3, hd_slope, hd_intercept = fig_high_dose_linear()
    out["fig3"]                                = f3
    out["intermediate_linear_slope_15_40Gy"]   = hd_slope
    out["intermediate_linear_intercept"]       = hd_intercept
    p_demo                                      = GLOBLEParams(eps_i=0.005, eps_c=0.40)
    out["saturation_neg_lnS_infinity"]         = saturation_value(p_demo)

    print("[4] Generating Fig 4 (α–β cloud)…")
    f4, r_uncon, r_fixed = fig_alpha_beta_anticorrelation()
    out["fig4"]                                  = f4
    out["pearson_alpha_beta_unconstrained"]      = r_uncon
    out["pearson_alpha_beta_fixed_eps_c"]        = r_fixed

    print("[5] Monte-Carlo cross-check of n_i, n_c …")
    p_mc = GLOBLEParams(eps_i=0.005, eps_c=0.40)
    mc   = mc_check(p_mc, np.array([0.5, 1, 2, 5, 10, 20]), n_nuclei=5000)
    out["mc_check"] = mc
    # max relative residual
    def relerr(a, b):
        a = np.asarray(a); b = np.asarray(b)
        m = b > 1e-6
        return float(np.max(np.abs(a[m] - b[m]) / b[m]))
    out["mc_max_relerr_ni"] = relerr(mc["n_i_MC"], mc["n_i_analytic"])
    out["mc_max_relerr_nc"] = relerr(mc["n_c_MC"], mc["n_c_analytic"])

    print("[6] LQ inversion round-trip check …")
    p0  = GLOBLEParams(eps_i=0.005, eps_c=0.40)
    a, b = lq_from_globle(p0)
    p1   = globle_from_lq(a, b)
    out["round_trip"] = {
        "input_eps_i": p0.eps_i, "input_eps_c": p0.eps_c,
        "lq_alpha":   a,         "lq_beta":     b,
        "recov_eps_i": p1.eps_i, "recov_eps_c": p1.eps_c,
    }

    # Save
    with open(os.path.join(RES_DIR, "replication_results.json"), "w") as fh:
        json.dump(out, fh, indent=2, default=str)
    print("\nDONE. Wrote results/replication_results.json")
    for k in ["fig1", "fig2", "fig3", "fig4"]:
        print(f"  {k}: {out[k]}")
    print(f"  MC max rel error  n_i: {out['mc_max_relerr_ni']:.3%}")
    print(f"  MC max rel error  n_c: {out['mc_max_relerr_nc']:.3%}")
    print(f"  Pearson r(α, β) unconstrained scan : {out['pearson_alpha_beta_unconstrained']:+.3f}")
    print(f"  Pearson r(α, β) fixed-ε_c slices    : {out['pearson_alpha_beta_fixed_eps_c']}")
    print(f"  Intermediate (15-40 Gy) slope : {out['intermediate_linear_slope_15_40Gy']:.4f} /Gy")
    print(f"  Static-GLOBLE saturation -lnS : {out['saturation_neg_lnS_infinity']:.2f}")


if __name__ == "__main__":
    main()
