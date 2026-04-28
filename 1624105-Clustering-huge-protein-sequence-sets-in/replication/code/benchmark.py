"""Scaling benchmark: Linclust (Python) vs naive O(N^2) greedy clustering.

Generates synthetic protein datasets of increasing size with known
ground-truth family assignments, runs both clusterers, records wall-clock
runtime and cluster-quality metrics, and produces the runtime-vs-N plot
that is the paper's headline result (Fig. 2 in Steinegger & Söding 2018).
"""
from __future__ import annotations
import json
import os
import sys
import time

import matplotlib.pyplot as plt
import numpy as np

from linclust_py import (
    ClusterResult,
    gen_dataset,
    linclust,
    naive_cluster,
    pairwise_prf,
)

OUT = os.path.join(os.path.dirname(__file__), "..", "results")
os.makedirs(OUT, exist_ok=True)


def run_one(N: int, seqs_per_family: int = 10, length: int = 100,
            mut_rate: float = 0.15, seed: int = 0,
            do_naive: bool = True):
    n_families = max(1, N // seqs_per_family)
    seqs, gt = gen_dataset(n_families, seqs_per_family, length=length,
                           mut_rate=mut_rate, seed=seed)
    # Truncate if off-by-a-few
    seqs = seqs[:N]; gt = gt[:N]

    lr = linclust(seqs, k=5, m=30, min_identity=0.6)
    l_q = pairwise_prf(lr.assignments, gt)

    out = {
        "N": N,
        "linclust_time": lr.runtime_s,
        "linclust_reps": len(lr.representatives),
        "linclust_f1": l_q["f1"],
        "linclust_precision": l_q["precision"],
        "linclust_recall": l_q["recall"],
    }
    if do_naive:
        nr = naive_cluster(seqs, min_identity=0.6)
        n_q = pairwise_prf(nr.assignments, gt)
        out.update({
            "naive_time": nr.runtime_s,
            "naive_reps": len(nr.representatives),
            "naive_f1": n_q["f1"],
            "naive_precision": n_q["precision"],
            "naive_recall": n_q["recall"],
        })
    print(out, flush=True)
    return out


def main():
    sizes = [500, 1000, 2000, 4000, 8000, 16000]
    # only run naive up to a cap; above that it would blow the time budget
    naive_cap = 4000
    # add linclust-only large sizes to show linearity
    linclust_extra = [32000, 64000]

    results = []
    for N in sizes:
        results.append(run_one(N, do_naive=(N <= naive_cap)))
    for N in linclust_extra:
        results.append(run_one(N, do_naive=False))

    with open(os.path.join(OUT, "benchmark.json"), "w") as f:
        json.dump(results, f, indent=2)

    # ---------- plots ----------
    Ns_l = [r["N"] for r in results]
    t_l = [r["linclust_time"] for r in results]
    Ns_n = [r["N"] for r in results if "naive_time" in r]
    t_n = [r["naive_time"] for r in results if "naive_time" in r]

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    ax = axes[0]
    ax.plot(Ns_l, t_l, "o-", label="Linclust-py (ours)", color="C0")
    ax.plot(Ns_n, t_n, "s-", label="Naive O(N²) greedy", color="C3")
    ax.set_xlabel("Number of sequences N")
    ax.set_ylabel("Wall-clock runtime (s)")
    ax.set_title("Clustering runtime vs. dataset size")
    ax.grid(alpha=0.3)
    ax.legend()

    ax = axes[1]
    ax.loglog(Ns_l, t_l, "o-", label="Linclust-py (ours)", color="C0")
    ax.loglog(Ns_n, t_n, "s-", label="Naive O(N²) greedy", color="C3")
    # reference slopes
    xs = np.array([min(Ns_l), max(Ns_l)])
    # calibrate linear reference to first linclust point
    ref_lin = t_l[0] * xs / Ns_l[0]
    ax.loglog(xs, ref_lin, "--", color="C0", alpha=0.4, label="O(N) reference")
    if len(Ns_n) >= 2:
        ref_quad = t_n[0] * (xs / Ns_n[0]) ** 2
        ax.loglog(xs, ref_quad, "--", color="C3", alpha=0.4, label="O(N²) reference")
    ax.set_xlabel("N (log)")
    ax.set_ylabel("runtime s (log)")
    ax.set_title("log–log scaling")
    ax.grid(alpha=0.3, which="both")
    ax.legend()

    fig.tight_layout()
    fig_path = os.path.join(OUT, "scaling.pdf")
    fig.savefig(fig_path)
    fig.savefig(os.path.join(OUT, "scaling.png"), dpi=150)
    print("saved", fig_path)

    # Quality plot
    fig2, ax = plt.subplots(figsize=(6, 4))
    ax.plot(Ns_l, [r["linclust_f1"] for r in results], "o-",
            label="Linclust-py F1", color="C0")
    ax.plot(Ns_n, [r["naive_f1"] for r in results if "naive_f1" in r],
            "s-", label="Naive F1", color="C3")
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("N")
    ax.set_ylabel("Pair-counting F1 vs. ground truth")
    ax.set_title("Cluster quality")
    ax.grid(alpha=0.3)
    ax.legend()
    fig2.tight_layout()
    fig2.savefig(os.path.join(OUT, "quality.pdf"))
    fig2.savefig(os.path.join(OUT, "quality.png"), dpi=150)

    # Fit log-log slopes
    def fit_slope(xs, ys):
        lx = np.log(xs); ly = np.log(ys)
        s, b = np.polyfit(lx, ly, 1)
        return float(s), float(b)
    sl_lin, _ = fit_slope(Ns_l, t_l)
    sl_nai = fit_slope(Ns_n, t_n)[0] if len(Ns_n) >= 2 else float("nan")
    print(f"log-log slope: linclust-py = {sl_lin:.3f}  naive = {sl_nai:.3f}")
    with open(os.path.join(OUT, "slopes.json"), "w") as f:
        json.dump({"linclust_slope": sl_lin, "naive_slope": sl_nai,
                   "linclust_sizes": Ns_l, "naive_sizes": Ns_n}, f, indent=2)


if __name__ == "__main__":
    main()
