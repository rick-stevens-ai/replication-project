# Artifacts Summary --- Urazhdin 2024 (arXiv:2408.08683v3)

**System:** SrTiO$_3$ (STO), Ti $d_\sigma$ + 4 O $p_z$ molecular-orbital plaquette.
**Method:** minimal 6-state molecular-orbital tight-binding + first-order TDPT for
chiral-phonon-induced transient orbital magnetization.
**Verdict:** **REPLICATED** --- Coverage ~6/10, Agreement ~9/10.

## 8-artifact inventory
| # | Artifact | Path | Status |
|---|----------|------|--------|
| 1 | Source paper | `textures-orbital-urazhdin2024.pdf` | present |
| 2 | Marker extraction (prose) | `extraction/marker.md` | **interim (pdftotext -layout)**; header flags degraded math |
| 3 | Nougat extraction (math) | `extraction/nougat.mmd` | **interim (pdftotext)** + hand-transcribed LaTeX Eqs.(1)-(18) |
| 4 | Report | `report/REPORT.tex` | complete (.tex source; no pdflatex on host) |
| 5 | Open questions | `report/open_questions.json` | 5 heavy Qs + next_steps |
| 6 | Workflow | `report/workflow.md` | complete |
| 7 | Artifacts summary | `report/artifacts_summary.md` | this file |
| 8 | Failure analysis | `report/failure_analysis.md` | complete |
| + | Evidence | `report/evidence/` | result JSON + kernel + recipe |
| + | Work | `work/` | kernel + result JSON (gitignored) |

## Headline numbers (traced to evidence JSON keys)
All from `report/evidence/urazhdin2024_result.json`:
| Quantity | Value | JSON key | Paper |
|----------|-------|----------|-------|
| MO eigenvalues (eV) | -1.60, -0.5415, -0.5415, 1.60, 4.80, 4.80 | `mo_eigenvalues_eV` | analytic Eqs.(1)-(3) |
| Analytic MO levels (eV) | identical to above | `mo_analytic_levels_eV` | Eqs.(1)-(3) |
| Bandgap (diag) | 3.2000 eV | `gap_from_diag_eV` | 3.2 |
| Bandgap (analytic) | 3.2000 eV | `gap_analytic_eV` | 3.2 |
| $\sin^2\theta_a$ | 0.8986 | `sin2_theta_a` | $\lesssim1$ |
| $a_t$ | 5.70 eV/nm | `koster_slater.a_t` | 5.7 |
| $a_l$ | 19.95 eV/nm | `koster_slater.a_l` | 20.0 |
| $a_+$ | 12.825 eV/nm | `koster_slater.a_plus` | 13 |
| $a_-$ | 7.125 eV/nm | `koster_slater.a_minus` | 7 |
| $a_+^2-a_-^2 = a_l a_t$ | 113.715 (eV/nm)$^2$ | `koster_slater.a2_diff` / `al_at` | identity |
| $\mu_1$ (inter-atomic scale) | 1.597 $\mu_B$ | `mu_1_muB` | 1.6 |
| TDPT numeric / Eq.(8) | 0.99996 | `atomic.ratio_num_over_eq8` | 1 |
| $Q_0$ for $10^{-2}\mu_B$ | 0.0899 nm | `atomic.Q0_nm_for_1e-2_muB` | 0.08 |

## Reproduce block
```bash
cd /home/stevens/textures-100/corpus/textures-orbital-urazhdin2024
/home/stevens/comfyui-env/bin/python work/urazhdin2024_repl.py
# -> work/urazhdin2024_result.json (mirrored in report/evidence/)
# Verified 2026-07-19: live re-run == saved JSON to all quoted digits.
```
Compile report off-host: `pdflatex report/REPORT.tex`.

## Notes
- Artifacts 2--3 are honest `pdftotext` interims (marker/nougat not installed). marker.md
  = prose (layout mode); nougat.mmd = math (hand-transcribed numbered equations + raw
  dump appendix). This is a tooling limitation, NOT a physics gap.
- Paper reports NO transport observable (no orbital Hall conductivity / no k-dependent
  band structure) --- it is a real-space MO model; we reproduced what it defines.
