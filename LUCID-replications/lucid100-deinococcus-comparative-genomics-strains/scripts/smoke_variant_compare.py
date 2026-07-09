#!/usr/bin/env python3
"""LUCID100 slot 54 smoke replication.

Paper: Jeong et al. 2024, Front. Microbiol. — "Comparative genomics of Deinococcus
radiodurans: unveiling genetic discrepancies between ATCC 13939K and BAA-816 strains."
DOI: 10.3389/fmicb.2024.1410024.

Headline numeric claim (Table 2, paper text):
  100 SNVs + 278 insertions + 58 short deletions = 436 total events
  between ATCC 13939K (query, CP150840-CP150843) and ATCC BAA-816 (ref, NC_001263/4
  and NC_000958/9).

This script independently aligns each homologous replicon pair with minimap2 (asm5 preset,
via the `mappy` python binding), then walks the CIGAR to enumerate single-base mismatches
(SNVs) and indel events ≤ 6 bp (the same size envelope reported in the paper, 1-6 bp).
We deliberately mirror the paper's filter so the counts are comparable.

Output:
  artifacts/smoke/per_replicon.tsv  — SNV/INS/DEL/total per replicon
  artifacts/smoke/summary.json      — totals + paper-expected values + match assessment
  prints a human-readable comparison table.

This is a smoke/scoping replication only — the paper's authors used a different
pipeline (PacBio+Illumina assembly with CANU+Pilon, then a custom comparison).
Exact-match is not required; we look for a small relative discrepancy (~±5%) on
the totals to call the replication GREEN.
"""
from __future__ import annotations
import json, sys, re
from pathlib import Path
import mappy as mp
from Bio import SeqIO

ROOT = Path(__file__).resolve().parents[1]
GEN  = ROOT / "artifacts" / "genomes"
OUT  = ROOT / "artifacts" / "smoke"
OUT.mkdir(parents=True, exist_ok=True)

# Replicon pairs: (tag, BAA-816 reference accession, ATCC 13939K query accession)
PAIRS = [
    ("chr1", "NC_001263.1", "CP150840.1"),
    ("chr2", "NC_001264.1", "CP150841.1"),
    ("pMP",  "NC_000958.1", "CP150842.1"),
    ("pCP",  "NC_000959.1", "CP150843.1"),
]

INDEL_MAX_BP = 6  # paper: insertions 1-6 bp; deletions are 'short' (paper text)

def load_seq(acc: str) -> tuple[str, str]:
    p = GEN / f"{acc}.fa"
    rec = next(SeqIO.parse(str(p), "fasta"))
    return rec.id, str(rec.seq).upper()

def count_events(ref_seq: str, qry_seq: str) -> dict:
    """Align query to reference with minimap2 asm5, then count short variants."""
    # asm5 = ≤5% divergence whole-genome aligner preset
    aligner = mp.Aligner(seq=ref_seq, preset="asm5", n_threads=2)
    if not aligner:
        raise RuntimeError("Failed to build aligner index")
    snv = ins = dele = 0
    ins_skipped_large = del_skipped_large = 0
    aligned_ref_bp = 0
    n_hits = 0
    for hit in aligner.map(qry_seq, cs=True):
        if not hit.is_primary:
            continue
        n_hits += 1
        aligned_ref_bp += hit.r_en - hit.r_st
        # The `cs` tag encodes per-position differences compactly.
        # cs grammar:
        #   :N    N identical bases
        #   *xy   substitution ref=x qry=y
        #   +seq  insertion in qry (relative to ref) of length len(seq)
        #   -seq  deletion in qry (relative to ref) of length len(seq)
        for tok in re.findall(r"(:\d+|\*[acgtn][acgtn]|\+[acgtn]+|-[acgtn]+)", hit.cs):
            t = tok[0]
            if t == ":":
                continue
            elif t == "*":
                snv += 1
            elif t == "+":
                L = len(tok) - 1
                if L <= INDEL_MAX_BP:
                    ins += 1
                else:
                    ins_skipped_large += 1
            elif t == "-":
                L = len(tok) - 1
                if L <= INDEL_MAX_BP:
                    dele += 1
                else:
                    del_skipped_large += 1
    return {
        "snv": snv, "ins": ins, "del": dele,
        "total_events": snv + ins + dele,
        "ins_skipped_large": ins_skipped_large,
        "del_skipped_large": del_skipped_large,
        "primary_hits": n_hits,
        "aligned_ref_bp": aligned_ref_bp,
    }

