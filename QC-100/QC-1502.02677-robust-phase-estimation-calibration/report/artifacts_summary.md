# Artifacts summary — QC-100 / arXiv:1502.02677

Directory: `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1502.02677-robust-phase-estimation-calibration/`

## Layout

```
QC-1502.02677-robust-phase-estimation-calibration/
├── work/
│   ├── paper.pdf                  arXiv PDF (v3, 2015 + 2021 erratum)
│   ├── abs.html                   arXiv landing page snapshot
│   └── paper.txt                  pdftotext -layout extraction
├── extraction/
│   └── nougat.mmd                 stub placeholder (see notes below)
├── code/
│   ├── qiskit_verify.py           analytic vs Qiskit Statevector check
│   ├── rpe_sim.py                 RPE ladder + shot-noise baseline
│   └── plot_and_fit.py            log-log fit + figure
├── data/
│   ├── qiskit_verify.json         max diff 1.8e-14, verdict MATCH
│   ├── rpe_sweep.json             14 K-values × 500 trials
│   └── scaling_fit.json           fitted slopes: RPE -0.98, shot -0.50
├── figures/
│   └── precision_vs_N.png         log-log RMSE vs N (both methods + theory)
└── report/
    ├── REPORT.md                  original Markdown replication report
    ├── REPORT.tex                 full LaTeX report with honest Critique
    ├── open_questions.json        5 open questions (JSON list)
    ├── open_questions_section.tex LaTeX render of the same 5 questions
    ├── workflow.md                chronological workflow record
    ├── artifacts_summary.md       this file
    ├── failure_analysis.md        honest critique of what was NOT tested
    └── evidence/                  copies of data + figures + code (evidence bundle)
```

## Artifact inventory (8-artifact standard)

| # | Artifact | Path | Present | Notes |
|---|----------|------|---------|-------|
| 1 | Original report | `report/REPORT.md` | ✅ | Original 2026-07-03 verdict + evidence |
| 2 | LaTeX report | `report/REPORT.tex` | ✅ | Backfilled 2026-07-06; embeds honest Critique + open questions |
| 3 | Open questions (JSON) | `report/open_questions.json` | ✅ | Bare JSON list of 5 objects `{q, basis, next_steps}` |
| 4 | Open questions (LaTeX section) | `report/open_questions_section.tex` | ✅ | Input by `REPORT.tex`; identical content to JSON |
| 5 | Workflow record | `report/workflow.md` | ✅ | Chronological account, backfill notes |
| 6 | Artifacts summary | `report/artifacts_summary.md` | ✅ | This file |
| 7 | Failure analysis | `report/failure_analysis.md` | ✅ | Honest catalog of untested/weakly-tested claims |
| 8 | Nougat extraction | `extraction/nougat.mmd` | Stub | `work/paper.txt` from `pdftotext` is the operative extraction; Nougat not run for this clean-LaTeX quantum-computing PDF |

## Evidence pointers

- **Circuit correctness anchor:** `data/qiskit_verify.json` (max abs diff
  `1.8e-14` between analytic cos/sin identity and Qiskit
  `Statevector` for `k ∈ {1,2,...,256}`, `A = π/2 + 0.037`).
- **Headline scaling result:** `data/scaling_fit.json` — RPE slope
  **−0.98** (R² 0.997), shot-noise slope **−0.50** (R² 0.9997); both
  within tolerance of theoretical **−1.00** / **−0.50**.
- **Raw evidence:** `data/rpe_sweep.json` (14 generations × 500 trials,
  seed 20260703).
- **Figure:** `figures/precision_vs_N.png` (log-log RMSE vs N with
  theory reference lines).

## Compute footprint

- Single laptop CPU (macOS 25.3.0 on CherryRd), Python 3.14.6, no
  accelerator.
- End-to-end wall clock: **~5 seconds**.
- No paid endpoints used. No external service calls. Free-endpoint rule
  respected.

## Verdict

**REPLICATED** for the headline Heisenberg-scaling claim (C1–C3).
SPAM-robustness (C4), multi-parameter nesting (C5), and RB comparison
are scoped-out extensions (see `failure_analysis.md` and Open Questions
#2, #3, #4).
