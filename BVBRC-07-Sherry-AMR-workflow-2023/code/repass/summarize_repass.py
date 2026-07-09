#!/usr/bin/env python3
"""Summarize re-pass LOD + precision results.

For each test genome:
  - Reference AMR call set = pass-1 AMRFinder result on the original reference assembly
  - Re-pass call set = AMRFinder on assembly built from wgsim-simulated reads
  - LOD per coverage = |ref ∩ rep| / |ref|  (recall)
  - Precision per coverage = |ref ∩ rep| / |rep|  (PPV)
  - Inter-replicate precision = pairwise Jaccard among the 3 seeds at 80X

Outputs:
  results/repass/SUMMARY.json
  results/repass/SUMMARY.md
"""

from __future__ import annotations
import csv
import itertools
import json
import os
import re
from pathlib import Path

REPO = Path("/Users/stevens/Dropbox/REPLICATE-PROJECT/BVBRC-07-Sherry-AMR-workflow-2023")
REPASS_DIR = REPO / "results" / "repass"
TRUTH_DIR = REPASS_DIR / "truth_with_org"

# (accession, organism flag) — matches run_lod_precision.sh
GENOMES = [
    ("GCA_000145595.1", "Staphylococcus_aureus"),
    ("GCA_003020685.1", "Enterococcus_faecium"),
]
COVERAGES = [40, 80, 120, 150]
SEEDS_PRECISION = [1, 2, 3]


def read_gene_set(tsv: Path, amr_only: bool = True) -> set[str]:
    """Return set of AMR gene symbols from an AMRFinder TSV.

    amr_only: when True, restrict to rows where column 'Type'=='AMR'
    (excludes STRESS/VIRULENCE — the paper scores AMR genes only).
    """
    if not tsv.exists():
        return set()
    genes = set()
    with tsv.open() as fh:
        reader = csv.reader(fh, delimiter="\t")
        header = next(reader, None)
        if not header:
            return set()
        try:
            sym_idx = header.index("Element symbol")
        except ValueError:
            sym_idx = 5
        try:
            type_idx = header.index("Type")
        except ValueError:
            type_idx = 8
        for row in reader:
            if len(row) <= max(sym_idx, type_idx):
                continue
            if amr_only and row[type_idx] != "AMR":
                continue
            if row[sym_idx]:
                genes.add(row[sym_idx])
    return genes


def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    u = a | b
    if not u:
        return 1.0
    return len(a & b) / len(u)


def recall_ppv(ref: set, rep: set) -> tuple[float, float]:
    if not ref:
        return (float("nan"), float("nan"))
    tp = len(ref & rep)
    recall = tp / len(ref)
    ppv = tp / len(rep) if rep else float("nan")
    return recall, ppv


