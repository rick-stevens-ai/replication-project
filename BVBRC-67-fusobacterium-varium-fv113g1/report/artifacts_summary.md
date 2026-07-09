# Artifacts Summary — BVBRC-67 (Fusobacterium varium Fv113-g1)

**Paper:** Sekizuka et al. 2017, PLOS ONE 12(12):e0189319
**Target directory:** `~/Dropbox/REPLICATE-PROJECT/BVBRC-67-fusobacterium-varium-fv113g1/`
**Verdict:** REPLICATED (spot-check)

---

## Report artefacts (`report/`)

| File | Purpose |
|---|---|
| `REPORT.md` | Narrative replication report; primary human-readable output |
| `REPORT.tex` | LaTeX version with a dedicated *Genuine critique* section |
| `open_questions.json` | 5 truly open follow-up questions grounded in Fv113-g1 biology |
| `workflow.md` | Step-by-step method the replication ran (this bundle) |
| `artifacts_summary.md` | This file |
| `failure_analysis.md` | Honest catalog of failure modes and known gaps |

## Evidence artefacts (`report/evidence/`)

| File | Content |
|---|---|
| `fv113g1_assembly_stats.json` | Per-replicon (chromosome + 2 plasmids) length and GC%; tRNA / rRNA / CDS / pseudogene counts from RefSeq PGAP GFF; product-name paralog counts (FadA, autotransporter) |
| `comparative_genomes.json` | *F. varium* ATCC 27725 and *F. ulcerans* SB070 length/GC stats used for C9 and interpretive context |
| `claims_vs_measured.csv` | Claim-by-claim verdict table (C1–C11) with paper value, measured value, delta, and MATCH/PARTIAL flag |

## Work artefacts (`work/`)

| Path | Content |
|---|---|
| `work/data/Fv113g1/` | NCBI Datasets bundle for GCF_002356455.1 — FASTA + GFF + protein.faa + `assembly_data_report.jsonl` + `md5sum.txt` + `README.md` |
| `work/data/ATCC27725/` | NCBI Datasets bundle for GCF_003019655.1 — comparator, C9 |
| `work/data/Fulcerans/` | NCBI Datasets bundle for GCF_037956035.1 (*F. ulcerans* SB070) — interpretive context |
| `work/esearch_*.json` | NCBI E-utilities accession-resolution provenance |
| `work/esummary_asm.json` | Assembly-summary provenance for the RefSeq mapping AP017968 → GCF_002356455.1 |

---

## Public accessions referenced

| Accession | Kind | Role in this replication |
|---|---|---|
| **GCF_002356455.1** (ASM235645v1) | RefSeq assembly | Primary Fv113-g1 assembly under test |
| AP017968 | GenBank | Chromosome, referenced by paper |
| AP017969 | GenBank | Plasmid pFV113-g1-1 |
| AP017970 | GenBank | Plasmid pFV113-g1-2 |
| PRJDB5491 | BioProject | Paper's project umbrella |
| DRA005507 | DDBJ raw reads | RNA-seq (D-MEM vs. BHI) — deferred, C12 |
| **GCF_003019655.1** | RefSeq assembly | *F. varium* ATCC 27725 comparator (C9) |
| **GCF_037956035.1** | RefSeq assembly | *F. ulcerans* SB070 (interpretive context) |
| Pfam PF09403 | Protein family | FadA domain — arbitration target for C11, deferred |

## Claims covered

- **In scope, verified:** C1–C10 → MATCH; C11 → PARTIAL (annotation-scheme divergence).
- **Deferred (not disputed):** C12 (RNA-seq DE on DRA005507); C13 (ISFv1/ISFv2 enumeration).

## Reproducibility inputs

- Python 3.13 (CPython, Apple silicon, stdlib only).
- NCBI Datasets CLI (version stamped per bundle in `README.md`).
- Public unauthenticated downloads only — no API keys required.

## Size + shape at a glance

- Fv113-g1 chromosome: **3,965,155 bp**, GC **29.17 %**.
- Plasmids: pFV113-g1-1 (~89.6 kb, GC 26.70 %); pFV113-g1-2 (~68.1 kb, GC 27.65 %).
- Whole-genome (RefSeq totalSequenceLength): **4,122,841 bp**.
- Annotation (PGAP current): **3,586 protein-coding genes**, **58 tRNA**, **7 rRNA operons** (22 rRNA gene features), **85 pseudogenes**.
- Paralog counts (product-name match): **45 autotransporters**, **8 FadA**.
