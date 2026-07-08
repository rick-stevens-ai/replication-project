"""Reproduce a version of Figure 6 from the paper."""
import json, pathlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

here = pathlib.Path(__file__).resolve().parent
res = json.loads((here.parent / "report" / "evidence" / "benchmark_results.json").read_text())

eps_list = sorted([r["epsilon"] for r in res["iqae"].values()], reverse=True)
iqae_Q   = [res["iqae"][k]["mean_Q"]   for k in sorted(res["iqae"].keys(), key=lambda k: -res["iqae"][k]["epsilon"])]
cheb_Q   = [res["chebae"][k]["mean_Q"] for k in sorted(res["chebae"].keys(), key=lambda k: -res["chebae"][k]["epsilon"])]

fig, ax = plt.subplots(figsize=(7,5))
ax.loglog(eps_list, iqae_Q, 'o-', label=f'IQAE  (our C≈{res["fits_fC"]["iqae"]["C_geom"]:.1f})',   color='tab:blue')
ax.loglog(eps_list, cheb_Q, 's-', label=f'ChebAE (our C≈{res["fits_fC"]["chebae"]["C_geom"]:.1f})', color='tab:orange')

# paper's fC lines
ax.loglog(eps_list, [9.93/e for e in eps_list], '--', color='tab:blue',   alpha=0.5, label='IQAE paper: 9.93/ε')
ax.loglog(eps_list, [4.66/e for e in eps_list], '--', color='tab:orange', alpha=0.5, label='ChebAE paper: 4.66/ε')

ax.set_xlabel('ε (target additive error)')
ax.set_ylabel(r'Mean queries $\langle Q_\Pi\rangle$')
ax.set_title(f'Amplitude Estimation query complexity (a=0.5, δ=0.05, N={res["n_runs"]} runs)\n'
             f'Replication of arXiv:2207.08628 Empirical Claims 18, 20')
ax.grid(True, which='both', alpha=0.3)
ax.invert_xaxis()
ax.legend(loc='upper right', fontsize=9)

fig.tight_layout()
out = here.parent / "figures" / "query_complexity.png"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=130)
print(f"[wrote] {out}")
