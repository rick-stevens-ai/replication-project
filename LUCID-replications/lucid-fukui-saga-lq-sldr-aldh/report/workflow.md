# Workflow — Fukui et al. 2022 IMK Replication

## Provenance
- **Pass 1:** LUCID initial replication, 2026-06 (script + vision digitization).
- **Re-pass:** 2026-06-23, adds 5 text-grounded claims (A–G) previously skipped.
- **Backfill:** 2026-07-06, adds 8-artifact-standard report/, extraction/, open questions.

## Steps executed

1. **Ingest.** PDF → `data/source-paper.pdf` (md5 `acbb80ecc6f5bfe135a0081aa2be4c9b`).
2. **Extract.** Marker on uicgpu 2026-06-22 → `data/marker_paper.md` (md5 `f01a1853869d563a72c5c1c06f145e12`) plus per-page JPEGs in `data/marker_figures/`. Nougat stub placeholder in `extraction/nougat.mmd`.
3. **Model implement.** `code/imk_model.py` re-implements Eqs 1, 2, 4, 6, 7, 12, 13, 14 in pure NumPy. Table 1 verbatim in `code/params_table1.py`.
4. **Fig 5 forward.** `code/replicate_fig5.py` — computes S(D) using Table 1 means, compares against vision-digitized points in `code/digitized_fig5.py`. R² 0.960–0.997 in −ln S space.
5. **MCMC refit.** `code/refit_mcmc.py` — independent MCMC on digitized Fig 5. Recovers `w_SLDR(SAS-R)=1.11±0.20` (paper 1.06±0.12), `w_SLDR(HSC2-R)=1.93±0.47` (paper 1.90±0.45).
6. **Fig 6 forward.** `code/replicate_fig6.py` — computes S_split(2+2, τ)/S_acute(4Gy). Pass-1 vision digitization was wrong-signed; re-pass uses forward-prediction only.
7. **Re-pass claims A–G.** `code/repass/repass_all_claims.py` — single script covering:
   - A: ALDH+% (Fig 3) vs f_s posterior (Table 1) → 4/4 within 1σ.
   - B: (a+c) from Fig 2 vs Table 1 (a+c)_p* → within 3%.
   - C: w_SLDR = (a+c)_H/(a+c)_p Eq 9 consistency → exact to 4 sig figs.
   - D: Fig 6 forward-predict recovery saturates at τ ≈ 2–3 h → matches paper.
   - E: Fig 7 forward-predict dose-rate saturates at 1 Gy/min and 0.01 Gy/min → matches.
   - F: α_0,s < α_0,p and β_0,s < β_0,p constraint → SAS OK, HSC2 α violates (<1σ, honest negative).
   - G: (a+c)_H within Matsuya 2018 reference range 1.506–2.218 → ±1σ overlap.
8. **Report.** Original REPORT.md at top level (preserved). LaTeX writeup in `report/REPORT.tex` with honest critique + `\input{open_questions_section.tex}`. 5 open questions with concrete next_steps in `report/open_questions.json`.

## Compute usage
- All CPU, free endpoints only (Argo Opus 4.7).
- No paid API calls, no author outreach, no wet-lab.
- Total wall time (both passes): ~4 hours on CherryRd.

## What was NOT done (see failure_analysis.md)
- No wet-lab clonogenic assay reproduction.
- No raw FCS re-analysis.
- Fig 7 not vision-digitized (only forward-predicted).
- No IMK microdosimetric-kernel first-principles re-derivation.
- No author contact.

## Artifacts summary → see `report/artifacts_summary.md`
