#!/usr/bin/env python3
"""Produce the log-log plot of logical error vs physical error."""

import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path


def load(path):
    with open(path) as f:
        return json.load(f)


def main():
    base = Path(__file__).parent.parent / "report" / "evidence"

    data = load(base / "production_noflag.json")
    scan = load(base / "v2_scan.json")

    # Merge points
    all_pts = data["results"] + scan["results"]
    # Dedupe by p
    seen = {}
    for r in all_pts:
        if r["p"] not in seen or r["n_shots"] > seen[r["p"]]["n_shots"]:
            seen[r["p"]] = r
    pts = sorted(seen.values(), key=lambda r: r["p"])

    p = np.array([r["p"] for r in pts])
    pL = np.array([r["p_logical_err_given_accept"] for r in pts])
    err = np.array([r["stderr"] for r in pts])
    n_acc = np.array([r["n_accept"] for r in pts])
    p_acc = np.array([r["p_accept"] for r in pts])

    # Filter to points with enough statistics for log-log fit
    good = (pL > 0) & (n_acc > 100)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Left: logical error rate
    ax1.errorbar(p[good], pL[good], yerr=err[good], fmt='o', capsize=3,
                 label='Stim MC (Steane [[7,1,3]] + noisy syndrome + post-select)')
    # Reference lines
    p_ref = np.logspace(-4, -1, 50)
    ax1.plot(p_ref, 4.41 * p_ref**2, '--', alpha=0.6, label='paper c=4.41 · p² (Y-channel low)')
    ax1.plot(p_ref, 9.95 * p_ref**2, '--', alpha=0.6, label='paper c=9.95 · p² (X-channel high)')
    # Fit
    slope, intercept = np.polyfit(np.log(p[good]), np.log(pL[good]), 1)
    coef = np.exp(intercept)
    ax1.plot(p_ref, coef * p_ref**slope, '-', alpha=0.7, label=f'MC fit: {coef:.2f} · p^{slope:.2f}')
    ax1.set_xscale('log'); ax1.set_yscale('log')
    ax1.set_xlabel('Physical error rate p')
    ax1.set_ylabel(r'Post-selected logical error rate $\Pr[\mathrm{err}\mid\mathrm{accept}]$')
    ax1.set_title('Level-1 Steane magic-state prep: p² scaling')
    ax1.legend(loc='lower right', fontsize=9)
    ax1.grid(True, which='both', alpha=0.3)

    # Right: acceptance
    ax2.plot(p, p_acc, 'o-', label='MC accept probability')
    ax2.plot(p_ref, (1-p_ref)**75, '--', label='paper: $(1-p)^{75}$')
    ax2.set_xscale('log'); ax2.set_yscale('log')
    ax2.set_xlabel('Physical error rate p')
    ax2.set_ylabel('Acceptance probability')
    ax2.set_title('Level-1 Steane: acceptance ≈ (1-p)^75')
    ax2.legend()
    ax2.grid(True, which='both', alpha=0.3)

    fig.suptitle('Replication of Chamberland & Cross (arXiv:1811.00566) Table 4, level-1',
                 fontsize=11)
    fig.tight_layout()

    out = base / "scaling_plot.png"
    fig.savefig(out, dpi=140, bbox_inches='tight')
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
