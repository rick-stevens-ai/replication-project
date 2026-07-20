# Artifacts summary — li2019 magnon spin Nernst replication

Paper: Li, Sandhoefner & Kovalev, *Intrinsic spin Nernst effect of magnons in a
noncollinear antiferromagnet*, arXiv:1907.10567v3.
Verdict: **PARTIAL** — Coverage 7/10, Agreement 6/10.

## The 8 artifacts

| # | Artifact | Path | Contents |
|---|----------|------|----------|
| 1 | Marker extraction | `extraction/marker.md` | pdftotext interim + marker-style header; abstract, model, main result, findings |
| 2 | Nougat extraction | `extraction/nougat.mmd` | Mathpix-markdown transcription with LaTeX equations (Eq. 15, 9, model) |
| 3 | Report (LaTeX) | `report/REPORT.tex` | Full write-up: model, method, results table, PARTIAL assessment |
| 4 | Open questions | `report/open_questions.json` | 5 questions (question/why/next_step) + next_steps list |
| 5 | Workflow | `report/workflow.md` | Step-by-step replication process incl. RETRY context |
| 6 | Artifacts summary | `report/artifacts_summary.md` | This file |
| 7 | Failure analysis | `report/failure_analysis.md` | Bugs found + fixes + remaining limitations |
| 8 | Evidence | `report/evidence/` | `li2019_result.json`, `li2019_kernel.py`, `replication_recipe.json` |

## Key numbers (nk=24 headline)

| Observable | Paper | This work | Verdict |
|---|---|---|---|
| Canting angle eta | 1.9 deg | 1.91 deg | exact match |
| Magnon band width / J1S | ~2-2.3 | 3.4 | same order |
| alpha^y_yx / kB peak | ~3.5 | 2.70 | same sign & order |
| alpha^z_yx / alpha^y_yx | ~1e-2 (2 orders) | 6.5e-3 | match |
| Chern (bottom->top) | -3, 1, 2 | not clean (Goldstone) | fail |

## 3-line physics summary
The in-plane DMI in the 120-degree noncollinear kagome AFM KFe3(OH)6(SO4)2 tilts
the spins out of plane by ~1.9 deg and generates a finite, intrinsic magnon spin
Nernst conductivity of order k_B via the bosonic-Kubo spin Berry curvature with
c1 Bose weighting. Our from-scratch BdG + Colpa build reproduces the canting
angle exactly and the correct sign, order of magnitude (~2.7 vs ~3.5 k_B), and
temperature rise of alpha^y_yx, plus the ~150x in-plane/out-of-plane anisotropy
set by the small canting. The integer Chern numbers and exact peak value remain
grid-limited by the near-gapless AFM Goldstone mode -> PARTIAL.

## Reproduce
```
/home/stevens/comfyui-env/bin/python \
  /home/stevens/textures-100/corpus/textures-spin-li2019/work/li2019_kernel.py
# ~8 s; writes work/li2019_result.json
```
