#!/usr/bin/env python3
"""
Build a sample mapping file (QIIME2-style) for the 80 16S runs of SRP098151
from the ENA filereport. Parses Time (days post-irradiation) and Dose (Gy)
from sample titles.
"""
import csv, re, pathlib, sys

SLOT = pathlib.Path(__file__).resolve().parents[1]
FRP  = SLOT / "harvest" / "ena_filereport.tsv"
OUT  = SLOT / "data" / "metadata.tsv"
OUT.parent.mkdir(parents=True, exist_ok=True)

PAT = re.compile(r'(\d+) days post-irradiation \(([\d.]+)Gy\)')

with open(FRP) as f, open(OUT, "w", newline="") as g:
    r = csv.DictReader(f, delimiter="\t")
    w = csv.writer(g, delimiter="\t")
    w.writerow(["sample-id", "run_accession", "sample_accession",
                "time_days", "dose_gy", "group", "library_layout",
                "fastq_ftp_r1", "fastq_ftp_r2"])
    seen = 0
    for row in r:
        m = PAT.search(row["sample_title"])
        if not m:
            print(f"WARN: cannot parse title for {row['run_accession']}: {row['sample_title']}", file=sys.stderr)
            continue
        time = m.group(1); dose = m.group(2)
        group = f"T{time}_D{dose}"
        urls = row["fastq_ftp"].split(";")
        r1 = "https://" + urls[0] if urls else ""
        r2 = "https://" + urls[1] if len(urls) > 1 else ""
        w.writerow([row["run_accession"], row["run_accession"], row["sample_accession"],
                    time, dose, group, row["library_layout"], r1, r2])
        seen += 1

print(f"Wrote {seen} rows to {OUT}")
