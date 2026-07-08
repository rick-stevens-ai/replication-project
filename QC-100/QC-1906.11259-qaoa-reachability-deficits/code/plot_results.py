"""Plot deficit vs clause density (analog of paper Fig 1 top)."""
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

here = os.path.dirname(os.path.abspath(__file__))
inp = os.path.join(here, "..", "data", "qaoa_3sat_sweep.json")
outfig = os.path.join(here, "..", "figures", "fig1_analog_deficit_vs_alpha.png")
outcsv = os.path.join(here, "..", "data", "qaoa_3sat_summary.csv")

with open(inp) as fh:
    data = json.load(fh)

# organize by p
by_p = {}
for row in data["results"]:
    by_p.setdefault(row["p"], []).append(row)

fig, ax = plt.subplots(figsize=(6, 4.5), dpi=140)
markers = {1: "s", 2: "o", 4: "^", 8: "D"}
colors  = {1: "tab:blue", 2: "tab:orange", 4: "tab:green", 8: "tab:red"}
for p in sorted(by_p):
    rows = sorted(by_p[p], key=lambda r: r["alpha"])
    alphas = [r["alpha"] for r in rows]
    fs = [r["f_mean"] for r in rows]
    sem = [r["f_sem"] for r in rows]
    ax.errorbar(alphas, fs, yerr=sem, marker=markers.get(p, "x"),
                color=colors.get(p, "black"),
                linewidth=1.2, capsize=3, label=f"QAOA, p={p}")

ax.set_xlabel(r"Clause density $\alpha = m/n$")
ax.set_ylabel(r"$f = E_g^{\rm QAOA} - \min(H_{\rm SAT})$")
ax.set_title(f"Reachability deficit vs clause density  (3-SAT, n={data['n']})\n"
             f"replication analog of arXiv:1906.11259 Fig 1 (top)")
ax.axhline(0, color="grey", lw=0.5)
ax.axvline(1.0, color="grey", lw=0.5, linestyle=":", label=r"$\alpha=1$ ref")
ax.legend()
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(outfig)
print("saved", outfig)

# also CSV
with open(outcsv, "w") as fh:
    fh.write("p,alpha,m,n_instances,f_mean,f_sem,f_std,min_e_mean,e_qaoa_mean\n")
    for row in sorted(data["results"], key=lambda r: (r["p"], r["alpha"])):
        fh.write(f"{row['p']},{row['alpha']},{row['m']},{row['n_instances']},"
                 f"{row['f_mean']:.6f},{row['f_sem']:.6f},{row['f_std']:.6f},"
                 f"{row['min_e_mean']:.6f},{row['e_qaoa_mean']:.6f}\n")
print("saved", outcsv)

# ---- Monotonicity + trend summary printed for the report ----
print("\n--- SUMMARY per-depth ---")
for p in sorted(by_p):
    rows = sorted(by_p[p], key=lambda r: r["alpha"])
    alphas = [r["alpha"] for r in rows]
    fs = [r["f_mean"] for r in rows]
    # check monotonic-nondecreasing trend approximately (allow small dips)
    diffs = [fs[i+1] - fs[i] for i in range(len(fs) - 1)]
    n_up = sum(1 for d in diffs if d > 0)
    n_down = sum(1 for d in diffs if d < -0.05)  # meaningful decrease
    f_at_low = fs[0]
    f_at_high = fs[-1]
    ratio = f_at_high / (f_at_low + 1e-9) if f_at_low > 1e-6 else float("inf")
    print(f"p={p}: f(alpha={alphas[0]})={f_at_low:.3f}  f(alpha={alphas[-1]})={f_at_high:.3f}  "
          f"ratio={ratio:.2f}   up={n_up}/{len(diffs)} down_sig={n_down}")
