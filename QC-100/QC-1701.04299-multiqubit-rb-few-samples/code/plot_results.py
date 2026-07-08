"""Make plots for the RB replication report."""
import json
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.join(HERE, "..", "report", "evidence")

with open(os.path.join(EV, "rb_raw_survivals.json")) as f:
    raw = json.load(f)
with open(os.path.join(EV, "rb_bootstrap_summary.json")) as f:
    summ = json.load(f)

lengths = raw["config"]["lengths"]
survivals = {int(m): raw["survivals"][str(m)] for m in lengths}

fit = summ["fit_full"]
A, B, ff = fit["A"], fit["B"], fit["f"]
r_ref = summ["fit_full"]["r"]

# --- Plot 1: RB decay curve ---
fig, ax = plt.subplots(figsize=(6.5, 4.2))
xs = np.array(lengths)
means = np.array([np.mean(survivals[m]) for m in lengths])
stds  = np.array([np.std(survivals[m]) / np.sqrt(len(survivals[m])) for m in lengths])
ax.errorbar(xs, means, yerr=stds, fmt='o', capsize=3, label='simulation (N=100)')
mm = np.linspace(1, max(lengths), 200)
ax.plot(mm, A * ff**mm + B, '-', label=f'fit  A·f^m+B\n f={ff:.4f}  r={r_ref:.4f}')
ax.set_xlabel('sequence length m')
ax.set_ylabel('survival probability P(|00>)')
ax.set_title('2-qubit RB decay (Qiskit Aer, depolarizing)')
ax.legend()
fig.tight_layout()
fig.savefig(os.path.join(EV, "rb_decay.png"), dpi=140)
print("Wrote rb_decay.png")

# --- Plot 2: r_fit vs N ---
Ns = sorted(int(k) for k in summ["per_N"].keys())
r_means = [summ["per_N"][str(N)]["r_mean"] for N in Ns]
r_stds  = [summ["per_N"][str(N)]["r_std"]  for N in Ns]

fig, ax = plt.subplots(figsize=(6.5, 4.2))
ax.errorbar(Ns, r_means, yerr=r_stds, fmt='s-', capsize=3, color='tab:red')
ax.axhline(r_ref, ls='--', color='k', alpha=0.5, label=f'reference r={r_ref:.4f}')
ax.set_xlabel('N (# random sequences per length m)')
ax.set_ylabel('fitted infidelity r  (bootstrap mean ± std)')
ax.set_title('Precision of RB fit vs number of sequences')
ax.legend()
fig.tight_layout()
fig.savefig(os.path.join(EV, "r_vs_N.png"), dpi=140)
print("Wrote r_vs_N.png")

# --- Plot 3: relative std vs N ---
rel_stds = [summ["per_N"][str(N)]["relative_std"] for N in Ns]
fig, ax = plt.subplots(figsize=(6.5, 4.2))
ax.plot(Ns, rel_stds, 'o-', color='tab:blue')
for tol, ls in [(0.10, ':'), (0.05, '--'), (0.02, '-.')]:
    ax.axhline(tol, ls=ls, color='gray', alpha=0.5,
               label=f'{int(tol*100)}% relative precision')
ax.set_xlabel('N (# random sequences)')
ax.set_ylabel('relative std of r-fit  (std / mean)')
ax.set_title('Relative precision of r vs N')
ax.legend()
fig.tight_layout()
fig.savefig(os.path.join(EV, "rel_std_vs_N.png"), dpi=140)
print("Wrote rel_std_vs_N.png")
