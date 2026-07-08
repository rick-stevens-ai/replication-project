"""Make matplotlib plots of the noise-vs-success curves for the report."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

EVID = Path(__file__).resolve().parent.parent / "report" / "evidence"

# --- Cai noise on N=15 Shor (baseline degenerate case) ---
cai_shor = json.loads((EVID / "cai_noise_sweep.json").read_text())

# --- QPE at 3 register sizes (non-dyadic phase) ---
qpes = {n: json.loads((EVID / f"qpe_cai_n{n}.json").read_text())
        for n in (6, 8, 10)}

# --- Depolarizing on N=15 Shor ---
dep = json.loads((EVID / "shor15_depolarizing.json").read_text())

# --- Depolarizing on QPE ---
qpe_dep = json.loads((EVID / "qpe_dep_n8.json").read_text())


fig, axes = plt.subplots(2, 2, figsize=(11, 8))

# (a) Cai noise on Shor N=15 (flat because peaks are dyadic)
ax = axes[0, 0]
xs = [r["eps"] for r in cai_shor["results"]]
ys = [r["mean_success_rate"] for r in cai_shor["results"]]
es = [r["std_success_rate"] for r in cai_shor["results"]]
ax.errorbar([max(x, 1e-6) for x in xs], ys, yerr=es, marker="o", capsize=3)
ax.set_xscale("log"); ax.set_xlabel("Cai noise amplitude eps")
ax.set_ylabel("Shor N=15 success rate")
ax.set_title("(a) Shor N=15 vs Cai QFT-angle noise\n"
             "(insensitive: all phase peaks are dyadic)")
ax.axhline(0.75, ls="--", color="gray", label="noiseless baseline")
ax.set_ylim(0, 1); ax.grid(True, alpha=0.4); ax.legend()

# (b) QPE non-dyadic phase, Cai noise, 3 register sizes
ax = axes[0, 1]
for n, color in zip((6, 8, 10), ("C0", "C1", "C2")):
    r = qpes[n]["results"]
    xs = [x["eps"] for x in r]
    ys = [x["mean_success"] for x in r]
    es = [x["std_success"] for x in r]
    ax.errorbar([max(x, 1e-6) for x in xs], ys, yerr=es,
                marker="o", capsize=3, label=f"n_count={n}", color=color)
ax.set_xscale("log"); ax.set_xlabel("Cai noise amplitude eps")
ax.set_ylabel("QPE success rate (+/-1 bin)")
ax.set_title("(b) QPE with non-dyadic phi = 1/golden vs Cai noise\n"
             "(clean Cai-predicted decay; larger register --> earlier onset)")
ax.set_ylim(0, 1); ax.grid(True, alpha=0.4); ax.legend()

# (c) Shor N=15 depolarizing
ax = axes[1, 0]
xs = [r["p_1q"] for r in dep["results"]]
ys = [r["success_rate"] for r in dep["results"]]
ax.plot([max(x, 1e-6) for x in xs], ys, marker="s", color="C3")
ax.set_xscale("log"); ax.set_xlabel("Depolarizing p (1q; 2q=10p)")
ax.set_ylabel("Shor N=15 success rate")
ax.set_title("(c) Shor N=15 vs depolarizing noise\n"
             "(decays sharply; floor ~ 9% is random-measurement luck)")
ax.set_ylim(0, 1); ax.grid(True, alpha=0.4)

# (d) QPE depolarizing
ax = axes[1, 1]
xs = [r["p_1q"] for r in qpe_dep["results"]]
ys = [r["success_rate"] for r in qpe_dep["results"]]
ax.plot([max(x, 1e-6) for x in xs], ys, marker="D", color="C4")
ax.set_xscale("log"); ax.set_xlabel("Depolarizing p (1q; 2q=10p)")
ax.set_ylabel("QPE success rate (+/-1 bin)")
ax.set_title("(d) QPE (phi=1/golden) vs depolarizing noise\n"
             "(clean decay to random floor ~ 3/256 = 1.2%)")
ax.set_ylim(0, 1); ax.grid(True, alpha=0.4)

fig.suptitle("Replication of Cai (arXiv:2306.10072): Shor's algorithm "
             "under noise\n"
             "(qiskit-aer statevector + density-matrix, small-N)",
             fontsize=11)
fig.tight_layout()
out = EVID / "noise_vs_success.png"
fig.savefig(out, dpi=150)
print(f"Wrote {out}")
