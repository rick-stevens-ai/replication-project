# PROGRESS — lucid100-snp-occupational-radiosensitivity

## 2026-06-09 13:35 — kickoff (subagent, depth 1, max-rate Wave 3 slot 26)

- Task: first-pass artifact harvest + replication scoping + minimal runnable attempt for Botbayev 2026, *Genes* 17(2):191, DOI 10.3390/genes17020191.
- LUCID100 source-of-truth row confirmed: rank 57, Wave 3, Tier A, priority 16, status `candidate_curated`, verdict_or_plan = "TODO: omics/signature replication; artifact harvest; brief; run; report".
- Created workspace at `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-snp-occupational-radiosensitivity/`.

## 2026-06-09 13:36 — paper acquisition

- `web_fetch` to MDPI: blocked (406).
- `curl` w/ Firefox UA + Akamai cookies: blocked (HTML challenge).
- **OpenClaw browser → navigate → pdf**: SUCCESS (3.9 MB rendered article PDF + full DOM).
- Verified Semantic Scholar entry: PubMed 41751575, 11 Kazakh authors, OA CC-BY.
- Verified Unpaywall: `is_oa=true`, version `publishedVersion`, license `cc-by`.

## 2026-06-09 13:37 — text + table extraction

- `pdftotext -layout` → `paper.txt` (127 KB, 2000 lines, full body + chrome).
- Discovered all 7 main-text tables are **rendered as images** in the PDF but ALSO live as HTML `<table>` elements in the DOM.
- Browser DevTools `document.querySelectorAll('table')` → 9 tables → wrote `tables/tables_extracted.json`.
- Key finding from text: **Data Availability = "available on request from corresponding author"** (no public deposit anywhere).
- Supplementary Materials S1 (Stepnogorsk APC/VEGF/XPD/RAD51) and S2 (Balkashinskoye APC/VEGF/XPD/RAD51) referenced at `/article/10.3390/genes17020191/s1`.

## 2026-06-09 13:38 — supplementary harvest attempt (blocked)

- `curl` w/ browser cookies → HTML challenge (Akamai `bm-verify`).
- Browser `navigate` to s1 → "Download is starting" navigation error (Chromium sandbox blocks downloads in our config).
- Synthetic anchor `.click()` → no file appeared in `~/Downloads`.
- **Decided to proceed without S1/S2** (only contain the 4 non-significant SNPs; primary claim unaffected). Documented blocker in MANIFEST.json.

## 2026-06-09 13:42 — minimal statistical replication

- Wrote `code/replicate_chi2_or.py`:
  - Reconstruct genotype counts via largest-remainder rounding of `f × N` (Table 1 gives N per location × ethnic group).
  - Recompute Pearson 2×3 genotype chi² and 2×2 allelic chi², plus Woolf allelic OR with 95% CI, plus HWE in both arms.
  - Compare to paper-reported chi²/p/OR/CI on every cell.
- Ran on CherryRd Python: scipy 1.17.1 / numpy 2.4.3. <1 second; no compute concerns.
- Output: `results/replication_chi2.json` (16 cohort × SNP cells = 4 SNPs × 4 cohort-by-ethnic strata).
- **Bug fix:** first pass overwrote paper-published stat fields with `None` on continuation rows; fixed to keep first non-None value per block.

## 2026-06-09 13:43 — concordance figure

- `code/plot_p_comparison.py` → `figures/p_value_comparison.png` (paper-reported vs recomputed −log10(p) for genotype and allele tests, both panels).

## 2026-06-09 13:45 — summary

- 13/16 genotype p<0.05 decisions agree with paper.
- All allelic OR values reproduce within ±5 % EXCEPT (a) rs1625895 cells where paper reports OR<1 against my OR≈2.0 (paper appears to flip allele convention), (b) two rs1801270 cells.
- **Likely typo flagged:** Table 4 row "Stepnogorsk × Russians × rs17878362" prints chi² genotype = 16.55, p = 4.736 — a p-value > 1 is impossible; this is a column-shift error in the source HTML/PDF.
- HWE issues detected: rs1625895 controls deviate from HWE in Stepnogorsk Kazakh (p<0.0001); the paper does not discuss HWE in either arm despite claiming "all loci were tested for Hardy–Weinberg equilibrium."

## Status: COMPLETE for first pass.

- Verdict: **PARTIAL (consistent at table-reconstruction level)**.
- No-go on deeper replication without author data; documented in FIRST_PASS_REPORT.
- QA retag: `replication_partial_table_only` — KEEP at Tier A.
