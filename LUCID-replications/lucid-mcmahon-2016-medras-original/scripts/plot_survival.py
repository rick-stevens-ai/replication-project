"""Plot the reproduced survival curves from McMahon 2016 srep33290 Fig. 5.

Reads ../results/Model Data - Survival.tsv (produced by upstream CellModelOutputs.py)
and renders the model curves for the four panels of Fig. 5:
  (a) CHO G1: normal vs NHEJ-defect
  (b) CHO G2: normal vs NHEJ-defect
  (c) Human G1 delayed plate: normal vs NHEJ-defect
  (d) Human G1 immediate plate: normal vs NHEJ-defect
"""
import csv
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "results", "Model Data - Survival.tsv")
OUT = os.path.join(ROOT, "figures", "fig5_reproduction_survival.png")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

with open(SRC) as f:
    reader = csv.reader(f, delimiter="\t")
    header = next(reader)
    rows = list(reader)

idx = {name: header.index(name) for name in header}
dose = [float(r[idx["Dose"]]) for r in rows]

def col(name):
    return [float(r[idx[name]]) for r in rows]

panels = [
    ("(a) CHO G1", ("G1CHO", "G1CHONHEJDefect")),
    ("(b) CHO G2", ("G2GHO", "G2CHONHEJDefect")),  # paper csv typo preserved
    ("(c) Human G1 (delayed plating)", ("G1HumanDelayed", "G1HumanNHEJDelayed")),
    ("(d) Human G1 (immediate plating)", ("G1HumanImmediate", "G1HumanNHEJImmediate")),
]

fig, axes = plt.subplots(2, 2, figsize=(10, 8))
for ax, (title, (normal, nhej)) in zip(axes.flat, panels):
    ax.semilogy(dose, col(normal), "-", color="C0", label="Repair-competent")
    ax.semilogy(dose, col(nhej), "--", color="C3", label="NHEJ defective")
    ax.set_xlim(0, 8)
    ax.set_ylim(1e-4, 1.2)
    ax.set_xlabel("Dose (Gy)")
    ax.set_ylabel("Surviving Fraction")
    ax.set_title(title)
    ax.legend(fontsize=8)
    ax.grid(True, which="both", alpha=0.3)

fig.suptitle("McMahon 2016 srep33290 — Fig. 5 reproduction (model curves only)", fontsize=11)
fig.tight_layout(rect=(0, 0, 1, 0.96))
fig.savefig(OUT, dpi=150)
print(f"Wrote {OUT}")
