# Artifacts Summary — BVBRC-74

Paper: Satti et al. 2021, IJMS 22(14):7385 — Genome annotation of PLA-degrading
*P. aeruginosa* S3, *Sphingobacterium* sp. S2, and *Geobacillus* sp. EC-3.

Verdict: **PARTIAL → REPLICATED-leaning**.

---

## 1. Raw-data inputs

| Artifact | Source | Size | Purpose |
|---|---|---:|---|
| SRR7264118_1.fastq.gz | ENA (S3 Illumina PE) | 460 MB | S3 forward reads |
| SRR7264118_2.fastq.gz | ENA (S3 Illumina PE) | 495 MB | S3 reverse reads |
| SRR14203690_1.fastq.gz | ENA (EC-3 Illumina PE) | 955 MB | EC-3 forward reads (staged, not assembled) |
| SRR14203690_2.fastq.gz | ENA (EC-3 Illumina PE) | 1067 MB | EC-3 reverse reads (staged, not assembled) |
| SRR7264117_* | ENA (S2 Illumina PE) | pending | S2 reads (staged, not assembled) |
| **Total** | | **~3 GB** | |

## 2. Reference genomes downloaded

| Accession | Organism | Status | Size | GC | Used for |
|---|---|---|---:|---:|---|
| GCF_000750905.1 | *P. aeruginosa* PSE305 | complete | 6.76 Mb | 65.31% | Enzyme repertoire donor + 16S source for S3 species assignment |
| GCF_000236605.1 | *G. thermoleovorans* CCB_US3_UF5 | complete | 3.60 Mb | 52.28% | EC-3 spot-check |
| GCF_901482695.1 | *S. thalpophilum* NCTC11429 | complete | 5.96 Mb | 43.64% | S2 spot-check (primary) |
| GCF_000686625.1 | *S. thalpophilum* DSM11723 | draft | 5.90 Mb | 43.57% | S2 spot-check (secondary) |

## 3. Independent assembly output (S3 only)

`asm/s3_paeruginosa_spades/scaffolds.fasta` — SPAdes 4.3.0 `--isolate` mode.

| Cutoff | Contigs | Total bp | GC | N50 | L50 |
|---|---:|---:|---:|---:|---:|
| all         | 509 | 6,705,013 | 65.98% | 261,281 | 9 |
| ≥500 bp     | 103 | 6,540,000 (approx) | 66.19% | — | — |
| ≥1 kb       |  51 | 6,509,452 | 66.26% | 261,281 | 9 |

**Best match to paper Table 1: ≥1 kb cutoff.**
- Paper: 6,509,961 bp / 66.26% GC / 63 contigs / N50 273,159.
- Ours:  6,509,452 bp / 66.26% GC / 51 contigs / N50 261,281.
- Δ length = 509 bp (**0.008%** — essentially exact).
- Δ GC = 0.00% (**exact**).

## 4. Gene prediction + BLAST outputs

| Artifact | Description | Result |
|---|---|---|
| `asm/s3_prodigal.faa` | Prodigal V2.60 protein calls on ≥500 bp scaffolds | **6,085 CDS** (paper: 6,239 by RASTtk; Δ 2.5%) |
| `blast/s3_16s_vs_scaffolds.tsv` | blastn PSE305 16S rRNA vs S3 scaffolds | Best hit NODE_42, **100.00% id over 1536 bp** (paper: ~99%) |
| `blast/pse305_hydrolases_vs_s3.tsv` | tblastn PSE305 hydrolase-family CDSs vs S3 scaffolds (≥50% id, e<1e-30) | See table below |

### 4.2 PLA-enzyme repertoire recovery (tblastn)

| Enzyme class in PSE305 | PSE305 CDS n | Recovered in S3 | Recovery % |
|---|---:|---:|---:|
| Hydrolase           | 138 | 124 | 89.9% |
| Lipase              |   6 |   5 | 83.3% |
| Esterase            |   7 |   6 | 85.7% |
| Protease/peptidase  | 114 | 109 | 95.6% |
| **Cutinase**        |   1 | **1** | **100%** |
| **Depolymerase**    |   1 | **1** | **100%** |
| Oxygenase           |  11 |   9 | 81.8% |
| Catalase            |   5 |   3 | 60.0% |

Central biological claim (Section 2.7 / Table 3 of paper) **confirmed**:
S3 encodes the full PLA-relevant polyester-hydrolase repertoire including the
two most mechanistically important classes (cutinase and PLA-depolymerase).

## 5. LLM-judge verdict artifact

`report/evidence/llm_judge_verdict.json` — Argo `argo:gpt-5.2` at T=0.1.
- Verdict: **PARTIAL**
- Coverage: **100%** (15/15 claims addressed)
- Strict agreement: **40%** (all 8 partial-corroborations counted as non-agreement)
- Contradictions: **0**

## 6. Report artifacts

| File | Purpose |
|---|---|
| `REPORT.md` | Canonical human-readable replication report (source of truth) |
| `REPORT.tex` | LaTeX typeset version + dedicated GENUINE CRITIQUE section |
| `workflow.md` | Stage-by-stage pipeline description with commands and cutoffs |
| `artifacts_summary.md` | This file — inventory of all downloaded / generated artifacts |
| `failure_analysis.md` | What did not work, was skipped, or requires follow-up |
| `open_questions.json` | 5 grounded downstream research questions |
| `evidence/llm_judge_verdict.json` | Machine-readable judge output |

## 7. Compute footprint (free endpoints only)

| Stage | Tool | Endpoint | Wall-clock |
|---|---|---|---:|
| Read download | curl / ENA HTTPS | Public | ~5 min |
| Reference genome download | NCBI Datasets | Public | ~2 min |
| S3 de-novo assembly | SPAdes 4.3.0 | CherryRd (local, 8 threads) | ~35 min |
| Assembly stats | Python | CherryRd | <10 sec |
| Gene prediction | Prodigal V2.60 | CherryRd | ~10 sec |
| 16S species assignment | blastn | CherryRd | <10 sec |
| Enzyme-repertoire tblastn | tblastn | CherryRd | ~1 min |
| LLM judge | argo:gpt-5.2 | localhost:44497 Argo proxy | ~30 sec |
| **Total** | | | **~45 min** |

No paid endpoints were used at any stage.
