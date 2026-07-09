# Artifacts Summary — Franken 2012 alpha vs gamma RBE

## Original paper
- `franken_2012.pdf` — Franken et al., Oncology Reports 27:769–774 (2012).
  DOI 10.3892/or.2011.1604.

## Reports (top-level, preserved)
- `REPORT.md` — canonical pass-2 report (source of truth for this replication).
- `REPORT.pass1.md` — preserved pass-1 report.
- `PROGRESS.md` / `PROGRESS.pass1.md` — pass status logs.
- `PARSER_PROVENANCE.md` — parser audit (pass 2).
- `README.md` — dir intro.

## Reports (this backfill, `report/` subdir)
- `report/REPORT.tex` — full LaTeX write-up with honest Critique section
  and `\input{open_questions_section.tex}` at the end.
- `report/open_questions.json` — 5 open questions (JSON list of `{q, basis, next_steps}`).
- `report/open_questions_section.tex` — LaTeX rendering of the same 5 questions.
- `report/workflow.md` — pipeline description (pass 1 + pass 2).
- `report/artifacts_summary.md` — this file.
- `report/failure_analysis.md` — honest critique / limits / what was NOT done.

## Code
- `code/refit_rbe.py` — pass 1: LQ α-ratio RBE recomputation + σ propagation
  for the 4 Table-I endpoints.
- `code/pass2_extended_claims.py` — pass 2: Fig-2 effect-level RBE, inferred
  β_γ from iso-survival constraint, factor-4 check, decade-divergence at 2 Gy.

## Results
- `results/rbe_recomputed.json` — pass 1: recomputed RBE + σ per endpoint,
  vs paper's Table I values, match booleans.
- `results/lethal_dsb_fraction.json` — pass 1: α_survival / α_γ-H2AX ratios
  for α and γ ("~1%" and "~10%" Discussion checks).
- `results/summary.json` — pass 1 rollup.
- `results/pass2_extended_claims.json` — pass 2: all 8 new claim results
  (C7-C12 + inferred β_γ + factor-4 ratios + divergence-at-2Gy).

## Figures
- `figures/fig2_reconstructed.png` — Fig. 2 reconstruction from LQ (α-only for
  linear endpoints; pure-exponential for survival) using Table I fit
  parameters. Not a raw-data replot (paper deposits no data); purely a
  fitted-curve rendering that visually matches Fig. 2's slopes.

## Extraction
- `extraction/nougat.mmd` — stub / placeholder for the Marker MD parser
  output pointer (canonical text lives under
  `_LUCID100_ADMIN/marker_md_uicgpu_20260622/merged/555f0ea0.../`).
  See `PARSER_PROVENANCE.md` for the actual parser trail.

## Claim coverage snapshot
- 13 testable claims enumerated.
- 12 recomputed and passing.
- 1 (C13, per-dose raw points) blocked by no data deposit — the single named
  "6/22 rule" missing artifact.
- Coverage 92%; agreement 12/12.
