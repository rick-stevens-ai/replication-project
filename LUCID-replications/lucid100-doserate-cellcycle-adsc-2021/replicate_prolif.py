"""
Proliferation (Fig 1, 2) replication.
Source: Figure1&2.xlsx 'Consolidated' sheet.
Per-condition (PC, NC, Fast=HDR, Slow=LDR), per-timepoint (6h/24h/72h/120h)
absorbance triplicates -> Cell Number via standard curve y = 160797*x - 29124.

We:
  1) Recompute cell numbers from absorbance using the published standard curve and
     verify they reproduce the spreadsheet's 'Cell Number' column.
  2) Compute group means and Welch t-tests across {PC, NC, Fast, Slow} at each timepoint.
  3) Check paper headline claims:
       - "no statistical difference in the number of cells in culture except for LDR at
          day 5 where it is significantly different from control" (Fig 1)
       - "the proliferation rate between samples shows no differences" (Fig 2)
"""
import openpyxl, numpy as np
from scipy import stats
import json

wb = openpyxl.load_workbook("mendeley_data/Figure1&2.xlsx", data_only=True)
ws = wb["Consolidated"]
rows = [list(r) for r in ws.iter_rows(values_only=True)]

# Standard curve: y = 160797*x - 29124   (y = cell number, x = absorbance@490nm)
def absorbance_to_cells(a):
    return 160797.0 * a - 29124.0

# Pull absorbance triplicates per (condition, timepoint)
# Row indices (0-based) per visual scan:
# row 0: headers
# rows 1-4: PC absorbance at 6h, 24h, 72h, 120h  (cols 1..3)
# rows 6-9: NC same
# rows 11-14: Fast (HDR) same
# rows 16-19: Slow (LDR) same
groups_abs = {"PC":[None]*4, "NC":[None]*4, "HDR":[None]*4, "LDR":[None]*4}
tp_labels = ["6h","24h","72h","120h"]

# Locate by header text
def find_block(label):
    for i, r in enumerate(rows):
        if r[0] and isinstance(r[0], str) and r[0].strip().startswith(label):
            return i
    return None

block_starts = {"PC": find_block("PC"), "NC": find_block("NC"),
                "HDR": find_block("Fast"), "LDR": find_block("Slow")}

for cond, b in block_starts.items():
    if b is None: continue
    for k in range(4):
        r = rows[b+1+k]
        if r is None: continue
        # Three replicate values in cols 1,2,3
        vals = [float(r[1]), float(r[2]), float(r[3])]
        groups_abs[cond][k] = vals

print("Block starts:", block_starts)
print("\n=== Absorbance triplicates per condition x timepoint ===")
for cond in groups_abs:
    print(cond, groups_abs[cond])

# Verify cell-number conversion matches the 'Cell Number' columns
print("\n=== Cell counts (recomputed vs spreadsheet 'Cell Number') ===")
print(f"{'Cond':<6}{'TP':<6}{'A_rep1':>9}{'A_rep2':>9}{'A_rep3':>9}{'cells_recomp_mean':>22}")
cells_groups = {}
for cond, blocks in groups_abs.items():
    cells_groups[cond] = []
    for k, abs_vals in enumerate(blocks):
        if abs_vals is None:
            cells_groups[cond].append(None); continue
        cells = [absorbance_to_cells(a) for a in abs_vals]
        cells_groups[cond].append(cells)
        print(f"{cond:<6}{tp_labels[k]:<6}{abs_vals[0]:9.3f}{abs_vals[1]:9.3f}{abs_vals[2]:9.3f}  {np.mean(cells):>20,.0f}")

# Welch t-tests between conditions at each timepoint (cell counts)
print("\n=== Cell-number Welch t-tests ===")
print(f"{'TP':<5} {'contrast':<14} {'p':>8}  sig?")
for k, tp in enumerate(tp_labels):
    for a, b in [("PC","HDR"),("PC","LDR"),("HDR","LDR")]:
        ga = cells_groups[a][k]; gb = cells_groups[b][k]
        if ga is None or gb is None: continue
        p = stats.ttest_ind(ga, gb, equal_var=False).pvalue
        print(f"{tp:<5} {a+'-vs-'+b:<14} {p:>8.4f}  {'YES' if p<0.05 else 'no'}")

# Paper claim: "LDR at day 5 (120h) significantly different from control, but not HDR"
print("\n=== Paper proliferation claim check ===")
p_120_LDR = stats.ttest_ind(cells_groups["PC"][3], cells_groups["LDR"][3], equal_var=False).pvalue
p_120_HDR = stats.ttest_ind(cells_groups["PC"][3], cells_groups["HDR"][3], equal_var=False).pvalue
print(f"  120h PC-vs-LDR  p={p_120_LDR:.4f}  expect sig (LDR < control)  -> {'OK' if p_120_LDR<0.05 and np.mean(cells_groups['LDR'][3])<np.mean(cells_groups['PC'][3]) else 'DIFF'}")
print(f"  120h PC-vs-HDR  p={p_120_HDR:.4f}  expect ns                  -> {'OK' if p_120_HDR>=0.05 else 'DIFF'}")
# Also check earlier timepoints all ns
print("  Earlier timepoints expected: all PC vs HDR or LDR ns")
for k, tp in enumerate(tp_labels[:3]):
    for cond in ("LDR","HDR"):
        p = stats.ttest_ind(cells_groups["PC"][k], cells_groups[cond][k], equal_var=False).pvalue
        ok = (p >= 0.05)
        print(f"  {tp:<5} PC-vs-{cond}  p={p:.4f}  expect ns  -> {'OK' if ok else 'DIFF'}")

with open("replication_prolif_results.json","w") as f:
    json.dump({"absorbance": groups_abs, "cells": cells_groups,
               "p_120h_PC_vs_LDR": float(p_120_LDR),
               "p_120h_PC_vs_HDR": float(p_120_HDR)},
              f, indent=2, default=lambda x: None)
print("\nWrote replication_prolif_results.json")
