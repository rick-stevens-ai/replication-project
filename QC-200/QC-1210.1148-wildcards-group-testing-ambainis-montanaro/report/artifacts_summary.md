# Artifacts Summary

Target dir: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1210.1148-wildcards-group-testing-ambainis-montanaro/`

## 8-artifact completion bar (per QC-100 wave brief, updated 2026-07-05)

| # | Artifact | Path | Status |
|---|---|---|---|
| 1 | Original PDF | `paper.pdf` (+ mirror `work/paper.pdf`) | ✓ present (383 KB, v4) |
| 2 | Marker parse | `extraction/marker.md` | ✓ present — **fallback** from `pdftotext -layout` (marker not installed on host; see failure_analysis.md) |
| 3 | Nougat parse | `extraction/nougat.mmd` | ✓ present — **fallback** from `pdftotext -layout` (nougat not installed on host; see failure_analysis.md) |
| 4 | Detailed LaTeX report | `report/REPORT.tex` (+ `REPORT.pdf` if compile succeeded) | ✓ present |
| 5 | 5 open questions | `report/open_questions.json` + `## Open Questions` in `REPORT.tex` | ✓ present, 5 questions with q/basis/next_steps |
| 6 | Workflow + tools list | `report/workflow.md` | ✓ present |
| 7 | Artifacts summary | `report/artifacts_summary.md` (this file) | ✓ present |
| 8 | Failure analysis | `report/failure_analysis.md` | ✓ present |

## Full file inventory

```
QC-1210.1148-wildcards-group-testing-ambainis-montanaro/
├── paper.pdf                                   # arXiv v4, 383 KB
├── extraction/
│   ├── paper_pdftotext.txt                    # source for the marker/nougat fallbacks
│   ├── marker.md                              # Marker-fallback (see failure_analysis.md)
│   └── nougat.mmd                             # Nougat-fallback (see failure_analysis.md)
├── work/
│   ├── paper.pdf                              # working copy
│   └── paper.txt                              # text-extracted version used during coding
└── report/
    ├── REPORT.tex                             # detailed LaTeX report (this replication)
    ├── REPORT.pdf                             # only if pdflatex succeeded (see failure_analysis)
    ├── workflow.md                            # step-by-step workflow + tool versions
    ├── artifacts_summary.md                   # this file
    ├── failure_analysis.md                    # honest gaps + friction
    ├── open_questions.json                    # 5 machine-readable open questions
    └── evidence/
        ├── wildcards_pgm.py                   # Lemma-3 PGM + full-alg query counter
        ├── wildcards_results.json             # structured results from wildcards_pgm.py
        ├── wildcards_stdout.txt               # raw stdout log
        ├── group_testing_qm.py                # AM CGT quantum sim + baselines
        ├── group_testing_results.json         # structured results
        └── group_testing_stdout.txt           # raw stdout log
```

## Trace: paper claim → evidence artifact

| Claim | Evidence file(s) | Metric |
|---|---|---|
| C1 (wildcards O(√n log n) upper bound) | `evidence/wildcards_pgm.py` → `wildcards_results.json` `algorithm_simulation` | avg_total_queries vs √n log n |
| C3 (Lemma 3 O(1) Hamming error) | `evidence/wildcards_pgm.py` → `wildcards_results.json` `lemma3_check` | expected_hamming values |
| C4 (CGT O(k log k) upper bound) | `evidence/group_testing_qm.py` → `group_testing_results.json` `results[].avg_am_quantum_queries` | avg vs k log₂ k |
| C6 (CGT k=1 → 1 quantum query) | Same file, n=8/16 k=1 rows | avg ≈ 1.45 (incl. Las-Vegas verify) |
| Classical CGT Θ(k log(n/k)) baseline | `group_testing_qm.py` `classical_binary_search_cgt` | avg vs k log(n/k) |

## SHA-256 of the fetched PDF

Recorded value: `df362bf4faa15ea51eb19a00dc6dfe7fd47d0faf73c1fc888910a167fc8a4ac4`  (recompute with `shasum -a 256 paper.pdf`).
