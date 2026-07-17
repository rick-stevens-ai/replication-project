# Failure / Gap Analysis — göbel2024 (arXiv:2410.00820)

Overall: the **headline physics replicated cleanly**. This file documents the two
places our minutes-scale CPU run fell short of the paper's *quantitative* figures, the
root cause of each, and what a full-fidelity reproduction requires. Nothing here changes
the qualitative conclusion (topological OHE without SOC, orbital ≫ spin).

## Gap 1 — Area-scaling exponent: ½(r×v) vs the modern orbital-magnetization operator (C2)

**Symptom.** The paper reports σ^Lz ∝ area² (quadratic) while σ_xy, σ^Sz ∝ area¹ (linear)
(Fig S2). In our run, at fixed filling:
- accumulated ⟨L_z⟩ vs λ slope ≈ **1.44** (linear-in-area — the paper's stated *mechanism*, reproduced ✅),
- but σ^Lz vs λ slope ≈ **1.005** (≈linear, not quadratic),
- and σ^Sz vs λ slope ≈ **2.40** — i.e. the exponent *ordering* is inverted vs the paper.

**Root cause.** We used the simplified itinerant orbital operator
`L_z = ½(X v_y − Y v_x)` (center-of-mass angular momentum, v = i[H,R]). This captures the
sign, magnitude, and the linear growth of the *moment per state*, but it under-weights the
transverse orbital *current*'s extra area factor. The paper uses the **modern
orbital-magnetization (Berry-phase) operator** (their Eq. 5 — flagged in method_extract.md
as "the error-prone piece") together with the orbital current `j^{Lz}_x = ½{v_x, L_z}`.
That operator supplies the additional "larger orbits ⇒ larger L_z per state" enhancement
which turns the linear moment growth into a quadratic conductivity growth.

**What a full reproduction needs.** Implement Eq.(5) (off-diagonal, corrected imaginary
unit) and the anticommutator current; re-run the λ sweep; fit the exponent. Expectation
(Q1/Q4): the modern operator recovers σ^Lz ∝ area² while σ^Sz stays linear.

## Gap 2 — Charge Hall not integer-quantized: single skyrmion in a finite cell (C3-charge)

**Symptom.** σ_xy (charge Hall) came out ≈ 0 (~1e-12) at every λ, not an integer Chern
number in a gap (paper Fig 3b).

**Root cause.** A **single** skyrmion embedded in a fixed finite periodic cell does not
open a *global* charge gap — there is no bulk insulating plateau on which a TKNN integer
can be defined. The vanishing value is therefore structurally expected, not a bug or a
convergence failure. (The texture-induced *minigap* we tune to is a local low-DOS window,
not a global charge gap.)

**What a full reproduction needs.** A **skyrmion-crystal supercell** where the magnetic
unit cell equals the skyrmion (paper's Fig S2 setup), with Bloch-space k-integration over
the magnetic BZ. That opens global gaps and lets σ_xy quantize to integer Chern values
while σ^Lz remains large and non-integer (Q2).

## Not attempted this pass (scope, not failure)
- **C4 (AFM skyrmion / bimeron, compensated charge Hall + pure orbital Hall):** only the
  FM Néel skyrmion was run. Requires the checkerboard AFM texture + 2nd-neighbor hopping (Q3).
- **C5 (orbital-polarized edge states / skipping orbits):** slab geometry not built.
- **Convergence vs L and k-mesh:** single L=28 real-space cell, Γ-only (Q5).

## What a complete reproduction requires (summary)
1. Modern orbital-magnetization operator (Eq. 5) + anticommutator orbital current → correct area exponent.
2. Skyrmion-crystal supercell + magnetic-BZ k-integration → integer charge quantization.
3. AFM/bimeron texture variants → C4.
4. Slab TB → C5 edge states.
5. Finite-size / k-mesh convergence study → error bars on the reported numbers.

None of these are expected to overturn C1 (finite OHE, no SOC) or the orbital ≫ spin
ordering; they sharpen the quantitative exponents and the quantization sub-claims.
