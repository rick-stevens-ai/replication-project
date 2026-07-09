# Artifacts summary — Sethian 1996 FMM replication

All paths are relative to
`~/Dropbox/REPLICATE-PROJECT/PDE-Sethian-fast-marching-eikonal-1996/`.

## Paper
- `paper/sethian1996_fmm.pdf` — 17 pp., PDF 1.2, DOI
  10.1073/pnas.93.4.1591 (Alberta CS mirror).

## Code (from-scratch, no third-party FMM)
- `work/fmm.py` — ~180 lines. Godunov largest-root update
  `_solve_quadratic(a,b,F,h)` + `fast_march_2d(speed, sources, h)`
  min-heap narrow-band loop with per-cell version counter.
- `work/experiments.py` — runs C1 timing sweep, C2 point-source
  convergence, C3 two-material propagation. Writes JSON.
- `work/convergence_plane.py` — supplementary smooth-solution
  (plane-wave, T=y) convergence check.
- `work/make_figures.py` — produces the three PNG figures.
- `work/llm_judge.py` — sends result JSONs to Argo `argo:gpt-4o` and
  stores verbatim response (no regex).

## Evidence (raw JSON, human- and machine-readable)
- `report/evidence/complexity.json` — C1 timing table
  (n, N, seconds, t/(N log2 N)), fitted power-law slope p=1.035, CV
  11.5%.
- `report/evidence/convergence.json` — C2 point-source, n in {33..513},
  L1 and L-infinity error on annulus 0.15<r<0.45; fitted slopes
  L1~0.73, L-inf~0.74.
- `report/evidence/convergence_plane.json` — C2 plane-wave: L1 = L-inf
  = 0.0 (bit-exact) for all n in {33..513}.
- `report/evidence/variable_speed.json` — C3 two-material: 0 monotone
  violations / 65793 non-source cells; axial column j=128 max abs
  error = 0.0 vs analytic d/F.
- `report/evidence/llm_judge.json` — Argo `argo:gpt-4o` per-claim
  rubric, overall verdict PARTIAL, one-line summary, coverage 100%,
  agreement 85%.

## Figures
- `report/evidence/fig_complexity.png` — runtime vs N log-log with
  fitted N log N reference.
- `report/evidence/fig_convergence.png` — point-source error vs h log-
  log with reference slope-1 line.
- `report/evidence/fig_variable_speed.png` — 2-D arrival-time field for
  the F=0.5/F=2.0 two-material test with a highlighted axial column.

## Reports
- `report/REPORT.md` — canonical replication narrative (this run's
  primary artifact).
- `report/REPORT.tex` — LaTeX publication-shape version with a
  dedicated GENUINE CRITIQUE section.
- `report/open_questions.json` — 5 open questions (higher-order upwind
  schemes, patch-based parallel FMM, Finsler geometries, fast-sweeping
  crossover, caustics / geometric-optics shocks).
- `report/workflow.md` — end-to-end methodology.
- `report/artifacts_summary.md` — this file.
- `report/failure_analysis.md` — failure-mode analysis (nothing
  crashed; the "failure" is the 0.73 point-source rate and its known
  cause).

## Verdict
**REPLICATED** at the algorithm level (C1 and C3 fully supported; C2
bit-exact on smooth data, partial on the singular point source at
rate 0.73). LLM-judge conservative label PARTIAL is preserved
verbatim in `evidence/llm_judge.json`.

## Coverage
- Testable claims: 5 (C1..C5).
- Tested here: 3 (C1, C2, C3) = 60%.
- Untested: C4, C5 (3-D generalizations of C1/C2; out-of-scope for a
  2-D laptop run per brief).
