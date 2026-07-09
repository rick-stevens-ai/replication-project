# Workflow — Sethian 1996 FMM replication

Date: 2026-07-04.
Host: CherryRd (macOS, local CPU, Python 3, NumPy).
Compute cost: negligible (~14 s total across all C1/C2/C3 runs at
n=1025).
No GPU, no HPC.

## 0. Fetch paper
- Downloaded PDF from Alberta CS course mirror
  (`http://ugweb.cs.ualberta.ca/~vis/courses/CompVis/readings/modelrec/sethian95fastlev.pdf`),
  canonical DOI `10.1073/pnas.93.4.1591`. 17 pp., PDF 1.2. Placed under
  `paper/`.

## 1. Extract claims (paper → JSON)
- Read the paper end-to-end.
- Recorded 5 claims (C1..C5), marked which are testable in 2-D on a
  laptop under a short time budget: C1, C2, C3 in-scope; C4, C5
  (3-D generalizations) out-of-scope per brief.

## 2. Implement from scratch
- No third-party FMM code was consulted or downloaded.
- `work/fmm.py` (~180 lines) implements:
  - `_solve_quadratic(a, b, F, h)`: Godunov largest-root selection with
    one-axis fallback when the two-axis discriminant is negative
    (i.e. `T = min_axis + h/F`).
  - `fast_march_2d(speed, sources, h)`: min-heap narrow-band loop with
    per-cell version counter (lazy deletion; equivalent to
    back-pointered heap up to a constant factor).
- `work/experiments.py`: runs C1 (timing), C2 (point-source
  convergence), C3 (two-material propagation) and writes JSON to
  `report/evidence/`.
- `work/convergence_plane.py`: supplementary smooth-solution
  (plane-wave) convergence test.
- `work/make_figures.py`: produces the three PNG figures.
- `work/llm_judge.py`: submits all JSON results to Argo `argo:gpt-4o`
  (127.0.0.1:44497, free) and stores the response verbatim.

## 3. Run experiments
```
cd work/
python3 experiments.py         # C1 timing sweep, C2 point-source, C3 two-material
python3 convergence_plane.py   # C2 smooth-data supplementary
python3 make_figures.py        # writes report/evidence/fig_*.png
python3 llm_judge.py           # writes report/evidence/llm_judge.json
```

Grids used:
- C1 timing: `n in {65, 129, 257, 513, 1025}`, median of 3 timed runs
  after a warm-up.
- C2 point-source: `n in {33, 65, 129, 257, 513}`, F=1, source at
  center, error on annulus 0.15 < r < 0.45 (avoid source singularity
  and boundary).
- C2 plane-wave: same n set, F=1, initial data on entire y=0 line,
  exact T = y, error in the interior column band.
- C3 two-material: n=257, F=0.5 (bottom) / F=2.0 (top), source at
  (128, 128) on the interface.

## 4. Score
- LLM judge (Argo `argo:gpt-4o`) returns per-claim rubric + overall
  verdict + coverage% + agreement% as JSON. No regex parsing.
- Human verdict re-derived from the raw evidence in
  `report/evidence/*.json` and reconciled with the judge in §6 of
  `REPORT.md`.

## 5. Write report
- `report/REPORT.md`: full narrative, tables, verdict, judge quote.
- `report/REPORT.tex`: publication-shape LaTeX version with a
  dedicated genuine-critique section.
- `report/open_questions.json`: 5 open questions grounded in the
  paper's scope limits (higher-order upwind, parallel FMM, Finsler,
  fast sweeping crossover, caustics).
- `report/artifacts_summary.md`, `report/failure_analysis.md`,
  `report/workflow.md` (this file).

## Provenance guarantees
- Implementation is from-scratch; no third-party FMM code.
- LLM judge output stored verbatim; no regex verdict extraction.
- All raw numbers reported in `REPORT.md` come from
  `report/evidence/*.json`; no numbers were hand-edited.
