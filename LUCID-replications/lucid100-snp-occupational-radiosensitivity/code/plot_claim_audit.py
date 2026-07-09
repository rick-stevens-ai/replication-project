#!/usr/bin/env python3
"""Plot per-stratum minor-allele frequency in miners vs controls, color = paper-claimed direction."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
data = json.load(open(ROOT / "results" / "extended_replication.json"))

snps = sorted({r["snp"] for r in data})
fig, axes = plt.subplots(2, 2, figsize=(10, 8), sharey=True)
for ax, snp in zip(axes.flat, snps):
    rows = [r for r in data if r["snp"] == snp]
    labels = [f"{r['location'][:6]}_{r['population'][:3]}" for r in rows]
    miners = [r["minor_freq_miners"] for r in rows]
    ctrls  = [r["minor_freq_controls"] for r in rows]
    x = range(len(labels))
    ax.bar([i - 0.2 for i in x], ctrls, width=0.4, color="#7aa6c2", label="Controls")
    ax.bar([i + 0.2 for i in x], miners, width=0.4, color="#c2766a", label="Miners (exposed)")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, rotation=30, ha="right", fontsize=8)
    ax.set_title(f"{snp} — minor allele = {rows[0]['minor_allele']}")
    ax.set_ylabel("Minor allele freq")
    ax.legend(fontsize=8)
    # annotate direction
    for i, (m, c) in enumerate(zip(miners, ctrls)):
        sign = "↑" if m > c else "↓"
        ax.text(i, max(m, c) + 0.01, sign,
                ha="center", fontsize=12,
                color="#2c8a2c" if m > c else "#a23b3b")
plt.suptitle("Botbayev 2026: minor-allele freq in exposed vs controls\n(paper claims ↑ in all four)",
             fontsize=12)
plt.tight_layout()
out = ROOT / "figures" / "claim_audit_minor_allele.png"
plt.savefig(out, dpi=120)
print(f"wrote {out}")
