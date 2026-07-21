# Failure / partial-replication analysis — zhang2024 (arXiv:2411.05576)

## Was it a drop? NO.
Flagged as `class=EXPERIMENT` / likely experiment-only drop (analogous to jia2026/shen2018). **This flag is incorrect for the theory core.** The paper is a *combined* theory+experiment work whose theory is a closed-form, mesh-free analytic construction (six-plane-wave SPP interference → normalized polarization → Pontryagin/skyrmion-number integral). That core is fully reproducible without any fabricated microscopy data, so a DROP would be dishonest. Recommendation: **REPLICATE (partial)**.

## What reproduced cleanly
- **Elementary single hexagonal SPP lattice → Q = +1.00 per primitive cell** (Berg–Lüscher), matching the paper's Q=±1 elementary-skyrmion claim. This validates the entire Eq.(1)→(4) implementation and the topological-charge integrator end-to-end.

## What did NOT fully reproduce (the partial)
- **Cluster value Q = −3 per moiré unit at θ=38.21°** was not isolated. Over the symmetric composite grid the *total* charge integrates to ≈0 — equal populations of positive and negative skyrmions nucleate (consistent with the paper's own red/blue topological-point figure), but the specific −3 per moiré unit could not be pinned down.

### Root cause (honest)
1. **Missing σ_j map.** Eq.(1) sets φ_j = 2πσ_j/N but the integer index map σ_j is not in the main text; it lives in the Supplemental Material. The cluster charge is highly sensitive to this map.
2. **Undefined integration cell.** Q=−3 is "per moiré unit," but the moiré primitive cell boundary (which sub-region to integrate) is defined in Supplemental S5, not the main text. A generic central box yields net ≈0 by symmetry.
3. **Δφ and displacement.** The relative group phase Δφ and the S5 critical-inversion condition (displacement error dx,dy) set the sign/magnitude; only qualitative choices were available.

### Not a numerical artifact
Berg–Lüscher (integer-robust) and the finite-difference integral agree, and the elementary case gives exactly +1 — so the integrator is correct. The gap is *information* (Supplemental parameters), not method.

## Path to full replication
Extract arXiv ancillary/Supplemental (S1–S5): σ_j table, moiré cell definition, inversion inequality → restrict the integral accordingly and re-score. See `open_questions.json`.
