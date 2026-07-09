# PROGRESS — LUCID replication: Guo et al. 2022 (industrial irradiation workers, blood parameters)

- **Status:** DONE (first-pass)
- **Verdict:** PARTIAL
- **Started:** 2026-06-09 13:12 CDT
- **Finished:** 2026-06-09 13:25 CDT
- **Target:** Guo et al., *Dose-Response Effects of Low-Dose Ionizing Radiation on Blood Parameters in Industrial Irradiation Workers,* DOI 10.1177/15593258221105695, PMC9174562
- **Output:** `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-industrial-workers-blood-dose-response/`

## Log

- 13:12 — Workspace created, paper located in LUCID100 master TSV (Wave 2 / Tier A / rank 48 / slot 17). Master labels worktype `simulation/model replication` — flagged for QA review on first read of abstract (paper is clearly an epidemiological cohort regression study).
- 13:13 — Crossref pulled metadata (8 authors, Guangdong Pharmaceutical University). PubMed -> PMID 35693871. Europe PMC fulltextXML -> PMC9174562 (118 kB JATS XML).
- 13:14 — Sage and PMC HTML scrapes blocked (403 / reCAPTCHA). Europe PMC `fullTextXML` succeeded. Plain-text + Markdown render of XML written to `paper.txt`, including all 3 tables.
- 13:16 — Confirmed: paper has **zero simulation content**. Stats stack = Stata 16.1 GLM + restricted-cubic-spline. No Monte Carlo, no biophysical model.
- 13:17 — Replication strategy chosen: (A) internal consistency of Table 3, (B) approximate refit from Table 2 medians+IQR with N=400 bootstrap. Both fit on commodity Python in seconds — no heavy compute needed.
- 13:19 — `statsmodels 0.14.6` installed via `pip --user --break-system-packages` (numpy 2.4.3, scipy 1.17.1, pandas 3.0.2 already present).
- 13:21 — `code/replicate_lucid.py` written and run.
- 13:22 — Results:
  - (A) Internal consistency: max |ΔZ|=0.039, max |ΔCI|=0.029 across all 9 rows. Printed numbers are mutually consistent to standard rounding. Noted likely sign typo in printed RBC CI upper bound (paper prints +0.015; (β, SE) implies −0.014).
  - (B) Approximate refit: 9/9 simulated β values within 2·SE_published of published values. Mean |z|=0.59, worst |z|=1.19. Signs match in 8/9 (the one discrepancy is statistically indistinguishable from zero in both).
- 13:23 — Forest plot `figures/beta_published_vs_simulated.png` rendered.
- 13:24 — README.md, REPORT.md, MANIFEST.json written.
- 13:25 — `memory/subagent-progress/lucid100-industrial-workers-blood-dose-response.json` updated to status=done.

## Key blockers and notes

- **No individual-level data deposited.** Restricted-cubic-spline curves and inflection points cannot be reproduced without raw data. Author contact not attempted (per backfill rules).
- **QA retag recommended:** worktype `simulation/model replication` → `statistical reanalysis / cohort regression replication`. Drop themes `computational model / simulation`, `DNA repair / DDR`, `radiation quality / RBE` — none apply. Add `epidemiology / cohort study`, `hematology / hematopoietic system`.
- **Compute footprint:** ~10 s on CherryRd CPU. No GPU. No heavy compute. No job-plan file needed.
