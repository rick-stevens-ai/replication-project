# PROGRESS log — LUCID100 slot 33

## 2026-06-09 (Wave 4 max-rate backfill, subagent)

### 13:47-14:00 CDT — context + artifact harvest
- Located paper in master QA TSV (`LUCID100_SOLID_MASTER_QA.tsv:82`); confirmed DOI, abstract, datasets (GSE8917/GSE43151/GSE23515) match.
- Source PDF behind Cloudflare on tandfonline.com (HTTP 403). PMC is reCAPTCHA-gated. Successfully retrieved the **full PMC NXML** via NCBI eutils `efetch.fcgi?db=pmc&id=10845127&rettype=xml` (134 KB), giving us complete methods, results, references, and Tables 1 and 2.
- Transcribed Table 1 (dataset metadata) and Table 2 (25 common DE genes with β1, β2, P2, cluster per dataset) to `data/table1_datasets.tsv` and `data/table2_25_common_DE_genes.tsv`.

### 14:00-14:08 CDT — GEO data ingest
- HEAD-checked GEO series-matrix sizes: 7.5 + 5.2 + 17.4 MB compressed → ~30 MB total. Trivially fits on CherryRd; no need for cluster compute.
- Downloaded all three `*_series_matrix.txt.gz` to `data/geo_series_matrix/`.
- Verified parses: GSE8917 = 50 samples × 43931 probes (GPL1708); GSE43151 = 121 samples × 19246 probes (GPL13497); GSE23515 = 95 samples × 41093 probes (GPL6480). All in log2-intensity range (0-20).

### 14:08-14:35 CDT — smoke replication script
- Wrote `code/01_smoke_lme_25genes.py`:
  1. Read each `series_matrix.txt.gz` and the corresponding GPL platform annotation (auto-downloaded once on first run).
  2. For each dataset, parse `Sample_title` into `(dose_Gy, time_h, donor)`.
  3. Compute per-sample LFC = `expr − mean(expr at dose=0 with matching time)`. Normalize dose and time to [0,1] as in the paper.
  4. Restrict to the 25 Table-2 genes (mean across probes per gene), fit `LFC ~ const + β1·dose + β2·time + (1|donor)` with `statsmodels.MixedLM` (REML=False, lbfgs); fall back to OLS with cluster-robust SE by donor when MixedLM is singular.
  5. Compare estimated (β1, β2, cluster) to Table 2; write 4 result TSVs + JSON summary.

### bugs & fixes during the smoke
- First pass: LD agreement was 8% (1/25 sign match). Root cause: `GSE43151` `Sample_title` dose tokens are e.g. `D0005Gy = 0.005 Gy` (decimal stripped); my regex captured `0005` and parsed it as float = 5 instead of 0.005. Fixed with explicit lookup table (`GSE43151_DOSE_LOOKUP`).
- Second pass: HD agreement was 40% (10/25), with the *fitting* 10 genes all matching β1 to 3 decimals but 15 silently returning NaN. Root cause: GSE8917 has different donors at 6 h and 24 h, so `donor` and `time_norm` are perfectly collinear → `MixedLM` random-intercept singularity → `LinAlgError`. Fixed by adding OLS-cluster-robust fallback inside `fit_lme`. After fix: all 23 mappable genes fit (CCDC109B and F11R don't appear in the GPL1708 annotation table under those symbols — probably retired aliases).
- Final pass results (in `results/lme_smoke_summary.json`):
  - **HD GSE8917**: 23/25 fit, dose-sign match 88%, cluster match 84%.
  - **LD GSE43151**: 25/25 fit, dose-sign match 100%, cluster match 64%.
  - **VAL GSE23515**: 24/25 fit (no time dimension; only β1 fitted).
  - 21/23 HD β1 estimates and 22/25 LD β1 estimates match the paper to within ±0.02.

### deliverables
- `data/efetch.xml`, `data/paper_fulltext.txt` (paper, full text)
- `data/table1_datasets.tsv`, `data/table2_25_common_DE_genes.tsv` (paper's own tables)
- `data/geo_series_matrix/{GSE8917,GSE43151,GSE23515}_series_matrix.txt.gz`
- `data/platform_annot/{GPL1708,GPL13497,GPL6480}_annot.tsv.gz`
- `code/00_download.sh`, `code/01_smoke_lme_25genes.py`
- `results/lme_smoke_HD_GSE8917.tsv`, `results/lme_smoke_LD_GSE43151.tsv`, `results/lme_smoke_VAL_GSE23515.tsv`, `results/lme_smoke_agreement.tsv`, `results/lme_smoke_summary.json`
- `README.md`, `FIRST_PASS_REPORT.md`

### blockers / not done
- The paper's supplementary `NIHMS1923450-supplement-Supp_4.xlsx` (full DEG lists with cluster assignments) sits behind PMC reCAPTCHA — not retrievable from `web_fetch` / `curl`. Not blocking: the GEO matrices contain everything needed to regenerate it.
- We did not regenerate the full ~266 HD / ~354 LD whole-transcriptome DEG lists; the smoke only fits the 25 Table-2 genes. Extending the same LME loop over all genes is a half-hour CPU job on CherryRd.
- Figures 1-5 were not regenerated as PNGs in this pass. The data underneath are available in `results/`; a `02_figures.py` script is the obvious next deliverable.

### next actions (not done in this pass)
1. Run the LME over the full preprocessed gene set per dataset (8639 / 13447 / 12152 genes) to regenerate the 266/354 DEG lists with cluster labels. Compare counts and overlap with the paper's 25 common DEGs.
2. Wire pathway enrichment via `gseapy.enrichr` (Python) or local `MSigDB` to reproduce Figures 1C-D, 4C (KEGG p53 / NK-cell etc.).
3. Render Figure 3 (LFC 3D surfaces by cluster) and Figure 5 (validation boxplots) — straightforward matplotlib.
4. Attempt PMC supplementary download via `browser` tool (logged-in profile) to cross-check our 266/354 DEG numbers against `Supp_4.xlsx` directly.

### QA retag recommendation for master spreadsheet
- KEEP slot 33 as `candidate_curated`.
- Add: `replication_status=PARTIAL-strong`, `data_availability=public (3 GEO series, ~30 MB total)`, `code_availability=none (MATLAB fitlme + R+Enrichr/STRING described in methods only)`.
