# Artifacts summary — QC-quant-ph-0603140

## Directory tree
```
QC-quant-ph-0603140-grover-hidden-subgroup/
├── paper.pdf                          # (1) source PDF, copy of work/0603140.pdf
├── extraction/
│   ├── marker.md                      # (2) pdftotext-flow fallback (Marker unavailable)
│   └── nougat.mmd                     # (3) pdftotext-layout fallback (Nougat unavailable)
├── code/
│   └── grover_hsp.py                  # Parts A–F end-to-end (~450 LOC)
├── work/
│   ├── 0603140.pdf                    # fetched from arxiv
│   ├── 0603140.txt                    # pdftotext -layout dump
│   └── 0603140_flow.txt               # pdftotext (no -layout) dump
├── figures/                           # (reserved; no per-figure outputs required)
└── report/
    ├── REPORT.tex                     # (4) detailed LaTeX report
    ├── open_questions.json            # (5) 5 heavy-duty open questions
    ├── open_questions_tex.tex         # Q1–Q5 formatted for REPORT.tex \input
    ├── workflow.md                    # (6) workflow + tools + effort
    ├── artifacts_summary.md           # (7) THIS file
    ├── failure_analysis.md            # (8) honest failure analysis
    └── evidence/
        └── results.json               # full numeric results, all Parts A–F
```

## Artifact inventory (with sizes / origins)

| # | Path                              | Origin / how produced                     | Notes |
|---|-----------------------------------|-------------------------------------------|-------|
| 1 | `paper.pdf`                       | `curl https://arxiv.org/pdf/quant-ph/0603140` | 185 KB |
| 2 | `extraction/marker.md`            | pdftotext (no -layout) + header note      | ~27 KB, fallback |
| 3 | `extraction/nougat.mmd`           | pdftotext -layout + header note           | ~37 KB, fallback |
| 4 | `report/REPORT.tex`               | authored                                  | detailed |
| 5 | `report/open_questions.json`      | authored                                  | 5 items, {q,basis,next_steps} |
| 6 | `report/workflow.md`              | authored                                  |  |
| 7 | `report/artifacts_summary.md`     | authored                                  |  |
| 8 | `report/failure_analysis.md`      | authored                                  |  |
|   | `code/grover_hsp.py`              | authored                                  | ~450 LOC |
|   | `report/evidence/results.json`    | `python code/grover_hsp.py`               | ~30 KB, numeric truth data |
|   | `work/0603140.pdf`                | curl                                      | source, keep |
|   | `work/0603140.txt`                | pdftotext -layout                         | reading aid |
|   | `work/0603140_flow.txt`           | pdftotext                                 | for marker.md |

## Traces (logs / run records / evidence)

- `report/evidence/results.json` — full nested dict, one top-level key per part:
  - `partA_standard_grover` — full k-curve for N=4,8,16, including
    `p_marked_sim`, `p_formula`, and per-k `abs_err`.
  - `partB_invariance_under_stab` — 20 stab + 20 non-stab fidelities per N.
  - `partC_coset_structure_Prop1` — disjointness / completeness booleans for
    N=3,4,5 with different j_0 choices.
  - `partD_section9_however` — per-normal-subgroup intersection sizes, plus
    per-(i,j) conjugacy checks.
  - `partE_qhs_indistinguishability` — induced-rep dimensions + textual
    conclusion.
  - `partF_pushed_oracle_equivalence` — j-by-j table of pushed-oracle vs
    Grover-oracle.

## External resources used

- arXiv preprint `quant-ph/0603140` (source paper, fetched 2026-07-05)
- No external datasets, no compute allocations, no LLM API calls.
