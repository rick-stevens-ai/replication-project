# Workflow: BVBRC-40 — S. thermophilus ACA-DC 2 Genome Replication

**Paper:** Alexandraki et al. (2017), *Standards in Genomic Sciences* **12**:18
**Genome:** GCA_900094135.1 / GCF_900094135.1 · ENA LT604076 · BioProject PRJEB14916
**Verdict:** PARTIAL (strong)
**Wave date:** 2026-07-01

---

## Overview

Free-endpoint-only replication of a bacterial complete-genome report. Strategy: pull the deposited
assembly + PGAP re-annotation from NCBI Datasets, recompute Table 3 statistics with a pure-stdlib
parser, re-annotate de novo with Prokka (RASTtk-analog), independently call CRISPR arrays with
minced, and adjudicate with an LLM judge on free Argo.

---

## Step-by-step pipeline

### 1. Paper text acquisition (free)
- **Endpoint:** Europe PMC REST — `PMC5282782/fullTextXML` (107 KB OA XML, CC BY 4.0).
- **Action:** Fetch OA XML, strip to plain text → `work/paper_text.txt`.
- **Extract:** Table 3 verbatim; ENA accession **LT604076**; BioProject **PRJEB14916**.
- **Cost:** $0. No auth. No paid pdf/image tools.

### 2. Assembly resolution (free)
- **Endpoint:** NCBI Datasets v2alpha REST —
  `genome/bioproject/PRJEB14916/dataset_report`.
- **Result:** Two assemblies resolved:
  - **GCA_900094135.1** — author GenBank deposit (paper's own annotation).
  - **GCF_900094135.1** — RefSeq / PGAP independent re-annotation of the same sequence.

### 3. Genome + annotation download (free, no auth)
- **Endpoint:** NCBI Datasets REST —
  `genome/accession/<acc>/download` with include=GENOME_FASTA + PROT_FASTA + GENOME_GFF + CDS_FASTA.
- **Output:** `work/genomes/GCA_900094135.1/` and `work/genomes/GCF_900094135.1/`.

### 4. Statistics recompute (pure stdlib)
- **Script:** `work/genome_stats.py` (Python 3 stdlib only).
- **Computes:** total length; GC bp and %; contig count; CDS count (from protein.faa and GFF);
  tRNA / rRNA / pseudogene counts from GFF; gene-biotype breakdown.
- **Output:** `work/genome_stats.json`.

### 5. De-novo re-annotation (RASTtk-analog)
- **Host:** uicgpu (conda env `bvbrc28`).
- **Tool:** **Prokka 1.12** (bundles Prodigal, Aragorn, barrnap — same tool families as BV-BRC CGA
  RASTtk).
- **Command shape:**
  ```
  prokka --kingdom Bacteria --genus Streptococcus --species thermophilus \
         --outdir work/prokka_out --prefix ACADC2 <chromosome.fna>
  ```
- **Output:** `work/prokka_out/` (GFF, GBK, TSV summary, .txt stats).
- **Runtime:** ~1 minute on uicgpu A100.

### 6. CRISPR detection
- **Tool:** **minced** 2.x on the chromosome.
- **Runs:** default `minNR=3` (returns 0 arrays); permissive `minNR=2` (returns 6 candidates).
- **Interpretation:** the default-empty result is itself corroborative of the paper's
  "single-spacer" claim (single-spacer arrays fail the default repeat-count threshold). The
  minNR=2 candidate at ~849,603–849,704 bp positionally matches the paper's cas-flanked STACADC2_0849
  array.

### 7. LLM-judge adjudication (free)
- **Endpoint:** Argo proxy — `argo:gpt-5.2` at localhost:44497.
- **Input:** `work/judge_input.txt` (claims table + real recomputed numbers).
- **Output:** `work/judge_output.txt` — verdict / coverage / agreement.
- **Judge result:** coverage 10/10, agreement 7/10, no contradictions.

### 8. Report assembly
- Markdown `report/REPORT.md` (canonical narrative).
- LaTeX `report/REPORT.tex` (compiles to PDF; includes dedicated GENUINE CRITIQUE section).
- Structured JSON `report/open_questions.json` (5 open questions grounded in yogurt-starter S.
  thermophilus biology).
- Supporting docs: `workflow.md` (this file), `artifacts_summary.md`, `failure_analysis.md`.

---

## Data provenance chain

```
Europe PMC (OA XML)
  └─▶ Paper text + Table 3 + ENA/BioProject accessions
        └─▶ NCBI Datasets REST (bioproject → assembly)
              └─▶ GCA_900094135.1 (author GenBank)
              │     └─▶ genome_stats.py (stdlib) → Table-3 recompute
              │     └─▶ Prokka 1.12 on uicgpu → de-novo re-annotation
              │     └─▶ minced (default + minNR=2) → CRISPR arrays
              └─▶ GCF_900094135.1 (PGAP)
                    └─▶ GFF parse → PGAP stats
        └─▶ argo:gpt-5.2 (LLM judge, free Argo)
              └─▶ verdict / coverage / agreement
```

---

## Deliberate scope choices

| In scope | Out of scope |
|---|---|
| Table 3 numerical claims (C1–C7) | RM (restriction-modification) systems |
| CRISPR presence + single-spacer character (C9) | Stress-response gene inventory |
| Function-assignment reproducibility check (C8) | Full BAGEL3 bacteriocin analysis |
| Prokka RASTtk-analog (C10) | Whole-genome phylogeny reconstruction |
| PGAP independent re-annotation cross-check | Actual BV-BRC CGA (RASTtk) web-service run |

Out-of-scope items are enumerated as open questions in `open_questions.json`.

---

## Cost budget (all free)

| Line item | Cost |
|---|---|
| Europe PMC + NCBI Datasets REST | $0 |
| Python stdlib recompute | $0 |
| Prokka + minced on uicgpu | $0 (idle A100) |
| Argo LLM judge (argo:gpt-5.2) | $0 |
| **Total** | **$0** |

No paid `pdf`, `image`, or gated API used. Free-endpoint hard rule honored.
