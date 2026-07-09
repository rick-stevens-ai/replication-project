#!/usr/bin/env python3
"""Parse ENA filereport into a tidy sample metadata table.
Sample alias schema:  Dose_<dose>_<time>days_<animal-well>
Example:              Dose_0.1_10days_4A1
"""
import csv, re, sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
src = ROOT / "data/ena_runs.tsv"
out = ROOT / "data/sample_metadata.tsv"

df = pd.read_csv(src, sep="\t")
pat = re.compile(r"Dose_([0-9.]+)_(\d+)days_(\w+)")

rows = []
for _, r in df.iterrows():
    m = pat.match(str(r["sample_alias"]))
    if not m:
        print("UNPARSED", r["sample_alias"], file=sys.stderr)
        continue
    dose, day, animal = m.group(1), int(m.group(2)), m.group(3)
    dose_f = float(dose)
    group = f"{dose_f:g}Gy_{day}d"
    rows.append({
        "run":           r["run_accession"],
        "sample":        r["sample_accession"],
        "library":       r["library_name"],
        "animal_id":     animal,
        "dose_Gy":       dose_f,
        "timepoint_day": day,
        "group":         group,
        "read_count":    int(r["read_count"]),
        "fastq_ftp":     r["fastq_ftp"],
    })

meta = pd.DataFrame(rows).sort_values(["dose_Gy","timepoint_day","animal_id"])
meta.to_csv(out, sep="\t", index=False)
print(f"Wrote {len(meta)} samples -> {out}")
print("\nGroup counts (paper says 10 mice per group, 4 doses × 2 timepoints = 8 groups, 80 total):")
print(meta.groupby(["dose_Gy","timepoint_day"]).size().rename("n").to_string())
print(f"\nTotal reads: {meta['read_count'].sum():,}   Mean/sample: {meta['read_count'].mean():,.0f}")
