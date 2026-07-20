# Artifacts summary — vedmedenko2008

| # | Artifact | Path | Description |
|---|----------|------|-------------|
| 1 | Extraction marker | `extraction/marker.md` | Provenance, headline claim, model summary, extraction confidence |
| 2 | Nougat interim | `extraction/nougat.mmd` | Header-normalized text-layer extraction (pdftotext -layout interim) |
| 3 | Report | `report/REPORT.tex` | Full replication write-up: model, method, results table, verdict |
| 4 | Open questions | `report/open_questions.json` | 5 Q's {question, why_it_matters, next_step} + next_steps list |
| 5 | Workflow | `report/workflow.md` | Step-by-step reproduction recipe |
| 6 | Artifacts summary | `report/artifacts_summary.md` | This file |
| 7 | Failure analysis | `report/failure_analysis.md` | Scope limits, discrepancies, honest caveats |
| 8 | Evidence | `report/evidence/` | Result JSON + code (physics + shared kernel) |

## Evidence contents
- `report/evidence/vedmedenko2008_result.json` — full diagnostics output
- `report/evidence/vedmedenko2008_penrose_multipole.py` — from-scratch physics
- `report/evidence/code/vedmedenko2008_penrose_multipole.py` — same (code dir)
- `report/evidence/code/ollie_multipolar_stevens_landau_kernel.py` — credited shared kernel
- `report/evidence/replication_recipe.json` — original recipe

## Key result
Odd-parity (dipole l=1, octopole l=3) rotors on a 151-site de Bruijn Penrose
patch: orientation peaks along n*pi/10 tiling directions; net magnetization
~0.05-0.08 (no ferro LRO); C(r) decays 0.55->0.04 (dipole) and 0.16->-0.03
(octopole) => short-range order; orientation structure factor barely above
random baseline (no orientational Bragg); frustration fraction 0.41 (dipole) /
0.83 (octopole) at high-coordination vertices. All 5 claim checks pass.

**Verdict: PARTIAL (qualitative REPLICATED). Coverage 7/10, Agreement 8/10.**
