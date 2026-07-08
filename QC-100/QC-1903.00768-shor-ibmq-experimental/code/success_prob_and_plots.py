#!/usr/bin/env python3
"""
Compute Shor 'success probability' (paper's second lens) and generate
probability-vs-phase plots + SSO-vs-r plots analogous to paper Figs. 4-7.

Success prob := P( phase s such that s/Q approximated by k/r via continued
fractions gives back the correct period r ). For our compiled small-N cases
we count the paper's "good phases" directly:
  - N=15,a=2 (r=4, Q=8): good phases = {0, 2, 4, 6} (peaks of ideal QPE)
  - N=15,a=11 (r=2, Q=8): good phases = {0, 4}
  - N=21,a=2 (r=6, Q=8): good phases = {0, 1, 3, 4, 5, 7} - all s such
    that s/Q rounded to nearest k/r gives r. Practically: since r=6 does
    not divide 8, we use the paper's convention: good phase = any s such
    that continued-fraction convergent of s/Q with denominator <= N/2
    yields r=6.
"""

import json, os, sys
from pathlib import Path
from fractions import Fraction
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
EVID = HERE.parent / "report" / "evidence"

def good_phases(N: int, r: int, Q: int) -> set:
    """Phases whose continued-fraction convergent (denom<=N) yields r."""
    good = set()
    for s in range(Q):
        frac = Fraction(s, Q).limit_denominator(N)
        if frac.denominator == r:
            good.add(s)
    # Special-case r divides Q: all comb peaks are exact
    if Q % r == 0:
        good.update(j * (Q // r) for j in range(r))
    return good

def success_prob(probs, good_set):
    return float(sum(probs[s] for s in good_set))

with open(EVID / "shor_replication_results.json") as f:
    results = json.load(f)

# Compute success prob per experiment
success_table = []
for label, res in results.items():
    if "error" in res:
        continue
    N, r, Q = res["N"], res["r_true"], 2**res["n_bits"]
    good = good_phases(N, r, Q)
    p_success = success_prob(res["probs"], good)
    success_table.append({
        "label": label, "N": N, "a": res["a"], "r_true": r,
        "depol_1q": res["depol_1q"], "depol_2q": res["depol_2q"],
        "good_phases": sorted(good),
        "success_prob": p_success,
        "best_r_by_sso": res["best_r_by_sso"],
        "best_sso": res["best_sso"],
        "sso_at_r_true": res["sso_at_true_r"],
    })

print(f"{'label':38s} {'success_prob':>13s} {'best_SSO':>10s} {'sso@r_true':>12s} {'best_r':>7s} {'r_true':>7s}")
for row in success_table:
    print(f"{row['label']:38s} {row['success_prob']:>13.4f} {row['best_sso']:>10.4f} {row['sso_at_r_true']:>12.4f} {row['best_r_by_sso']:>7d} {row['r_true']:>7d}")

with open(EVID / "success_prob_summary.json", "w") as f:
    json.dump(success_table, f, indent=2)

# Plot 1: probability-vs-phase for the three noiseless + one noisy per case
# 3 (N,a) x 4 noise levels -> 3x4 grid
cases = [("N=15,a=2", 15, 2, 4),
         ("N=15,a=11", 15, 11, 2),
         ("N=21,a=2", 21, 2, 6)]
noise_labels = ["noiseless", "depol_p=1e-4", "depol_p=1e-3", "depol_p=1e-2"]

fig, axes = plt.subplots(3, 4, figsize=(16, 9))
for i, (case, N, a, r) in enumerate(cases):
    for j, nl in enumerate(noise_labels):
        key = f"{case},{nl}"
        if key not in results:
            continue
        res = results[key]
        probs = np.array(res["probs"])
        Q = 2**res["n_bits"]
        # theoretical for r_true
        from shor_replicate import theoretical_distribution
        th = theoretical_distribution(r, res["n_bits"])
        ax = axes[i][j]
        idx = np.arange(Q)
        w = 0.4
        ax.bar(idx - w/2, probs, width=w, label="sim", color="tab:blue")
        ax.bar(idx + w/2, th, width=w, label=f"theory (r={r})", color="tab:orange", alpha=0.8)
        ax.set_title(f"{case}  {nl}\nSSO@r={res['sso_at_true_r']:.3f}  best_r={res['best_r_by_sso']}", fontsize=9)
        ax.set_xlabel("phase s")
        ax.set_ylabel("prob")
        ax.set_ylim(0, max(0.55, probs.max()*1.15))
        if i == 0 and j == 0:
            ax.legend(fontsize=8)
fig.suptitle("Shor semi-classical QPE: simulated (Qiskit Aer) vs theoretical distribution\n"
             "arXiv:1903.00768 replication — compiled Shor for N=15, 21 with depolarizing noise", fontsize=11)
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig(EVID / "shor_probability_plots.png", dpi=120)
print(f"\nWrote {EVID / 'shor_probability_plots.png'}")

# Plot 2: SSO vs r (analog of paper Figs 4c, 5c, 6c) for noiseless case
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for i, (case, N, a, r_true) in enumerate(cases):
    key = f"{case},noiseless"
    if key not in results:
        continue
    res = results[key]
    sso_by_r = {int(k): float(v) for k, v in res["sso_by_r"].items()}
    rs = sorted(sso_by_r)
    ax = axes[i]
    bars = ax.bar(rs, [sso_by_r[r] for r in rs], color=["tab:green" if r == r_true else "tab:blue" for r in rs])
    ax.set_title(f"{case} noiseless — best r={res['best_r_by_sso']} (true r={r_true})")
    ax.set_xlabel("candidate period r")
    ax.set_ylabel("SSO")
    ax.set_ylim(0, 1.05)
    for r_, s_ in sso_by_r.items():
        ax.text(r_, s_ + 0.02, f"{s_:.2f}", ha="center", fontsize=8)
fig.suptitle("SSO vs candidate period r  (Paper Figs 4c, 5c, 6c analog)")
fig.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig(EVID / "shor_sso_vs_r_noiseless.png", dpi=120)
print(f"Wrote {EVID / 'shor_sso_vs_r_noiseless.png'}")

# Plot 3: SSO vs noise-level per case (the noise-degradation story)
noise_levels = [0.0, 1e-4, 1e-3, 1e-2]
noise_x = [1e-6, 1e-4, 1e-3, 1e-2]  # for log-x plot with tiny offset for "noiseless"
fig, ax = plt.subplots(figsize=(8, 5))
for case, N, a, r_true in cases:
    ys_best = []
    ys_true = []
    for nl_label, nl in zip(noise_labels, noise_levels):
        key = f"{case},{nl_label}"
        if key in results:
            ys_best.append(results[key]["best_sso"])
            ys_true.append(results[key]["sso_at_true_r"])
        else:
            ys_best.append(np.nan)
            ys_true.append(np.nan)
    ax.plot(noise_x, ys_true, "o-", label=f"{case} SSO@r_true", linewidth=2)
    ax.plot(noise_x, ys_best, "x--", label=f"{case} best SSO", alpha=0.6)
ax.set_xscale("log")
ax.set_xlabel("depolarizing error rate per gate (1q & 2q)")
ax.set_ylabel("SSO")
ax.set_title("Shor SSO vs depolarizing noise (Qiskit Aer sim)\nDemonstrates paper's central story: more qubits/gates → faster SSO degradation")
ax.axvline(1e-3, color="gray", linestyle=":", alpha=0.5, label="typical NISQ ~1e-3")
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)
ax.set_ylim(0, 1.05)
fig.tight_layout()
fig.savefig(EVID / "shor_sso_vs_noise.png", dpi=120)
print(f"Wrote {EVID / 'shor_sso_vs_noise.png'}")

# Save success-prob summary text
with open(EVID / "success_prob_summary.txt", "w") as f:
    f.write(f"{'label':38s} {'success_prob':>13s} {'best_SSO':>10s} {'sso@r_true':>12s} {'best_r':>7s} {'r_true':>7s}\n")
    for row in success_table:
        f.write(f"{row['label']:38s} {row['success_prob']:>13.4f} {row['best_sso']:>10.4f} {row['sso_at_r_true']:>12.4f} {row['best_r_by_sso']:>7d} {row['r_true']:>7d}\n")

print("\nDone.")
