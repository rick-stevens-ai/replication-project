# Artifacts summary — gurung2023 (Mn₃GaN nearly-100% spin polarization)

**Verdict: REPLICATED** (tight-binding headline mechanism) — DFT/ETMR out of scope.

## Self-score
| Axis | Score | Basis |
|---|---|---|
| **Coverage** | **7/10** | Headline mechanism + spin-polarization definition (Eq. 2) fully reproduced from scratch on the paper's own kagome model. DFT Mn₃GaN Fermi surface and ETMR ~10⁴% transport intentionally not attempted. |
| **Agreement** | **9/10** | max p_k∥ = 0.99997 ≈ **100%** vs "nearly 100%"; 6 spin-split bands (no SOC) exactly as paper. Only gap: whole-grid "broad area" fraction under-reports vs paper's fixed-E_F map (metric artifact, documented). |

## Headline comparison
- **Claim:** noncollinear AFM exhibits **nearly 100%** spin-polarized conduction channels.
- **This work:** `p_k∥^max = 0.99997` on a from-scratch kagome noncollinear-AFM TB model (Δ/t=1.5). ✓
- Bands: 6 (paper: 6) ✓ ; spin-split without SOC ✓.

## The 8 artifacts
1. `extraction/marker.md` — extraction summary (pdftotext interim + header).
2. `extraction/nougat.mmd` — Nougat-style .mmd (interim pdftotext body + header).
3. `report/REPORT.tex` — full LaTeX replication report.
4. `report/open_questions.json` — 5 questions {question, why_it_matters, next_step} + next_steps.
5. `report/workflow.md` — step-by-step method.
6. `report/artifacts_summary.md` — this file.
7. `report/failure_analysis.md` — scope limits, metric caveats, no-fabrication note.
8. `report/evidence/` — `gurung2023_result.json` + `code/` (model script, kernel, result copy).

## Evidence
- Model: `report/evidence/code/gurung2023_noncollinear_kagome_spinpol.py` (from scratch).
- Result: `report/evidence/gurung2023_result.json` (verbatim script output); saved-early to `work/gurung2023_result.json`.
- Kernel credited: `report/evidence/code/gobel2024_sd_skyrmion_kubo_Lz_kernel.py` (s–d lattice pattern).
- Runtime: ~2.3 s on `/home/stevens/comfyui-env/bin/python`.

## 3-line physics summary
A 2D kagome tight-binding model with a 120° noncollinear AFM exchange texture
(Γ₅g-like, Δ/t=1.5) breaks P̂T̂ and T̂t̂, producing six spin-split bands without SOC.
Collecting Fermi-crossing conduction channels at each (k_y, E_F) and applying the
paper's Eq. 2, p_k∥ = |Σₙsₙ|/Σₙ|sₙ| reaches 0.99997 — confirming the "nearly 100%"
effective spin polarization that underpins the predicted ETMR in Mn₃GaN AFMTJs.
