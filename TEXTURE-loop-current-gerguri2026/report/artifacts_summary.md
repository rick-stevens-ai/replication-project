# Artifacts Summary --- Gerguri et al. 2026 (CeRu3Si2 q=1/2 charge order)

Replication of arXiv:2603.27408 headline: *DFT+U reproduces the experimentally dominant
q=1/2 (Pmma) charge order in CeRu3Si2 only for Ce-4f U>6 eV, with q=1/3 (Imma) nearly
degenerate; Ce-4f-as-core fails to stabilize q=1/2.* DFT+U scoped out; kagome tight-binding
+ mean-field surrogate built instead.

## Verdict: PARTIAL  |  Coverage 7/10  |  Agreement 7/10

## Artifacts (all paths absolute)
| # | Artifact | Path |
|---|----------|------|
| 1 | Marker extraction (interim pdftotext) | `/home/stevens/textures-100/corpus/textures-loop-current-gerguri2026/extraction/marker.md` |
| 2 | Nougat extraction (interim pdftotext) | `/home/stevens/textures-100/corpus/textures-loop-current-gerguri2026/extraction/nougat.mmd` |
| 3 | Report (LaTeX) | `/home/stevens/textures-100/corpus/textures-loop-current-gerguri2026/report/REPORT.tex` |
| 4 | Open questions (5 Qs + next_steps) | `/home/stevens/textures-100/corpus/textures-loop-current-gerguri2026/report/open_questions.json` |
| 5 | Workflow | `/home/stevens/textures-100/corpus/textures-loop-current-gerguri2026/report/workflow.md` |
| 6 | Artifacts summary (this file) | `/home/stevens/textures-100/corpus/textures-loop-current-gerguri2026/report/artifacts_summary.md` |
| 7 | Failure analysis | `/home/stevens/textures-100/corpus/textures-loop-current-gerguri2026/report/failure_analysis.md` |
| 8 | Evidence dir (result JSON + code + kernels) | `/home/stevens/textures-100/corpus/textures-loop-current-gerguri2026/report/evidence/` |

Evidence contents: `gerguri2026_result.json`, `gerguri2026_replication.py`,
`loop_current_kagome_kernel.py`, `loop_current_meanfield_kernel.py`, `replication_recipe.json`.
Primary result also at `work/gerguri2026_result.json`; runnable code at
`work/gerguri2026_replication.py`.

## Key numbers (CDW susceptibility chi_q; larger = favored)
| U (eV) | chi(1/2) | chi(1/3) | chi(1/4) | ground state |
|--------|----------|----------|----------|--------------|
| 0 | 0.389 | **0.448** | 0.292 | q=1/3 |
| 4 | 0.313 | **0.324** | 0.179 | q=1/3 (near-degenerate) |
| 5 | **0.297** | 0.278 | 0.162 | q=1/2 (crossover) |
| 6 | **0.284** | 0.233 | 0.149 | q=1/2 |
| 9 | **0.265** | 0.145 | 0.129 | q=1/2 |
| f-as-core | 0.285 | 0.109 | **0.472** | q=1/4 (CO*) |

Surrogate crossover U~=5 vs paper U*=6 eV. f-as-core -> q=1/4 CO* (q=1/3 suppressed,
q=1/2 not ground state) reproduces the paper's failure mode.

## Kernel credit
`loop_current_kagome_kernel.py` (kagome geometry / TB conventions) and
`loop_current_meanfield_kernel.py` (occupied-density / band-energy pattern), both from
`/home/stevens/shared-kernels-cache/`.
