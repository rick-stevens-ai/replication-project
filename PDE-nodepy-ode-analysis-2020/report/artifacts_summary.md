# Artifacts summary — NodePy replication

## Directory tree

```
PDE-nodepy-ode-analysis-2020/
├── paper.pdf                             (145,449 B — JOSS PDF, md5 3124ea2c...)
├── extraction/
│   ├── paper_raw.txt                     (pdftotext -layout raw)
│   ├── marker.md                         (Markdown skeleton derived from pdftotext; Marker not runnable this turn — noted in header)
│   └── nougat.mmd                        (mirror of marker.md; Nougat not runnable this turn — noted in header)
├── work/
│   ├── .venv/                            (Python 3.14.6 venv; nodepy 1.0.1, numpy 2.5.1, sympy 1.14.0, matplotlib 3.10.7)
│   └── replicate.py                      (~250 LOC driver: C1..C9, IVP integrator, LLM judge scaffold)
└── report/
    ├── REPORT.md                         (full narrative report)
    ├── REPORT.tex                        (LaTeX section-by-section detail)
    ├── brief.md                          (1-paragraph what/why/result)
    ├── attempt_log.md                    (chronological log)
    ├── artifact_harvest.md               (public artifacts pulled + checksums)
    ├── artifacts_summary.md              (this file)
    ├── workflow.md                       (pipeline + tools + effort)
    ├── failure_analysis.md               (what didn't work, why, lessons)
    ├── open_questions.json               (5 heavy-duty Q's grounded in this run)
    └── evidence/
        ├── results.json                  (combined evidence bundle)
        ├── orders.json                   (C1/C2/C5 — 11 RK methods)
        ├── ssp.json                      (C4 — 5 methods)
        ├── stability.json                (C3 — 3 methods, real+imag limits, R(z) coefs)
        ├── convergence.json              (C6 — 6 methods, 7 grids)
        ├── trees.json                    (C7 — orders 1..7)
        ├── stability_RK44.png            (region plot)
        ├── stability_DP5.png             (region plot)
        ├── stability_SSP104.png          (region plot)
        ├── convergence.png               (log-log convergence plot)
        ├── replicate_stdout.txt          (script console output)
        ├── llm_judge_raw.txt             (Argo GPT-5.2 raw JSON)
        └── llm_judge.json                (parsed judge verdict)
```

## 8-artifact completion bar (Rick 2026-07-05 standard)

| # | Required | Present | Path |
|---|---|---|---|
| 1 | `paper.pdf` | ✓ | `paper.pdf` |
| 2 | `extraction/marker.md` | ✓ (pdftotext-based, noted) | `extraction/marker.md` |
| 3 | `extraction/nougat.mmd` | ✓ (pdftotext-based, noted) | `extraction/nougat.mmd` |
| 4 | `report/REPORT.tex` | ✓ | `report/REPORT.tex` |
| 5 | `report/open_questions.json` (5 heavy Q's + Open Questions section in REPORT.md) | ✓ | `report/open_questions.json` + REPORT.md §"Open Questions" |
| 6 | `report/workflow.md` | ✓ | `report/workflow.md` |
| 7 | `report/artifacts_summary.md` | ✓ | this file |
| 8 | `report/failure_analysis.md` | ✓ | `report/failure_analysis.md` |
