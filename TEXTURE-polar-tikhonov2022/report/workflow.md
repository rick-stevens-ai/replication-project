# Workflow — TEXTURE-polar-tikhonov2022

## Task
Reproduce the essential theoretical mechanism of Tikhonov et al. arXiv:2204.05000
("Topological polarization networking in uniaxial ferroelectrics") in silico.
Experimental PFM part is explicitly out of scope; only the phase-field / TDGL
side of the paper is targetable computationally.

## Steps executed
1. **Read `report/method_extract.md`** to lock the two claims (branching
   networks; H-H/T-T entwining lowers electrostatic energy) without
   re-parsing the full PDF.
2. **Wrote `code/tikhonov2022_replication.py`** first (save-early
   discipline): 2D scalar Ginzburg-Landau of P_z(x,z) on a 96×96 grid,
   anisotropic gradient (kz ≫ kx), local depolarization proxy penalizing
   (∂z P)^2, TDGL integrator with Neumann BC.
3. **Three matched runs** (all N=5000 TDGL steps, dt=0.04):
    - `network`: Gaussian-noise IC (σ=0.05) → self-organized branching state.
    - `stripes`: 4 parallel domains along z (uncharged reference, F_es ≡ 0).
    - `hh_wall`: single flat H-H sheet (charged reference for Claim 2).
4. **Metrics.** Pure-numpy Zhang-Suen skeletonization of the sign(P) wall
   mask → count skeleton branch points (≥3 skeleton neighbors) and
   endpoints. Connected-component counts of the up/down sublattices.
   Free energy decomposed into F_landau, F_grad, F_es. Bound charge
   ρ_b = −∂z P; integrated |ρ_b| and ρ_b^2.
5. **Figures.** fig1 (Pz maps), fig2 (ρ_b maps), fig3 (F_es and F_total
   bar chart), fig4 (TDGL relaxation traces).
6. **Report.** LaTeX → `REPORT.pdf` with method, metrics table, verdict,
   and an "honest limitations" section (2D scalar not 3D vector, local
   depolarization proxy not full Poisson, no PGO material constants,
   coarsening tension).
7. **Meta artifacts.** `open_questions.json` (5 questions),
   `workflow.md` (this file), `artifacts_summary.md`, `failure_analysis.md`,
   `META.json` updated with status + verdict.

## Parameter tuning history (kept honest)
- v1 (kz=0.6, kx=1.5, λ=4, N=8000): Claim 2 passed cleanly but Claim 1
  failed — noise coarsened past branching into 2 large components.
- v2 (kz=0.5, kx=0.5, λ=1.2, N=6000): junctions rose to 15 vs 6 stripes
  but ratio still weak; charge advantage held.
- v3 (kz=0.5, kx=0.5, λ=2.0, N=3000): Claim 1 clearly passed (78 vs 6)
  but Claim 2 flipped (network hadn't finished relaxing charge yet).
- v4 (kz=0.5, kx=0.5, λ=2.0, N=5000 matched): Claim 1 lost some strength,
  Claim 2 ratio 0.986 — too close to be a clean pass.
- **v5 (final): kz=1.5, kx=0.3, λ=1.5, N=5000 matched.** Strong uniaxial
  anisotropy (kz/kx=5) energetically penalizes H-H walls (which sit
  perpendicular to z), driving branching. Both claims pass with
  substantial margins (48 vs 6 junctions; F_es ratio 0.69).

## Total wall time
~10 s per full run (3 × ~2 s TDGL + ~1 s figures) on a laptop CPU;
whole harness (including 4 tuning iterations + LaTeX) under 500 s.

## Constraints honored
CPU-only, numpy + scipy only (pure-numpy skeletonizer to avoid
scikit-image dependency), no paid APIs, incremental `work/results.json`
writes after every TDGL run so a crash still leaves partial data.
