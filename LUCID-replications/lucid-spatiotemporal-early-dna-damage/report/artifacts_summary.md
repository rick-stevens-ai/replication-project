# Artifacts Summary

Full inventory of what lives in this replication directory, plus friction
tags for anything that a downstream reader should know is fragile,
digitized, or otherwise non-canonical.

## Source paper

| Path | What it is | Friction |
|---|---|---|
| `source.pdf` | PLOS ONE PDF of Tobias et al. 2013 | — |
| `source.txt` | `pdftotext -layout` extract of the body | layout-mode; column headers occasionally split |
| `PARSER_PROVENANCE.md` | Which parser produced which artifact | — |
| `supplements/` | All 6 PLOS supplements (S1–S4 TIFFs, Table S1 DOC, File S1 DOC + `.txt` extracts) | textutil DOC→txt is lossy for embedded tables — Table S1 required manual cleanup |

## Claims & report

| Path | What it is | Friction |
|---|---|---|
| `CLAIMS.md` | Full enumeration of testable claims with cov/new/blocked tags | manually curated; check completeness against paper before extending |
| `REPORT.md` | Canonical Markdown report (re-pass) | — |
| `REPORT.pass1.md` | Prior-pass report preserved as sibling | do not delete — provenance |
| `report/REPORT.tex` | LaTeX version (this backfill) | requires `open_questions_section.tex` via `\input` |
| `report/open_questions.json` | 5 truly-open questions with next steps | JSON, machine-readable |
| `report/open_questions_section.tex` | LaTeX mirror of open_questions.json | included by REPORT.tex |
| `report/workflow.md` | Pipeline, tools, versions, reproducer | — |
| `report/artifacts_summary.md` | This file | — |
| `report/failure_analysis.md` | Honest critique of what didn't work | — |
| `PROGRESS.md` | Stage-by-stage log | — |
| `README.md` | Quick-start | — |

## Code

| Path | What it is | Friction |
|---|---|---|
| `code/lucid_model.py` | 9-reaction / 13-species ODE model, `scipy.solve_ivp` LSODA | one File-S1 parameter-mapping ambiguity is resolved by explicit choice; documented in the file header |
| `code/figure11_replication.py` | Reproduces Fig. 11 (4 panels) | deterministic |
| `code/quantitative_check.py` | Compares model to digitized Fig-S1 A + L | digitization noise ~10–20%; Panel F dropped (LET label unreadable) |
| `code/figure_overlay.py` | Model + digitized data overlay figure | requires digitized points from `figures/` metadata |
| `code/c3_dsb_fluence_arithmetic.py` | A3 | pure arithmetic |
| `code/c4_diffusion_arithmetic.py` | A4, A5, A6 | 2D vs 3D geometry ambiguity resolved by matching paper's 0.83 s — see file comments |
| `code/c5_tableS1_trends.py` | C1, C2, C3 | Ni-ions outlier NOT excluded from Spearman ρ |
| `code/c6_model_extended_claims.py` | B5, B6, B7, B8 | integrates ODE model at multiple LETs; ~30 s runtime |
| `code/c7_mdc1_diffusive_influx.py` | B9 | qualitative check only (no Fig. 12B digitization) |

## Extraction

| Path | What it is | Friction |
|---|---|---|
| `extraction/nougat.mmd` | Nougat-style extraction stub with paper.pdf sha256 pointer | STUB — no GPU parse performed; body text is available via `source.txt` |

## Figures

| Path | What it is | Friction |
|---|---|---|
| `figures/figure11_replication.png` | Our re-implemented Fig. 11 | matches paper qualitatively across 4 panels |
| `figures/data_overlay.png` | Model+data overlay for panels A, L | digitized points; ~10–20% precision |

## Results (per-claim JSON)

| Path | Claims | Friction |
|---|---|---|
| `results/figure11_summary.json` | Panel-by-panel τ₆₃ and inner-fraction | — |
| `results/quantitative_check.json` | Numerical agreement table (digitized) | digitization noise |
| `results/c3_dsb_fluence.json` | A3 | — |
| `results/c4_diffusion.json` | A4, A5, A6 | — |
| `results/c5_tableS1_trends.json` | C1, C2, C3 | Ni-ions outlier included |
| `results/c6_model_extended.json` | B5, B6, B7, B8 | — |
| `results/c7_mdc1_diffusive.json` | B9 | qualitative only |

## Traces

- All ODE integrations use `scipy.integrate.solve_ivp` with method
  `LSODA` and `rtol=1e-8`, `atol=1e-3`, `max_step=1.0`. No RNG in the
  numerical layer — every re-run gives bit-identical output on the same
  hardware/BLAS.
- Digitized figure points (Fig. S1 panels A and L) are stored as inline
  literals in `code/quantitative_check.py`; their provenance
  (vision-model + manual QA) is noted in-file.

## Friction tag summary

- **digitization** — anything derived from digitized figure points
  (~10–20% precision)
- **parameter ambiguity** — one File-S1 "and"-joined rate value with two
  possible mappings; explicit choice made in `lucid_model.py`
- **qualitative only** — B9, D4
- **blocked** — A7, A8, D1, D2, D3 need raw imaging or FRAP CSVs not
  in the public record; contact GSI / TU Darmstadt authors
- **outlier included** — C1 Spearman ρ includes the Ni-ions outlier
  (LET=3430, koff=0.030) which the paper's Fig 8A shows has large
  error bars

## Blocked claims / missing artifacts

- **A7 & A8** — raw MDC1-GFP FRAP intensity time-series CSVs (X-ray, C-ion
  LET=170, Au-ion LET=13000) with bleach geometry parameters. Not
  published.
- **D1** — raw beamline microscopy `.tif`/`.h5` time-lapse stacks. Not
  published.
- **D2** — raw NBS1 FRAP intensity time-series (all LETs, ±CK2i). Not
  published.
- **D3** — raw confocal `.czi`/`.tif` stacks for foci-size analysis. Not
  published.
- **D4** — 53BP1 lag phase (Fig S2). Digitizable but claim is purely
  qualitative.

All five would require direct contact with GSI Darmstadt / TU Darmstadt
authors to obtain.
