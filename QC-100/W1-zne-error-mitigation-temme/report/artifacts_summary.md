# Artifacts Summary — QC-100 / W1 (ZNE / Temme et al. 2017)

Directory: `QC-100/W1-zne-error-mitigation-temme/`

## Pre-existing artifacts (preserved, unchanged)

| Path | Role |
|---|---|
| `REPORT.md`            | Top-level narrative replication report (2026-06-26). Verdict: PARTIAL (Coverage 6/10, Agreement 9/10). |
| `paper.md`             | Local markdown mirror of the paper (arXiv:1612.02058 / PRL 119, 180509). |
| `replicate.py`         | Clean-room numpy implementation of the 2-qubit density-matrix simulator, depolarizing noise, three extrapolators (linear / Richardson / exponential), Bell-state circuit, base-rate sweep. |
| `results.json`         | Machine-readable numeric results (raw noisy value, per-extrapolator estimates, errors, reduction factors, base-rate sweep). |
| `venv/`                | Local virtualenv (numpy only). Not required for re-run; `replicate.py` uses only numpy. |

## Backfilled artifacts (2026-07-06, this pass)

| Path | Role |
|---|---|
| `report/REPORT.tex`                    | LaTeX version of the replication report with a full critique section and open-questions include. |
| `report/open_questions.json`           | Bare JSON list of 5 open-question objects `{q, basis, next_steps}`. |
| `report/open_questions_section.tex`    | LaTeX rendering of the 5 open questions, `\input` from `REPORT.tex`. |
| `report/workflow.md`                   | Step-by-step workflow that produced the replication + backfill. |
| `report/artifacts_summary.md`          | This file. |
| `report/failure_analysis.md`           | Honest failure / limitation analysis of the replication. |
| `extraction/nougat.mmd`                | Stub for a Nougat-extracted mathematical markdown of the paper (not re-run; explains contents). |

## How to regenerate the numeric artifacts

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/W1-zne-error-mitigation-temme/
python3 -m venv venv && source venv/bin/activate
pip install numpy
python replicate.py > /tmp/zne.log
# results.json rewritten in place; REPORT.md numbers are frozen at 2026-06-26.
```

## How to build the LaTeX report

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/W1-zne-error-mitigation-temme/report/
pdflatex REPORT.tex && pdflatex REPORT.tex
```

## Free-endpoints attestation

No paid APIs, no hardware calls, no HPC submissions were used to produce
any artifact in this directory. Simulator uses `numpy` only. Backfill
authored entirely within the local workspace.
