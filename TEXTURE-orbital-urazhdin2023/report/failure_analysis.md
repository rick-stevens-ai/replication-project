# Failure Analysis — urazhdin2023

**Verdict:** REPLICATED. No compute failures — the paper is fully analytic/closed-form, so
"replication" means independent re-derivation of every quoted number, which succeeded.

## What worked cleanly
- **All 5 claims reproduced.** C1 (crystal-field torque continuity) verified symbolically; C2
  (t2g dispersion, band width, degeneracy) exact; C3 (⟨Lz⟩ oscillation, ⟨Lx⟩=⟨Ly⟩=0, ~10^14 Hz)
  exact with analytic-vs-numeric agreement at machine precision; C4 (Slater-Koster hopping
  V22=1/16, V2-2=35/48, V20=−5√3/24) exact symbolic match; C5 (~1-lattice-constant relaxation)
  follows analytically from C4.
- No numerical instabilities, no convergence tuning, no data acquisition, no HPC needed.

## The one real discrepancy (resolved)
- **V20 normalization convention.** Our first pass in the normalized complex |2,m⟩ basis gave
  V20 = −0.2551 V_ddσ, which does NOT match the paper's −0.36. Investigation showed the paper's
  −0.36 corresponds to the **unnormalized real** two-center element E(x²−y²,3z²−r²) = −5√3/24 =
  −0.3608. Both are internally consistent; they differ by a 1/√2 normalization factor. We report
  the convention that matches the paper (unnormalized real) and flag the ambiguity as Open Question 1,
  because it materially affects any downstream OHE-magnitude prediction. This is a documentation gap
  in the paper (normalization not stated), not a replication error.

## What is NOT covered (out of scope / not replicable here)
- **No experimental component to reproduce.** The paper is purely theoretical; there is no
  measured data, ARPES, or transport experiment to compare against. The reproduction validates the
  theory's internal consistency, not its experimental correctness.
- **Minimal-model limitations inherited from the paper.** Nearest-neighbor-only Slater-Koster,
  single t2g manifold, no e-ph or disorder. These are the paper's own assumptions; testing whether
  its qualitative conclusions survive realistic DFT hopping / temperature is deferred to the
  open-questions program (Q2, Q3, Q4).

## Residual gaps / what would close them
- A first-principles Wannier tight-binding cross-check (Open Q1, Q2) would resolve the V20
  convention question and test the 1-a relaxation length in a real material. That requires a DFT
  run (uicgpu) and is out of scope for this analytic replication but is the natural follow-on.
