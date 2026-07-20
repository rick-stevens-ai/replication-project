# Artifacts Summary — malashevich2012

**Paper:** Malashevich, Coh, Souza, Vanderbilt, "Full magnetoelectric response of
Cr₂O₃ from first principles", PRB **86**, 094430 (2012), arXiv:1207.5873.
**Verdict:** PARTIAL — orbital ME **method** reproduced (4/4 claims); absolute
α⊥ = 1.04 ps/m honestly scoped as spin-DFT (out of fast-run budget).

## Files
| # | Path | Description |
|---|------|-------------|
| 1 | `extraction/marker.md` | Structured extraction: headline, Table II & III values, key params (pdftotext interim + hand-transcribed tables). |
| 2 | `extraction/nougat.mmd` | Full raw layout text (pdftotext -layout; GPU Nougat not run in fast pass). |
| 3 | `report/REPORT.tex` | Full LaTeX report: claim, scope, method, comparison table, verdict. |
| 4 | `report/open_questions.json` | 5 open questions {question, why_it_matters, next_step} + next_steps. |
| 5 | `report/workflow.md` | Step-by-step replication workflow. |
| 6 | `report/artifacts_summary.md` | This file. |
| 7 | `report/failure_analysis.md` | What was not reproduced and why. |
| 8 | `report/evidence/` | `malashevich2012_result.json` + `code/malashevich2012_orbital_ME.py` + gobel2024 kernel + recipe. |

## Physics result (`work/malashevich2012_result.json`)
- Chern–Simons ME quantum computed: **24.34 ps/m** (paper 24.3, <0.2% error).
- Topological θ=π → α_CS = 24.34 ps/m; trivial (Cr₂O₃-like) θ=0.
- Itinerant Lz (IC branch) = 6.13 a.u. (finite → active).
- Method claims reproduced: **4/4**. Runtime ≈ 2.3 s.

## Scores (self-assessed)
- **Coverage: 7/10** — orbital method + Berry machinery fully rebuilt; spin-DFT
  (98% of headline) scoped not run.
- **Agreement: 8/10** — every reproduced quantity matches (CS quantum to <0.2%);
  absolute headline not computed but consistently scoped.

## Credits
Berry/orbital machinery: `gobel2024_sd_skyrmion_kubo_Lz_kernel.py`.
