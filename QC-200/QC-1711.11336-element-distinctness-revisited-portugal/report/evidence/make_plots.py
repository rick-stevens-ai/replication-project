#!/usr/bin/env python3
"""Produce log-log query-count plot + psucc-vs-N plot for the report."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent
with open(OUT / "results.json") as f:
    R = json.load(f)

sweep = R["sweep"]
N = np.array([x["N"] for x in sweep])
r = np.array([x["r"] for x in sweep])
t1 = np.array([x["t1"] for x in sweep])
t2 = np.array([x["t2"] for x in sweep])
Q = np.array([x["queries_estimate"] for x in sweep])
psucc = np.array([x["psucc_final"] for x in sweep])

fit_mask = N >= 15
slope, intercept = np.polyfit(np.log(N[fit_mask]), np.log(Q[fit_mask]), 1)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Panel 1: log-log query count vs N with fit
ax1.loglog(N, Q, "o", ms=7, label="Portugal reduced-subspace sim (this work)")
Nfit = np.logspace(np.log10(N[fit_mask].min()), np.log10(N.max()), 100)
ax1.loglog(
    Nfit,
    np.exp(intercept) * Nfit ** slope,
    "-",
    color="C1",
    label=f"fit: Q ~ N^{{{slope:.3f}}} (fit N>=15)",
)
# reference N^(2/3) line, normalized to match at N=100
ref_N = 100.0
ref_Q_at_100 = np.exp(intercept) * ref_N ** slope
ax1.loglog(
    Nfit,
    ref_Q_at_100 * (Nfit / ref_N) ** (2 / 3),
    "--",
    color="C2",
    alpha=0.7,
    label="Ambainis theory: N^{2/3}",
)
ax1.set_xlabel("List size N")
ax1.set_ylabel("Total queries Q = r + t1*t2")
ax1.set_title("Query complexity vs N (log-log)\nElement 2-distinctness, Portugal (2017) reduction")
ax1.legend(loc="upper left", fontsize=9)
ax1.grid(True, which="both", alpha=0.3)

# Panel 2: success probability approaching 1
ax2.semilogx(N, psucc, "o-", ms=6, color="C3", label="p_success at optimal t1")
ax2.axhline(1.0, color="k", linestyle=":", alpha=0.5, label="theoretical limit 1")
ax2.set_xlabel("List size N")
ax2.set_ylabel("Success probability")
ax2.set_ylim(0, 1.05)
ax2.set_title(f"Success probability vs N\n1 - psucc = O(r^(-1/k)), k=2")
ax2.legend(loc="lower right", fontsize=9)
ax2.grid(True, alpha=0.3)

fig.suptitle(
    "Independent replication of Portugal (2017) 'Element Distinctness Revisited' "
    "arXiv:1711.11336",
    fontsize=11,
    y=1.02,
)
fig.tight_layout()
fig.savefig(OUT / "portugal_replication.png", dpi=140, bbox_inches="tight")
fig.savefig(OUT / "portugal_replication.pdf", bbox_inches="tight")
print(f"Saved: {OUT / 'portugal_replication.png'}")
print(f"Saved: {OUT / 'portugal_replication.pdf'}")
print(f"Fit slope: {slope:.4f}  (theory 2/3 = 0.6667)")
