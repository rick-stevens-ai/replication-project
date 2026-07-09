#!/usr/bin/env python3
"""
Figures: replicate Fig 2A bar chart (up/down DEG counts at 0.05 Gy),
Fig 5A counterpart at 2 Gy, and a volcano plot for one combo.
"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

PROJECT = Path(__file__).resolve().parents[1]
FIGS = PROJECT / "figures"
FIGS.mkdir(parents=True, exist_ok=True)
DEG_FILE = PROJECT / "data" / "AF1a_degs.tsv"
COUNTS = PROJECT / "results" / "deg_counts.tsv"


def load_counts():
    with open(COUNTS) as f:
        return list(csv.DictReader(f, delimiter="\t"))


def load_degs():
    out = []
    with open(DEG_FILE) as f:
        rdr = csv.DictReader(f, delimiter="\t")
        for r in rdr:
            try:
                r["log2FC"] = float(r["log2FC"])
                r["FDR"] = float(r["FDR"])
                r["P-value"] = float(r["P-value"])
            except (ValueError, TypeError):
                continue
            out.append(r)
    return out


def fig_deg_bars():
    counts = load_counts()
    groups = ["N0", "N1", "N2+"]
    models = ["crude model", "model 1", "model 2"]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5), sharey=False)
    for ax, dose in zip(axes, ["0.05 Gy", "2 Gy"]):
        x_labels = []
        ups = []
        downs = []
        for g in groups:
            for m in models:
                row = next((r for r in counts if r["Group"] == g and r["Dose"] == dose and r["Model"] == m), None)
                if row is None:
                    continue
                x_labels.append(f"{g}\n{m.replace(' model','')}")
                ups.append(int(row["Up"]))
                downs.append(int(row["Down"]))
        x = np.arange(len(x_labels))
        ax.bar(x, ups, color="#d23a3a", label="Upregulated")
        ax.bar(x, [-d for d in downs], color="#3a5fd2", label="Downregulated")
        ax.axhline(0, color="black", lw=0.5)
        ax.set_xticks(x)
        ax.set_xticklabels(x_labels, fontsize=8)
        ax.set_title(f"DEGs at FDR<0.05 after {dose}")
        ax.set_ylabel("# DEGs (down ← | → up)")
        ax.legend(fontsize=8, loc="upper left")
        # annotate totals
        for i, (u, d) in enumerate(zip(ups, downs)):
            ax.text(i, u + max(ups) * 0.02, str(u + d), ha="center", fontsize=7)
    fig.suptitle("Grandt et al. 2022 (KiKme) — DEG counts replicated from Additional File 1a", fontsize=11)
    fig.tight_layout()
    fig.savefig(FIGS / "fig1_deg_counts.png", dpi=150)
    fig.savefig(FIGS / "fig1_deg_counts.pdf")
    plt.close(fig)
    print(f"Wrote {FIGS/'fig1_deg_counts.png'}")


def fig_volcano():
    degs = load_degs()
    fig, axes = plt.subplots(2, 3, figsize=(12, 7), sharex=True, sharey=True)
    for col, group in enumerate(["N0", "N1", "N2+"]):
        for row_i, dose in enumerate(["0.05 Gy", "2 Gy"]):
            ax = axes[row_i, col]
            subset = [r for r in degs if r["Group"] == group and r["Dose"] == dose and r["Model"] == "model 1"]
            lfc = np.array([r["log2FC"] for r in subset])
            mp = np.array([-np.log10(max(r["P-value"], 1e-300)) for r in subset])
            sig = np.array([r["FDR"] < 0.05 for r in subset])
            ax.scatter(lfc[~sig], mp[~sig], s=4, color="lightgray", alpha=0.5)
            ax.scatter(lfc[sig], mp[sig], s=6, color="#d23a3a", alpha=0.7)
            # Label top 5 by FDR (only sig genes)
            sig_subset = [r for r in subset if r["FDR"] < 0.05]
            sig_subset.sort(key=lambda r: r["FDR"])
            for r in sig_subset[:5]:
                ax.text(r["log2FC"], -np.log10(max(r["P-value"], 1e-300)),
                        r["Gene"], fontsize=7, ha="center", va="bottom")
            ax.set_title(f"{group} | {dose}  (n_sig={sig.sum()})", fontsize=10)
            ax.axhline(-np.log10(0.05), ls="--", color="gray", lw=0.5)
            ax.axvline(0, color="black", lw=0.5)
            if row_i == 1:
                ax.set_xlabel("log2 fold-change")
            if col == 0:
                ax.set_ylabel("-log10(p-value)")
    fig.suptitle("Volcano plots (model 1) — replicated from Grandt et al. 2022 Additional File 1a", fontsize=11)
    fig.tight_layout()
    fig.savefig(FIGS / "fig2_volcano.png", dpi=150)
    fig.savefig(FIGS / "fig2_volcano.pdf")
    plt.close(fig)
    print(f"Wrote {FIGS/'fig2_volcano.png'}")


def fig_p53_enrichment():
    # Headline plot: HALLMARK_P53_PATHWAY fold-enrichment per combo
    import csv
    with open(PROJECT / "results" / "pathway_enrichment_bg.tsv") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    target = [(r["Group"], r["Dose"], float(r["fold"]), float(r["p_right_fisher"]), int(r["a_hits"]), int(r["K_in_bg"]))
              for r in rows if r["Pathway"] == "HALLMARK_P53_PATHWAY" and r["Model"] == "model 1"]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    groups = ["N0", "N1", "N2+"]
    doses = ["0.05 Gy", "2 Gy"]
    x = np.arange(len(groups))
    w = 0.38
    colors = {"0.05 Gy": "#71b3df", "2 Gy": "#d23a3a"}
    for i, d in enumerate(doses):
        vals = [next((t[2] for t in target if t[0] == g and t[1] == d), 0) for g in groups]
        ax.bar(x + (i - 0.5) * w, vals, w, color=colors[d], label=d)
        for j, v in enumerate(vals):
            ax.text(x[j] + (i - 0.5) * w, v + 0.1, f"{v:.2f}×", ha="center", fontsize=9)
    ax.set_xticks(x)
    ax.set_xticklabels(groups)
    ax.set_ylabel("Fold enrichment vs. background")
    ax.set_title("HALLMARK_P53_PATHWAY over-representation in DEGs (model 1)\n"
                 "Right-tailed Fisher's exact, background = all genes in AF1a (n=8,134)")
    ax.axhline(1, ls="--", color="gray", lw=0.6)
    ax.legend(title="Dose")
    fig.tight_layout()
    fig.savefig(FIGS / "fig3_p53_enrichment.png", dpi=150)
    fig.savefig(FIGS / "fig3_p53_enrichment.pdf")
    plt.close(fig)
    print(f"Wrote {FIGS/'fig3_p53_enrichment.png'}")


if __name__ == "__main__":
    fig_deg_bars()
    fig_volcano()
    fig_p53_enrichment()
