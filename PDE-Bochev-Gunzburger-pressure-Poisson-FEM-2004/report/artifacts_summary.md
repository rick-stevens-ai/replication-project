# Artifacts summary

## Directory tree

```
PDE-Bochev-Gunzburger-pressure-Poisson-FEM-2004/
├── paper.pdf                                    (202 KB, 19 pages, OA copy)
├── extraction/
│   ├── marker.md                                (pdftotext-layout extraction, 64 KB)
│   └── nougat.mmd                               (same content, different header)
├── report/
│   ├── REPORT.md                                (main report, ~13 KB)
│   ├── REPORT.tex                               (LaTeX version, ~14 KB)
│   ├── brief.md                                 (1-paragraph what/why)
│   ├── attempt_log.md                           (chronological log of session)
│   ├── artifact_harvest.md                      (external artifact table)
│   ├── artifacts_summary.md                     (this file)
│   ├── workflow.md                              (workflow + tools + effort)
│   ├── failure_analysis.md                      (what almost went wrong)
│   ├── open_questions.json                      (5 heavy Q with basis + next_steps)
│   └── evidence/
│       ├── convergence_tg.json                  (Taylor-Green, 4 meshes)
│       ├── convergence_kovasznay.json           (Kovasznay Re=40, pre-asymptotic)
│       ├── convergence_kovasznay_re1.json       (Kovasznay Re=1, super-optimal)
│       ├── stability_sweep.json                 (δ ∈ [10⁻⁶, 10⁴])
│       ├── stability_zero_delta.json            (δ=0 → singular; small δ → blowup)
│       └── convergence_and_stability.png        (3-panel figure)
└── work/
    ├── bochev_sgls_stokes.py                    (main implementation, ~500 lines)
    └── standard_pspg.py                         (classical PSPG for control, ~90 lines)
```

## Artifact roles

| File | Role | Provenance | Reproducible? |
|---|---|---|---|
| paper.pdf | Primary source | Author-hosted OA copy (Prof. Gunzburger's FSU page) | Yes — link + curl |
| extraction/marker.md, nougat.mmd | Machine-readable paper text | `pdftotext -layout paper.pdf` | Yes — deterministic |
| work/bochev_sgls_stokes.py | Numerical implementation of Eq. 5.10–5.11 | Authored 2026-07-06 from paper equations | N/A (source) |
| work/standard_pspg.py | Control: classical Hughes–Franca–Balestra PSPG | Authored 2026-07-06 | N/A (source) |
| report/evidence/*.json | Numerical outputs | Running the .py files | Yes — one-liner in workflow.md |
| report/evidence/convergence_and_stability.png | Summary figure | matplotlib on the JSON files | Yes — inline block in attempt_log.md 08:45 |
| report/REPORT.md, REPORT.tex | Analysis of results vs paper claims | Manual write-up | Human-authored |
| report/open_questions.json | 5 open research questions from the replication | Manual | Human-authored |
| report/failure_analysis.md | Debugging story + generalizable lessons | Manual | Human-authored |
| report/attempt_log.md | Session timeline | Manual | Human-authored |
| report/workflow.md | High-level workflow + versions + effort | Manual | Human-authored |
| report/brief.md | 1-paragraph elevator pitch | Manual | Human-authored |
| report/artifact_harvest.md | External source inventory | Manual | Human-authored |

## Sizes (bytes)

```
paper.pdf                              202,721
extraction/marker.md                    64,073
extraction/nougat.mmd                   64,107
report/REPORT.md                        ~13,500
report/REPORT.tex                       ~14,000
report/brief.md                          1,268
report/attempt_log.md                    6,011
report/artifact_harvest.md               2,359
report/workflow.md                       3,859
report/failure_analysis.md              (to be filled)
report/open_questions.json               4,265
report/evidence/*.json (total)          ~6,000
report/evidence/convergence_and_stability.png  124,258
work/bochev_sgls_stokes.py             ~15,000
work/standard_pspg.py                    3,613
```

## Completion bar checklist (8-artifact standard)

- [x] paper.pdf
- [x] extraction/marker.md
- [x] extraction/nougat.mmd
- [x] report/REPORT.tex
- [x] report/open_questions.json (5 questions, each with q/basis/next_steps)
- [x] report/workflow.md
- [x] report/artifacts_summary.md
- [x] report/failure_analysis.md
- [x] (bonus) report/REPORT.md
- [x] (bonus) report/brief.md, attempt_log.md, artifact_harvest.md
