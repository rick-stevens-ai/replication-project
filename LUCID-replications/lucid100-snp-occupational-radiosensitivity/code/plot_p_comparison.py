#!/usr/bin/env python3
"""Scatter of paper-reported vs recomputed -log10(p) for genotype and allele."""
import json, math
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
RES  = HERE.parent / "results" / "replication_chi2.json"
OUT  = HERE.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

d = json.loads(RES.read_text())

def neglog10(x):
    try:
        x = float(x)
        x = max(x, 1e-12)
        return -math.log10(x)
    except Exception:
        return None

fig, axes = plt.subplots(1, 2, figsize=(11, 5))
for ax, key, title in [(axes[0], "p_genotype", "Genotype 2x3 χ²"),
                       (axes[1], "p_allele",   "Allelic 2x2 χ²")]:
    xs, ys, labels = [], [], []
    for r in d["results"]:
        paper = r["paper_published"][key]
        comp  = r["computed"][key]
        # filter out obvious source typos like 4.736 etc.
        if paper is None or paper > 1.0:
            continue
        xs.append(neglog10(paper)); ys.append(neglog10(comp))
        labels.append(f"{r['snp']} {r['location'][:5]}/{r['population'][:3]}")
    ax.scatter(xs, ys, alpha=0.7)
    lim = max(xs + ys + [3.5])
    ax.plot([0, lim], [0, lim], "k--", lw=0.8, alpha=0.4)
    ax.axhline(-math.log10(0.05), color="r", lw=0.5, alpha=0.4)
    ax.axvline(-math.log10(0.05), color="r", lw=0.5, alpha=0.4)
    ax.set_xlabel("Paper-reported −log10(p)")
    ax.set_ylabel("Recomputed −log10(p)")
    ax.set_title(title)
    for x, y, lab in zip(xs, ys, labels):
        ax.annotate(lab, (x, y), fontsize=6, alpha=0.75)
plt.tight_layout()
plt.savefig(OUT / "p_value_comparison.png", dpi=140)
print("wrote", OUT / "p_value_comparison.png")
