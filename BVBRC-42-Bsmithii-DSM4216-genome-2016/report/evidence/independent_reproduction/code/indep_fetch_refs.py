#!/usr/bin/env python3
"""
Independently fetch the 7 UniProt reference enzymes used in the paper's
Fig. 4 (present/absent panel) directly from UniProt REST.

References are cited by their UniProt accessions in the paper text/report:
  P13714  Ldh    L-lactate dehydrogenase (B. subtilis)              -> PRESENT
  P21881  PdhA   Pyruvate DH E1 alpha (B. subtilis)                 -> PRESENT
  P39646  Pta    Phosphotransacetylase (B. subtilis)                -> ABSENT (headline)
  P37877  AckA   Acetate kinase (B. subtilis)                       -> ABSENT (headline)
  P09373  PflB   Pyruvate formate-lyase (E. coli)                   -> ABSENT
  P06672  Pdc    Pyruvate decarboxylase (Zymomonas mobilis)         -> ABSENT
  P94692  PFOR   Pyruvate:ferredoxin oxidoreductase (D. africanus)  -> ABSENT

We fetch each as FASTA via https://rest.uniprot.org/uniprotkb/{ACC}.fasta
"""
import urllib.request
import time
import sys
from pathlib import Path

REFS = [
    ("P13714", "Ldh",  "PRESENT"),
    ("P21881", "PdhA", "PRESENT"),
    ("P39646", "Pta",  "ABSENT_HEADLINE"),
    ("P37877", "AckA", "ABSENT_HEADLINE"),
    ("P09373", "PflB", "ABSENT"),
    ("P06672", "Pdc",  "ABSENT"),
    ("P94692", "PFOR", "ABSENT"),
]

out_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("refs.faa")

records = []
for acc, sym, call in REFS:
    url = f"https://rest.uniprot.org/uniprotkb/{acc}.fasta"
    print(f"[fetch] {acc}  {sym:5s}  ({call})  <- {url}", file=sys.stderr)
    req = urllib.request.Request(url, headers={"User-Agent": "indep-repro/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read().decode()
    # Rewrite header so BLAST output is easy to trace back
    lines = data.splitlines()
    if lines and lines[0].startswith(">"):
        lines[0] = f">{sym}__{acc}__{call}  {lines[0][1:]}"
    records.append("\n".join(lines))
    time.sleep(0.4)

out_path.write_text("\n".join(records) + "\n")
print(f"[write] {out_path}  ({len(records)} records)", file=sys.stderr)
