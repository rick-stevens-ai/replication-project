# Artifacts Summary — BVBRC-01-CRKP-Zhang2022

Inventory of every artifact produced or pulled during this replication (Phase 1 BV-BRC,
Phase 2 Kleborate, Phase 3 backfill), plus provenance traces (URLs, accessions, sizes,
checksums).

## Paper (item 1)

| File          | Bytes    | SHA-256 (first 16)      | Source |
|---------------|----------|-------------------------|--------|
| `paper.pdf`   | 1,519,987| `a5b493624898fe77`      | https://res.mdpi.com/d_attachment/genes/genes-13-01624/article_deploy/genes-13-01624.pdf (MDPI CC-BY, open access) |

- Journal: Genes 2022, 13(9):1624
- DOI: 10.3390/genes13091624
- Corresponding authors: chenyonger@126.com, science2008@hotmail.com
- Fetched 2026-07-05 09:08 CDT (Phase 3 backfill)

## Text extractions (items 2 & 3)

| File                        | Bytes  | Method                        | Notes |
|-----------------------------|--------|-------------------------------|-------|
| `extraction/marker.md`      | 48,623 | `pdftotext -layout paper.pdf` | Marker central-corpus miss; fallback |
| `extraction/nougat.mmd`     | 1,406  | Stub                          | Pending central Nougat parse; sha256 recorded for later corpus resolver |

## Report artifacts (items 4–8)

| File                                     | Bytes   | Item | Role |
|------------------------------------------|---------|------|------|
| `report/REPORT.tex`                      | 19,492  | (4)  | LaTeX detailed replication report (10 sections including critique) |
| `report/REPORT.pdf`                      | 309,451 | (4)  | Compiled with pdflatex TeX Live 2026, 7 pages |
| `report/REPORT.md`                       | 18,739  | (4a) | Legacy Phase 1+2 markdown report (kept for continuity) |
| `report/PROGRESS.md`                     | 4,896   | (4b) | Timestamped progress log Phases 1–2 |
| `report/open_questions.json`             | 9,643   | (5)  | 5 open questions (JSON array) with basis + next_steps |
| `report/workflow.md`                     | 5,828   | (6)  | Workflow narrative, tool inventory, compute/effort estimate |
| `report/artifacts_summary.md`            | this    | (7)  | This file |
| `report/failure_analysis.md`             | see     | (8)  | Failure analysis + honest critique of evidence strength |

## Genomic data / evidence

| File                                     | Bytes    | Content |
|------------------------------------------|----------|---------|
| `data/kp_all_genomes.json`               | 2,203,410| 9,418 K. pneumoniae genome metadata records (BV-BRC `genome` endpoint) |
| `data/kp_carbapenemase_genomes.json`     | 198,490  | 8,152 genomes with any carbapenemase gene (BV-BRC `sp_gene`) |
| `data/crkp_genomes.json`                 | 566,626  | 2,153 CRKP (K. pneumoniae ∩ carbapenemase-positive) |
| `data/st11_crkp_clean.json`              | 291,607  | 955 ST11 CRKP with metadata (final analysis set) |
| `analysis/claim_analysis.json`           | 5,999    | Structured per-claim evaluation, Phase 1 verdicts |
| `analysis/kleborate/kleborate_results_all.tsv` | 611,935 | Full Kleborate v3.2.4 output, 955 rows × ~30 columns (ST, K-locus, O-locus, AMR genes, virulence loci, virulence score, ...) |
| `analysis/kleborate/kleborate_analysis.json`   | 3,782   | Structured Kleborate summary (KL count breakdown, year-by-year, virulence-locus prevalence) |
| `analysis/kleborate/kleborate_parallel/batch_{0..7}/` | ~1 MB total | Per-batch Kleborate outputs, logs, hAMRonization outputs |
| `analysis/kleborate/test_run/`                 | small    | Kleborate smoke-test output from env-setup step |
| `paper/paper_content.md`                       | 3,294    | Extracted quantitative claims from paper (Phase 1) |

## External data traces / accessions

- **BV-BRC API base:** https://www.bv-brc.org/api/
- **BV-BRC taxon:** 573 (Klebsiella pneumoniae)
- **Kleborate release:** v3.2.4 (bioconda, 2026)
- **Kaptive DB:** bundled with Kleborate v3.2.4
- **PATRIC/BV-BRC snapshot delta:** paper 2022; ours 2026 (~2.5× ST11 CRKP growth)

## Compute location

- **Host:** uicgpu (8× NVIDIA A100 80GB, 2 TB RAM)
- **Working directory:** `/data/stevens/projects-active/crkp-kleborate/`
- **Conda env:** `/data/stevens/envs/kleborate` (Python 3.10 + Kleborate 3.2.4 stack)
- **Assembly staging:** ~5.3 GB FASTA in a subdir; not synced to Dropbox

## Checksums (paper only; genomic assemblies not checksummed here)

```
SHA-256(paper.pdf) = a5b493624898fe77b50df4ba4d91dd2e483292460d10cc979d14b552661853df
```

## Missing / not-generated artifacts (see failure_analysis.md)

- Roary core-genome alignment (would test C20)
- IQ-TREE / RAxML-ng phylogenetic tree (would test C20)
- ClonalFrameML recombination analysis (would test C20 + partly C18)
- Abricate + VFDB full 134-gene panel (would test C17 gene-by-gene)
- BLASTn alignment of wzc CD1-VR2-CD2 (would test C18 directly)
- CGview visualization (would test C20 visualization aspect)
- NCBI BioSample sample-source scrape (would fill C12 blocker)
- Per-assembly QC (N50, BUSCO) audit (would address critique §7 assembly-quality gap)
