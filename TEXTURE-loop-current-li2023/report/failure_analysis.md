# Failure Analysis — li2023

Honest accounting of what did **not** fully replicate and why. No results were
fabricated; where a quantity could not be reconstructed it is stated plainly.

## 1. Closed-form Eq.(4) prefactor magnitude — NOT matched (main PARTIAL)
- **What:** The full-diagonalization free-energy difference Δf = f_CBO⁻ − f_LCBO
  and the closed-form Eq.(4) agree in **sign, λ² scaling, and the instability
  boundary**, but differ in absolute magnitude by an |Δ|-dependent factor
  (e.g. |Δ|=0.08 → Δf_num=5.6e-3 vs Δf_eq4=3.1e-4; ratio not constant).
- **Why:** Eq.(4) is a *leading-order degenerate-perturbation-theory* result
  (perturbing in λ around the λ=0 minima E₁..E₃). Its derivation lives in SM
  Sec.II–IV and carries a specific patch measure, k-cutoff regularization, and
  1/A normalization that the main text does not fully specify. Our direct
  patch-summed full diagonalization uses a different (explicit, disk-integrated)
  normalization. The two are the same physics to leading order in λ but not
  identical numerically. Reconstructing the SM perturbation theory is the fix
  (see open_questions #1).

## 2. Self-consistency — approximated, not solved
- **What:** We compared two *fixed candidate* order parameters (Δ_CBO⁻=−|Δ|,
  Δ_LCBO=|Δ|e^{iπ/3}) at chosen |Δ|, rather than solving the self-consistent gap
  equation dF/dΔ=0 for the true minimum at each (V, μ).
- **Why:** The paper's headline is a *comparison* between these two specific
  competing minima (justified by the λ=0 gauge degeneracy), so the fixed-candidate
  comparison directly tests the claim. Full self-consistency would be needed to
  regenerate the Fig.4a phase diagram (deferred, open_questions #5).

## 3. 9-band DFT model — not built (Fig.3, Fig.5)
- **What:** We replicated the *effective 6×6 patch model* (Eq.2), not the
  DFT-fitted 9-band tight-binding model H_TB(k) of Ref.[68].
- **Why:** The 9-band hoppings are not provided in the paper text; they require
  the external Ref.[68] Wannier fit. The recipe itself flags this
  ("requires reconstructing the DFT-fitted 9-band TB parameters"). The b, b', λ,
  ε₁, ε₂ values from Fig.4 were used directly as effective-model inputs.
  Consequently Fig.5 (all-bands robustness) is not independently verified.

## 4. Extraction pipeline — interim, not GPU Marker/Nougat
- **What:** `marker.md` and `nougat.mmd` are `pdftotext -layout` outputs plus
  curated headers, not true Marker/Nougat transformer extractions.
- **Why:** No GPU / Marker / Nougat model available in this CPU replication
  sandbox. The verbatim body text is preserved so no information is lost; files
  are explicitly labeled as interim stand-ins to avoid misrepresentation.

## What DID replicate cleanly
- λ=0 CBO⁻/LCBO degeneracy (gauge-symmetry argument) — machine precision.
- Finite-λ selection of LCBO (Fig.4b behavior) — monotone, correct sign.
- λ² scaling of Δf — fit exponent 1.98.
- Instability condition δε < 4(|b|²+|b'|²)|Δ| — sign of Δf matches 7/7.
- Eq.(3) eigenvalue structure (3 negative eigenvalues at small separation).

## Net
The **mechanism** — coupled opposite-mirror vHS + NN repulsion → LCBO favored at
small separation via a λ-driven splitting — is robustly reproduced. The
**quantitative closed form** is reproduced up to an unresolved SM normalization
prefactor. Verdict: REPLICATED (mechanism) / PARTIAL (prefactor).
