# Artifacts Summary — LL16 Milerienė 2023 Replication

Every file produced or consumed by the three passes (Pass-1, Re-pass, Independent Reproduction), organized by role.

## Inputs (from public sources)

| Path | Description | Source | Fetched |
|---|---|---|---|
| `data/LL16.fna` (or NCBI download tree) | LL16 assembly, 372 contigs, 2,473,617 bp | NCBI Datasets: `datasets download genome accession GCF_029912225.1` | Multiple (Pass-1, Re-pass, Independent 2026-07-03) |
| `data/IL1403/IL1403.fna` | *L. lactis* subsp. *lactis* IL1403 reference genome, GenBank AE005176.1 | NCBI E-utilities: `efetch -db nucleotide -id AE005176.1 -format fasta` | Re-pass and Independent (2026-07-03) |

## Code

| Path | Purpose | Introduced in |
|---|---|---|
| `code/repass/mine_annotations.py` | Single re-pass driver: reads PGAP GFF3, applies category-regex sweeps, writes JSON of hits per claim | Re-pass (2026-06-23) |
| `report/evidence/independent_reproduction/code/genome_stats.py` | From-scratch BioPython assembly statistics (contigs, bp, GC, N50) | Independent (2026-07-03) |
| `report/evidence/independent_reproduction/code/gff_counts.py` | PGAP GFF3 feature counter (CDS, RNA subtypes, pseudogenes) | Independent (2026-07-03) |
| `report/evidence/independent_reproduction/code/feature_grep.py` | 49-category functional-gene regex mining across the PGAP annotation | Independent (2026-07-03) |

## Results — Re-pass (2026-06-23)

| Path | Content |
|---|---|
| `results/repass/annotation_mining.json` | All re-pass gene hits (adhesion, acid/bile, LDH, stress, vitamins, trp, IS, enzymes, lactose) |
| `results/repass/skani_LL16_vs_IL1403.tsv` | skani 0.3.2 output: **98.70% ANI**, align_fraction_ref 0.80, align_fraction_query 0.77 |
| `results/repass/fastani_LL16_vs_IL1403.tsv` | FastANI 1.33 output: **98.24% ANI**, 533/643 fragments mapped |
| `results/repass/minced_LL16.crisprs` | MinCED default thresholds: **0 canonical CRISPR arrays** |
| `results/repass/minced_LL16_loose.crisprs` | MinCED loose thresholds: 16 candidate arrays (mostly low-complexity tandem repeats, not canonical CRISPR) |

## Results — Independent Reproduction (2026-07-03)

Directory tree: `report/evidence/independent_reproduction/`

```
├── downloads/
│   ├── LL16_ncbi/ncbi_dataset/data/GCF_029912225.1/   (fresh 2026-07-03 assembly download)
│   └── IL1403_AE005176.fna                             (fresh efetch)
├── code/
│   ├── genome_stats.py
│   ├── gff_counts.py
│   └── feature_grep.py
└── outputs/
    ├── genome_stats_LL16.json          (contigs=372, bp=2,473,617, GC=35.55%)
    ├── gff_counts_LL16.json            (CDS=2,511; RNA subtypes; pseudogenes)
    ├── feature_grep_LL16.json          (49-category functional-gene evidence)
    ├── skani_LL16_vs_IL1403.tsv        (98.70% independently reproduced)
    ├── fastani_LL16_vs_IL1403.tsv      (98.24% independently reproduced)
    ├── minced_LL16_default.crisprs     (0 arrays; matches Re-pass)
    ├── minced_LL16_loose.crisprs       (16 arrays; matches Re-pass)
    ├── minced_LL16_default.gff
    ├── minced_LL16_loose.gff
    ├── abricate_resfinder_LL16.tsv     (0 acquired AMR)
    ├── abricate_card_LL16.tsv          (1 intrinsic: lmrD)
    ├── abricate_vfdb_LL16.tsv          (0 virulence)
    ├── abricate_plasmidfinder_LL16.tsv (0; DB scope Enterobacteriaceae)
    ├── prodigal_LL16.gff               (2,594 independent CDS calls — orthogonal 3rd gene caller)
    ├── indep_summary.json              (full 29-row headline metric comparison)
    └── tool_versions.txt               (skani 0.3.2, FastANI 1.33, MinCED 0.4.2, abricate 1.4.0, prodigal V2.60, datasets 18.25.1, Python 3.14.6)
```

