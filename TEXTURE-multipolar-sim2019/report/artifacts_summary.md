# Artifacts summary — Sim et al. 2019 (arXiv:1911.13224)

**Paper:** Multipolar superconductivity in Luttinger semimetals — Sim, Mishra, Park, Kim, Cho, Lee (2019)
**System:** cubic j=3/2 Luttinger semimetal (4-band) + quadrupolar Kondo; PrBi.
**Headline claim tested:** zero quadrupolar order → weak-coupling mean-field ground state is the
TR-breaking d-wave Delta_eg=(1,i)=d_{x2-y2}+i d_{3z2-r2}.
**Verdict: PARTIAL — Coverage 6/10, Agreement 6/10.**

## 8-artifact inventory
| # | Artifact | Path | Status |
|---|----------|------|--------|
| 1 | Source paper | `textures-multipolar-sim2019.pdf` | present |
| 2 | Marker extraction (prose) | `extraction/marker.md` | interim (pdftotext -layout + provenance header) |
| 3 | Nougat extraction (math) | `extraction/nougat.mmd` | interim (hand-transcribed eqs + pdftotext appendix) |
| 4 | Report | `report/REPORT.tex` | complete (.tex source; no pdflatex) |
| 5 | Open questions | `report/open_questions.json` | 5 Qs + next_steps, parse-checked |
| 6 | Workflow | `report/workflow.md` | complete |
| 7 | Artifacts summary | `report/artifacts_summary.md` | this file |
| 8 | Failure analysis | `report/failure_analysis.md` | complete |
| + | Evidence | `report/evidence/sim2019_result.json`, `report/evidence/code/` | result + code + kernel |
| + | Work | `work/sim2019_luttinger_bdg.py`, `work/sim2019_result.json` | run code + result |

## Headline numbers (traced to evidence JSON)
- `partA_pairing_susceptibility.lambda_eg_max` = **0.8973** vs `lambda_t2g_max` = **0.7983**
  → `leading_irrep` = **eg** (matches paper). ✔
- `partB_eg_selection_quartic.q2_invariant` = **-4.92e4** (< 0) → real state favored by our proxy,
  `TRB_1i_is_ground_state` = **false** (paper says true). MISMATCH (primary gap)
- `partB...strong_coupling_crosscheck_wholeBZ.q2_invariant` = **-7.91e3** (< 0) → real TR-symmetric
  eg d-wave favored at strong coupling (matches paper's weak→strong transition trend). ✔
- `clifford_algebra_ok` = true; `O20_matches_kernel_convention` = true.

## Comparison table
| Claim | Paper | This work | Match |
|-------|-------|-----------|-------|
| Leading irrep | eg | eg | yes |
| Weak-coupling GS | (1,i) TR-breaking | (1,0)/(0,1) real | no |
| Strong-coupling GS | real d_{3z2-r2} | real eg d-wave | yes (trend) |

## Reproduce block
```bash
cd /home/stevens/textures-100/corpus/textures-multipolar-sim2019
~/comfyui-env/bin/python work/sim2019_luttinger_bdg.py   # ~11 s, writes work/sim2019_result.json
# regenerate extraction (real tools when available):
#   marker_single textures-multipolar-sim2019.pdf ./extraction --output_format markdown
#   nougat textures-multipolar-sim2019.pdf -o ./extraction --markdown
#   pdflatex report/REPORT.tex
```

## Provenance
Physics kernel builds on the Stevens/multipole operator conventions of
`ollie_multipolar_stevens_landau_kernel.py` (cross-check of the j=3/2 O20 quadrupole);
BdG/pairing physics is a from-scratch build. Copy bundled at `report/evidence/code/`.
