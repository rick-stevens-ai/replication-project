# Workflow: BVBRC-50 Shewanella oncorhynchi Z-P2 Pan-Genome Replication

**Paper:** Zhang, Pan et al. (2023), *Microorganisms* 11(12):2961. DOI: 10.3390/microorganisms11122961. PMC10745600.
**Target genome:** GenBank CP132914 = RefSeq GCF_030848765.1 (locus-tag prefix RA178).
**Verdict achieved:** PARTIAL REPLICATION (strong).
**Compute:** uicgpu (8×A100, 255 cores) — conda env `bvbrc28` at `/data/stevens/envs/bvbrc28`.
**Endpoints:** Free-only (NCBI Datasets REST + Argo proxy `localhost:44497`).

---

## Overview

This workflow independently reproduces the paper's core comparative-genomics claims (C1–C5) using deliberately **different** tools than the original (fastANI vs kSNP/MUMmer; Prokka+Roary vs IPGA/PanOCT; RefSeq PGAP vs RAST). Claims C6 (UPLC-MS m/z) is wet-lab / out of scope; C7 (genomic islands / virulence / CRISPR) is computationally reproducible but was not attempted in this pass.

---

## Step-by-Step

### Step 1 — Environment setup
- Activate conda env: `conda activate bvbrc28` (Python 3.11, Prokka 1.12, Roary 3.12, fastANI, BLAST+, NCBI datasets CLI).
- Work root: `/data/stevens/bvbrc50/` on uicgpu.
- Analysis scripts staged under `work/`.

### Step 2 — Genome retrieval
- Resolve target strain:
  ```
  datasets summary genome taxon "Shewanella oncorhynchi"
  ```
  → confirms Z-P2 = GCF_030848765.1 with `total_sequence_length` = 5,034,612 (exactly the paper's value).
- Download Z-P2 + 10 complete RefSeq *S. putrefaciens* genomes (including YZ08 = GCF_019599085.1, the paper's closest strain) via NCBI Datasets REST:
  ```
  datasets download genome accession <acc> --include genome,protein,gff3
  ```
- 11-genome set matches the paper's Z-P2 + 10-comparator design.

### Step 3 — Genome statistics (C1, C2)
- `work/genome_stats.py`: pure-Python recomputation of length, contig count, GC from the Z-P2 assembly FASTA.
- `awk` on the RefSeq PGAP GFF feature column to count tRNA / rRNA / CDS features.
- Output → `evidence/genome_stats.json`.

### Step 4 — BGC verification (C3)
- For each of the paper's five antiSMASH cluster coordinate windows (APE, beta-lactone, putrebactin/NIS, EPA/hglE-KS, RiPP), extract CDS products annotated within the window from the Z-P2 RefSeq GFF.
- Check for the canonical marker enzyme(s) of each cluster type.
- Output → `evidence/bgc_regions.txt`.
- **Note:** antiSMASH itself was NOT re-run (not installed in `bvbrc28`) — cluster boundaries are taken from the paper and the content is independently verified via marker-enzyme identity.

### Step 5 — Pan-/core-genome (C4)
- Re-annotate all 11 genomes uniformly with **Prokka 1.12** (`--genus Shewanella`).
- Run **Roary 3.12** twice:
  - Default: BLASTp 95% identity.
  - Rerun: BLASTp 70% identity (closer to PanOCT-style orthology grouping used in the paper).
- Compute cluster counts + per-genome uniques from `gene_presence_absence.csv` via `work/roary_analyze.py`.
- Output → `evidence/roary70_analysis.json`, `evidence/roary70_summary_statistics.txt`, `evidence/roary_default_analysis.json`.

### Step 6 — ANI / closest strain (C5)
- **fastANI** with Z-P2 as query against all 11 genomes.
- Output → `evidence/fastani_zp2_vs_all.txt`.

### Step 7 — LLM-judge scoring
- `work/llm_judge.py` provides the full claim-by-claim evidence bundle to Argo `argo:gpt-5.2` (free) via `localhost:44497`.
- LLM issues per-claim rating (STRONG / MODERATE / FAIL) + overall verdict from the canonical vocabulary.
- Output → `evidence/llm_judge_argo_gpt52.md`.
- **No regex scoring** — LLM-only qualitative assessment on top of numerical evidence.

### Step 8 — Report assembly
- Consolidate all evidence into `REPORT.md` with claim-by-claim tables.
- Verdict: **PARTIAL REPLICATION (strong)** — 5/7 claims tested, 2 STRONG + 3 MODERATE, no FAIL, no contradictions.

---

## Reproducibility

- **Env:** conda env `bvbrc28` at `/data/stevens/envs/bvbrc28` on uicgpu.
- **Scripts:** `work/genome_stats.py`, `work/roary_analyze.py`, `work/llm_judge.py`.
- **Evidence artifacts:** `report/evidence/` (JSON + text).
- **Raw data:** genomes, Prokka annotations, Roary outputs retained on uicgpu at `/data/stevens/bvbrc50/`.
- **Endpoints:** All free — NCBI Datasets REST (no auth), Argo proxy for LLM judge. No paid `pdf`/`image` tools invoked.

---

## Skipped / Out-of-Scope

- **C6 (UPLC-MS m/z 373.21):** wet-lab mass-spec measurement — not computationally reproducible from public sequence data.
- **C7 (genomic islands, virulence genes, CRISPR arrays):** would require IslandPath-DIMOB + VFDB BLAST + CRISPRdigger/CRISPRCasFinder; not re-run in this pass. RefSeq GFF's 5 direct-repeat features + 12 riboswitches are noted as weak circumstantial signal only.
- **antiSMASH re-run:** cluster boundaries not independently derived; content verified from marker enzymes at paper-stated windows.
- **RAST re-run:** CDS-count gap (4544 vs 4290) attributed to RAST-vs-PGAP pipeline difference but not directly demonstrated.
