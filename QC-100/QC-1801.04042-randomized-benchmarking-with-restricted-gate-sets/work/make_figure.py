"""Make fidelity-decay figures for the RB replication."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

evidence = Path("/Users/stevens/Dropbox/REPLICATE-PROJECT/QC-100/"
                "QC-1801.04042-randomized-benchmarking-with-restricted-gate-sets/report/evidence")

with open(evidence / "results.json") as f:
    sym = json.load(f)
with open(evidence / "results_asym.json") as f:
    asym = json.load(f)

# ---- Figure 1: Symmetric depolarizing, all 4 experiments ----
fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

def plot_exp(ax, key, results, label, color, marker):
    d = results[key]
    lengths = np.array(d["lengths"])
    fs = np.array(d["fs"])
    ax.scatter(lengths, fs, color=color, marker=marker, s=60, label=f"{label} data", zorder=3)
    # overlay fit
    if "fit" in d:
        fit = d["fit"]
        a, b, lam = fit["a"], fit["b"], fit["lam"]
    else:
        fit = d["fit_single"]
        a, b, lam = fit["a"], fit["b"], fit["lam"]
    xs = np.linspace(1, lengths.max(), 200)
    ys = a + b * lam**xs
    ax.plot(xs, ys, color=color, ls="-", alpha=0.7,
            label=f"{label} fit λ={lam:.4f}")
    # theory line
    if "theory_lambda" in d:
        lam_t = d["theory_lambda"]
    elif "theory_lambda1" in d:
        lam_t = d["theory_lambda1"]
    elif "theory" in d:
        lam_t = d["theory"].get("lam1", d["theory"].get("lam2"))
    ys_t = a + b * lam_t**xs
    ax.plot(xs, ys_t, color=color, ls="--", alpha=0.5,
            label=f"{label} theory λ={lam_t:.4f}")

ax = axes[0]
plot_exp(ax, "exp1_full_clifford_n2", sym, "Full Clifford", "C0", "o")
plot_exp(ax, "exp2_real_clifford_n2", sym, "Real Clifford, |00⟩", "C1", "s")
ax.set_xscale("log", base=2)
ax.set_xlabel("Sequence length m")
ax.set_ylabel("Survival probability")
ax.set_title("Symmetric depolarizing (p_dep=0.01/qubit)\nFull vs Real Clifford, n=2")
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

ax = axes[1]
plot_exp(ax, "exp3a_cnot_pauli_n2_00", sym, "CNOT+Pauli, |00⟩", "C2", "^")
plot_exp(ax, "exp3b_cnot_pauli_n2_plusplus", sym, "CNOT+Pauli, |++⟩", "C3", "v")
ax.set_xscale("log", base=2)
ax.set_xlabel("Sequence length m")
ax.set_title("CNOT+Pauli subgroup, n=2, symmetric noise")
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(evidence / "rb_decay_symmetric.png", dpi=140)
print(f"Wrote {evidence / 'rb_decay_symmetric.png'}")

# ---- Figure 2: Asymmetric (pure Z) noise — probes block structure ----
fig, ax = plt.subplots(figsize=(8, 5))

for key, label, color, marker in [
    ("zerror_00", "|00⟩  (block B1: Z-only)", "C4", "o"),
    ("zerror_pp", "|++⟩  (block B2: X-only)", "C5", "s"),
]:
    d = asym[key]
    lengths = np.array(d["lengths"])
    fs = np.array(d["fs"])
    ax.scatter(lengths, fs, color=color, marker=marker, s=60, label=f"{label} data", zorder=3)
    fit = d["fit"]
    a, b, lam = fit["a"], fit["b"], fit["lam"]
    lam_t = d["lam_theory"]
    xs = np.linspace(1, lengths.max(), 200)
    ax.plot(xs, a + b*lam**xs, color=color, ls="-", alpha=0.6, label=f"fit λ={lam:.4f}")
    ax.plot(xs, a + b*lam_t**xs, color=color, ls="--", alpha=0.5, label=f"theory λ={lam_t:.4f}")

ax.set_xscale("log", base=2)
ax.set_xlabel("Sequence length m")
ax.set_ylabel("Survival probability")
ax.set_title("Asymmetric noise (pure per-qubit Z, p_z=0.02)\nCNOT+Pauli RB, n=2\n"
             "|00⟩ sees λ₁=1 (Z errors preserve Z eigenstates); |++⟩ sees λ₂ decay.")
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_ylim(0.15, 1.05)
plt.tight_layout()
plt.savefig(evidence / "rb_decay_asymmetric.png", dpi=140)
print(f"Wrote {evidence / 'rb_decay_asymmetric.png'}")
