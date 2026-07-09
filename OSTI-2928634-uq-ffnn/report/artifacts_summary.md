# Artifacts Summary

## Directory contents

```
OSTI-2928634-uq-ffnn/
├── paper.pdf                                      # Original OSTI PDF (27.5 MB)
├── extraction/                                    # Marker + Nougat placeholder (see note)
├── report/
│   ├── REPORT.md                                  # Full report
│   ├── REPORT.tex                                 # LaTeX section-by-section version
│   ├── brief.md                                   # 1-paragraph what/why + verdict
│   ├── attempt_log.md                             # Chronological narrative
│   ├── workflow.md                                # Workflow + tools/versions + effort
│   ├── artifact_harvest.md                        # External artifacts pulled
│   ├── artifacts_summary.md                       # This file
│   ├── failure_analysis.md                        # What didn't reproduce and why
│   ├── open_questions.json                        # 5 new open questions
│   └── evidence/
│       ├── replication_results.json               # Full quantitative results
│       ├── judge_verdict.json                     # LLM judge output
│       ├── run.log                                # L=1 + L=5 + L=20-first-try training log
│       ├── run_L20.log                            # L=20 Kaiming-init retraining log
│       ├── model_L1.pt                            # Trained MLP L=1
│       ├── model_L5.pt                            # Trained MLP L=5
│       ├── model_L20.pt                           # Trained MLP L=20 (Kaiming init)
│       ├── fig_pdf_beta0p1.png                    # Analytic vs MC PDF, small β
│       ├── fig_pdf_beta1p5.png                    # Analytic vs MC PDF, large β
│       ├── fig_corr_rmse_vs_beta.png              # Correlation RMSE vs β per depth
│       ├── fig_var_err_vs_beta.png                # Variance rel err vs β per depth
│       ├── fig_table2_bars.png                    # Table 2 head-to-head bar chart
│       └── fig_speedup.png                        # Analytic-vs-MC speedup
└── work/
    ├── replicate.py                               # Main replication driver
    ├── retrain_L20.py                             # L=20 Kaiming-init retraining
    ├── make_figures.py                            # Report figures
    └── judge.py                                   # LLM-judge call
```

## Extraction sub-directory note

The wave brief requires `extraction/marker.md` and `extraction/nougat.mmd`. Neither `marker` nor `nougat` is installed on cherryrd or uicgpu (checked with `which marker` / `which nougat` — both empty). This paper's text was extracted with `PyMuPDF` (`fitz`) directly, saved as `~/.openclaw/workspace/tmp-osti-2928634.txt` (82 KB) and copied into `extraction/pymupdf.txt`. This is a documented deviation from the ideal artifact set. A future run with marker/nougat installed would upgrade this to the standard artifacts.

## Key numerical evidence

- **Trained networks**: L=1 nRMSE 0.044, L=5 nRMSE 0.028, L=20 nRMSE 0.078 (see `run.log`, `run_L20.log`).
- **Analytic vs MC agreement**: `replication_results.json` → `per_layer/L=*/beta_experiments/beta=*/{mean_max_err, var_median_rel_err, corr_offdiag_rmse}`.
- **Table 2 comparison**: `replication_results.json` → `per_layer/L=5/beta_experiments/beta=1.5/{table2_corr_analytic, table2_corr_mc}` and `fig_table2_bars.png`.
- **Judge verdict**: `judge_verdict.json` (Argo GPT-5.2 fallback after Opus 4.7 502) → per-claim + overall + confidence.
