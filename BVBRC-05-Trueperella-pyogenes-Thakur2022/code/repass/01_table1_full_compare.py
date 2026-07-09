#!/usr/bin/env python3
"""Pass-2 claim test: full Table 1 — rRNA, tRNA, tmRNA, repeat_region counts per strain.

Paper Table 1 columns: bases, GC, CDS, rRNA, tRNA, tmRNA, RR.
Pass-1 tested bases / GC / CDS only.
Pass-2 adds rRNA, tRNA, tmRNA, RR per strain.
"""
import json, os, re
from pathlib import Path

ROOT = Path("/Users/stevens/Dropbox/REPLICATE-PROJECT/BVBRC-05-Trueperella-pyogenes-Thakur2022")
PROKKA = ROOT / "analysis" / "prokka"
OUT = ROOT / "results" / "repass"
OUT.mkdir(parents=True, exist_ok=True)

# Paper Table 1 values (exact transcription from pdftotext output)
# Cols: bases, GC, CDS, rRNA, tRNA, tmRNA, RR; "-" => not reported
paper = {
    "2012CQ-ZSH": dict(bases=2295822, GC=59.67, CDS=2045, rRNA=6, tRNA=46, tmRNA=1, RR=None),
    "Arash114":   dict(bases=2338282, GC=59.49, CDS=2109, rRNA=6, tRNA=46, tmRNA=1, RR=1),
    "jx18":       dict(bases=2415007, GC=59.33, CDS=2180, rRNA=9, tRNA=46, tmRNA=1, RR=1),
    "TP1":        dict(bases=2332403, GC=59.76, CDS=2126, rRNA=9, tRNA=46, tmRNA=1, RR=1),
    "TP2":        dict(bases=2245225, GC=59.68, CDS=1993, rRNA=9, tRNA=46, tmRNA=1, RR=1),
    "TP3":        dict(bases=2384650, GC=59.35, CDS=2112, rRNA=9, tRNA=46, tmRNA=1, RR=1),
    "TP4":        dict(bases=2427168, GC=59.43, CDS=2169, rRNA=9, tRNA=47, tmRNA=1, RR=1),
    "TP8":        dict(bases=2272494, GC=59.58, CDS=2069, rRNA=3, tRNA=45, tmRNA=1, RR=1),
    "TP6375":     dict(bases=2338390, GC=59.50, CDS=2100, rRNA=6, tRNA=46, tmRNA=1, RR=1),
    "TP4479":     dict(bases=2382253, GC=59.35, CDS=2114, rRNA=9, tRNA=46, tmRNA=1, RR=1),
    "TP-2849":    dict(bases=2384672, GC=59.35, CDS=2113, rRNA=9, tRNA=46, tmRNA=1, RR=1),
    "Bu5":        dict(bases=2218921, GC=59.66, CDS=1948, rRNA=3, tRNA=46, tmRNA=1, RR=2),
    "MS249":      dict(bases=2216617, GC=59.80, CDS=1984, rRNA=3, tRNA=46, tmRNA=1, RR=10),
    "UFV1":       dict(bases=2407507, GC=59.75, CDS=2149, rRNA=2, tRNA=51, tmRNA=1, RR=2),
    "NCTC5224":   dict(bases=2310711, GC=59.57, CDS=2073, rRNA=9, tRNA=48, tmRNA=1, RR=1),
    "SH02":       dict(bases=2380432, GC=59.49, CDS=2116, rRNA=5, tRNA=46, tmRNA=1, RR=1),
    "SH03":       dict(bases=2350892, GC=59.58, CDS=2079, rRNA=7, tRNA=51, tmRNA=1, RR=1),
    "SH01":       dict(bases=2334225, GC=59.49, CDS=2068, rRNA=3, tRNA=46, tmRNA=1, RR=2),
    "DSM20630":   dict(bases=2187257, GC=59.49, CDS=1958, rRNA=9, tRNA=45, tmRNA=1, RR=1),
}

def parse_prokka_txt(path):
    d = {"rRNA": 0, "tRNA": 0, "tmRNA": 0, "repeat_region": 0, "CDS": 0, "bases": 0, "contigs": 0}
    for line in open(path):
        line = line.strip()
        if ":" not in line: continue
        k, v = line.split(":", 1)
        k, v = k.strip(), v.strip()
        if k in d:
            try: d[k] = int(v)
            except: pass
    return d

rows = []
for strain, p in paper.items():
    txt = PROKKA / strain / f"{strain}.txt"
    if not txt.exists():
        rows.append(dict(strain=strain, missing="prokka txt"))
        continue
    o = parse_prokka_txt(txt)
    rows.append(dict(
        strain=strain,
        paper_rRNA=p["rRNA"], our_rRNA=o["rRNA"], rRNA_match=(p["rRNA"]==o["rRNA"]),
        paper_tRNA=p["tRNA"], our_tRNA=o["tRNA"], tRNA_match=(p["tRNA"]==o["tRNA"]),
        paper_tmRNA=p["tmRNA"], our_tmRNA=o["tmRNA"], tmRNA_match=(p["tmRNA"]==o["tmRNA"]),
        paper_RR=p["RR"], our_RR=o["repeat_region"],
        RR_match=(p["RR"] is None or p["RR"]==o["repeat_region"]),
    ))

import csv
out_csv = OUT / "table1_full_compare.tsv"
with open(out_csv, "w") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter="\t")
    w.writeheader(); w.writerows(rows)

# Summary
n = len(rows)
r_match = sum(1 for r in rows if r.get("rRNA_match"))
t_match = sum(1 for r in rows if r.get("tRNA_match"))
m_match = sum(1 for r in rows if r.get("tmRNA_match"))
rr_match = sum(1 for r in rows if r.get("RR_match"))
print(f"Strains compared: {n}")
print(f"rRNA exact match : {r_match}/{n}")
print(f"tRNA exact match : {t_match}/{n}")
print(f"tmRNA exact match: {m_match}/{n}")
print(f"RR exact match   : {rr_match}/{n}  (RR=None counted as match)")

# Mismatch detail
print("\n-- Mismatches --")
for r in rows:
    bad = [k.replace("_match","") for k in ("rRNA_match","tRNA_match","tmRNA_match","RR_match") if not r.get(k)]
    if bad:
        print(f"  {r['strain']}: {bad}")
