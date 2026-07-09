# Workflow — GLOBLE photon cell-killing replication

Paper: Herr, Friedrich, Durante & Scholz, *A Model of Photon Cell Killing Based on
the Spatio-Temporal Clustering of DNA Damage in Higher Order Chromatin Structures*,
PLoS ONE 9(1):e83923 (2014). DOI 10.1371/journal.pone.0083923.

## Chronology
- **2026-05-29** — pass 1: paper.md extraction cached; GLOBLE ODE implemented in
  `code/globle.py`; Figs 2–6 reproduced for RT112 + MT; GLOBLE/LQ Lea–Catcheside
  equivalence (Fig 4), LL split-dose plateau (Fig 6), dose-rate deterministic
  effect (Fig 5). Report: `REPORT.pass1.md`.
- **2026-06-09 / 06-23** — re-pass: `code/repass/repass_globle.py` adds six claim
  batches A–F, extending coverage to all 17 Table-2 cell lines, both Table-3
  columns, high/low dose-rate analytical limits, Eq.(8) identity, and paper text
  statistics. Report: `REPORT.md`. Parser provenance recorded in
  `PARSER_PROVENANCE.md`.
- **2026-07-06** — 8-artifact backfill (this pass): wrote `report/REPORT.tex`,
  `report/open_questions.json` (+ `open_questions_section.tex`), `report/workflow.md`,
  `report/artifacts_summary.md`, `report/failure_analysis.md`, and
  `extraction/nougat.mmd` stub. **No sims re-run** — items synthesized from the
  existing rich REPORT.md + on-disk results/figures + paper re-read. Backfill
  performed directly in the parent session after two subagent attempts timed out on
  the write-flush step.

## Tools / versions
- Python 3.11; NumPy, SciPy (`solve_ivp` / stiff ODE integration), Matplotlib.
- Source text: `paper.md` (Marker/Nougat-style extraction, sha `cb54cfea…`),
  cross-checked with `pdftotext -layout artifacts/paper.pdf` (Tables 2 & 3 and all
  numeric values agree between parses).
- LLM inference (verdict cross-checks in the wider programme): Argo proxy
  (localhost:44497, key=stevens), free endpoints only.

## Reproducer
```
cd code && python globle.py          # pass-1 figures
cd repass && python repass_globle.py # claims A–F, writes results/repass/*.json
```

## Repo layout
- `code/globle.py`, `code/cell_lines.py` — ODE + Table-2 parameters (17 lines / 22 sets)
- `code/repass/repass_globle.py` — re-pass driver (claims A–F)
- `results/`, `results/repass/` — JSON evidence per claim
- `figures/`, `figures/repass/` — reproduced figures (dose-rate + split-dose grids)
- `artifacts/paper.pdf` (md5 4b7d8f78…), `paper.md`, `PARSER_PROVENANCE.md`

## Work estimate
~2 person-days over pass-1 + re-pass (ODE implementation, 22-parameter-set
transcription, six claim batches, figure generation), plus ~0.5 h backfill.
No HPC/GPU used — all runs are small CPU ODE integrations.
