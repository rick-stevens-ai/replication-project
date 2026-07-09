# Artifacts Summary

## Inventory
| Path | Type | Description | Friction |
|---|---|---|---|
| `source.pdf` | input | Local copy of Ulyanenko 2019 IJMS OA PDF | none |
| `source.txt` | input | pdftotext extraction of source.pdf | none |
| `REPORT.md` | report | Original Markdown replication report (verdict + tables) | none |
| `README.md` | doc | Quickstart | none |
| `PROGRESS.md` | log | Running work log | none |
| `code/digitize_from_tables.py` | code | Algebraic inversion of Tables 1–3 → I_0, I_Di + linear fits + hockey-stick fits | none |
| `code/make_figures.py` | code | Regenerate all 6 figures | none |
| `results/digitized_tables.json` | output | Recovered per-dose foci counts + all fit coefficients | none |
| `figures/fig1A_gH2AX_dose_response.png` | figure | Reproduces paper Fig 1A | none |
| `figures/fig1B_gH2AX_chronic_hockey_stick.png` | figure | Reproduces paper Fig 1B | none |
| `figures/fig2A_pATM_dose_response.png` | figure | Reproduces paper Fig 2A | none |
| `figures/fig2B_pATM_chronic_hockey_stick.png` | figure | Reproduces paper Fig 2B | none |
| `figures/fig3_colocalization.png` | figure | Approximates Fig 3 (interpolated intermediate points, flagged) | **medium**: intermediate dose points are interpolations, not digitized pixels |
| `figures/fig4_kinetics.png` | figure | Reproduces Fig 4 via single-exp decay | **medium**: single-exp is a stand-in; paper decay form not stated |
| `report/REPORT.tex` | report | This backfill: LaTeX report with critique + open-questions include | none |
| `report/open_questions.json` | data | 5 truly-open questions in structured form | none |
| `report/open_questions_section.tex` | report | LaTeX render of the 5 open questions | none |
| `report/workflow.md` | doc | Reproducer + tool versions + work estimate | none |
| `report/artifacts_summary.md` | doc | This file | none |
| `report/failure_analysis.md` | report | Honest critique of gaps & residual uncertainty | none |
| `extraction/nougat.mmd` | placeholder | Would-be Nougat parse; stub with PDF SHA-256 pointer | **low**: no GPU parse actually run; PDF text via pdftotext is sufficient |

## Trace / provenance summary
- All numerical claims trace back to `results/digitized_tables.json`, itself derived
  from Tables 1–3 of `source.pdf`. No hidden LLM-generated numbers.
- All fits reproducible via `code/digitize_from_tables.py` from `source.pdf` alone.
- Figures reproducible via `code/make_figures.py` from `results/digitized_tables.json`.
- Report backfill (this pass) added: `report/REPORT.tex`, `report/open_questions.json`,
  `report/open_questions_section.tex`, `report/workflow.md`, `report/artifacts_summary.md`,
  `report/failure_analysis.md`, `extraction/nougat.mmd`.

## Friction tags — legend
- **none** = fully reproducible from source
- **low** = missing but not blocking (e.g., Nougat parse skipped, pdftotext suffices)
- **medium** = qualitative reproduction; exact numeric match not possible without
  the raw underlying data
- **high** = would require author contact, paid resources, or wet-lab work

## Total artifacts on disk
~21 files across `code/`, `results/`, `figures/`, `report/`, `extraction/`, plus
top-level `source.pdf`, `source.txt`, `README.md`, `REPORT.md`, `PROGRESS.md`.
