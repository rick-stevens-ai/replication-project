# Workflow — nakazawa2024 replication

## 1. Read & understand
- Parsed `report/evidence/replication_recipe.json` and `work/*.txt` (full paper text).
- Identified headline: **R = −ΔM_orb / M_orb⁰ > 50% at ~1% impurity**, and the
  surprise sub-claim: **R is insensitive to η**.
- Model: kagome tight-binding (A/B/C), t=−0.5, t'=−0.02, T=0.01, n=2.55, μ=0;
  cLC = purely imaginary NN hopping δt=±iη (triple-Q); unitary impurity I=100 eV.

## 2. Build physics (from scratch)
- `work/nakazawa2024_replicate.py`:
  - Real-space kagome flake builder (`build_lattice`, `build_H`) with distance-based
    NN + 3rd-nearest bond detection and chirality-signed imaginary cLC hopping.
  - **Modern-theory orbital magnetization** via the itinerant circulation operator
    `L_z = ½(X v_y − Y v_x)`, `v = i[H,R]`, summed over occupied states —
    **reused from the gobel2024 kernel** (the paper's stated "nonlocal itinerant
    circulation" mechanism).
  - Impurity = single unitary site potential I=100 eV on a central A site; averaged
    over an Imp1-like and Imp2-like site.
  - Three scans: (A) η-scan of clean & impurity M_orb; (B) R normalized to 1%
    density vs η (insensitivity test); (C) system-size / impurity-density scan.

## 3. Run & SAVE-EARLY
- Runner: `/home/stevens/comfyui-env/bin/python` (numpy 2.3.5). Runtime ~seconds.
- Output saved immediately to `work/nakazawa2024_result.json`.

## 4. Compare & score
- Magnitude R (up to ~83% at small η, mean ~49% at 1%) → **matches** "can exceed 50%".
- η-insensitivity → **not** reproduced (R falls with η). Clean η³ law → not reproduced.
- Verdict: **PARTIAL**.

## 5. Package (8 artifacts)
- `extraction/marker.md`, `extraction/nougat.mmd` (pdftotext interim + header).
- `report/REPORT.tex`, `report/open_questions.json`, `report/workflow.md`,
  `report/artifacts_summary.md`, `report/failure_analysis.md`.
- Copied result JSON + replication code + both kernels to `report/evidence/`.

## Tools
- `pdftotext -layout` for extraction; numpy for physics; no GPU/Nougat available.
