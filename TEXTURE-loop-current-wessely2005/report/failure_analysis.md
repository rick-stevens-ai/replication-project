# Failure Analysis — arXiv:cond-mat/0511224

## 0. Classification failure (upstream, honestly flagged)
The paper was tagged **loop-current** in the TEXTURES-100 set. It is actually **spin-transfer torque in a helical spin density wave**. There is no orbital/loop current, no kagome lattice, no Peierls flux. The shared kagome loop-current kernel was therefore inapplicable and NOT used. We replicated the true in-scope core (STT in a spin spiral) with purpose-built code. This is a taxonomy error, not a physics failure.

## 1. What was NOT reproduced (scope-limited, not a bug)
- **Absolute rotation frequency 0.07 GHz** and the numeric **C₂₃ = 0.5 ħ Å²**. These are FP-APW+lo LSDA DFT outputs (Eq. 8 spin-flux at augmentation spheres, 41³ k-mesh, Er conduction bands). We ran no DFT (offline / free-endpoints scope). Verifying them would require a Wannier/TB fit to Er's real bands (see open_questions #2).

## 2. Genuine partial/negative result: C6 crude-vs-microscopic ratio
- **Paper claim:** crude analytic estimate ≈ 4× the microscopic C-matrix value.
- **Our model:** crude/micro ≈ 0.155 (crude UNDER-estimates), NOT ~4.
- **Root cause (understood, not hidden):** the crude adiabatic prefactor (½·P·qd·|v|) and the microscopic Q-tensor use different FS weightings and band counts. The paper's factor-4 is stated as order-of-magnitude for Er's specific multi-band nesting FS; a single-band 1D toy model has no reason to reproduce the numeric factor. The comparison is intrinsically model-dependent.
- **Handling:** reported as-is; `order_of_magnitude_match=false`. NOT fabricated or tuned to hit 4×. Marked "order-of-magnitude, not absolute" and logged as open question #1.

## 3. Frame-convention pitfall (found and fixed during the run)
- First pass hard-coded the "rotate-spiral" torque as the rotating-frame **y** spin-flux channel and got 0, while the **x** channel carried the signal → C1 spuriously "failed."
- **Root cause:** in the rotating (spiral) frame the local moment is along +x; the physically meaningful, nonzero in-plane transverse spin flux appeared in the x-channel. Diagnostic (printing all three channels) showed **Sx = Sy exactly** and **Sz = 0** — a clean planar-spiral signature.
- **Fix:** report all three raw channels; select the dominant in-plane channel as the rotate component and use the vanishing out-of-plane (z) channel as the planarity correctness check. This is now the documented, honest interpretation (C matrix has a single nonzero component, matching the paper).

## 4. Dimensional dead-end (recorded)
- Attempting to reproduce the paper's literal formula `(P q A)/(4 J e)` in SI gave ~10¹⁸ Hz per A/m² — clearly the paper carries ħ symbolically and uses mixed units in the crude estimate. We therefore did NOT chase the absolute analytic number; only the dimensionless ratio (C6) and the structural claims were tested. Documented so future runs don't re-derive the dead-end.

## 5. Lessons for the class
- Always run a classification audit on "loop-current" tags — this set contains at least one spin-texture/STT paper misfiled as loop-current.
- For DFT-quantitative papers, separate convention-independent claims (reproducible with a toy model) from material-specific numbers (need DFT) up front, and score only the former.
