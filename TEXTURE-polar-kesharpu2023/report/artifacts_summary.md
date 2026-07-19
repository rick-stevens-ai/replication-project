# Artifacts Summary — TEXTURE-polar-kesharpu2023 (arXiv:2305.13423)

Verdict: **replicated** (4/4 qualitative topological claims; partial on exact
phase-boundary values). Runtime ≈ 30 s, CPU-only.

## The 8 artifacts

| # | Artifact | Path | Status |
|---|----------|------|--------|
| 1 | Paper PDF | `paper.pdf` | present (pre-existing) |
| 2 | Text extraction | `extraction/marker.md` (4941 lines) | present (pre-existing) |
| 3 | Replication code | `code/kesharpu2023_replication.py` | written + run |
| 4 | Structured results | `work/results.json` | written (4 claims, all match) |
| 5 | Figure | `figs/chern_phase_diagram.png` | written (Chern phase diagram S=1, S=3) |
| 6 | Report | `report/REPORT.tex` + `report/REPORT.pdf` | written + compiled (3 pp.) |
| 7 | Open questions | `report/open_questions.json` | written (5 questions) |
| 8a | Workflow | `report/workflow.md` | written |
| 8b | Failure analysis | `report/failure_analysis.md` | written |
| 8c | Artifacts summary | `report/artifacts_summary.md` | this file |
| — | Method extract | `report/method_extract.md` | present (pre-existing) |
| — | Metadata | `META.json` | updated (status + verdict) |

## Claims and reproduced numbers

1. **Eq. (5), S=1: `c1 = sgn[sin(q2x)]`** — sign agreement **1.00** over the q2x
   scan; numeric Chern = −1 for q2x<0, +1 for q2x>0. **MATCH.**
2. **THE sign flip with modulation vector** — **1** Chern sign flip across
   q2x ∈ [−2.9, 2.9] at fixed S=1. **MATCH.**
3. **Azimuthal dominance / polar factor subdominant (Eq. 7)** — numeric Chern
   q1x-independent for S=1,2,3; analytic max|S·g2/2| = **0.689 < 1** in the
   well-defined lobe |S·q2x|<π. Reproduces the paper's conclusion that topology
   depends essentially only on q2x. **MATCH.**
4. **Haldane mass transition (Eq. 11)** — M scan gives
   `[0,0,1,1,1,0,0]`: |c|=1 for small |M|, c=0 for large |M|. **MATCH.**

## Method
Self-contained two-band honeycomb Bloch Hamiltonian with Haldane-type NNN complex
hopping (phase φ_n = S q2·b_n), Chern number via Fukui-Hatsugai-Suzuki plaquette
method. Independent numerical reproduction of the paper's analytic Eqs. (5),(7),(11).

## Scope / honesty
Reproduces topology + sign structure, not exact phase-boundary values (Eq. 10 gap
closing), because the OCR-fragmented weight factors (Eq. 2) were reconstructed and
the p(k')/ε Fourier corrections were set to zero per the paper's own
approximation. See `failure_analysis.md` and `open_questions.json`.
