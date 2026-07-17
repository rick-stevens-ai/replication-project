# Failure Analysis — feng2026

**Verdict:** PARTIAL. One claim cleanly reproduced (C1), two method-limited (C2, C3), three out of scope (C4–C6).

## 1. What worked
- **C1 — d-wave altermagnet band symmetry (clean reproduction).** The 4-band model H0+H^c+H^f with the paper's exact parameters yields a SOC-free spin splitting of **0.365 eV on the x-axis** and **exactly 0.0 on the BZ diagonal** (kx=ky). This is the defining d-wave altermagnet signature (spin splitting ∝ cos kx − cos ky, nodal along ⟨11⟩). Parameter-exact, convention-independent, no fitting.

## 2. What did not reproduce — and why (honest diagnosis)

### C2 — MOHE conductivity σ^{Lz}_xy came out ~1e-22 (numerical zero)
- **Not a refutation of the paper.** It is a limitation of the simplified transport formula we implemented.
- **Root cause:** we used a naive T=0 intraband Drude-like sum, `σ ∝ Σ_{n occ} ⟨j^{Lz}_x⟩_n ⟨v_y⟩_n`. For fully-occupied Bloch bands integrated over the full BZ, the product of the orbital current and the band group velocity cancels by k-space (time-reversal-like) symmetry, giving ≈0.
- **The paper's Eq.9** is a second-order / nonlinear magneto-response that carries (i) a proper Fermi-surface weighting (∂f0/∂k, i.e. partial occupation matters) and (ii) the interband orbital-moment normalization in the ieħ²/4μ_B form. Our linear filled-band coding captures neither, so the finite response it should produce is washed out.
- **Evidence it is a method issue, not convergence:** the ~1e-22 value is stable across 60² and 90² k-meshes and across both μ regimes — a genuine cancellation, not undersampling.

### C3 — symmetry-allowed vs forbidden tensor components not numerically resolved
- Same underlying cause: with both the allowed (xy) and forbidden (xx) components sitting at numerical zero, the numerical allowed-set could not be extracted. The allowed set is nonetheless clear analytically from the spin-Laue group 2 4/1m2m1m — it just was not demonstrated numerically here.

## 3. Out of scope
- **C4/C5/C6 (CrSb, FeSb2 first-principles MOHE).** Require Ref[50] Supplemental-Material DFT parameters (plane-wave cutoff, U, k-mesh) plus a VASP/QE + Wannier90 pipeline and T-dependent transport with experimental τ (CrSb 15 fs, FeSb2 2.5 fs). The SM parameters are not in the extracted text and no DFT stack was available (uicgpu has only ASE). Deferred as a stretch goal.

## 4. What a fuller reproduction needs
1. Implement Eq.9 as the correct nonlinear/second-order Kubo response with ∂f0/∂k weighting and the ieħ²/4μ_B interband orbital-moment normalization → should yield finite σ^{Lz}_xy.
2. Sweep all (a,b,c) tensor indices to confirm the spin-Laue-group allowed-set numerically.
3. Disentangle λ_c (spin-conserving) vs λ_f (spin-flip) SOC contributions.
4. For C4–C6: obtain Ref[50] SM params and run the CrSb/FeSb2 DFT+Wannier+transport pipeline.
