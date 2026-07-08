#!/usr/bin/env python3
"""Analyze linear-in-p regime and produce plots for the noisy-VQE replication."""
import json
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

evidence = Path(__file__).resolve().parent.parent / "report" / "evidence"

runs = {
    "d=2": evidence / "main_n4_d2" / "results.json",
    "d=3": evidence / "main_n4_d3" / "results.json",
}
data = {k: json.loads(p.read_text()) for k, p in runs.items()}

# -------- Analysis: extract noise-induced shift, isolate from optimizer bias --------
analysis = {}
for label, d in data.items():
    p_arr = np.array([row["p"] for row in d["noisy_sweep"]])
    rel_arr = np.array([row["rel_err"] for row in d["noisy_sweep"]])
    # Noise-induced shift = (rel_err at p) - (rel_err at p=0) = purely the noise effect.
    # In terms of energy:
    E0 = d["E0_exact"]
    E_arr = np.array([row["E_noisy"] for row in d["noisy_sweep"]])
    E_at_zero = E_arr[np.argmin(p_arr)]
    delta_E = E_arr - E_at_zero  # noise-induced energy shift
    # For small p, expect delta_E ~ n_gates * p * (some factor)
    gates = d["ansatz_gates"]
    n_gates_eff = gates["cx_total"] + gates["single_qubit_rot_total"]

    # Fit delta_E = a * p in the small-p regime (p <= 3e-3)
    mask = (p_arr > 0) & (p_arr <= 3e-3)
    if mask.sum() >= 2:
        # Linear regression through origin: minimize sum((delta_E - a*p)^2)
        a = float(np.sum(p_arr[mask] * delta_E[mask]) / np.sum(p_arr[mask] ** 2))
    else:
        a = float("nan")

    per_gate_slope = a / n_gates_eff if n_gates_eff else float("nan")
    analysis[label] = {
        "d": d["d"],
        "n_qubits": d["n_qubits"],
        "E0_exact": E0,
        "E_noiseless_best": d["noiseless_best"]["E"],
        "ratio_E_over_E0": d["noiseless_best"]["ratio_E_over_E0"],
        "n_gates_total": n_gates_eff,
        "gates_breakdown": gates,
        "p": p_arr.tolist(),
        "E_noisy": E_arr.tolist(),
        "rel_err": rel_arr.tolist(),
        "delta_E_from_p0": delta_E.tolist(),
        "slope_delta_E_over_p_small_p": a,
        "slope_per_gate": per_gate_slope,
    }

# monotonicity check
for label, a in analysis.items():
    rel = np.array(a["rel_err"])
    mono = bool(np.all(np.diff(rel) >= 0))
    a["monotonic_in_p"] = mono

# Comparative: does d=3 (more gates) have larger noise-induced shift at each p than d=2?
d2 = analysis["d=2"]
d3 = analysis["d=3"]
noise_accum = []
for i, p in enumerate(d2["p"]):
    dE2 = d2["delta_E_from_p0"][i]
    dE3 = d3["delta_E_from_p0"][i]
    noise_accum.append({
        "p": p,
        "delta_E_d2": dE2,
        "delta_E_d3": dE3,
        "d3_gt_d2": abs(dE3) > abs(dE2),
    })

summary = {
    "per_run_analysis": analysis,
    "noise_accumulation_over_depth": noise_accum,
    "d2_greater_than_d3_gate_ratio": d3["n_gates_total"] / d2["n_gates_total"],
}

out_path = evidence / "analysis_summary.json"
out_path.write_text(json.dumps(summary, indent=2, default=float))
print(f"[write] {out_path}")

# -------- Plot 1: E_VQE(p) vs p, both d --------
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))

ax = axes[0]
for label, a in analysis.items():
    p_arr = np.array(a["p"])
    E_arr = np.array(a["E_noisy"])
    ax.plot(p_arr, E_arr, "o-", label=f"noisy VQE ({label}, {a['n_gates_total']} gates)")
ax.axhline(analysis["d=2"]["E0_exact"], color="k", linestyle="--", alpha=0.6, label=f"$E_0$ exact = {analysis['d=2']['E0_exact']:.3f}")
ax.set_xlabel("per-gate depolarizing error $p$")
ax.set_ylabel("$E_{VQE}(p)$")
ax.set_title("TIsing $n=4$, $J=h=1$ (PBC): VQE energy vs noise")
ax.set_xscale("symlog", linthresh=1e-4)
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

ax = axes[1]
for label, a in analysis.items():
    p_arr = np.array(a["p"])
    rel = np.array(a["rel_err"])
    ax.plot(p_arr, rel, "s-", label=f"{label}")
ax.set_xlabel("per-gate depolarizing error $p$")
ax.set_ylabel(r"$(E - E_0)/|E_0|$")
ax.set_title("Relative energy error vs $p$")
ax.set_xscale("symlog", linthresh=1e-4)
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

fig.tight_layout()
plot1 = evidence / "energy_vs_p.png"
fig.savefig(plot1, dpi=150)
print(f"[write] {plot1}")

# -------- Plot 2: linearity check --------
fig2, ax = plt.subplots(1, 1, figsize=(6, 4.2))
for label, a in analysis.items():
    p_arr = np.array(a["p"])
    delta = np.array(a["delta_E_from_p0"])
    ax.plot(p_arr, delta, "o-", label=f"$\\Delta E$ ({label})")
    # Linear fit line
    if not np.isnan(a["slope_delta_E_over_p_small_p"]):
        ps = np.linspace(0, max(p_arr), 100)
        ax.plot(ps, a["slope_delta_E_over_p_small_p"] * ps, "--", alpha=0.5,
                label=f"linear fit p≤3e-3 ({label}): slope={a['slope_delta_E_over_p_small_p']:.2f}")
ax.set_xlabel("per-gate depolarizing error $p$")
ax.set_ylabel(r"$\Delta E(p) = E_{VQE}(p) - E_{VQE}(0)$")
ax.set_title("Noise-induced energy shift vs $p$ (small-$p$ linearity)")
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)
fig2.tight_layout()
plot2 = evidence / "delta_E_vs_p_linearity.png"
fig2.savefig(plot2, dpi=150)
print(f"[write] {plot2}")

# Console summary
print("\n=== VERDICT-RELEVANT NUMBERS ===")
for label, a in analysis.items():
    print(f"{label}: n_gates={a['n_gates_total']}, monotonic_in_p={a['monotonic_in_p']}, "
          f"slope_dE/dp (small p)={a['slope_delta_E_over_p_small_p']:.3f}, "
          f"slope_per_gate={a['slope_per_gate']:.4f}")
print("\nNoise accumulation with depth (|delta E(d=3)| > |delta E(d=2)|?):")
for row in noise_accum:
    print(f"  p={row['p']:.2e}: dE_d2={row['delta_E_d2']:+.4e}  dE_d3={row['delta_E_d3']:+.4e}  d3>d2: {row['d3_gt_d2']}")
