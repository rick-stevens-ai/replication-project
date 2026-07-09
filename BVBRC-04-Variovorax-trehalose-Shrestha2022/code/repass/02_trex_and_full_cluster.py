#!/usr/bin/env python3
"""
02_trex_and_full_cluster.py — Re-pass:
  - Check whether PAMC28711 has TreX (EC 3.2.1.68 / glycogen-debranching
    enzyme) which the paper explicitly lists as part of MetaCyc 'trehalose
    biosynthesis V' (TreX + TreY + TreZ). Pass-1 did NOT test this.
  - Dump the full trehalose / α-glucan cluster around 3.35 Mbp and also
    the glycogen cluster around 2.4 Mbp (because TreX in MetaCyc
    nomenclature is the glycogen-debranching enzyme that supplies
    maltodextrins to TreY).
  - Re-audit the paper's "335612 to 3352054" TreY coordinate.

PGAP GenBank for this organism has ZERO /EC_number qualifiers, so all
matching is by product-name / gene-name keywords. This is the same way
NCBI's Pathway tool and KEGG's own auto-mapping resolve EC→gene for
PAMC28711.

Inputs:  data/CP014517.1.gb
Output:  results/repass/trex_and_cluster.json
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from Bio import SeqIO

ROOT = Path(__file__).resolve().parents[2]
GB = ROOT / "data" / "CP014517.1.gb"
OUT = ROOT / "results" / "repass" / "trex_and_cluster.json"
OUT.parent.mkdir(parents=True, exist_ok=True)


# Paper-named enzymes → (EC, product-keyword regex)
TARGETS = [
    ("OtsA",  "2.4.1.15",
     r"trehalose[-\s]*(6[-\s]*)?phosphate\s+synthase|otsA"),
    ("OtsB",  "3.1.3.12",
     r"trehalose[-\s]*(6[-\s]*)?phosphat(ase|e\s+phosphatase)|otsB"),
    ("TreY",  "5.4.99.15",
     r"(malto[-\s]?oligosyl[-\s]?trehalose\s+synthase|"
     r"4[-\s]?alpha[-\s]?glucanotransferase|treY)"),
    ("TreZ",  "3.2.1.141",
     r"malto[-\s]?oligosyl[-\s]?trehalose\s+trehalohydrolase|treZ"),
    ("TreS",  "5.4.99.16",
     # Avoid 'general stress', 'stress response', etc. by anchoring to
     # 'trehalose synthase' / 'alpha-amylase' / explicit gene tag.
     r"trehalose\s+synthase|\btreS\b|alpha[-\s]?amylase"),
    ("TreF/TreH", "3.2.1.28",
     r"alpha,alpha[-\s]?trehalase|\btrehalase\b|\btreF\b|\btreH\b"),
    ("TreP",  "2.4.1.64",
     r"trehalose\s+phosphorylase|treP"),
    ("TreT",  "2.4.1.245",
     r"trehalose\s+glycosyltransferring\s+synthase|treT"),
    ("TreX",  "3.2.1.68",
     r"glycogen[-\s]?debranching|isoamylase|pullulanase|"
     r"limit\s*dextrinase|treX"),
    ("GlgC",  "2.7.7.27", r"glucose[-\s]?1[-\s]?phosphate\s+adenylyltransferase|glgC"),
    ("GlgA",  "2.4.1.21", r"glycogen\s+synthase|starch\s+synthase|glgA"),
    ("GlgB",  "2.4.1.18", r"glycogen[-\s]?branching|glgB"),
    ("GlgP",  "2.4.1.1",  r"glycogen\s+phosphorylase|glgP"),
]


def feat_q(feat, key, default=""):
    vals = feat.qualifiers.get(key)
    return vals[0] if vals else default


def main() -> None:
    rec = next(SeqIO.parse(GB, "genbank"))

    flat_targets: list[dict] = []
    by_name: dict[str, list[dict]] = {name: [] for name, *_ in TARGETS}

    for feat in rec.features:
        if feat.type != "CDS":
            continue
        prod = feat_q(feat, "product")
        gene = feat_q(feat, "gene")
        note = " ".join(feat.qualifiers.get("note", []))
        blob = f"{prod} {gene} {note}"
        for name, ec, pat in TARGETS:
            if re.search(pat, blob, re.IGNORECASE):
                start = int(feat.location.start) + 1
                end = int(feat.location.end)
                strand = "+" if feat.location.strand == 1 else "-"
                tlen = len(feat_q(feat, "translation"))
                entry = {
                    "matched_paper_enzyme": name,
                    "matched_paper_EC": ec,
                    "locus_tag": feat_q(feat, "locus_tag", "?"),
                    "gene": gene,
                    "product": prod,
                    "start_1based": start,
                    "end_1based": end,
                    "strand": strand,
                    "gene_length_nt": end - start + 1,
                    "protein_length_aa": tlen or None,
                    "pseudo": "pseudo" in feat.qualifiers,
                }
                flat_targets.append(entry)
                by_name[name].append(entry)

    # Presence summary
    presence = {}
    for name, ec, _ in TARGETS:
        hits = by_name[name]
        presence[name] = {
            "EC": ec,
            "n_hits": len(hits),
            "functional_hits": [h for h in hits if not h["pseudo"]],
            "pseudo_hits": [h for h in hits if h["pseudo"]],
        }

    # Dump 3.30–3.40 Mbp trehalose cluster
    cluster = []
    for feat in rec.features:
        if feat.type != "CDS":
            continue
        s = int(feat.location.start) + 1
        e = int(feat.location.end)
        if e < 3_300_000 or s > 3_400_000:
            continue
        cluster.append({
            "locus_tag": feat_q(feat, "locus_tag", "?"),
            "gene": feat_q(feat, "gene"),
            "product": feat_q(feat, "product"),
            "start_1based": s,
            "end_1based": e,
            "strand": "+" if feat.location.strand == 1 else "-",
            "pseudo": "pseudo" in feat.qualifiers,
        })

    # Dump 2.35–2.45 Mbp glycogen / TreX cluster
    glycogen = []
    for feat in rec.features:
        if feat.type != "CDS":
            continue
        s = int(feat.location.start) + 1
        e = int(feat.location.end)
        if e < 2_350_000 or s > 2_450_000:
            continue
        glycogen.append({
            "locus_tag": feat_q(feat, "locus_tag", "?"),
            "gene": feat_q(feat, "gene"),
            "product": feat_q(feat, "product"),
            "start_1based": s,
            "end_1based": e,
            "strand": "+" if feat.location.strand == 1 else "-",
            "pseudo": "pseudo" in feat.qualifiers,
        })

    # Coordinate audit: paper says "335612 to 3352054".
    treY_pgap = next(
        (e for e in flat_targets if e["locus_tag"] == "AX767_16200"), None
    )
    coord_audit = {
        "paper_text_range": "335612 to 3352054",
        "candidate_explanations": [
            {"explanation": "missing '6' before '12' → 3356112 to 3352054",
             "matches": "BV-BRC RAST peg.3325 (3352054..3356112)"},
            {"explanation": "missing '7' before '12' → 3357112 to 3352054",
             "matches": "PGAP AX767_16200 (3352054..3357119), off by 7 bp at upstream end"},
        ],
        "PGAP_AX767_16200": treY_pgap,
    }

    out = {
        "genbank": str(GB),
        "targets_defined": TARGETS,
        "presence_per_enzyme": presence,
        "all_target_hits_flat": flat_targets,
        "trehalose_cluster_3.30_to_3.40_Mbp": cluster,
        "glycogen_cluster_2.35_to_2.45_Mbp": glycogen,
        "n_trehalose_cluster_features": len(cluster),
        "n_glycogen_cluster_features": len(glycogen),
        "TreY_coordinate_audit": coord_audit,
    }
    OUT.write_text(json.dumps(out, indent=2))

    print(f"Wrote {OUT}")
    for name, ec, _ in TARGETS:
        info = presence[name]
        n = info["n_hits"]
        nf = len(info["functional_hits"])
        np = len(info["pseudo_hits"])
        status = "ABSENT" if n == 0 else f"hits={n} functional={nf} pseudo={np}"
        print(f"  {name:10s} EC {ec:<10s} {status}")
        for h in info["functional_hits"] + info["pseudo_hits"]:
            ps = "PSEUDO " if h["pseudo"] else "       "
            print(f"        {ps}{h['locus_tag']} {h['start_1based']}..{h['end_1based']}{h['strand']} "
                  f"{h['product']}")
    print(f"\nTrehalose cluster (3.30–3.40 Mbp): {len(cluster)} CDS")
    print(f"Glycogen cluster   (2.35–2.45 Mbp): {len(glycogen)} CDS")


if __name__ == "__main__":
    main()
