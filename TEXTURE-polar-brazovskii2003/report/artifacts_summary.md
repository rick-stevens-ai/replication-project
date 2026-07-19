# Artifacts Summary — brazovskii2003

**Paper:** S. Brazovskii, arXiv:cond-mat/0306006v2, *Theory of the ferroelectric phase
in organic conductors: optics and physics of solitons* (ECRYS-2002 proceedings).
**Verdict:** PARTIAL (mechanism-level REPLICATED) — coverage 8/10, agreement 9/10.

## 8-artifact inventory
| # | Artifact | Path | Status |
|---|----------|------|--------|
| 1 | Source paper | `textures-polar-brazovskii2003.pdf` | present |
| 2 | Marker text extraction (PROSE) | `extraction/marker.md` | **INTERIM** — pdftotext `-layout` (marker not installed) |
| 3 | Nougat math extraction (MATH) | `extraction/nougat.mmd` | **INTERIM** — hand-transcribed LaTeX eqs + pdftotext dump (nougat not installed) |
| 4 | Detailed report + critique | `report/REPORT.tex` | complete (.tex source; no pdflatex on host) |
| 5 | Open questions + next steps | `report/open_questions.json` | complete (5 heavy Qs + next_steps) |
| 6 | Workflow / tools / effort | `report/workflow.md` | complete |
| 7 | Artifacts summary | `report/artifacts_summary.md` | this file |
| 8 | Failure / gap analysis | `report/failure_analysis.md` | complete |
| + | Evidence | `report/evidence/` | result JSON + output JSON + solver `.py` |
| + | Work / scratch | `work/` | solver + both result JSONs (gitignored) |

## Extraction-tooling note (NOT a physics gap)
`marker` and `nougat` are not installed on the packaging host; only poppler `pdftotext`
is available. Both extraction files carry an in-file NOTE header stating the interim
status, the fidelity caveat (Unicode math degraded by pdftotext), and the exact
regenerate command. The authoritative equation transcriptions live in `REPORT.tex`
and in the `\section*{Key equations}` block at the top of `nougat.mmd`.

## Headline numbers (traced to evidence JSON keys)
| Quantity | Value | Evidence key (`brazovskii2003_output.json`) |
|----------|-------|---------------------------------------------|
| Optical edge ratio `omega_t/(2*Delta)` @ gamma=0.25 | **0.3927** | `gaps.omega_t_over_2Delta` |
| `H` form identity max abs err | 4.44e-16 | `hamiltonian.form_identity_max_abs_err` |
| Ground-state min at phi=alpha | true | `hamiltonian.min_matches_alpha` |
| alpha-soliton charges (-2a/pi, 1-2a/pi) | -0.1652, 0.8348 | `soliton_charges_in_e.*` |
| Resonance rel err at Z=0.9999 | 1.17e-5 | `dielectric_response.w0t_rel_err_near_crit` |
| Soft-mode rel err at Z=0.9999 | 1.17e-5 | `dielectric_response.wfe_rel_err_near_crit` |
| Fano antiresonance eps/eps_inf(w0) | 1.0 | `dielectric_response.antiresonance_eps_over_epsinf_at_w0` |
| Curie amplitude A=(wp*/wt)^2 | 900 (~1e3) | `curie_law_and_soft_mode.A_amplitude_(wp*/wt)^2` |
| Curie product constancy std/mean | 5.5e-16 | `curie_law_and_soft_mode.curie_product_std_over_mean` |
| Spin tail/core ratio | 7.37 | `spin_sector.xi_sigma_spin_tail` |
| Checks passed | 10 / 10 | `verdict.n_passed` / `verdict.n_total` |

## Reproduce block
```bash
cd textures-polar-brazovskii2003/
/home/stevens/comfyui-env/bin/python report/evidence/brazovskii2003_replication.py
# prints results JSON; verdict.checks all true, n_passed=10.
# Live re-run on 2026-07-19 matched the saved JSON to the quoted digits.
```
Interpreter: `/home/stevens/comfyui-env/bin/python` (NumPy 2.3.5, SciPy 1.17.0).
