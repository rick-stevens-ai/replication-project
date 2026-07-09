"""Numerical-convergence study: refine N for the Fig 4.3(a)-like setup
(low correlation, all models converge cleanly) and verify that the
diffuse charge Q converges as N -> infinity for each model. This is the
mPNP-equivalent of a discretization-error / mesh-convergence study.
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
    eps, q, a, gamma, V = 0.0813, 0.0604, 0.01269, 0.0, 0.5
    Ns = [50, 100, 200, 400, 800]
    rows = []
    Q_by_model = {m: [] for m in ("MF", "SC", "LC", "LS")}
    init_for_LS = None
    for N in Ns:
        print(f"\nN = {N}")
        Q_at_N = {}
        for model in ("MF", "SC", "LC", "LS"):
            p = mPBParams(eps=eps, q=q, a=a, V=V, gamma=gamma, model=model,
                          N=N, tol=1e-7, max_iter=2000, damping=0.1,
                          phi_damping=0.3, canonical=False, voltage_steps=3)
            c_init = None
            if model == "LS" and init_for_LS is not None:
                # Resample from previous N to current grid
                pass  # use cold start; quick at low correlation
            res = solve_mpb(p, verbose=False)
            Q = diffuse_charge(res["x"], res["c_plus"], res["c_minus"])
            Q_at_N[model] = float(Q)
            Q_by_model[model].append(float(Q))
            print(f"  {model}: Q = {Q:.6f}, conv={res['converged']}, it={res['iter']}")
        rows.append({"N": N, **Q_at_N})

    # Q vs N plot
    fig, ax = plt.subplots(figsize=(7, 5))
    colors = {"MF": "tab:blue", "SC": "tab:orange",
              "LC": "tab:green", "LS": "tab:red"}
    for m in ("MF", "SC", "LC", "LS"):
        ax.semilogx(Ns, Q_by_model[m], "o-", color=colors[m], label=m)
    ax.set_xlabel("Grid points N")
    ax.set_ylabel("Diffuse charge Q (left half)")
    ax.set_title("Mesh-convergence of diffuse charge\n"
                 f"(eps,q,a,gamma,V) = ({eps},{q},{a},{gamma},{V})")
    ax.legend(); ax.grid(alpha=0.3, which="both")
    fig.tight_layout()
    out = os.path.join(outdir, "convergence_Q.png")
    fig.savefig(out, dpi=140)
    print(f"\nSaved {out}")

    # Convergence-rate plot (relative to richest N)
    fig2, ax2 = plt.subplots(figsize=(7, 5))
    Q_ref = {m: Q_by_model[m][-1] for m in Q_by_model}
    for m in ("MF", "SC", "LC", "LS"):
        errs = [abs(q - Q_ref[m]) for q in Q_by_model[m][:-1]]
        Ns_err = Ns[:-1]
        ax2.loglog(Ns_err, errs, "o-", color=colors[m], label=m)
    # Reference O(h^2) = O(N^-2)
    Ns_arr = np.array(Ns[:-1])
    ax2.loglog(Ns_arr, 1e-3 * (Ns_arr / Ns_arr[0]) ** (-2),
               "k--", lw=1, label=r"$O(N^{-2})$ ref")
    ax2.set_xlabel("N")
    ax2.set_ylabel(r"$|Q(N) - Q(N_{ref})|$")
    ax2.set_title(f"Self-convergence of Q (ref: N={Ns[-1]})")
    ax2.legend(); ax2.grid(alpha=0.3, which="both")
    fig2.tight_layout()
    out2 = os.path.join(outdir, "convergence_rate.png")
    fig2.savefig(out2, dpi=140)
    print(f"Saved {out2}")

    with open(os.path.join(outdir, "convergence_summary.json"), "w") as f:
        json.dump({
            "params": {"eps": eps, "q": q, "a": a, "gamma": gamma, "V": V},
            "Ns": Ns,
            "Q_by_model": Q_by_model,
            "Q_ref": Q_ref,
            "note": "Self-convergence with reference Q taken from richest N.",
        }, f, indent=2)


if __name__ == "__main__":
    here = os.path.dirname(__file__)
    outdir = os.path.abspath(os.path.join(here, "..", "figures"))
    os.makedirs(outdir, exist_ok=True)
    main(outdir)
