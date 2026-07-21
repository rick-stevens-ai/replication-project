# Artifacts summary — textures-polar-dahl2002

**Paper:** Ingolf Dahl, "Ferroelectricity, SSFLC, bistability and all that", arXiv:cond-mat/0211693
**Class:** polar / ferroelectric bistability
**Verdict (judge, argo:claude-opus-4.5, njudges=1):** PARTIAL — Coverage=3, Agreement=8.
Rationale: the from-scratch 0D LGD/TDGL model confirms Dahl's testable diagnostic
quantitatively (double-well loop width frequency-independent, slope −0.02;
single-well lossy width ∝ frequency, slope +1.06), but this is one narrow
diagnostic — the paper's central SSFLC surface-stabilization thesis (needing
spatial P(z) + anchoring) is out of scope, limiting coverage.

## Artifact inventory
| # | Artifact | Path |
|---|----------|------|
| 1 | Marker extraction (interim) | `extraction/marker.md` |
| 2 | Nougat extraction (interim) | `extraction/nougat.mmd` |
| 3 | Report (LaTeX) | `report/REPORT.tex` |
| 4 | Open questions (5 + next_steps) | `report/open_questions.json` |
| 5 | Workflow | `report/workflow.md` |
| 6 | Artifacts summary | `report/artifacts_summary.md` |
| 7 | Failure analysis | `report/failure_analysis.md` |
| 8 | Evidence (result + code + figure + recipe) | `report/evidence/` |

## Supporting files
- Physics runner: `code/dahl2002_lgd_tdgl.py` (also copied to `report/evidence/`)
- Raw result: `work/dahl2002_result.json` (SAVE-EARLY) + copy in `report/evidence/`
- Parsed text: `work/textures-polar-dahl2002.txt` (1317 lines)
- Recipe: `report/evidence/replication_recipe.json`
- Figure: `report/evidence/dahl2002_hysteresis_diagnostic.png`
- Source PDF: `dahl2002.pdf` (327 KB, %PDF-1.2)

## Physics summary (3 lines)
Built a from-scratch 0D Landau–Ginzburg–Devonshire polarization model
(F=½aP²+¼bP⁴+⅙cP⁶−EP) driven by AC field under overdamped TDGL dynamics,
comparing a double-well (bistable) vs. a single-well nonlinear-lossy potential.
Dahl's diagnostic is reproduced quantitatively: the double-well hysteresis-loop
width is frequency-independent (log-log slope −0.02) while the lossy single-well
width is proportional to frequency (slope +1.06), with the double well retaining
a finite coercive field (~0.42) as ω→0 versus ~0.009 for the lossy case.

## Provenance / credit
LGD free-energy + Landau–Khalatnikov TDGL update adapted from
`ollie_tdgl_phasefield_polar_skyrmion_kernel.py` (author: Ollie), reduced to the
0D scalar polarization needed for the loop-width-vs-frequency diagnostic.

## Judge
Re-judged with `judge_verdict.py --model argo:claude-opus-4.5 --njudges 1`
(verdict recorded at pipeline end).
