#!/usr/bin/env python3
"""Make verification figures for the replication."""
from __future__ import annotations
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

FIGDIR = Path(__file__).resolve().parent.parent / "figures"
FIGDIR.mkdir(exist_ok=True)

# Re-run Eq. 1 cross-check (lightweight, no import gymnastics)
HALF_LIFE_H = {
    "125I":  60.140 * 24,
    "123I":  13.2235,
    "111In": 67.317,
    "99mTc":  6.0067,
    "64Cu":  12.7012,
}
DSB_PER_DECAY_025 = {
    "125I":  1.94, "123I": 1.20, "111In": 1.09, "99mTc": 0.378, "64Cu": 0.171,
}
PAPER_N0 = {
    "125I":  17416, "123I": 451, "111In": 1625, "99mTc": 1095, "64Cu": 3107,
}
PAPER_BQ = {
    "125I":  2.32, "123I": 6.58, "111In": 4.65, "99mTc": 35.0, "64Cu": 47.1,
}

calc_N0 = []
calc_Bq = []
labels  = []
paper_N0_l = []
paper_Bq_l = []
for nuc in ["125I", "123I", "111In", "99mTc", "64Cu"]:
    t12 = HALF_LIFE_H[nuc]
    lam_h = math.log(2) / t12
    lam_s = math.log(2) / (t12 * 3600.0)
    N0 = 194.0 / ((1 - math.exp(-lam_h * 24)) * DSB_PER_DECAY_025[nuc]) * 2.0
    Bq = lam_s * N0 * 1e3
    calc_N0.append(N0); calc_Bq.append(Bq); labels.append(nuc)
    paper_N0_l.append(PAPER_N0[nuc]); paper_Bq_l.append(PAPER_BQ[nuc])

# Figure 1: N0 calc vs paper (loglog)
fig, ax = plt.subplots(1, 2, figsize=(10, 4.5))
ax[0].scatter(paper_N0_l, calc_N0, s=80, c="tab:blue", zorder=3)
mx = max(max(paper_N0_l), max(calc_N0)) * 1.5
mn = min(min(paper_N0_l), min(calc_N0)) * 0.5
ax[0].plot([mn, mx], [mn, mx], "k--", lw=1, label="y=x")
for n, x, y in zip(labels, paper_N0_l, calc_N0):
    ax[0].annotate(n, (x, y), xytext=(6, 6), textcoords="offset points", fontsize=9)
ax[0].set_xscale("log"); ax[0].set_yscale("log")
ax[0].set_xlim(mn, mx); ax[0].set_ylim(mn, mx)
ax[0].set_xlabel("$N_0$ reported (Table 2)")
ax[0].set_ylabel("$N_0$ recomputed from Eq. 1")
ax[0].set_title("Lethal-damage atom count: this work vs paper")
ax[0].legend()
ax[0].grid(True, alpha=0.3, which="both")

ax[1].scatter(paper_Bq_l, calc_Bq, s=80, c="tab:orange", zorder=3)
mx2 = max(max(paper_Bq_l), max(calc_Bq)) * 1.5
mn2 = min(min(paper_Bq_l), min(calc_Bq)) * 0.5
ax[1].plot([mn2, mx2], [mn2, mx2], "k--", lw=1, label="y=x")
for n, x, y in zip(labels, paper_Bq_l, calc_Bq):
    ax[1].annotate(n, (x, y), xytext=(6, 6), textcoords="offset points", fontsize=9)
ax[1].set_xscale("log"); ax[1].set_yscale("log")
ax[1].set_xlim(mn2, mx2); ax[1].set_ylim(mn2, mx2)
ax[1].set_xlabel("Initial activity (Bq $\\times 10^{-3}$) reported")
ax[1].set_ylabel("Recomputed from Eq. 1")
ax[1].set_title("Initial activity per cell")
ax[1].legend(); ax[1].grid(True, alpha=0.3, which="both")
fig.tight_layout()
fig.savefig(FIGDIR / "fig01_eq1_crosscheck.png", dpi=140)
print(f"wrote {FIGDIR/'fig01_eq1_crosscheck.png'}")

# Figure 2: DSB:SSB ratio from track-correlated synthesizer vs literature regimes
rng = np.random.default_rng(42)
def synth(n_tracks, mcpt, mspc, ext, genome_bp=6_080_000_000):
    all_pos = []; all_str = []
    for _ in range(n_tracks):
        start = rng.integers(0, genome_bp - 100_000)
        n_c = max(1, rng.poisson(mcpt))
        steps = rng.exponential(200.0, n_c).astype(np.int64) + 1
        centers = start + np.cumsum(steps)
        for c in centers:
            k = rng.poisson(mspc)
            if k == 0: continue
            offs = rng.integers(-ext, ext+1, size=k)
            all_pos.extend((c + offs).tolist())
            all_str.extend(rng.integers(0, 2, size=k).tolist())
    return np.array(all_pos, dtype=np.int64), np.array(all_str, dtype=np.int8)

def score(pos, strd, w=10):
    order = np.argsort(pos); pos = pos[order]; strd = strd[order]
    n = len(pos); used = np.zeros(n, dtype=bool); dsb = 0
    for i in range(n):
        if used[i]: continue
        for j in range(i+1, n):
            if used[j]: continue
            if pos[j] - pos[i] > w: break
            if strd[j] != strd[i]:
                used[i] = True; used[j] = True; dsb += 1; break
    return dsb

scenarios = [
    ("low-LET",          2000, 20, 0.15, 3, "tab:blue"),
    ("mid-LET",           500, 30, 0.30, 3, "tab:orange"),
    ("125I-like Auger",    50, 40, 0.80, 3, "tab:red"),
    ("64Cu-like",         500, 10, 0.30, 3, "tab:green"),
]
fig2, ax2 = plt.subplots(figsize=(8, 5))
xpos = np.arange(len(scenarios))
ratios = []
for name, nt, mcpt, mspc, ext, col in scenarios:
    pos, strd = synth(nt, mcpt, mspc, ext)
    n_dsb = score(pos, strd, 10)
    r = n_dsb / max(1, len(pos))
    ratios.append(r)
bars = ax2.bar(xpos, ratios, color=[s[5] for s in scenarios])
ax2.set_xticks(xpos); ax2.set_xticklabels([s[0] for s in scenarios])
ax2.set_ylabel("DSB / SSB (proximity rule, $\\leq$ 10 bp opposite strand)")
ax2.set_title("Synthetic track-correlated DSB:SSB ratios\n(method reproduction of Carrasco-Hernandez 2023 scoring rule)")
ax2.axhspan(0.02, 0.05, alpha=0.12, color="blue", label="literature low-LET range")
ax2.axhspan(0.10, 0.30, alpha=0.10, color="red",  label="literature high-LET / near-DNA Auger")
for b, r in zip(bars, ratios):
    ax2.text(b.get_x()+b.get_width()/2, r+0.005, f"{r:.3f}", ha="center", fontsize=10)
ax2.legend(loc="upper left")
ax2.grid(True, alpha=0.3, axis="y")
fig2.tight_layout()
fig2.savefig(FIGDIR / "fig02_dsb_ssb_ratio.png", dpi=140)
print(f"wrote {FIGDIR/'fig02_dsb_ssb_ratio.png'}")
