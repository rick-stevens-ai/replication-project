# Artifacts Summary — LUCID slot 63

Backfilled 2026-07-06 to the LUCID 8-artifact standard. Original first-pass
material preserved unchanged.

## On-disk layout

```
lucid-friedrich-gldm-dsb-clustering-loops-slot63/
├── REPORT.md                          [ORIGINAL, top-level, preserved]
├── code/
│   ├── globle_static.py               [ORIGINAL — Eqs. 1–7 + Eqs. 12–13, 17-line dict]
│   └── make_figures.py                [ORIGINAL — driver script for Fig. 1–3]
├── figures/
│   ├── fig1_dose_response_RT112.png   [ORIGINAL — Claim 1]
│   ├── fig2_alpha_beta_anticorr.png   [ORIGINAL — Claim 2]
│   └── fig3_decomposition.png         [ORIGINAL — mechanistic decomposition]
├── extraction/
│   └── nougat.mmd                     [BACKFILL — stub, no PDF available]
└── report/
    ├── REPORT.tex                     [BACKFILL — LaTeX report]
    ├── open_questions.json            [BACKFILL — 5 open questions, machine-readable]
    ├── open_questions_section.tex     [BACKFILL — LaTeX version]
    ├── workflow.md                    [BACKFILL — step-by-step methodology]
    ├── artifacts_summary.md           [BACKFILL — this file]
    └── failure_analysis.md            [BACKFILL — honest critique]
```

## Artifact status table

| # | Artifact | Origin | Status |
|---|---|---|---|
| 1 | REPORT.md (top-level) | First pass | Present, preserved |
| 2 | report/REPORT.tex | Backfill 2026-07-06 | Added |
| 3 | report/open_questions.json | Backfill 2026-07-06 | Added (5 items) |
| 4 | report/open_questions_section.tex | Backfill 2026-07-06 | Added |
| 5 | report/workflow.md | Backfill 2026-07-06 | Added |
| 6 | report/artifacts_summary.md | Backfill 2026-07-06 | Added (this file) |
| 7 | report/failure_analysis.md | Backfill 2026-07-06 | Added |
| 8 | extraction/nougat.mmd | Backfill 2026-07-06 | Stub (PDF closed-access, no extraction possible) |

Extras beyond the 8-artifact minimum: `code/` (2 files) and `figures/`
(3 PNGs) from the first pass.

## Verdict

**PARTIAL** — preserved from the first-pass self-verdict and the 2026-06-20
3-judge external audit. See `failure_analysis.md` for the honest critique
of why this is PARTIAL rather than REPLICATED, and `open_questions.json`
for the five concrete probes that would either strengthen it toward
REPLICATED (Q1: full PIDE 150-line refit) or extend it usefully (Q2–Q5).

## Reproducibility

- No paid endpoints, no HPC, no GPU.
- Total wall-clock < 5 s.
- `python code/make_figures.py` re-produces all figures and numerics on
  any laptop with numpy + matplotlib + scipy.
