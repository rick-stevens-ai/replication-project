#!/usr/bin/env python3
"""Independent feature counts from the PGAP GFF."""
import json
import sys
from collections import Counter
from pathlib import Path

GFF = Path(sys.argv[1])
types = Counter()
rna_subtypes = Counter()
pseudo_cds = 0
cds_with_protein_id = 0

for line in GFF.read_text().splitlines():
    if not line or line.startswith("#"):
        continue
    p = line.split("\t")
    if len(p) < 9:
        continue
    t = p[2]
    types[t] += 1
    attrs = dict(kv.split("=", 1) for kv in p[8].split(";") if "=" in kv)
    if t == "CDS":
        if "pseudo" in attrs and attrs["pseudo"].lower() == "true":
            pseudo_cds += 1
        if "protein_id" in attrs:
            cds_with_protein_id += 1
    if t in {"rRNA", "tRNA", "tmRNA", "SRP_RNA", "RNase_P_RNA", "ncRNA", "misc_RNA", "antisense_RNA"}:
        rna_subtypes[t] += 1

# CDS de-dup by protein_id gives unique proteins; PGAP often has 1 CDS row per protein
out = {
    "gff_file": str(GFF),
    "all_feature_type_counts": dict(types),
    "CDS_total_rows": types.get("CDS", 0),
    "CDS_with_protein_id_(non-pseudo)": cds_with_protein_id,
    "CDS_pseudo_rows": pseudo_cds,
    "gene_rows": types.get("gene", 0),
    "pseudogene_rows": types.get("pseudogene", 0),
    "rna_breakdown": dict(rna_subtypes),
    "rna_total": sum(rna_subtypes.values()),
}
print(json.dumps(out, indent=2))
