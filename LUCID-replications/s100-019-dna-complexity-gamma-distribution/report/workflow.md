# Workflow — Slot #19 (LUCID-Second100)

**Paper:** Bertolet et al. (2023), *Frontiers in Oncology* 13:1196502
**doi:** 10.3389/fonc.2023.1196502
**Replicator:** Ollie (LUCID-Second100 pipeline)
**Date:** 2026-06-22; backfilled 2026-07-06
**Compute:** local CPU only (Python 3 + numpy + scipy + matplotlib + pandas). ≈10 s total wall.
**Endpoints used:** Argo Opus 4.7 (free) only. No paid APIs. No author contact. No new MC.

---

## Chronological steps

### 1. Paper acquisition + text extraction
- Downloaded PDF from Frontiers (open access).
- Extracted layout text with `pdftotext -layout` → `ocr/raw_layout.txt`.
- (No `nougat.mmd` at original replication time; backfill stub added
  2026-07-06 as `extraction/nougat.mmd` — placeholder only, since the
  layout extract was sufficient for parameter-constant retrieval.)

### 2. Code + data acquisition
- Cloned `github.com/MGHPhysicsResearch/MGM`.
- Copied `src/mgm.py`, `README.md`, `script_monoenergetic.py`, and
  `data/xray_microdosimetry_1um.phsp` into `source/` verbatim (single
  code + one data file; the repo has no other bundled data).
- No TOPAS-nBio SDD files exist in the repo, in Frontiers SM, or in any
  public TOPAS-nBio dataset located — confirmed as reproducibility Blocker #1.

### 3. Analytical-layer replication (`code/replicate_mgm.py`)
- Ported the authors' parametric forms verbatim (linear SBD, saturating-exp
  SBI, linear BDD, saturating-exp BDI, linear+saturating-exp N_sites,
  linear-quadratic N_sites_with_DSB) with the constants copied directly
  from `src/mgm.py`.
- Evaluated all six functions on a 400-point dense yF grid ∈ [0.5, 400]
  keV/µm → `evidence/fig2_damage_vs_yF.csv`.
- Evaluated α(yF), β(yF) quadratics on the same grid →
  `evidence/fig3_gamma_parameters_vs_yF.csv`.
- Generated Gamma complexity PDF at yF = 7.5 keV/µm (5-MeV proton regime)
  and yF = 95 keV/µm (4-MeV alpha regime) →
  `evidence/fig3_summary_per_beam.csv`.

### 4. Gamma-form audit (Issue #1 diagnostic)
- Ran three candidate SciPy Gamma calls at yF ∈ {2, 5, 10, 30, 100, 150, 200}:
  (a) paper text formula `stats.gamma(a, scale=1/b).pdf(C)`;
  (b) author-code call `stats.gamma(a, b).pdf(C)`;
  (c) author-code-with-scale `stats.gamma(a, scale=b).pdf(C)`.
- Recorded per-C values for C ∈ {1, 2, 3, 5, 10} for each yF and each variant →
  `evidence/gamma_form_audit.csv` (21 rows).
- Documented finding as Issue #1 (author-code passes b as loc, not as rate).

### 5. Spot-value validation
- Evaluated α, β at the five canonical yF referenced in the paper text:
  2, 10.95 (3-MeV proton), 50, 115.3 (3-MeV alpha), 200 keV/µm.
- Confirmed β(200) = -0.859 → improper Gamma at upper end of claimed
  validity window → Issue #2. Recorded in `evidence/replication_summary.json`.

### 6. End-to-end pipeline test (X-ray)
- Loaded `source/xray_microdosimetry_1um.phsp` (116 077 events).
- Subsampled 1 000 events per README example.
- For each event: computed lineal energy y, evaluated MGM per-event,
  accumulated complexity PDF weighted by event probability.
- Recovered `n_sites_with_DSB_per_track = 0.091`, mean complexity = 2.35,
  mode = 2 → `evidence/xray_complexity_distribution.csv`.

### 7. Figure regeneration
- `figures/fig2_damage_vs_yF.png` — 3-panel reproduction of Figure 2.
- `figures/fig3_complexity_and_gamma_params.png` — 4-panel reproduction of Figure 3.
- `figures/xray_complexity_distribution.png` — X-ray bar chart.

### 8. Reporting
- Wrote `report/REPORT.md` with four-tier verdict, coverage 7/10,
  agreement 9/10, claim-by-claim table (12 claims), two flagged issues,
  four blockers, files inventory.

### 9. Backfill (2026-07-06)
- Added `report/REPORT.tex` (LaTeX render with expanded critique).
- Added `report/open_questions.json` (5 concrete follow-up probes).
- Added `report/open_questions_section.tex` (LaTeX version).
- Added `report/workflow.md` (this file).
- Added `report/artifacts_summary.md` (artifact inventory).
- Added `report/failure_analysis.md` (honest critique of what this
  replication does not answer).
- Added `extraction/nougat.mmd` stub (placeholder — see note under §1).
- Flagged verdict cross-check: queue-side REPLICATED label is a
  candidate mismatch (analytical-only replication, MC never re-run
  → should probably map to PARTIAL/SPOT-CHECK under the four-tier
  rubric). Preserved as REPLICATED per instruction; flag documented
  in REPORT.tex §"Verdict cross-check".

---

## What was skipped and why

- **TOPAS-nBio MC re-run.** GBs of compute + not-deposited raw data
  → outside slot budget. This is the central reproducibility gap of
  the paper and is honestly documented, not hidden.
- **Least-squares refit of (α, β).** Cannot refit without raw SDD →
  we adopted authors' published constants verbatim.
- **Figures 4 (3-MeV validation) and 5 (cell survival).** Depend on
  external experimental data (Hill 2004, Jones 1987) and a sigmoid
  repair model the paper itself calls "qualitative" → out of scope.
- **Alternative distribution-family comparison (Gamma vs log-normal
  vs negative-binomial vs mixture).** Cannot do without the raw
  histograms; flagged as Open Question #1 for follow-up.
- **Author contact.** Explicitly excluded per free-endpoints-only
  policy (no new solicitation of authors during automated slot work).

---

## How to re-run

```bash
cd code && python3 replicate_mgm.py
```

≈10 s on any CPU with numpy + scipy + matplotlib + pandas installed.
Outputs land in `evidence/` and `figures/` (deterministic;
`numpy.random.default_rng(seed=42)` for the 1 000-event X-ray subsample).
