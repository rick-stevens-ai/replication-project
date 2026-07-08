# Artifacts Summary — QC-2308.05237-qml-fraud-detection

Wave: **QC-100**. Verdict: **REPLICATED**. Backfilled: 2026-07-06.

## Directory layout

```
QC-2308.05237-qml-fraud-detection/
├── code/
│   └── replicate.py                       # 13 KB single-file replication script
├── data/
│   └── banksim_like_200.csv               # 200-row synthetic BankSim-like dataset
├── extraction/
│   └── nougat.mmd                         # OCR / structured-extract stub (see failure_analysis)
├── logs/
│   └── run1.log                           # stdout of the full replicate.py run
├── report/
│   ├── REPORT.md                          # canonical narrative report (preserved)
│   ├── REPORT.tex                         # LaTeX report with genuine critique
│   ├── artifacts_summary.md               # this file
│   ├── failure_analysis.md                # honest critique of what did NOT work
│   ├── open_questions.json                # 5 open questions (JSON list, machine-readable)
│   ├── open_questions_section.tex         # same 5 questions rendered as a LaTeX section
│   └── workflow.md                        # end-to-end reproduction workflow
├── results/
│   └── replication_results.json           # per-model per-featuremap metrics + VQC loss curve
└── work/
    ├── paper.pdf                          # arXiv 2308.05237v1
    └── paper.txt                          # pdftotext extract for grep
```

## 8-artifact standard checklist

| # | Artifact                          | Path                                     | Status |
|---|-----------------------------------|------------------------------------------|--------|
| 1 | Narrative report                  | `report/REPORT.md`                       | ✅ preserved |
| 2 | LaTeX report                      | `report/REPORT.tex`                      | ✅ new  |
| 3 | Open questions (JSON)             | `report/open_questions.json`             | ✅ new  |
| 4 | Open questions (LaTeX section)    | `report/open_questions_section.tex`      | ✅ new  |
| 5 | Workflow                          | `report/workflow.md`                     | ✅ new  |
| 6 | Artifacts summary                 | `report/artifacts_summary.md`            | ✅ new (this file) |
| 7 | Failure analysis                  | `report/failure_analysis.md`             | ✅ new  |
| 8 | Extraction stub                   | `extraction/nougat.mmd`                  | ✅ new stub |

## Evidence for the verdict

- **Headline reproduced.** QSVC + ZFeatureMap wins both the paper's 12-cell grid and
  our 6-cell grid. Paper F1 = 0.98 → ours 0.943, |Δ| = 0.037, inside ±0.10 tolerance.
- **Feature-map ordering reproduced exactly.** QSVC: Z ≫ ZZ ≈ Pauli, both in paper
  and here.
- **VQC loss ordering reproduced.** ZFeatureMap final loss 0.562 < ZZ 0.799, Pauli
  0.764 — matches Fig. 13.
- **Classical baselines added by us** show QSVC/Z is within 0.04 of LogReg/linear-SVC.
  Paper's C6 competitiveness claim survives in the weak reading only.

## Free-endpoint compliance
Zero paid API calls. Local Qiskit Aer only. No LLM inference. No Kaggle API.
