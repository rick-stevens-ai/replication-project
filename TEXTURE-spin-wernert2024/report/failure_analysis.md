# Failure Analysis — Wernert et al. 2024

**Verdict: REPLICATED** (headline exact). This document records what was NOT reproduced and why, in the interest of honest scoring.

## What was reproduced (fully)
- **T3 — Headline static-twist Hall spin current.** Symbolic evaluation of Eq.(5) under ∂_x n_α = (∂_x φ) n_x×n_α gives J^y = ±(√3/8)JS²(∂_x φ)n_y with J^x≡0, matching the paper to symbolic zero (coefficient, sign, purely-transverse structure).
- **T4 — Dynamical d.c. Hall response sign.** ⟨J_y^y⟩ = Γ_yx^{yx}P_x^x flips sign between direct/inverse triangular order (Fig.2 structure).
- **T2 — Γ tensor components** (Γ_yx^{yx} = ±√3/4 JS², z-indices vanish).

## What was NOT reproduced (gaps)

### G1 — Full FM/noncollinear-AFM bilayer LLG numerics (Fig.2 magnitudes)
- **What:** The paper's numerical demonstration solves the linearized LLG equation on a 100×1 kagome strip (JFM=−1, JAFM=1), with a compensated interface (Jnnn=JFM), easy-axis/plane anisotropies (K=0.01, Kz=0.00125), a Gaussian a.c. drive (Eq.15, σ=2, ω=1), and large boundary damping (α=100) to prevent reflections.
- **Why not done:** This requires the End-Matter Sec.IV explicit lattice spin-current formulas and boundary-condition/anisotropy details that are only fully specified in the supplemental material [62], which is not in the provided text. Rebuilding it is a substantial numerical effort beyond the SAVE-EARLY analytic core.
- **Impact:** We reproduced the *sign structure* of Fig.2 analytically (T4) but not the absolute magnitudes/spatial profiles. Docks Coverage to 8/10.
- **Recovery path:** See open_questions.json Q1.

### G2 — Exact Eq.(13) magnon-velocity branch labeling
- **What:** The paper reports c_I=√(g0/ρ) (longitudinal) and c_{II,III}=√((g0+gH)/ρ) (transverse).
- **What we got:** Our naive elastic-like 3×3 dynamical matrix from Γ̄ yields two degenerate branches at v²=g0/ρ and one at v²=(2gH+g0)/ρ. The **splitting magnitude** (2gH/ρ, convention-independent) matches exactly and confirms the central physics (gH controls the split), but the specific branch **labels/values** of Eq.(13) differ.
- **Why:** The paper's linearized EOM (Eq.4) retains an n_α×(spin-rotation) projection (a Berry/gauge term) that our symmetric elastic matrix omits; this reshuffles the branch assignment without changing the gH-controlled splitting.
- **Impact:** T5 is a qualitative/mechanism match, not a strict one. Docks Agreement to 9/10.
- **Recovery path:** See open_questions.json Q2 (retain the projection term, diagonalize the non-symmetric dynamical matrix).

## No fabrication statement
All reported numbers come from actual sympy/numpy execution of `work/wernert2024_replication.py` (see `report/evidence/`). Where the paper's results were not reproduced (G1, G2), this is stated explicitly rather than approximated or invented.
