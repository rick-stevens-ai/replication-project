# Workflow — LUCID DNA-repair kinetics × dose-rate × RBE

Independent replication of Liew et al., IJMS 23, 6268 (2022).

## Stages executed

1. **Paper acquisition.**
   Downloaded MDPI open-access PDF; cached as `paper.pdf`.
   Ran `pdftotext -layout paper.pdf paper.txt`.

2. **Model transcription.**
   Read Sec. 5.2 and Eq. 5; transcribed the photon-side per-cell Monte-Carlo
   into `code/universe_photon.py`. Parameters lifted from Table 1
   (DU145 and RSC rows) verbatim.

3. **Sanity check on photon model.**
   DU145, 2 Gy, 2 Gy/min → S ≈ 0.640 vs LQ prediction 0.622 (2.8% agreement).
   Confirmed by design: at intermediate rate, kinetics is nearly the LQ
   limit, and Table 1 α/β lands on El-Awady 2003 within noise.

4. **R_TD50 headline reproduction (Sec. 3.1 of REPORT.md).**
   Script `code/fig4_left_rtd50.py`:
   - Anchor S* to RSC single-fraction TD50 = 20 Gy (Karger 2003) for the
     1-fraction column and 12 Gy/fr (Karger 2006) for the 2-fraction column.
   - For each dose rate in the paper's Table 3 (11, 18, 42, 53 Gy/min for
     proton 1-fr; 8, 14, 31, 41 for proton 2-fr; 9, 10, 11 for helium 1-fr;
     6, 7, 8 for helium 2-fr), solve for the dose that yields S = S*.
   - Divide by the same dose at 3.75 Gy/min reference to get R_TD50.
   - 600 MC iterations per call; N_t = 100 slabs; N_dom = 3200 domains.

5. **Table 2 saturation-gain reproduction (Sec. 3.2).**
   Script `code/fig12_photon_trend.py`:
   Compute (S_norepair / S_withrepair) at high rate for D ∈ {2, 6, 12, 24} Gy.
   Compare to the paper's low-LET (2 keV/μm) column.

6. **Figures.**
   `code/plot_rtd50.py` overlays the full R_TD50(rate) curve (3.75–100 Gy/min)
   with the 14 paper data points. Output: `figures/fig4_left_RTD50_replication.png`.

7. **Results captured.**
   Numeric outputs saved to `results/rtd50_results.json`,
   `results/fig12_photon_trend.json`, and matching `.log` files.

## Stages NOT executed (out of scope, per REPORT.md §5)

- Ion track-structure sub-model (Kiefer–Chatterjee RDD, Eqs. 6–10).
- Friedrich-2015 LET-dependent DSB-yield boost (formula not printed).
- FLUKA HIT scanned-SOBP beamline simulation (proprietary geometry).
- Full proton/helium RBE-vs-dose-rate curves (Figs. 1, 2, 4 mid/right, 5).
- Independent Bayesian refit of Table 1 parameters (would require assembling
  Karger 2003 + Karger 2006 + Saager 2018 + Hintz 2022 primary TD50 data and
  running MCMC).

## Reproducibility

- All parameters printed in paper Table 1 are used verbatim.
- MC seed is not fixed in `universe_photon.py`; re-run gives ±1% scatter on
  R_TD50 at n_iter=600, consistent with reported MAD floor.
- Runtime on a single M1 core: R_TD50 reproduction ≈ 12 min wall;
  Table 2 sweep ≈ 4 min.

## Backfill note (2026-07-06)

This `report/` subdir was added retroactively to bring the replication into
line with the standard 8-artifact layout (report/REPORT.tex,
open_questions.json, open_questions_section.tex, workflow.md,
artifacts_summary.md, failure_analysis.md, extraction/nougat.mmd).
The original top-level `REPORT.md`, the source scripts under `code/`, the
numeric outputs under `results/`, and the figure under `figures/` are
preserved unchanged. No simulations were re-run for this backfill; the
new artifacts are derivative and reference the existing outputs.
