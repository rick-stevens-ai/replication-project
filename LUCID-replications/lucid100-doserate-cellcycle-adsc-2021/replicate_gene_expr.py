"""
Gene expression (Fig 5) replication.

The Mendeley file Figure5GeneExpression.xlsx has:
  * Sheet 'Results': raw Cт values from StepOnePlus PCR (96 wells, 4 timepoints)
    with Sample Name & Target Name (GAPDH, TP53). CD44 raw Cт is NOT in 'Results'.
  * Sheet 'Sheet1': per-timepoint computed table with GAPDH/CD44/TP53 Cт means,
    ΔCt, ΔΔCt, and X_test/X_control fold-change for CD44 and TP53.
  * Sheet 'Sheet2': flat list of CD44 and TP53 fold-changes used for the plot.

We:
  1) Read CD44 and TP53 fold-changes from Sheet1 (per replicate per condition per timepoint).
  2) Compute mean fold-change for each (condition, timepoint).
  3) Compare to the qualitative narrative in the paper:
       - "no significant differences between samples until day 2 when HDR has higher
          [CD44] expression than control and LDR"
       - "On day 3, LDR and HDR are significantly different from each other, but are
          not different from control" (CD44)
       - "p53 expression in irradiated samples is relatively suppressed compared to control.
          However, the differences are only statistically significant at day 3 where LDR
          and HDR are also statistically different from each other"
  4) Run Welch t-tests (Control vs LDR, Control vs HDR, LDR vs HDR) at each timepoint
     for each gene and report sig/ns.
"""
import openpyxl, numpy as np
from scipy import stats
import json

wb = openpyxl.load_workbook("mendeley_data/Figure5GeneExpression.xlsx", data_only=True)
ws = wb["Sheet1"]
rows = [list(r) for r in ws.iter_rows(values_only=True)]

# Per-timepoint block layout: 9 replicate rows (Ctrl1..3, LDR1..3, HDR1..3) with
# each row repeating once (two Cт rows from technical replicates) but
# Xtest/Xcontrol only filled in the FIRST of the two rows.
# Easier route: parse Sheet1 rows and pick those with a non-blank "Sample Name".
# Columns: 1=SampleName, 2=Cт GAPDH (raw), 3=mean GAPDH, 4=Cт CD44, 5=mean CD44,
#          6=Cт TP53, 7=mean TP53, 8=ΔCt(CD44), 9=ΔΔCt, 10=ΔCt mean, 11=fold CD44,
#          12=ΔCt(TP53), 13=ΔΔCt, 14=ΔCt mean, 15=fold TP53.

# Detect timepoint headers: rows whose SampleName starts with "4hrs" / "24hrs" / "48hrs" / "72hrs"
records = []  # (tp, cond, rep, fold_cd44, fold_tp53)
current_tp = None
for r in rows:
    if r is None: continue
    # Update current timepoint if column 0 (or sample name) marks a new block
    tp_marker = r[0]
    if tp_marker and isinstance(tp_marker, str) and tp_marker.strip() in ("4hrs","24hrs","48hrs","72hrs"):
        current_tp = tp_marker.strip()
    if r[1] is None: continue
    name = str(r[1]).strip()
    # Sometimes timepoint is embedded in sample name (e.g. '4hrs Control 1')
    if name.startswith(("4hrs ","24hrs ","48hrs ","72hrs ")):
        tp_key, rest = name.split(None, 1)
        current_tp = tp_key
        name_for_cond = rest.strip()
    else:
        name_for_cond = name
    # Determine condition and rep
    cond = None
    for c in ("Control","LDR","HDR"):
        if name_for_cond.startswith(c):
            cond = c
            try:
                rep = int(name_for_cond.split()[1])
            except Exception:
                rep = None
            break
    if cond is None: continue
    fold_cd44 = r[11]
    fold_tp53 = r[15]
    # Only keep the row where fold values are populated (first of the two tech-rep rows)
    if fold_cd44 is None and fold_tp53 is None: continue
    records.append((current_tp, cond, rep, float(fold_cd44) if fold_cd44 is not None else None,
                                          float(fold_tp53) if fold_tp53 is not None else None))

print(f"Parsed {len(records)} records")
# Group by (tp, cond)
from collections import defaultdict
groups_cd44 = defaultdict(list)
groups_tp53 = defaultdict(list)
for tp, cond, rep, fc, ft in records:
    if fc is not None: groups_cd44[(tp,cond)].append(fc)
    if ft is not None: groups_tp53[(tp,cond)].append(ft)