Plus `comparison.md` — the full 35-row side-by-side comparison table (Re-pass vs. Independent).

## Reports (this directory)

| Path | Content |
|---|---|
| `report/REPORT.md` | Canonical narrative report: methods, 36-claim table, key findings, limitations, verdict (PARTIAL, Coverage 8, Agreement 8) |
| `report/REPORT.pass1.md` | Pass-1 (2026-05-10) report, preserved unchanged for provenance |
| `report/REPORT.tex` | LaTeX rendering of this report with a dedicated Genuine Critique section |
| `report/open_questions.json` | 5 open questions grounded in Milerienė 2023 LL16 genomics (nisin cluster completeness, plasmid-borne dairy-adaptation genes + pCI2000 identity, comparative genomics vs. subsp. lactis/cremoris references, safety-relevant AMR mobility screening, in-vitro dairy-starter validation gap) |
| `report/workflow.md` | Full step-by-step reproducibility recipe for all three passes |
| `report/artifacts_summary.md` | This file |
| `report/failure_analysis.md` | Honest analysis of what the replication failed to fully verify and why |
| `PARSER_PROVENANCE.md` | Tool/parser provenance for both passes |

## Headline metrics table (compressed)

| Metric | Paper | Re-pass | Independent (2026-07-03) | Status |
|---|---|---|---|---|
| Contigs | — | 372 | 372 | EXACT |
| Total bp | 2,589,406 | 2,473,617 | 2,473,617 | PARTIAL (4.5% smaller assembly; NCBI filter) |
| GC% | 35.4 | 35.55 | 35.55 | VERIFIED |
| CDS | 2,878 (Prokka) | 2,514 (PGAP) + 218 pseudo = 2,732 | 2,511 | PARTIAL (naming/pipeline) |
| RNAs | 63 | 61 | 61 | VERIFIED (within 2) |
| OrthoANI vs IL1403 | 98.73% | skani 98.70% / FastANI 98.24% | 98.70% / 98.24% | VERIFIED |
| CRISPR canonical array | 3 spacers, 23 DR | MinCED default 0 | MinCED default 0 | PARTIAL |
| Cas protein | present | Cas2 (contig 069) | 1 CRISPR-associated | VERIFIED |
| Acquired AMR | 0 | 0 | 0 (ResFinder) | VERIFIED |
| Virulence | 0 | 0 | 0 (VFDB) | VERIFIED |
| gadB / gadC | present | present + contiguous (contig 048) | present | VERIFIED |
| trp operon | present | complete (contig 016) | 5/5 components | VERIFIED |
| L-LDH paralogs | present | 3 | 3 | VERIFIED |
| D-LDH specific | present | absent (D-2-hydroxyacid DH only) | 0 specific; 2 D-2-hydroxyacid DH | PARTIAL |
| Vitamins B1/B2/B6/B7/B9 | all 5 | all 5 | all 5 | VERIFIED |
| LPXTG surface proteins | present | 4 | 4 | VERIFIED |
| BSH | present | 2 | 2 | VERIFIED |
| Plasmid (RepB / pCI2000 99.57%) | 1 plasmid, 99.57% id | RepB present; identity not measured | 13 RepB + 9 mobilization | PARTIAL |
| Bacteriocin lactococcin B | 37.5% id | Lactococcin-972 family + 3 immunity | 5 bacteriocin-related | PARTIAL |
| IS elements (named 3) | 3 | 21 family-level | 22 family-level | PARTIAL (family-level; naming needs ISfinder) |

Full expanded table lives in `report/REPORT.md` §2.1 and `report/evidence/independent_reproduction/comparison.md`.