def main():
    per_rep = []
    sums = {"snv": 0, "ins": 0, "del": 0, "total_events": 0,
            "ins_skipped_large": 0, "del_skipped_large": 0}
    for tag, ref_acc, qry_acc in PAIRS:
        ref_id, ref_seq = load_seq(ref_acc)
        qry_id, qry_seq = load_seq(qry_acc)
        counts = count_events(ref_seq, qry_seq)
        row = {"replicon": tag, "ref": ref_acc, "qry": qry_acc,
               "ref_len": len(ref_seq), "qry_len": len(qry_seq), **counts}
        per_rep.append(row)
        for k in sums:
            sums[k] += counts[k]

    # Write per-replicon TSV
    tsv = OUT / "per_replicon.tsv"
    with tsv.open("w") as fh:
        fh.write("replicon\tref\tqry\tref_len\tqry_len\tsnv\tins\tdel\ttotal_events\tins_skipped_large\tdel_skipped_large\taligned_ref_bp\n")
        for r in per_rep:
            fh.write(f"{r['replicon']}\t{r['ref']}\t{r['qry']}\t{r['ref_len']}\t{r['qry_len']}\t"
                     f"{r['snv']}\t{r['ins']}\t{r['del']}\t{r['total_events']}\t"
                     f"{r['ins_skipped_large']}\t{r['del_skipped_large']}\t{r['aligned_ref_bp']}\n")

    # Paper expected values
    paper_total = {"snv": 100, "ins": 278, "del": 58, "total_events": 436}
    pct = lambda obs, exp: (obs - exp) / exp * 100.0 if exp else float("nan")

    summary = {
        "doi": "10.3389/fmicb.2024.1410024",
        "paper_expected_total": paper_total,
        "observed_total": sums,
        "absolute_diff": {k: sums[k] - paper_total.get(k, 0) for k in paper_total},
        "percent_diff": {k: pct(sums[k], paper_total[k]) for k in paper_total},
        "per_replicon": per_rep,
        "method": "minimap2 asm5 (via mappy) on each homologous replicon pair, "
                  "indel events restricted to ≤6 bp to match the paper's reported size envelope.",
        "limitations": [
            "minimap2 asm5 is not the paper's pipeline (CANU+Pilon assembly + custom comparison).",
            "Large structural insertions/duplications are intentionally excluded.",
            "Counts events at single-bp resolution; the paper's 1-6bp insertion bucket may "
            "collapse adjacent ins/del bases differently from minimap2's CIGAR segmentation.",
        ],
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2))

    # Pretty print
    print(f"{'replicon':<6} {'ref':<14} {'qry':<14} {'SNV':>6} {'INS':>6} {'DEL':>6} {'TOTAL':>6}")
    for r in per_rep:
        print(f"{r['replicon']:<6} {r['ref']:<14} {r['qry']:<14} "
              f"{r['snv']:>6} {r['ins']:>6} {r['del']:>6} {r['total_events']:>6}")
    print(f"{'TOTAL':<6} {'-':<14} {'-':<14} "
          f"{sums['snv']:>6} {sums['ins']:>6} {sums['del']:>6} {sums['total_events']:>6}")
    print()
    print("Paper expected (Jeong 2024, text):")
    print(f"  SNV={paper_total['snv']}  INS={paper_total['ins']}  DEL={paper_total['del']}  "
          f"TOTAL={paper_total['total_events']}")
    print("Observed - Expected:")
    for k in ("snv", "ins", "del", "total_events"):
        print(f"  {k:>13}: obs={sums[k]:>5}  exp={paper_total[k]:>5}  "
              f"diff={sums[k]-paper_total[k]:+5d}  ({pct(sums[k],paper_total[k]):+6.1f}%)")
    print()
    print(f"Wrote: {tsv}")
    print(f"Wrote: {OUT/'summary.json'}")

if __name__ == "__main__":
    sys.exit(main() or 0)