tps = ["4hrs","24hrs","48hrs","72hrs"]   # paper labels: 4hr, day1, day2, day3
paper_tp_label = {"4hrs":"4hr","24hrs":"Day1","48hrs":"Day2","72hrs":"Day3"}
print("\n--- CD44 fold-change Xtest/Xcontrol per (timepoint, condition) ---")
print(f"{'tp':<8}{'Cond':<10}{'n':>3}  {'mean':>7}  {'sd':>7}  values")
for tp in tps:
    for cond in ("Control","LDR","HDR"):
        vals = groups_cd44.get((tp,cond), [])
        if not vals: continue
        print(f"{paper_tp_label[tp]:<8}{cond:<10}{len(vals):>3}  {np.mean(vals):7.3f}  {np.std(vals,ddof=1):7.3f}  {[round(v,3) for v in vals]}")
print("\n--- TP53 fold-change Xtest/Xcontrol per (timepoint, condition) ---")
for tp in tps:
    for cond in ("Control","LDR","HDR"):
        vals = groups_tp53.get((tp,cond), [])
        if not vals: continue
        print(f"{paper_tp_label[tp]:<8}{cond:<10}{len(vals):>3}  {np.mean(vals):7.3f}  {np.std(vals,ddof=1):7.3f}  {[round(v,3) for v in vals]}")

print("\n--- Welch t-tests vs control ---")
print(f"{'tp':<8}{'Gene':<6}{'Contrast':<22}{'p':>8}  sig?")
def do_tests(groups, gene):
    for tp in tps:
        for c in [("Control","LDR"),("Control","HDR"),("LDR","HDR")]:
            a = groups.get((tp, c[0]), [])
            b = groups.get((tp, c[1]), [])
            if len(a)<2 or len(b)<2: continue
            p = stats.ttest_ind(a, b, equal_var=False).pvalue
            print(f"{paper_tp_label[tp]:<8}{gene:<6}{c[0]+'-vs-'+c[1]:<22}{p:>8.4f}  {'YES' if p<0.05 else 'no'}")
do_tests(groups_cd44, "CD44")
do_tests(groups_tp53, "TP53")

# Paper qualitative claims to check
paper_claims = {
    "CD44 day2 HDR > Control":  ("48hrs", "CD44", "Control-vs-HDR", "sig+HDR-higher"),
    "CD44 day2 HDR > LDR":      ("48hrs", "CD44", "LDR-vs-HDR",     "sig+HDR-higher"),
    "CD44 day3 LDR vs HDR sig": ("72hrs", "CD44", "LDR-vs-HDR",     "sig"),
    "CD44 day3 LDR vs Control ns": ("72hrs","CD44","Control-vs-LDR","ns"),
    "CD44 day3 HDR vs Control ns": ("72hrs","CD44","Control-vs-HDR","ns"),
    "TP53 day3 LDR vs Control sig (downregulated)": ("72hrs","TP53","Control-vs-LDR","sig+irrad-lower"),
    "TP53 day3 HDR vs Control sig (downregulated)": ("72hrs","TP53","Control-vs-HDR","sig+irrad-lower"),
    "TP53 day3 LDR vs HDR sig":                     ("72hrs","TP53","LDR-vs-HDR","sig"),
}
print("\n--- Paper qualitative claim checks ---")
agree = 0; checked = 0
for claim, (tp, gene, contrast, expect) in paper_claims.items():
    groups = groups_cd44 if gene=="CD44" else groups_tp53
    g1, g2 = contrast.split("-vs-")
    a = groups.get((tp,g1),[]); b = groups.get((tp,g2),[])
    if len(a)<2 or len(b)<2:
        print(f"  [skip] {claim}: insufficient data")
        continue
    p = stats.ttest_ind(a,b,equal_var=False).pvalue
    sig = p<0.05
    ma, mb = np.mean(a), np.mean(b)
    higher = "g1" if ma>mb else "g2"   # i.e. which side higher
    ok = False
    if expect == "ns":
        ok = (not sig)
    elif expect == "sig":
        ok = sig
    elif expect == "sig+HDR-higher":
        # HDR is the "g2" of contrasts Control-vs-HDR and LDR-vs-HDR
        ok = sig and (mb > ma)
    elif expect == "sig+irrad-lower":
        # irradiated (LDR or HDR) lower than control => mb < ma
        ok = sig and (mb < ma)
    checked += 1
    if ok: agree += 1
    print(f"  {'OK ' if ok else 'DIFF'}  {claim}: p={p:.4f} sig={'Y' if sig else 'n'}  ({g1} mean={ma:.3f}, {g2} mean={mb:.3f}); expect={expect}")
print(f"\nGene-expression claim match: {agree}/{checked}")

with open("replication_gene_results.json","w") as f:
    json.dump({"cd44": {f"{tp}|{c}": v for (tp,c),v in groups_cd44.items()},
               "tp53": {f"{tp}|{c}": v for (tp,c),v in groups_tp53.items()},
               "claims_matched": [agree, checked]}, f, indent=2)
print("Wrote replication_gene_results.json")
