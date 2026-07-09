"""Generate replication plots for MARL-AMR (VDGN vs heuristic baselines)."""
import csv
import os
import statistics

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.normpath(os.path.join(HERE, "..", "results"))
PLOTS = os.path.normpath(os.path.join(HERE, "..", "plots"))
os.makedirs(PLOTS, exist_ok=True)


def load_csv(path, dof_col, err_col, max_n=None):
    rows = []
    with open(path) as f:
        r = csv.DictReader(f)
        for row in r:
            try:
                d = row.get(dof_col)
                e = row.get(err_col)
                if d is None or e is None or d == '' or e == '':
                    continue
                # skip the 'avg' / 'avg_t_*' rollup rows
                ep = row.get('episode', '')
                if not ep or not ep.replace('.', '').isdigit():
                    continue
                rows.append((int(float(d)), float(e)))
            except (ValueError, KeyError, TypeError):
                continue
    rows = [x for x in rows if x[1] > 0]
    if max_n:
        rows = rows[:max_n]
    return rows


def summarize(rows):
    dofs = [x[0] for x in rows]
    errs = [x[1] for x in rows]
    return (
        statistics.mean(dofs),
        statistics.stdev(dofs) if len(dofs) > 1 else 0,
        statistics.mean(errs),
        statistics.stdev(errs) if len(errs) > 1 else 0,
    )


# Load 20-episode runs
vdgn = load_csv(os.path.join(RES, "vdgn_random20_0.csv"), "sum_of_dofs", "true_global_error", max_n=20)
heur = {
    "1e-4": load_csv(os.path.join(RES, "ht_h1e-4_0.0001.csv"), "sum_of_dofs", "true_global_error"),
    "5e-4": load_csv(os.path.join(RES, "ht_h5e-4_0.0005.csv"), "sum_of_dofs", "true_global_error"),
    "1e-3": load_csv(os.path.join(RES, "ht_h1e-3_0.001.csv"), "sum_of_dofs", "true_global_error"),
    "5e-3": load_csv(os.path.join(RES, "ht_h5e-3_0.005.csv"), "sum_of_dofs", "true_global_error"),
}
fixed_coarse = load_csv(os.path.join(RES, "fixed20_coarse.csv"), "sum_of_dofs", "true_global_error")
fixed_fine = load_csv(os.path.join(RES, "fixed20_fine.csv"), "sum_of_dofs", "true_global_error")

# ============================================================
# Plot 1: Pareto — DoF (x) vs L2 error (y)
# ============================================================
fig, ax = plt.subplots(figsize=(7.5, 5.5))

# Scatter individual episodes (small, transparent)
for label, rows, color, marker in [
    ("VDGN (pretrained)", vdgn, "C0", "o"),
    ("Fixed coarse", fixed_coarse, "C3", "s"),
    ("Fixed fine (uniform refine)", fixed_fine, "C2", "D"),
]:
    xs = [r[0] for r in rows]
    ys = [r[1] for r in rows]
    ax.scatter(xs, ys, c=color, marker=marker, alpha=0.25, s=20)

for k, rows in heur.items():
    xs = [r[0] for r in rows]
    ys = [r[1] for r in rows]
    ax.scatter(xs, ys, c="C1", marker="x", alpha=0.18, s=22)

# Mean ± std error bars
points = []
mu_d, s_d, mu_e, s_e = summarize(vdgn)
ax.errorbar(
    mu_d, mu_e, xerr=s_d, yerr=s_e, fmt="o", color="C0", capsize=4,
    markersize=10, label=f"VDGN  (μ_DoF={mu_d:.0f}, μ_err={mu_e:.2e})",
)
points.append(("VDGN", mu_d, mu_e))

for k, rows in sorted(heur.items(), key=lambda kv: float(kv[0])):
    mu_d, s_d, mu_e, s_e = summarize(rows)
    ax.errorbar(
        mu_d, mu_e, xerr=s_d, yerr=s_e, fmt="x", color="C1", capsize=3, markersize=10,
        label=f"Heuristic h={k}  (μ_DoF={mu_d:.0f}, μ_err={mu_e:.2e})",
    )
    points.append((f"H {k}", mu_d, mu_e))

# Heuristic Pareto curve through means
heur_means = []
for k in ["1e-4", "5e-4", "1e-3", "5e-3"]:
    mu_d, _, mu_e, _ = summarize(heur[k])
    heur_means.append((mu_d, mu_e))
heur_means.sort()
ax.plot([p[0] for p in heur_means], [p[1] for p in heur_means], "-", color="C1", alpha=0.5, label="Heuristic Pareto curve")

mu_d, s_d, mu_e, s_e = summarize(fixed_coarse)
ax.errorbar(mu_d, mu_e, xerr=s_d, yerr=s_e, fmt="s", color="C3", capsize=4, markersize=10, label=f"Fixed coarse  ({mu_d:.0f}, {mu_e:.2e})")

mu_d, s_d, mu_e, s_e = summarize(fixed_fine)
ax.errorbar(mu_d, mu_e, xerr=s_d, yerr=s_e, fmt="D", color="C2", capsize=4, markersize=10, label=f"Fixed fine  ({mu_d:.0f}, {mu_e:.2e})")

ax.set_xlabel("Cumulative DoF (cost)")
ax.set_ylabel("True global L2 error")
ax.set_yscale("log")
ax.set_title(
    "MARL-AMR replication — Pareto on linear advection\n"
    "20 random Gaussian ICs each; nx=ny=16, max_depth=1, t_final=0.75"
)
ax.legend(loc="upper right", fontsize=8)
ax.grid(True, which="both", alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(PLOTS, "pareto_dof_vs_error.png"), dpi=150)
print("wrote", os.path.join(PLOTS, "pareto_dof_vs_error.png"))

