# Workflow — Chatterjee, Bultinck, Zaletel 2019 (arXiv:1908.00986) Replication

## Scope
Replicate the **analytic O(3)/CP¹ nonlinear sigma-model skyrmion argument** for
skyrmionic transport in magic-angle twisted bilayer graphene (hBN-aligned) at
filling ν=2. **Explicitly out of scope:** full self-consistent Hartree-Fock of
the continuum flat-band model (the microscopic origin of ρ_s, the anisotropy K,
and the moiré-scale energy units). We take those as effective parameters.

## Steps executed
1. **Read** `report/method_extract.md` for the extracted physics (did NOT
   re-derive). Confirmed: flat bands carry non-zero Chern number → cheap
   charged excitations are skyrmion textures; Zeeman shifts skyrmion energy →
   non-monotonic magnetoresistance R(B).
2. **Wrote** `code/chatterjee2019_replication.py`:
   - Radial winding-1 O(3) skyrmion ansatz `n=(sinθcosφ, sinθsinφ, cosθ)`,
     θ(0)=π (core down), θ(∞)=0 (aligned with easy axis).
   - Free energy `F = 2π ∫ dr r [ (ρ_s/2)(θ'² + sin²θ/r²) + b(1−cosθ) + K(1−cos²θ) ]`.
   - **Log-spaced radial grid** (600 pts, r∈[0.01, 400]) to resolve both the
     core and the long 1/r gradient tail — essential for the BP baseline.
   - Belavin-Polyakov initial profile θ=2·arctan(λ/r); L-BFGS-B relaxation of
     the interior with clamped boundary conditions.
3. **Claim 1** — evaluated the pure O(3) (b=K=0) BP energy at several scales λ
   to verify scale-invariance and recover the 4πρ_s topological baseline.
4. **Claim 2** — swept the Zeeman field b∈[0.002, 0.30] (30 points), relaxing
   the skyrmion at each b (warm-started from the previous relaxed size).
   Constructed the observable activation gap as the min-envelope of the
   skyrmion channel vs a bare-electron channel (Δ_e = E_e0 + c_e·b), and
   computed R(B) ∝ exp(Δ_obs/2T).
5. **Saved** `work/results.json` (all arrays + per-claim expectation /
   reproduced / match / note) and three figures.
6. **Built** the 8 artifacts (this file, REPORT.tex/pdf, open_questions.json,
   artifacts_summary.md, failure_analysis.md, updated META.json).

## Key numerical decisions
- **Factor of 1/2** on the gradient term: the O(3) sigma-model energy density is
  (ρ_s/2)(∂n)². Omitting it gives 8πρ_s and a spurious 2× error in the BP
  baseline (caught and fixed during development — see failure_analysis.md).
- **Log grid** over linear: a linear grid under-resolves the tail and drifts
  the scale-free BP energy.
- numpy 2.x: `np.trapz` → `np.trapezoid` (API change; fixed).

## Reproduce
```
cd TEXTURE-polar-chatterjee2019
python3 code/chatterjee2019_replication.py   # ~80 s, CPU-only, numpy/scipy
```
Outputs: `work/results.json`, `figs/{skyrmion_profile,delta_vs_B,R_vs_B}.png`.
