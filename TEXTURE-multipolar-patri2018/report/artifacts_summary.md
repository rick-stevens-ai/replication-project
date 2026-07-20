# Artifacts Summary — Patri et al. (2018) Replication

**System:** Pr(Ti,V,Ir)₂(Al,Zn)₂₀ cage compounds (PrV₂Al₂₀); non-Kramers Γ3 doublet on the diamond lattice, low-energy DOF = quadrupoles O₂₀,O₂₂ + octupole T_xyz.
**Method built:** symmetry-based Landau theory + full strain-tensor minimization (from scratch), reusing `ollie_multipolar_stevens_landau_kernel.py` for single-ion multipole ops & susceptibility.
**Headline tested:** for B‖[111] below T_O, `(ΔL/L)_[111] ∝ (g_O/c44) m h` (linear-in-h, coeff ∝ ferro-octupole m, with hysteresis).

## Verdict: REPLICATED — Coverage 8/10, Agreement 10/10

| # | Claim | Paper | This work | Match |
|---|-------|-------|-----------|-------|
| 1 | `(ΔL/L)_[111] ∝ h¹` | linear-in-h | log-log exponent = 1.0000 | ✅ |
| 2 | coefficient ∝ m (FO) | yes | R² = 1.000 vs m | ✅ |
| 3 | coefficient ∝ g_O/c44 | yes | ratio = 1/√3 (geometric [111]) | ✅ |
| 4 | hysteresis below T_O | yes | loop width = 1.0 (units of spontaneous m) | ✅ |

Supporting (part A): Γ3 doublet orthonormal (overlaps ~1e-16); τ^z from T_xyz maps to ½σ_z with residual 4e-17; octupole susceptibility Curie-like (χ=220 @T=0.3 vs 22 @T=3.0).

## Files (absolute paths)
- Extraction:
  - `/home/stevens/textures-100/corpus/textures-multipolar-patri2018/extraction/marker.md` (INTERIM: pdftotext fallback)
  - `/home/stevens/textures-100/corpus/textures-multipolar-patri2018/extraction/nougat.mmd` (INTERIM: pdftotext fallback)
- Report:
  - `/home/stevens/textures-100/corpus/textures-multipolar-patri2018/report/REPORT.tex`
  - `/home/stevens/textures-100/corpus/textures-multipolar-patri2018/report/open_questions.json`
  - `/home/stevens/textures-100/corpus/textures-multipolar-patri2018/report/workflow.md`
  - `/home/stevens/textures-100/corpus/textures-multipolar-patri2018/report/artifacts_summary.md`
  - `/home/stevens/textures-100/corpus/textures-multipolar-patri2018/report/failure_analysis.md`
- Evidence:
  - `/home/stevens/textures-100/corpus/textures-multipolar-patri2018/report/evidence/patri2018_result.json`
  - `/home/stevens/textures-100/corpus/textures-multipolar-patri2018/report/evidence/patri2018_replicate.py`
  - `/home/stevens/textures-100/corpus/textures-multipolar-patri2018/report/evidence/ollie_multipolar_stevens_landau_kernel.py`

## Provenance
Angular-momentum matrices, Stevens multipole operators (O₂₀,O₂₂,T_xyz), and the fluctuation susceptibility are reused from Ollie's shared `ollie_multipolar_stevens_landau_kernel.py`. Landau/strain minimization and scaling analysis are original.