# ============================================================
# Plot 2: per-episode error (matched seed, since both use seed=12343 for VDGN,
# 12340 for heuristic — but IC distribution is the same)
# ============================================================
fig, ax = plt.subplots(figsize=(8.5, 4.5))
n = min(len(vdgn), len(heur["1e-4"]))
xs = list(range(1, n + 1))
ax.plot(xs, [vdgn[i][1] for i in range(n)], "o-", label="VDGN (pretrained)", color="C0", linewidth=2)
for k, color in zip(["1e-4", "5e-4", "1e-3", "5e-3"], ["C1", "C4", "C5", "C6"]):
    rows = heur[k]
    ax.plot(xs, [rows[i][1] for i in range(n)], "x--", label=f"Heuristic h={k}", color=color, alpha=0.7)
ax.set_xlabel("Episode index (different random IC)")
ax.set_ylabel("True L2 error at t_final=0.75")
ax.set_title("Per-episode error comparison (note: VDGN seed=12343, heuristic seed=12340; same IC distribution but different draws)")
ax.legend(fontsize=9, loc="best")
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(PLOTS, "per_episode_error.png"), dpi=150)
print("wrote", os.path.join(PLOTS, "per_episode_error.png"))

# ============================================================
# Plot 3: VDGN error-vs-time on deterministic single-Gaussian IC
# ============================================================
vdgn_evt = []
with open(os.path.join(RES, "vdgn_err_vs_time_singleGauss.csv")) as f:
    r = csv.DictReader(f)
    for row in r:
        vdgn_evt.append((float(row["time"]), float(row["global_error"]), int(row["sum_of_dof"])))

# Heuristic err-vs-time also lives in `~/Dropbox/.../heuristic_out` from pass-1 (smaller dt mult)
heur_evt_path = os.path.join(RES, "..", "logs", "..", "results", "heuristic_err_vs_time.csv")
# Actually it's at results/ if I copied it. Re-derive from the 4-line file pulled earlier:
heur_evt = [
    (0.000, 1.160974e-02, 1204),
    (0.250, 1.429987e-02, 2408),
    (0.500, 1.789606e-02, 3636),
    (0.750, 1.945447e-02, 4900),
]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
ax1.plot([t for t, _, _ in vdgn_evt], [e for _, e, _ in vdgn_evt], "o-", color="C0", label="VDGN", linewidth=2)
ax1.plot([t for t, _, _ in heur_evt], [e for _, e, _ in heur_evt], "x--", color="C1", label="Heuristic h=5e-4", linewidth=2)
ax1.set_xlabel("Solver time t")
ax1.set_ylabel("True global L2 error")
ax1.set_title("Error vs. time (deterministic single Gaussian)")
ax1.legend()
ax1.grid(True, alpha=0.3)

ax2.plot([t for t, _, _ in vdgn_evt], [d for _, _, d in vdgn_evt], "o-", color="C0", label="VDGN", linewidth=2)
ax2.plot([t for t, _, _ in heur_evt], [d for _, _, d in heur_evt], "x--", color="C1", label="Heuristic h=5e-4", linewidth=2)
ax2.set_xlabel("Solver time t")
ax2.set_ylabel("Cumulative DoF")
ax2.set_title("Cost vs. time (deterministic single Gaussian)")
ax2.legend()
ax2.grid(True, alpha=0.3)

fig.suptitle(
    "Single-Gaussian deterministic IC (θ=0.125, u₀=2.12, w=100, x₀=y₀=0.5)\n"
    "—NOT representative; paper averages over random ICs (see pareto_dof_vs_error.png)",
    fontsize=10,
)
fig.tight_layout()
fig.savefig(os.path.join(PLOTS, "err_vs_time_singleGauss.png"), dpi=150)
print("wrote", os.path.join(PLOTS, "err_vs_time_singleGauss.png"))

# ============================================================
# Plot 4: cost-normalized "efficiency" — error * DoF (lower is better)
# ============================================================
fig, ax = plt.subplots(figsize=(7.5, 4.5))
methods = []
prod_means = []
prod_stds = []
for name, rows in [
    ("VDGN", vdgn),
    ("H 1e-4", heur["1e-4"]),
    ("H 5e-4", heur["5e-4"]),
    ("H 1e-3", heur["1e-3"]),
    ("H 5e-3", heur["5e-3"]),
    ("Fixed coarse", fixed_coarse),
    ("Fixed fine", fixed_fine),
]:
    prods = [d * e for d, e in rows]
    methods.append(name)
    prod_means.append(statistics.mean(prods))
    prod_stds.append(statistics.stdev(prods) if len(prods) > 1 else 0)
colors = ["C0", "C1", "C1", "C1", "C1", "C3", "C2"]
ax.bar(methods, prod_means, yerr=prod_stds, color=colors, alpha=0.75, capsize=4)
ax.set_ylabel("DoF × L2 error  (lower = better Pareto)")
ax.set_title("Cost-error product (proxy Pareto distance)")
ax.tick_params(axis="x", rotation=20)
ax.grid(True, axis="y", alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(PLOTS, "dof_x_error_product.png"), dpi=150)
print("wrote", os.path.join(PLOTS, "dof_x_error_product.png"))

print("\nAll plots saved to", PLOTS)
