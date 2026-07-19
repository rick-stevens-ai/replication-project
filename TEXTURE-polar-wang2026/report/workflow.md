# Workflow — TEXTURE-polar-wang2026

## Goal
Replicate at the mechanism level three claims of Wang, Yang & Chen (arXiv:2604.26100)
about polar-skyrmion superlattices, using a minimal CPU-only phase-field model.

## Steps executed

1. **Read pre-extracted physics.** `report/method_extract.md` already contained
   the model class (TDGL phase-field, interlayer-coupled two-layer), the three
   claims, and the compute profile. No re-derivation from the PDF.

2. **Design a reduced model.**
   - 2 layers × 32×32, 3-component polarization P(x,y).
   - Landau sextic + gradient + uniaxial (K_z) + mean-field depolarization + weak
     interlayer exchange J.
   - Explicit-Euler TDGL, FFT Laplacian, Langevin noise scaling as
     kT_noise = 0.03·T.
   - Skyrmions seeded as Bloch cores at t=0.

3. **Write `code/wang2026_replication.py` FIRST**, then run.
   Total code: ~450 lines, dependencies numpy + scipy + matplotlib (Agg).

4. **Iteration 1 (killed at 13 s).** With initial parameters J=0.35 and a
   loose minimum-filter core detector, the interlayer correlation saturated at
   ~1.0 across ALL temperatures (J too strong, no crossover visible) and the
   "skyrmion count" was inflated to ~75 per layer (spurious minima). Killed at
   the AC-sweep start.

5. **Iteration 2 (114 s, kept).** Fixes:
   - Weakened `J: 0.35 → 0.05` so interlayer alignment becomes an emergent
     T-dependent effect.
   - Replaced minimum-filter core count with NMS on a smoothed
     `|P_xy|·max(-Pz,0)` field so counts fall to a physical ~6-10 per layer.
   - Widened T range (0.30 … 1.60, 10 points, straddling T0=0.9).
   - Longer equilibration (`n_eq=1000`) and per-step sampling (`n_meas=1200`)
     for lower variance on χ.

6. **Save incrementally.** `work/results.json` was overwritten after every
   temperature point in the sweep and after the AC block, so a mid-run kill
   would still leave partial results on disk.

7. **Honest re-scoring after the run.** The auto-scorer initially declared
   Claim 3 PASS because `argmax(|χ'(T)|)` was equal for the three ω's (all
   pinned to the top of the T window). This is a degenerate "pass": the true
   peak likely sits ABOVE the sampled range and its shift with ω is
   unresolved. Manually downgraded Claim 3 to UNRESOLVED and updated the
   verdict from "all three PASS" → "PARTIAL (mechanism-only; Claims 1 & 2
   reproduced, Claim 3 unresolved)".

8. **Artifacts generated:**
   - Code: `code/wang2026_replication.py`
   - Numerical outputs: `work/results.json`, `work/run.log`
   - Figures: `figs/{chi_vs_T,corr_vs_T,chi_ac_vs_T,nsky_vs_T,skyrmion_snapshot}.png`
   - LaTeX report + PDF: `report/REPORT.tex`, `report/REPORT.pdf`
   - Open questions: `report/open_questions.json` (5 entries)
   - This workflow file, plus `artifacts_summary.md` and `failure_analysis.md`
   - `META.json` updated with `status=complete` and the verdict.

## Compute footprint
- CPU-only, single Python process (numpy 2.4.3, scipy 1.18.0).
- Wallclock: 114 s for the full main sweep + AC block.
- Peak memory: <200 MB.

## What was NOT done
- 3D grid, full electrostatic Poisson solve, elastic coupling: OUT OF SCOPE
  for the minimal target.
- No J=0 ablation (would separate correlation-enhanced from Landau soft-mode
  contribution to χ) — flagged in `open_questions.json`.
- No true skyrmion-number density (topological charge) — flagged as
  open question 4.
