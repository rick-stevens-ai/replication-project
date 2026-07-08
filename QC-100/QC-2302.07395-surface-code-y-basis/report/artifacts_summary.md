# Artifacts Summary — QC-2302.07395 (Inplace Surface-Code Y Basis)

**Paper:** Craig Gidney, *"Inplace Access to the Surface Code Y Basis"*, arXiv:2302.07395v2 (2024).
**Wave:** QC-100 (2026-07-03).
**Verdict:** REPLICATED.

## Directory layout

```
QC-2302.07395-surface-code-y-basis/
├── scripts/
│   └── replicate.py                  # driver, ~230 lines, one file
├── report/
│   ├── REPORT.md                     # canonical prose report (this file's parent)
│   ├── REPORT.tex                    # LaTeX build with critique section
│   ├── open_questions.json           # 5 open questions (machine-readable)
│   ├── open_questions_section.tex    # 5 open questions (LaTeX \input)
│   ├── workflow.md                   # provenance + reproduction steps
│   ├── artifacts_summary.md          # this index
│   ├── failure_analysis.md           # honest critique of what could still be wrong
│   └── evidence/
│       ├── expA_cross_check.json     # X/Y/Z LER table vs paper
│       ├── expB_inplace_vs_braid.json # d=9 head-to-head
│       ├── expC_padding_sweep.json   # padding-round saturation at d=5
│       ├── expD_structure.json       # round-count/qubit-count structure
│       └── run_log.txt               # verbatim stdout of replicate.py
├── extraction/
│   └── nougat.mmd                    # stub / placeholder for OCR pass
└── work/                             # paper's own primary artifacts
    ├── paper.pdf                     # arXiv v2 PDF
    ├── stats.csv                     # Zenodo — paper's LER numbers
    └── circuits/                     # Zenodo — ~500 .stim files
```

## Artifact list (8-artifact standard)

| # | Artifact                          | Location                              | Purpose                                     |
|---|-----------------------------------|---------------------------------------|---------------------------------------------|
| 1 | REPORT.md                         | report/REPORT.md                      | Canonical prose report                      |
| 2 | REPORT.tex                        | report/REPORT.tex                     | LaTeX build with critique                   |
| 3 | open_questions.json               | report/open_questions.json            | 5 open questions, machine-readable          |
| 4 | open_questions_section.tex        | report/open_questions_section.tex     | 5 open questions, LaTeX                     |
| 5 | workflow.md                       | report/workflow.md                    | Provenance + repro steps                    |
| 6 | artifacts_summary.md              | report/artifacts_summary.md           | This index                                  |
| 7 | failure_analysis.md               | report/failure_analysis.md            | Honest critique of residual risks           |
| 8 | extraction/nougat.mmd             | extraction/nougat.mmd                 | OCR/mmd stub                                |

## Evidence bundle (already present, pre-backfill)

- **`report/evidence/expA_cross_check.json`** — LERs at `p=0.001` for
  `basis ∈ {X, Y, Z, Y_folded}`, `d ∈ {3, 5, 7}`; ratio to `stats.csv`.
- **`report/evidence/expB_inplace_vs_braid.json`** — LERs for
  `basis ∈ {Y, Y_braid}` at `d=9, rb=4, p=0.001`; both within 1σ of each other
  and of paper.
- **`report/evidence/expC_padding_sweep.json`** — Y LERs at `d=5, p=0.001`,
  `rb ∈ {0,1,2,3,4,6,8,10}`; saturation at `rb ≈ 2 = ⌊d/2⌋` reproduced.
- **`report/evidence/expD_structure.json`** — REPEAT-block multiplicities and
  qubit counts at `d ∈ {3, 5, 7, 9, 11, 13, 15}`; `⌊d/2⌋+2` round envelope
  and `2d²−1` qubit-count fingerprint verified.
- **`report/evidence/run_log.txt`** — full stdout of `replicate.py`.

## Verdict cross-check

- **verdict_preserved:** REPLICATED
- **Rationale:** all four headline-testable claim families (existence/decodability,
  round envelope, qubit footprint, inplace-matches-braid LER) reproduced on
  paper's own released circuits with an independent open-source decoder.
  Absolute LERs offset by the paper-predicted correlated-vs-MWPM decoder gap,
  offset identical across X/Y/Z bases (rules out Y-specific bug). Headline
  exercised: inplace Y-basis construction executed end-to-end at `d ∈ {3..9}`.
