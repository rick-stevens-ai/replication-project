# Artifacts Summary — BVBRC-97

**Paper**: Pell et al. 2021, *Sci Rep* 11:15893 — *L. plantarum* ATCC 202195 WGS + AMR/VF
**Verdict**: REPLICATED

---

## Downloaded genomes / sequences

Location: `work/genomes/`

| Accession | Size | Description | Purpose |
|---|---:|---|---|
| CP063750.1 | 3,295,397 bp | ATCC 202195-A chromosome (Pell 2021) | Primary retested assembly |
| CP063751.1 | 56,489 bp | ATCC 202195-A unnamed plasmid 1 | Genome-stats + plasmid homology |
| CP063752.1 | 1,815 bp | ATCC 202195-A unnamed plasmid 2 | Genome-stats + pPECL-1 comparison |
| GCA_010586945.1 | 3,356,433 bp | Prior 202195 complete assembly (CP040858.1 + CP040857.1) | ANI reference |
| GCA_004354995.1 | ~3.30 Mb | Wright et al. 202195 draft assembly | ANI reference |
| NC_016635.1 | 1,815 bp | *P. claussenii* pPECL-1 plasmid | Plasmid-2 homology comparator |

**Not pulled** (deliberately, not needed for claim-level replication):
- SRR13686146 raw reads for ATCC 202195-B (the paper's B-isolate SPAdes assembly)

## Analytic outputs (evidence directory)

Location: `report/evidence/`

### Genome-composition stats

- `genome_stats.tsv` — per-replicon length and GC for CP063750/CP063751/CP063752 plus totals
  - Tests claim **C1**

### ANI

- `ani_A_vs_GCA010586945.tsv` — fastANI 202195-A vs GCA_010586945.1 (99.9982%)
- `ani_A_vs_GCA004354995.tsv` — fastANI 202195-A vs GCA_004354995.1 (99.978%)
- `skani_dist_*.tsv` — skani cross-check outputs (100.00% and 99.99% respectively)
  - Tests claims **C2, C3**

### BLASTn plasmid homology

- `blastn_plasmid2_vs_pPECL1.tsv` — CP063752.1 vs pPECL-1: 99.04% id / 100.1% qcov
  - Tests claim **C4**
- `blastn_plasmid1_vs_CP040857.tsv` — CP063751.1 vs prior-assembly plasmid: 100.00% id / ~100% qcov
  - Tests claim **C5**
- `blastn_plasmid2_vs_GCA010586945_full.tsv` — CP063752.1 vs full GCA_010586945.1: 0 hits (null result)
  - Tests claim **C6**

### AMR / VF screening (ABRicate)

Naming convention: `{db}_{high|low}.tsv`

| File | DB | Stringency | Hit count |
|---|---|---|---:|
| `card_high.tsv` | CARD | HIGH (id>80, cov>80) | 0 |
| `card_low.tsv` | CARD | LOW (id>50, cov>10) | 4 (lmrD, rpoB2, Bifi rpoB, IreK) |
| `resfinder_high.tsv` | ResFinder | HIGH | 0 |
| `resfinder_low.tsv` | ResFinder | LOW | 0 |
| `ncbi_high.tsv` | NCBI-AMR | HIGH | 0 |
| `ncbi_low.tsv` | NCBI-AMR | LOW | 0 |
| `vfdb_high.tsv` | VFDB | HIGH | 0 |
| `vfdb_low.tsv` | VFDB | LOW | 24 hits / 14 unique VF gene names |
| `victors_high.tsv` | Victors | HIGH | 0 |
| `victors_low.tsv` | Victors | LOW | 75 partial hits |

  - Tests claims **C7, C8, C10**

### LLM-judge scoring

- `llm_judge_verdict.txt` — verbatim Argo GPT-5.2 (T=0) output with per-claim evaluation,
  coverage (0.89), agreement (1.00), and overall verdict (REPLICATED).

## Report bundle

Location: `report/`

| File | Format | Purpose |
|---|---|---|
| `REPORT.md` | Markdown | Canonical human-readable report (source of truth) |
| `REPORT.tex` | LaTeX | Publication-formatted version with dedicated Genuine Critique section |
| `open_questions.json` | JSON | Five truly OPEN questions in ATCC 202195 / neonatal probiotic biology |
| `workflow.md` | Markdown | Pipeline architecture and per-stage documentation |
| `artifacts_summary.md` | Markdown | This file — inventory of everything produced |
| `failure_analysis.md` | Markdown | What went sideways, what almost went sideways, and what stayed inside expected drift |

## Provenance summary

- **All raw data**: NCBI public deposits, fetched via `curl` (no auth, no gated resources)
- **All tool versions**: fastANI 1.34, skani 0.2, ncbi-blast+ 2.16.0, abricate (DB snap 2026-07-03), python 3.13
- **LLM-judge model**: Argo `gpt-5.2`, temperature 0, free ANL Argo endpoint (`:44497`)
- **No post-hoc parameter tuning** after LLM-judge scoring pass
- **No wet-lab work** attempted (C9 excluded, transparently)

## Reproducibility one-liner

Anyone with `curl`, `fastANI`, `skani`, `ncbi-blast+`, and `abricate` (with the five listed DBs)
installed can recreate this replication end-to-end from the `report/REPORT.md` `2.3 Commands`
section in under an hour on a laptop; the LLM-judge pass requires an OpenAI-compatible endpoint
of any recent frontier model at T=0.
