# Artifacts Summary — OSTI-3020618

## Files in target dir

```
OSTI-3020618-nnqs-nuclear/
├── paper.pdf                              5.6 MB (fetched via uicgpu proxy)
├── extraction/
│   ├── pdftotext.txt                      pdftotext -layout output
│   └── marker.md                          same content, marker-substitute label
├── report/
│   ├── REPORT.md                          Full replication report (Markdown)
│   ├── REPORT.pdf                         Same, PDF-rendered
│   ├── REPORT.tex                         Section-by-section LaTeX (per-claim status)
│   ├── brief.md                           1-paragraph what/why
│   ├── attempt_log.md                     Chronological log
│   ├── artifact_harvest.md                External artifacts pulled
│   ├── artifacts_summary.md               This file
│   ├── failure_analysis.md                What failed, why, how to avoid
│   ├── workflow.md                        Tools + steps + effort
│   ├── open_questions.json                5 heavy-duty new research questions
│   └── evidence/
│       ├── deuteron_results.json          Full sweep numeric results
│       ├── run.log                        Sweep stdout
│       └── llm_judge.txt                  LLM-judge verdict transcript
└── work/
    └── nnqs_deuteron.py                   Replication code (Python/PyTorch)
```

## Numerical evidence (highlight)

- **Exact benchmark (Yamaguchi-tuned):** E = −2.224608 MeV
- **NNQS best (N_hid=10, seed=1000):** E = −2.224088 MeV, ΔE = 0.52 keV, F_S = 0.99997
- **Reproduced claims:** C1 (MLP reaches keV precision), C3 (post-training σ < few keV).
- **Not attempted:** C2 (Table 4.1 pionless-EFT SJ for ²H/³H/⁴He — needs a 4-body VMC engine).

## 8-artifact completion bar (Rick 2026-07-05 standard) — checklist

| # | Artifact | Path | Status |
|---|---|---|---|
| 1 | paper.pdf | `paper.pdf` | ✅ |
| 2 | extraction/marker.md | `extraction/marker.md` | ✅ (pdftotext substitute, marker not available on uicgpu) |
| 3 | extraction/nougat.mmd | — | ⚠️ NOT AVAILABLE (no nougat env on uicgpu; not in cache) |
| 4 | report/REPORT.tex | `report/REPORT.tex` | ✅ |
| 5 | report/open_questions.json | `report/open_questions.json` | ✅ (5 heavy-duty items) |
| 6 | report/workflow.md | `report/workflow.md` | ✅ |
| 7 | report/artifacts_summary.md | this file | ✅ |
| 8 | report/failure_analysis.md | `report/failure_analysis.md` | ✅ |

7/8 hard artifacts present; nougat MMD listed as GAP with justification.
