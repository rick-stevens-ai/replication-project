# Workflow — wang2026 nonlinear magnetic orbital Hall replication

## 1. Read
- Parsed `work/textures-orbital-wang2026.txt` (full paper text) and
  `report/evidence/replication_recipe.json`.
- Extracted target: second-order nonlinear MOHE in PT-AFM CuMnAs, mechanism =
  orbital Berry-curvature dipole (OBD), `chi_dabc = tau * D_dabc`.
- Headline: `chi_zzyy^(O) = -1.3` vs `chi_zzyy^(S) = -0.0087` (h/e Ohm^-1 V^-1)
  at 50 K, tau=1.4 ps; orbital > spin by >2 orders of magnitude; SOC-induced,
  non-perturbative (weak SOC gaps a nodal line near X, <20 meV), T-odd.

## 2. Decide approach (SAVE-EARLY, <6 min, coarse grid)
- DFT+Wannier (paper's method) is out of budget -> build a from-scratch
  **4-band PT-symmetric AFM nodal-line tight-binding surrogate**.
- Reuse the itinerant-L_z + Kubo/velocity machinery from the shared kernel
  `gobel2024_sd_skyrmion_kubo_Lz_kernel.py`, generalized to k-space multiband +
  the SECOND-ORDER (Berry-curvature-dipole) response.

## 3. Build & run (`work/wang2026_replication.py`)
- H(k) = nodal-line term (rho_z, rho_y) + Neel AFM (J rho_z sigma_z) + SOC
  (lambda rho_x sigma). Velocities by finite difference.
- L_z via paper Eq.(3); j^z_a = 1/2{v_a, L^z}; spin analog with S^z.
- Omega^{z,n}_{zy} (orbital Berry curvature) and D_zzyy = sum_n int Omega * df0/dk_y
  on a coarse 18^3 grid at finite T; chi = tau*D.
- **Pitfall hit & fixed:** initial mu=0 sat in a global gap (empty Fermi surface)
  -> results were pure numerical noise (~1e-22). Probed the spectrum, moved
  mu=1.0 onto the nodal-line-derived Fermi surface. Also raised smearing
  T=0.02->0.08 and unified all grids to Nk=18 so the FS integral converged, and
  fixed a sign-flip guard threshold (1e-12 -> 1e-30) that was larger than the
  model-unit magnitudes.
- Runtime ~16 s.

## 4. Measurements
- **main:** ratio orbital/spin ~6.0e3 (paper ~150) at lambda=0.12.
- **soc_scan:** |D^(O)| rises as SOC weakens (slope -1.1) -> non-perturbative.
- **soc_zero:** D^(O) -> 3e-22 (noise), D^(S)=0 -> SOC required.
- **T_odd:** J -> -J flips the sign of D^(O).

## 5. Compare, score, package
- SAVE-EARLY to `work/wang2026_result.json`.
- Scored honestly (see `artifacts_summary.md`, `failure_analysis.md`).
- Built 8 artifacts; copied result JSON + code to `report/evidence/`.

## Tools
- Runner: `/home/stevens/comfyui-env/bin/python` (numpy 2.3.5, scipy 1.17.0).
- Extraction: `pdftotext` (interim, marker/nougat not run in budget).
