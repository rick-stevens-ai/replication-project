"""Generate plots for the report."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent

# ------ Plot 1: gap vs s for n=8, both paths (full 2^n) ------
with open(HERE / "results.json") as f:
    small_n = json.load(f)

n_show = "8"
data = small_n["per_n"][n_show]
s_grid = np.array(data["s_grid"])
g_lin = np.array(data["gaps_linear"])
g_far = np.array(data["gaps_farhi_A"])

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(s_grid, g_lin, label=f"Linear path H(s)=(1-s)H_B+s H_P", color="C0", lw=2)
ax.plot(s_grid, g_far, label=f"Farhi-A path H(s)+s(1-s)H_E", color="C3", lw=2)
ax.axhline(y=data["linear_path"]["g_min"], color="C0", ls=":", alpha=0.5,
           label=f"g_min(linear)={data['linear_path']['g_min']:.3f}")
ax.axhline(y=data["farhi_A_path"]["g_min"], color="C3", ls=":", alpha=0.5,
           label=f"g_min(Farhi-A)={data['farhi_A_path']['g_min']:.3f}")
ax.set_xlabel("s"); ax.set_ylabel("spectral gap (E1-E0)")
ax.set_title(f"Spectral gap vs s at n={n_show} (full 2^n exact-diag)")
ax.legend(loc="upper left"); ax.grid(True, alpha=0.3)
fig.tight_layout(); fig.savefig(HERE / "fig1_gap_vs_s_n8.png", dpi=140)
plt.close(fig)

# ------ Plot 2: g_min scaling with n ------
with open(HERE / "refined_scaling.json") as f:
    scaling = json.load(f)

ns = sorted(int(k) for k in scaling.keys())
g_lin_arr = [scaling[str(n)]["linear"]["g_min"] for n in ns]
g_far_arr = [scaling[str(n)]["farhi_A"]["g_min"] for n in ns]

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.semilogy(ns, g_lin_arr, "o-", label="linear path", color="C0", lw=2)
ax.semilogy(ns, g_far_arr, "s-", label="Farhi-A path", color="C3", lw=2)
ax.set_xlabel("n (# qubits)"); ax.set_ylabel("min spectral gap  g_min")
ax.set_title("g_min scaling: linear vs Farhi-A path (symm subspace)")
ax.legend(); ax.grid(True, which="both", alpha=0.3)
# Annotate that Farhi-A is full for n<=12 else leading-order
ax.axvline(x=12.5, color="gray", ls="--", alpha=0.5)
ax.text(13, 1e2, "n>12: leading-order H_E\n(asymptotic form)", fontsize=8, color="gray")
fig.tight_layout(); fig.savefig(HERE / "fig2_gmin_scaling.png", dpi=140)
plt.close(fig)

# ------ Plot 3: ratio scaling ------
ratios = [scaling[str(n)]["gap_ratio"] for n in ns]
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.semilogy(ns, ratios, "d-", color="C2", lw=2)
ax.axhline(y=1.5, color="k", ls="--", alpha=0.5, label="paper's 1.5x bar (weakest form)")
ax.set_xlabel("n"); ax.set_ylabel("g_min(Farhi-A) / g_min(linear)")
ax.set_title("Gap-improvement ratio vs n (log scale)")
ax.legend(); ax.grid(True, which="both", alpha=0.3)
fig.tight_layout(); fig.savefig(HERE / "fig3_ratio_scaling.png", dpi=140)
plt.close(fig)

# ------ Plot 4: random-A histogram ------
rand = small_n["random_A_at_n8"]
records = rand["records"]
ratios_rand = [r["ratio"] for r in records]
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.hist(ratios_rand, bins=20, color="C4", edgecolor="k", alpha=0.85)
ax.axvline(x=1.0, color="k", ls="--", label="=1 (equal to linear)")
ax.axvline(x=1.5, color="r", ls="--", label="1.5x bar")
ax.set_xlabel("g_min(random-A) / g_min(linear)"); ax.set_ylabel("count")
ax.set_title(f"Random-A gap-ratio distribution (n=8, {rand['n_samples']} samples)\n"
             f"beat linear: {rand['n_beats_linear']}/{rand['n_samples']}={rand['beat_fraction']:.3f}  |  "
             f">=1.5x: {rand['n_ratio_ge_1p5']}/{rand['n_samples']}  |  paper: 351/1000=0.351")
ax.legend(); ax.grid(True, alpha=0.3)
fig.tight_layout(); fig.savefig(HERE / "fig4_random_A_hist.png", dpi=140)
plt.close(fig)

print("Wrote fig1_gap_vs_s_n8.png, fig2_gmin_scaling.png, fig3_ratio_scaling.png, fig4_random_A_hist.png")
