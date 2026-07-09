"""
Master comparison table for REPORT.md
"""
import csv
rows = list(csv.DictReader(open("parsed_supp/all_supp_significance.csv")))
RANK = {"ns":0, "*":1, "**":2, "***":3, "****":4}

# Build counts per panel
from collections import Counter
panels = sorted(set(r['panel'] for r in rows))
print("Panel  N_cells  sig_distribution")
for p in panels:
    sub = [r for r in rows if r['panel']==p]
    c = Counter(r['sig'] for r in sub if r['comparison']!='P value summary')
    print(f"{p:30}  {len([r for r in sub if r['comparison']!='P value summary']):4d}  {dict(c)}")
