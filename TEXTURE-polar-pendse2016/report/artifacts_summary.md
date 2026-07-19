# Artifacts Summary — Pendse & Bhattacharyay 2016

| # | Artifact | Path | Description |
|---|----------|------|-------------|
| 1 | Solver code | `code/pendse2016_replication.py` | Single-file numpy/scipy replication: GP vortex BVP, thick/thin scale selection, thin-vortex profiles, energy comparison, figure generation. |
| 2 | Results JSON | `work/results.json` | 12 claims with paper_value / reproduced_value / match / note, plus a `meta` block of headline numbers. 12/12 PASS. |
| 3 | Figures | `figs/*.png` | 4 figures (see below). |
| 4 | Report (LaTeX) | `report/REPORT.tex` | Full write-up: physics recap, method, scorecard table, figures, discussion. |
| 5 | Report (PDF) | `report/REPORT.pdf` | Compiled (pdflatex ×2), figures embedded. |
| 6 | Open questions | `report/open_questions.json` | 5 questions (q / basis / next_steps). |
| 7 | Workflow | `report/workflow.md` | Step-by-step + reproduce instructions. |
| 8 | Failure analysis | `report/failure_analysis.md` | Limitations, one fixed bug, honest caveats. |
| — | Meta | `META.json` | Updated status + verdict. |

## Figures
- `figs/thick_vortex_profile.png` — conventional vortex f(η) from GP ODE Eq.3, core ~ ξ₀, with r/√(β²+r²) ansatz overlay.
- `figs/thin_vortex_profiles.png` — thin-vortex generalized non-local profiles for |s|=1,2,3 vs r/a (reproduces paper Fig.1); core ~ a.
- `figs/two_length_scales.png` — thick vs thin plotted each in its own core unit, showing the independent microscopic (a) and mesoscopic (ξ₀) scales.
- `figs/thick_existence_boundary.png` — discriminant D⁴−32ξ₀⁴ vs D/ξ₀; sign flip at 32^{1/4} marks where the thick vortex ceases and the thin branch survives.

## Headline reproduced numbers
- Conventional core width = **1.30 ξ₀** (O(1) healing length). ✓
- Thin core width = **1.41 a** (β_thin = 0.7071/a), **independent of ξ₀**. ✓
- Thick-vortex existence boundary D_crit/ξ₀ = **2.3784 = 32^{1/4}** (exact). ✓
- Thin near-origin selection β = **0.500/a** = 1/(2√g₂). ✓
- Energy-minimizing α_{s=1} = **0.6325 = √40/10** (exact). ✓
- Energy: ξ₀~a → comparable (ratio 0.83); ξ₀≫a → thick favoured (1.61 < 5.06). ✓

**Score: 12/12 claims reproduced. Verdict: REPLICATED.**
