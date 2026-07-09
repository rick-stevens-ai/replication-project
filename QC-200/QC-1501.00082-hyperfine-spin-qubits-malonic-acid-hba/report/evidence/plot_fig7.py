#!/usr/bin/env python3
"""Reproduce paper Fig. 7 'Theory' curve (black dashed) using our HBAC simulator."""
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "hbac_results.json")) as f:
    R = json.load(f)

curve = R["fig7_like_curve_3q"]
ratios = curve["ratio_pol_over_eps_b_per_round"]
rounds = list(range(len(ratios)))

# Paper's theoretical trajectory (Fig 7 black dashed): 1 (r=0), 1.5, 1.75, 1.875, ..., -> 2
paper_theory = [2 - 0.5 * (0.5 ** (r // 2 * 2 + (0 if r == 0 else 0))) for r in rounds]
# Cleaner: PPA on n=3 gives at round r the ratio 2 - 2*(1/2)^ceil((r+1)/... )
# The recurrence I saw: 1, 1.5, 1.5, 1.75, 1.75, 1.875, ...  = 2 - 1/2^ceil(r/2)
paper_theory = [1.0] + [2 - (0.5) ** ((r + 1) // 2) for r in range(1, len(ratios))]

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(rounds, ratios, "o-", label="This replication (numpy PPA)")
ax.plot(rounds, paper_theory, "k--", label=r"Paper 'Theory': $2 - 2^{-\lceil r/2\rceil}$")
ax.axhline(2.0, color="gray", ls=":", label=r"Asymptote $2\epsilon_b$")
ax.axhline(1.5, color="gray", ls=":")
ax.set_xlabel("HBAC round r")
ax.set_ylabel(r"$\epsilon_{Cm}/\epsilon_b$ (target/bath polarization ratio)")
ax.set_title("3-qubit HBAC (idealized) — replication of paper Fig. 7 black-dashed curve")
ax.set_ylim(0.9, 2.1)
ax.legend(loc="lower right", fontsize=8)
ax.grid(True, alpha=0.3)
fig.tight_layout()
out = os.path.join(HERE, "fig7_replication.png")
fig.savefig(out, dpi=140)
print(f"[ok] wrote {out}")
