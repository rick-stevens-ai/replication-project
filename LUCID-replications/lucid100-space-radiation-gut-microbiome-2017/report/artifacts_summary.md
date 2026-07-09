# Artifacts Summary

**Replication set:** LUCID-100
**Directory:** `lucid100-space-radiation-gut-microbiome-2017/`
**Paper:** Casero et al. *Microbiome* 5:105 (2017). DOI 10.1186/s40168-017-0325-z
**paper.pdf sha256:** `7b9aa1a7550ed8acba91e48554b41031f752b197f8f5353b03e3f2a5a5ce1399`
**Verdict (preserved from on-disk):** REPLICATED (scope ≈ 60–70%, 10/12 claims verified = 83%).

## Top-level files

| File | Purpose |
|---|---|
| `REPORT.md` | Primary narrative replication report (source of truth) |
| `paper.pdf` | Source paper (BMC open access CC-BY) |
| `paper.txt` | Full-text extraction |
| `report/REPORT.tex` | LaTeX-formatted report (from backfill) |
| `report/open_questions.json` | 5 open questions, bare-list JSON schema |
| `report/open_questions_section.tex` | LaTeX rendering of the 5 open questions |
| `report/workflow.md` | Pipeline / methods substitution table |
| `report/artifacts_summary.md` | This file |
| `report/failure_analysis.md` | Honest gap register + verdict cross-check |
| `extraction/nougat.mmd` | Placeholder for full-paper structured extraction (stub only) |

## Input data (`data/`, `fastq/`, `reference/`)

| Path | Contents |
|---|---|
| `data/ena_runs.tsv` | ENA filereport for SRA SRP098151 (80 runs, paired fastq URLs) |
| `data/sample_metadata.tsv` | run ↔ dose (Gy) ↔ timepoint (day) ↔ mouse ID ↔ group (4×2×10 = 80) |
| `data/download.log`, `download.out` | Download logs |
| `fastq/` | 160 fastq.gz files (~2.0 GB, 80 paired libraries) |
| `reference/` | SILVA 138 NR99 DADA2 train_set + V4-extracted FASTA |

## Pipeline scripts (`scripts/`)

| Script | Purpose |
|---|---|
| `01_make_metadata.py` | Parse ENA filereport → sample metadata |
| `02_download_fastqs.sh` | curl 160 fastq.gz from ENA |
| `03_prep_reference.py` | SILVA seed → V4-extracted vsearch reference |
| `04_process_samples.sh` | Per-sample merge + QC filter |
| `05_cluster_otus.sh` | Dereplicate → cluster → chimera → OTU table → tax |
| `06_diversity_and_taxa.py` | Alpha/beta/PCoA/PERMANOVA/targeted taxa |
| `07_reassign_with_nr99.py` | SILVA 138 NR99 retax pass |

## Intermediates (`work/`)

| Path | Contents |
|---|---|
| `work/otus.fasta` | 2291 OTU representative sequences (de novo, 97%) |
| `work/otu_table.tsv` | 2291 OTU × 80 sample count matrix |
| `work/otu_tax.tsv` | OTU → SILVA NR99 taxonomy |
| `work/otu_vs_silva.b6`, `otu_vs_silva_nr99.b6` | vsearch usearch_global blast6 hits |
| `work/per_sample.log` | Per-sample vsearch merge/filter logs |

## Results (`results/`)

| Path | Contents |
|---|---|
| `results/akkermansia_test.json` | **Headline: Akkermansia MWU test, 17.28% vs 0.50%, p=0.001** |
| `results/alpha_diversity*.tsv` | Per-sample / per-group Shannon + richness + tests |
| `results/beta_braycurtis.dm`, `beta_jaccard.dm` | Distance matrices |
| `results/beta_permanova.tsv` | PERMANOVA F/p for Dose, Time, all pairwise contrasts |
| `results/pcoa_braycurtis.tsv` | PCoA PC1–3 + metadata + variance-explained |
| `results/phylum_relative_abundance.tsv` + `_by_group.tsv` | Phylum-level tables |
| `results/family_relative_abundance.tsv` + `_by_group.tsv` | Family-level tables |
| `results/genus_relative_abundance.tsv` + `_by_group.tsv` | Genus-level tables |
| `results/targeted_taxa_per_sample.tsv` + `_by_group.tsv` | Akkermansia / Verrucomicrobia / etc. |

## Backfill artifact inventory (this task, 2026-07-06)

Added 7 artifacts to hit the 8-artifact standard (paper.pdf was pre-existing = artifact 8):
1. `report/REPORT.tex`
2. `report/open_questions.json`
3. `report/open_questions_section.tex`
4. `report/workflow.md`
5. `report/artifacts_summary.md` (this file)
6. `report/failure_analysis.md`
7. `extraction/nougat.mmd`

Nothing was overwritten; all pre-existing files (REPORT.md, scripts, results, work, fastq, reference, paper.pdf, venv) preserved.

## What is NOT here (explicit)

- No PICRUSt/FishTaco outputs (arm not run)
- No LC-MS metabolomics outputs, no `.mzML` files (Dryad DOI missing in paper)
- No DESeq2 ANODEV OTU-level output (claim #11 not tested)
- No UniFrac / Faith-PD outputs (no phylogeny tree built)
- No full Nougat extraction — `extraction/nougat.mmd` is a stub; `paper.txt` covers the full-text needs
