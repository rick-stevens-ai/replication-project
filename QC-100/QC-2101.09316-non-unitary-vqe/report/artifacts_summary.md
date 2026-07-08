# Artifacts Summary — QC-2101.09316-non-unitary-vqe

**Wave:** QC-100
**Verdict:** REPLICATED
**Backfill date:** 2026-07-06

## Directory layout

```
QC-2101.09316-non-unitary-vqe/
├── work/
│   ├── paper.pdf                       # arXiv:2101.09316v1 source
│   └── paper.txt                       # text extraction
├── extraction/
│   └── nougat.mmd                      # Nougat/text extraction stub (backfill)
├── code/
│   └── nu_vqe_h2.py                    # full independent implementation
└── report/
    ├── REPORT.md                       # original Markdown report (pre-existing)
    ├── REPORT.tex                      # LaTeX version + critique (backfill)
    ├── open_questions.json             # 5 open questions, bare JSON list (backfill)
    ├── open_questions_section.tex      # LaTeX rendering, \input'd by REPORT.tex (backfill)
    ├── workflow.md                     # step-by-step pipeline (backfill)
    ├── artifacts_summary.md            # THIS FILE (backfill)
    ├── failure_analysis.md             # honest critique standalone (backfill)
    └── evidence/
        ├── results.json                # machine-readable results
        └── run.log                     # full stdout from the run
```

## Artifact inventory (8-artifact standard)

| # | Artifact | Path | Status |
|---|----------|------|--------|
| 1 | Paper (raw) | `work/paper.pdf`, `work/paper.txt` | ✅ pre-existing |
| 2 | Structured extraction | `extraction/nougat.mmd` | ✅ backfill stub |
| 3 | Independent code | `code/nu_vqe_h2.py` | ✅ pre-existing |
| 4 | Evidence (logs, JSON) | `report/evidence/{run.log,results.json}` | ✅ pre-existing |
| 5 | Markdown report | `report/REPORT.md` | ✅ pre-existing |
| 6 | LaTeX report + critique | `report/REPORT.tex` (+ `open_questions_section.tex`) | ✅ backfill |
| 7 | Open questions (JSON+TeX) | `report/open_questions.json`, `report/open_questions_section.tex` | ✅ backfill |
| 8 | Workflow / artifacts / failure docs | `report/{workflow.md,artifacts_summary.md,failure_analysis.md}` | ✅ backfill |

## Headline result (one line)
nu-VQE achieved 31.6×–33.7× lower energy error than standard VQE on
noisy density-matrix simulation at *identical* circuit depth for H2/STO-3G
—reproducing and slightly exceeding the paper's stated "~10×" claim
(Sec. V.B / Figs. 7–8).

## Endpoints / cost
Free-tier only. No paid endpoints. Numerical work: local CPU (Qiskit/Aer).
Any LLM assistance for prose: Argo free (argo:claude-opus-4.7/4.8).
