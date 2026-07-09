"""Run uniform / AMR / MR Sod-shock-tube sweeps and write CSV + figures."""
import sys, os, csv, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from euler_solver import (
    run_uniform, run_amr, run_mr, sod_exact, cons_to_prim,
)

OUTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "results"))
FIGDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "figures"))
os.makedirs(OUTDIR, exist_ok=True)
os.makedirs(FIGDIR, exist_ok=True)


def stats_to_dict(s, kind, params):
    return {
        "kind": kind,
        "name": s.name,
        "params": json.dumps(params),
        "N_active_max": s.N_active_max,
        "N_active_avg": round(s.N_active_avg, 2),
        "N_uniform_equiv": s.N_uniform_equiv,
        "compression_ratio_avg": round(s.N_active_avg / s.N_uniform_equiv, 4),
        "wall_time_s": round(s.wall_time_s, 4),
        "steps": s.steps,
        "final_dt": s.final_dt,
        "err_L1_rho": s.err_L1_rho,
        "err_L2_rho": s.err_L2_rho,
        "err_Linf_rho": s.err_Linf_rho,
    }


def main():
    rows = []
    T = 0.2
    cfl = 0.5

    # ---- Uniform baselines at multiple resolutions for convergence reference ----
    print("=== UNIFORM sweep ===")
    for N in [100, 200, 400, 800, 1600, 3200]:
        x, U, s = run_uniform(N=N, T=T, cfl=cfl)
        rows.append(stats_to_dict(s, "uniform", {"N": N}))
        print(f"  N={N}: L1={s.err_L1_rho:.4e} L2={s.err_L2_rho:.4e} time={s.wall_time_s:.3f}s steps={s.steps}")

    # ---- AMR sweep: vary refinement threshold ----
    print("=== AMR sweep ===")
    for N0, r in [(100, 4), (200, 4), (400, 4)]:
        for thr in [0.5, 0.2, 0.1, 0.05, 0.02]:
            x, U, s, patches = run_amr(N_coarse=N0, refine_ratio=r, T=T, cfl=cfl,
                                       refine_threshold=thr, regrid_every=4, buffer_cells=2)
            rows.append(stats_to_dict(s, "amr",
                                       {"N0": N0, "r": r, "thr": thr,
                                        "regrid_every": 4, "buffer": 2,
                                        "N_eff": N0 * r}))
            print(f"  N0={N0} r={r} thr={thr}: L1={s.err_L1_rho:.4e} "
                  f"compr={s.N_active_avg/s.N_uniform_equiv:.3f} time={s.wall_time_s:.3f}s")

    # ---- MR sweep: vary tolerance and J levels ----
    print("=== MR sweep ===")
    for Nfine, J in [(400, 4), (800, 4), (1600, 4)]:
        for tol in [1e-1, 5e-2, 1e-2, 5e-3, 1e-3, 1e-4]:
            x, U, s = run_mr(N_fine=Nfine, J_levels=J, T=T, cfl=cfl, tol=tol)
            rows.append(stats_to_dict(s, "mr",
                                       {"N_fine": Nfine, "J": J, "tol": tol}))
            print(f"  N_fine={Nfine} J={J} tol={tol}: L1={s.err_L1_rho:.4e} "
                  f"compr={s.N_active_avg/s.N_uniform_equiv:.3f} time={s.wall_time_s:.3f}s")

    # ---- Write CSV ----
    csv_path = os.path.join(OUTDIR, "sweep_results.csv")
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"\nWrote {csv_path} with {len(rows)} rows")

    # ---- Figures ----
    # Figure 1: density profile at T=0.2 for the three solvers at matched effective N
    x_u, U_u, s_u = run_uniform(N=400, T=T, cfl=cfl)
    x_a, U_a, s_a, _ = run_amr(N_coarse=100, refine_ratio=4, T=T, cfl=cfl,
                                refine_threshold=0.05)
    x_m, U_m, s_m = run_mr(N_fine=400, J_levels=4, T=T, cfl=cfl, tol=1e-3)
    x_ref = np.linspace(0, 1, 4001)
    rho_ex, u_ex, p_ex = sod_exact(x_ref, T)

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.2), sharex=True)
    for ax, (var_idx, var_name, ex) in zip(
        axes,
        [(0, "Density", rho_ex), (1, "Velocity", u_ex), (2, "Pressure", p_ex)]
    ):
        if var_idx == 0:
            yu = cons_to_prim(U_u)[0]; ya = cons_to_prim(U_a)[0]; ym = cons_to_prim(U_m)[0]
        elif var_idx == 1:
            yu = cons_to_prim(U_u)[1]; ya = cons_to_prim(U_a)[1]; ym = cons_to_prim(U_m)[1]
        else:
            yu = cons_to_prim(U_u)[2]; ya = cons_to_prim(U_a)[2]; ym = cons_to_prim(U_m)[2]
        ax.plot(x_ref, ex, "k-", lw=1.5, label="exact")
        ax.plot(x_u, yu, "b.", ms=2.5, label=f"uniform N=400")
        ax.plot(x_a, ya, "r.", ms=2.5, label=f"AMR N0=100,r=4")
        ax.plot(x_m, ym, "g.", ms=2.5, label=f"MR N=400,tol=1e-3")
        ax.set_xlabel("x")
        ax.set_ylabel(var_name)
        ax.legend(fontsize=8, loc="best")
        ax.grid(alpha=0.3)
    fig.suptitle("Sod shock tube at T=0.2 — three adaptive strategies vs exact", fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "fig1_solution_profiles.png"), dpi=140)
    plt.close(fig)

    # Figure 2: pareto — L1 error vs avg active cells, all rows
    import itertools
    fig, ax = plt.subplots(figsize=(8, 5.5))
    markers = {"uniform": ("ko-", "Uniform FV"), "amr": ("rs-", "AMR (block-structured)"),
               "mr": ("g^-", "MR (Harten-style)")}
    for kind, (style, label) in markers.items():
        subset = [r for r in rows if r["kind"] == kind]
        xs = [r["N_active_avg"] for r in subset]
        ys = [r["err_L1_rho"] for r in subset]
        # Sort by xs
        idx = np.argsort(xs)
        xs = [xs[i] for i in idx]; ys = [ys[i] for i in idx]
        ax.loglog(xs, ys, style, label=label, ms=6, lw=1)
    ax.set_xlabel("Average active cells")
    ax.set_ylabel("L1 error in density at T=0.2")
    ax.set_title("Accuracy vs degrees-of-freedom: Sod 1D Euler")
    ax.grid(which="both", alpha=0.3)
    ax.legend(loc="best", fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "fig2_pareto_error_vs_dof.png"), dpi=140)
    plt.close(fig)

    # Figure 3: compression ratio vs accuracy
    fig, ax = plt.subplots(figsize=(8, 5.5))
    for kind, (style, label) in markers.items():
        subset = [r for r in rows if r["kind"] == kind]
        xs = [r["compression_ratio_avg"] for r in subset]
        ys = [r["err_L1_rho"] for r in subset]
        ax.loglog(xs, ys, style, label=label, ms=6, lw=1)
    ax.set_xlabel("Avg active cells / N_uniform_equivalent  (compression ratio)")
    ax.set_ylabel("L1 error in density at T=0.2")
    ax.set_title("Error vs compression: lower-left = best")
    ax.grid(which="both", alpha=0.3)
    ax.legend(loc="best", fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "fig3_error_vs_compression.png"), dpi=140)
    plt.close(fig)

    # Figure 4: wall time vs error
    fig, ax = plt.subplots(figsize=(8, 5.5))
    for kind, (style, label) in markers.items():
        subset = [r for r in rows if r["kind"] == kind]
        xs = [r["wall_time_s"] for r in subset]
        ys = [r["err_L1_rho"] for r in subset]
        ax.loglog(xs, ys, style, label=label, ms=6, lw=1)
    ax.set_xlabel("Python wall time (s)")
    ax.set_ylabel("L1 error in density at T=0.2")
    ax.set_title("Cost vs accuracy (Python prototype, not production code)")
    ax.grid(which="both", alpha=0.3)
    ax.legend(loc="best", fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "fig4_walltime_vs_error.png"), dpi=140)
    plt.close(fig)

    print(f"\nFigures written to {FIGDIR}")


if __name__ == "__main__":
    main()
