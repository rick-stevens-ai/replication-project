# Workflow — mestral2025 Pockels replication

## 1. Recon
- Read `report/evidence/replication_recipe.json` → method=DFT, Pockels tensor of BTO
  (recipe correctly identifies the paper; only the *directory name* says "spin").
- Read `work/textures-spin-mestral2025.txt` (paper full text). Confirmed: **no spin
  physics**. Real headline = clamped r51 = 730 ± 150 pm/V.

## 2. Locate the ONE testable headline
- Eq. (4): ionic Pockels response `r_ion ~ Σ_m α_m p_m / ω_m²`.
- Table IV: r51 vs Ti off-centering series (0.466/0.45/0.425%) with soft-mode ω.
- Chosen headline: **r51 is soft-mode dominated (∝ 1/ω²); rises as off-centering drops,
  bracketing experiment near 0.45%.**

## 3. Build from scratch (physics, <6 min, no DFT)
- `report/evidence/mestral2025_pockels_model.py` — two models:
  - **Model 1**: mode-sum with 1/ω² soft-mode dominance. Calibrate one constant at the
    P4bm ground state; predict the other two Table-IV points from ω alone.
  - **Model 2**: Landau anharmonic double-well F(Q)=½aQ²+¼bQ⁴ → ω²(q)∝3q²−1 for
    the microscopic origin of soft-mode softening.
- Runner: `/home/stevens/comfyui-env/bin/python`.

## 4. SAVE-EARLY
- Wrote `work/mestral2025_result.json` immediately on first successful run.

## 5. Compare + score
- r51 predictions vs paper Table IV: MARE(non-anchor) = 3.68%; r51@0.45% = 695.5 pm/V
  ∈ [580, 880] exp band. ω model MARE = 33% (qualitative only).
- Honest verdict: **PARTIAL** (headline r51 strongly reproduced; ω law weak).

## 6. Package (8 artifacts)
- extraction/marker.md, extraction/nougat.mmd (pdftotext -layout interim + headers)
- report/REPORT.tex, open_questions.json, workflow.md, artifacts_summary.md,
  failure_analysis.md
- Copied result JSON + model code into report/evidence/.

## Tools / kernels
- `pdftotext -layout` (poppler) for extraction.
- gobel2024 skyrmion Kubo kernel + spin_ed_probes: **inspected, not used** (irrelevant).
