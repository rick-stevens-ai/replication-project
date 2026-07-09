"""Reproduce (qualitatively) Fig. 4.3(a): cation density profiles for 1:1
electrolyte without dielectric mismatch (gamma = 0). For our reduced model
(steady state, symmetric), we use V > 0 (charged surfaces) and compare the
four model variants. The paper reports that for the weak-correlation regime
all modified PNP models agree well with MC and with each other; we expect
the same here, since gamma=0 turns OFF the strong dielectric-image
repulsion that drives the layering in Fig 4.5.

Dimensional parameters from Fig 4.3(a) (paper): c0=100 mM, a+/-=0.15 nm,
L=11.825 nm, l_B=0.714 nm at 298 K -> dimensionless q = l_B/L = 0.0604,
a = 0.15/11.825 = 0.01269 (very thin Stern layer relative to gap).
Debye length l_0 = 1/sqrt(8 pi l_B c0) = 0.962 nm at 100 mM, so
eps = l_0/L = 0.0814. Surface charge ~ +/-0.02 C/m^2 corresponds to
dimensionless V = e*sigma_s*L/(eps_w*kT) but a direct equivalent here is
to impose moderate V on a symmetric system.

We do a tractable variant: same dimensionless ratios as Fig 4.3(a) but
modest V=0.5 (the paper's surface charge maps to a moderate potential at
this electrolyte concentration), gamma=0.
"""
from __future__ import annotations
import json
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
from mpnp import mPBParams, solve_mpb, diffuse_charge


def main(outdir):
    # Dimensionless params from paper Fig 4.3(a):
    L_phys = 11.825   # nm
    a_phys = 0.15     # nm
    c0_mM = 100.0
    lB_phys = 0.714   # nm at 298 K, water
    # Debye length at 1:1, c0 (in nm): l0 [nm] = 0.304 / sqrt(c0[M]) = 0.962 at 0.1 M
    l0_phys = 0.304 / np.sqrt(c0_mM * 1e-3)
    eps = l0_phys / L_phys
    q = lB_phys / L_phys
    a = a_phys / L_phys
    print(f"Fig 4.3(a) dimensionless params: eps={eps:.4f}, q={q:.4f}, a={a:.5f}")
    gamma = 0.0
    V = 0.5  # moderate dimensionless potential
    N = 300

    results = {}
    init_for_LS = None
    for model in ("MF", "SC", "LC", "LS"):
        print(f"\n=== Solving model {model} ===")
        p = mPBParams(eps=eps, q=q, a=a, V=V, gamma=gamma, model=model,
                      N=N, tol=1e-7, max_iter=2000, damping=0.1,
                      phi_damping=0.3, canonical=False, voltage_steps=4)
        c_init = None
        if model == "LS" and init_for_LS is not None:
            c_init = init_for_LS
        res = solve_mpb(p, c_init=c_init, verbose=False)
        print(f"  converged={res['converged']} after {res['iter']} iters, "
              f"final res={res['residuals'][-1]:.3e}")
        Q = diffuse_charge(res["x"], res["c_plus"], res["c_minus"])
        print(f"  diffuse charge Q = {Q:.5f}")
        results[model] = res
        if model == "LC":
            init_for_LS = (res["c_plus"].copy(), res["c_minus"].copy())

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    colors = {"MF": "tab:blue", "SC": "tab:orange",
              "LC": "tab:green", "LS": "tab:red"}
    styles = {"MF": "-", "SC": "--", "LC": "-.", "LS": "-"}

    for model, res in results.items():
        x = res["x"]
        axes[0].plot(x, res["c_plus"], colors[model], ls=styles[model],
                     lw=1.7, label=model)
        axes[1].plot(x, res["phi"], colors[model], ls=styles[model], lw=1.7,
                     label=model)

    axes[0].set_xlabel("x (dimensionless)")
    axes[0].set_ylabel(r"$c_+(x)$")
    axes[0].set_title(r"(a) Cation density, no dielectric mismatch ($\gamma=0$)")
    axes[0].legend(); axes[0].grid(alpha=0.3)

    axes[1].set_xlabel("x")
    axes[1].set_ylabel(r"$\phi(x)$")
    axes[1].set_title("(b) Electrostatic potential")
    axes[1].legend(); axes[1].grid(alpha=0.3)

    Qs = {m: diffuse_charge(r["x"], r["c_plus"], r["c_minus"])
          for m, r in results.items()}
    axes[2].bar(list(Qs.keys()), list(Qs.values()),
                color=[colors[m] for m in Qs])
    axes[2].set_ylabel("Q (left-half diffuse charge)")
    axes[2].set_title("(c) Total diffuse charge")
    axes[2].grid(alpha=0.3, axis="y")

    fig.suptitle(f"Fig. 4.3(a)-like setup (no dielectric mismatch): "
                 f"eps={eps:.3f}, q={q:.3f}, a={a:.4f}, V={V}")
    fig.tight_layout()
    out = os.path.join(outdir, "fig43a_no_dielectric.png")
    fig.savefig(out, dpi=140)
    print(f"\nSaved {out}")

    summary = {
        "params": {"eps": eps, "q": q, "a": a, "gamma": gamma, "V": V,
                   "N": N},
        "diffuse_charge": {m: float(Q) for m, Q in Qs.items()},
        "iterations": {m: int(r["iter"]) for m, r in results.items()},
        "converged": {m: bool(r["converged"]) for m, r in results.items()},
        "final_residual": {m: float(r["residuals"][-1])
                           for m, r in results.items()},
        "note": "Paper Fig 4.3(a) reports good MF-vs-mPNP agreement in this "
                "weak-correlation regime; we expect similar small differences.",
    }
    with open(os.path.join(outdir, "fig43a_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)


if __name__ == "__main__":
    here = os.path.dirname(__file__)
    outdir = os.path.abspath(os.path.join(here, "..", "figures"))
    os.makedirs(outdir, exist_ok=True)
    main(outdir)
