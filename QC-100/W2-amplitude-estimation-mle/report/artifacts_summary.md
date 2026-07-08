# Artifacts Summary — QC-100 W2 MLE-QAE

## Top-level (pre-existing, preserved by this backfill)
- `REPORT.md` — authoritative report, source-of-truth (Markdown). NOT moved.
- `replicate.py` — full NumPy driver (Bernoulli sim + coarse-then-refine MLE + CRB).
- `results.json` — 156 configurations: per-(schedule, M, a) RMSE, bias, CRB, mean(a_hat).
- `fig_scaling_a1_48.png` — Fig. 2 replication (three-slope log-log at a = 1/48).
- `run.log` — execution log.

## Added by this backfill (report/*.tex + companions)
- `report/REPORT.tex` — LaTeX form of REPORT.md, with honest Critique section
  and `\input{open_questions_section.tex}` at end.
- `report/open_questions.json` — BARE JSON list of 5 open-question objects
  (`q`, `basis`, `next_steps`). Validated with `json.load`.
- `report/open_questions_section.tex` — LaTeX version of the same 5 questions.
- `report/workflow.md` — replication workflow / provenance.
- `report/artifacts_summary.md` — this file.
- `report/failure_analysis.md` — honest critique / limitations of the replication.

## Added extraction stub
- `extraction/nougat.mmd` — placeholder: paper was not re-extracted (report was
  written directly from the primary source at replication time). Stub documents
  which sections would need extraction if this were ever redone from scratch.

## Coverage / Agreement (from REPORT.md, preserved)
- Coverage: 8/10 (algorithm + scaling covered; App. A QPE comparison + Sec. 4
  CNOT-count baselines out of scope).
- Agreement: 9/10 (classical / LIS slopes within ±0.02 of paper; EIS shallower
  by 0.084, attributed to finite-N_shot bias per paper's own caveat).

## Verdict
REPLICATED. Headline three-slope Fig. 2 result independently reproduced with
own implementation at the paper's own target amplitudes.
