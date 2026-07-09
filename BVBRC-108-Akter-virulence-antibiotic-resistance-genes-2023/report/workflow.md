# Workflow — BVBRC-108 (Akter 2023 replication)

**Paper:** Akter T. et al., *Sci. Rep.* 13:1551 (2023). DOI [10.1038/s41598-022-25968-8](https://doi.org/10.1038/s41598-022-25968-8).
**Verdict:** PARTIAL REPLICATION (strong).
**Compute:** uicgpu (8×A100, 255 cores), `/data/stevens/bvbrc108/`.
**Env:** `micromamba envs/amr` — AMRFinderPlus 3.12.8 (DB 2024-07-22.1), NCBI datasets 18.32.0, BLAST+ 2.16.0, EDirect 22.4, Biopython.
**End-to-end runtime:** ~4 min.

---

## Step 0 — Setup

- Provisioned `envs/amr` on uicgpu via micromamba (single reproducible env for AMRFinderPlus + BLAST + datasets + edirect + Biopython).
- Verified AMRFinderPlus DB freshness (2024-07-22.1) and downloaded VFDB set-A (`VFDB_setA_pro.fas.gz`, 4,732 curated virulence proteins) from `mgc.ac.cn/VFs/Down/`.

## Step 1 — Pull assemblies from NCBI (no auth, free)

For each strain listed in the paper (BFFF11, BFF1B1, BFPS6):

- BFFF11 → `efetch -db nuccore -id CP045918.1 -format fasta` → `assemblies/BFFF11.fna`
- BFF1B1 → `efetch -db nuccore -id CP046022.1 -format fasta` → `assemblies/BFF1B1.fna`
- BFPS6  → `datasets download genome accession GCF_021375735.1` → unzip → `assemblies/BFPS6.fna`

Recomputed length / GC / contig count / N50 / L50 with a Biopython one-liner and cross-checked against paper Table 1. **Result:** bp-exact for BFFF11 & BFF1B1; 0.05% drift for BFPS6 (SPAdes-vs-RefSeq post-processing); **novel side-finding:** paper Table 1 column labels for BFFF11 and BFF1B1 are swapped relative to the deposited NCBI records.

## Step 2 — AMR screen (AMRFinderPlus)

Per strain:
```
amrfinder -n assemblies/<strain>.fna \
          -O Enterococcus_faecalis \
          --plus --threads 8 \
          -o amr/<strain>_amr_v2.tsv
```

Aggregated results into `report/evidence/amr_summary.tsv`. Compared strain-by-strain against paper Table 2 exclusivity claims.

## Step 3 — Virulence screen (VFDB set-A tblastn)

- Filtered VFDB set-A to 50 proteins (43 unique symbols) matching paper-mentioned targets (all *E. faecalis* references + cross-species targets for `hylA/hylB/psr/tpx/perR/glf/clpP/agg/esp/cylR2/srtA`).
- Built BLAST DB per assembly:
  ```
  makeblastdb -in assemblies/<strain>.fna -dbtype nucl -out blast/<strain>
  ```
- Ran per strain:
  ```
  tblastn -query vfdb_filtered.faa -db blast/<strain> \
          -evalue 1e-10 -num_threads 8 \
          -outfmt '6 qseqid sseqid pident length qcovs evalue bitscore' \
          > vf/<strain>_tblastn.tsv
  ```
- Kept best hit per query at `pident >= 40%` and `qcov >= 40%` → per-strain hit tables → `report/evidence/*_tblastn_best.tsv` + consolidated `report/evidence/vf_presence.json`.

## Step 4 — LLM-judge scoring

- Composed full claims-vs-results comparison prompt (paper claims C1–C4 vs. rerun results from Steps 1–3).
- Called Argo proxy `http://127.0.0.1:44497/v1`. `argo:claude-opus-4.7` returned **502 Bad Gateway** on prompt size → routed to `argo:claude-sonnet-4.6`.
- Received structured verdict JSON (`verdict=PARTIAL, coverage=72%, agreement=85%`) → `report/evidence/judge_output.json`.

## Step 5 — Report synthesis

- Wrote `report/REPORT.md` (13 KB) with paper-in-a-paragraph, claim-by-claim table, per-strain evidence, novel side-finding (Table 1 header swap), and reproducibility block.
- Backfilled: `REPORT.tex` (LaTeX + dedicated critique), `open_questions.json`, `workflow.md` (this file), `artifacts_summary.md`, `failure_analysis.md`.

## Provenance notes

- Every raw output preserved under `report/evidence/`.
- Assemblies preserved under `work/assemblies/` (BFPS6 zip preserved for reproducibility).
- All BLAST DBs discardable (rebuild from `assemblies/*.fna` in ~10 s per strain).
- AMRFinderPlus DB version and VFDB download date pinned in `report/REPORT.md` §5.