def main() -> None:
    summary = {
        "genomes": {},
        "lod_overall": {},
        "precision_overall": {},
        "notes": {
            "ref_call_set": "pass-1 AMRFinder 4.2.7 on original reference assembly (results/amrfinder/<acc>.tsv)",
            "metric": "gene-symbol set (column 'Element symbol' in AMRFinder TSV)",
            "lod_definition": "recall (TP / |ref|); how much of the reference call set is recovered",
            "precision_definition": "PPV (TP / |rep|); how much of the re-pass call set matches the reference",
            "interreplicate_metric": "pairwise Jaccard among 3 seeds at 80X",
        },
    }

    # Per-genome LOD sweep at each coverage (seed=1)
    for acc, org in GENOMES:
        ref = read_gene_set(TRUTH_DIR / f"{acc}.tsv")
        per_cov = {}
        for cov in COVERAGES:
            tsv = REPASS_DIR / f"amrfinder_{acc}_cov{cov}_seed1.tsv"
            rep = read_gene_set(tsv)
            recall, ppv = recall_ppv(ref, rep)
            per_cov[str(cov)] = {
                "ref_n": len(ref),
                "rep_n": len(rep),
                "tp": len(ref & rep),
                "fn_genes": sorted(ref - rep),
                "fp_genes": sorted(rep - ref),
                "recall": recall,
                "ppv": ppv,
                "ran": tsv.exists(),
            }

        # Precision replicates at 80X
        replicate_sets = {}
        for s in SEEDS_PRECISION:
            tsv = REPASS_DIR / f"amrfinder_{acc}_cov80_seed{s}.tsv"
            replicate_sets[s] = read_gene_set(tsv)
        jacc_pairs = {}
        ran_count = sum(1 for s in SEEDS_PRECISION if replicate_sets[s])
        for a, b in itertools.combinations(SEEDS_PRECISION, 2):
            jacc_pairs[f"seed{a}_vs_seed{b}"] = jaccard(replicate_sets[a], replicate_sets[b])
        # Identity rate: fraction of replicate pairs with identical gene sets
        all_identical = (
            ran_count == len(SEEDS_PRECISION)
            and all(replicate_sets[a] == replicate_sets[b] for a, b in itertools.combinations(SEEDS_PRECISION, 2))
        )
        summary["genomes"][acc] = {
            "ref_genes": sorted(ref),
            "ref_n": len(ref),
            "lod_sweep_seed1": per_cov,
            "precision_replicates_80X": {
                "replicates_run": ran_count,
                "set_sizes": {f"seed{s}": len(replicate_sets[s]) for s in SEEDS_PRECISION},
                "pairwise_jaccard": jacc_pairs,
                "all_identical": all_identical,
            },
        }

    # Aggregate LOD across genomes per coverage
    for cov in COVERAGES:
        recs = []
        ppvs = []
        total_ref = 0
        total_tp = 0
        total_rep = 0
        ran = 0
        for acc, _org in GENOMES:
            cell = summary["genomes"][acc]["lod_sweep_seed1"][str(cov)]
            if cell["ran"]:
                ran += 1
                total_ref += cell["ref_n"]
                total_tp += cell["tp"]
                total_rep += cell["rep_n"]
                if cell["ref_n"]:
                    recs.append(cell["recall"])
                if cell["rep_n"]:
                    ppvs.append(cell["ppv"])
        summary["lod_overall"][str(cov)] = {
            "genomes_run": ran,
            "total_ref_genes": total_ref,
            "total_tp": total_tp,
            "total_rep_genes": total_rep,
            "pooled_recall": (total_tp / total_ref) if total_ref else None,
            "pooled_ppv": (total_tp / total_rep) if total_rep else None,
            "mean_recall_per_genome": (sum(recs) / len(recs)) if recs else None,
            "mean_ppv_per_genome": (sum(ppvs) / len(ppvs)) if ppvs else None,
        }

    # Aggregate precision
    all_pairs = []
    all_identical = []
    for acc, _org in GENOMES:
        pj = summary["genomes"][acc]["precision_replicates_80X"]["pairwise_jaccard"]
        all_pairs.extend(pj.values())
        all_identical.append(summary["genomes"][acc]["precision_replicates_80X"]["all_identical"])
    summary["precision_overall"] = {
        "genomes_with_3_replicates": sum(
            1 for acc, _o in GENOMES if summary["genomes"][acc]["precision_replicates_80X"]["replicates_run"] == 3
        ),
        "mean_pairwise_jaccard": (sum(all_pairs) / len(all_pairs)) if all_pairs else None,
        "min_pairwise_jaccard": min(all_pairs) if all_pairs else None,
        "all_replicates_identical_per_genome": all_identical,
        "fraction_genomes_identical": (sum(all_identical) / len(all_identical)) if all_identical else None,
    }

    REPASS_DIR.mkdir(parents=True, exist_ok=True)
    (REPASS_DIR / "SUMMARY.json").write_text(json.dumps(summary, indent=2))

    # Markdown summary
    md = []
    md.append("# Re-pass summary — Sherry 2023 LOD (C15) + Precision (C16)\n")
    md.append("Truth set = pass-1 AMRFinder 4.2.7 / DB 2026-03-24.1 on the reference assembly with `-O <organism>`, filtered to Type=AMR rows. Re-pass runs use identical version/DB/flags; only difference is upstream wgsim+SPAdes.\n")
    md.append("## LOD sweep (seed=1)\n")
    md.append("| Genome | Ref AMR genes | 40X recall | 80X recall | 120X recall | 150X recall |")
    md.append("|---|---|---|---|---|---|")
    for acc, _org in GENOMES:
        row = [acc, str(summary["genomes"][acc]["ref_n"])]
        for cov in COVERAGES:
            cell = summary["genomes"][acc]["lod_sweep_seed1"][str(cov)]
            if cell["ran"]:
                row.append(f"{cell['recall']*100:.1f}% ({cell['tp']}/{cell['ref_n']})")
            else:
                row.append("—")
        md.append("| " + " | ".join(row) + " |")
    md.append("")
    md.append("## Pooled LOD across test genomes\n")
    md.append("| Coverage | Pooled recall | Pooled PPV | Total TP / ref |")
    md.append("|---|---|---|---|")
    for cov in COVERAGES:
        c = summary["lod_overall"][str(cov)]
        if c["pooled_recall"] is not None:
            md.append(
                f"| {cov}X | {c['pooled_recall']*100:.2f}% | "
                f"{(c['pooled_ppv'] or 0)*100:.2f}% | {c['total_tp']}/{c['total_ref_genes']} |"
            )
        else:
            md.append(f"| {cov}X | — | — | — |")
    md.append("")
    md.append("## Precision @ 80X (3 seeds)\n")
    md.append("| Genome | seed1 size | seed2 size | seed3 size | mean Jaccard | identical? |")
    md.append("|---|---|---|---|---|---|")
    for acc, _org in GENOMES:
        p = summary["genomes"][acc]["precision_replicates_80X"]
        ms = p["set_sizes"]
        jvals = list(p["pairwise_jaccard"].values())
        mean_j = (sum(jvals) / len(jvals)) if jvals else float("nan")
        md.append(
            f"| {acc} | {ms['seed1']} | {ms['seed2']} | {ms['seed3']} | "
            f"{mean_j*100:.2f}% | {'YES' if p['all_identical'] else 'no'} |"
        )
    md.append("")
    po = summary["precision_overall"]
    md.append(
        f"**Overall precision**: mean pairwise Jaccard = "
        f"{(po['mean_pairwise_jaccard'] or 0)*100:.2f}%, "
        f"min = {(po['min_pairwise_jaccard'] or 0)*100:.2f}%, "
        f"identical sets in {(po['fraction_genomes_identical'] or 0)*100:.0f}% of genomes."
    )

    (REPASS_DIR / "SUMMARY.md").write_text("\n".join(md) + "\n")
    print(f"Wrote {REPASS_DIR/'SUMMARY.json'}")
    print(f"Wrote {REPASS_DIR/'SUMMARY.md'}")


if __name__ == "__main__":
    main()
