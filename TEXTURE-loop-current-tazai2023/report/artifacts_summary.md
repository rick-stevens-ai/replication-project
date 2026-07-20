# Artifacts Summary --- Tazai-Yamakawa-Kontani (arXiv:2303.00623v4)

Kagome AV3Sb5 loop-current order; tiny orbital magnetization & ~1 T chiral-domain switching.

## Verdict: PARTIAL
Named gap: quantitative GL power laws (M_orb ∝ η³ current-only; ∝ η with bond
order) and the bond-order **enhancement** coefficient m1 are not reproduced. The
core mechanism (3Q chiral current → finite M_orb; ΔF = −3 h_z M_orb; h_z=1e-4 ↔
1 T switches the domain) is reproduced qualitatively with correct sign & scale.

## Self-score
- **Coverage: 8/10** — all four headline claim families (C1 selection rule, C2
  power law, C3 bond enhancement, C4 field switching) implemented from scratch
  and tested; multi-orbital realistic model and dense-mesh convergence not done.
- **Agreement: 5/10** — magnitude of M_orb (~1e-4 μB), geometric flux
  non-cancellation, and the field-coupling sign/scale all match; but the two
  quantitative power-law exponents and the bond-order enhancement sign do not.

## 8 Artifacts
| # | Artifact | Path |
|---|---|---|
| 1 | Extraction (marker) | `extraction/marker.md` |
| 2 | Extraction (nougat, INTERIM pdftotext fallback) | `extraction/nougat.mmd` |
| 3 | Report (LaTeX) | `report/REPORT.tex` |
| 4 | Open questions (5 Qs + next_steps) | `report/open_questions.json` |
| 5 | Workflow | `report/workflow.md` |
| 6 | Artifacts summary (this file) | `report/artifacts_summary.md` |
| 7 | Failure analysis | `report/failure_analysis.md` |
| 8 | Evidence (result JSON + code + kernel) | `report/evidence/` |

## Evidence contents
- `report/evidence/tazai2023_result.json` — numerical results (runtime 5.0 s)
- `report/evidence/tazai2023_replicate.py` — from-scratch replication code
- `report/evidence/loop_current_kagome_kernel.py` — credited shared kernel
- `report/evidence/replication_recipe.json` — extraction recipe

## Key numbers
| Quantity | Value | Paper |
|---|---|---|
| M_orb (3Q, η=0.02) | 2.64e-4 μB | ~1e-4 (Fig 2a) ✓ |
| net flux 1Q / 3Q | 4e-19 / 5.4e-2 | 0 / finite ✓ |
| slope current-only | 1.31 | 3 ✗ |
| slope with bond | 1.21 | 1 (~) |
| bond factor @η=0.02 | ×0.52 (suppress) | enhance ✗ |
| ΔF switch @1T | 8.2e-8 (μB-eV) | tiny field switches ✓ |
| h_z ↔ field | 1e-4 ↔ 1 T | 1e-4 ↔ 1 T ✓ |
| runtime | 5.0 s | budget <3 min ✓ |

## Credits
Kernel: `loop_current_kagome_kernel.py` (shared-kernels-cache; Fernandes-Birol-
Ye-Vanderbilt kagome flux-phase kernel). Runner: `/home/stevens/comfyui-env/bin/python`.
