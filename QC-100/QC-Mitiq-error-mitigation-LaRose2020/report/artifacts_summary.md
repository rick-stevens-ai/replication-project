# Artifacts summary — Mitiq (LaRose et al. 2020)

**Set:** QC-100 · **Dir:** `QC-Mitiq-error-mitigation-LaRose2020/` · **Verdict:** REPLICATED

## 8-artifact checklist

| # | Artifact | Path | Status |
|---|----------|------|--------|
| 1 | Primary report (Markdown) | `report/REPORT.md` | ✅ present (source of truth) |
| 2 | Primary report (LaTeX) | `report/REPORT.tex` | ✅ added in backfill |
| 3 | Open questions (JSON) | `report/open_questions.json` | ✅ added in backfill (5 items) |
| 4 | Open questions (LaTeX section) | `report/open_questions_section.tex` | ✅ added in backfill |
| 5 | Workflow description | `report/workflow.md` | ✅ added in backfill |
| 6 | Artifacts summary (this file) | `report/artifacts_summary.md` | ✅ added in backfill |
| 7 | Failure / critique analysis | `report/failure_analysis.md` | ✅ added in backfill |
| 8 | Extraction stub | `extraction/nougat.mmd` | ✅ added in backfill (stub) |

## Pre-existing supporting artifacts (preserved unchanged)

- `report/brief.md` — 1-paragraph summary
- `report/attempt_log.md` — chronological log
- `report/artifact_harvest.md` — pulled artifacts + checksums
- `report/results.json` — machine-readable results
- `report/evidence/` — raw JSON outputs, LLM-judge transcript, paper excerpt
- `work/rep_pec.py`, `work/rep_pec_multiseed.py`, `work/rep_zne.py`, `work/run_judge.py`
- `work/venv/` — Python 3.12 venv (mitiq 1.0.0, cirq 1.6.1)
- `work/paper_text.txt` — extracted paper text

## Headline-exercised evidence

- **Mitiq installed independently from PyPI** (mitiq 1.0.0 + cirq 1.6.1 in fresh venv).
- **Specific error-mitigation benchmark reproduced from paper** (Fig 5 toy circuit: `H;X;CNOT` under depolarizing p=0.1).
- **Quantitative match**: unmitigated 0.062222 vs paper 0.0622 (4 sig figs).
- **PEC primitive verified**: mean improvement 6.4× vs no-mitigation baseline, 10/10 seeds better.
- **ZNE primitive verified**: mean |err| reduction 1.77×, 20/20 RB circuits improved.
- **Baseline comparison explicit**: unmitigated numbers reported side-by-side with mitigated in every result table.
- **CDR primitive**: package presence only (not benchmarked — flagged as limitation in critique).

## Endpoints used
Free Argo proxy only (`localhost:44497`). No paid inference.
