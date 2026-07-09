# LUCID100 Score-Curve Ledger

Goal: drive paper replication scores toward **10/10 coverage** and **10/10 accuracy**, while measuring return on spend in tokens, CPU-hours, and GPU-hours.

## Score definitions

- **Coverage (1–10):** how much of the paper's replication-relevant content is reproduced.
  - Full PDF is a hard gate for master-level scoring.
  - No full PDF => triage/scaffold only; coverage capped low until acquired.
  - Supplements/data/code/raw tables may cap coverage if required by the paper.
- **Accuracy (1–10):** agreement of reproduced outputs with the paper for the covered subset.
  - Must be judged from report/output text under the rubric, not regex-only scoring.

## Iteration accounting

Each iteration should record:

- `iteration_id`
- `timestamp_utc`
- `scope`: all corpus / wave / slot(s)
- `action_type`: pdf_hunt, marker_ocr, supplement_hunt, code_port, rerun, judge_score, etc.
- `input_state`: prior score/readiness state
- `output_state`: new score/readiness state
- `coverage_before_mean`, `coverage_after_mean`, `coverage_delta`
- `accuracy_before_mean`, `accuracy_after_mean`, `accuracy_delta`
- `tokens_prompt`, `tokens_completion`, `tokens_total`
- `cpu_wall_hours`, `cpu_core_hours`
- `gpu_wall_hours`, `gpu_count`, `gpu_hours`
- `new_full_pdfs`, `new_marker_extractions`, `new_supplements`, `new_code_or_data_artifacts`
- `blockers_resolved`, `blockers_remaining`
- `notes`

## Efficiency metrics

Computed from the checkpoint table:

- coverage gain / 100k tokens
- accuracy gain / 100k tokens
- coverage gain / CPU-hour
- accuracy gain / CPU-hour
- coverage gain / GPU-hour
- accuracy gain / GPU-hour
- papers advanced per CPU/GPU-hour

## Important caveat

Historical first-pass LUCID work did not consistently meter tokens/CPU/GPU per slot. The score curve should be treated as **instrumented from this ledger forward**, with earlier work only roughly reconstructable from logs.
