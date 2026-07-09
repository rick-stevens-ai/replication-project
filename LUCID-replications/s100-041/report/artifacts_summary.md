# Artifacts summary — s100-041

## Paper source
- `source/paper.pdf` — 2.2 MB, 11 pp, pdfTeX 1.40.21 / LaTeX. Abolfath R, Grosshans D, Mohan R. Med. Phys. 47(12), Dec 2020. arXiv:2010.00744v1. DOI 10.1002/mp.14548.

## Text extraction
- `ocr/paper.txt` — 729 lines. Produced by `pdftotext -layout` (no true OCR required; PDF has native text).
- `extraction/nougat.mmd` — stub only. Not run because pdftotext extraction was already clean; nougat would add zero value on a text-embedded PDF.

## Reproduction code
- `code/repro_eq12.py` — numerical integration of Eqs 1–2 with `scipy.integrate.solve_ivp(method='Radau')`. Reproduces Figs 6 and 7 using the paper's pulse parameters (G1=100, τ1=0.01 s FLASH; G2=0.01, τ2=100 s CDR).
- `code/verify_scaling.py` — log-log slope fits over four decades in t at constant G ∈ {1, 100}. Verifies Eqs 7 (slope 1), 8 (slope 3), 9 (slope 1/3).

## Evidence (numerical outputs)
- `evidence/repro_results.txt` — measured N1(FLASH) peak, N1(CDR) peak, N1 and N2 values at t=100 s, ratio N2(FLASH)/N2(CDR) = 1.70.
- `evidence/scaling_exponents.txt` — fitted slopes: 1.0000 (Eq 7), 3.0000 (Eq 8), 0.342 (Eq 9).

## Figures (regenerated from equations)
- `figures/fig6_repro_N1.png` — N1(t) FLASH vs CDR, showing high FLASH peak and long-time CDR dominance.
- `figures/fig7_repro_N2.png` — N2(t) FLASH vs CDR, showing FLASH ≈ 2× CDR at long times.

## Report bundle
- `report/REPORT.md` — original refined markdown, source of truth for numeric claims.
- `report/REPORT.tex` — LaTeX version with honest critique and downgraded verdict.
- `report/open_questions.json` — 5 open questions (bare JSON list; keys q, basis, next_steps).
- `report/open_questions_section.tex` — LaTeX rendering of Q1–Q5, \input'd by REPORT.tex.
- `report/workflow.md` — step-by-step methodology + what was intentionally left out.
- `report/artifacts_summary.md` — this file.
- `report/failure_analysis.md` — honest queue-vs-substance mismatch analysis (SPOT-CHECK, not REPLICATED).

## What is NOT in this directory
- No MD trajectories (Geant4-DNA, CPMD, LAMMPS-ReaxFF, GROMACS). None were rerun.
- No force-field parameter files. The paper does not supply them either.
- No oxygen-sweep data. Claim in §III is text-only in the paper.
- No environment lockfile (Python deps are only scipy + numpy + matplotlib on Python 3.11; trivially reproducible).

## Verdict
- **Queue label:** REPLICATED.
- **Substance:** SPOT-CHECK. Analytical rate-equation panel (2 ODEs, laptop-scale, < 5 s wall time) reproduces cleanly; MD pipeline that constitutes the paper's actual scientific contribution was NOT independently regenerated.
- Coverage 7/10, Agreement 8/10 for the part reproduced.
