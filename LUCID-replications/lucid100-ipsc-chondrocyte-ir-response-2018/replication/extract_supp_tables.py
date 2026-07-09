"""
Extract supplementary tables (S1-S5) from Stelcer 2018 PLoS ONE.
These tables contain ANOVA + Dunnett's post-hoc significance summaries.
Output: structured CSVs we can audit for internal consistency.
"""
import os, csv, re
from docx import Document

SUPP_DIR = "../supp"
OUT_DIR  = "../replication/parsed_supp"
os.makedirs(OUT_DIR, exist_ok=True)

def sig_to_p(s):
    s = s.strip()
    mapping = {"ns":">0.05", "*":"<0.05", "**":"<0.01", "***":"<0.001", "****":"<0.0001"}
    return mapping.get(s, s)

def parse_doses_block(rows, label):
    """
    Rows for one cell line. Each dose block is 4 rows:
      [<line>, dose, dose, dose, dose]
      [<line>, 1h, 5h, 9h, 24h]
      [vs. X, sig, sig, sig, sig]
      [vs. Y, sig, sig, sig, sig]
      [P value summary, sig, sig, sig, sig]
    """
    out = []
    i = 0
    while i < len(rows):
        r = rows[i]
        if len(r)>=2 and 'Gy' in r[1]:
            dose = r[1].strip()
            cell_line = r[0].strip()
            times = rows[i+1][1:5]
            comp_rows = []
            j = i+2
            while j < len(rows) and not (len(rows[j])>=2 and 'Gy' in rows[j][1]):
                comp_rows.append(rows[j])
                j += 1
            for cr in comp_rows:
                comp = cr[0].strip()
                for t_idx,t in enumerate(times):
                    sig = cr[t_idx+1].strip() if t_idx+1 < len(cr) else ""
                    out.append({
                        "panel": label,
                        "cell_line": cell_line,
                        "dose_Gy": dose,
                        "time": t.strip(),
                        "comparison": comp,
                        "sig": sig,
                        "p_bound": sig_to_p(sig),
                    })
            i = j
        else:
            i += 1
    return out

def extract(fn, name):
    doc = Document(os.path.join(SUPP_DIR, fn))
    # Tables of interest carry numeric data; skip empty header table
    real_tables = []
    for t in doc.tables:
        all_rows = [[c.text for c in row.cells] for row in t.rows]
        non_empty = [r for r in all_rows if any(c.strip() for c in r)]
        if non_empty:
            real_tables.append(non_empty)
    return real_tables

ALL = []

# S1: gH2AX, one big table covering all 4 doses for hiPSCs comparisons.
# Actually S1 has 2 tables; the second is the data table.
t = extract("S1_table.docx", "gH2AX")
# S1 table 1 (second non-empty) is the dose blocks - but the parsed output above showed
# this table has all dose blocks ALL anchored on hiPSCs. So label panel "S1_gH2AX".
recs = parse_doses_block(t[-1], "S1_gH2AX")
ALL.extend(recs)

# S2: BRCA2 with panels A (anchored on HC-402-05a) and B (anchored on hiPSCs)
for i, fn in enumerate(["S2_table.docx","S3_table.docx","S4_table.docx","S5_table.docx"], start=2):
    gene = {"S2":"BRCA2","S3":"RAD51","S4":"PRKDC","S5":"XRCC4"}[f"S{i}"]
    tabs = extract(fn, gene)
    # Two tables: A (HC anchor), B (hiPSC anchor)
    if len(tabs) >= 1:
        ALL.extend(parse_doses_block(tabs[0], f"S{i}_{gene}_A_anchorHC"))
    if len(tabs) >= 2:
        ALL.extend(parse_doses_block(tabs[1], f"S{i}_{gene}_B_anchoriPSC"))

# Write combined CSV
out_csv = os.path.join(OUT_DIR, "all_supp_significance.csv")
with open(out_csv, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["panel","cell_line","dose_Gy","time","comparison","sig","p_bound"])
    w.writeheader()
    for r in ALL:
        w.writerow(r)

print(f"Wrote {len(ALL)} rows -> {out_csv}")
# Print a sample
for r in ALL[:15]:
    print(r)
