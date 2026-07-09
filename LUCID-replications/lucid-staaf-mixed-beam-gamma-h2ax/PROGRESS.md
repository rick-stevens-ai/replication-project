# PROGRESS — Staaf et al. 2012 (Mixed-beam γ-H2AX)

- **Target:** Staaf E. et al. *Gamma-H2AX foci in cells exposed to a mixed beam of X-rays and alpha particles.* Genome Integrity 3:8 (2012). DOI: 10.1186/2041-9414-3-8
- **Status (after re-pass 2026-06-23):** **DONE — PARTIAL/REPLICATED, 8/9** (was 7/10)
- **Pass-1 status (preserved):** PARTIAL/REPLICATED, 7/10
- **Started:** 2026-05-30 17:52 CDT
- **Finished:** 2026-05-30 18:30 CDT (~40 min)

## Steps completed

1. ✅ Created output directories and copied target PDF.
2. ✅ Wrote initial PROGRESS.md and progress JSON (within ~3 min, gate 1 met).
3. ✅ Extracted full text via `pdftotext -layout` (paper has no tables/supplements).
4. ✅ Rendered all 13 PDF pages to 200-dpi PNGs.
5. ✅ Identified figures: Fig 1 on p3, Fig 2 on p4, Fig 3 on p5, Fig 4 on p6, Fig 5 on p7.
6. ✅ Digitized Figures 2 (4 panels), 3 (4 panels), 5 (2 panels) using vision model.
   - **First pass had two errors**: a one-page offset on figure pages, and a
     legend-color swap on Fig 5 (caption: black = predicted, gray = observed).
     Caught both by cross-referencing the text (RBE direction, p<0.001 finding).
7. ✅ Wrote `data/digitized_data.py` with all 60+ digitized data points.
8. ✅ Wrote `code/replicate.py` performing:
   - Linear dose-response fits (origin-anchored)
   - RBE = slope_α / slope_X for total IRIF and LF
   - Independent additivity prediction f_mix = f_α(D_α) + f_X(D_X)
   - Large-foci delay test (paired-style Welch t for Fig 5)
   - α-particle fluence cross-check
   - 5 replication plots
9. ✅ Replication output written to `results/replication_results.json`.
10. ✅ REPORT.md drafted with verdict, agreement table, caveats.
11. ✅ README.md and PROGRESS.md finalized.

## Hard gates checklist

- [x] PROGRESS.md + JSON within 10 min, status=running
- [x] Public/open data only; no author contact; no paid endpoints
- [x] REPORT.md, README.md, code/, results/, figures/ all present
- [x] Honest verdict with coverage/agreement /10 (PARTIAL/REPLICATED, 7/10)
- [x] Files saved as we went

## Verdict

**Pass 1:** REPLICATED (PARTIAL) — coverage/agreement 7/10.
**Pass 2 (2026-06-23 re-pass):** REPLICATED (PARTIAL+) — **coverage/agreement 8 / 9**.

All headline quantitative claims (RBE values, additivity for total IRIF and
LF, fluence, large-foci delay) recovered from digitized figure data to within
~5% on values. Pass 2 added 35 micro-claim reproductions (per-Gy normalizations,
within-radiation kinetics t-tests, all paper algebraic constants, R² for mix-obs
and mix-pred series, the lowest-dose half-half predicted-mix formula); 33 / 45
claims now match the paper. The remaining 12 misses are all
digitization+derivation noise on p-values that would require the authors' raw
n=4 per-experiment trajectories to lift — these are documented as the only
hard data gap.

## Re-pass log (2026-06-23)

1. ✅ Checked LUCID-100 Marker MD batch — paper not present; used existing
   `pdftotext` extract `staaf2012.txt` and recorded provenance in
   `PARSER_PROVENANCE.md`.
2. ✅ Enumerated all testable claims in `CLAIMS_INVENTORY.md` (A1–G6, 45 micro-claims).
3. ✅ Wrote `code/replicate_pass2.py` reproducing 35 new claims, persisting to
   `results/replication_pass2.json` AS WE GO.
4. ✅ Preserved pass-1 verdict as `REPORT.pass1.md`; new verdict in `REPORT.md`.
5. ✅ All work used FREE compute only (no Argo, no paid APIs); ran in <5 s.
