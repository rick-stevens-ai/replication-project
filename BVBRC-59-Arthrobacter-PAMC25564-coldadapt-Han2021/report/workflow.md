# Workflow — BVBRC-59 Replication of Han et al. 2021 (*Arthrobacter* sp. PAMC25564)

**Paper:** Han S-R, Kim B, Jang JH, Park H, Oh TJ (2021). *Complete genome sequence of Arthrobacter sp. PAMC25564 and its comparative genome analysis for elucidating the role of CAZymes in cold adaptation.* BMC Genomics 22:403. PMID 34078272.

**Verdict achieved:** REPLICATED (Argo gpt-5.2 judge, coverage 9/10, agreement 8/10).

---

## Overview

Six-step open-source rerun on public NCBI data with free endpoints only. Focal genome CP039290.1 (assembly GCA_004798705.1, BioProject PRJNA531357). All compute on uicgpu01 (16 CPU, HMMER 3.4, conda `antismash` env). LLM judge = Argo gpt-5.2 (localhost:44497).

## Step-by-step

### M1 — Genome length + GC (parses FASTA)
- **Input:** CP039290.1 FASTA from NCBI Datasets v2.
- **Tool:** Python 3.8 (Biopython/plain parse).
- **Output:** length in bp, GC%.
- **Paper vs rerun:** 4,170,970 bp vs 4,170,970 bp (EXACT); 66.74% vs 66.71% (Δ0.03).

### M2 — Gene / CDS / RNA counts
- **Input:** NCBI Datasets v2 for GCA_004798705.1 + efetch of feature table using the **original GenBank annotation of 2019-04-11** (paper-contemporaneous, not the drifted 2024 RefSeq re-annotation).
- **Tool:** NCBI Datasets v2 REST + NCBI E-utilities `efetch`.
- **Output:** total genes, CDS, pseudogene, rRNA, tRNA counts.
- **Paper vs rerun:** 3,829/3,613/147/15/51 vs 3,829/3,613/147/15/51 (all EXACT).

### M3 — Proteome
- **Input:** NCBI Datasets PROT_FASTA for the same assembly.
- **Output:** `work/genomes/PAMC25564_proteins.faa` (3,613 sequences).
- **Paper vs rerun:** 3,613 CDS vs 3,613 sequences (EXACT).

### M4 — CAZyme classification
- **Input:** PAMC25564_proteins.faa.
- **Tool:** HMMER 3.4 `hmmscan` vs **dbCAN-HMMdb-V9** (pro.unl.edu; 99 MB HMMER3 DB). Substituted for the paper's dbCAN2/V8-era DB because bcb.unl.edu is offline post-cyberattack.
- **Filter:** canonical dbCAN `hmmscan-parser` — E < 1e-15 if alignment > 80 aa else E < 1e-5; HMM coverage > 0.35; overlap > 0.5 resolution.
- **Output:** per-protein CAZyme family assignments + class counts.
- **Paper vs rerun:** 108 vs 102 CAZymes (33/45/23/5/2/0 vs 34/43/16/5/9/0).

### M5 — Cold-adaptation families
- **Input:** M4 domain-table.
- **Method:** family-membership check against paper Table 2 signature list.
- **Output:** presence/absence per family.
- **Paper vs rerun:** GH1, GH13 (7 subfamilies incl. GH13_11, GH13_26), GH65, GH77, CBM48 — **FULL MATCH**.

### M6 — Comparator availability
- **Input:** sampled comparator accessions from the paper.
- **Tool:** NCBI `esummary`.
- **Output:** availability + strain-name resolution.
- **Paper vs rerun:** CP040018.1, CP007595.1, CP017421.1, CP018863.1, CP002379.1 — all resolve to real complete public genomes of the named strains. **VERIFIED**.

## LLM judge step
- **Judge model:** Argo gpt-5.2 (localhost:44497, free endpoint).
- **Inputs:** paper OA XML (Europe PMC) + this replication's REPORT.md + claims table.
- **Output:** coverage 9/10, agreement 8/10, verdict REPLICATED.
- **Rationale:** core genome statistics match exactly or near-exactly on the same public assembly/annotation; comparative dataset verified; CAZyme totals differ modestly (102 vs 108) with category shifts plausibly explained by dbCAN/HMMdb versioning, while all key cold-adaptation CAZyme families are fully recovered.

## Tooling summary
| Category | Tool | Version | Notes |
|---|---|---|---|
| Sequence parse | Python | 3.8 | uicgpu01 |
| Annotation | NCBI Datasets v2 REST | — | Free |
| Feature fetch | NCBI E-utilities | — | Free |
| Homology search | HMMER | 3.4 | conda `antismash` env |
| CAZyme HMM DB | dbCAN-HMMdb-V9 | V9 | pro.unl.edu mirror |
| CAZyme parser | canonical dbCAN hmmscan-parser | — | E-value + coverage + overlap filter |
| LLM judge | Argo gpt-5.2 | — | localhost:44497 |

## BV-BRC mapping
- Genome stats + PGAP annotation ↔ BV-BRC **Comprehensive Genome Analysis**.
- CAZyme classification ↔ BV-BRC **Specialty Genes / protein-family services**.

## Reproducibility notes
- Pin annotation to **2019-04-11 GenBank** vintage; current RefSeq (RS_2024_05_22) drifts (3,863/3,718/75) and will make counts look wrong.
- V8 dbCAN DB not currently available; V9 substitution documented as the primary source of CAZyme count delta.
- All endpoints used are free; no paid API calls were made.
