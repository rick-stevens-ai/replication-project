"""Reproduce (qualitatively) Fig. 4.5: cation density, potential and total
diffuse charge profiles from the four model variants (MF, SC, LC, LS) at
equilibrium.

Paper parameters for Fig. 4.5: (eps, q, a, gamma) = (0.2, 0.3, 0.15, 1.0),
V = 1. Note: the paper shows transient profiles at t=0.2 and t=5; we report
the steady-state (long-time) equilibrium, which corresponds to t=5 in
their two-plate problem (system tends to steady state).
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


def main(outdir, logdir):
    eps, q, a, gamma, V = 0.2, 0.3, 0.15, 1.0, 1.0
    N = 200
    results = {}
    init_for_LS = None  # warm-start LS from LC solution
    for model in ("MF", "SC", "LC", "LS"):
        print(f"\n=== Solving model {model} ===")
        # Grand-canonical (no rescaling): mu_bulk is fixed at 0 by the
        # subtraction inside mu_co / mu_hs. Use heavier damping on densities.
        if model == "LS":
            # LS combines two strong nonlinearities; warm-start from LC and
            # use very small damping. The MFMT integration is the most
            # sensitive piece, so we lower max growth and run longer.
            p = mPBParams(eps=eps, q=q, a=a, V=V, gamma=gamma, model=model,
                          N=N, tol=1e-5, max_iter=3000, damping=0.02,
                          phi_damping=0.2, canonical=False, voltage_steps=10)
        else:
            p = mPBParams(eps=eps, q=q, a=a, V=V, gamma=gamma, model=model,
                          N=N, tol=1e-6, max_iter=2000, damping=0.05,
                          phi_damping=0.3, canonical=False, voltage_steps=5)
        c_init = None
        if model == "LS" and init_for_LS is not None:
            c_init = init_for_LS
        res = solve_mpb(p, c_init=c_init, verbose=True)
        if model == "LC":
            init_for_LS = (res["c_plus"].copy(), res["c_minus"].copy())
        print(f"  converged={res['converged']} after {res['iter']} iters, "
              f"final res={res['residuals'][-1]:.3e}")
        Q = diffuse_charge(res["x"], res["c_plus"], res["c_minus"])
        print(f"  diffuse charge Q = {Q:.5f}")
        results[model] = res

    # ---- Plot: (a) cation density, (b) potential, (c) diffuse charge bar
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

    axes[0].set_xlabel("x")
    axes[0].set_ylabel(r"$c_+(x)$")
    axes[0].set_title(r"(a) Cation density (steady state)")
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

    fig.suptitle(f"Fig. 4.5 replication: (eps,q,a,gamma,V) = "
                 f"({eps},{q},{a},{gamma},{V}), N={N}")
    fig.tight_layout()
    out = os.path.join(outdir, "fig45_four_models.png")
    fig.savefig(out, dpi=140)
    print(f"\nSaved {out}")

    # Save numerical results
    np.savez(os.path.join(outdir, "fig45_data.npz"),
             **{f"{m}_{k}": v
                for m, r in results.items()
                for k, v in r.items()
                if isinstance(v, np.ndarray) and k in ("x", "c_plus",
                                                       "c_minus", "phi",
                                                       "mu_hs", "mu_co")})
    summary = {
        "params": {"eps": eps, "q": q, "a": a, "gamma": gamma, "V": V,
                   "N": N},
        "diffuse_charge": {m: float(Q) for m, Q in Qs.items()},
        "iterations": {m: int(r["iter"]) for m, r in results.items()},
        "converged": {m: bool(r["converged"]) for m, r in results.items()},
        "final_residual": {m: float(r["residuals"][-1])
                           for m, r in results.items()},
    }
    with open(os.path.join(outdir, "fig45_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)


if __name__ == "__main__":
    here = os.path.dirname(__file__)
    outdir = os.path.abspath(os.path.join(here, "..", "figures"))
    logdir = os.path.abspath(os.path.join(here, "..", "logs"))
    os.makedirs(outdir, exist_ok=True)
    os.makedirs(logdir, exist_ok=True)
    main(outdir, logdir)
