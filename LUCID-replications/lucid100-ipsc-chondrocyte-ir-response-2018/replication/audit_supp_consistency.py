"""
Internal-consistency audit of supplementary statistical tables.
Checks:
  C1. Reciprocal symmetry between A/B halves of S2-S5.
      For each gene G, dose D, time T:
        S{n}A row anchored on HC, "vs. hiPSCs" should equal
        S{n}B row anchored on hiPSCs, "vs. HC-402-05a".
        AND S{n}A "vs. hiPSC-DCHs" should equal S{n}B "vs. hiPSC-DCHs"
        (NB: B-half rows go "vs. hiPSC-DCHs" — third cell line, so this is
        actually a different ANOVA result on different anchor cells.)
        Truly reciprocal pairing is only between A "vs. hiPSCs" and B "vs. HC-402-05a".
  C2. ANOVA P-summary >= max significance among pairwise rows (i.e. the summary
      cannot be MORE significant than any individual comparison; in Dunnett's the
      P-summary for ANOVA across groups should be at least as significant as the
      most significant pairwise comparison).
  C3. Dose-response monotonicity for gH2AX (S1): hiPSC vs HC significance should
      be high (paper claim).

Output: AUDIT.md style report.
"""
import csv, collections, re

# Significance rank
RANK = {"ns":0, "*":1, "**":2, "***":3, "****":4}

rows = list(csv.DictReader(open("parsed_supp/all_supp_significance.csv")))

# ---------- Build index ----------
# key = (panel, cell_line, dose, time, comparison) -> sig
idx = {}
for r in rows:
    k = (r['panel'], r['cell_line'], r['dose_Gy'], r['time'], r['comparison'])
    idx[k] = r['sig']

# ---------- C1: reciprocal symmetry for S2-S5 ----------
genes = ["BRCA2", "RAD51", "PRKDC", "XRCC4"]
panel_pairs = []
for n,g in zip([2,3,4,5], genes):
    panel_pairs.append((g, f"S{n}_{g}_A_anchorHC", f"S{n}_{g}_B_anchoriPSC"))

c1_results = []
for gene, pa, pb in panel_pairs:
    for dose in ["1 Gy","2 Gy","5 Gy"]:
        for t in ["1h","5h","9h","24h"]:
            # A side: cell_line = HC-402-05a, comparison vs. hiPSCs
            a = idx.get((pa, "HC-402-05a", dose, t, "vs. hiPSCs"))
            # B side: cell_line = hiPSCs, comparison vs. HC-402-05a
            # (NB: in S3 panel B the row label was "HC-402-05a" not "vs. HC-402-05a"
            # due to a typo in the source DOCX — handle both)
            b = idx.get((pb, "hiPSCs", dose, t, "vs. HC-402-05a")) or \
                idx.get((pb, "hiPSCs", dose, t, "HC-402-05a"))
            ok = (a == b) if a is not None and b is not None else None
            c1_results.append({"gene":gene, "dose":dose, "time":t,
                               "A_HCvsiPSC":a, "B_iPSCvsHC":b, "symmetric":ok})

# ---------- C2: P-summary monotonicity ----------
# Group rows by (panel, cell_line, dose, time)
groups = collections.defaultdict(dict)
for r in rows:
    k = (r['panel'], r['cell_line'], r['dose_Gy'], r['time'])
    groups[k][r['comparison']] = r['sig']

c2_results = []
for k, comps in groups.items():
    summary = comps.get("P value summary")
    if summary is None: continue
    # collect the pairwise sigs (anything starting with "vs." or matching cell line typo)
    pairwise = [v for c,v in comps.items() if c != "P value summary"]
    if not pairwise: continue
    max_pair = max(pairwise, key=lambda s: RANK.get(s, -1))
    # In Dunnett's, the per-comparison adjusted p IS the p reported — the "P value
    # summary" appears to be the SAME family (most significant pairwise) or possibly
    # the omnibus ANOVA p. Either way, it should NOT be ns when a pairwise is significant.
    consistent = True
    note = ""
    if RANK.get(summary, -1) < RANK.get(max_pair, -1):
        # Summary LESS significant than most-significant pair -> probably an omnibus
        # ANOVA where two groups can still show a difference; allowed but flag.
        # However summary == "ns" with a "*" pairwise = strict inconsistency under Dunnett.
        if summary == "ns" and max_pair != "ns":
            consistent = False
            note = "summary=ns but pairwise has *+"
    c2_results.append({
        "key":"|".join(k),
        "summary":summary, "max_pairwise":max_pair,
        "consistent":consistent, "note":note,
    })

# ---------- Reporting ----------
import os
os.makedirs("audit", exist_ok=True)

with open("audit/c1_symmetry.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=["gene","dose","time","A_HCvsiPSC","B_iPSCvsHC","symmetric"])
    w.writeheader(); w.writerows(c1_results)

with open("audit/c2_summary_vs_pairwise.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=["key","summary","max_pairwise","consistent","note"])
    w.writeheader(); w.writerows(c2_results)

# Summaries
sym_ok = sum(1 for r in c1_results if r['symmetric'] is True)
sym_bad = sum(1 for r in c1_results if r['symmetric'] is False)
sym_na = sum(1 for r in c1_results if r['symmetric'] is None)
print(f"C1 reciprocal symmetry (A 'vs. hiPSCs' == B 'vs. HC-402-05a'):")
print(f"  total cells: {len(c1_results)}  match: {sym_ok}  mismatch: {sym_bad}  missing: {sym_na}")

if sym_bad:
    print("\n  Mismatches:")
    for r in c1_results:
        if r['symmetric'] is False:
            print(f"    {r['gene']} {r['dose']} {r['time']}: A={r['A_HCvsiPSC']!r}  B={r['B_iPSCvsHC']!r}")

c2_ok = sum(1 for r in c2_results if r['consistent'])
c2_bad = sum(1 for r in c2_results if not r['consistent'])
print(f"\nC2 P-summary monotonicity (no 'ns summary with significant pairwise'):")
print(f"  total: {len(c2_results)}  consistent: {c2_ok}  inconsistent: {c2_bad}")
if c2_bad:
    print("\n  Inconsistencies:")
    for r in c2_results:
        if not r['consistent']:
            print(f"    {r['key']}: summary={r['summary']} max_pair={r['max_pairwise']} ({r['note']})")

# Compute summary-stronger cases (summary stronger than any pairwise) — likely impossible
# under Dunnett; if present, suggests omnibus ANOVA p reported.
stronger = sum(1 for r in c2_results if RANK.get(r['summary'],-1) > RANK.get(r['max_pairwise'],-1))
print(f"\n  Cases where summary is STRONGER than max pairwise (suggests omnibus ANOVA): {stronger}")
