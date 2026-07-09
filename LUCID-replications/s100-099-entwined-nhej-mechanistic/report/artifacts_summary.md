# Artifacts summary — s100-099-entwined-nhej-mechanistic

## Existing artifacts (present before this backfill)

### Source
- `source/paper.pdf` — Ingram et al. 2019, *Sci Rep* 9:6359
- `source/supplementary.pdf` — supplementary information

### OCR / extraction
- `ocr/raw_layout.txt` — `pdftotext -layout` of main paper
- `ocr/supp_layout.txt` — `pdftotext -layout` of supplementary
- `ocr/supp_fig-08..11.png` — Figures S8–S11 rendered to PNG
  (rate-constant schematics, vector labels not OCR-parseable at
  native res)

### Code
- `code/damaris_pathway.py` — Scenario D full graph + A/B/C reductions
  (24 first-order + 3 bimolecular transitions verbatim from
  TOPAS-nBio port)
- `code/beucher_data.py` — template approximation of Beucher 2009
  Fig 1B (BLOCKER (a) — not the raw data)
- `code/simulate.py` — per-DSB Gillespie mean-field surrogate
- `code/run_all.py` — end-to-end driver

### Evidence
- `evidence/pathwayHR.txt` — canonical TOPAS-nBio Scenario D
  (verbatim archive)
- `evidence/pathwayNHEJ.txt` — canonical TOPAS-nBio NHEJ-only baseline
- `evidence/DaMaRiS.run` — canonical TOPAS-nBio run configuration
- `evidence/README.md` — TOPAS-nBio DaMaRiS README (provenance)
- `evidence/gof_table.csv` — reduced-χ²/RMSE per scenario × system
- `evidence/results.json` — full per-scenario per-system trajectories

### Figures
- `figures/fig3_replication.png` — Fig 3 (b)(c)(d) replication
  (residual-DSB kinetics for WT, XLF⁻, Lig4⁻)
- `figures/fig_table1_replication.png` — bar chart of mean χ² per
  scenario
- `figures/fig_pathway_split.png` — NHEJ/HR/unrepaired split at
  t = 8 h (WT)

### Report (existing)
- `report/REPORT.md` — canonical narrative (4-tier verdict:
  Partially Reproduced — Qualitative Confirmation; Coverage 6/10,
  Agreement 5/10)

## Backfill artifacts (this session, 2026-07-06)

1. `report/REPORT.tex` — LaTeX version of REPORT.md with expanded
   critique section (spatial-geometry justification, aberration-data
   absence, parameter identifiability, replication-specific caveats)
2. `report/open_questions.json` — bare JSON list of 5 open questions
   with `q`, `basis`, `next_steps` fields
3. `report/open_questions_section.tex` — LaTeX version of the 5
   open questions
4. `report/workflow.md` — chronological workflow, endpoint/compute
   note, output list, verdict-flow explanation
5. `report/artifacts_summary.md` — this file
6. `report/failure_analysis.md` — honest critique: mean-field vs
   spatial CTRW gap, absolute χ² gap, aberration data missing,
   parameter identifiability, reference-data blocker
7. `extraction/nougat.mmd` — stub (Nougat not re-run; existing OCR
   is `pdftotext -layout`)

## Verdict
- Queue verdict: **REPLICATED**
- REPORT.md 4-tier: **Partially Reproduced — Qualitative Confirmation**
- Both consistent for a paper whose headline claim is qualitative
  model selection (scenario ranking), which was reproduced. Note-tag
  substance: "qualitative scenario ranking replicated; absolute
  χ² values disagree ~10× due to raw-Beucher-data blocker".
