#!/usr/bin/env python3
"""Produce two summary figures for the replication report."""
import json
import os
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "results.json")) as f:
    R = json.load(f)
with open(os.path.join(HERE, "results_wreath_pgm.json")) as f:
    W = json.load(f)

# ---------------- Figure 1: Δ_char vs t, for GI setting ---------------
fig, ax = plt.subplots(figsize=(6, 4))
gi = W["graph_iso_wreath_char_sweep"]
# organize by n_graph
by_n = {}
for r in gi:
    by_n.setdefault(r["n_underlying_graph"], []).append(r)
for n, rows in sorted(by_n.items()):
    rows.sort(key=lambda r: r["t"])
    ts = [r["t"] for r in rows]
    bs = [r["delta_char_bound"] for r in rows]
    ax.semilogy(ts, bs, marker="o", label=f"n_graph={n}, |S_{{2n}}|={rows[0]['|S_{2n}|']}")
ax.axhline(1.0, color="k", linestyle="--", alpha=0.5, label="bound = 1")
ax.set_xlabel("t = # coset states")
ax.set_ylabel("Δ_char(n, t) = (2^t/|G|) · Σ_τ d_τ|χ_τ(h)|  (upper bound on 1-norm)")
ax.set_title("Theorem 12 RHS for GI (G = S_{2n}, h = (2^n))")
ax.legend(fontsize=8)
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_delta_char_gi.png"), dpi=140)
plt.close(fig)

# ---------------- Figure 2: t*(n) vs n·log₂n (linear fit) -------------
fig, ax = plt.subplots(figsize=(6, 4))
ts = W["t_star_growth_graph_iso"]
xs = np.array([r["n_log2_n"] for r in ts])
ys = np.array([r["t_star"] for r in ts])
ns = np.array([r["n_graph"] for r in ts])
ax.plot(xs, ys, "o-", label="t*(n) = log₂(|S_{2n}| / Σd|χ|)")
# linear fit through origin
slope = np.sum(xs * ys) / np.sum(xs ** 2)
xline = np.linspace(0, xs.max() * 1.05, 100)
ax.plot(xline, slope * xline, "r--", label=f"linear fit: t* ≈ {slope:.3f}·(n·log₂n)")
for x, y, n in zip(xs, ys, ns):
    ax.annotate(f"n={n}", (x, y), xytext=(4, -8), textcoords="offset points", fontsize=8)
ax.set_xlabel("n · log₂(n)")
ax.set_ylabel("t*(n) = smallest t with Δ_char ≥ 1")
ax.set_title("Threshold t*(n) grows Θ(n log n) — matches paper Corollary 14")
ax.legend()
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_t_star_scaling.png"), dpi=140)
plt.close(fig)

# ---------------- Figure 3: exact LHS vs bound (S_n setting) ---------------
fig, ax = plt.subplots(figsize=(6, 4))
ev = R["exact_trace_distance_verification"]
# 1-norm LHS vs bound at fixed t=1 across n=2,3,4
by_t = {}
for r in ev:
    by_t.setdefault(r["t"], []).append(r)
for t, rows in sorted(by_t.items()):
    rows.sort(key=lambda r: r["n"])
    ns = [r["n"] for r in rows]
    lhs = [r["trace_distance_LHS"] for r in rows]   # this is 1-norm in our code
    rhs = [r["delta_char_bound_RHS"] for r in rows]
    ax.semilogy(ns, lhs, "o-", label=f"t={t}: exact 1-norm ||·||₁")
    ax.semilogy(ns, rhs, "s--", label=f"t={t}: Thm 12 bound")
ax.set_xlabel("n (S_n)")
ax.set_ylabel("|| E_a ρ_{H^a}^{⊗t} − ρ_{{1}}^{⊗t} ||₁")
ax.set_title("Exact LHS ≤ Theorem-12 RHS (S_n setting)")
ax.legend(fontsize=8)
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_lhs_vs_rhs.png"), dpi=140)
plt.close(fig)

print("Wrote 3 figures.")
