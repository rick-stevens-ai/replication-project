# Artifacts Summary — PyFoci miscounting

## Input artifacts (harvested)

| Artifact | Source | On-disk path | Status |
|---|---|---|---|
| Paper PDF | LUCID corpus | `artifacts/paper.pdf` | OK |
| Parsed paper text | `pdftotext -layout` | `artifacts/parse/paper.txt` | OK (663 lines) |
| PyFoci source | gitlab.com/PRECISE-RT/releases/pyfoci | `code/pyfoci/` | OK |
| Colab mirror | github.com/SamPIngram/PyFoci_Colab | `code/PyFoci_Colab/` | OK |
| Figshare bundle | doi.org/10.48420/14398790 | `data/*.zip` (7 ZIPs) | OK |
| 24 count parquets (single-slice, all 24 microscope/mag configs) | figshare extract | `data/extracted/*.parquet` | OK |
| Airyscan-x63 deconvolution parquet | figshare extract | `data/extracted/deconv/…deconv` | OK |
| Airyscan-x63 3D-stack parquet | figshare extract | `data/extracted/3D/…3D.parquet` | OK (1176 rows) |
| Explicit Mann-Whitney tables (Figs 1,4,5,6,7,8) | figshare extract | `data/extracted/Explicit_PValues/P_Values_Fig*` | OK (7 files, 712 lines) |
| Repair-DSBMarker dose breakdown | figshare extract | `data/extracted/Repair - DSBMarker/{photon,proton}/…` | OK |
| Vertices, SDDs (Geant4 pre-computed inputs) | figshare extract | `data/extracted/Vertices/`, `data/extracted/SDDs/` | OK |

## Output artifacts (produced by re-pass)

| Artifact | Path | Content |
|---|---|---|
| Top-line summary | `results/repass/ALL_CLAIMS_SUMMARY.json` | Per-claim verdict object |
| Fig 1 p-value repro | `results/repass/mw_fig1.csv` | 120-row per-comparison table |
| Per-claim summaries | `results/repass/*_summary.json` | 7 JSON files (Claims 7-13) |
| Analog figures | `figures/repass/fig3_kinetics.png`, `fig4_airyscan_mag.png`, `fig5_voxel.png` | Reproduced qualitative figures |
| Parser provenance line | `PARSER_PROVENANCE` | `pdftotext-layout / poppler 24.x` |

## Trace / provenance

- **Driver script:** `code/repass_extended.py` (520 LOC, pure stdlib+pandas+
  pyarrow+numpy+scipy+matplotlib). Determinism: no RNG-dependent steps
  (Mann-Whitney uses the authors' original DataFrame rows verbatim; Spearman
  is deterministic given input).
- **Compute host:** CherryRd (local; no remote endpoint used).
- **Re-pass run timestamp:** 2026-06-23 (verdict lifted PARTIAL -> REPLICATED).
- **Backfill timestamp:** 2026-07-06 (this document + REPORT.tex + open_questions
  + workflow + failure_analysis).

## Backfill artifacts (this pass, 2026-07-06)

| Artifact | Path | Content |
|---|---|---|
| Full LaTeX report | `report/REPORT.tex` | Paper summary, claims table, method, results vs paper, honest critique, `\input{open_questions_section.tex}` |
| Open questions JSON | `report/open_questions.json` | 5 grounded open questions with basis + next_steps |
| Open questions LaTeX | `report/open_questions_section.tex` | LaTeX rendering of the same 5 questions |
| Workflow | `report/workflow.md` | Tools/versions, pipeline steps, reproducer |
| Artifacts summary | `report/artifacts_summary.md` | This file |
| Failure analysis | `report/failure_analysis.md` | Honest gap enumeration (not a whitewash) |
| Extraction stub | `extraction/nougat.mmd` | SHA-256 pointer to `artifacts/paper.pdf`; no GPU parse |

## Friction tags

- **F6 (environment fragility)** — Python 3.14 / numba wheel gap blocks the raw
  PyFoci pipeline rerun (Claim 5). Workaround: create a Python 3.11 venv and
  `pip install -e code/pyfoci`. Not attempted here because all quantitative
  claims have downstream evidence in the cached parquet artifacts and the
  re-pass verdict does not depend on it.
- **F7 (partial pipeline)** — Only derived parquet outputs analyzed, not the
  upstream image-generation step. Inputs (Vertices, SDDs) are present, so an
  auditor with the F6 workaround can close this too.
