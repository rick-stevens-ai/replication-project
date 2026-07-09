#!/usr/bin/env python3
"""Produce figures for the replication report."""
import json
import math
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main():
    here = Path(__file__).resolve().parent
    ev = (here.parent / "report" / "evidence").resolve()
    figs = (here.parent / "figures").resolve()
    figs.mkdir(exist_ok=True, parents=True)
    data = json.loads((ev / "results.json").read_text())
    sweep = None
    for t in data["tests"]:
        if t["name"] == "sweep_pgm_success":
            sweep = t["rows"]
    assert sweep is not None

    # Group by k
    by_k = {}
    for r in sweep:
        by_k.setdefault(r["k"], []).append(r)

    # Fig 1: PGM success prob vs N, one curve per k
    fig, ax = plt.subplots(figsize=(6, 4))
    colors = {2: "#c62828", 3: "#2e7d32", 4: "#1565c0"}
    for k in sorted(by_k):
        rows = sorted(by_k[k], key=lambda r: r["N"])
        Ns = [r["N"] for r in rows]
        ps = [r["p_success"] for r in rows]
        ax.plot(Ns, ps, "o-", color=colors.get(k, "gray"),
                label=f"k = {k}  (M = ⌊N^(1/k)⌋)")
    ax.set_xlabel("N (size of Z_N)")
    ax.set_ylabel("PGM success probability  (Eq. 15)")
    ax.set_title("Childs–van Dam PGM success probability\n"
                 "M chosen as ⌊N^(1/k)⌋ (paper regime, Lemma 2)")
    ax.grid(alpha=0.3)
    ax.set_ylim(0, 1)
    ax.legend()
    fig.tight_layout()
    fig.savefig(figs / "fig1_pgm_success_vs_N.png", dpi=140)
    plt.close(fig)

    # Fig 2: Lemma 2 fraction Pr(1<=eta<=4) vs N
    fig, ax = plt.subplots(figsize=(6, 4))
    for k in sorted(by_k):
        rows = sorted(by_k[k], key=lambda r: r["N"])
        Ns = [r["N"] for r in rows]
        ps = [r["lemma2_frac"] for r in rows]
        ax.plot(Ns, ps, "s-", color=colors.get(k, "gray"),
                label=f"k = {k}")
    ax.set_xlabel("N")
    ax.set_ylabel("Pr(1 ≤ η_w^x ≤ 4)  (Lemma 2)")
    ax.set_title("Fraction of matrix-sum instances with 1-4 solutions\n"
                 "M = ⌊N^(1/k)⌋")
    ax.grid(alpha=0.3)
    ax.set_ylim(0, 1)
    ax.legend()
    fig.tight_layout()
    fig.savefig(figs / "fig2_lemma2_fraction.png", dpi=140)
    plt.close(fig)

    # Fig 3: Show what happens when M is held constant (M=2, dihedral regime)
    # We already have k=3, k=4 curves for M=2 because floor(N^(1/k))=2 for a range of N.
    # Isolate those rows.
    fig, ax = plt.subplots(figsize=(6, 4))
    for k in (3, 4):
        rows = [r for r in by_k[k] if r["M"] == 2]
        rows = sorted(rows, key=lambda r: r["N"])
        if not rows:
            continue
        Ns = [r["N"] for r in rows]
        ps = [r["p_success"] for r in rows]
        ax.plot(Ns, ps, "d-", color=colors.get(k, "gray"),
                label=f"k = {k}, M = 2 (below N^(1/k))")
    # Also the M=floor(N^(1/k)) baseline for k=3
    rows = sorted(by_k[3], key=lambda r: r["N"])
    Ns = [r["N"] for r in rows]
    ps = [r["p_success"] for r in rows]
    ax.plot(Ns, ps, "o--", color="#2e7d32", alpha=0.5,
            label="k = 3, M = ⌊N^(1/k)⌋")
    ax.set_xlabel("N")
    ax.set_ylabel("PGM success probability")
    ax.set_title("Success decays if M is held below N^(1/k)\n"
                 "(paper: dihedral regime M=2 has no efficient known algorithm)")
    ax.grid(alpha=0.3)
    ax.set_ylim(0, 1)
    ax.legend()
    fig.tight_layout()
    fig.savefig(figs / "fig3_M_too_small_regime.png", dpi=140)
    plt.close(fig)

    print("Wrote figures:")
    for p in figs.iterdir():
        print(f"  {p}")


if __name__ == "__main__":
    main()
