# Artifacts Summary — QC-2206.12780

## Report layer
- `report/REPORT.md` — canonical narrative report (pre-existing, hand-authored).
- `report/REPORT.tex` — LaTeX build of REPORT.md with additional Critique section and Open Questions include.
- `report/open_questions.json` — 5 open questions with `basis` + `next_steps`, JSON list of 5 objects.
- `report/open_questions_section.tex` — LaTeX version of the same 5 questions, imported by REPORT.tex.
- `report/workflow.md` — step-by-step replication workflow (materials → env → scripts → analysis → verdict).
- `report/artifacts_summary.md` — this file.
- `report/failure_analysis.md` — honest critique of what is and isn't established.

## Evidence layer
- `report/evidence/threshold_sweep.json` — Experiment A raw results (baseline surface-code threshold sweep, d∈{3,5,7}, 8 p values).
- `report/evidence/summary.json` — threshold-crossing summary from Experiment A.
- `report/evidence/run.log` — Experiment A stdout.
- `report/evidence/pentagon_vs_chao.json` — Experiment B raw results, 36 rows across (family, d, p) with paper LER cross-references.
- `report/evidence/pentagon_run.log` — Experiment B stdout.

## Source & inputs
- `work/paper.pdf`, `work/paper.txt` — source paper from arXiv.
- `work/stats.csv` — paper's own raw Monte-Carlo statistics (Zenodo 6626417), 720 rows from correlated MWPM.
- `work/circuits/` — 720 paper Stim circuits (Zenodo 6626417), family × distance × error-rate grid.

## Code layer
- `code/replicate.py` — Experiment A: Stim built-in rotated_memory_x threshold sweep, uncorrelated MWPM.
- `code/replicate_pentagon.py` — Experiment B: head-to-head chao vs pentagonal_sharp vs honeycomb on paper's circuits.

## Extraction layer
- `extraction/nougat.mmd` — stub. Paper's native PDF+LaTeX was authoritative; Nougat extraction was skipped in original run. Stub records this decision.

## Environment
- Host: CherryRd (macOS).
- venv: `.venv/` with `stim 1.16.0 + pymatching 2.4.0 + numpy 2.5.0`.
- Wall time: ~50 s total for both experiments.

## What each artifact establishes
| Artifact | Establishes |
|---|---|
| REPORT.md / REPORT.tex | Verdict + narrative + claims table + head-to-head result |
| threshold_sweep.json | Baseline pipeline is well-calibrated (~1% MWPM threshold) |
| pentagon_vs_chao.json | 12/12 pentagon < chao ordering + cross-check with paper LER |
| stats.csv | Paper's ground-truth LER numbers (external reference) |
| circuits/ | Paper's own Stim circuit definitions (external reference, ensures ordering result is on identical circuits) |
| replicate*.py | Reproducibility contract — anyone can rerun and see the same numbers |
| open_questions* | Explicit gap list — what a follow-up should attack |
| failure_analysis.md | Honest boundaries of what was and wasn't verified |

## Reproduction cost
- Time: <10 minutes on laptop CPU.
- Compute: single-thread Python.
- Data download: ~few MB from Zenodo 6626417.
- Free endpoints only: no external LLM calls for numerical results.
