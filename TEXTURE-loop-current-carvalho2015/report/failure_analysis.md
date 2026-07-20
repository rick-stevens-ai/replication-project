# Failure analysis — arXiv:1506.07172 replication

Honest log of what broke and how it was fixed. Every fix was applied and
re-verified; no results were fabricated.

## F1. Misclassification (loop-current KAGOME vs cuprate hot-spot)
- **Symptom:** task routed the paper to the kagome tight-binding loop-current
  class and the kagome kernel.
- **Root cause:** the paper is genuinely about *loop-current order* (Varma ΘII),
  so the keyword matched — but the model is a square-lattice CuO2 8-hot-spot
  spin-fermion theory, not kagome.
- **Fix:** flagged in `extraction/marker.md`; did NOT force the kagome kernel;
  reused only its conceptual content (cited). Replicated the paper's real core.
- **Prevention:** "loop-current" is a physics *theme* spanning many lattices;
  always confirm the lattice/model before binding a geometry-specific kernel.

## F2. Grid+refine minimizer too slow (first `hotspot_mft.py`)
- **Symptom:** single default solve did not finish in >100 s.
- **Root cause:** per-k Python loop building 24×24 matrices → millions of
  `eigvalsh` calls across the grid search × BZ × optimizer iterations.
- **Fix:** vectorized the Bloch-kernel construction into a batched
  `(N_k, 24, 24)` stack and a single `np.linalg.eigvalsh` call; added a small-k
  cutoff. Solve time dropped to ~15 ms per free-energy evaluation.
- **Prevention:** always batch eigen-decompositions over the BZ; never loop.

## F3. Runaway order parameters (b → 2.4e5)
- **Symptom:** minimizer drove b to ~240000.
- **Root cause (two layers):**
  (a) wrong QDW stiffness: used b²/J0 with J0 = 3λ²/m_a ≈ 1.2e5, far too weak;
  (b) in `hotspot_mft.py` the two orders gapped *independent* sectors, so each
      grew until only its own (weak) penalty stopped it — no competition, and
      the electronic gain from b was unbounded.
- **Fix (a):** replaced with the **verbatim Eq. 32** coefficient
  (8/3λ²)·⟨D_eff⁻¹⟩·b² (which correctly *decreases* with λ → drives claim 3).
- **Fix (b):** built `hotspot_competition.py` where both orders open
  **anticommuting gaps on the SAME hot-spot fermion**
  (E = ±√(ξ²+gap_R²+gap_b²)), so the condensation gain from one saturates as the
  other grows → genuine competition, matching the paper's det[G⁻¹] = Π D_l^(m)
  shared-spectral-weight mechanism.

## F4. Whole-BZ integral of a uniform gap diverges
- **Symptom:** even the condensation-energy form gave runaway (R_II≈9, b≈16).
- **Root cause:** integrating a k-independent gap over the *entire* BZ with a
  linearized dispersion overcounts condensation gain (unphysical for an
  effective hot-spot theory that lives only near the Fermi surface).
- **Fix:** restricted the condensation integral to the hot-spot patch |ξ|<Λ
  (the effective theory's UV cutoff). Order parameters became finite and O(1).
- **Verified cutoff-independence:** competition signs identical for
  Λ = 0.6, 1.0, 1.5 (corr(R,V_pd) ≈ +1.0, corr(b,V_pd) < 0 throughout).

## Residual limitations (not failures, honest scope)
- Absolute R_II, b magnitudes are calibration-dependent because the full
  Appendix-B/C D_l^(m) closed forms are not present in the extracted PDF text.
  The claims the paper actually makes (trends, competition, ratio ≈ 0.2, M_LC
  order of magnitude) are reproduced and are calibration-robust.
- b assumed k,ε-independent (the paper makes the SAME assumption, §III).
- SSC sector Δ₊ set to 0 (paper also sets Δ₊=0 for the QDW-sector equations).
