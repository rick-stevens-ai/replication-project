#!/usr/bin/env python3
"""Make replication plots comparing to paper Fig 5."""
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DIR = os.path.join(os.path.dirname(__file__), "..", "report", "evidence")
with open(os.path.join(DIR, "results.json")) as f:
    data = json.load(f)

results = data["results"]

def sel(basis, p):
    xs, ys_ps, ys_dr, ys_ld, ys_lp = [], [], [], [], []
    for r in results:
        if r["basis"] == basis and abs(r["p"] - p) < 1e-9:
            xs.append(r["rounds"])
            ys_ps.append(r["p_success"])
            ys_dr.append(r["mean_detector_rate"])
            ys_ld.append(r["logical_err_decoded"])
            ys_lp.append(r["logical_err_postsel"])
    order = np.argsort(xs)
    return (np.array(xs)[order], np.array(ys_ps)[order],
            np.array(ys_dr)[order], np.array(ys_ld)[order],
            np.array(ys_lp)[order])

p_list = sorted(set(r["p"] for r in results))

# Plot 1: p_success vs N cycles (mirrors Fig 5(c) of paper)
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
for basis, ax in zip(("Z", "X"), axes):
    for p in p_list:
        x, ps, dr, ld, lp = sel(basis, p)
        ax.semilogy(x, ps, "o-", label=f"p={p}")
    ax.set_xlabel("N (rounds)")
    ax.set_ylabel("Success prob $p_s$ (no detector fires)")
    ax.set_title(f"Basis {basis} — repl. of Fig 5(c)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8)
    # Overlay paper's approximate p_s(10) ~ 10^-4 experiment, ~6e-4 sim
    if basis == "Z":
        ax.axhline(1e-4, color="k", ls="--", lw=0.8, alpha=0.6)
        ax.axhline(6e-4, color="k", ls=":",  lw=0.8, alpha=0.6)
        ax.text(0.5, 1.3e-4, "paper exp $p_s(10)$~10$^{-4}$", fontsize=7)
        ax.text(0.5, 7.5e-4, "paper sim $p_s(10)$~6×10$^{-4}$", fontsize=7)
fig.tight_layout()
fig.savefig(os.path.join(DIR, "fig_success_vs_rounds.png"), dpi=150)
plt.close(fig)

# Plot 2: detector-event rate vs rounds -- our CENTRAL check of "repeated" detection.
# The claim is that detector rate is (approximately) constant across rounds:
# each round detects errors independently at the same rate.
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
for basis, ax in zip(("Z", "X"), axes):
    for p in p_list:
        x, ps, dr, ld, lp = sel(basis, p)
        ax.plot(x, dr, "o-", label=f"p={p}")
    ax.set_xlabel("N (rounds)")
    ax.set_ylabel("Mean detector-fire rate per detector")
    ax.set_title(f"Basis {basis} — 'repeated detection' central claim")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(os.path.join(DIR, "fig_detector_rate_vs_rounds.png"), dpi=150)
plt.close(fig)

# Plot 3: logical error rate vs N (decoded, no postselection).
# Approximate paper values: at their effective noise, logical error accumulates ~0.3%/cycle.
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
for basis, ax in zip(("Z", "X"), axes):
    for p in p_list:
        x, ps, dr, ld, lp = sel(basis, p)
        ax.plot(x, ld, "o-", label=f"p={p}")
    ax.set_xlabel("N (rounds)")
    ax.set_ylabel("Logical error rate (decoded, no postselection)")
    ax.set_title(f"Basis {basis} — logical error accumulation")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(os.path.join(DIR, "fig_logical_err_vs_rounds.png"), dpi=150)
plt.close(fig)

print("wrote plots to", DIR)
