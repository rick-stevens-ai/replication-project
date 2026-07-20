# Workflow — Wernert et al. 2024 replication

## 1. Ingest
- Read `report/evidence/replication_recipe.json` (method=model-Hamiltonian; headline = static-twist transverse Noether spin current).
- Read paper text `work/textures-spin-wernert2024.txt` (835 lines incl. End Matter): identified Eqs. (1)-(13), the static-twist headline, Fig.2 sign structure, and the polycrystal Hall-mass definition.
- Inspected shared kernel `gobel2024_sd_skyrmion_kubo_Lz_kernel.py` (Kubo/Berry, s-d tight binding) — recognized it as the *itinerant-electron* texture-Hall sibling method, while this paper's response is *magnonic/Noether*.

## 2. Choose replication strategy
- The paper's headline is an **analytic continuum result**, so the faithful, non-fabricated replication is a **symbolic re-derivation** with sympy directly from the paper's own Lagrangian, Γ-tensor (Eq.2), and Noether current (Eq.5) — not a fitted number.
- Added a **numerical** LSWT check (3×3 dynamical matrix from Γ̄, Eq.12) for the polycrystal Hall-mass mode splitting (Eq.13).

## 3. Build (from scratch) — `work/wernert2024_replication.py`
- T2: construct Γ_ab^{αβ} for direct (η=+1) and inverse triangular order.
- T3 (HEADLINE): apply static twist ∂_x n_α = (∂_x φ) n_x×n_α to Eq.(5); verify J^y = ±(√3/8)JS²(∂_x φ)n_y and J^x≡0.
- T4: dynamical d.c. response ⟨J_y^y⟩ = Γ_yx^{yx} P_x^x; verify sign flip direct vs inverse (Fig.2).
- T5: diagonalize 3×3 dynamical matrix from Γ̄; verify one longitudinal + two degenerate transverse magnon branches split by 2g_H/ρ.

## 4. SAVE-EARLY
- Wrote `work/wernert2024_result.json` immediately after computation (verdict, tests, scores, summary).

## 5. Compare & score
- T3 exact (symbolic zero), T4 exact sign flip, T5 exact splitting magnitude (branch labeling partial).
- Verdict: **REPLICATED**. Coverage 8/10, Agreement 9/10.

## 6. Package (8 artifacts)
- `extraction/marker.md`, `extraction/nougat.mmd` (pdftotext interim + header)
- `report/REPORT.tex`, `report/open_questions.json`, `report/workflow.md`, `report/artifacts_summary.md`, `report/failure_analysis.md`
- Copied result JSON + code into `report/evidence/`.

## Tools & environment
- Runner: `/home/stevens/comfyui-env/bin/python` (sympy 1.14.0, numpy 2.3.5)
- Extraction: poppler `pdftotext`
- Runtime: ~0.06 s (symbolic + tiny numeric).
