#!/usr/bin/env python3
"""
01_genome_features.py — Re-pass: derive genome-level descriptors from the
cached PGAP GenBank flatfile (data/CP014517.1.gb).

Reproduces the implicit / contextual genome claims (size, GC%, CDS count,
rRNAs, tRNAs, contig count, isolation source) that pass-1 took on trust
from secondary sources (KEGG/BV-BRC API) instead of grounding directly in
the GenBank file.

Output: ../../results/repass/genome_features.json
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter
from pathlib import Path

try:
    from Bio import SeqIO
except ImportError:
    sys.stderr.write(
        "BioPython not installed in this env. Try: pip install biopython\n"
    )
    sys.exit(2)


ROOT = Path(__file__).resolve().parents[2]
GB = ROOT / "data" / "CP014517.1.gb"
OUT = ROOT / "results" / "repass" / "genome_features.json"
OUT.parent.mkdir(parents=True, exist_ok=True)


def gc_fraction(seq) -> float:
    s = str(seq).upper()
    g = s.count("G")
    c = s.count("C")
    a = s.count("A")
    t = s.count("T")
    total = a + c + g + t
    return (g + c) / total if total else 0.0


def main() -> None:
    if not GB.exists():
        sys.exit(f"GenBank file missing: {GB}")

    records = list(SeqIO.parse(GB, "genbank"))
    if not records:
        sys.exit("No records parsed from GenBank file.")

    by_record = []
    total_len = 0
    cds = 0
    cds_pseudo = 0
    rrna = 0
    trna = 0
    tmrna = 0
    ncrna = 0
    misc_features = 0
    gene_total = 0
    pseudo_gene = 0
    rrna_lengths = []
    product_counter: Counter = Counter()
    isolation = {}

    for rec in records:
        total_len += len(rec.seq)
        topology = rec.annotations.get("topology", "")
        organism = rec.annotations.get("organism", "")
        # Grab source-feature qualifiers
        for feat in rec.features:
            if feat.type == "source":
                for k in ("isolation_source", "country", "host", "lat_lon",
                          "collection_date", "strain", "type_material"):
                    v = feat.qualifiers.get(k)
                    if v:
                        isolation.setdefault(k, v[0])
            if feat.type == "gene":
                gene_total += 1
                if "pseudo" in feat.qualifiers:
                    pseudo_gene += 1
            elif feat.type == "CDS":
                cds += 1
                if "pseudo" in feat.qualifiers:
                    cds_pseudo += 1
                prod = feat.qualifiers.get("product", ["?"])[0]
                product_counter[prod] += 1
            elif feat.type == "rRNA":
                rrna += 1
                rrna_lengths.append(int(feat.location.end) - int(feat.location.start))
            elif feat.type == "tRNA":
                trna += 1
            elif feat.type == "tmRNA":
                tmrna += 1
            elif feat.type == "ncRNA":
                ncrna += 1
            elif feat.type == "misc_feature":
                misc_features += 1

        by_record.append({
            "id": rec.id,
            "name": rec.name,
            "length_bp": len(rec.seq),
            "gc_fraction": gc_fraction(rec.seq),
            "topology": topology,
            "organism": organism,
        })

    out = {
        "genbank_path": str(GB),
        "n_records": len(records),
        "total_length_bp": total_len,
        "gc_percent_total": (
            sum(gc_fraction(r.seq) * len(r.seq) for r in records) / total_len * 100.0
        ),
        "per_record": by_record,
        "feature_counts": {
            "gene_total": gene_total,
            "gene_pseudo": pseudo_gene,
            "CDS_total": cds,
            "CDS_pseudo": cds_pseudo,
            "rRNA": rrna,
            "tRNA": trna,
            "tmRNA": tmrna,
            "ncRNA": ncrna,
            "misc_feature": misc_features,
        },
        "rRNA_lengths_bp": rrna_lengths,
        "isolation_source_qualifiers": isolation,
        "top_products": product_counter.most_common(20),
    }

    OUT.write_text(json.dumps(out, indent=2))
    print(f"Wrote {OUT}")
    print(json.dumps(
        {
            "size_bp": out["total_length_bp"],
            "n_records": out["n_records"],
            "GC%": round(out["gc_percent_total"], 3),
            "CDS_total": cds,
            "CDS_pseudo": cds_pseudo,
            "rRNA": rrna,
            "tRNA": trna,
            "isolation": isolation,
            "topology": by_record[0]["topology"] if by_record else "",
            "organism": by_record[0]["organism"] if by_record else "",
        },
        indent=2,
    ))


if __name__ == "__main__":
    main()
