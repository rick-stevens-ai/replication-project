# Artifacts Summary — s100-072 (Analytical track-structure formulas)

Paper: Kundrát et al., Sci. Rep. 10:15775 (2020). DOI 10.1038/s41598-020-72857-z.

## Directory tree

```
s100-072-analytical-track-structure-formulas/
├── source/
│   └── paper.pdf                          # input PDF, 1.16 MB, 11 pages, CC-BY 4.0
├── ocr/
│   └── paper.txt                          # pdftotext extraction, 836 lines
├── extraction/
│   └── nougat.mmd                         # stub (not required; pdftotext+tesseract sufficed)
├── code/
│   ├── reproduce.py                       # ~16 KB; Eq. (1)+(2) + 540 fit params + plot logic
│   └── __pycache__/                       # auto (bytecode)
├── figures/
│   ├── fig1_SB.png                        # reproduction of paper Fig. 1 (27 curves)
│   ├── fig2_SSB.png                       # reproduction of paper Fig. 2 (27 curves)
│   ├── fig3_DSB.png                       # reproduction of paper Fig. 3 (27 curves)
│   ├── fig4_DSBclusters.png               # reproduction of paper Fig. 4 (27 curves)
│   └── fig5_DSBsites.png                  # reproduction of paper Fig. 5 (27 curves)
├── evidence/
│   ├── console.log                        # full run stdout + acceptance-probe pass/fail
│   ├── run_log.txt                        # sampled yields per ion at probe LETs
│   └── yield_samples.tsv                  # 135 rows × 10 LET points
└── report/
    ├── REPORT.md                          # original prose report
    ├── REPORT.tex                         # LaTeX version + formal critique section
    ├── open_questions.json                # 5 questions {q, basis, next_steps}
    ├── open_questions_section.tex         # LaTeX-formatted open questions
    ├── workflow.md                        # stage-by-stage execution log
    ├── artifacts_summary.md               # this file
    └── failure_analysis.md                # honest what-did-NOT-happen critique
```

## Artifact provenance

| Artifact | Origin | Provenance |
| --- | --- | --- |
| `source/paper.pdf`         | Nature/Springer CC-BY 4.0 download           | Pre-staged, unmodified |
| `ocr/paper.txt`            | `pdftotext -layout`                          | Deterministic |
| `extraction/nougat.mmd`    | Stub                                         | Not required (see file) |
| `code/reproduce.py`        | Human-authored from paper Eqs. + Tables      | 540 params transcribed |
| `figures/fig{1..5}_*.png`  | `matplotlib` output of `code/reproduce.py`   | Regenerable, deterministic |
| `evidence/console.log`     | Captured stdout of reproduction run          | Regenerable |
| `evidence/run_log.txt`     | Additional log written by `reproduce.py`     | Regenerable |
| `evidence/yield_samples.tsv` | TSV written by `reproduce.py`              | 135 rows × 10 LET grid |
| `report/REPORT.md`         | Human-authored                               | Prose replicator report |
| `report/REPORT.tex`        | Backfill 2026-07-06                          | LaTeX version + critique |
| `report/open_questions.*`  | Backfill 2026-07-06                          | Grounded in paper re-read |
| `report/workflow.md`       | Backfill 2026-07-06                          | Stage-by-stage recap |
| `report/artifacts_summary.md` | Backfill 2026-07-06                       | This file |
| `report/failure_analysis.md`  | Backfill 2026-07-06                       | Honest limitations |

## Reproducibility

Full reproduction: `cd code && python3 reproduce.py`. Requires: Python 3, numpy, matplotlib. No GPU, no MC engine, no proprietary software. Runtime: ~5 seconds on CPU.

## What is NOT included (documented gaps)

- No PARTRAC re-run (PARTRAC is proprietary, Helmholtz Munich; not publicly released).
- No independent MC cross-check (Geant4-DNA / TRAX / KURBUC). Would require multi-week study on `uicgpu`; out of scope for a paper whose deliverable is closed-form formulas.
- No PARTRAC MC datapoints in Figs. 1–5 (only fitted curves; underlying MC output not published in the paper).
- No experimental cross-check against measured DSB yields (γ-H2AX, PFGE).
- No downstream survival-model mapping (LEM/MKM/RMF) — see open_questions Q4.
- No chromatin-heterogeneity extension (target is fixed to PARTRAC G0/G1 spherical lymphocyte) — see open_questions Q3.
