# Artifacts Summary — BVBRC-22-Arthrobacter-uranium-Chauhan2018

Every quantitative claim in `report/REPORT.md` and `report/REPORT.tex` traces back to one of the artifacts listed below. No numbers were introduced that are not supported by an artifact on disk.

## Genome assemblies (`data/genomes/`)
| Role | Organism | Accession | Notes |
|---|---|---|---|
| Focal | *Arthrobacter* sp. SRS-W-1-2016 | **GCA_002009585.1** (WGS MTPV00000000, BioProject PRJNA352261) | 4,564,701 bp / 64.1% GC / 93 contigs |
| Comparator (paper-named) | *Paenarthrobacter aurescens* TC1 | GCA_000014925.1 | Paper's stated closest relative |
| Comparator (substitute) | *Arthrobacter cupressi* DSM 24664 | GCA_013409905.1 | Substitutes CGMCC1 (no public assembly) |
| Comparator (substitute) | *A. globiformis* CNM05 | GCA_046536215.2 | Substitutes NBRC 1237 (no public assembly) |

## Predicted proteome
- `data/SRS_proteins.faa` — CDS translations from `prodigal` on GCA_002009585.1; used as the query set for both lineage-specific and BacMet2 analyses.
- Supports: **CDS count = 4327** (exact match to paper).

## ANI (`data/ani_srs_vs_all.tsv`)
- Produced by `fastANI` (SRS-W-1-2016 vs. each of the 3 comparators).
- Supports: **ANI SRS-W-1-2016 vs. TC1 = 80.58%** vs. paper's 80.28% (±0.3%, VERIFIED).

## Lineage-specific gene set (`data/srs_vs_comp.tsv`)
- `diamond blastp` of `SRS_proteins.faa` vs. the pooled proteomes of the 3 comparators; thresholds id ≥ 30%, qcov ≥ 50%. A query with no hit meeting these thresholds is called "lineage-specific."
- Supports: **858 lineage-specific CDS** (vs. paper's 1159 by EDGAR; PARTIAL — same order of magnitude, method + comparator substitution documented).

## Metal / biocide resistance (`data/abricate/bacmet2_SRS.tsv`)
- `abricate --db bacmet2` on the focal assembly.
- Supports: **132 total hits**, covering the same six metal categories the paper reports:
  - Arsenic — arsC, arsT
  - Copper — copR, cutC
  - Cadmium — cadD
  - Chromium — chrR
  - Zinc / cobalt / cadmium — czcP, czcR, czrA
  - Iron — fbpABC, fecDE

## Antibiotic-resistance negative controls
- `data/ncbi_SRS.tsv` — `abricate --db ncbi` on the focal assembly: **0 hits**.
- `data/card_SRS.tsv` — `abricate --db card` on the focal assembly: **0 hits**.
- Supports the "environmental isolate, no clinical AMR focus" claim.

## Not-attempted (documented gaps, no artifact)
- No `data/antismash/…` directory — antiSMASH BGC mining was not rerun; the paper's secondary-metabolite claim is un-audited by this replication. This is the dominant reason the verdict is PARTIAL rather than FULL.
- No phenotypic uranium-tolerance data (no MIC, no ICP-MS uptake); the paper likewise did not produce such data.
- No pan-genome reconstruction beyond diamond best-hit; a matched EDGAR / roary rerun would be needed to fully reconcile the 858-vs-1159 gap.

## Orchestration
- `scripts/run_all.sh` — single entry point that, given the four assemblies in `data/genomes/`, regenerates all `data/*.tsv` and `data/abricate/*` artifacts above.

## Report artifacts (`report/`)
- `REPORT.md` — canonical results narrative + verdict rationale.
- `REPORT.tex` — LaTeX rendition with an added `GENUINE CRITIQUE` section.
- `open_questions.json` — 5 open scientific questions (structured, with basis + next steps).
- `workflow.md` — step-by-step methods pipeline.
- `artifacts_summary.md` — this file.
- `failure_analysis.md` — post-mortem of what did / did not replicate and why.
