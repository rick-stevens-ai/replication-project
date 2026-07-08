"""Plot strong-scaling curves for distributed 3-WL on chiatta00.

Reads results/wl3_mpi_chiatta00.jsonl and produces:
  figures/wl3_strong_scaling.pdf
"""
from __future__ import annotations
import json, os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results" / "wl3_mpi_chiatta00.jsonl"
FIGDIR = ROOT / "figures"
FIGDIR.mkdir(exist_ok=True)

records = []
with open(RESULTS) as f:
    for line in f:
        line = line.strip()
        if line:
            records.append(json.loads(line))

# Take steady-state per-iteration time (median of last two iters)
def steady(rec):
    t = rec["iter_times_ms"]
    if len(t) >= 2:
        return float(np.median(t[-2:]))
    return float(t[-1])

def steady_compute(rec):
    t = rec["iter_compute_ms"]
    if len(t) >= 2:
        return float(np.median(t[-2:]))
    return float(t[-1])

# Group: pure-MPI runs only (we'll detect by no hybrid label; we tag via threads later).
# We can identify pure-MPI vs hybrid by whether the rec was generated under OMP_NUM_THREADS=1.
# Since we didn't store thread count in JSONL, we infer from rank/n combos. Strong-scaling
# pure-MPI runs are: n in {30,60,80,100} with single seed=7, and ranks in {1,2,4,8,16,32,64}.
# Hybrid runs at n=100 will have duplicate (n=100,P) entries; we keep the FIRST occurrence
# of each (n,P) which corresponds to the pure-MPI sweep.

curves: dict[int, list[tuple[int, float, float]]] = {}
seen_keys: set[tuple[int, int]] = set()
for r in records:
    n = r["n"]; p = r["ranks"]
    key = (n, p)
    if key in seen_keys:
        continue  # skip duplicates from hybrid sweep
    seen_keys.add(key)
    curves.setdefault(n, []).append((p, steady(r), steady_compute(r)))

for n in curves:
    curves[n].sort()

# --- Plot 1: time vs ranks (log-log) for each n
fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

ax = axes[0]
colors = plt.cm.viridis(np.linspace(0.1, 0.85, len(curves)))
for (n, pts), c in zip(sorted(curves.items()), colors):
    P = [x[0] for x in pts]; T = [x[1] for x in pts]; Tc = [x[2] for x in pts]
    ax.loglog(P, T, "o-", color=c, label=f"n={n} (total)")
    ax.loglog(P, Tc, "o--", color=c, alpha=0.5, label=f"n={n} (compute only)")
ax.set_xlabel("MPI ranks (chiatta00, 1 thread/rank)")
ax.set_ylabel("Steady-state ms / iter")
ax.set_title("3-WL distributed strong scaling — chiatta00")
ax.grid(True, which="both", alpha=0.3)
ax.legend(fontsize=8, ncol=2)

# --- Plot 2: speedup vs ranks at n=100, with paper's 2-WL Table 4 paper curve and our previous 2-WL
ax = axes[1]
for n in sorted(curves):
    pts = curves[n]
    if len(pts) < 2:
        continue
    P = np.array([x[0] for x in pts])
    T = np.array([x[1] for x in pts])
    speedup = T[0] / T  # relative to ranks=1
    ax.plot(P, speedup, "o-", label=f"3-WL ours, n={n}")
ax.plot([1, 64], [1, 64], "k:", alpha=0.4, label="ideal linear")

# Paper's 2-WL single-node Table 4 averages (relative to p=1):
paper_p = [1, 2, 4, 8, 16, 20]
paper_s = [1.00, 2.38, 4.26, 7.64, 13.20, 16.06]
ax.plot(paper_p, paper_s, "s--", color="gray", label="paper 2-WL Table 4 (1 node, 20 cores)")

ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel("MPI ranks")
ax.set_ylabel("Speedup vs 1 rank")
ax.set_title("Strong-scaling speedup")
ax.grid(True, which="both", alpha=0.3)
ax.legend(fontsize=8)

plt.tight_layout()
out = FIGDIR / "wl3_strong_scaling.pdf"
plt.savefig(out, bbox_inches="tight")
plt.savefig(FIGDIR / "wl3_strong_scaling.png", dpi=150, bbox_inches="tight")
print(f"wrote {out}")

# Print summary table for inclusion in report
print("\n=== Steady-state ms/iter, pure MPI, 1 thread/rank ===")
print(f"{'n':>4} | " + " | ".join(f"P={p:>3d}" for p in [1,2,4,8,16,32,64]))
for n in sorted(curves):
    pts = dict((p, t) for (p, t, _) in curves[n])
    row = f"{n:>4} | " + " | ".join(f"{pts.get(p, float('nan')):>5.0f}" for p in [1,2,4,8,16,32,64])
    print(row)
print()

# Print hybrid table (n=100 duplicates)
print("=== Hybrid runs at n=100 (later occurrences) ===")
hybrid_seen = set()
n100_recs = [r for r in records if r["n"] == 100]
# First record per rank is pure-MPI; subsequent are hybrid
counts = {}
for r in n100_recs:
    p = r["ranks"]; counts[p] = counts.get(p, 0) + 1
    if counts[p] >= 2:
        print(f"  ranks={p}, steady={steady(r):.1f} ms (compute={steady_compute(r):.1f} ms)")
